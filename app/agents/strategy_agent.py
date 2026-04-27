from app.services import ollama_service


SYSTEM_PROMPT = """You are a chief strategy officer at a world-class advertising agency.
Your job is to take market research and a business brief, then develop a powerful strategic direction.
Create a compelling insight (not generic), a clear positioning statement, and a strategic framework.
Think like the best strategists: find the tension, the truth, the unexpected angle."""


async def run(brand_name: str, problem_statement: str, target_audience: str, tone: str, research: dict) -> dict:
    prompt = f"""Develop an advertising strategy for "{brand_name}".

Brief:
- Problem: {problem_statement}
- Target Audience: {target_audience}
- Tone: {tone}

Research Summary:
- Brand: {research.get('brand_summary', '')}
- Market Trends: {', '.join(research.get('market_trends', []))}
- Audience Insights: {', '.join(research.get('audience_insights', []))}
- Competitors: {', '.join(research.get('competitors', []))}
- Opportunities: {', '.join(research.get('opportunities', []))}

Produce a JSON response:
{{
    "key_insight": "A non-obvious, specific insight about the audience/market tension",
    "positioning": "One sentence positioning statement",
    "value_proposition": "Core value proposition in one line",
    "strategic_pillars": ["pillar 1", "pillar 2", "pillar 3"],
    "target_emotion": "The primary emotion to evoke",
    "competitive_advantage": "What makes this brand different"
}}"""

    result = await ollama_service.generate_json(prompt, SYSTEM_PROMPT)
    if result.get("parse_error"):
        result = {
            "key_insight": f"{target_audience} are looking for a solution that truly understands their needs in {problem_statement}.",
            "positioning": f"{brand_name}: The smarter way to solve {problem_statement}.",
            "value_proposition": f"Empowering {target_audience} with innovative solutions.",
            "strategic_pillars": ["Innovation", "Trust", "Impact"],
            "target_emotion": "Confidence",
            "competitive_advantage": f"Purpose-built for {target_audience}"
        }
    return result
