import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import CRON_SECRET
from app.db import get_db
from app.services.cleanup import run_cleanup

router = APIRouter(prefix="/api/cron", tags=["system"])


def _check_secret(authorization: str | None) -> None:
    # Vercel Cron sends "Authorization: Bearer <CRON_SECRET>"
    expected = f"Bearer {CRON_SECRET}"
    if not CRON_SECRET or not secrets.compare_digest(authorization or "", expected):
        raise HTTPException(status_code=401, detail="Not allowed")


@router.get("/cleanup", include_in_schema=False)
def cleanup(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    _check_secret(authorization)
    result = run_cleanup(db)
    db.commit()
    return result