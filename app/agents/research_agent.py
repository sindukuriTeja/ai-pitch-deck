from app.services import search_service
from app.services import huggingface_service


SYSTEM_PROMPT = """You are a senior market research analyst at a top advertising agency.
Your job is to analyze raw research data and produce a clear, structured market research brief.
Focus on: market size, key trends, target audience pain points, competitive landscape, and opportunities.
Be specific and insightful - avoid generic observations."""


async def run(brand_name: str, problem_statement: str, target_audience: str) -> dict:
    # Gather web research
    industry = problem_statement.split()[0:5]
    industry_str = " ".join(industry)
    raw_research = search_service.gather_research(brand_name, industry_str)

    prompt = f"""Analyze this research data for a pitch deck about "{brand_name}".
If the Raw Research is limited or says 'Live Data Unavailable', use your deep internal knowledge and reasoning capabilities to generate highly accurate, specific, and realistic data for this industry. DO NOT use generic placeholders like 'trend 1'. Provide actual, real-world industry trends, real competitors, and deep insights based on facts.

Problem: {problem_statement}
Target Audience: {target_audience}

Raw Research:
{raw_research}

Produce a JSON response with these fields:
{{
    "brand_summary": "2-3 sentence brand overview",
    "market_trends": ["trend 1", "trend 2", "trend 3"],
    "audience_insights": ["insight 1", "insight 2", "insight 3"],
    "competitors": ["competitor 1", "competitor 2", "competitor 3"],
    "opportunities": ["opportunity 1", "opportunity 2"],
    "key_data_points": ["stat or fact 1", "stat or fact 2", "stat or fact 3"]
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
