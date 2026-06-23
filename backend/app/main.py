import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from .routes import agent, tests, workflow

# Initialize FastAPI App
app = FastAPI(
    title="Plateforme de Validation des Agents IA",
    description="Backend API de conformité et de monitoring de l'atelier de validation continue",
    version="1.0.0"
)

# Enable CORS for frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(agent.router, prefix="/api")
app.include_router(tests.router, prefix="/api")
app.include_router(workflow.router, prefix="/api")

@app.get("/health", tags=["System"])
def health_check():
    """
    Returns system health status.
    """
    return {"status": "healthy", "service": "validation-engine", "uptime": "nominal"}

# Serve frontend statically
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    @app.get("/")
    def index():
        return HTMLResponse("<h1>Plateforme de Validation active</h1><p>Dossier frontend introuvable.</p>")
