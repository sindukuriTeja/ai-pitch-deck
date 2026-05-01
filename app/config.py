import os

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "XiaomiMiMo/MiMo-V2-Flash")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
GENERATION_TIMEOUT = 300  # seconds per agent call
