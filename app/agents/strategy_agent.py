from app.services import huggingface_service
from app.agents.templates import get_template


SYSTEM_PROMPT = """You are a Master Pitch Architect. You design winning strategies for Silicon Valley startups.
Your goal is to build an unshakeable narrative bridge between the 'Intelligence' (research) and the 'Invention' (the product).
You don't just state facts; you craft a logical and emotional arc that makes the 'Funding Ask' feel inevitable.

Strategic Alignment Rules:
1. PROBLEM-SOLUTION TIGHTNESS: Every pain point identified in research must have a specific feature in the solution.
2. MARKET ALIGNMENT: The 'Why Now' from research must be the foundation of the 'Vision'.
3. COMPETITIVE DESTRUCTION: The 'Competitor Blindspots' must be the core of the 'Competitive Advantage'.
4. NARRATIVE FLOW: Ensure a smooth transition from market tension to product relief."""


async def run(brand_name: str, problem_statement: str, target_audience: str, tone: str, research: dict, theme_id: str) -> dict:
    template_structure = "\n".join([f"- {s}" for s in get_template(theme_id)])
    
    # Extract smarter research components
    intel = research.get('market_intelligence', {})
    comp = research.get('competitor_intelligence', {})
    psycho = research.get('audience_psychographics', {})

    prompt = f"""Architect a winning strategy for "{brand_name}" in the {theme_id} domain.

Market Intelligence:
- The Why Now: {intel.get('the_why_now')}
- Market Drivers: {', '.join(intel.get('market_dynamics', {}).get('growth_drivers', []))}
- Direct Rival Blindspots: {', '.join([c.get('blindspot', '') for c in comp.get('direct_rivals', [])])}
- Core Human Tension: {psycho.get('core_tension')}

Strategic Requirements for {theme_id}:
{template_structure}

Brief:
- Problem: {problem_statement}
- Audience: {target_audience}
- Tone: {tone}

Generate a 'Master Strategy JSON'. This is the blueprint for the entire deck.

JSON structure:
{{
    "narrative_arc": {{
        "the_hook": "The opening punch that grabs attention",
        "the_villain": "The specific market force or frustration we are fighting",
        "the_epiphany": "The moment the audience realizes why {brand_name} is the only answer",
        "the_climax": "The peak of the product demo/solution"
    }},
    "positioning": {{
        "category_definition": "The new or redefined category we own",
        "unique_value_prop": "The one-sentence reason we win",
        "pillars": ["Pillar 1: Technical", "Pillar 2: Emotional", "Pillar 3: Economic"]
    }},
    "alignment_matrix": {{
        "problem_mapped_to_solution": "Direct link between research pain and product gain",
        "competitor_gap_mapped_to_us": "How we fill the blindspot"
    }},
    "target_emotion": "The desired emotional state at the end of the pitch (e.g., Fear of Missing Out, Relieved Certainty)"
}}"""

    result = await huggingface_service.generate_json(prompt, SYSTEM_PROMPT)
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
