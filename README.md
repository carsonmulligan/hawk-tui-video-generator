![HawkTUI Splash Screen](docs/splash.png)

i built this to give the claude code agent sdk access to my replicate fine tunes (https://replicate.com/digital-prairie-labs). i use these fine tunes to create short form content as marketing for ios apps on tik tok and instagram. after using claude code for a while i have fallen in love with the terminal ui (tui) so here we are. 

ai slop readme below :) 

# HawkTUI

A terminal-based TikTok video creator with AI image generation. Generate images using Replicate API, **local Stable Diffusion/Flux models**, or enhance prompts with **local Ollama LLMs**. Assemble images into 9:16 TikTok-format videos with FFmpeg.

[![PyPI version](https://badge.fury.io/py/hawk-tui-video.svg)](https://pypi.org/project/hawk-tui-video/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)



![HawkTUI Main Interface](docs/app.png)

## Features

- **AI Image Generation** - Generate images using:
  - **Replicate API** - Cloud-based with custom fine-tuned models
  - **Local Diffusers** - Run Flux, SDXL-Turbo, SD locally on your GPU/MPS
- **Ollama Integration** - Enhance prompts with local LLMs before generation
- **TikTok Video Creation** - Automatically assemble images into 9:16 vertical videos
- **Multiple Projects** - Switch between different models/styles
- **Terminal UI** - Beautiful TUI built with Textual
- **Keyboard-Driven** - Fast workflow with intuitive shortcuts
- **Progress Tracking** - Real-time progress bar during generation

## Installation

```bash
pip install hawk-tui-video
```

> **Note:** This installs PyTorch and Diffusers (~2GB+) for local image generation.

### Requirements

- Python 3.11+
- FFmpeg (for video creation)
- [Ollama](https://ollama.ai/) (optional, for prompt enhancement)
- [chafa](https://hpjansson.org/chafa/) (optional, for in-terminal image preview)

```bash
# macOS
brew install ffmpeg
brew install ollama  # optional, for prompt enhancement
brew install chafa   # optional, for in-terminal image preview

# Ubuntu/Debian
sudo apt install ffmpeg
# For Ollama: https://ollama.ai/download

# Windows
# Download from https://ffmpeg.org/download.html
# Ollama: https://ollama.ai/download
```

## Quick Start

### Option 1: Replicate Cloud (Default)

1. **Get a Replicate API token** from [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)

2. **Create a `.env` file**:

```bash
REPLICATE_API_TOKEN=r8_your_token_here
```

3. **Run HawkTUI**:

```bash
hawktui
```

### Option 2: Local Generation (Flux/SDXL)

1. **Create a `.env` file**:

```bash
# Enable local generation
USE_LOCAL_IMAGE_GEN=true

# Choose your model
SD_MODEL=black-forest-labs/FLUX.1-schnell  # Best quality (needs ~23GB RAM)
# SD_MODEL=stabilityai/sdxl-turbo          # Faster, less RAM (~6GB)

# Optimal settings for Flux
SD_INFERENCE_STEPS=4
SD_GUIDANCE_SCALE=0.0

# Optional: Ollama prompt enhancement
USE_OLLAMA=true
OLLAMA_MODEL=llama3.2:latest
```

2. **Run HawkTUI**:

```bash
hawktui
```

The model will download on first run (~6-23GB depending on model).

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REPLICATE_API_TOKEN` | - | Replicate API token (for cloud generation) |
| `USE_LOCAL_IMAGE_GEN` | `false` | Enable local Diffusers generation |
| `SD_MODEL` | `stabilityai/stable-diffusion-xl-base-1.0` | HuggingFace model ID |
| `SD_INFERENCE_STEPS` | `15` | Denoising steps (4 for Flux, 15+ for SDXL) |
| `SD_GUIDANCE_SCALE` | `0.0` | CFG scale (0.0 for Flux/Turbo, 7.5 for standard) |
| `USE_OLLAMA` | `false` | Enable Ollama prompt enhancement |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.2:latest` | Ollama model for prompt enhancement |
| `VERBOSE` | `false` | Enable verbose logging |

### Recommended Model Settings

| Model | Steps | Guidance | RAM | Speed |
|-------|-------|----------|-----|-------|
| `black-forest-labs/FLUX.1-schnell` | 4 | 0.0 | ~23GB | Fast |
| `stabilityai/sdxl-turbo` | 8-15 | 0.0-1.5 | ~6GB | Fast |
| `stabilityai/stable-diffusion-xl-base-1.0` | 20-30 | 7.5 | ~6GB | Slow |
| `runwayml/stable-diffusion-v1-5` | 20-30 | 7.5 | ~4GB | Medium |

## Usage

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑/↓` or `j/k` | Navigate lists |
| `Tab` | Switch between panels |
| `Enter` | Select project / Open image / Submit prompt |
| `Space` | Toggle image selection |
| `a` | Select all images |
| `p` | Preview image (chafa in-terminal or Quick Look) |
| `v` | Create video from selected images (with captions) |
| `b` | Browse project folder in Finder |
| `d` | Delete selected images |
| `l` | View logs (for debugging) |
| `1/2/3` | Quick switch projects |
| `Esc` | Clear selection / Cancel |
| `q` | Quit |

### Workflow

1. **Select a project** using arrow keys or number shortcuts
2. **Type a prompt** in the input field at the bottom
3. **Press Enter** to generate an image
4. **Watch progress** in the status bar (shows step-by-step progress)
5. **Select images** using Space to toggle selection
6. **Press `v`** to create a TikTok video from selected images

### Status Bar

The status bar shows real-time information:
- Current backend: `Local (MPS)` or `Replicate`
- Ollama status: `Ollama:llama3.2:latest`
- Generation progress: `[████░░░░░░] Step 3/8`

## Adding Your Own Models

Edit `hawk/config.py` to add your Replicate models:

```python
PROJECTS = {
    "my-style": Project(
        name="My Style",
        slug="my-style",
        model="your-username/your-model",
        trigger="TOK",  # Trigger word if your model uses one
        description="Description of your model",
    ),
}
```

### Default Models

The app comes pre-configured with three example models from Digital Prairie Labs:

| Project | Model | Style |
|---------|-------|-------|
| Wedding Vision | `digital-prairie-labs/spring-wedding` | Wedding florals |
| Latin Bible | `digital-prairie-labs/catholic-prayers-v2.1` | Religious imagery |
| DXP Labs | `digital-prairie-labs/futuristic` | Sci-fi landscapes |

## Project Structure

```
hawk/
├── app.py              # Main Textual TUI application
├── config.py           # Project and model configuration
├── replicate_client.py # Replicate API wrapper
├── local_image_gen.py  # Local Diffusers generation
├── ollama_client.py    # Ollama LLM integration
├── image_generator.py  # Abstraction layer for backends
├── logger.py           # Logging utilities
├── video.py            # FFmpeg video assembly
├── screens/
│   └── splash.py       # Splash screen
└── main.py             # Entry point

content/                # Generated content (created automatically)
├── {project}/
│   ├── images/         # Generated images
│   ├── audio/          # Audio files for videos
│   └── exports/        # Final TikTok videos

hawk.log                # Debug log file
```

## Development

```bash
# Clone the repo
git clone https://github.com/carsonmulligan/hawk-tui-video-generator.git
cd hawk-tui-video-generator

# Install with uv (recommended)
uv sync

# Run
uv run hawk

# Or install in development mode with pip
pip install -e .
python -m hawk.main
```

## Troubleshooting

### Token limit warnings
If you see "Token indices sequence length is longer than the specified maximum", the prompt is being truncated. This is handled automatically - prompts are limited to 77 tokens for CLIP-based models.

### Model loading fails on macOS
Set environment variables before running:
```bash
TOKENIZERS_PARALLELISM=false uv run hawk
```

### Out of memory
Try a smaller model:
```bash
SD_MODEL=runwayml/stable-diffusion-v1-5
```

### View logs
Press `l` in the TUI or check `hawk.log` in the project directory.

## Tech Stack

- **[Textual](https://textual.textualize.io/)** - TUI framework
- **[Rich](https://rich.readthedocs.io/)** - Terminal formatting
- **[Replicate](https://replicate.com/)** - Cloud AI model inference
- **[Diffusers](https://huggingface.co/docs/diffusers)** - Local image generation
- **[Ollama](https://ollama.ai/)** - Local LLM inference
- **[FFmpeg](https://ffmpeg.org/)** - Video processing

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Author

**Carson Mulligan** - [GitHub](https://github.com/carsonmulligan)

---

Built with [Claude Code](https://claude.ai/code)
