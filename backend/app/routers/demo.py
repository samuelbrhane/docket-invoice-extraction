from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Visitor
from app.services.visitors import get_visitor, reset_visitor, set_visitor_cookie

router = APIRouter(prefix="/api/demo", tags=["demo"])


@router.post("/reset", status_code=204, summary="Clear this visitor's data and start again with the example history")
def reset(response: Response, visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    fresh = reset_visitor(db, visitor)
    db.commit()
    set_visitor_cookie(response, fresh)