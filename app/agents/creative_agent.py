from app.services import huggingface_service
from app.agents.templates import get_template

SYSTEM_PROMPT = """You are a Cinematic Pitch Designer. You turn cold strategies into burning desires.
Your goal is to populate the pitch deck with content that feels 'Smarter' and more 'Aligned'.

Content Principles:
1. THE NARRATIVE ARC: Follow the 'Hook -> Villain -> Epiphany -> Climax' arc provided in strategy.
2. ALIGNMENT CHECK: Every slide must directly reference the research-backed insights or the strategic pillars.
3. SMARTER COPY: Use 'Power Headlines' that sell an outcome, not just a feature.
4. EVIDENCE-BASED: Proactively include 'Heuristic Data Points' (e.g., '30% efficiency increase' or '5x faster than legacy systems') to make the pitch smarter.
5. HTML DESIGN: Use <h1> for the Power Headline, <h2> for the value statement, and <p> or <ul> for details.
6. CONCISENESS: NEVER exceed 3-4 bullet points or 2 short sentences per slide. This is critical for visual alignment.
7. VISUAL ALIGNMENT: Identify 2-3 key slides where a professional image or illustration would add value (e.g., Solution, Market, Team, or Big Idea). Provide a specific 'Cinematic' image prompt for these slides.
   *   Z-Image-Turbo Prompting Rule: Be descriptive and visual. Describe subjects, lighting, and environment. (e.g., 'A sleek glass-walled boardroom overlooking a futuristic neon city at dusk, soft bokeh, cinematic lighting' instead of 'meeting room').

Produce a JSON response with creative content designed with HTML code.

JSON structure:
{{
    "big_idea": "The central creative theme",
    "tagline": "The 3-5 word memorable tagline",
    "slides": [
        {{
            "slide_number": 1,
            "html": "<h1>Headline</h1><p>Content...</p>",
            "image_prompt": "A professional minimalist illustration of..." (optional)
        }}
    ]
}}"""

async def run(brand_name: str, problem_statement: str, target_audience: str, tone: str, strategy: dict, theme_id: str) -> dict:
    template_slides = get_template(theme_id)
    template_str = "\n".join([f"Slide {i+1} Target: {s}" for i, s in enumerate(template_slides)])

    arc = strategy.get('narrative_arc', {})
    pos = strategy.get('positioning', {})
    align = strategy.get('alignment_matrix', {})

    prompt = f"""Design a 'Smart Pitch Deck' for "{brand_name}" ({theme_id}).

The Narrative Framework:
- The Hook: {arc.get('the_hook')}
- The Villain (Market Tension): {arc.get('the_villain')}
- The Epiphany (Our Solution): {arc.get('the_epiphany')}
- The Climax (Product Power): {arc.get('the_climax')}

Strategic Alignment:
- Category: {pos.get('category_definition')}
- Unique Value: {pos.get('unique_value_prop')}
- Pillars: {', '.join(pos.get('pillars', []))}
- Problem-Solution Map: {align.get('problem_mapped_to_solution')}

Required Deck Structure:
{template_str}

Tone: {tone}
Audience: {target_audience}

Generate a JSON object with {len(template_slides)} slides. 
EACH SLIDE MUST:
- Use professional, high-impact copy.
- Include at least one 'Smarter' detail (a statistic, a specific workflow step, or a technical proof point).
- Strictly follow the HTML tag usage.

JSON structure:
{{
    "big_idea": "The central creative theme",
    "tagline": "The 3-5 word memorable tagline",
    "slides": [
        {{
            "slide_number": 1,
            "html": "<h1>Headline</h1><p>Content...</p>",
            "image_prompt": "A professional minimalist illustration of..." (optional)
        }}
    ]
}}"""

    result = await huggingface_service.generate_json(prompt, SYSTEM_PROMPT)
    
    if result.get("parse_error") or "slides" not in result:
        fallback_slides = []
        for i, title in enumerate(template_slides):
            fallback_slides.append({
                "slide_number": i + 1,
                "html": f"<h1>{title.split('—')[0].strip()}</h1><p>Content for {title.split('—')[0].strip()} in {theme_id} context.</p>"
            })
        
        result = {
            "big_idea": f"Reimagining {problem_statement[:20]} for a better tomorrow",
            "tagline": f"{brand_name} - The Future Starts Here",
            "slides": fallback_slides
        }
    return result
