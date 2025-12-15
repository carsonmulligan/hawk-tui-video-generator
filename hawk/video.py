"""FFmpeg video assembly for TikTok content."""

import subprocess
import shutil
import textwrap
from pathlib import Path
from datetime import datetime
from typing import Optional

from hawk.config import Project, TIKTOK_WIDTH, TIKTOK_HEIGHT


def check_ffmpeg() -> bool:
    """Check if FFmpeg is installed."""
    return shutil.which("ffmpeg") is not None


def wrap_text_for_video(text: str, max_chars: int = 35) -> str:
    """
    Wrap text to fit within video frame.
    FFmpeg drawtext doesn't auto-wrap, so we insert newlines.
    """
    # Use textwrap to break into lines
    lines = textwrap.wrap(text, width=max_chars)
    # Limit to 3 lines max for readability
    if len(lines) > 3:
        lines = lines[:3]
        lines[2] = lines[2][:max_chars-3] + "..."
    return "\n".join(lines)


def create_slideshow(
    project: Project,
    images: list[Path],
    output_name: Optional[str] = None,
    duration_per_image: float = 3.0,
    audio_path: Optional[Path] = None,
    captions: Optional[list[str]] = None,
) -> Path:
    """
    Create a TikTok-format video from images.

    Args:
        project: The project to save to
        images: List of image paths to include
        output_name: Optional custom output filename
        duration_per_image: Seconds to show each image
        audio_path: Optional audio file to add
        captions: Optional list of captions (one per image)

    Returns:
        Path to the created video file
    """
    if not check_ffmpeg():
        raise RuntimeError("FFmpeg not found. Install with: brew install ffmpeg")

    if not images:
        raise ValueError("No images provided")

    project.ensure_dirs()

    # Generate output filename
    if output_name:
        output_file = project.exports_dir / f"{output_name}.mp4"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = project.exports_dir / f"tiktok_{timestamp}.mp4"

    # Build filter complex for slideshow
    inputs = []
    filter_parts = []

    for i, img in enumerate(images):
        inputs.extend(["-loop", "1", "-t", str(duration_per_image), "-i", str(img)])

        # Scale and pad each image to TikTok dimensions
        filter_parts.append(
            f"[{i}:v]scale={TIKTOK_WIDTH}:{TIKTOK_HEIGHT}:"
            f"force_original_aspect_ratio=decrease,"
            f"pad={TIKTOK_WIDTH}:{TIKTOK_HEIGHT}:(ow-iw)/2:(oh-ih)/2:black,"
            f"setsar=1[v{i}]"
        )

    # Concatenate all video streams
    concat_inputs = "".join(f"[v{i}]" for i in range(len(images)))
    filter_parts.append(f"{concat_inputs}concat=n={len(images)}:v=1:a=0[outv]")

    # Add captions if provided
    output_stream = "[outv]"
    if captions and any(c.strip() for c in captions):
        # Build drawtext filters for each caption
        drawtext_filters = []
        for i, caption in enumerate(captions[:len(images)]):
            if not caption or not caption.strip():
                continue
            
            # Wrap long text to multiple lines
            wrapped_caption = wrap_text_for_video(caption.strip(), max_chars=30)
            
            # Escape special characters for FFmpeg drawtext
            safe_caption = (
                wrapped_caption
                .replace("\\", "\\\\")
                .replace("'", "'\\''")
                .replace(":", "\\:")
                .replace("%", "\\%")
            )
            start_time = i * duration_per_image
            end_time = (i + 1) * duration_per_image
            
            # Count lines for vertical positioning adjustment
            line_count = safe_caption.count("\n") + 1
            # Adjust y position based on line count (move up for more lines)
            y_offset = 0.85 - (line_count * 0.04)
            
            # Position: centered horizontally, bottom area adjusted for line count
            drawtext_filters.append(
                f"drawtext=text='{safe_caption}':"
                f"fontsize=48:"
                f"fontcolor=white:"
                f"borderw=3:"
                f"bordercolor=black:"
                f"x=(w-text_w)/2:"
                f"y=h*{y_offset}:"
                f"line_spacing=8:"
                f"enable='between(t\\,{start_time}\\,{end_time})'"
            )
        
        if drawtext_filters:
            # Chain all drawtext filters together
            caption_filter = "[outv]" + ",".join(drawtext_filters) + "[final]"
            filter_parts.append(caption_filter)
            output_stream = "[final]"

    # Build the FFmpeg command
    cmd = ["ffmpeg", "-y"]
    cmd.extend(inputs)

    if audio_path and audio_path.exists():
        cmd.extend(["-i", str(audio_path)])

    cmd.extend([
        "-filter_complex", ";".join(filter_parts),
        "-map", output_stream,
    ])

    if audio_path and audio_path.exists():
        cmd.extend(["-map", f"{len(images)}:a", "-c:a", "aac", "-shortest"])

    cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(output_file)
    ])

    # Run FFmpeg
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr}")

    return output_file


def add_audio_to_video(
    video_path: Path,
    audio_path: Path,
    output_path: Optional[Path] = None,
    loop_audio: bool = True,
) -> Path:
    """Add or replace audio in a video file."""
    if output_path is None:
        output_path = video_path.with_stem(f"{video_path.stem}_audio")

    cmd = ["ffmpeg", "-y", "-i", str(video_path)]

    if loop_audio:
        cmd.extend(["-stream_loop", "-1"])

    cmd.extend([
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_path)
    ])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr}")

    return output_path


def get_video_duration(video_path: Path) -> float:
    """Get duration of a video in seconds."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def get_project_exports(project: Project) -> list[Path]:
    """Get all exported videos in a project."""
    project.ensure_dirs()
    return sorted(
        project.exports_dir.glob("*.mp4"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )


def get_project_audio(project: Project) -> list[Path]:
    """Get all audio files in a project."""
    project.ensure_dirs()
    extensions = {".mp3", ".wav", ".m4a", ".aac"}
    return sorted(
        [f for f in project.audio_dir.iterdir() if f.suffix.lower() in extensions],
        key=lambda x: x.name
    )
