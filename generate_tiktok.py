#!/usr/bin/env python3
"""Generate 5 futuristic images and create a TikTok video."""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add hawk to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

import replicate
import httpx

# Config
MODEL = "digital-prairie-labs/futuristic:27415b8d4f84571b5ae8828da7da1cae63bdcd9fa54ccbc723bfdeb984cc128d"
TRIGGER = "TOK"
OUTPUT_DIR = Path("content/dxp-albs/images")
EXPORTS_DIR = Path("content/dxp-albs/exports")

# Ensure dirs exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 5 variations - always "cloaked wanderer + descriptor", Egyptian twists, NO sky references
PROMPTS = [
    "TOK cloaked wanderer bearing pharaoh mask, void horizon",
    "TOK cloaked wanderer with ankh staff, pyramid silhouette",
    "TOK cloaked wanderer adorned in gold, sphinx guardian",
    "TOK cloaked wanderer hieroglyph-robed, obsidian temple",
    "TOK cloaked wanderer scarab-armored, desert ruins",
]

def generate_image(prompt: str, index: int) -> Path:
    """Generate a single image."""
    print(f"[{index+1}/5] Generating: {prompt}")

    output = replicate.run(
        MODEL,
        input={
            "model": "dev",
            "prompt": prompt,
            "go_fast": False,
            "lora_scale": 1,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": "9:16",  # TikTok format
            "output_format": "png",
            "guidance_scale": 3,
            "output_quality": 90,
            "num_inference_steps": 28,
        }
    )

    # Download
    url = output[0] if isinstance(output, list) else output
    response = httpx.get(str(url), follow_redirects=True)
    response.raise_for_status()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wanderer_{timestamp}_{index+1}.png"
    filepath = OUTPUT_DIR / filename

    with open(filepath, "wb") as f:
        f.write(response.content)

    print(f"    Saved: {filepath}")
    return filepath


def create_video(images: list[Path]) -> Path:
    """Create TikTok video from images using FFmpeg."""
    import subprocess

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = EXPORTS_DIR / f"wanderer_tiktok_{timestamp}.mp4"

    # Build FFmpeg command
    inputs = []
    filter_parts = []

    duration = 3.0  # seconds per image

    for i, img in enumerate(images):
        inputs.extend(["-loop", "1", "-t", str(duration), "-i", str(img)])
        filter_parts.append(
            f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1[v{i}]"
        )

    # Concatenate
    concat_inputs = "".join(f"[v{i}]" for i in range(len(images)))
    filter_parts.append(f"{concat_inputs}concat=n={len(images)}:v=1:a=0[outv]")

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[outv]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(output_file)
    ]

    print(f"\nCreating video...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr}")
        raise RuntimeError("Video creation failed")

    print(f"Video saved: {output_file}")
    return output_file


def main():
    print("=" * 60)
    print("Generating 5 cloaked wanderer images (Egyptian twists)...")
    print("=" * 60)

    images = []
    for i, prompt in enumerate(PROMPTS):
        path = generate_image(prompt, i)
        images.append(path)

    print("\n" + "=" * 60)
    print("Creating TikTok video...")
    print("=" * 60)

    video_path = create_video(images)

    print("\n" + "=" * 60)
    print("DONE!")
    print(f"Images: {OUTPUT_DIR}")
    print(f"Video: {video_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
