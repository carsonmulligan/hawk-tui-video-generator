"""Caption editor screen for video creation."""

from pathlib import Path
from textual.screen import ModalScreen
from textual.widgets import Static, Input, Button, Label
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.binding import Binding


class CaptionEditor(ModalScreen[list[str] | None]):
    """Modal screen for editing captions for each image in a video."""

    CSS = """
    CaptionEditor {
        align: center middle;
    }
    
    #caption-dialog {
        width: 85%;
        max-width: 110;
        height: auto;
        max-height: 85%;
        background: $surface;
        border: tall $primary;
        padding: 1 2;
    }
    
    #caption-title {
        text-align: center;
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }
    
    #caption-help {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }
    
    .caption-row {
        height: auto;
        margin-bottom: 1;
        padding: 0 1;
    }
    
    .caption-label {
        width: 100%;
        color: $accent;
        margin-bottom: 0;
    }
    
    .caption-input {
        width: 100%;
    }
    
    #caption-scroll {
        height: auto;
        max-height: 25;
        margin-bottom: 1;
        border: solid $primary-darken-2;
        padding: 1;
    }
    
    #button-row {
        height: 3;
        align: center middle;
        margin-top: 1;
    }
    
    #button-row Button {
        margin: 0 1;
    }
    
    #create-btn {
        background: $success;
    }
    
    #skip-btn {
        background: $warning;
    }
    
    #cancel-btn {
        background: $error;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("ctrl+enter", "create", "Create Video"),
        Binding("tab", "focus_next_input", "Next field", priority=True),
        Binding("shift+tab", "focus_prev_input", "Prev field", priority=True),
    ]

    def __init__(self, images: list[Path]) -> None:
        super().__init__()
        self.images = images
        self.captions: list[str] = [""] * len(images)
        self._current_input = 0

    def compose(self) -> ComposeResult:
        with Container(id="caption-dialog"):
            yield Static(f"📝 Add Captions ({len(self.images)} images)", id="caption-title")
            yield Static("Tab/↓ next • Shift+Tab/↑ prev • Ctrl+Enter create • Esc cancel", id="caption-help")
            
            with VerticalScroll(id="caption-scroll"):
                for i, img in enumerate(self.images):
                    with Container(classes="caption-row"):
                        yield Label(f"{i+1}. {img.stem[:35]}", classes="caption-label")
                        yield Input(
                            placeholder="Caption text (leave empty for no text)",
                            id=f"caption-{i}",
                            classes="caption-input",
                        )
            
            with Horizontal(id="button-row"):
                yield Button("Create Video", id="create-btn", variant="success")
                yield Button("Skip Captions", id="skip-btn", variant="warning")
                yield Button("Cancel", id="cancel-btn", variant="error")

    def on_mount(self) -> None:
        """Focus first input on mount."""
        self._focus_input(0)

    def _focus_input(self, index: int) -> None:
        """Focus a specific input by index."""
        if 0 <= index < len(self.images):
            try:
                input_widget = self.query_one(f"#caption-{index}", Input)
                input_widget.focus()
                self._current_input = index
                # Scroll to make sure it's visible
                input_widget.scroll_visible()
            except Exception:
                pass

    def action_focus_next_input(self) -> None:
        """Focus next caption input."""
        next_idx = (self._current_input + 1) % len(self.images)
        self._focus_input(next_idx)

    def action_focus_prev_input(self) -> None:
        """Focus previous caption input."""
        prev_idx = (self._current_input - 1) % len(self.images)
        self._focus_input(prev_idx)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Track which input is currently focused."""
        if event.input.id and event.input.id.startswith("caption-"):
            try:
                self._current_input = int(event.input.id.split("-")[1])
            except (ValueError, IndexError):
                pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create-btn":
            self._collect_captions()
            self.dismiss(self.captions)
        elif event.button.id == "skip-btn":
            # Return empty captions (no text overlay)
            self.dismiss([])
        elif event.button.id == "cancel-btn":
            self.dismiss(None)

    def _collect_captions(self) -> None:
        """Collect all caption values from inputs."""
        for i in range(len(self.images)):
            try:
                input_widget = self.query_one(f"#caption-{i}", Input)
                self.captions[i] = input_widget.value.strip()
            except Exception:
                self.captions[i] = ""

    def action_cancel(self) -> None:
        self.dismiss(None)

    def action_create(self) -> None:
        self._collect_captions()
        self.dismiss(self.captions)

