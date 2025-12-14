"""Hawk TUI - Main Textual application."""

from textual.app import App, ComposeResult
from textual.containers import Container, ScrollableContainer
from textual.widgets import Header, Footer, Input, Static
from textual.binding import Binding
from textual.reactive import reactive
from textual import work
from rich.text import Text
from rich.panel import Panel
from pathlib import Path

from hawk.config import PROJECTS, COLORS, Project
from hawk import replicate_client, video


class ProjectSelector(Static):
    """Sidebar showing available projects."""

    selected = reactive("dxp-albs")  # Default to DXP where images exist

    def render(self) -> Panel:
        lines = []
        for i, (slug, proj) in enumerate(PROJECTS.items(), 1):
            if slug == self.selected:
                line = f"[bold {COLORS['accent']}]▶[{i}] {proj.name}[/]"
            else:
                line = f" [{COLORS['dim']}][{i}][/] {proj.name}"
            lines.append(line)
            lines.append(f"    [dim]{proj.description}[/]")
            lines.append("")

        return Panel(
            "\n".join(lines),
            title="[bold]PROJECTS[/]",
            border_style=COLORS["border"],
        )


class ImageList(Static):
    """Display list of images in current project."""

    cursor = reactive(0)

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

    def set_selected(self, selected: set[int]) -> None:
        """Update selected indices."""
        self._selected = selected
        self.refresh()

    def toggle_current(self) -> None:
        """Toggle selection of current image."""
        if self._images and 0 <= self.cursor < len(self._images):
            if self.cursor in self._selected:
                self._selected.discard(self.cursor)
            else:
                self._selected.add(self.cursor)
            self.refresh()

    def select_all(self) -> None:
        """Select all images."""
        self._selected = set(range(len(self._images)))
        self.refresh()

    def clear_selection(self) -> None:
        """Clear all selections."""
        self._selected = set()
        self.refresh()

    def move_up(self) -> None:
        """Move cursor up."""
        if self._images and self.cursor > 0:
            self.cursor -= 1
            self.refresh()

    def move_down(self) -> None:
        """Move cursor down."""
        if self._images and self.cursor < len(self._images) - 1:
            self.cursor += 1
            self.refresh()

    @property
    def images(self) -> list[Path]:
        return self._images

    @property
    def selected_indices(self) -> set[int]:
        return self._selected

    def render(self) -> Panel:
        if not self._images:
            content = "[dim]No images yet.\n\nPress [3] for DXP Albums\nPress [g] to generate.[/]"
        else:
            lines = []
            # Show images around cursor
            start = max(0, self.cursor - 8)
            end = min(len(self._images), start + 18)

            for i in range(start, end):
                img = self._images[i]
                # Cursor indicator
                if i == self.cursor:
                    cursor_mark = f"[bold {COLORS['accent']}]▶[/]"
                else:
                    cursor_mark = " "

                # Selection indicator
                if i in self._selected:
                    select_mark = f"[green]✓[/]"
                else:
                    select_mark = " "

                # Filename (truncate if needed)
                name = img.name
                if len(name) > 35:
                    name = name[:32] + "..."

                lines.append(f"{cursor_mark}{select_mark}[{i+1:2}] {name}")

            content = "\n".join(lines)

            # Show scroll indicator
            if len(self._images) > 18:
                content += f"\n[dim]({self.cursor + 1}/{len(self._images)}) ↑/↓ to scroll[/]"

        selected_count = len(self._selected)
        title = f"[bold]IMAGES ({len(self._images)})"
        if selected_count > 0:
            title += f" [{COLORS['accent']}]{selected_count} selected[/]"
        title += "[/]"

        return Panel(
            content,
            title=title,
            border_style=COLORS["border"],
        )


class StatusBar(Static):
    """Bottom status bar."""

    message = reactive("Ready - Press 3 for DXP Albums with images")
    is_working = reactive(False)

    def render(self) -> Text:
        if self.is_working:
            return Text(f"⏳ {self.message}", style=f"bold {COLORS['accent']}")
        return Text(f"✓ {self.message}", style=f"bold {COLORS['success']}")


