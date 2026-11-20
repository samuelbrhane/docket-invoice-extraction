from app.routers.documents import router as documents_router
from app.routers.extraction import router as extraction_router
from app.routers.invoices import router as invoices_router

__all__ = ["documents_router", "extraction_router", "invoices_router"]