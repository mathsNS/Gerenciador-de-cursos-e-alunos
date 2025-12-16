from fastapi import APIRouter
from src.core.container import sistema
from src.core.repository import Repository

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
def health():
    return {"status": "ok"}
