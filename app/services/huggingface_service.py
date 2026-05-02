import json
import re
from huggingface_hub import InferenceClient
from app.config import HUGGINGFACE_API_KEY, HUGGINGFACE_MODEL, GENERATION_TIMEOUT

client = InferenceClient(
    model=HUGGINGFACE_MODEL,
    token=HUGGINGFACE_API_KEY,
    timeout=GENERATION_TIMEOUT,
)


def _strip_thinking(text: str) -> str:
    """Remove <think>...</think> blocks that Qwen3 may produce."""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()


async def generate(prompt: str, system_prompt: str = "") -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat_completion(
        messages=messages,
        max_tokens=4096,
        temperature=0.7,
        top_p=0.9,
    )
    raw = resp.choices[0].message.content
    return _strip_thinking(raw)


async def generate_json(prompt: str, system_prompt: str = "") -> dict:
    full_system = system_prompt + "\n\nIMPORTANT: Respond ONLY with valid JSON. No markdown, no code fences, no explanation. Do not include any thinking or reasoning."
    raw = await generate(prompt, full_system)
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
        resp = client.chat_completion(
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5,
        )
        return resp.choices[0].message.content is not None
    except Exception:
        return False
