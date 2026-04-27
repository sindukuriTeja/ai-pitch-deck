from app.services import ollama_service


SYSTEM_PROMPT = """You are an award-winning creative director at a top advertising agency.
Your job is to take strategy and create compelling creative content for a pitch deck.
You must design each slide using HTML code. Use <h1> for titles, <h2> for subtitles, <p> for body text, and <ul>/<li> for bullet points.
Every word must earn its place. Be bold, specific, and memorable. Avoid cliches."""


async def run(brand_name: str, problem_statement: str, target_audience: str, tone: str, strategy: dict) -> dict:
    prompt = f"""Create creative content for a pitch deck for "{brand_name}".

Strategy:
- Key Insight: {strategy.get('key_insight', '')}
- Positioning: {strategy.get('positioning', '')}
- Value Proposition: {strategy.get('value_proposition', '')}
- Strategic Pillars: {', '.join(strategy.get('strategic_pillars', []))}
- Target Emotion: {strategy.get('target_emotion', '')}
- Tone: {tone}

Brief: {problem_statement}
Audience: {target_audience}

Produce a JSON response with creative content for 10-15 slides. Each slide MUST be designed with HTML code.
Format:
{{
    "big_idea": "The overarching creative concept in one phrase",
    "tagline": "A memorable tagline for the brand",
    "slides": [
        {{
            "slide_number": 1,
            "html": "<h1>Brand Name</h1><h2>Tagline goes here</h2>"
        }},
        {{
            "slide_number": 2,
            "html": "<h1>The Challenge</h1><p>Description of the problem...</p>"
        }}
    ]
}}"""

    result = await ollama_service.generate_json(prompt, SYSTEM_PROMPT)
    if result.get("parse_error") or "slides" not in result:
        result = {
            "big_idea": f"Reimagining {problem_statement.split()[0:3]} for a better tomorrow",
            "tagline": strategy.get("positioning", f"{brand_name} - The Future Starts Here"),
            "slides": [
                {"slide_number": 1, "html": f"<h1>{brand_name}</h1><h2>{strategy.get('positioning', '')}</h2>"},
                {"slide_number": 2, "html": f"<h1>The Challenge</h1><p>{problem_statement}</p>"},
                {"slide_number": 3, "html": f"<h1>The Insight</h1><p>{strategy.get('key_insight', '')}</p>"},
                {"slide_number": 4, "html": f"<h1>The Opportunity</h1><p>A growing market ready for disruption.</p><ul><li>Growing demand</li><li>Underserved market</li></ul>"},
                {"slide_number": 5, "html": f"<h1>Introducing {brand_name}</h1><h2>{strategy.get('value_proposition', '')}</h2>"},
            ]
        }
    return result
