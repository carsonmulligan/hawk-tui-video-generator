"""Image preview screen using terminal graphics."""

from textual.screen import Screen
from textual.widgets import Static
from textual.app import ComposeResult
from textual.containers import Container
from textual.binding import Binding
from pathlib import Path
from rich.panel import Panel
from rich.text import Text
from PIL import Image
import subprocess
import io


def image_to_ascii(image_path: Path, width: int = 80, height: int = 40) -> str:
    """Convert image to ASCII art using block characters."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")

        # Calculate aspect ratio preserving dimensions
        img_width, img_height = img.size
        aspect = img_height / img_width

        # Terminal characters are ~2x taller than wide
        new_width = width
        new_height = int(width * aspect * 0.5)

        if new_height > height:
            new_height = height
            new_width = int(height / aspect * 2)

        img = img.resize((new_width, new_height))

        # Convert to ASCII using half-block characters for better resolution
        lines = []
        pixels = list(img.getdata())

        for y in range(0, new_height - 1, 2):
            line = ""
            for x in range(new_width):
                # Top pixel
                idx_top = y * new_width + x
                r1, g1, b1 = pixels[idx_top] if idx_top < len(pixels) else (0, 0, 0)

                # Bottom pixel
                idx_bot = (y + 1) * new_width + x
                r2, g2, b2 = pixels[idx_bot] if idx_bot < len(pixels) else (0, 0, 0)

                # Use half-block character with foreground (top) and background (bottom)
                line += f"[rgb({r1},{g1},{b1}) on rgb({r2},{g2},{b2})]▀[/]"

            lines.append(line)

        return "\n".join(lines)

    except Exception as e:
        return f"[red]Error loading image: {e}[/]"


class ImagePreview(Static):
    """Widget to display image as ASCII art."""

    def __init__(self, image_path: Path, **kwargs):
        super().__init__(**kwargs)
        self.image_path = image_path

    def render(self) -> Panel:
        # Get terminal size and compute ASCII art dimensions
        size = self.size
        width = max(40, size.width - 4)
        height = max(20, size.height - 4)

        ascii_art = image_to_ascii(self.image_path, width, height)

        return Panel(
            ascii_art,
            title=f"[bold]{self.image_path.name}[/]",
            subtitle="[dim]Esc/q=close | ←/→=prev/next | f=full res[/]",
            border_style="#c9a227",
        )


class ImagePreviewScreen(Screen):
    """Full screen image preview."""

    CSS = """
    ImagePreviewScreen {
        background: #1a1d23;
    }

    ImagePreview {
        width: 100%;
        height: 100%;
    }
    """

    BINDINGS = [
        Binding("escape", "close", "Close", priority=True),
        Binding("q", "close", "Close"),
        Binding("f", "open_full", "Full Resolution"),
        Binding("left", "prev_image", "Previous"),
        Binding("right", "next_image", "Next"),
        Binding("h", "prev_image", "Previous"),
        Binding("l", "next_image", "Next"),
    ]

    def __init__(self, image_path: Path, all_images: list[Path] = None, **kwargs):
        super().__init__(**kwargs)
        self.image_path = image_path
        self.all_images = all_images or [image_path]
        self.current_index = self.all_images.index(image_path) if image_path in self.all_images else 0

    def compose(self) -> ComposeResult:
        yield ImagePreview(self.image_path, id="preview")

    def on_mount(self) -> None:
        """Open full resolution image in system viewer when preview opens."""
        self._open_in_preview()

    def _open_in_preview(self) -> None:
        """Open current image in macOS Preview."""
        subprocess.Popen(["open", str(self.image_path)])

    def key_escape(self) -> None:
        """Handle escape key to close preview."""
        self.app.pop_screen()

    def key_q(self) -> None:
        """Handle q key to close preview."""
        self.app.pop_screen()

    def action_close(self) -> None:
        """Close the preview and return to main app."""
        self.app.pop_screen()

    def action_open_full(self) -> None:
        """Open current image in full resolution viewer."""
        self._open_in_preview()

    def action_prev_image(self) -> None:
        """Show previous image."""
        if self.current_index > 0:
            self.current_index -= 1
            self._update_image()

    def action_next_image(self) -> None:
        """Show next image."""
        if self.current_index < len(self.all_images) - 1:
            self.current_index += 1
            self._update_image()

    def _update_image(self) -> None:
        """Update the displayed image."""
        self.image_path = self.all_images[self.current_index]
        preview = self.query_one("#preview", ImagePreview)
        preview.image_path = self.image_path
        preview.refresh()
        # Also open the new image in Preview
        self._open_in_preview()
