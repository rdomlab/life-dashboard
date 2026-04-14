from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import json
import os

from app.data import storage
from app.api import ollama_client
from app.memory import semantic_memory

router = APIRouter(
    prefix="/api",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)

@router.get("/metrics")
async def get_metrics():
    """Get all dashboard metrics"""
    try:
        # Get data from local storage
        tasks = storage.get_tasks()
        calendar_events = storage.get_calendar_events()
        health_logs = storage.get_health_logs()
        github_activity = storage.get_github_activity()

        return {
            "tasks": tasks,
            "calendar_events": calendar_events,
            "health_logs": health_logs,
            "github_activity": github_activity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks")
async def get_tasks():
    """Get all tasks"""
    try:
        return storage.get_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calendar")
async def get_calendar():
    """Get calendar events"""
    try:
        return storage.get_calendar_events()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health-logs")
async def get_health_logs():
    """Get health logs"""
    try:
        return storage.get_health_logs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/github")
async def get_github_activity():
    """Get GitHub activity"""
    try:
        return storage.get_github_activity()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/insight")
async def get_ai_insight(prompt: Dict[str, str]):
    """Get AI insights based on user prompt"""
    try:
        insight = ollama_client.get_ai_insight(prompt["text"])
        return {"insight": insight}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/summarize")
async def summarize_week():
    """Summarize the user's week"""
    try:
        summary = ollama_client.summarize_week()
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/plan")
async def generate_plan(days: Dict[str, int] = {"days": 3}):
    """Generate a plan for specified number of days"""
    try:
        plan = ollama_client.generate_plan(days["days"])
        return {"plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory")
async def get_memory():
    """Get semantic memory"""
    try:
        memory = semantic_memory.get_memory()
        return {"memory": memory}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/memory/add")
async def add_to_memory(data: Dict[str, Any]):
    """Add data to semantic memory"""
    try:
        # Handle different input formats
        if isinstance(data, dict):
            # If it's a dictionary with text field
            if "text" in data:
                semantic_memory.add_to_memory(data["text"])
            # If it's a dictionary with memory field (structured memory)
            elif "memory" in data:
                # For structured memory, convert to JSON string
                memory_text = json.dumps(data["memory"], indent=2)
                semantic_memory.add_to_memory(memory_text)
            else:
                # If no specific field, treat entire data as text
                text = json.dumps(data, indent=2)
                semantic_memory.add_to_memory(text)
        else:
            # If it's just text
            semantic_memory.add_to_memory(str(data))
        return {"status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))