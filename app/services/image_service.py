import os
import uuid
import asyncio
from huggingface_hub import InferenceClient
from app.config import HUGGINGFACE_API_KEY, HUGGINGFACE_IMAGE_MODEL, IMAGE_DIR

client = InferenceClient(
    model=HUGGINGFACE_IMAGE_MODEL,
    token=HUGGINGFACE_API_KEY
)

async def generate_image(prompt: str) -> str:
    """
    Generates a high-quality image using Z-Image-Turbo optimized parameters.
    Runs in a separate thread to avoid blocking the event loop.
    Returns the path to the saved image.
    """
    return await asyncio.to_thread(_generate_image_sync, prompt)

def _generate_image_sync(prompt: str) -> str:
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    # Z-Image-Turbo optimization:
    # Highly descriptive, cinematic, and professional visual language.
    # The model works best with detailed environmental and lighting descriptions.
    enhanced_prompt = (
        f"Cinematic professional photography for a business pitch deck, {prompt}, "
        "minimalist corporate style, 8k resolution, highly detailed textures, "
        "clean composition, soft studio lighting, ultra-modern aesthetic, "
        "professional color grading, sharp focus, high contrast, clean background."
    )
    
    try:
        # guidance_scale=0.0 is crucial for Turbo/Distilled models to avoid artifacts
        image = client.text_to_image(
            enhanced_prompt,
            guidance_scale=0.0,
            num_inference_steps=2 # Turbo models only need 1-4 steps
        )
        
        image_name = f"{uuid.uuid4()}.png"
        image_path = os.path.join(IMAGE_DIR, image_name)
        image.save(image_path)
        return image_path
    except Exception as e:
        print(f"Error generating image with Z-Image-Turbo: {e}")
        # Log error to file for debugging
        with open(os.path.join(OUTPUT_DIR, "image_error.log"), "a") as f:
            f.write(f"Prompt: {prompt}\nError: {str(e)}\n---\n")
        return ""
