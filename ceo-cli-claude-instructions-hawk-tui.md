# HAWK TUI v4 — CEO Agent CLI

> **Domain**: hawktui.xyz  
> **Author**: Carson Mulligan  
> **Version**: 4.0  
> **Inspiration**: [Paul Klein IV's CEO CLI](https://x.com/pk_iv) — Browserbase

---

## DESIGN REFERENCE

The UI should feel like Paul Klein's CEO CLI v4:

### Visual Language
- **Dark theme** with muted blue-gray background (`#1a1d23`)
- **Yellow/gold accent** for menu items and highlights (`#c9a227`)
- **Green border boxes** for panels and dialogs (`#4a5f4a`)
- **PS2-style loading screen** with pixelated retro font
- **Monospace throughout** — feels like a real terminal

### Layout Pattern
```
┌─────────────────────────────────────┬─────────────────────┐
│                                     │        MENU         │
│           MESSAGE                   │                     │
│                                     │  [v] View Full      │
│  Source: GMAIL                      │  [a] AI Prompt      │
│  From: sabina@company.com           │  [r] Reply          │
│  Subject: Q1 Meeting                │  [f] Forward        │
│                                     │  [t] Add to Todos   │
│  Hi Paul,                           │  [m] Monitor        │
│                                     │ ▶[d] Done/Archive   │
│  Should we find time to meet        │  [x] Auto-Archive   │
│  in Q1? Let us know...              │  [c] Cruise Mode    │
│                                     │  [s] Skip           │
│  Link: https://mail.google.com/...  │  [q] Quit           │
│                                     │                     │
│                                     │  ↑/↓ arrows, Enter  │
│                                     │  or type a letter   │
└─────────────────────────────────────┴─────────────────────┘
```

### AI Reasoning Panel
```
┌───────────────────────────────────────────────────────────┐
│  Action: REPLY                                            │
│                                                           │
│  Reasoning:                                               │
│  Checked Paul's January calendar.                         │
│  The calendar is busy but has                             │
│  several 30-60+ minute windows                            │
│  available, with the best                                 │
│  availability in the week of Jan 6.                       │
│                                                           │
│  Draft:                                                   │
│  Hey Sabina,                                              │
│                                                           │
│  Yes, let's do it. I have some ti...                      │
│                                                           │
│  Paul                                                     │
└───────────────────────────────────────────────────────────┘
```

### Human-in-the-Loop Confirmation
```
Execute this?
[v] View Full
[y] Yes
[e] Edit
[f] Feedback
[n] No
```

### Key UX Principles
1. **Keyboard-first** — single letter shortcuts for everything
2. **AI transparency** — show reasoning before action
3. **Human approval** — never auto-send, always confirm
4. **Cruise mode** — rapid-fire review for inbox zero
5. **Context linking** — direct Gmail/Calendar links

---

## PROJECT OVERVIEW

Hawk TUI is a terminal-based CEO agent powered by the **Claude Agent SDK**. It provides an intelligent CLI assistant with rich integrations for productivity, content creation, and business automation.

### Core Philosophy
- **"The CEO in your terminal"** — a single command-line interface for managing email, calendar, CRM, data, tasks, and creative content
- PS2-inspired aesthetic with beautiful loading animations
- Modular skill system for extensibility
- MCP (Model Context Protocol) native architecture

---

## TECH STACK

| Layer | Technology |
|-------|------------|
| **Agent Runtime** | Claude Agent SDK (Python) |
| **TUI Framework** | Textual + Rich |
| **Image Generation** | Replicate (FLUX models) |
| **Video Creation** | FFmpeg |
| **Package Manager** | uv (recommended) or pip |
| **Python Version** | 3.10+ |

---

## DIRECTORY STRUCTURE

```
hawktui/
├── hawk/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── app.py                  # Textual TUI application
│   ├── agent.py                # Claude Agent SDK wrapper
│   ├── config.py               # Configuration management
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── loading.py          # PS2-style loading animation
│   │   ├── theme.py            # Color schemes and styling
│   │   ├── widgets/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py         # Chat interface widget
│   │   │   ├── status.py       # Status bar widget
│   │   │   └── sidebar.py      # Skills sidebar
│   │   └── screens/
│   │       ├── __init__.py
│   │       ├── home.py
│   │       ├── email.py
│   │       └── calendar.py
│   │
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── base.py             # Base skill class
│   │   ├── email/
│   │   │   ├── __init__.py
│   │   │   ├── gmail.py        # Gmail API integration
│   │   │   └── SKILL.md
│   │   ├── calendar/
│   │   │   ├── __init__.py
│   │   │   ├── gcal.py         # Google Calendar API
│   │   │   └── SKILL.md
│   │   ├── crm/
│   │   │   ├── __init__.py
│   │   │   ├── hubspot.py      # HubSpot API
│   │   │   └── SKILL.md
│   │   ├── data/
│   │   │   ├── __init__.py
│   │   │   ├── snowflake.py    # Snowflake connector
│   │   │   └── SKILL.md
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── fizzy.py        # Fizzy API (37signals kanban)
│   │   │   └── SKILL.md
│   │   ├── graphics/
│   │   │   ├── __init__.py
│   │   │   ├── replicate_img.py  # FLUX image generation via Replicate
│   │   │   └── SKILL.md
│   │   ├── video/
│   │   │   ├── __init__.py
│   │   │   ├── ffmpeg.py       # FFmpeg wrapper
│   │   │   ├── tiktok.py       # TikTok video assembly
│   │   │   └── SKILL.md
│   │   ├── apps/
│   │   │   ├── __init__.py
│   │   │   ├── creator.py      # App scaffolding
│   │   │   └── SKILL.md
│   │   └── web/
│   │       ├── __init__.py
│   │       ├── search.py       # Web search capability
│   │       └── SKILL.md
│   │
│   └── mcp/
│       ├── __init__.py
│       └── server.py           # MCP server for skills
│
├── tests/
│   └── ...
├── pyproject.toml
├── .env.example
└── README.md
```

---

## INSTALLATION STEPS

### Step 1: Prerequisites

```bash
# Install uv (recommended Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# OR use pip with Python 3.11+
python --version  # Ensure 3.11+

# Install Claude Code CLI (bundled with SDK, but can install separately)
curl -fsSL https://claude.ai/install.sh | bash

# Install FFmpeg (for video skills)
# macOS
brew install ffmpeg
# Ubuntu/Debian
sudo apt install ffmpeg
```

### Step 2: Create Project

```bash
mkdir hawktui && cd hawktui
uv init
uv add claude-agent-sdk textual rich replicate httpx pillow python-dotenv
```

### Step 3: Environment Variables

Create `.env.example` (copy to `.env` and fill in):

```bash
# ═══════════════════════════════════════════════════════════
# HAWK TUI v4 — Environment Configuration
# ═══════════════════════════════════════════════════════════
# Copy this file to .env and fill in your values
# cp .env.example .env

# ───────────────────────────────────────────────────────────
# CORE — Required
# ───────────────────────────────────────────────────────────

# Claude Agent SDK (get from console.anthropic.com)
ANTHROPIC_API_KEY=sk-ant-api03-...

# ───────────────────────────────────────────────────────────
# IMAGE GENERATION — Replicate
# ───────────────────────────────────────────────────────────

# Replicate API (get from replicate.com/account/api-tokens)
REPLICATE_API_TOKEN=r8_...

# Model tier: fast ($0.003), quality ($0.03), pro ($0.055)
REPLICATE_IMAGE_MODEL=fast

# ───────────────────────────────────────────────────────────
# EMAIL & CALENDAR — Google
# ───────────────────────────────────────────────────────────

# Google OAuth (create at console.cloud.google.com)
GOOGLE_CLIENT_ID=...apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-...

# Path to OAuth token (auto-generated on first auth)
GOOGLE_TOKEN_PATH=~/.hawk/google_token.json

# ───────────────────────────────────────────────────────────
# TASK MANAGEMENT — Fizzy (37signals)
# ───────────────────────────────────────────────────────────

# Fizzy instance URL (self-hosted or fizzy.app)
FIZZY_BASE_URL=https://fizzy.app

# Access token (Settings → Developer → Access Tokens)
FIZZY_ACCESS_TOKEN=...

# Default board ID (optional)
FIZZY_DEFAULT_BOARD_ID=

# ───────────────────────────────────────────────────────────
# CRM — HubSpot
# ───────────────────────────────────────────────────────────

# HubSpot Private App Token (developers.hubspot.com)
HUBSPOT_API_KEY=pat-na1-...

# ───────────────────────────────────────────────────────────
# DATA WAREHOUSE — Snowflake
# ───────────────────────────────────────────────────────────

# Snowflake connection
SNOWFLAKE_ACCOUNT=xy12345.us-east-1
SNOWFLAKE_USER=HAWK_USER
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ANALYTICS
SNOWFLAKE_SCHEMA=PUBLIC

# ───────────────────────────────────────────────────────────
# UI SETTINGS
# ───────────────────────────────────────────────────────────

# Theme: dark, light, ps2
HAWK_THEME=dark

# Show AI reasoning panel: true, false
HAWK_SHOW_REASONING=true

# Auto-play boot animation: true, false
HAWK_BOOT_ANIMATION=true

# Default email action: archive, skip, none
HAWK_DEFAULT_EMAIL_ACTION=none

# Cruise mode speed (seconds between items)
HAWK_CRUISE_SPEED=2.0
```

---

## CORE IMPLEMENTATION

### 1. PS2-Style Loading Animation

Create `hawk/ui/loading.py`:

```python
"""
PS2-style loading animation for Hawk TUI.
Inspired by Paul Klein's CEO CLI boot sequence.
"""

import asyncio
import sys
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.style import Style

# Color palette (CEO CLI style)
COLORS = {
    "bg": "#1a1d23",
    "fg": "#e0e0e0",
    "accent": "#c9a227",      # Gold/yellow for highlights
    "border": "#4a5f4a",       # Muted green for borders
    "dim": "#6b7280",
    "blue": "#3b82f6",
}

# PS2-inspired pixelated logo
HAWK_LOGO = """
██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
██║  ██║██╔══██╗██║    ██║██║ ██╔╝
███████║███████║██║ █╗ ██║█████╔╝ 
██╔══██║██╔══██║██║███╗██║██╔═██╗ 
██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝
"""

CEO_CLI_TEXT = """
 ██████╗███████╗ ██████╗      ██████╗██╗     ██╗
██╔════╝██╔════╝██╔═══██╗    ██╔════╝██║     ██║
██║     █████╗  ██║   ██║    ██║     ██║     ██║
██║     ██╔══╝  ██║   ██║    ██║     ██║     ██║
╚██████╗███████╗╚██████╔╝    ╚██████╗███████╗██║
 ╚═════╝╚══════╝ ╚═════╝      ╚═════╝╚══════╝╚═╝
"""

# Retro scanline effect frames
BOOT_FRAMES = [
    "█" * 40,
    "█" * 35 + "░" * 5,
    "█" * 30 + "░" * 10,
    "█" * 25 + "░" * 15,
    "█" * 20 + "░" * 20,
]


async def ps2_boot_sequence(console: Console):
    """
    Render PS2-inspired boot animation.
    Matches CEO CLI aesthetic.
    """
    # Phase 1: Black screen with loading bar
    console.clear()
    for i in range(5):
        progress = "█" * (i * 8) + "░" * (40 - i * 8)
        console.clear()
        console.print("\n" * 10)
        console.print(Align.center(Text(progress, style=f"bold {COLORS['accent']}")))
        await asyncio.sleep(0.1)
    
    # Phase 2: CEO CLI logo reveal
    console.clear()
    logo = Text(CEO_CLI_TEXT, style=f"bold {COLORS['accent']}")
    subtitle = Text("Property of hawktui.xyz", style=f"dim {COLORS['dim']}")
    
    console.print("\n" * 5)
    console.print(Align.center(logo))
    console.print(Align.center(subtitle))
    await asyncio.sleep(1.5)
    
    # Phase 3: Loading skills with checkmarks
    console.clear()
    console.print("\n")
    console.print(
        Align.center(
            Text("HAWK TUI v4.0", style=f"bold {COLORS['accent']}")
        )
    )
    console.print(
        Align.center(
            Text("Initializing...\n", style=f"dim {COLORS['dim']}")
        )
    )
    
    skills = [
        ("Gmail API", "Email management"),
        ("Google Calendar", "Schedule access"),
        ("Fizzy Kanban", "Task tracking"),
        ("HubSpot CRM", "Contact management"),
        ("Snowflake", "Data queries"),
        ("Replicate FLUX", "Image generation"),
        ("FFmpeg", "Video processing"),
        ("Claude Agent", "AI reasoning"),
    ]
    
    for skill_name, skill_desc in skills:
        # Show loading
        loading_text = Text(f"  ◌ Loading {skill_name}...", style=COLORS['dim'])
        console.print(loading_text, end="\r")
        await asyncio.sleep(0.15)
        
        # Show complete
        complete_text = Text(f"  ✓ {skill_name}", style=f"bold green")
        desc_text = Text(f" — {skill_desc}", style=COLORS['dim'])
        console.print(complete_text + desc_text)
    
    console.print()
    console.print(
        Align.center(
            Text("Ready. Press any key to continue...", style=f"bold {COLORS['accent']}")
        )
    )
    await asyncio.sleep(0.5)


def run_boot():
    """Synchronous wrapper for boot sequence."""
    console = Console()
    asyncio.run(ps2_boot_sequence(console))


if __name__ == "__main__":
    run_boot()
```

---

### 2. Claude Agent SDK Integration

Create `hawk/agent.py`:

```python
"""
Hawk Agent - Claude Agent SDK wrapper with custom skills.
"""

import asyncio
from typing import AsyncIterator
from claude_agent_sdk import query, ClaudeAgentOptions, ClaudeSDKClient
from claude_agent_sdk.tools import tool, create_sdk_mcp_server

from hawk.skills import (
    gmail_skill,
    gcal_skill,
    hubspot_skill,
    snowflake_skill,
    fizzy_skill,
    replicate_img_skill,
    ffmpeg_skill,
    app_creator_skill,
    tiktok_skill,
    web_search_skill,
)


HAWK_SYSTEM_PROMPT = """
You are Hawk, a CEO agent CLI assistant. You help busy executives and entrepreneurs 
manage their digital life from the terminal.

Your capabilities include:
- Email management (Gmail)
- Calendar scheduling (Google Calendar)
- CRM operations (HubSpot)
- Data queries (Snowflake)
- Task management (Fizzy - 37signals kanban)
- Image generation (Replicate FLUX)
- Video creation (FFmpeg + TikTok assembly)
- App scaffolding

Be concise, actionable, and proactive. Suggest next steps when appropriate.
Format responses for terminal readability.
"""


class HawkAgent:
    """Main agent class wrapping Claude Agent SDK."""
    
    def __init__(self):
        self.options = ClaudeAgentOptions(
            model="claude-sonnet-4-5",
            system_prompt=HAWK_SYSTEM_PROMPT,
            max_tokens=4096,
            allowed_tools=[
                "Bash",
                "Read",
                "Write",
                "Edit",
                "Glob",
                "WebSearch",
            ],
        )
        
        # Register custom MCP tools
        self.mcp_server = create_sdk_mcp_server(
            tools=[
                gmail_skill.send_email,
                gmail_skill.read_inbox,
                gmail_skill.search_emails,
                gcal_skill.list_events,
                gcal_skill.create_event,
                hubspot_skill.get_contacts,
                hubspot_skill.create_deal,
                snowflake_skill.run_query,
                fizzy_skill.list_boards,
                fizzy_skill.list_cards,
                fizzy_skill.create_card,
                fizzy_skill.move_card,
                fizzy_skill.close_card,
                replicate_img_skill.generate_image,
                replicate_img_skill.edit_image,
                replicate_img_skill.generate_variations,
                ffmpeg_skill.create_video,
                ffmpeg_skill.add_audio,
                app_creator_skill.scaffold_app,
                tiktok_skill.create_tiktok,
                web_search_skill.search,
            ]
        )
        
        self.client = ClaudeSDKClient(
            options=self.options,
            mcp_servers=[self.mcp_server],
        )
    
    async def chat(self, prompt: str) -> AsyncIterator[str]:
        """
        Send a prompt to the agent and stream the response.
        """
        async for message in self.client.query(prompt=prompt):
            if hasattr(message, 'text'):
                yield message.text
            elif hasattr(message, 'tool_use'):
                yield f"\n[dim]Using tool: {message.tool_use.name}[/]\n"
    
    async def run_task(self, task: str) -> str:
        """
        Run a task and return the complete response.
        """
        response_parts = []
        async for chunk in self.chat(task):
            response_parts.append(chunk)
        return "".join(response_parts)


# Convenience function for one-shot queries
async def hawk_query(prompt: str) -> AsyncIterator[str]:
    """Simple one-shot query interface."""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="claude-sonnet-4-5",
            system_prompt=HAWK_SYSTEM_PROMPT,
        )
    ):
        yield str(message)
```

---

### 3. Replicate Image Generation Skill (FLUX)

Create `hawk/skills/graphics/replicate_img.py`:

```python
"""
Replicate skill - FLUX image generation via Replicate API.
https://replicate.com/collections/text-to-image

Models available:
- black-forest-labs/flux-schnell  ($0.003/image, fast)
- black-forest-labs/flux-dev      ($0.030/image, high quality)
- black-forest-labs/flux-1.1-pro  ($0.055/image, best quality)
- black-forest-labs/flux-kontext-pro (image editing)
"""

import os
import httpx
from pathlib import Path
from typing import Optional

import replicate
from claude_agent_sdk.tools import tool

# Model tiers
MODELS = {
    "fast": "black-forest-labs/flux-schnell",
    "quality": "black-forest-labs/flux-dev",
    "pro": "black-forest-labs/flux-1.1-pro",
    "edit": "black-forest-labs/flux-kontext-pro",
}

DEFAULT_MODEL = os.getenv("REPLICATE_IMAGE_MODEL", "fast")


def _download_image(url: str, output_path: str) -> str:
    """Download image from URL to local path."""
    response = httpx.get(url, follow_redirects=True)
    response.raise_for_status()
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    return output_path


@tool(
    name="generate_image",
    description="Generate an image from a text prompt using FLUX via Replicate",
    input_schema={
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Detailed description of the image to generate"
            },
            "output_path": {
                "type": "string",
                "description": "Path to save the generated image",
                "default": "generated_image.png"
            },
            "model_tier": {
                "type": "string",
                "enum": ["fast", "quality", "pro"],
                "description": "Model tier: fast ($0.003), quality ($0.03), pro ($0.055)",
                "default": "fast"
            },
            "aspect_ratio": {
                "type": "string",
                "enum": ["1:1", "16:9", "9:16", "4:3", "3:4"],
                "description": "Aspect ratio (9:16 for TikTok/Reels)",
                "default": "1:1"
            },
            "num_outputs": {
                "type": "integer",
                "description": "Number of images to generate (1-4)",
                "default": 1
            }
        },
        "required": ["prompt"]
    }
)
def generate_image(args: dict) -> str:
    """Generate an image from a text prompt using FLUX."""
    prompt = args["prompt"]
    output_path = args.get("output_path", "generated_image.png")
    model_tier = args.get("model_tier", DEFAULT_MODEL)
    aspect_ratio = args.get("aspect_ratio", "1:1")
    num_outputs = min(args.get("num_outputs", 1), 4)
    
    model = MODELS.get(model_tier, MODELS["fast"])
    
    try:
        # Build input params (vary by model)
        input_params = {
            "prompt": prompt,
            "num_outputs": num_outputs,
            "output_format": "png",
        }
        
        # FLUX schnell uses fewer steps
        if model_tier == "fast":
            input_params["num_inference_steps"] = 4
        else:
            input_params["num_inference_steps"] = 28
            input_params["guidance_scale"] = 3.5
        
        # Aspect ratio handling
        if aspect_ratio == "9:16":
            input_params["width"] = 768
            input_params["height"] = 1344
        elif aspect_ratio == "16:9":
            input_params["width"] = 1344
            input_params["height"] = 768
        elif aspect_ratio == "4:3":
            input_params["width"] = 1024
            input_params["height"] = 768
        elif aspect_ratio == "3:4":
            input_params["width"] = 768
            input_params["height"] = 1024
        else:  # 1:1
            input_params["width"] = 1024
            input_params["height"] = 1024
        
        # Run model
        output = replicate.run(model, input=input_params)
        
        # Handle output (can be list or single URL)
        if isinstance(output, list):
            urls = output
        else:
            urls = [output]
        
        # Download images
        saved_paths = []
        for i, url in enumerate(urls):
            if num_outputs > 1:
                path = output_path.replace(".png", f"_{i+1}.png")
            else:
                path = output_path
            _download_image(str(url), path)
            saved_paths.append(path)
        
        return f"✓ Generated {len(saved_paths)} image(s): {', '.join(saved_paths)}"
    
    except replicate.exceptions.ReplicateError as e:
        return f"✗ Replicate error: {str(e)}"
    except Exception as e:
        return f"✗ Error generating image: {str(e)}"


@tool(
    name="edit_image",
    description="Edit an existing image with natural language instructions using FLUX Kontext",
    input_schema={
        "type": "object",
        "properties": {
            "input_path": {
                "type": "string",
                "description": "Path to the image to edit"
            },
            "instruction": {
                "type": "string",
                "description": "Natural language editing instruction (e.g., 'add sunglasses', 'change background to beach')"
            },
            "output_path": {
                "type": "string",
                "description": "Path to save the edited image",
                "default": "edited_image.png"
            }
        },
        "required": ["input_path", "instruction"]
    }
)
def edit_image(args: dict) -> str:
    """Edit an image using natural language instructions via FLUX Kontext."""
    input_path = args["input_path"]
    instruction = args["instruction"]
    output_path = args.get("output_path", "edited_image.png")
    
    try:
        # Read input image
        with open(input_path, "rb") as f:
            image_data = f.read()
        
        # Upload to Replicate (or use base64)
        # For simplicity, we'll use a file URI approach
        output = replicate.run(
            MODELS["edit"],
            input={
                "image": open(input_path, "rb"),
                "prompt": instruction,
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
            }
        )
        
        # Download result
        if isinstance(output, list):
            url = str(output[0])
        else:
            url = str(output)
        
        _download_image(url, output_path)
        
        return f"✓ Edited image saved to {output_path}"
    
    except replicate.exceptions.ReplicateError as e:
        return f"✗ Replicate error: {str(e)}"
    except Exception as e:
        return f"✗ Error editing image: {str(e)}"


@tool(
    name="generate_variations",
    description="Generate multiple style variations of an image concept",
    input_schema={
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Base description of the image"
            },
            "styles": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of styles to apply (e.g., ['photorealistic', 'watercolor', 'anime'])"
            },
            "output_dir": {
                "type": "string",
                "description": "Directory to save variations",
                "default": "variations"
            }
        },
        "required": ["prompt", "styles"]
    }
)
def generate_variations(args: dict) -> str:
    """Generate multiple style variations of a concept."""
    base_prompt = args["prompt"]
    styles = args["styles"]
    output_dir = args.get("output_dir", "variations")
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    results = []
    for i, style in enumerate(styles):
        styled_prompt = f"{style} style: {base_prompt}"
        
        try:
            output = replicate.run(
                MODELS["fast"],
                input={
                    "prompt": styled_prompt,
                    "num_inference_steps": 4,
                    "num_outputs": 1,
                }
            )
            
            url = str(output[0]) if isinstance(output, list) else str(output)
            filename = f"{output_dir}/{style.replace(' ', '_').lower()}.png"
            _download_image(url, filename)
            results.append(f"✓ {style}: {filename}")
        
        except Exception as e:
            results.append(f"✗ {style}: {str(e)}")
    
    return "\n".join(results)
```

---

### 4. Fizzy Skill (37signals Kanban)

Create `hawk/skills/tasks/fizzy.py`:

```python
"""
Fizzy skill - 37signals kanban board (Linear replacement).
API added by DHH in PR #1766: https://github.com/basecamp/fizzy/pull/1766

Authentication: Bearer token via HTTP Authorization header
Docs: https://github.com/basecamp/fizzy/blob/main/docs/API.md
"""

import os
import httpx
from typing import Optional, List, Dict, Any

from claude_agent_sdk.tools import tool

# Configuration
BASE_URL = os.getenv("FIZZY_BASE_URL", "https://fizzy.app")
ACCESS_TOKEN = os.getenv("FIZZY_ACCESS_TOKEN")


def _fizzy_request(
    method: str,
    endpoint: str,
    json_data: Optional[Dict] = None,
    params: Optional[Dict] = None
) -> Dict[str, Any]:
    """Make authenticated request to Fizzy API."""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    
    response = httpx.request(
        method=method,
        url=url,
        headers=headers,
        json=json_data,
        params=params,
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


@tool(
    name="fizzy_list_boards",
    description="List all Fizzy boards (kanban boards)",
    input_schema={
        "type": "object",
        "properties": {},
        "required": []
    }
)
def list_boards(args: dict) -> str:
    """List all boards."""
    try:
        boards = _fizzy_request("GET", "/boards.json")
        
        if not boards:
            return "No boards found."
        
        lines = ["📋 **Fizzy Boards**\n"]
        for board in boards:
            lines.append(f"• {board['name']} (id: {board['id']})")
        
        return "\n".join(lines)
    
    except httpx.HTTPStatusError as e:
        return f"✗ Fizzy API error: {e.response.status_code}"
    except Exception as e:
        return f"✗ Error: {str(e)}"


@tool(
    name="fizzy_list_cards",
    description="List cards in a Fizzy board, optionally filtered by column",
    input_schema={
        "type": "object",
        "properties": {
            "board_id": {
                "type": "integer",
                "description": "Board ID to list cards from"
            },
            "column": {
                "type": "string",
                "description": "Optional column name to filter (e.g., 'In Progress', 'Done')"
            },
            "limit": {
                "type": "integer",
                "description": "Max cards to return",
                "default": 20
            }
        },
        "required": ["board_id"]
    }
)
def list_cards(args: dict) -> str:
    """List cards in a board."""
    board_id = args["board_id"]
    column_filter = args.get("column")
    limit = args.get("limit", 20)
    
    try:
        cards = _fizzy_request("GET", f"/boards/{board_id}/cards.json")
        
        if column_filter:
            cards = [c for c in cards if c.get("column", {}).get("name", "").lower() == column_filter.lower()]
        
        cards = cards[:limit]
        
        if not cards:
            return "No cards found."
        
        lines = ["🎴 **Cards**\n"]
        for card in cards:
            column_name = card.get("column", {}).get("name", "Unknown")
            lines.append(f"• [{column_name}] {card['title']} (id: {card['id']})")
        
        return "\n".join(lines)
    
    except httpx.HTTPStatusError as e:
        return f"✗ Fizzy API error: {e.response.status_code}"
    except Exception as e:
        return f"✗ Error: {str(e)}"


@tool(
    name="fizzy_create_card",
    description="Create a new card in a Fizzy board",
    input_schema={
        "type": "object",
        "properties": {
            "board_id": {
                "type": "integer",
                "description": "Board ID to create card in"
            },
            "column_id": {
                "type": "integer",
                "description": "Column ID to place the card"
            },
            "title": {
                "type": "string",
                "description": "Card title"
            },
            "content": {
                "type": "string",
                "description": "Card description/content (supports HTML)",
                "default": ""
            },
            "due_on": {
                "type": "string",
                "description": "Due date in YYYY-MM-DD format",
                "default": None
            }
        },
        "required": ["board_id", "column_id", "title"]
    }
)
def create_card(args: dict) -> str:
    """Create a new card."""
    board_id = args["board_id"]
    column_id = args["column_id"]
    title = args["title"]
    content = args.get("content", "")
    due_on = args.get("due_on")
    
    payload = {
        "title": title,
        "content": content,
    }
    if due_on:
        payload["due_on"] = due_on
    
    try:
        card = _fizzy_request(
            "POST",
            f"/boards/{board_id}/columns/{column_id}/cards.json",
            json_data=payload
        )
        
        return f"✓ Created card: {card['title']} (id: {card['id']})"
    
    except httpx.HTTPStatusError as e:
        return f"✗ Fizzy API error: {e.response.status_code}"
    except Exception as e:
        return f"✗ Error: {str(e)}"


@tool(
    name="fizzy_move_card",
    description="Move a card to a different column",
    input_schema={
        "type": "object",
        "properties": {
            "board_id": {
                "type": "integer",
                "description": "Board ID"
            },
            "card_id": {
                "type": "integer",
                "description": "Card ID to move"
            },
            "column_id": {
                "type": "integer",
                "description": "Target column ID"
            }
        },
        "required": ["board_id", "card_id", "column_id"]
    }
)
def move_card(args: dict) -> str:
    """Move a card to a different column."""
    board_id = args["board_id"]
    card_id = args["card_id"]
    column_id = args["column_id"]
    
    try:
        _fizzy_request(
            "POST",
            f"/boards/{board_id}/cards/{card_id}/moves.json",
            json_data={"column_id": column_id}
        )
        
        return f"✓ Moved card {card_id} to column {column_id}"
    
    except httpx.HTTPStatusError as e:
        return f"✗ Fizzy API error: {e.response.status_code}"
    except Exception as e:
        return f"✗ Error: {str(e)}"


@tool(
    name="fizzy_close_card",
    description="Close/complete a card",
    input_schema={
        "type": "object",
        "properties": {
            "board_id": {
                "type": "integer",
                "description": "Board ID"
            },
            "card_id": {
                "type": "integer",
                "description": "Card ID to close"
            }
        },
        "required": ["board_id", "card_id"]
    }
)
def close_card(args: dict) -> str:
    """Close a card."""
    board_id = args["board_id"]
    card_id = args["card_id"]
    
    try:
        _fizzy_request(
            "PUT",
            f"/boards/{board_id}/cards/{card_id}/close.json"
        )
        
        return f"✓ Closed card {card_id}"
    
    except httpx.HTTPStatusError as e:
        return f"✗ Fizzy API error: {e.response.status_code}"
    except Exception as e:
        return f"✗ Error: {str(e)}"


@tool(
    name="fizzy_get_identity",
    description="Get current user identity and available accounts",
    input_schema={
        "type": "object",
        "properties": {},
        "required": []
    }
)
def get_identity(args: dict) -> str:
    """Get user identity."""
    try:
        identity = _fizzy_request("GET", "/identity.json")
        
        name = identity.get("name", "Unknown")
        email = identity.get("email", "")
        accounts = identity.get("accounts", [])
        
        lines = [f"👤 **{name}** ({email})\n"]
        if accounts:
            lines.append("Accounts:")
            for acc in accounts:
                lines.append(f"  • {acc.get('name', 'Unknown')}")
        
        return "\n".join(lines)
    
    except httpx.HTTPStatusError as e:
        return f"✗ Fizzy API error: {e.response.status_code}"
    except Exception as e:
        return f"✗ Error: {str(e)}"
```

---

### 5. FFmpeg / TikTok Video Skill

Create `hawk/skills/video/ffmpeg.py`:

```python
"""
FFmpeg skill - Video creation and manipulation.
"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional

from claude_agent_sdk.tools import tool


@tool(
    name="create_video_from_images",
    description="Create a video from a sequence of images using FFmpeg",
    input_schema={
        "type": "object",
        "properties": {
            "image_pattern": {
                "type": "string",
                "description": "Glob pattern for input images (e.g., 'frames/*.png')"
            },
            "output_path": {
                "type": "string",
                "description": "Output video file path"
            },
            "fps": {
                "type": "integer",
                "description": "Frames per second",
                "default": 30
            },
            "codec": {
                "type": "string",
                "description": "Video codec (libx264, libx265, etc.)",
                "default": "libx264"
            },
            "resolution": {
                "type": "string",
                "description": "Output resolution (e.g., '1080x1920' for TikTok)",
                "default": "1080x1920"
            }
        },
        "required": ["image_pattern", "output_path"]
    }
)
def create_video_from_images(args: dict) -> str:
    """Create video from image sequence."""
    image_pattern = args["image_pattern"]
    output_path = args["output_path"]
    fps = args.get("fps", 30)
    codec = args.get("codec", "libx264")
    resolution = args.get("resolution", "1080x1920")
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-pattern_type", "glob",
        "-i", image_pattern,
        "-c:v", codec,
        "-s", resolution,
        "-pix_fmt", "yuv420p",
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"✓ Video created: {output_path}"
    except subprocess.CalledProcessError as e:
        return f"✗ FFmpeg error: {e.stderr}"


@tool(
    name="add_audio_to_video",
    description="Add audio track to a video file",
    input_schema={
        "type": "object",
        "properties": {
            "video_path": {
                "type": "string",
                "description": "Input video file path"
            },
            "audio_path": {
                "type": "string",
                "description": "Input audio file path"
            },
            "output_path": {
                "type": "string",
                "description": "Output video file path"
            },
            "loop_audio": {
                "type": "boolean",
                "description": "Loop audio to match video length",
                "default": True
            }
        },
        "required": ["video_path", "audio_path", "output_path"]
    }
)
def add_audio_to_video(args: dict) -> str:
    """Add audio track to video."""
    video_path = args["video_path"]
    audio_path = args["audio_path"]
    output_path = args["output_path"]
    loop_audio = args.get("loop_audio", True)
    
    # Build FFmpeg command
    if loop_audio:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-stream_loop", "-1",
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"✓ Audio added: {output_path}"
    except subprocess.CalledProcessError as e:
        return f"✗ FFmpeg error: {e.stderr}"


@tool(
    name="create_tiktok_video",
    description="Create a TikTok-format video with text overlays and transitions",
    input_schema={
        "type": "object",
        "properties": {
            "images": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of image paths to include"
            },
            "captions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Text captions for each image"
            },
            "audio_path": {
                "type": "string",
                "description": "Background audio file path"
            },
            "output_path": {
                "type": "string",
                "description": "Output video file path"
            },
            "duration_per_image": {
                "type": "number",
                "description": "Seconds to display each image",
                "default": 3.0
            }
        },
        "required": ["images", "output_path"]
    }
)
def create_tiktok_video(args: dict) -> str:
    """
    Create a TikTok-style video with images, captions, and audio.
    Uses FFmpeg filter complex for text overlays and transitions.
    """
    images = args["images"]
    captions = args.get("captions", [])
    audio_path = args.get("audio_path")
    output_path = args["output_path"]
    duration = args.get("duration_per_image", 3.0)
    
    # TikTok dimensions
    width, height = 1080, 1920
    
    # Build filter complex for image slideshow with captions
    inputs = []
    filter_parts = []
    
    for i, img in enumerate(images):
        inputs.extend(["-loop", "1", "-t", str(duration), "-i", img])
        
        # Scale and pad each image to TikTok size
        filter_parts.append(
            f"[{i}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black[v{i}]"
        )
    
    # Concatenate all video streams
    concat_inputs = "".join(f"[v{i}]" for i in range(len(images)))
    filter_parts.append(f"{concat_inputs}concat=n={len(images)}:v=1:a=0[outv]")
    
    # Add captions if provided
    if captions:
        caption_filter = "[outv]"
        for i, caption in enumerate(captions):
            # Escape special characters
            safe_caption = caption.replace("'", "'\\''").replace(":", "\\:")
            start_time = i * duration
            end_time = (i + 1) * duration
            caption_filter += (
                f"drawtext=text='{safe_caption}':"
                f"fontsize=60:fontcolor=white:borderw=3:bordercolor=black:"
                f"x=(w-text_w)/2:y=h-200:"
                f"enable='between(t,{start_time},{end_time})',"
            )
        caption_filter = caption_filter.rstrip(",") + "[final]"
        filter_parts.append(caption_filter)
        output_stream = "[final]"
    else:
        output_stream = "[outv]"
    
    # Build command
    cmd = ["ffmpeg", "-y"]
    cmd.extend(inputs)
    
    if audio_path:
        cmd.extend(["-i", audio_path])
    
    cmd.extend([
        "-filter_complex", ";".join(filter_parts),
        "-map", output_stream,
    ])
    
    if audio_path:
        cmd.extend(["-map", f"{len(images)}:a", "-c:a", "aac", "-shortest"])
    
    cmd.extend(["-c:v", "libx264", "-pix_fmt", "yuv420p", output_path])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"✓ TikTok video created: {output_path}"
    except subprocess.CalledProcessError as e:
        return f"✗ FFmpeg error: {e.stderr}"
```

---

### 6. Main TUI Application

Create `hawk/app.py`:

```python
"""
Hawk TUI - Main Textual application.
Inspired by Paul Klein's CEO CLI v4 aesthetic.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Static, RichLog
from textual.binding import Binding
from textual.reactive import reactive
from textual import events
from rich.text import Text
from rich.panel import Panel

from hawk.agent import HawkAgent
from hawk.ui.loading import ps2_boot_sequence

# CEO CLI color palette
COLORS = {
    "bg": "#1a1d23",
    "fg": "#e0e0e0",
    "accent": "#c9a227",
    "border": "#4a5f4a",
    "dim": "#6b7280",
    "highlight": "#2d3748",
}


class MessagePanel(Static):
    """Left panel showing current message/content."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = ""
        self.source = ""
        self.link = ""
    
    def set_message(self, source: str, content: str, link: str = ""):
        self.source = source
        self.content = content
        self.link = link
        self.refresh()
    
    def render(self) -> Panel:
        lines = []
        if self.source:
            lines.append(f"[bold]Source:[/] [cyan]{self.source}[/]")
        lines.append("")
        lines.append(self.content)
        if self.link:
            lines.append("")
            lines.append(f"[dim]Link: {self.link}[/]")
        
        return Panel(
            "\n".join(lines),
            title="[bold]MESSAGE[/]",
            border_style=COLORS["border"],
        )


class MenuPanel(Static):
    """Right panel showing available actions."""
    
    MENU_ITEMS = [
        ("v", "View Full", "Show complete message"),
        ("a", "AI Prompt", "Give AI instructions"),
        ("r", "Reply", "Compose response"),
        ("f", "Forward", "Forward to someone"),
        ("t", "Add to Todos", "Create task item"),
        ("m", "Monitor", "Track for updates"),
        ("d", "Done/Archive", "Mark as resolved"),
        ("x", "Auto-Archive", "Create archive rule"),
        ("c", "Cruise Mode", "Quick review"),
        ("s", "Skip", "Move to next"),
        ("q", "Quit", "Save and exit"),
    ]
    
    selected = reactive(6)  # Default to "Done/Archive"
    
    def render(self) -> Panel:
        lines = []
        for i, (key, name, desc) in enumerate(self.MENU_ITEMS):
            if i == self.selected:
                line = f"[bold {COLORS['accent']}]▶[{key}] {name}[/]"
            else:
                line = f" [{COLORS['accent']}][{key}][/] {name}"
            lines.append(line)
            lines.append(f"   [dim]{desc}[/]")
        
        lines.append("")
        lines.append(f"[dim]↑/↓ arrows, Enter,[/]")
        lines.append(f"[dim]or type a letter[/]")
        
        return Panel(
            "\n".join(lines),
            title="[bold]MENU[/]",
            border_style=COLORS["border"],
        )


class ReasoningPanel(Static):
    """Panel showing AI reasoning before action."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = ""
        self.reasoning = ""
        self.draft = ""
    
    def set_reasoning(self, action: str, reasoning: str, draft: str = ""):
        self.action = action
        self.reasoning = reasoning
        self.draft = draft
        self.refresh()
    
    def render(self) -> Panel:
        lines = [
            f"[bold {COLORS['accent']}]Action:[/] {self.action}",
            "",
            f"[bold]Reasoning:[/]",
            f"[dim]{self.reasoning}[/]",
        ]
        
        if self.draft:
            lines.extend([
                "",
                f"[bold]Draft:[/]",
                self.draft,
            ])
        
        return Panel(
            "\n".join(lines),
            border_style=COLORS["border"],
        )


class ConfirmDialog(Static):
    """Human-in-the-loop confirmation dialog."""
    
    def render(self) -> Panel:
        lines = [
            "[bold]Execute this?[/]",
            "",
            f"[{COLORS['accent']}][v][/] View Full",
            f"[{COLORS['accent']}][y][/] Yes",
            f"[{COLORS['accent']}][e][/] Edit",
            f"[{COLORS['accent']}][f][/] Feedback",
            f"[{COLORS['accent']}][n][/] No",
        ]
        
        return Panel(
            "\n".join(lines),
            border_style=COLORS["accent"],
        )


class HawkApp(App):
    """Hawk TUI main application."""
    
    CSS = """
    Screen {
        background: #1a1d23;
    }
    
    #main-container {
        layout: horizontal;
        height: 100%;
    }
    
    #message-panel {
        width: 2fr;
        height: 100%;
        padding: 1;
    }
    
    #menu-panel {
        width: 1fr;
        height: 100%;
        padding: 1;
    }
    
    #reasoning-panel {
        height: auto;
        padding: 1;
        display: none;
    }
    
    #input-container {
        height: 3;
        dock: bottom;
        padding: 0 1;
    }
    
    #prompt-input {
        width: 100%;
        background: #2d3748;
        color: #e0e0e0;
        border: solid #4a5f4a;
    }
    
    .highlight {
        background: #2d3748;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "quit", "Quit"),
        Binding("v", "view_full", "View Full"),
        Binding("a", "ai_prompt", "AI Prompt"),
        Binding("r", "reply", "Reply"),
        Binding("d", "done", "Done/Archive"),
        Binding("s", "skip", "Skip"),
        Binding("c", "cruise", "Cruise Mode"),
        Binding("up", "menu_up", "Menu Up"),
        Binding("down", "menu_down", "Menu Down"),
        Binding("enter", "menu_select", "Select"),
    ]
    
    def __init__(self):
        super().__init__()
        self.agent = HawkAgent()
        self.is_processing = False
        self.show_reasoning = True
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            MessagePanel(id="message-panel"),
            MenuPanel(id="menu-panel"),
            id="main-container",
        )
        yield ReasoningPanel(id="reasoning-panel")
        yield Container(
            Input(
                placeholder="Your instruction: ",
                id="prompt-input"
            ),
            id="input-container",
        )
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when app starts."""
        self.query_one("#prompt-input", Input).focus()
        
        # Set initial message
        msg_panel = self.query_one("#message-panel", MessagePanel)
        msg_panel.set_message(
            source="HAWK",
            content="Welcome to Hawk TUI v4.0\n\nReady to process your inbox, calendar, and tasks.\n\nType an instruction or press a key to begin.",
            link=""
        )
    
    def action_menu_up(self) -> None:
        menu = self.query_one("#menu-panel", MenuPanel)
        menu.selected = max(0, menu.selected - 1)
    
    def action_menu_down(self) -> None:
        menu = self.query_one("#menu-panel", MenuPanel)
        menu.selected = min(len(menu.MENU_ITEMS) - 1, menu.selected + 1)
    
    def action_ai_prompt(self) -> None:
        """Focus the AI prompt input."""
        self.query_one("#prompt-input", Input).focus()
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user instruction submission."""
        if self.is_processing:
            return
        
        instruction = event.value.strip()
        if not instruction:
            return
        
        # Clear input
        input_widget = self.query_one("#prompt-input", Input)
        input_widget.value = ""
        
        # Show reasoning panel
        reasoning_panel = self.query_one("#reasoning-panel", ReasoningPanel)
        reasoning_panel.display = True
        reasoning_panel.set_reasoning(
            action="THINKING",
            reasoning="Processing your instruction...",
        )
        
        self.is_processing = True
        
        try:
            # Get AI response
            response_parts = []
            async for chunk in self.agent.chat(instruction):
                response_parts.append(chunk)
            
            full_response = "".join(response_parts)
            
            # Update reasoning panel with result
            reasoning_panel.set_reasoning(
                action="REPLY",
                reasoning=f"Processed instruction: {instruction[:50]}...",
                draft=full_response[:200] + "..." if len(full_response) > 200 else full_response,
            )
            
        except Exception as e:
            reasoning_panel.set_reasoning(
                action="ERROR",
                reasoning=str(e),
            )
        finally:
            self.is_processing = False
            input_widget.focus()


def main():
    """Entry point."""
    app = HawkApp()
    app.run()


if __name__ == "__main__":
    main()
```

---

### 7. Entry Point

Create `hawk/main.py`:

```python
"""
Hawk TUI entry point.
"""

import sys
import asyncio
from rich.console import Console

from hawk.ui.loading import ps2_boot_sequence
from hawk.app import HawkApp


def main():
    """Main entry point with boot sequence."""
    console = Console()
    
    # Check for --no-boot flag
    if "--no-boot" not in sys.argv:
        asyncio.run(ps2_boot_sequence(console))
    
    # Launch TUI
    app = HawkApp()
    app.run()


if __name__ == "__main__":
    main()
```

---

## SKILL TEMPLATES

### Base Skill Class

Create `hawk/skills/base.py`:

```python
"""
Base skill class for Hawk TUI.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from dataclasses import dataclass


@dataclass
class SkillMetadata:
    """Metadata for a skill."""
    name: str
    description: str
    version: str
    author: str
    requires_auth: bool = False
    env_vars: List[str] = None


class BaseSkill(ABC):
    """Abstract base class for all Hawk skills."""
    
    metadata: SkillMetadata
    
    @abstractmethod
    def get_tools(self) -> List[callable]:
        """Return list of tool functions for this skill."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the skill is properly configured and working."""
        pass
    
    def __repr__(self) -> str:
        return f"<Skill: {self.metadata.name} v{self.metadata.version}>"
```

---

## API INTEGRATION GUIDES

### Replicate API Setup (Image Generation)

1. Go to [Replicate](https://replicate.com/) and sign up
2. Navigate to [Account Settings](https://replicate.com/account/api-tokens)
3. Create an API token
4. Add to `.env` as `REPLICATE_API_TOKEN=r8_...`
5. Add billing (pay-per-use, no minimums)

**Pricing** (as of 2024):
- FLUX schnell: ~$0.003/image (fastest)
- FLUX dev: ~$0.030/image (high quality)
- FLUX pro: ~$0.055/image (best quality)

### Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json`
6. First run will prompt for authentication

### Google Calendar API Setup

Same as Gmail - enable Calendar API in the same project.

### HubSpot API Setup

1. Go to [HubSpot Developer Portal](https://developers.hubspot.com/)
2. Create a private app
3. Add required scopes (contacts, deals, etc.)
4. Copy the access token to `HUBSPOT_API_KEY`

### Snowflake Setup

1. Get your account identifier from Snowflake console
2. Create a service user or use your credentials
3. Set up warehouse and database access

### Fizzy API Setup (37signals Kanban)

Fizzy is 37signals' new kanban tool — a Linear replacement. API added by DHH in [PR #1766](https://github.com/basecamp/fizzy/pull/1766).

**Self-hosted option:**
1. Clone [basecamp/fizzy](https://github.com/basecamp/fizzy)
2. Deploy with Kamal or Docker
3. Go to Settings → Developer → Access Tokens
4. Create token, add to `.env` as `FIZZY_ACCESS_TOKEN`

**Hosted option (fizzy.app):**
1. Sign up at fizzy.app
2. Go to Settings → Developer → Access Tokens
3. Create token, add to `.env`

**API Endpoints:**
- `GET /boards.json` — List boards
- `GET /boards/:id/cards.json` — List cards
- `POST /boards/:id/columns/:col_id/cards.json` — Create card
- `POST /boards/:id/cards/:card_id/moves.json` — Move card
- `PUT /boards/:id/cards/:card_id/close.json` — Close card
- `GET /identity.json` — Get user info
- `GET /users.json` — List users
- `GET /tags.json` — List tags

---

## USAGE EXAMPLES

```bash
# Start Hawk TUI
python -m hawk.main

# Skip boot animation
python -m hawk.main --no-boot

# One-shot query (for scripting)
hawk "Summarize my unread emails"
```

### In-TUI Commands

```
# Email
"Show my unread emails"
"Send an email to john@example.com about the Q4 report"
"Search emails from last week about budgets"

# Calendar
"What's on my calendar today?"
"Schedule a meeting with Sarah tomorrow at 2pm"
"Find time for a 30-minute call next week"

# CRM (HubSpot)
"Show my recent contacts"
"Create a deal for Acme Corp worth $50k"
"Update the status of deal #123 to closed-won"

# Data (Snowflake)
"Run a query: SELECT * FROM sales LIMIT 10"
"What were our top products last month?"

# Tasks (Fizzy)
"Show my Fizzy boards"
"List cards in the Engineering board"
"Create a card: Fix login button bug"
"Move card 123 to In Progress"
"Close card 456"

# Graphics (Replicate FLUX)
"Generate an image of a hawk flying over mountains"
"Edit profile.png: remove the background"
"Create 4 variations of 'sunset beach' in watercolor, anime, photorealistic, and oil painting styles"

# Video (TikTok)
"Create a TikTok from these 5 product photos with captions"
"Add trending-song.mp3 to my video"

# Apps
"Scaffold a new iOS app called MealPlanner"
"Create a landing page for my SaaS"
```

---

## CONFIGURATION

### pyproject.toml

```toml
[project]
name = "hawktui"
version = "4.0.0"
description = "CEO Agent CLI powered by Claude Agent SDK"
authors = [
    {name = "Carson Mulligan", email = "carson@hawktui.xyz"}
]
requires-python = ">=3.11"
dependencies = [
    "claude-agent-sdk>=0.1.0",
    "textual>=0.50.0",
    "rich>=13.0.0",
    "replicate>=0.25.0",
    "httpx>=0.27.0",
    "pillow>=10.0.0",
    "python-dotenv>=1.0.0",
    "google-auth-oauthlib>=1.0.0",
    "google-api-python-client>=2.0.0",
    "hubspot-api-client>=8.0.0",
    "snowflake-connector-python>=3.0.0",
]

[project.scripts]
hawk = "hawk.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| `CLINotFoundError` | Ensure Claude Code CLI is installed and in PATH |
| `ANTHROPIC_API_KEY not set` | Add key to `.env` or export in shell |
| `Replicate rate limit` | Check billing at replicate.com/account |
| `FFmpeg not found` | Install FFmpeg: `brew install ffmpeg` or `apt install ffmpeg` |
| `Permission denied` on OAuth | Delete `token.json` and re-authenticate |

---

## ROADMAP

- [ ] v4.0 - Core skills + PS2 boot animation
- [ ] v4.1 - Voice input (Whisper)
- [ ] v4.2 - MCP remix server for portability
- [ ] v4.3 - Plugin marketplace
- [ ] v5.0 - Multi-agent orchestration

---

## CREDITS

- **Claude Agent SDK** by Anthropic
- **Textual** by Textualize
- **FLUX** by Black Forest Labs (via Replicate)
- **PS2 aesthetic** inspired by Sony PlayStation 2

---

*hawktui.xyz — Your CEO in the terminal.*