from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from database import db, create_document
from schemas import Contact
import os

app = FastAPI(title="Connor Clark Portfolio API")

# CORS
frontend_url = os.getenv("FRONTEND_URL")
origins = [
    frontend_url or "*",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Backend is running"}


@app.get("/test")
async def test_db():
    status = "connected" if db is not None else "unavailable"
    resp: Dict[str, Any] = {
        "backend": "ok",
        "database": "mongodb",
        "connection_status": status,
        "database_url": os.getenv("DATABASE_URL", "unset"),
        "database_name": os.getenv("DATABASE_NAME", "unset"),
        "collections": list(db.list_collection_names()) if db is not None else [],
    }
    return resp


@app.post("/contact")
async def submit_contact(payload: Contact):
    try:
        doc_id = create_document("contact", payload)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
