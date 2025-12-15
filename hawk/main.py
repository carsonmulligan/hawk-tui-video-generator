"""Hawk TUI entry point."""

import os
import sys

# Fix macOS multiprocessing issue - must be set before any imports
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"


def _preload_local_model():
    """Preload the local SD model before starting TUI."""
    from hawk.config import SD_MODEL, SD_INFERENCE_STEPS, SD_GUIDANCE_SCALE
    from hawk import local_image_gen

    print(f"Loading local image model...")
    print(f"   Model: {SD_MODEL}")
    print(f"   Settings: {SD_INFERENCE_STEPS} steps, guidance={SD_GUIDANCE_SCALE}")

    if not local_image_gen.is_model_cached():
        size = local_image_gen.get_model_size()
        print(f"Downloading {SD_MODEL} ({size})...")
        print("   This is a one-time download, please wait...")
    else:
        print(f"Loading from cache...")

    def progress(msg):
        print(f"   {msg}")

    success = local_image_gen.preload_model(progress_callback=progress)

    if success:
        print("Model ready! Starting TUI...\n")
    else:
        print("Failed to load model. Check logs for details.")
        print("   You can still use Replicate by setting USE_LOCAL_IMAGE_GEN=false\n")

    return success


def _print_help():
    """Print help message."""
    print("""
Hawk TUI - Terminal-based TikTok Video Creator

Usage:
  hawk              Start the TUI application
  hawk init         Interactive setup wizard (first-time setup)
  hawk config       Show current configuration
  hawk --help       Show this help message
  hawk --version    Show version

Getting Started:
  1. Run 'hawk init' to configure settings
  2. Run 'hawk' to start creating videos

For more info: https://github.com/carsonmulligan/hawktui
""")


def _print_version():
    """Print version."""
    print("hawk-tui 1.0.0")


def main():
    """Main entry point."""
    args = sys.argv[1:]

    # Handle subcommands
    if args:
        cmd = args[0].lower()

        if cmd in ("init", "setup"):
            from hawk.setup import run_setup
            run_setup()
            return

        if cmd == "config":
            from hawk.setup import show_config
            show_config()
            return

        if cmd in ("--help", "-h", "help"):
            _print_help()
            return

        if cmd in ("--version", "-v", "version"):
            _print_version()
            return

        # Unknown command
        print(f"Unknown command: {cmd}")
        print("Run 'hawk --help' for usage information.")
        sys.exit(1)

    # Check if first run (no config and no .env)
    from hawk.setup import config_exists
    from pathlib import Path

    has_env = Path(".env").exists() or os.getenv("REPLICATE_API_TOKEN") or os.getenv("USE_LOCAL_IMAGE_GEN")

    if not config_exists() and not has_env:
        print("Welcome to Hawk TUI!")
        print("It looks like this is your first time running hawk.\n")
        print("Run 'hawk init' to set up your configuration.")
        print("Or set USE_LOCAL_IMAGE_GEN=true to use local image generation.\n")
        response = input("Would you like to run setup now? [Y/n]: ").strip().lower()
        if response in ("", "y", "yes"):
            from hawk.setup import run_setup
            run_setup()
            return
        print("\nStarting with defaults (local image generation)...\n")

    # Import config after potential setup
    from hawk.config import USE_LOCAL_IMAGE_GEN

    # Preload local model BEFORE starting Textual (avoids multiprocessing conflicts)
    if USE_LOCAL_IMAGE_GEN:
        _preload_local_model()

    from hawk.app import HawkTUI
    app = HawkTUI()
    app.run()


if __name__ == "__main__":
    main()
