from app.services import search_service
from app.services import huggingface_service


SYSTEM_PROMPT = """You are a Lead Market Intelligence Officer at a Tier-1 Venture Capital firm.
Your job is to perform deep-dive research for high-stakes investment pitches.
You must synthesize raw search data into a 'Smarter Research Brief' that connects the dots between market gaps, technological shifts, and consumer behavior.

Focus on:
1. 'The Why Now': What confluence of factors makes this business critical TODAY?
2. 'Unfair Advantage': Identify potential moats (data, network effects, regulatory barriers).
3. 'Quantifiable Market Dynamics': TAM/SAM/SOM with realistic, research-backed logic.
4. 'Competitor Blindspots': Where are the incumbents failing?
5. 'Alignment Vector': How does the research support the proposed solution?

Be hyper-specific. Use real industry jargon, actual competitor names, and recent market events (2024-2025)."""


async def run(brand_name: str, problem_statement: str, target_audience: str) -> dict:
    # Gather web research
    words = problem_statement.split()
    industry_str = " ".join(words[:5]) if len(words) > 5 else problem_statement
    
    raw_research = search_service.gather_research(brand_name, industry_str)

    prompt = f"""Synthesize this intelligence for a high-stakes pitch for "{brand_name}".

Context:
- Primary Problem: {problem_statement}
- Core Audience: {target_audience}

Raw Intelligence Data:
{raw_research}

Generate a 'Smart Intelligence Report' in JSON.
DO NOT use placeholders. If data is sparse, use 'Heuristic Estimation' based on your training to provide realistic, professional values.

Expected JSON structure:
{{
    "market_intelligence": {{
        "the_why_now": "The specific confluence of trends making this urgent",
        "market_dynamics": {{
            "tam": "Global opportunity description",
            "sam": "Serviceable opportunity",
            "growth_drivers": ["Driver 1", "Driver 2"]
        }},
        "trends": ["Quantified trend 1", "Emerging technology shift"]
    }},
    "competitor_intelligence": {{
        "direct_rivals": [
            {{"name": "Company X", "moat": "Their strength", "blindspot": "The gap we exploit"}}
        ],
        "indirect_threats": ["Alternative solution 1"]
    }},
    "audience_psychographics": {{
        "core_tension": "The underlying frustration/fear",
        "aspirational_state": "What they actually want to feel",
        "purchasing_triggers": ["Trigger 1"]
    }},
    "strategic_opportunities": ["High-value opportunity 1", "Low-hanging fruit"],
    "alignment_notes": "How this research validates the Brand's approach"
}}"""

    result = await huggingface_service.generate_json(prompt, SYSTEM_PROMPT)
    if result.get("parse_error"):
        # Fallback with structured defaults
        result = {
            "brand_summary": f"{brand_name} addresses {problem_statement} for {target_audience}.",
            "market_trends": ["Digital transformation", "Customer-centric innovation", "Sustainable growth"],
            "audience_insights": [f"{target_audience} seek better solutions", "Growing demand for innovation", "Value-driven purchasing"],
            "competitors": ["Market leaders", "Emerging disruptors", "Traditional players"],
            "opportunities": ["Untapped market segments", "Technology-driven differentiation"],
            "key_data_points": ["Growing market demand", "Increasing digital adoption", "Shifting consumer preferences"]
        }
    return result
