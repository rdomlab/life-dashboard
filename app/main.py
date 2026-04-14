from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import os

# Import our application components
from app.api import routes
from app.data import storage
from app.memory import semantic_memory

# Initialize FastAPI app
app = FastAPI(
    title="Life Dashboard",
    description="Personal dashboard for tracking metrics and AI insights",
    version="0.1.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

# Include API routes
app.include_router(routes.router)

# Initialize data storage and memory
storage.init_storage()
semantic_memory.init_memory()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)