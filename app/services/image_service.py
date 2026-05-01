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
    Generates an image from a prompt and saves it to the IMAGE_DIR.
    Returns the path to the saved image.
    """
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    # Enhancing prompt for "plain" and professional pitch deck style
    enhanced_prompt = f"Professional pitch deck illustration, {prompt}, clean design, high resolution, minimalist, corporate aesthetic, isolated on plain background"
    
    try:
        image = client.text_to_image(enhanced_prompt)
        image_name = f"{uuid.uuid4()}.png"
        image_path = os.path.join(IMAGE_DIR, image_name)
        image.save(image_path)
        return image_path
    except Exception as e:
        print(f"Error generating image: {e}")
        return ""
