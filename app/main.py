import asyncio
import os
import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.models.schemas import GenerateRequest, TaskStatus
from app.pptx_engine.themes import list_themes
from app.pptx_engine.builder import build_presentation
from app.agents import research_agent, strategy_agent, creative_agent, structure_agent, review_agent, image_agent
from app.services import huggingface_service, image_service
from app.config import OUTPUT_DIR

app = FastAPI(title="AI Pitch Deck Generator", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# In-memory task store
tasks: dict[str, TaskStatus] = {}
decks: dict[str, dict] = {}
websocket_connections: dict[str, list[WebSocket]] = {}

async def notify_progress(task_id: str, status: str, progress: int, message: str, download_url: str = None):
    task = TaskStatus(task_id=task_id, status=status, progress=progress, message=message, download_url=download_url)
    tasks[task_id] = task
    if task_id in websocket_connections:
        for ws in websocket_connections[task_id]:
            try:
                await ws.send_json(task.model_dump())
            except Exception:
                pass

async def generate_deck(task_id: str, request: GenerateRequest):
    try:
        # Step 1: Research
        await notify_progress(task_id, "researching", 10, "Researching brand and market data...")
        research = await research_agent.run(
            request.brand_name, request.problem_statement, request.target_audience
        )

        # Step 2: Strategy
        await notify_progress(task_id, "strategizing", 30, "Developing strategic direction...")
        strategy = await strategy_agent.run(
            request.brand_name, request.problem_statement,
            request.target_audience, request.tone, research, request.theme_id
        )

        # Step 3: Creative & Structure (HTML Generation)
        await notify_progress(task_id, "creating", 50, "Generating high-impact creative content...")
        creative = await creative_agent.run(
            request.brand_name, request.problem_statement,
            request.target_audience, request.tone, strategy, request.theme_id
        )

        # Step 4: Quality Review & Refinement
        await notify_progress(task_id, "reviewing", 75, "Refining copy and ensuring quality...")
        creative = await review_agent.run(creative, request.tone)

        # Step 5: Image Generation via Image Agent (Z-Image-Turbo)
        await notify_progress(task_id, "visualizing", 80, "Image Agent: Generating cinematic AI illustrations with Z-Image-Turbo...")
        creative = await image_agent.run(creative)

        img_stats = creative.get("image_generation_stats", {})
        gen_count = img_stats.get("successfully_generated", 0)
        total_req = img_stats.get("total_requested", 0)
        await notify_progress(task_id, "structuring", 85, f"Image Agent complete: {gen_count}/{total_req} visuals generated.")

        # Step 6: Build PPTX
        await notify_progress(task_id, "building", 90, "Building professional PowerPoint file...")
        output_path = build_presentation(creative, request.theme_id, task_id)

        await notify_progress(task_id, "complete", 100,
                              "Pitch deck ready for download!",
                              f"/api/download/{task_id}")

    except Exception as e:
        await notify_progress(task_id, "error", 0, f"Error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/themes")
async def get_themes():
    return {"themes": list_themes()}

@app.get("/api/health")
async def health():
    model_ok = await huggingface_service.check_health()
    image_ok = await image_service.check_model_health()
    return {"status": "ok", "text_model": model_ok, "image_model": image_ok}

@app.post("/api/generate")
async def start_generation(request: GenerateRequest):
    task_id = str(uuid.uuid4())[:8]
    tasks[task_id] = TaskStatus(
        task_id=task_id, status="pending", progress=0, message="Starting generation..."
    )
    asyncio.create_task(generate_deck(task_id, request))
    return {"task_id": task_id}

@app.get("/api/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks:
        return {"error": "Task not found"}, 404
    return tasks[task_id].model_dump()

@app.get("/presentation/{task_id}", response_class=HTMLResponse)
async def presentation(request: Request, task_id: str):
    if task_id not in decks:
        return HTMLResponse("Presentation not found or expired.", status_code=404)
    return templates.TemplateResponse("presentation.html", {"request": request, "deck": decks[task_id]})

@app.get("/api/download/{task_id}")
async def download(task_id: str):
    filepath = os.path.join(OUTPUT_DIR, f"{task_id}.pptx")
    if not os.path.exists(filepath):
        return {"error": "File not found"}, 404
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=f"pitch_deck_{task_id}.pptx"
    )

@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    if task_id not in websocket_connections:
        websocket_connections[task_id] = []
    websocket_connections[task_id].append(websocket)
    try:
        # Send current status if exists
        if task_id in tasks:
            await websocket.send_json(tasks[task_id].model_dump())
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_connections[task_id].remove(websocket)
