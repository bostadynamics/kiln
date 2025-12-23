# src/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .routers import hardware, monitoring, ui
from .core.config import STATIC_DIR

app = FastAPI(title="Unified Kiln Controller")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include Routers
app.include_router(hardware.router)
app.include_router(monitoring.router)
app.include_router(ui.router)


@app.on_event("startup")
async def startup_event():
    print("Unified Kiln Service starting...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Unified Kiln Service shutting down...")
    await monitoring.shutdown_monitoring()
