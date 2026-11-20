import json
import uuid
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models import Invoice, InvoiceStatus, Visitor
from app.routers.invoices import visitor_invoice
from app.schemas import SpendingOut, StatsOut
from app.services.reports import spending, stats, to_csv, to_json
from app.services.visitors import get_visitor

router = APIRouter(prefix="/api", tags=["reports"])

Format = Literal["csv", "json"]
EXPORT_RESPONSES = {200: {"content": {"text/csv": {}, "application/json": {}}}}


def _download(db: Session, invoices: list[Invoice], fmt: Format, name: str) -> Response:
    if fmt == "csv":
        body, media_type = to_csv(db, invoices), "text/csv"
    else:
        body, media_type = json.dumps(to_json(db, invoices), indent=2, ensure_ascii=False), "application/json"
    return Response(
        content=body,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{name}.{fmt}"'},
    )


@router.get("/spending", response_model=SpendingOut, summary="Approved spending by month, supplier and category")
def get_spending(visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    return spending(db, visitor.id)


@router.get("/stats", response_model=StatsOut, summary="AI accuracy, issues caught and extraction cost")
def get_stats(visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    return stats(db, visitor.id)


@router.get("/export", summary="Download invoices as CSV or JSON", response_class=Response, responses=EXPORT_RESPONSES)
def export_invoices(
    format: Format = Query("csv", description="csv has one row per line item"),
    status: InvoiceStatus = Query(InvoiceStatus.APPROVED),
    visitor: Visitor = Depends(get_visitor),
    db: Session = Depends(get_db),
):
    invoices = list(db.scalars(
        select(Invoice)
        .options(selectinload(Invoice.lines))
        .where(Invoice.visitor_id == visitor.id, Invoice.status == status)
        .order_by(Invoice.issue_date)
    ))
    return _download(db, invoices, format, f"docket-{status.value}-{date.today().isoformat()}")


@router.get(
    "/invoices/{invoice_id}/export",
    summary="Download one invoice as CSV or JSON",
    response_class=Response,
    responses=EXPORT_RESPONSES,
)
def export_invoice(
    invoice_id: uuid.UUID,
    format: Format = Query("json"),
    visitor: Visitor = Depends(get_visitor),
    db: Session = Depends(get_db),
):
    invoice = visitor_invoice(db, visitor, invoice_id)
    name = f"docket-{(invoice.invoice_number or 'invoice').replace('/', '-').replace(' ', '')}"
    return _download(db, [invoice], format, name)