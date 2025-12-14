"""Splash screen for HawkTUI."""

from textual.screen import Screen
from textual.widgets import Static
from textual.app import ComposeResult
from textual.containers import Center, Middle

SPLASH_CONTENT = """[bold #c9a227]
██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗████████╗██╗   ██╗██╗
██║  ██║██╔══██╗██║    ██║██║ ██╔╝╚══██╔══╝██║   ██║██║
███████║███████║██║ █╗ ██║█████╔╝    ██║   ██║   ██║██║
██╔══██║██╔══██║██║███╗██║██╔═██╗    ██║   ██║   ██║██║
██║  ██║██║  ██║╚███╔███╔╝██║  ██╗   ██║   ╚██████╔╝██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝[/]

[#4a5f4a]         ╔═══════════════════════════════════╗
         ║     TikTok Video Creator TUI      ║
         ╚═══════════════════════════════════╝[/]

[dim]      // Powered by Claude Code Agent SDK + Replicate[/]

                        [#8B7355]▄▄▄▄▄[/]
                      [#8B7355]▄█[/][#D2B48C]████[/][#8B7355]█▄[/]
                     [#8B7355]█[/][#D2B48C]██████[/][#8B7355]██[/]
                    [#D2B48C]███[/][#2F2F2F]●[/][#D2B48C]████[/][#8B7355]█▄[/]
                   [#D2B48C]████████[/][#c9a227]▀[/][#6B5344]▄▄[/]
                   [#F5DEB3]█[/][#D2B48C]███████[/][#6B5344]█[/]
                  [#F5DEB3]██[/][#8B7355]▄[/][#D2B48C]██████[/][#6B5344]█[/]
                  [#F5DEB3]██[/][#8B7355]█▄[/][#D2B48C]█████[/][#6B5344]█[/]
                 [#F5DEB3]███[/][#8B7355]██▄[/][#D2B48C]████[/][#6B5344]█[/]
                 [#F5DEB3]███[/][#8B7355]███▄[/][#D2B48C]███[/][#6B5344]█[/]
                [#F5DEB3]████[/][#8B7355]████▄[/][#D2B48C]██[/][#6B5344]█[/]
                [#F5DEB3]████[/][#8B7355]█████▄[/][#6B5344]██[/]
                [#F5DEB3]███[/][#8B7355]███████[/][#6B5344]█[/]
                 [#F5DEB3]██[/][#8B7355]███████[/][#6B5344]█[/]
                  [#8B7355]████████[/][#6B5344]▀[/]
                   [#c9a227]█▀[/]   [#c9a227]▀█[/]
                  [#c9a227]██[/]     [#c9a227]██[/]
                 [#6B5344]▄██[/]     [#6B5344]██▄[/]
              [#4a4a4a]▄▄███▄▄▄▄▄███▄▄[/]


[bold #c9a227]              ▶ Press ENTER to continue ◀[/]
"""


class SplashScreen(Screen):
    """Splash screen with HawkTUI branding."""

    CSS = """
    SplashScreen {
        background: #1a1d23;
        align: center middle;
    }

    #splash-text {
        width: auto;
        height: auto;
        text-align: center;
    }
    """

    BINDINGS = [
        ("enter", "continue", "Continue"),
        ("space", "continue", "Continue"),
        ("escape", "continue", "Continue"),
    ]

    def compose(self) -> ComposeResult:
        yield Middle(
            Center(
                Static(SPLASH_CONTENT, id="splash-text")
            )
        )

    def action_continue(self) -> None:
        """Continue to main app."""
        self.dismiss()
