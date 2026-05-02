import asyncio
import os
import uuid
from huggingface_hub import InferenceClient
from app.config import (
    HUGGINGFACE_API_KEY, HUGGINGFACE_IMAGE_MODEL, IMAGE_DIR,
    IMAGE_GENERATION_TIMEOUT, MAX_IMAGE_RETRIES, IMAGE_WIDTH, IMAGE_HEIGHT
)


class ImageGenerationAgent:
    """
    AI Agent responsible for generating professional images for pitch deck slides
    using the Z-Image-Turbo model from Hugging Face.

    Pipeline:
    1. Receives slide content and image prompts from the creative agent
    2. Enhances prompts with cinematic/professional styling
    3. Generates images via Z-Image-Turbo (optimized turbo diffusion)
    4. Validates and saves images
    5. Returns image paths mapped to slide numbers
    """

    def __init__(self):
        self.client = InferenceClient(
            model=HUGGINGFACE_IMAGE_MODEL,
            token=HUGGINGFACE_API_KEY,
            timeout=IMAGE_GENERATION_TIMEOUT,
        )
        self.model_name = HUGGINGFACE_IMAGE_MODEL
        os.makedirs(IMAGE_DIR, exist_ok=True)

    def _enhance_prompt(self, raw_prompt: str, slide_context: str = "") -> str:
        """
        Enhance a raw image prompt with Z-Image-Turbo optimized parameters.
        The model excels with detailed, cinematic descriptions.
        """
        style_prefix = (
            "Professional cinematic photography for a corporate pitch deck presentation, "
        )
        style_suffix = (
            ", minimalist modern corporate aesthetic, 8k ultra high resolution, "
            "highly detailed textures, clean geometric composition, "
            "soft diffused studio lighting with rim highlights, "
            "professional color grading, tack sharp focus, high contrast, "
            "clean gradient background, photorealistic rendering"
        )

        if slide_context:
            context_hint = f" representing {slide_context},"
        else:
            context_hint = ""

        enhanced = f"{style_prefix}{raw_prompt}{context_hint}{style_suffix}"
        return enhanced

    def _generate_single_image(self, prompt: str) -> str:
        """
        Synchronous image generation using Z-Image-Turbo.
        Uses guidance_scale=0.0 and 2 inference steps (turbo/distilled model optimization).
        """
        enhanced_prompt = self._enhance_prompt(prompt)

        for attempt in range(MAX_IMAGE_RETRIES + 1):
            try:
                image = self.client.text_to_image(
                    enhanced_prompt,
                    guidance_scale=0.0,
                    num_inference_steps=2,
                    width=IMAGE_WIDTH,
                    height=IMAGE_HEIGHT,
                )

                image_name = f"{uuid.uuid4()}.png"
                image_path = os.path.join(IMAGE_DIR, image_name)
                image.save(image_path)

                if os.path.exists(image_path) and os.path.getsize(image_path) > 0:
                    return image_path

            except Exception as e:
                if attempt < MAX_IMAGE_RETRIES:
                    continue
                self._log_error(prompt, str(e))
                return ""

        return ""

    async def generate_image(self, prompt: str) -> str:
        """Async wrapper for single image generation."""
        return await asyncio.to_thread(self._generate_single_image, prompt)

    async def run(self, creative_data: dict) -> dict:
        """
        Main agent entry point. Processes all slides and generates images
        for those with image_prompt fields.

        Args:
            creative_data: Dict with 'slides' list from creative agent

        Returns:
            Updated creative_data with 'image_path' added to relevant slides
        """
        slides = creative_data.get("slides", [])

        image_tasks = []
        image_indices = []

        for i, slide in enumerate(slides):
            if slide.get("image_prompt"):
                image_tasks.append(self.generate_image(slide["image_prompt"]))
                image_indices.append(i)

        if not image_tasks:
            return creative_data

        image_results = await asyncio.gather(*image_tasks, return_exceptions=True)

        for idx, result in zip(image_indices, image_results):
            if isinstance(result, str) and result:
                creative_data["slides"][idx]["image_path"] = result
            elif isinstance(result, Exception):
                self._log_error(
                    creative_data["slides"][idx].get("image_prompt", ""),
                    str(result)
                )

        generated_count = sum(1 for r in image_results if isinstance(r, str) and r)
        creative_data["image_generation_stats"] = {
            "total_requested": len(image_tasks),
            "successfully_generated": generated_count,
            "failed": len(image_tasks) - generated_count,
            "model": self.model_name,
        }

        return creative_data

    def _log_error(self, prompt: str, error: str):
        """Log image generation errors for debugging."""
        log_path = os.path.join(IMAGE_DIR, "generation_errors.log")
        try:
            with open(log_path, "a") as f:
                f.write(f"Model: {self.model_name}\n")
                f.write(f"Prompt: {prompt[:200]}\n")
                f.write(f"Error: {error}\n")
                f.write("---\n")
        except Exception:
            pass


# Singleton instance for the agent pipeline
image_agent = ImageGenerationAgent()


async def run(creative_data: dict) -> dict:
    """Module-level entry point matching the agent pipeline pattern."""
    return await image_agent.run(creative_data)
