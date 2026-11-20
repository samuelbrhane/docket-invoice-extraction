from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db
from app.routers import (
    demo_router,
    documents_router,
    extraction_router,
    inventory_router,
    invoices_router,
    reports_router,
)

app = FastAPI(
    title="Docket API",
    description="AI invoice extraction with validation checks, human review and inventory updates.",
    version="0.1.0",
    # Under /api so the docs work through the Next.js proxy too
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)

app.include_router(documents_router)
app.include_router(extraction_router)
app.include_router(invoices_router)
app.include_router(inventory_router)
app.include_router(reports_router)
app.include_router(demo_router)


@app.get("/api/health", tags=["system"], summary="Check the API and database")
def health(db: Session = Depends(get_db)):
    db.execute(text("select 1"))
    return {"status": "ok", "database": "ok"}