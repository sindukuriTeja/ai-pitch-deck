# AI Pitch Deck Generator

An intelligent, multi-agent AI system built with FastAPI and Python that automatically researches, structures, and generates professional, editable PowerPoint (`.pptx`) pitch decks from a simple prompt.

## Features

- **Multi-Agent Architecture**: Employs specialized AI agents for different stages of generation:
  - 🔍 **Research Agent**: Gathers market and brand data using DuckDuckGo search.
  - 🎯 **Strategy Agent**: Formulates a strategic direction tailored to the target audience.
  - 🎨 **Creative Agent**: Generates structured, compelling slide content and HTML layouts.
  - 🖼️ **Image Agent**: Generates professional AI images for slide visuals using Stable Diffusion XL.
  - ✅ **Review Agent**: Performs quality review and alignment checks on the final deck.
- **HTML to PPTX Engine**: Converts structured AI output directly into an editable `.pptx` file.
- **Real-Time Updates**: Uses WebSockets to stream generation progress to the UI.
- **Modern Web Interface**: Built-in web dashboard to input your brand details, problem statement, and audience.
- **Cloud AI Powered**: Integrated with Hugging Face Inference API using Qwen3-30B-A3B model.
- **12 Industry Themes**: Tech Startup, Healthcare, Finance, Creative Agency, E-Commerce, Education, Real Estate, Food & Beverage, SaaS/B2B, Sustainability, Fashion & Luxury, Sports & Fitness.

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI Text Model**: Hugging Face Inference API (`huggingface-hub`), Qwen3-30B-A3B
- **AI Image Model**: Stable Diffusion XL (via Hugging Face Inference API)
- **Search**: `duckduckgo-search`
- **Document Generation**: `python-pptx`
- **Frontend**: HTML/Jinja2 Templates, Vanilla JS, WebSockets

## Prerequisites

1. **Python 3.10+** installed on your system.
2. **Hugging Face API Key** with access to inference endpoints.

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sindukuriTeja/ai-pitch-deck.git
   cd ai-pitch-deck
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Hugging Face API key
   ```

## Configuration

You can configure the following environment variables in your `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `HUGGINGFACE_API_KEY` | *(required)* | Your Hugging Face API token |
| `HUGGINGFACE_MODEL` | `Qwen/Qwen3-30B-A3B` | The text model for content generation |
| `HUGGINGFACE_IMAGE_MODEL` | `stabilityai/stable-diffusion-xl-base-1.0` | The image model for slide visuals |

## Running the Application

1. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Open your browser and navigate to: [http://localhost:8000](http://localhost:8000)

## How it Works

1. Enter your **Brand Name**, **Problem Statement**, **Target Audience**, and desired **Tone** on the web interface.
2. Select an industry **Theme** that matches your pitch.
3. The backend spins up asynchronous AI agents that:
   - Research the market using DuckDuckGo
   - Develop a strategic narrative direction
   - Generate creative slide content with HTML layouts
   - Review and refine the copy for quality
   - Generate AI images for key slides
   - Build the final `.pptx` file
4. Real-time progress is streamed back to your browser via WebSockets.
5. Once generation is complete, download the fully formatted, editable `.pptx` file directly from the UI.

## Model Info

This project uses **Qwen3-30B-A3B** by Alibaba/Qwen, a powerful conversational AI model available on Hugging Face. It excels at structured reasoning, JSON generation, and creative content — making it ideal for pitch deck generation.

For image generation, **Stable Diffusion XL** is used to create professional, cinematic visuals for the pitch deck slides.
