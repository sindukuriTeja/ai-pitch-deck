from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ToneEnum(str, Enum):
    professional = "professional"
    bold = "bold"
    friendly = "friendly"
    inspirational = "inspirational"
    minimal = "minimal"
    playful = "playful"


class GenerateRequest(BaseModel):
    brand_name: str
    problem_statement: str
    target_audience: str
    tone: str = "professional"
    theme_id: str = "tech_startup"
    additional_context: Optional[str] = ""


class TaskStatus(BaseModel):
    task_id: str
    status: str  # pending, researching, strategizing, creating, structuring, reviewing, building, complete, error
    progress: int  # 0-100
    message: str
    download_url: Optional[str] = None


class SlideContent(BaseModel):
    slide_number: int
    layout_type: str
    title: str
    subtitle: Optional[str] = ""
    body: Optional[str] = ""
    bullets: Optional[list[str]] = None
    stats: Optional[list[dict]] = None
    quote: Optional[str] = ""
    cta: Optional[str] = ""
    visual_suggestion: Optional[str] = ""


class DeckPlan(BaseModel):
    brand_name: str
    tagline: str
    big_idea: str
    slides: list[SlideContent]
