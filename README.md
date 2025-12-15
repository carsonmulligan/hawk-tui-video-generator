# HawkTUI

Terminal-based TikTok video creator with AI image generation.

Generate images using custom Replicate models and assemble them into 9:16 TikTok videos with FFmpeg.

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
```

## Setup

1. Get your API token from [Replicate](https://replicate.com/account/api-tokens)

2. Create a `.env` file in your project directory:

```bash
REPLICATE_API_TOKEN=r8_your_token_here
```

3. Configure your models in `hawk/config.py`

## Usage

```bash
# Run the TUI
hawktui

# Or
hawk
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑/↓` | Navigate |
| `Tab` | Switch panels |
| `Enter` | Select/Open |
| `Space` | Toggle image selection |
| `a` | Select all images |
| `v` | Create video |
| `b` | Browse folder |
| `d` | Delete selected |
| `1/2/3` | Switch projects |
| `q` | Quit |

## How It Works

1. **Select a project** - Choose from your configured Replicate models
2. **Enter a prompt** - Type your image generation prompt
3. **Generate** - Press Enter to generate images via Replicate
4. **Select images** - Use Space to select images for your video
5. **Create video** - Press `v` to assemble a TikTok-format video

## Configuration

Edit `hawk/config.py` to add your own Replicate models:

```python
PROJECTS = {
    "my-project": Project(
        name="My Project",
        slug="my-project",
        model="username/model-name",
        trigger="TOK",  # Optional trigger word
        description="Description",
    ),
}
```

## License

MIT
