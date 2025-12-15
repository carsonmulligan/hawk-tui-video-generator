"""Local image generation using Hugging Face Diffusers."""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable

# Fix macOS multiprocessing issue with diffusers
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

from hawk.config import Project, SD_MODEL, TIKTOK_WIDTH, TIKTOK_HEIGHT, SD_INFERENCE_STEPS, SD_GUIDANCE_SCALE
from hawk import logger

# Lazy load heavy imports
_pipeline = None
_current_model = None
_model_loaded = False


def is_model_cached(model_name: Optional[str] = None) -> bool:
    """Check if the model is already downloaded to HuggingFace cache."""
    model_name = model_name or SD_MODEL
    
    try:
        from huggingface_hub import try_to_load_from_cache, model_info
        
        # Check if model index file exists in cache
        cache_path = try_to_load_from_cache(model_name, "model_index.json")
        return cache_path is not None
    except Exception as e:
        logger.debug(f"Cache check failed: {e}")
        return False


def get_model_size(model_name: Optional[str] = None) -> str:
    """Get approximate download size for a model."""
    model_name = model_name or SD_MODEL
    
    # Approximate sizes for common models
    sizes = {
        "black-forest-labs/FLUX.1-schnell": "~23 GB",
        "black-forest-labs/FLUX.1-dev": "~23 GB",
        "stabilityai/stable-diffusion-xl-base-1.0": "~6.5 GB",
        "stabilityai/sdxl-turbo": "~6.5 GB",
        "stabilityai/stable-diffusion-3-medium-diffusers": "~12 GB",
        "runwayml/stable-diffusion-v1-5": "~4.3 GB",
        "stabilityai/stable-diffusion-2-1": "~5.2 GB",
        "SimianLuo/LCM_Dreamshaper_v7": "~4.0 GB",
    }
    return sizes.get(model_name, "~4-7 GB")


