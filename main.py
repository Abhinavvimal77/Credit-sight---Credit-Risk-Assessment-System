# ============================================================
#  main.py — FinGuard FastAPI Application Entry Point
#  Run with: uvicorn main:app --reload
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.database        import init_db
from backend.routes.predict      import router as predict_router
from backend.routes.applications import router as apps_router

# ── Initialize FastAPI app ────────────────────────────────────
app = FastAPI(
    title       = "FinGuard Credit Risk API",
    description = "AI-powered credit risk assessment for loan applications",
    version     = "1.0.0",
)

# ── CORS — allows frontend to call the API ────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],   # In production: restrict to your domain
    allow_methods  = ["*"],
    allow_headers  = ["*"],
)

# ── Initialize database on startup ───────────────────────────
@app.on_event("startup")
def startup():
    print()
    print("=" * 50)
    print("  FinGuard API Starting...")
    print("=" * 50)
    init_db()
    print("  All systems ready!")
    print("=" * 50)
    print()

# ── Register routes ───────────────────────────────────────────
app.include_router(predict_router, tags=["Prediction"])
app.include_router(apps_router,    tags=["Applications"])

# ── Serve frontend static files ───────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# ── Health check endpoint ─────────────────────────────────────
@app.get("/health")
def health_check():
    return {
        "status" : "running",
        "app"    : "FinGuard Credit Risk API",
        "version": "1.0.0"
    }

# ── API docs available at /docs ───────────────────────────────
# FastAPI auto-generates this — visit http://localhost:8000/docs
