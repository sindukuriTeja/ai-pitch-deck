from dataclasses import dataclass
from pptx.util import Pt
from pptx.dml.color import RGBColor


@dataclass
class ThemeColors:
    primary: str       # 60% - backgrounds, main areas
    secondary: str     # 30% - supporting elements
    accent: str        # 10% - CTAs, highlights
    text_dark: str     # main text
    text_light: str    # text on dark backgrounds
    bg_light: str      # light background variant
    bg_dark: str       # dark background variant


@dataclass
class ThemeFonts:
    heading: str
    body: str
    heading_size: int  # in points
    body_size: int
    subtitle_size: int


@dataclass
class Theme:
    id: str
    name: str
    description: str
    industry: str
    style: str  # modern, corporate, creative, minimal, bold, elegant
    colors: ThemeColors
    fonts: ThemeFonts
    icon: str  # emoji for UI


def rgb(hex_color: str) -> RGBColor:
    h = hex_color.lstrip('#')
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


THEMES: dict[str, Theme] = {
    "tech_startup": Theme(
        id="tech_startup",
        name="Tech Startup",
        description="Electric blue on dark. Modern and innovative.",
        industry="Technology",
        style="modern",
        colors=ThemeColors(
            primary="#0A1628", secondary="#1E3A5F", accent="#00D4FF",
            text_dark="#1A1A2E", text_light="#FFFFFF", bg_light="#F0F8FF", bg_dark="#0A1628"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=36, body_size=16, subtitle_size=20),
        icon="rocket"
    ),
    "healthcare": Theme(
        id="healthcare",
        name="Healthcare",
        description="Teal and white. Clean and professional.",
        industry="Healthcare & Life Sciences",
        style="corporate",
        colors=ThemeColors(
            primary="#006D77", secondary="#83C5BE", accent="#EDF6F9",
            text_dark="#2C3E50", text_light="#FFFFFF", bg_light="#EDF6F9", bg_dark="#006D77"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=34, body_size=16, subtitle_size=18),
        icon="heart"
    ),
    "finance": Theme(
        id="finance",
        name="Finance",
        description="Navy and gold. Corporate and trustworthy.",
        industry="Finance & Banking",
        style="corporate",
        colors=ThemeColors(
            primary="#1B2A4A", secondary="#2C4A7C", accent="#D4A843",
            text_dark="#1B2A4A", text_light="#FFFFFF", bg_light="#F5F1E8", bg_dark="#1B2A4A"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=34, body_size=15, subtitle_size=18),
        icon="chart"
    ),
    "creative_agency": Theme(
        id="creative_agency",
        name="Creative Agency",
        description="Bold gradients and vibrant colors. Playful and energetic.",
        industry="Creative & Marketing",
        style="creative",
        colors=ThemeColors(
            primary="#FF6B6B", secondary="#4ECDC4", accent="#FFE66D",
            text_dark="#2C3E50", text_light="#FFFFFF", bg_light="#FFF9E6", bg_dark="#2C3E50"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=38, body_size=16, subtitle_size=20),
        icon="palette"
    ),
    "ecommerce": Theme(
        id="ecommerce",
        name="E-Commerce",
        description="Vibrant orange and purple. Energetic and conversion-focused.",
        industry="E-Commerce & Retail",
        style="bold",
        colors=ThemeColors(
            primary="#6C5CE7", secondary="#A29BFE", accent="#FD79A8",
            text_dark="#2D3436", text_light="#FFFFFF", bg_light="#F8F9FA", bg_dark="#2D3436"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=36, body_size=16, subtitle_size=20),
        icon="cart"
    ),
    "education": Theme(
        id="education",
        name="Education",
        description="Green and warm tones. Friendly and approachable.",
        industry="Education & EdTech",
        style="modern",
        colors=ThemeColors(
            primary="#2D6A4F", secondary="#52B788", accent="#F9C74F",
            text_dark="#264653", text_light="#FFFFFF", bg_light="#F0FFF4", bg_dark="#2D6A4F"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=34, body_size=16, subtitle_size=18),
        icon="book"
    ),
    "real_estate": Theme(
        id="real_estate",
        name="Real Estate",
        description="Charcoal and gold. Luxury and sophistication.",
        industry="Real Estate & Property",
        style="elegant",
        colors=ThemeColors(
            primary="#2C2C2C", secondary="#5C5C5C", accent="#C9A96E",
            text_dark="#1A1A1A", text_light="#FFFFFF", bg_light="#FAF5EF", bg_dark="#2C2C2C"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=36, body_size=15, subtitle_size=18),
        icon="building"
    ),
    "food_beverage": Theme(
        id="food_beverage",
        name="Food & Beverage",
        description="Warm reds and earthy tones. Appetizing and inviting.",
        industry="Food & Beverage",
        style="creative",
        colors=ThemeColors(
            primary="#C44536", secondary="#772E25", accent="#F7B267",
            text_dark="#3D1C11", text_light="#FFFFFF", bg_light="#FFF5EB", bg_dark="#3D1C11"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=36, body_size=16, subtitle_size=20),
        icon="utensils"
    ),
    "saas_b2b": Theme(
        id="saas_b2b",
        name="SaaS / B2B",
        description="Purple-blue gradient. Tech-forward and professional.",
        industry="SaaS & Enterprise",
        style="modern",
        colors=ThemeColors(
            primary="#5B2C6F", secondary="#7D3C98", accent="#48C9B0",
            text_dark="#2C3E50", text_light="#FFFFFF", bg_light="#F4ECF7", bg_dark="#5B2C6F"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=34, body_size=16, subtitle_size=18),
        icon="cloud"
    ),
    "sustainability": Theme(
        id="sustainability",
        name="Sustainability",
        description="Earth tones and organic greens. Natural and purpose-driven.",
        industry="Green Tech & Environment",
        style="minimal",
        colors=ThemeColors(
            primary="#386641", secondary="#6A994E", accent="#A7C957",
            text_dark="#344E41", text_light="#FFFFFF", bg_light="#F0F7E8", bg_dark="#344E41"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=34, body_size=16, subtitle_size=18),
        icon="leaf"
    ),
    "fashion_luxury": Theme(
        id="fashion_luxury",
        name="Fashion & Luxury",
        description="Black, white, and gold. Elegant and minimal.",
        industry="Fashion & Luxury",
        style="elegant",
        colors=ThemeColors(
            primary="#000000", secondary="#333333", accent="#C9A96E",
            text_dark="#000000", text_light="#FFFFFF", bg_light="#FAFAFA", bg_dark="#000000"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=38, body_size=14, subtitle_size=18),
        icon="gem"
    ),
    "sports_fitness": Theme(
        id="sports_fitness",
        name="Sports & Fitness",
        description="Red and black. Bold and dynamic energy.",
        industry="Sports & Fitness",
        style="bold",
        colors=ThemeColors(
            primary="#D90429", secondary="#2B2D42", accent="#EDF2F4",
            text_dark="#2B2D42", text_light="#FFFFFF", bg_light="#EDF2F4", bg_dark="#2B2D42"
        ),
        fonts=ThemeFonts(heading="Calibri", body="Calibri", heading_size=38, body_size=16, subtitle_size=20),
        icon="trophy"
    ),
}


def get_theme(theme_id: str) -> Theme:
    return THEMES.get(theme_id, THEMES["tech_startup"])


def list_themes() -> list[dict]:
    return [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "industry": t.industry,
            "style": t.style,
            "icon": t.icon,
            "colors": {
                "primary": t.colors.primary,
                "secondary": t.colors.secondary,
                "accent": t.colors.accent,
                "bg_light": t.colors.bg_light,
            }
        }
        for t in THEMES.values()
    ]