class MenuPanel(Static):
    """Right panel showing available actions."""

    def render(self) -> Panel:
        lines = [
            f"[bold]Navigation[/]",
            f"[{COLORS['accent']}]↑/↓[/] Move cursor",
            f"[{COLORS['accent']}]Tab[/] Toggle select",
            f"[{COLORS['accent']}]a[/]   Select all",
            f"[{COLORS['accent']}]Esc[/] Clear selection",
            "",
            f"[bold]Actions[/]",
            f"[{COLORS['accent']}]g[/] Generate images",
            f"[{COLORS['accent']}]v[/] Create video",
            f"[{COLORS['accent']}]b[/] Browse folder",
            f"[{COLORS['accent']}]o[/] Open image",
            f"[{COLORS['accent']}]d[/] Delete selected",
            "",
            f"[bold]Projects[/]",
            f"[{COLORS['accent']}]1[/] Wedding Vision",
            f"[{COLORS['accent']}]2[/] Latin Bible",
            f"[{COLORS['accent']}]3[/] DXP Albums",
            "",
            f"[{COLORS['accent']}]q[/] Quit",
        ]

        return Panel(
            "\n".join(lines),
            title="[bold]ACTIONS[/]",
            border_style=COLORS["border"],
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

    #left-panel {
        width: 1fr;
        height: 100%;
        padding: 1;
    }

    #center-panel {
        width: 2fr;
        height: 100%;
        padding: 1;
    }

    #right-panel {
        width: 1fr;
        height: 100%;
        padding: 1;
    }

    #prompt-container {
        height: 5;
        dock: bottom;
        padding: 1;
    }

    #prompt-input {
        width: 100%;
        background: #2d3748;
        color: #e0e0e0;
        border: solid #4a5f4a;
    }

    #status-bar {
        height: 1;
        dock: bottom;
        padding: 0 1;
        background: #2d3748;
    }

    ProjectSelector {
        height: auto;
    }

    ImageList {
        height: 1fr;
    }

    MenuPanel {
        height: auto;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("g", "generate", "Generate"),
        Binding("b", "browse", "Browse"),
        Binding("v", "create_video", "Video"),
        Binding("o", "open_image", "Open"),
        Binding("tab", "toggle_select", "Select"),
        Binding("space", "toggle_select", "Select"),
        Binding("a", "select_all", "Select All"),
        Binding("d", "delete_selected", "Delete"),
        Binding("1", "select_project_1", "Wedding"),
        Binding("2", "select_project_2", "Latin"),
        Binding("3", "select_project_3", "DXP"),
        Binding("escape", "clear_selection", "Clear"),
        Binding("up", "cursor_up", "Up"),
        Binding("down", "cursor_down", "Down"),
        Binding("k", "cursor_up", "Up"),
        Binding("j", "cursor_down", "Down"),
    ]

    current_project = reactive("dxp-albs")  # Start with DXP where images exist

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Container(
                ProjectSelector(id="project-selector"),
                id="left-panel",
            ),
            Container(
                ImageList(id="image-list"),
                id="center-panel",
            ),
            Container(
                MenuPanel(id="menu-panel"),
                id="right-panel",
            ),
            id="main-container",
        )
        yield Container(
            Input(
                placeholder="Enter prompt for image generation... (press Enter)",
                id="prompt-input"
            ),
            id="prompt-container",
        )
        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app."""
        # Set initial project selector state
        selector = self.query_one("#project-selector", ProjectSelector)
        selector.selected = self.current_project
        self.refresh_images()

    @property
    def project(self) -> Project:
        """Get the current project."""
        return PROJECTS[self.current_project]

    @property
    def image_list(self) -> ImageList:
        """Get the image list widget."""
        return self.query_one("#image-list", ImageList)

    def refresh_images(self) -> None:
        """Refresh the image list."""
        images = replicate_client.get_project_images(self.project)
        self.image_list.set_images(images)
        self.set_status(f"{self.project.name}: {len(images)} images")

    def watch_current_project(self, project_slug: str) -> None:
        """Called when project changes."""
        selector = self.query_one("#project-selector", ProjectSelector)
        selector.selected = project_slug
        self.refresh_images()

    def set_status(self, message: str, working: bool = False) -> None:
        """Update the status bar."""
        status = self.query_one("#status-bar", StatusBar)
        status.message = message
        status.is_working = working

    # Project selection
    def action_select_project_1(self) -> None:
        self.current_project = "wedding-vision"

    def action_select_project_2(self) -> None:
        self.current_project = "latin-bible"

    def action_select_project_3(self) -> None:
        self.current_project = "dxp-albs"

    # Cursor movement
    def action_cursor_up(self) -> None:
        self.image_list.move_up()

    def action_cursor_down(self) -> None:
        self.image_list.move_down()

    # Selection
    def action_toggle_select(self) -> None:
        """Toggle selection of current image."""
        self.image_list.toggle_current()
        count = len(self.image_list.selected_indices)
        self.set_status(f"{count} images selected")

    def action_select_all(self) -> None:
        """Select all images."""
        self.image_list.select_all()
        count = len(self.image_list.selected_indices)
        self.set_status(f"Selected all {count} images")

    def action_clear_selection(self) -> None:
        """Clear all selections."""
        self.image_list.clear_selection()
        self.set_status("Selection cleared")

    def action_open_image(self) -> None:
        """Open the current image."""
        images = self.image_list.images
        cursor = self.image_list.cursor
        if images and 0 <= cursor < len(images):
            import subprocess
            subprocess.run(["open", str(images[cursor])])
            self.set_status(f"Opened: {images[cursor].name}")

    def action_delete_selected(self) -> None:
        """Delete selected images."""
        selected = self.image_list.selected_indices
        images = self.image_list.images
        if not selected:
            self.set_status("No images selected (Tab to select)")
            return
        count = 0
        for idx in sorted(selected, reverse=True):
            if idx < len(images):
                if replicate_client.delete_image(images[idx]):
                    count += 1
        self.refresh_images()
        self.set_status(f"Deleted {count} images")

    @work(exclusive=True, thread=True)
    def action_generate(self) -> None:
        """Generate images from prompt."""
        prompt_input = self.query_one("#prompt-input", Input)
        prompt = prompt_input.value.strip()

        if not prompt:
            self.call_from_thread(self.set_status, "Enter a prompt first")
            return

        self.call_from_thread(self.set_status, f"Generating with {self.project.name}...", True)

        try:
            paths = replicate_client.generate_image(self.project, prompt)
            self.call_from_thread(self.refresh_images)
            self.call_from_thread(self.set_status, f"Generated {len(paths)} image(s)")
            self.call_from_thread(lambda: setattr(prompt_input, "value", ""))
        except Exception as e:
            self.call_from_thread(self.set_status, f"Error: {str(e)[:50]}")

    @work(exclusive=True, thread=True)
    def action_create_video(self) -> None:
        """Create video from selected images."""
        selected = self.image_list.selected_indices
        images = self.image_list.images

        if not selected:
            self.call_from_thread(self.set_status, "Select images first (Tab or 'a' for all)")
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

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in prompt input."""
        if event.input.id == "prompt-input":
            self.action_generate()


def main():
    """Entry point."""
    app = HawkApp()
    app.run()


if __name__ == "__main__":
    main()
