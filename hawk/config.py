"""Project and model configuration."""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Load .env file (for backwards compatibility)
load_dotenv()

# Also load from ~/.config/hawk/config.toml if it exists
_CONFIG_FILE = Path.home() / ".config" / "hawk" / "config.toml"
if _CONFIG_FILE.exists():
    try:
        with open(_CONFIG_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    # Only set if not already in environment (env vars take precedence)
                    if key not in os.environ:
                        os.environ[key] = value
    except Exception:
        pass

# Base paths
BASE_DIR = Path(__file__).parent.parent
# Allow override via config for PyPI users who don't clone the repo
_custom_content = os.getenv("CONTENT_DIR")
if _custom_content:
    CONTENT_DIR = Path(_custom_content)
else:
    CONTENT_DIR = BASE_DIR / "content"


@dataclass
class Project:
    """A content project with its Replicate model."""
    name: str
    slug: str
    model: str
    trigger: str
    description: str

    @property
    def images_dir(self) -> Path:
        return CONTENT_DIR / self.slug / "images"

    @property
    def audio_dir(self) -> Path:
        return CONTENT_DIR / self.slug / "audio"

    @property
    def exports_dir(self) -> Path:
        return CONTENT_DIR / self.slug / "exports"

    def ensure_dirs(self):
        """Create project directories if they don't exist."""
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)


# Your 3 custom Replicate models
PROJECTS = {
    "wedding-vision": Project(
        name="Wedding Vision",
        slug="wedding-vision",
        model="digital-prairie-labs/spring-wedding",
        trigger="TOK",
        description="Spring wedding florals and bouquets",
    ),
    "latin-bible": Project(
        name="Latin Bible",
        slug="latin-bible",
        model="digital-prairie-labs/catholic-prayers-v2.1",
        trigger="",  # Uses prayer text directly
        description="Catholic prayers and religious imagery",
    ),
    "dxp-labs": Project(
        name="DXP Labs",
        slug="dxp-labs",
        model="digital-prairie-labs/futuristic",
        trigger="TOK",
        description="Futuristic sci-fi landscapes and spaceships",
    ),
}


# TikTok video settings
TIKTOK_WIDTH = 1080
TIKTOK_HEIGHT = 1920
TIKTOK_ASPECT = "9:16"

# Replicate settings
REPLICATE_DEFAULT_PARAMS = {
    "model": "dev",
    "go_fast": False,
    "lora_scale": 1,
    "megapixels": "1",
    "num_outputs": 1,
    "aspect_ratio": TIKTOK_ASPECT,
    "output_format": "png",
    "guidance_scale": 3,
    "output_quality": 90,
    "prompt_strength": 0.8,
    "extra_lora_scale": 1,
    "num_inference_steps": 28,
}

# API Keys (from .env)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Ollama settings (for prompt enhancement)
USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() == "true"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

# Local image generation settings (Hugging Face Diffusers)
USE_LOCAL_IMAGE_GEN = os.getenv("USE_LOCAL_IMAGE_GEN", "false").lower() == "true"
# Model options:
#   black-forest-labs/FLUX.1-schnell - Best quality, 4 steps, ~23GB RAM
#   stabilityai/sdxl-turbo - Fast, 8-15 steps, ~6GB RAM
#   stabilityai/stable-diffusion-xl-base-1.0 - Standard, 20-30 steps, ~6GB RAM
SD_MODEL = os.getenv("SD_MODEL", "stabilityai/sdxl-turbo")
SD_INFERENCE_STEPS = int(os.getenv("SD_INFERENCE_STEPS", "15"))  # 4 for Flux, 8-15 for turbo, 20-30 for standard
SD_GUIDANCE_SCALE = float(os.getenv("SD_GUIDANCE_SCALE", "0.0"))  # 0.0 for Flux/turbo, 7.5 for standard

# Debug/verbose mode
VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"
LOG_FILE = BASE_DIR / "hawk.log"


# Color palette (CEO CLI style)
COLORS = {
    "bg": "#1a1d23",
    "fg": "#e0e0e0",
    "accent": "#c9a227",      # Gold for highlights
    "border": "#4a5f4a",       # Green borders
    "dim": "#6b7280",
    "success": "#22c55e",
    "error": "#ef4444",
}
