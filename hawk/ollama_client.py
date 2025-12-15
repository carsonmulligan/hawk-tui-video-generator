"""Ollama client for prompt enhancement using local LLMs."""

import httpx
from typing import Optional

from hawk.config import OLLAMA_HOST, OLLAMA_MODEL
from hawk import logger

# System prompt for enhancing image generation prompts
# CLIP tokenizer limit is 77 tokens - we enforce ~50 words max
ENHANCE_SYSTEM_PROMPT = """Enhance this prompt for Stable Diffusion. 

STRICT LIMIT: Maximum 50 words. Use comma-separated phrases only.

Add: style, lighting, mood, quality keywords (8k, detailed, cinematic).
Output ONLY the enhanced prompt - no explanations."""

# Maximum characters for enhanced prompts (77 tokens ≈ 250 chars)
MAX_PROMPT_CHARS = 250


def list_models() -> list[str]:
    """List available Ollama models."""
    try:
        response = httpx.get(f"{OLLAMA_HOST}/api/tags", timeout=10.0)
        response.raise_for_status()
        data = response.json()
        return [model["name"] for model in data.get("models", [])]
    except Exception:
        return []


def is_available() -> bool:
    """Check if Ollama server is running and accessible."""
    try:
        logger.debug(f"Checking Ollama availability at {OLLAMA_HOST}")
        response = httpx.get(f"{OLLAMA_HOST}/api/tags", timeout=5.0)
        available = response.status_code == 200
        logger.debug(f"Ollama available: {available}")
        return available
    except Exception as e:
        logger.debug(f"Ollama not available: {e}")
        return False


def enhance_prompt(
    prompt: str,
    model: Optional[str] = None,
    style_hint: Optional[str] = None,
) -> str:
    """
    Enhance a basic prompt using Ollama LLM.
    
    Args:
        prompt: The user's basic prompt
        model: Ollama model to use (defaults to config OLLAMA_MODEL)
        style_hint: Optional style guidance (e.g., "cinematic", "anime", "photorealistic")
    
    Returns:
        Enhanced prompt string, or original prompt if enhancement fails
    """
    model = model or OLLAMA_MODEL
    
    user_message = f"Enhance this image generation prompt: {prompt}"
    if style_hint:
        user_message += f"\n\nDesired style: {style_hint}"
    
    try:
        logger.debug(f"Sending prompt to Ollama model {model}")
        response = httpx.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": ENHANCE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                "stream": False,
            },
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()
        enhanced = data.get("message", {}).get("content", "").strip()
        
        if not enhanced:
            logger.warning("Ollama returned empty response")
            return prompt
        
        # Enforce token limit - truncate if too long
        if len(enhanced) > MAX_PROMPT_CHARS:
            # Truncate at last comma or space before limit
            truncated = enhanced[:MAX_PROMPT_CHARS]
            last_break = max(truncated.rfind(","), truncated.rfind(" "))
            if last_break > 150:
                enhanced = truncated[:last_break].rstrip(",").strip()
            else:
                enhanced = truncated.strip()
            logger.warning(f"Ollama prompt truncated: {len(enhanced)} chars (max {MAX_PROMPT_CHARS})")
        
        logger.info(f"Ollama enhanced prompt ({len(prompt)} -> {len(enhanced)} chars)")
        return enhanced
    except Exception as e:
        # Return original prompt if enhancement fails
        logger.error(f"Ollama enhancement failed: {type(e).__name__}: {e}")
        return prompt


def generate_prompts(
    topic: str,
    count: int = 5,
    model: Optional[str] = None,
    style: Optional[str] = None,
) -> list[str]:
    """
    Generate multiple image prompts for a given topic.
    
    Args:
        topic: The subject/theme to generate prompts for
        count: Number of prompts to generate
        model: Ollama model to use
        style: Optional style constraint
    
    Returns:
        List of generated prompts
    """
    model = model or OLLAMA_MODEL
    
    system = """You are an expert at creating diverse, creative prompts for AI image generation.
Generate prompts that are visually descriptive and varied in composition, lighting, and mood.
Return each prompt on a new line, numbered 1-N. No other text."""

    user_message = f"Generate {count} diverse image prompts about: {topic}"
    if style:
        user_message += f"\nStyle: {style}"
    
    try:
        response = httpx.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_message},
                ],
                "stream": False,
            },
            timeout=120.0,
        )
        response.raise_for_status()
        data = response.json()
        content = data.get("message", {}).get("content", "")
        
        # Parse numbered list
        prompts = []
        for line in content.strip().split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                # Remove number prefix like "1. " or "1) "
                parts = line.split(". ", 1) if ". " in line else line.split(") ", 1)
                if len(parts) > 1:
                    prompts.append(parts[1].strip())
                else:
                    prompts.append(line)
        
        return prompts[:count] if prompts else []
    except Exception:
        return []

