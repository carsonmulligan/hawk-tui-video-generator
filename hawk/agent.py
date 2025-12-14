"""Claude Agent SDK integration for Hawk TUI."""

import asyncio
from claude_agent_sdk import query, ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, ResultMessage, TextBlock


async def _run_query(prompt: str, system_prompt: str = "", max_tokens: int = 500) -> str:
    """Run a query and extract text response."""
    options = ClaudeAgentOptions(
        max_tokens=max_tokens,
        system_prompt=system_prompt if system_prompt else None,
    )

    result_text = ""
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    result_text += block.text
        elif isinstance(message, ResultMessage):
            if message.result:
                result_text = message.result

    return result_text.strip()


async def enhance_prompt(base_prompt: str, style: str = "futuristic") -> str:
    """
    Use Claude to enhance a sparse prompt into something more evocative.

    Args:
        base_prompt: The user's basic prompt idea
        style: The style context (futuristic, wedding, religious)

    Returns:
        Enhanced prompt optimized for image generation
    """
    system = f"""You are a prompt engineer for AI image generation models.
Given a sparse prompt, enhance it while keeping it concise (under 20 words).
Style context: {style}
Keep the original concept intact. Add atmospheric details.
Output ONLY the enhanced prompt, nothing else."""

    return await _run_query(
        prompt=f"Enhance this prompt: {base_prompt}",
        system_prompt=system,
        max_tokens=100
    )


async def generate_prompt_variations(
    core_concept: str,
    count: int = 5,
    style: str = "futuristic",
    twist: str = ""
) -> list[str]:
    """
    Generate multiple prompt variations from a core concept.

    Args:
        core_concept: The main idea (e.g., "cloaked wanderer intergalactique")
        count: Number of variations to generate
        style: Style context
        twist: Additional thematic element (e.g., "ancient egyptian")

    Returns:
        List of varied prompts
    """
    system = f"""You are a prompt engineer for AI image generation.
Generate {count} distinct variations of a concept.
Style: {style}
{"Additional theme to weave in: " + twist if twist else ""}

Rules:
- Keep each prompt sparse (10-15 words max)
- Each variation should feel different but cohesive
- Focus on atmosphere, setting, and visual elements
- Output ONLY the prompts, one per line, numbered 1-{count}"""

    response = await _run_query(
        prompt=f"Generate {count} variations of: {core_concept}",
        system_prompt=system,
        max_tokens=500
    )

    # Parse numbered prompts
    lines = response.strip().split('\n')
    prompts = []
    for line in lines:
        # Remove numbering like "1.", "1)", "1:"
        cleaned = line.strip()
        for i in range(1, count + 2):
            for sep in ['. ', ') ', ': ', '- ']:
                prefix = f"{i}{sep}"
                if cleaned.startswith(prefix):
                    cleaned = cleaned[len(prefix):]
                    break
        if cleaned and len(cleaned) > 5:
            prompts.append(cleaned)

    return prompts[:count]


async def generate_captions(
    prompts: list[str],
    style: str = "mysterious"
) -> list[str]:
    """
    Generate short TikTok captions for a series of images.

    Args:
        prompts: The prompts used to generate images
        style: Caption style (mysterious, poetic, dramatic)

    Returns:
        List of short captions
    """
    system = f"""Generate ultra-short TikTok captions (3-6 words each).
Style: {style}
Make them punchy and atmospheric.
Output one caption per line, matching the input order."""

    prompt_list = "\n".join(f"{i+1}. {p}" for i, p in enumerate(prompts))

    response = await _run_query(
        prompt=f"Generate captions for these images:\n{prompt_list}",
        system_prompt=system,
        max_tokens=200
    )

    # Parse captions
    lines = response.strip().split('\n')
    captions = []
    for line in lines:
        cleaned = line.strip()
        # Remove numbering
        for i in range(1, len(prompts) + 2):
            for sep in ['. ', ') ', ': ', '- ']:
                prefix = f"{i}{sep}"
                if cleaned.startswith(prefix):
                    cleaned = cleaned[len(prefix):]
                    break
        if cleaned:
            captions.append(cleaned)

    return captions[:len(prompts)]


# Synchronous wrappers for TUI use
def enhance_prompt_sync(base_prompt: str, style: str = "futuristic") -> str:
    """Sync wrapper for enhance_prompt."""
    return asyncio.run(enhance_prompt(base_prompt, style))


def generate_prompt_variations_sync(
    core_concept: str,
    count: int = 5,
    style: str = "futuristic",
    twist: str = ""
) -> list[str]:
    """Sync wrapper for generate_prompt_variations."""
    return asyncio.run(generate_prompt_variations(core_concept, count, style, twist))


def generate_captions_sync(prompts: list[str], style: str = "mysterious") -> list[str]:
    """Sync wrapper for generate_captions."""
    return asyncio.run(generate_captions(prompts, style))
