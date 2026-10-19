
import json
import os
from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# Load environment variables from the backend directory
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

from .schemas import CropInputs, KnowledgeQuestion, AdvisoryRequest
from .db import SessionLocal, init_db, PredictionRecord
from .ml import load_model, predict
from .knowledge import retrieve, grounded_answer
from .agents_crewai import specialist_advisory


_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _model

    init_db()

    try:
        _model = load_model()
    except RuntimeError:
        _model = None

    yield


app = FastAPI(
    title="AgroMind Nexus AI API",
    version="1.0.0",
    description=(
        "Crop recommendation, explainability baseline, "
        "agricultural RAG and advisory prototype."
    ),
    lifespan=lifespan,
)


# Configure CORS for the frontend
origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:5173",
    ).split(",")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def require_model():
    if _model is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Model is not trained. "
                "Run `python scripts/train_model.py` from backend."
            ),
        )

    return _model


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_loaded": _model is not None,
    }


@app.get("/api/model/metrics")
def metrics():
    metrics_path = BASE_DIR / "data" / "metrics.json"

    if not metrics_path.exists():
        return {
            "available": False,
            "message": (
                "Run scripts/train_model.py "
                "to generate metrics."
            ),
        }

    metrics_data = json.loads(
        metrics_path.read_text(encoding="utf-8")
    )

    return {
        "available": True,
        **metrics_data,
    }


@app.post("/api/predict")
def crop_predict(
    payload: CropInputs,
    db: Session = Depends(get_db),
):
    model = require_model()

    inputs = payload.model_dump()
    result = predict(model, inputs)

    record = PredictionRecord(
        crop=result["crop"],
        confidence=result["model_score"],
        inputs_json=json.dumps(inputs),
    )

    db.add(record)
    db.commit()

    return {
        **result,
        "inputs": inputs,
        "disclaimer": (
            "Model score is not the probability of successful "
            "harvest. Validate with local agronomic advice."
        ),
    }


@app.post("/api/knowledge/ask")
def knowledge_ask(payload: KnowledgeQuestion):
    docs = retrieve(payload.question)

    answer = grounded_answer(
        payload.question,
        docs,
        os.getenv("GEMINI_API_KEY"),
        os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    )

    return {
        "question": payload.question,
        "answer": answer,
        "sources": [
            {
                "id": doc["id"],
                "title": doc["title"],
                "source": doc["source"],
                "relevance": doc["relevance"],
            }
            for doc in docs
        ],
    }


@app.post("/api/advisory")
def advisory(
    payload: AdvisoryRequest,
    db: Session = Depends(get_db),
):
    model = require_model()

    inputs = payload.model_dump()

    prediction_inputs = {
        key: value
        for key, value in inputs.items()
        if key != "location"
    }

    prediction = predict(model, prediction_inputs)

    docs = retrieve(
        f"crop suitability soil pH rainfall "
        f"{prediction['crop']} Bangladesh"
    )

    return specialist_advisory(
        inputs,
        prediction,
        docs,
    )


@app.get("/api/history")
def history(
    limit: int = 20,
    db: Session = Depends(get_db),
):
    limit = max(1, min(limit, 100))

    rows = (
        db.query(PredictionRecord)
        .order_by(PredictionRecord.id.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": row.id,
            "created_at": (
                row.created_at.isoformat()
                if row.created_at
                else None
            ),
            "crop": row.crop,
            "model_score": row.confidence,
            "inputs": json.loads(row.inputs_json),
        }
        for row in rows
    ]


# Serve the built frontend if the static directory exists.
# Keep this after the API routes so the API endpoints remain available.
STATIC_DIR = BASE_DIR.parent / "static"

if STATIC_DIR.is_dir():
    app.mount(
        "/",
        StaticFiles(
            directory=str(STATIC_DIR),
            html=True,
        ),
        name="frontend",
    )
