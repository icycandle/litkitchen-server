from fastapi import APIRouter, HTTPException

from fastapi import Depends
from litkitchen_server.api.schemas import BarcodeMappingSchema
from litkitchen_server.infrastructure.barcode_mapping_repository import (
    BarcodeMappingRepository,
)
from litkitchen_server.infrastructure.repository_provider import (
    get_barcode_mapping_repo,
)
from datetime import datetime

from litkitchen_server.domain.models import BarcodeMapping

from litkitchen_server.api.schemas import BarcodeMappingCreateSchema


router = APIRouter()


@router.get("/", response_model=list[BarcodeMappingSchema])
def get_barcodemappings(
    repo: BarcodeMappingRepository = Depends(get_barcode_mapping_repo),
):
    result = repo.get_all()
    return [BarcodeMappingSchema.from_domain(item) for item in result]


@router.post("/", response_model=BarcodeMappingSchema)
def create_barcodemapping(
    item: BarcodeMappingCreateSchema,
    repo: BarcodeMappingRepository = Depends(get_barcode_mapping_repo),
):
    # 將 create schema 轉 domain model，id/created_at 由後端補上
    barcode_item = item.model_dump()
    domain_obj = BarcodeMapping(**barcode_item)
    if not domain_obj.created_at:
        domain_obj.created_at = datetime.now()
    created = repo.create(domain_obj)
    return BarcodeMappingSchema.from_domain(created)


@router.delete("/{item_id}")
def delete_barcodemapping(
    item_id: int, repo: BarcodeMappingRepository = Depends(get_barcode_mapping_repo)
):
    deleted = repo.delete(item_id)
    if deleted:
        return {"ok": True}
    raise HTTPException(status_code=404, detail="BarcodeMapping not found")
