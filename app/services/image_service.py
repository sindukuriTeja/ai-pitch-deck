import os
import uuid
from huggingface_hub import InferenceClient
from app.config import HUGGINGFACE_API_KEY, HUGGINGFACE_IMAGE_MODEL, IMAGE_DIR

client = InferenceClient(
    model=HUGGINGFACE_IMAGE_MODEL,
    token=HUGGINGFACE_API_KEY
)

def generate_image(prompt: str) -> str:
    """
    Generates a high-quality image using Z-Image-Turbo optimized parameters.
    Returns the path to the saved image.
    """
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    # Z-Image-Turbo specific optimization:
    # 1. No negative prompts (not effective)
    # 2. Focus on descriptive, high-quality visual language
    # 3. Parameters: guidance_scale=0.0 (as per official recommendation for Turbo)
    
    enhanced_prompt = (
        f"Cinematic professional photography, {prompt}, "
        "minimalist corporate style, 8k resolution, highly detailed, "
        "clean composition, soft studio lighting, ultra-modern aesthetic, "
        "professional color grading, sharp focus."
    )
    
    try:
        # Using the standard text_to_image with optimized model defaults
        # Most HF Inference API endpoints for Turbo models handle steps/guidance automatically
        # but we ensure the prompt is formatted for maximum clarity.
        image = client.text_to_image(
            enhanced_prompt,
            # For some API versions, we can pass extra headers or params if supported
        )
        
        image_name = f"{uuid.uuid4()}.png"
        image_path = os.path.join(IMAGE_DIR, image_name)
        image.save(image_path)
        return image_path
    except Exception as e:
        print(f"Error generating image with Z-Image-Turbo: {e}")
        return ""
