from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.ai import generate
from app.notion import save
from app.validation import validate_feature

from app.schemas import (
    GenerateRequest,
    ImproveRequest,
    SaveRequest
)

from app.prompts import (
    TEMPLATES,
    QUIZ_PROMPT,
    GRAMMAR_PROMPT,
    REWRITE_PROMPT,
    SUMMARY_PROMPT,
    EXPAND_PROMPT
)


app = FastAPI(
    title="AI Writing Assistant"
)


FRONTEND = (
    Path(__file__)
    .resolve()
    .parent.parent.parent
    / "frontend"
)


app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND),
    name="frontend"
)


@app.get("/")
def home():
    return FileResponse(
        FRONTEND / "index.html"
    )


@app.post("/generate")
def create(data: GenerateRequest):

    if not data.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Topic required"
        )

    valid, message = validate_feature(
        data.content_type,
        data.topic
    )

    if not valid:
        raise HTTPException(
            status_code=400,
            detail=message
        )

    if data.content_type == "Quiz Generation":
        prompt = f"""
{QUIZ_PROMPT}

Topic:
{data.topic}
"""
    else:
        prompt = f"""
Create educational content.

Type:
{data.content_type}

Tone:
{data.tone}

Topic:
{data.topic}

Instructions:
{TEMPLATES.get(data.content_type, "")}
"""

    try:
        return {
            "output": generate(prompt),
            "content_type": data.content_type,
            "quiz": data.content_type == "Quiz Generation"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/generate-improve")
def improve(data: ImproveRequest):

    if not data.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text required"
        )

    prompts = {
        "Correct Grammar": GRAMMAR_PROMPT,
        "Rewrite & Improve": REWRITE_PROMPT,
        "Summarize": SUMMARY_PROMPT,
        "Expand": EXPAND_PROMPT
    }

    prompt = f"""
{prompts.get(data.task, GRAMMAR_PROMPT)}

Text:
{data.text}
"""

    try:
        return {
            "output": generate(
                prompt,
                data.temperature
            )
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/save-notion")
def save_notion(data: SaveRequest):

    try:
        save(data.text)

        return {
            "message": "Saved successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/health")
def health():
    return {
        "status": "ok"
    }