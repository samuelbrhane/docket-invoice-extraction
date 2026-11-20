from app.routers.demo import router as demo_router
from app.routers.documents import router as documents_router
from app.routers.extraction import router as extraction_router
from app.routers.inventory import router as inventory_router
from app.routers.invoices import router as invoices_router
from app.routers.reports import router as reports_router
from app.routers.session import router as session_router

__all__ = [
    "demo_router",
    "documents_router",
    "extraction_router",
    "inventory_router",
    "invoices_router",
    "reports_router",
    "session_router",
]