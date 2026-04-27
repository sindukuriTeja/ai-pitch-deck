import httpx
import json
import re
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL, GENERATION_TIMEOUT


async def generate(prompt: str, system_prompt: str = "") -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 4096,
        }
    }
    async with httpx.AsyncClient(timeout=GENERATION_TIMEOUT) as client:
        resp = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        resp.raise_for_status()
        return resp.json()["response"]


async def generate_json(prompt: str, system_prompt: str = "") -> dict:
    full_system = system_prompt + "\n\nIMPORTANT: Respond ONLY with valid JSON. No markdown, no code fences, no explanation."
    raw = await generate(prompt, full_system)
    # Try to extract JSON from the response
    raw = raw.strip()
    # Remove markdown code fences if present
    if raw.startswith("```"):
        raw = re.sub(r'^```(?:json)?\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)
    # Try to find JSON object or array
    for start_char, end_char in [('{', '}'), ('[', ']')]:
        start = raw.find(start_char)
        if start != -1:
            depth = 0
            for i in range(start, len(raw)):
                if raw[i] == start_char:
                    depth += 1
                elif raw[i] == end_char:
                    depth -= 1
                if depth == 0:
                    try:
                        parsed = json.loads(raw[start:i+1])
                        if isinstance(parsed, dict):
                            return parsed
                        elif isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], dict):
                            return parsed[0]
                    except json.JSONDecodeError:
                        break
    # Last resort: try parsing the whole thing
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
        elif isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], dict):
            return parsed[0]
    except json.JSONDecodeError:
        pass

    return {"raw_response": raw, "parse_error": True}


async def check_health() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False
