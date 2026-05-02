import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "Qwen/Qwen3-30B-A3B")
HUGGINGFACE_IMAGE_MODEL = os.getenv("HUGGINGFACE_IMAGE_MODEL", "stabilityai/stable-diffusion-xl-base-1.0")

IS_VERCEL = os.getenv("VERCEL", "") == "1"
if IS_VERCEL:
    OUTPUT_DIR = "/tmp/output"
else:
    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")

IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
GENERATION_TIMEOUT = 300  # seconds per agent call
IMAGE_GENERATION_TIMEOUT = 120  # seconds for image generation
MAX_IMAGE_RETRIES = 2
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024
