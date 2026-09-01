from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.api import events, risk, cases, simulator, policies, audit, metrics, webhooks, experiments

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    yield

app = FastAPI(title="REVIVE Backend API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS if settings.BACKEND_CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)
app.include_router(risk.router)
app.include_router(cases.router)
app.include_router(simulator.router)
app.include_router(policies.router)
app.include_router(audit.router)
app.include_router(metrics.router)
app.include_router(webhooks.router)
app.include_router(experiments.router)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0", "env": settings.APP_ENV}

@app.post("/api/admin/clear-db")
async def clear_database():
    from app.database import reset_db
    return reset_db()


