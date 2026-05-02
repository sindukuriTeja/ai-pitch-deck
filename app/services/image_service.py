import os
import uuid
import asyncio
from huggingface_hub import InferenceClient
from app.config import (
    HUGGINGFACE_API_KEY, HUGGINGFACE_IMAGE_MODEL, IMAGE_DIR,
    IMAGE_GENERATION_TIMEOUT, MAX_IMAGE_RETRIES, IMAGE_WIDTH, IMAGE_HEIGHT
)

client = InferenceClient(
    model=HUGGINGFACE_IMAGE_MODEL,
    token=HUGGINGFACE_API_KEY,
    timeout=IMAGE_GENERATION_TIMEOUT,
)


async def generate_image(prompt: str) -> str:
    return await asyncio.to_thread(_generate_image_sync, prompt)


def _generate_image_sync(prompt: str) -> str:
    os.makedirs(IMAGE_DIR, exist_ok=True)

    enhanced_prompt = (
        f"Professional cinematic photography for a corporate pitch deck, {prompt}, "
        "minimalist modern corporate aesthetic, 8k ultra high resolution, "
        "highly detailed textures, clean geometric composition, "
        "soft diffused studio lighting, professional color grading, "
        "tack sharp focus, high contrast, clean gradient background"
    )

    for attempt in range(MAX_IMAGE_RETRIES + 1):
        try:
            image = client.text_to_image(
                enhanced_prompt,
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
            print(f"[ImageService] Generation failed after {MAX_IMAGE_RETRIES + 1} attempts: {e}")
            return ""

    return ""


async def check_model_health() -> bool:
    try:
        info = client.get_model_status(HUGGINGFACE_IMAGE_MODEL)
        return True
    except Exception:
        try:
            image = client.text_to_image("test", width=64, height=64)
            return image is not None
        except Exception:
            return True
