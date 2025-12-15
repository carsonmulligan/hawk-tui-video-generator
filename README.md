![HawkTUI Splash Screen](docs/splash.png)

i built this to give the claude code agent sdk access to my replicate fine tunes (https://replicate.com/digital-prairie-labs). i use these fine tunes to create short form content as marketing for ios apps on tik tok and instagram. after using claude code for a while i have fallen in love with the terminal ui (tui) so here we are. 

ai slop readme below :) 

# HawkTUI

A terminal-based TikTok video creator with AI image generation. Generate images using custom Replicate models and assemble them into 9:16 TikTok-format videos with FFmpeg.

[![PyPI version](https://badge.fury.io/py/hawk-tui-video.svg)](https://pypi.org/project/hawk-tui-video/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)



![HawkTUI Main Interface](docs/app.png)

## Features

- **AI Image Generation** - Generate images using custom Replicate fine-tuned models
- **TikTok Video Creation** - Automatically assemble images into 9:16 vertical videos
- **Multiple Projects** - Switch between different Replicate models/styles
- **Terminal UI** - Beautiful TUI built with Textual
- **Keyboard-Driven** - Fast workflow with intuitive shortcuts

## Installation

```bash
pip install hawk-tui-video
```

### Requirements

- Python 3.11+
- FFmpeg (for video creation)

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## Quick Start

1. **Get a Replicate API token** from [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)

2. **Create a `.env` file** in your working directory:

```bash
REPLICATE_API_TOKEN=r8_your_token_here
```

3. **Run HawkTUI**:

```bash
hawktui
```

## Usage

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑/↓` or `j/k` | Navigate lists |
| `Tab` | Switch between panels |
| `Enter` | Select project / Open image / Submit prompt |
| `Space` | Toggle image selection |
| `a` | Select all images |
| `v` | Create video from selected images |
| `b` | Browse project folder in Finder |
| `d` | Delete selected images |
| `1/2/3` | Quick switch projects |
| `Esc` | Clear selection / Cancel |
| `q` | Quit |

### Workflow

1. **Select a project** using arrow keys or number shortcuts
2. **Type a prompt** in the input field at the bottom
3. **Press Enter** to generate an image via Replicate
4. **Select images** using Space to toggle selection
5. **Press `v`** to create a TikTok video from selected images

## Configuration

### Adding Your Own Models

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
├── video.py            # FFmpeg video assembly
├── screens/
│   └── splash.py       # Splash screen
└── main.py             # Entry point

content/                # Generated content (created automatically)
├── {project}/
│   ├── images/         # Generated images
│   ├── audio/          # Audio files for videos
│   └── exports/        # Final TikTok videos
```

## Development

```bash
# Clone the repo
git clone https://github.com/carsonmulligan/hawk-tui-video-generator.git
cd hawk-tui-video-generator

# Install in development mode
pip install -e .

# Run
python -m hawk.main
```

## Tech Stack

- **[Textual](https://textual.textualize.io/)** - TUI framework
- **[Rich](https://rich.readthedocs.io/)** - Terminal formatting
- **[Replicate](https://replicate.com/)** - AI model inference
- **[FFmpeg](https://ffmpeg.org/)** - Video processing

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Author

**Carson Mulligan** - [GitHub](https://github.com/carsonmulligan)

---

Built with [Claude Code](https://claude.ai/code)
