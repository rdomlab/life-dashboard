import ollama
import json
import os
from typing import Dict, List, Any

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "gemma:2b")

# Additional configuration for optimized performance
CONTEXT_LENGTH = int(os.getenv("OLLAMA_CONTEXT_LENGTH", "2048"))
KEEP_ALIVE = os.getenv("OLLAMA_KEEP_ALIVE", "2m")
MAX_LOADED_MODELS = int(os.getenv("OLLAMA_MAX_LOADED_MODELS", "2"))
NUM_PARALLEL = int(os.getenv("OLLAMA_NUM_PARALLEL", "1"))
KV_CACHE_TYPE = os.getenv("OLLAMA_KV_CACHE_TYPE", "f16")

# Validate that we can connect to Ollama
try:
    import httpx
    response = httpx.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
    if response.status_code != 200:
        print(f"Warning: Could not connect to Ollama at {OLLAMA_HOST}")
except Exception as e:
    print(f"Warning: Could not verify Ollama connection: {e}")

def get_ai_insight(prompt: str) -> str:
    """Get AI insight based on user prompt"""
    try:
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            stream=False
        )
        return response['response']
    except Exception as e:
        return f"Error generating insight: {str(e)}"

def summarize_week() -> str:
    """Summarize the user's week"""
    try:
        # Get all metrics from local storage to provide context
        from app.data import storage

        tasks = storage.get_tasks()
        calendar_events = storage.get_calendar_events()
        health_logs = storage.get_health_logs()
        github_activity = storage.get_github_activity()

        # Create a more informative summary prompt
        prompt = f"""
        Please summarize the user's week in a concise and helpful way.
        Include key accomplishments, challenges, and suggestions for improvement.

        Here's what I can tell you about the user's activities:
        Tasks completed: {len(tasks)} tasks
        Calendar events: {len(calendar_events)} events
        Health logs: {len(health_logs)} entries
        GitHub activity: {len(github_activity)} activities

        If you can't summarize from this data, please explain that the dashboard can only summarize data it has access to locally.
        """

        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            stream=False
        )
        return response['response']
    except Exception as e:
        return f"Error summarizing week: {str(e)}. The dashboard can only summarize data it has access to locally. Please add your activities to the dashboard first. For now, here's what I can tell you: This dashboard provides AI insights based on your local data. Your activities are stored locally in the database and can be viewed on the main dashboard page."

def generate_plan(days: int = 3) -> str:
    """Generate a plan for specified number of days"""
    try:
        prompt = f"""
        Please generate a {days}-day plan for the user.
        The plan should include priorities, tasks, and recommendations.
        """
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            stream=False
        )
        return response['response']
    except Exception as e:
        return f"Error generating plan: {str(e)}"

def list_available_models() -> List[Dict[str, Any]]:
    """List all available models"""
    try:
        response = ollama.list()
        return response['models']
    except Exception as e:
        return []

def load_model(model_name: str) -> bool:
    """Load a specific model (this is handled automatically by Ollama)"""
    try:
        # Ollama automatically loads models when first used
        # This function is here for future expansion
        return True
    except Exception as e:
        return False

def unload_model(model_name: str) -> bool:
    """Unload a specific model"""
    try:
        ollama.delete(model=model_name)
        return True
    except Exception as e:
        return False