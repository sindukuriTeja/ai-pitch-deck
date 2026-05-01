# AI Pitch Deck Generator

An intelligent, multi-agent AI system built with FastAPI and Python that automatically researches, structures, and generates professional, editable PowerPoint (`.pptx`) pitch decks from a simple prompt.

## Features

- **Multi-Agent Architecture**: Employs specialized AI agents for different stages of generation:
  - 🔍 **Research Agent**: Gathers market and brand data using DuckDuckGo search.
  - 🎯 **Strategy Agent**: Formulates a strategic direction tailored to the target audience.
  - 🎨 **Creative Agent**: Generates structured, compelling slide content and HTML layouts.
- **HTML to PPTX Engine**: Converts structured AI output directly into an editable `.pptx` file.
- **Real-Time Updates**: Uses WebSockets to stream generation progress to the UI.
- **Modern Web Interface**: Built-in web dashboard to input your brand details, problem statement, and audience.
- **Cloud AI Powered**: Integrated with Hugging Face Inference API using Xiaomi's MiMo-V2-Flash model.

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI Processing**: Hugging Face Inference API (`huggingface-hub`), MiMo-V2-Flash
- **Search**: `duckduckgo-search`
- **Document Generation**: `python-pptx`
- **Frontend**: HTML/Jinja2 Templates, Vanilla JS, WebSockets

## Prerequisites

1. **Python 3.10+** installed on your system.
2. **Hugging Face API Key** with access to inference endpoints.

## Installation & Setup

1. **Clone the repository** (if you haven't already):
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

5. **Set your Hugging Face API key** (optional if hardcoded in config):
   ```bash
   export HUGGINGFACE_API_KEY="hf_your_api_key_here"
   ```

## Configuration

You can configure the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `HUGGINGFACE_API_KEY` | *(set in config)* | Your Hugging Face API token |
| `HUGGINGFACE_MODEL` | `XiaomiMiMo/MiMo-V2-Flash` | The model to use for inference |

## Running the Application

1. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Open your browser and navigate to: [http://localhost:8000](http://localhost:8000)

## How it Works

1. Enter your **Brand Name**, **Problem Statement**, **Target Audience**, and desired **Tone** on the web interface.
2. The backend spins up asynchronous AI agents that research the market, develop a content strategy, and write the slides.
3. The real-time progress is streamed back to your browser via WebSockets.
4. Once generation is complete, you can download the fully formatted, editable `.pptx` file directly from the UI.

## Model Info

This project uses **MiMo-V2-Flash** by Xiaomi, a powerful conversational AI model available on Hugging Face. It excels at structured reasoning, JSON generation, and creative content — making it ideal for pitch deck generation.
