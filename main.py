import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

from claude_analyzer import analyze_lead
from database import init_db, save_lead, get_all_leads, get_lead_stats

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="AutoFlow AI Demo", lifespan=lifespan)


class LeadRequest(BaseModel):
    name: str
    email: str
    company: str = ""
    budget: int = 0
    message: str = ""


class N8nWebhookPayload(BaseModel):
    name: str
    email: str
    company: str = ""
    budget: int = 0
    message: str = ""


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "AutoFlow AI Demo"}


@app.post("/analyze-lead")
async def analyze_lead_endpoint(lead: LeadRequest):
    lead_data = lead.model_dump()
    try:
        analysis = await analyze_lead(lead_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Claude analysis failed: {str(e)}")

    lead_id = await save_lead(lead_data, analysis)

    return {
        "id": lead_id,
        "lead": lead_data,
        "analysis": analysis,
    }


@app.post("/webhook/n8n")
async def n8n_webhook(payload: N8nWebhookPayload):
    lead_data = payload.model_dump()
    try:
        analysis = await analyze_lead(lead_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    lead_id = await save_lead(lead_data, analysis)

    score = analysis.get("score", "Cold")
    routing = {
        "Hot": "high_priority_queue",
        "Warm": "standard_queue",
        "Cold": "nurture_queue",
    }.get(score, "standard_queue")

    return {
        "id": lead_id,
        "score": score,
        "routing": routing,
        "analysis": analysis,
        "lead": lead_data,
    }


@app.get("/dashboard")
async def dashboard():
    leads = await get_all_leads()
    stats = await get_lead_stats()
    return {"stats": stats, "leads": leads}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")
