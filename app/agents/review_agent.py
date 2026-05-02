import json
from app.services import huggingface_service

SYSTEM_PROMPT = """You are the 'Pitch Doctor'. You have a 100% success rate in helping startups get funded.
Your job is to take a draft pitch deck and perform a 'Surgical Alignment' and 'Intelligence Injection'.

Review Criteria:
1. ALIGNMENT: Does every slide follow the narrative arc? Is the solution solving the SPECIFIC problem research identified?
2. INTELLIGENCE: Are the data points specific? Replace generic words like 'best' or 'fast' with 'industry-leading' or '300% faster'.
3. PUNCHY HEADLINES: Every headline (h1) should be an assertive claim, not a label.
4. COHESION: Does the big idea flow through every slide?
5. ALIGNMENT & SPACING: Ensure NO slide has more than 5 lines of total text. If it does, aggressively summarize it into punchy bullet points to prevent overlapping or overflowing.
6. VISUAL STORYTELLING: Check the 'image_prompt' fields. They should be cinematic and descriptive, optimized for the Z-Image-Turbo model. DO NOT delete existing image prompts; improve them.

CRITICAL: You MUST preserve the 'image_prompt' field for each slide in your response. If a slide doesn't have one and needs it, add it."""


async def run(creative_data: dict, tone: str) -> dict:
    slides = creative_data.get("slides", [])
    big_idea = creative_data.get("big_idea", "")
    tagline = creative_data.get("tagline", "")

    prompt = f"""Perform a surgical review of this pitch deck. Make it 'Fundable'.
Tone: {tone}
Big Idea: {big_idea}

Slides (HTML Format with Image Prompts):
{json.dumps(slides, indent=2)}

Instructions:
- Sharpen every Headline (h1) to be a strong, active claim.
- Inject specific 'Smarter' details (heuristic metrics or technical jargon) where appropriate.
- Ensure 'Strategic Alignment' by reinforcing the big idea in at least 30% of the slides.
- PRESERVE OR IMPROVE ALL 'image_prompt' FIELDS. DO NOT DROP THEM.
- Keep the HTML valid.

Produce the 'Master JSON' with updated slides:
{{
    "slides": [
        {{
            "slide_number": 1,
            "html": "<h1>Assertive Headline</h1><p>Intelligent, aligned copy...</p>",
            "image_prompt": "Cinematic professional illustration of..."
        }},
        ...
    ],
    "pitch_doctor_notes": ["Major alignment fix on slide X", "Intelligence injection on slide Y"]
}}"""

    result = await huggingface_service.generate_json(prompt, SYSTEM_PROMPT)
    if not result.get("parse_error") and "slides" in result:
        # Merge back to ensure we don't lose the top-level tagline/big_idea if not returned
        creative_data["slides"] = result["slides"]
        creative_data["pitch_doctor_notes"] = result.get("pitch_doctor_notes", [])
    
    return creative_data
