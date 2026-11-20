import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Invoice, Visitor
from app.schemas import InvoiceDetail, InvoiceSummary, InvoiceUpdate, RejectIn
from app.services.invoices import (
    EditError,
    ReviewError,
    apply_update,
    approve,
    inventory_by_sku,
    list_summaries,
    reject,
    to_detail,
)
from app.services.visitors import get_visitor

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


def visitor_invoice(db: Session, visitor: Visitor, invoice_id: uuid.UUID) -> Invoice:
    invoice = db.get(Invoice, invoice_id)
    if invoice is None or invoice.visitor_id != visitor.id:
        raise HTTPException(404, "Invoice not found")
    return invoice


@router.get("", response_model=list[InvoiceSummary], summary="List the visitor's invoices, newest first")
def list_invoices(visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    return list_summaries(db, visitor.id)


@router.get("/{invoice_id}", response_model=InvoiceDetail, summary="Get one invoice with lines, flags and cost")
def get_invoice(invoice_id: uuid.UUID, visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    return to_detail(db, visitor_invoice(db, visitor, invoice_id))


@router.patch(
    "/{invoice_id}",
    response_model=InvoiceDetail,
    summary="Save edits, confirm flagged fields and re-run the checks",
    responses={409: {"description": "Invoice is approved or rejected"}},
)
def update_invoice(
    invoice_id: uuid.UUID,
    update: InvoiceUpdate,
    visitor: Visitor = Depends(get_visitor),
    db: Session = Depends(get_db),
):
    invoice = visitor_invoice(db, visitor, invoice_id)
    try:
        apply_update(db, invoice, update, inventory_by_sku(db, visitor.id))
    except EditError as error:
        raise HTTPException(409, str(error)) from error
    db.commit()
    return to_detail(db, invoice)


@router.post(
    "/{invoice_id}/approve",
    response_model=InvoiceDetail,
    summary="Approve the invoice and add its stock lines to inventory",
    responses={409: {"description": "Red fields are still open, or the invoice is already done"}},
)
def approve_invoice(invoice_id: uuid.UUID, visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    invoice = visitor_invoice(db, visitor, invoice_id)
    try:
        approve(db, invoice, inventory_by_sku(db, visitor.id))
    except ReviewError as error:
        raise HTTPException(409, str(error)) from error
    db.commit()
    return to_detail(db, invoice)


@router.post(
    "/{invoice_id}/reject",
    response_model=InvoiceDetail,
    summary="Reject the invoice with a reason",
    responses={409: {"description": "Invoice is already approved or rejected"}},
)
def reject_invoice(
    invoice_id: uuid.UUID,
    body: RejectIn,
    visitor: Visitor = Depends(get_visitor),
    db: Session = Depends(get_db),
):
    invoice = visitor_invoice(db, visitor, invoice_id)
    try:
        reject(invoice, body.reason)
    except ReviewError as error:
        raise HTTPException(409, str(error)) from error
    db.commit()
    return to_detail(db, invoice)