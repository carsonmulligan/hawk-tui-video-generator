"""Hawk TUI - Main Textual application."""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Input, Static
from textual.binding import Binding
from textual.reactive import reactive
from textual.message import Message
from textual import work
from rich.text import Text
from rich.panel import Panel
from pathlib import Path

from hawk.config import PROJECTS, COLORS, Project
from hawk import replicate_client, video
from hawk.screens.splash import SplashScreen


class ProjectSelector(Static, can_focus=True):
    """Sidebar showing available projects."""

    selected = reactive("dxp-labs")
    _project_slugs = list(PROJECTS.keys())

    BINDINGS = [
        Binding("up", "move_up", "Up", priority=True),
        Binding("down", "move_down", "Down", priority=True),
        Binding("k", "move_up", "Up"),
        Binding("j", "move_down", "Down"),
        Binding("enter", "select", "Select", priority=True),
    ]

    def action_move_up(self) -> None:
        """Move to previous project."""
        idx = self._project_slugs.index(self.selected)
        if idx > 0:
            self.selected = self._project_slugs[idx - 1]
            self.post_message(self.Changed(self.selected))

    def action_move_down(self) -> None:
        """Move to next project."""
        idx = self._project_slugs.index(self.selected)
        if idx < len(self._project_slugs) - 1:
            self.selected = self._project_slugs[idx + 1]
            self.post_message(self.Changed(self.selected))

    def action_select(self) -> None:
        """Select current project and move to prompt."""
        self.post_message(self.Selected(self.selected))

    class Changed(Message):
        """Project changed message."""
        def __init__(self, value: str) -> None:
            super().__init__()
            self.value = value

    class Selected(Message):
        """Project selected (Enter pressed) message."""
        def __init__(self, value: str) -> None:
            super().__init__()
            self.value = value

    def render(self) -> Panel:
        lines = []
        for i, (slug, proj) in enumerate(PROJECTS.items(), 1):
            if slug == self.selected:
                line = f"[bold {COLORS['accent']}]▶ [{i}] {proj.name}[/]"
            else:
                line = f"  [{COLORS['dim']}][{i}][/] {proj.name}"
            lines.append(line)

        return Panel(
            "\n".join(lines),
            title="[bold]PROJECTS[/]",
            border_style=COLORS["border"],
        )


