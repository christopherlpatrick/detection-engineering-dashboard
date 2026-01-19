"""
Detection Engineering Simulation Dashboard - Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import init_db
from app.routers import dashboard, detections, events, incidents, response_actions

app = FastAPI(
    title="Detection Engineering Simulation Dashboard API",
    description="API for SOC Detection Engineering Simulation Dashboard",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
app.include_router(detections.router, prefix="/api/v1", tags=["Detections"])
app.include_router(events.router, prefix="/api/v1", tags=["Events"])
app.include_router(incidents.router, prefix="/api/v1", tags=["Incidents"])
app.include_router(response_actions.router, prefix="/api/v1", tags=["Response Actions"])


@app.get("/")
async def root():
    return {
        "name": "Detection Engineering Simulation Dashboard API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}
