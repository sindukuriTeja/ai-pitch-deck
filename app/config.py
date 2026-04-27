import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
GENERATION_TIMEOUT = 300  # seconds per agent call
