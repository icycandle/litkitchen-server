from fastapi import APIRouter

from litkitchen_server.api_endpoints import (
    barcodemapping,
    options,
    printjob,
    textvariant,
)

router = APIRouter()

router.include_router(options.router, prefix="/options", tags=["Options"])
router.include_router(textvariant.router, prefix="/text-variants", tags=["TextVariant"])
router.include_router(printjob.router, prefix="", tags=["PrintJob"])
router.include_router(
    barcodemapping.router, prefix="/barcode-mappings", tags=["BarcodeMapping"]
)
