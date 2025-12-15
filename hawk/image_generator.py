"""Image generation abstraction layer.

Routes to either Replicate API or local Diffusers based on configuration.
Optionally enhances prompts using Ollama when enabled.
"""

from pathlib import Path
from typing import Optional, Callable

from hawk.config import (
    Project,
    USE_OLLAMA,
    USE_LOCAL_IMAGE_GEN,
    OLLAMA_MODEL,
    SD_MODEL,
)
from hawk import logger


def get_backend_info() -> dict:
    """Get information about current backend configuration."""
    info = {
        "image_backend": "local" if USE_LOCAL_IMAGE_GEN else "replicate",
        "prompt_enhancement": USE_OLLAMA,
        "ollama_model": OLLAMA_MODEL if USE_OLLAMA else None,
        "image_model": SD_MODEL if USE_LOCAL_IMAGE_GEN else "replicate",
    }
    
    # Check availability
    if USE_LOCAL_IMAGE_GEN:
        from hawk import local_image_gen
        info["local_available"] = local_image_gen.is_available()
        info["device_info"] = local_image_gen.get_device_info()
    
    if USE_OLLAMA:
        from hawk import ollama_client
        info["ollama_available"] = ollama_client.is_available()
    
    return info


def get_backend_status() -> str:
    """Get a short status string for display in TUI."""
    parts = []
    
    if USE_LOCAL_IMAGE_GEN:
        from hawk import local_image_gen
        if local_image_gen.is_available():
            device = local_image_gen.get_device_info()
            if device["cuda"]:
                parts.append(f"Local (CUDA)")
            elif device["mps"]:
                parts.append(f"Local (MPS)")
            else:
                parts.append(f"Local (CPU)")
        else:
            parts.append("Local (unavailable)")
    else:
        parts.append("Replicate")
    
    if USE_OLLAMA:
        from hawk import ollama_client
        if ollama_client.is_available():
            parts.append(f"Ollama:{OLLAMA_MODEL}")
        else:
            parts.append("Ollama (offline)")
    
    return " | ".join(parts)


def _maybe_enhance_prompt(prompt: str, style_hint: Optional[str] = None) -> tuple[str, bool]:
    """
    Enhance prompt with Ollama if enabled.
    
    Returns:
        Tuple of (prompt, was_enhanced)
    """
    if not USE_OLLAMA:
        return prompt, False
    
    from hawk import ollama_client
    
    if not ollama_client.is_available():
        return prompt, False
    
    enhanced = ollama_client.enhance_prompt(prompt, style_hint=style_hint)
    return enhanced, enhanced != prompt


def generate_image(
    project: Project,
    prompt: str,
    num_outputs: int = 1,
    aspect_ratio: str = "9:16",
    seed: Optional[int] = None,
    enhance_prompt: bool = True,
    style_hint: Optional[str] = None,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
) -> tuple[list[Path], dict]:
    """
    Generate images using the configured backend.
    
    Args:
        project: Project to save images to
        prompt: Text prompt for generation
        num_outputs: Number of images to generate
        aspect_ratio: Aspect ratio string
        seed: Optional seed for reproducibility
        enhance_prompt: Whether to use Ollama for prompt enhancement (if enabled)
        style_hint: Optional style guidance for prompt enhancement
        progress_callback: Optional callback(step, total, status) for progress updates
    
    Returns:
        Tuple of (list of image paths, metadata dict)
    """
    backend = "local" if USE_LOCAL_IMAGE_GEN else "replicate"
    logger.info(f"Starting image generation: backend={backend}, project={project.slug}")
    logger.debug(f"Prompt: {prompt[:100]}...")
    
    metadata = {
        "original_prompt": prompt,
        "enhanced": False,
        "backend": backend,
    }
    
    # Optionally enhance prompt
    final_prompt = prompt
    if enhance_prompt and USE_OLLAMA:
        if progress_callback:
            progress_callback(0, 1, "Enhancing prompt with Ollama...")
        logger.info(f"Enhancing prompt with Ollama ({OLLAMA_MODEL})...")
        final_prompt, was_enhanced = _maybe_enhance_prompt(prompt, style_hint)
        metadata["enhanced"] = was_enhanced
        metadata["final_prompt"] = final_prompt
        if was_enhanced:
            logger.info(f"Prompt enhanced successfully")
            logger.debug(f"Enhanced prompt: {final_prompt[:100]}...")
        else:
            logger.warning("Prompt enhancement failed or returned unchanged")
    
    # Generate using appropriate backend
    try:
        if USE_LOCAL_IMAGE_GEN:
            from hawk import local_image_gen
            
            logger.info(f"Generating with local Diffusers ({SD_MODEL})...")
            paths = local_image_gen.generate_image(
                project=project,
                prompt=final_prompt,
                num_outputs=num_outputs,
                aspect_ratio=aspect_ratio,
                seed=seed,
                progress_callback=progress_callback,
            )
            metadata["model"] = SD_MODEL
        else:
            from hawk import replicate_client
            
            logger.info(f"Generating with Replicate ({project.model})...")
            paths = replicate_client.generate_image(
                project=project,
                prompt=final_prompt,
                num_outputs=num_outputs,
                aspect_ratio=aspect_ratio,
                seed=seed,
            )
            metadata["model"] = project.model
        
        logger.info(f"Generated {len(paths)} image(s): {[p.name for p in paths]}")
        return paths, metadata
        
    except Exception as e:
        logger.error(f"Image generation failed: {type(e).__name__}: {e}")
        raise


def generate_batch(
    project: Project,
    prompts: list[str],
    aspect_ratio: str = "9:16",
    enhance_prompts: bool = True,
) -> tuple[list[Path], list[dict]]:
    """Generate images for multiple prompts."""
    all_paths = []
    all_metadata = []
    
    for prompt in prompts:
        paths, meta = generate_image(
            project=project,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            enhance_prompt=enhance_prompts,
        )
        all_paths.extend(paths)
        all_metadata.append(meta)
    
    return all_paths, all_metadata


# Re-export utility functions from replicate_client for backwards compatibility
from hawk.replicate_client import get_project_images, delete_image

