"""Hawk TUI entry point."""

import os

# Fix macOS multiprocessing issue - must be set before any imports
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

from hawk.config import USE_LOCAL_IMAGE_GEN, SD_MODEL, SD_INFERENCE_STEPS, SD_GUIDANCE_SCALE


def _preload_local_model():
    """Preload the local SD model before starting TUI."""
    from hawk import local_image_gen
    
    print(f"🚀 HawkTUI - Loading local image model...")
    print(f"   Model: {SD_MODEL}")
    print(f"   Settings: {SD_INFERENCE_STEPS} steps, guidance={SD_GUIDANCE_SCALE}")
    
    if not local_image_gen.is_model_cached():
        size = local_image_gen.get_model_size()
        print(f"📥 Downloading {SD_MODEL} ({size})...")
        print("   This is a one-time download, please wait...")
    else:
        print(f"📦 Loading from cache...")
    
    def progress(msg):
        print(f"   {msg}")
    
    success = local_image_gen.preload_model(progress_callback=progress)
    
    if success:
        print("✅ Model ready! Starting TUI...\n")
    else:
        print("❌ Failed to load model. Check logs for details.")
        print("   You can still use Replicate by setting USE_LOCAL_IMAGE_GEN=false\n")
    
    return success


def main():
    """Main entry point."""
    # Preload local model BEFORE starting Textual (avoids multiprocessing conflicts)
    if USE_LOCAL_IMAGE_GEN:
        _preload_local_model()
    
    from hawk.app import HawkTUI
    app = HawkTUI()
    app.run()


if __name__ == "__main__":
    main()
