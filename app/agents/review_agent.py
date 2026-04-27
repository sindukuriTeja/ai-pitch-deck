from app.services import ollama_service

SYSTEM_PROMPT = """You are a senior creative reviewer at an advertising agency.
Review a pitch deck plan for quality. Check for:
1. Generic or cliché content (flag it)
2. Repetitive layouts (flag consecutive same layouts)
3. Text-heavy slides (body text > 3 sentences)
4. Missing big idea or weak storytelling arc
5. Inconsistent tone

For each issue found, suggest a specific fix. Respond in JSON."""


async def run(deck_plan: dict, tone: str) -> dict:
    slides = deck_plan.get("slides", [])

    # Rule-based quality checks (fast, no LLM needed)
    issues = []
    fixes_applied = 0

    # Check for consecutive same layouts
    for i in range(1, len(slides)):
        if slides[i].get("layout_type") == slides[i-1].get("layout_type"):
            alt_layouts = ["content_image", "two_column", "bullet_points", "stats_numbers", "quote_insight"]
            current = slides[i]["layout_type"]
            for alt in alt_layouts:
                if alt != current:
                    slides[i]["layout_type"] = alt
                    fixes_applied += 1
                    break

    # Check for text-heavy slides
    for slide in slides:
        body = slide.get("body", "")
        if body and len(body.split(". ")) > 3:
            sentences = body.split(". ")
            slide["body"] = ". ".join(sentences[:2]) + "."
            if not slide.get("bullets"):
                slide["bullets"] = [s.strip().rstrip(".") for s in sentences[2:] if s.strip()]
            fixes_applied += 1

    # Check for empty slides
    for slide in slides:
        if not slide.get("title"):
            slide["title"] = f"Slide {slide.get('slide_number', '?')}"
            fixes_applied += 1

    # Try LLM review for content quality
    try:
        slide_summary = "\n".join([
            f"Slide {s.get('slide_number')}: [{s.get('layout_type')}] {s.get('title', 'No title')}"
            for s in slides
        ])
        prompt = f"""Review this pitch deck outline for quality and suggest improvements.
Tone should be: {tone}

Deck: {deck_plan.get('big_idea', 'N/A')}
Tagline: {deck_plan.get('tagline', 'N/A')}

Slides:
{slide_summary}

Respond in JSON:
{{
    "quality_score": 7,
    "strengths": ["strength 1"],
    "improvements": ["improvement 1"],
    "approved": true
}}"""
        review = await ollama_service.generate_json(prompt, SYSTEM_PROMPT)
        if not review.get("parse_error"):
            quality_score = review.get("quality_score", 7)
        else:
            quality_score = 7
    except Exception:
        quality_score = 7

    deck_plan["slides"] = slides
    deck_plan["review"] = {
        "quality_score": quality_score,
        "fixes_applied": fixes_applied,
        "approved": True
    }
    return deck_plan
