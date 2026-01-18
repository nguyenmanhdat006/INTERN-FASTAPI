from fastapi import APIRouter
from .categories import router as category_router
from .products import router as product_router
from .invoices import router as invoice_router
from .auth import router as auth_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(category_router)
router.include_router(product_router)
router.include_router(invoice_router)

__all__ = ["router"]
