from app.services import ollama_service

SYSTEM_PROMPT = """You are a presentation design director. Your job is to assign the best visual layout
to each slide based on its content type. You ensure variety - never use the same layout twice in a row.
Available layouts: title_slide, section_header, content_image, stats_numbers, bullet_points, two_column, quote_insight, full_image"""

LAYOUT_MAP = {
    "title": "title_slide",
    "problem": "content_image",
    "insight": "quote_insight",
    "opportunity": "stats_numbers",
    "solution": "section_header",
    "how_it_works": "bullet_points",
    "feature_1": "content_image",
    "feature_2": "two_column",
    "feature_3": "content_image",
    "audience": "bullet_points",
    "traction": "stats_numbers",
    "competitive": "two_column",
    "vision": "quote_insight",
    "roadmap": "bullet_points",
    "closing": "title_slide",
}

ALL_LAYOUTS = ["title_slide", "section_header", "content_image", "stats_numbers",
               "bullet_points", "two_column", "quote_insight", "full_image"]


async def run(creative_content: dict, theme_id: str) -> dict:
    slides = creative_content.get("slides", [])
    structured_slides = []
    last_layout = None

    for slide in slides:
        purpose = slide.get("purpose", "content")
        layout = LAYOUT_MAP.get(purpose, "content_image")

        # Avoid repeating the same layout consecutively
        if layout == last_layout:
            for alt in ALL_LAYOUTS:
                if alt != last_layout and alt != "title_slide":
                    layout = alt
                    break

        structured_slides.append({
            **slide,
            "layout_type": layout,
            "visual_suggestion": f"Use {theme_id} theme styling with {layout} layout"
        })
        last_layout = layout

    return {
        "brand_name": creative_content.get("brand_name", ""),
        "tagline": creative_content.get("tagline", ""),
        "big_idea": creative_content.get("big_idea", ""),
        "slides": structured_slides,
        "theme_id": theme_id
    }
