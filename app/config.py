import os

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "XiaomiMiMo/MiMo-V2-Flash")
HUGGINGFACE_IMAGE_MODEL = os.getenv("HUGGINGFACE_IMAGE_MODEL", "Tongyi-MAI/Z-Image-Turbo")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
GENERATION_TIMEOUT = 300  # seconds per agent call
IMAGE_GENERATION_TIMEOUT = 120  # seconds for image generation
MAX_IMAGE_RETRIES = 2
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024