def preload_model(
    model_name: Optional[str] = None,
    progress_callback: Optional[Callable[[str], None]] = None,
) -> bool:
    """
    Download and load the model into memory.
    
    Args:
        model_name: Model to load (defaults to SD_MODEL)
        progress_callback: Optional callback for progress updates
    
    Returns:
        True if successful, False otherwise
    """
    global _pipeline, _current_model, _model_loaded
    
    model_name = model_name or SD_MODEL
    
    def update(msg: str):
        logger.info(msg)
        if progress_callback:
            progress_callback(msg)
    
    try:
        # Check if already loaded
        if _pipeline is not None and _current_model == model_name:
            update("Model already loaded")
            return True
        
        # Check if model is cached
        cached = is_model_cached(model_name)
        if cached:
            update(f"Loading {model_name} from cache...")
        else:
            update(f"Downloading {model_name} ({get_model_size(model_name)})...")
            update("This may take several minutes on first run...")
        
        # Import and load
        import torch
        
        # Fix macOS multiprocessing issue (fds_to_keep error)
        import multiprocessing
        try:
            multiprocessing.set_start_method("spawn", force=True)
        except RuntimeError:
            pass  # Already set
        
        from diffusers import AutoPipelineForText2Image
        
        # Determine device and dtype
        # Note: Flux requires bfloat16 on MPS (float16 produces black images)
        is_flux = "flux" in model_name.lower()
        
        if torch.cuda.is_available():
            device = "cuda"
            dtype = torch.bfloat16 if is_flux else torch.float16
            update("Using CUDA GPU")
        elif torch.backends.mps.is_available():
            device = "mps"
            # MPS + Flux requires bfloat16; other models use float16
            dtype = torch.bfloat16 if is_flux else torch.float16
            update(f"Using Apple Silicon (MPS) with {'bfloat16' if is_flux else 'float16'}")
        else:
            device = "cpu"
            dtype = torch.float32
            update("Using CPU (slow)")
        
        update("Loading model weights...")
        _pipeline = AutoPipelineForText2Image.from_pretrained(
            model_name,
            torch_dtype=dtype,
            use_safetensors=True,
        )
        
        update(f"Moving model to {device}...")
        _pipeline = _pipeline.to(device)
        _current_model = model_name
        _model_loaded = True
        
        # Enable memory optimizations
        if device == "cuda":
            _pipeline.enable_model_cpu_offload()
        
        update("Model ready!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        if progress_callback:
            progress_callback(f"Error: {e}")
        return False


def is_model_loaded() -> bool:
    """Check if a model is currently loaded in memory."""
    return _model_loaded and _pipeline is not None


def _get_pipeline(model_name: Optional[str] = None):
    """Get or create the diffusion pipeline (lazy loaded)."""
    global _pipeline, _current_model, _model_loaded
    
    model_name = model_name or SD_MODEL
    
    # Return cached pipeline if same model
    if _pipeline is not None and _current_model == model_name:
        return _pipeline
    
    # Load the model
    success = preload_model(model_name)
    if not success:
        raise RuntimeError(f"Failed to load model {model_name}")
    
    return _pipeline


def is_available() -> bool:
    """Check if local image generation is available (torch installed)."""
    try:
        import torch
        return True
    except ImportError:
        return False


def get_device_info() -> dict:
    """Get information about available compute devices."""
    try:
        import torch
        return {
            "cuda": torch.cuda.is_available(),
            "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "mps": torch.backends.mps.is_available(),
            "cpu": True,
        }
    except ImportError:
        return {"cuda": False, "mps": False, "cpu": True}


def list_available_models() -> list[str]:
    """Return list of recommended models for local generation."""
    return [
        "black-forest-labs/FLUX.1-schnell",  # Best quality, fast (4 steps)
        "black-forest-labs/FLUX.1-dev",  # Best quality, slower (20+ steps)
        "stabilityai/sdxl-turbo",  # Good quality, fast
        "stabilityai/stable-diffusion-xl-base-1.0",  # Good quality, slow
        "SimianLuo/LCM_Dreamshaper_v7",  # Fast, smaller
        "runwayml/stable-diffusion-v1-5",  # Classic, small
    ]


def _aspect_to_dimensions(aspect_ratio: str) -> tuple[int, int]:
    """Convert aspect ratio string to width/height dimensions."""
    ratios = {
        "9:16": (768, 1344),   # TikTok portrait (SDXL optimized)
        "16:9": (1344, 768),   # Landscape
        "1:1": (1024, 1024),   # Square
        "4:3": (1152, 896),    # Classic
        "3:4": (896, 1152),    # Portrait classic
    }
    return ratios.get(aspect_ratio, (768, 1344))


def generate_image(
    project: Project,
    prompt: str,
    num_outputs: int = 1,
    aspect_ratio: str = "9:16",
    seed: Optional[int] = None,
    model: Optional[str] = None,
    num_inference_steps: Optional[int] = None,
    guidance_scale: Optional[float] = None,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
) -> list[Path]:
    """
    Generate images using local Stable Diffusion.
    
    Args:
        project: Project to save images to
        prompt: Text prompt for generation
        num_outputs: Number of images to generate
        aspect_ratio: Aspect ratio (9:16, 16:9, 1:1, etc.)
        seed: Optional seed for reproducibility
        model: Model to use (defaults to SD_MODEL from config)
        num_inference_steps: Denoising steps (defaults to SD_INFERENCE_STEPS)
        guidance_scale: How closely to follow the prompt (defaults to SD_GUIDANCE_SCALE)
        progress_callback: Optional callback(step, total_steps, status) for progress updates
    
    Returns:
        List of paths to generated images
    """
    # Use config defaults if not specified
    if num_inference_steps is None:
        num_inference_steps = SD_INFERENCE_STEPS
    if guidance_scale is None:
        guidance_scale = SD_GUIDANCE_SCALE
    
    logger.info(f"Generation settings: steps={num_inference_steps}, guidance={guidance_scale}")
    
    # Truncate prompt to fit CLIP's 77 token limit (~250 chars)
    MAX_PROMPT_CHARS = 250
    if len(prompt) > MAX_PROMPT_CHARS:
        truncated = prompt[:MAX_PROMPT_CHARS]
        last_break = max(truncated.rfind(","), truncated.rfind(" "))
        if last_break > 150:
            prompt = truncated[:last_break].rstrip(",").strip()
        else:
            prompt = truncated.strip()
        logger.warning(f"Prompt truncated to {len(prompt)} chars (CLIP 77 token limit)")
    
    import torch
    
    project.ensure_dirs()
    
    pipeline = _get_pipeline(model)
    width, height = _aspect_to_dimensions(aspect_ratio)
    
    # Set up generator for reproducibility
    device = pipeline.device
    generator = None
    if seed is not None:
        generator = torch.Generator(device=device).manual_seed(seed)
    
    saved_paths = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create step callback for progress updates
    # Note: Different pipelines use different callback signatures
    def step_callback(pipe, step, timestep, callback_kwargs):
        if progress_callback:
            progress_callback(step + 1, num_inference_steps, f"Step {step + 1}/{num_inference_steps}")
        return callback_kwargs
    
    for i in range(num_outputs):
        if progress_callback:
            progress_callback(0, num_inference_steps, f"Generating image {i + 1}/{num_outputs}...")
        
        # Build pipeline kwargs - not all pipelines support all params
        pipe_kwargs = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_inference_steps": num_inference_steps,
            "generator": generator,
        }
        
        # Only add guidance_scale if > 0 (Flux doesn't use it)
        if guidance_scale > 0:
            pipe_kwargs["guidance_scale"] = guidance_scale
        
        # Try to add callback - not all pipelines support it
        try:
            pipe_kwargs["callback_on_step_end"] = step_callback
            result = pipeline(**pipe_kwargs)
        except TypeError:
            # Fallback without callback if not supported
            del pipe_kwargs["callback_on_step_end"]
            if progress_callback:
                progress_callback(1, num_inference_steps, f"Generating... (no step progress for this model)")
            result = pipeline(**pipe_kwargs)
        
        image = result.images[0]
        
        # Resize to exact TikTok dimensions if needed
        if aspect_ratio == "9:16" and (image.width != TIKTOK_WIDTH or image.height != TIKTOK_HEIGHT):
            from PIL import Image
            image = image.resize((TIKTOK_WIDTH, TIKTOK_HEIGHT), Image.LANCZOS)
        
        # Save image
        safe_prompt = "".join(c if c.isalnum() or c in " -_" else "" for c in prompt[:30])
        safe_prompt = safe_prompt.strip().replace(" ", "_")
        filename = f"{timestamp}_{safe_prompt}_{i+1}.png"
        filepath = project.images_dir / filename
        
        image.save(filepath, "PNG")
        saved_paths.append(filepath)
    
    return saved_paths


def unload_model():
    """Unload the model from memory to free up VRAM/RAM."""
    global _pipeline, _current_model
    if _pipeline is not None:
        del _pipeline
        _pipeline = None
        _current_model = None
        
        # Force garbage collection
        import gc
        gc.collect()
        
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass


def imgcat(image_path: Path, width: int = 40) -> str:
    """
    Generate iTerm2 imgcat escape sequence for displaying image in terminal.
    
    Args:
        image_path: Path to the image file
        width: Display width in terminal columns
    
    Returns:
        Escape sequence string to display the image
    """
    import base64
    
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    b64_data = base64.b64encode(image_data).decode("ascii")
    
    # iTerm2 inline image protocol
    # \033]1337;File=inline=1;width=Ncols:BASE64\007
    return f"\033]1337;File=inline=1;width={width}:{b64_data}\007"


def print_image(image_path: Path, width: int = 40) -> None:
    """Print an image to the terminal using iTerm2 imgcat protocol."""
    import sys
    print(imgcat(image_path, width), file=sys.stdout, flush=True)