class ImageList(Static, can_focus=True):
    """Display list of images in current project."""

    cursor = reactive(0)

    BINDINGS = [
        Binding("up", "move_up", "Up", priority=True),
        Binding("down", "move_down", "Down", priority=True),
        Binding("k", "move_up", "Up"),
        Binding("j", "move_down", "Down"),
        Binding("enter", "open_current", "Open", priority=True),
        Binding("space", "toggle_select", "Select"),
        Binding("a", "select_all", "All"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._images: list[Path] = []
        self._selected: set[int] = set()

    def set_images(self, images: list[Path]) -> None:
        """Update the image list."""
        self._images = images
        self._selected = set()
        self.cursor = 0
        self.refresh()

    def action_move_up(self) -> None:
        """Move cursor up."""
        if self._images and self.cursor > 0:
            self.cursor -= 1
            self.refresh()

    def action_move_down(self) -> None:
        """Move cursor down."""
        if self._images and self.cursor < len(self._images) - 1:
            self.cursor += 1
            self.refresh()

    def action_open_current(self) -> None:
        """Open current image."""
        if self._images and 0 <= self.cursor < len(self._images):
            import subprocess
            subprocess.Popen(["open", str(self._images[self.cursor])])

    def action_toggle_select(self) -> None:
        """Toggle selection of current image."""
        if self._images and 0 <= self.cursor < len(self._images):
            if self.cursor in self._selected:
                self._selected.discard(self.cursor)
            else:
                self._selected.add(self.cursor)
            self.refresh()

    def action_select_all(self) -> None:
        """Select all images."""
        self._selected = set(range(len(self._images)))
        self.refresh()

    def clear_selection(self) -> None:
        """Clear all selections."""
        self._selected = set()
        self.refresh()

    @property
    def images(self) -> list[Path]:
        return self._images

    @property
    def selected_indices(self) -> set[int]:
        return self._selected

    def render(self) -> Panel:
        if not self._images:
            content = f"[dim]No images yet.\n\nType a prompt below and press Enter to generate.[/]"
        else:
            lines = []
            start = max(0, self.cursor - 8)
            end = min(len(self._images), start + 18)

            for i in range(start, end):
                img = self._images[i]
                cursor_mark = f"[bold {COLORS['accent']}]▶[/]" if i == self.cursor else " "
                select_mark = f"[green]✓[/]" if i in self._selected else " "
                name = img.name[:32] + "..." if len(img.name) > 35 else img.name
                lines.append(f"{cursor_mark}{select_mark}[{i+1:2}] {name}")

            content = "\n".join(lines)
            if len(self._images) > 18:
                content += f"\n[dim]({self.cursor + 1}/{len(self._images)})[/]"

        selected_count = len(self._selected)
        title = f"[bold]IMAGES ({len(self._images)})"
        if selected_count > 0:
            title += f" [{COLORS['accent']}]{selected_count} selected[/]"
        title += "[/]"

        return Panel(content, title=title, border_style=COLORS["border"])


class PromptInput(Input):
    """Custom input that handles Enter for generation."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", priority=True),
    ]

    def action_cancel(self) -> None:
        """Cancel and clear input."""
        self.value = ""
        self.post_message(self.Cancelled())

    class Cancelled(Message):
        """Input cancelled message."""
        pass


class HawkTUI(App):
    """Hawk TUI - TikTok video creator."""

    TITLE = "HawkTUI"

    CSS = """
    Screen {
        background: #1a1d23;
    }

    #main-container {
        layout: horizontal;
        height: 1fr;
    }

    #left-panel {
        width: 25;
        height: 100%;
        padding: 1;
    }

    #center-panel {
        width: 1fr;
        height: 100%;
        padding: 1;
    }

    #right-panel {
        width: 28;
        height: 100%;
        padding: 1;
    }

    #prompt-input {
        dock: bottom;
        margin: 1;
        background: #2d3748;
        color: #e0e0e0;
        border: solid #4a5f4a;
    }

    #prompt-input:focus {
        border: solid #c9a227;
    }

    #status-bar {
        height: 1;
        dock: bottom;
        padding: 0 1;
        background: #2d3748;
        text-style: bold;
    }

    #prompt-input.disabled {
        background: #1a1d23;
        color: #c9a227;
    }

    ProjectSelector {
        height: auto;
    }

    ProjectSelector:focus {
        border: solid #c9a227;
    }

    ImageList {
        height: 1fr;
    }

    ImageList:focus {
        border: solid #c9a227;
    }

    #help-panel {
        height: auto;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+g", "focus_prompt", "Generate"),
        Binding("b", "browse", "Browse"),
        Binding("v", "create_video", "Video"),
        Binding("d", "delete_selected", "Delete"),
        Binding("1", "select_project_1", "Wedding"),
        Binding("2", "select_project_2", "Latin"),
        Binding("3", "select_project_3", "DXP"),
        Binding("escape", "clear_or_focus_images", "Clear"),
        Binding("tab", "focus_next", "Next", priority=True),
        Binding("shift+tab", "focus_prev", "Prev", priority=True),
    ]

    current_project = reactive("dxp-labs")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Container(ProjectSelector(id="project-selector"), id="left-panel"),
            Container(ImageList(id="image-list"), id="center-panel"),
            Container(Static(self._help_text(), id="help-panel"), id="right-panel"),
            id="main-container",
        )
        yield PromptInput(
            placeholder="Enter prompt and press Enter to generate...",
            id="prompt-input"
        )
        yield Static("Ready", id="status-bar")
        yield Footer()

    def _help_text(self) -> str:
        return f"""[bold]Navigation[/]
[{COLORS['accent']}]↑/↓[/] Move cursor
[{COLORS['accent']}]Tab[/] Switch panels
[{COLORS['accent']}]Enter[/] Select/Open

[bold]Images[/]
[{COLORS['accent']}]Space[/] Toggle select
[{COLORS['accent']}]a[/] Select all
[{COLORS['accent']}]Esc[/] Clear selection

[bold]Actions[/]
[{COLORS['accent']}]v[/] Create video
[{COLORS['accent']}]b[/] Browse folder
[{COLORS['accent']}]d[/] Delete selected

[bold]Projects[/]
[{COLORS['accent']}]1[/] Wedding Vision
[{COLORS['accent']}]2[/] Latin Bible
[{COLORS['accent']}]3[/] DXP Labs

[{COLORS['accent']}]q[/] Quit"""

    def on_mount(self) -> None:
        """Initialize the app."""
        self.push_screen(SplashScreen())
        selector = self.query_one("#project-selector", ProjectSelector)
        selector.selected = self.current_project
        self.refresh_images()
        # Focus the prompt input by default for immediate generation
        self.query_one("#prompt-input").focus()

    @property
    def project(self) -> Project:
        return PROJECTS[self.current_project]

    @property
    def image_list(self) -> ImageList:
        return self.query_one("#image-list", ImageList)

    def refresh_images(self) -> None:
        images = replicate_client.get_project_images(self.project)
        self.image_list.set_images(images)
        self.set_status(f"{self.project.name}: {len(images)} images")

    def watch_current_project(self, project_slug: str) -> None:
        selector = self.query_one("#project-selector", ProjectSelector)
        selector.selected = project_slug
        self.refresh_images()

    def set_status(self, message: str, working: bool = False) -> None:
        status = self.query_one("#status-bar", Static)
        if working:
            status.update(f"[bold {COLORS['accent']}]⏳ {message}[/]")
        else:
            status.update(f"[{COLORS['success']}]✓[/] {message}")

    # Focus management
    def action_focus_next(self) -> None:
        """Cycle focus: prompt -> projects -> images -> prompt."""
        focused = self.focused
        if isinstance(focused, PromptInput):
            self.query_one("#project-selector").focus()
        elif isinstance(focused, ProjectSelector):
            self.query_one("#image-list").focus()
        else:
            self.query_one("#prompt-input").focus()

    def action_focus_prev(self) -> None:
        """Cycle focus backwards."""
        focused = self.focused
        if isinstance(focused, PromptInput):
            self.query_one("#image-list").focus()
        elif isinstance(focused, ProjectSelector):
            self.query_one("#prompt-input").focus()
        else:
            self.query_one("#project-selector").focus()

    def action_focus_prompt(self) -> None:
        """Focus the prompt input."""
        self.query_one("#prompt-input").focus()

    def action_clear_or_focus_images(self) -> None:
        """Clear selection or focus images panel."""
        if isinstance(self.focused, PromptInput):
            self.query_one("#image-list").focus()
        else:
            self.image_list.clear_selection()
            self.set_status("Selection cleared")

    # Project selection
    def action_select_project_1(self) -> None:
        self.current_project = "wedding-vision"

    def action_select_project_2(self) -> None:
        self.current_project = "latin-bible"

    def action_select_project_3(self) -> None:
        self.current_project = "dxp-labs"

    # Message handlers
    def on_project_selector_changed(self, event: ProjectSelector.Changed) -> None:
        """Handle project navigation."""
        self.current_project = event.value

    def on_project_selector_selected(self, event: ProjectSelector.Selected) -> None:
        """Handle project selection (Enter)."""
        self.current_project = event.value
        self.query_one("#prompt-input").focus()
        self.set_status(f"Selected {self.project.name} - enter a prompt")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter in prompt input."""
        if event.input.id == "prompt-input":
            prompt = event.value.strip()
            if prompt:
                self._do_generate(prompt)
                event.input.value = ""

    def on_prompt_input_cancelled(self, event: PromptInput.Cancelled) -> None:
        """Handle Escape in prompt input."""
        self.query_one("#image-list").focus()
        self.set_status("Cancelled")

    @work(exclusive=True, thread=True)
    def _do_generate(self, prompt: str) -> None:
        """Generate images."""
        self.call_from_thread(self._show_generating, prompt)
        try:
            paths = replicate_client.generate_image(self.project, prompt)
            self.call_from_thread(self.refresh_images)
            self.call_from_thread(self.set_status, f"Generated {len(paths)} image(s)")
            self.call_from_thread(self._focus_images)
        except Exception as e:
            self.call_from_thread(self.set_status, f"Error: {str(e)[:50]}")
        finally:
            self.call_from_thread(self._hide_generating)

    def _show_generating(self, prompt: str) -> None:
        """Show generating state."""
        self.set_status(f"⏳ Generating: {prompt[:30]}...", True)
        # Disable input while generating
        prompt_input = self.query_one("#prompt-input", PromptInput)
        prompt_input.placeholder = "⏳ Generating... please wait"
        prompt_input.disabled = True

    def _hide_generating(self) -> None:
        """Hide generating state."""
        prompt_input = self.query_one("#prompt-input", PromptInput)
        prompt_input.placeholder = "Enter prompt and press Enter to generate..."
        prompt_input.disabled = False

    def _focus_images(self) -> None:
        """Focus images after generation."""
        self.query_one("#image-list").focus()

    def action_delete_selected(self) -> None:
        """Delete selected images."""
        selected = self.image_list.selected_indices
        images = self.image_list.images
        if not selected:
            self.set_status("No images selected (Space to select)")
            return
        count = 0
        for idx in sorted(selected, reverse=True):
            if idx < len(images):
                if replicate_client.delete_image(images[idx]):
                    count += 1
        self.refresh_images()
        self.set_status(f"Deleted {count} images")

    @work(exclusive=True, thread=True)
    def action_create_video(self) -> None:
        """Create video from selected images."""
        selected = self.image_list.selected_indices
        images = self.image_list.images

        if not selected:
            self.call_from_thread(self.set_status, "Select images first (Space or 'a' for all)")
            return

        self.call_from_thread(self.set_status, "Creating video...", True)
        try:
            selected_paths = [images[i] for i in sorted(selected)]
            output = video.create_slideshow(self.project, selected_paths)
            self.call_from_thread(self.set_status, f"Video saved: {output.name}")
        except Exception as e:
            self.call_from_thread(self.set_status, f"Error: {str(e)[:50]}")

    def action_browse(self) -> None:
        """Open the project images folder."""
        import subprocess
        subprocess.run(["open", str(self.project.images_dir)])
        self.set_status(f"Opened {self.project.images_dir}")


def main():
    """Entry point."""
    app = HawkTUI()
    app.run()


if __name__ == "__main__":
    main()
