from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Visitor
from app.schemas import InventoryItemOut, MovementOut
from app.services.reports import find_item, list_inventory, list_movements
from app.services.visitors import get_visitor

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.get("", response_model=list[InventoryItemOut], summary="List stock items with quantity, value and last delivery")
def get_inventory(visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    return list_inventory(db, visitor.id)


@router.get("/{sku}/movements", response_model=list[MovementOut], summary="List the approved deliveries for one item")
def get_movements(sku: str, visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    item = find_item(db, visitor.id, sku)
    if item is None:
        raise HTTPException(404, "Inventory item not found")
    return list_movements(db, item)