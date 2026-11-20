from fastapi import APIRouter, Depends

from app.models import Visitor
from app.services.visitors import get_visitor

router = APIRouter(prefix="/api", tags=["session"])


@router.get("/session", summary="Start or continue the visitor session")
def session(visitor: Visitor = Depends(get_visitor)):
    """The frontend calls this once before anything else, so only one visitor is created on a first visit."""
    return {"ok": True}