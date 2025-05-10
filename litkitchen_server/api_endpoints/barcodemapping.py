from typing import List

from fastapi import APIRouter, HTTPException

from fastapi import Depends
from litkitchen_server.api.schemas import BarcodeMappingSchema
from litkitchen_server.infrastructure.barcode_mapping_repository import (
    BarcodeMappingRepository,
)
from litkitchen_server.infrastructure.repository_provider import (
    get_barcode_mapping_repo,
)

router = APIRouter()


@router.get("/", response_model=List[BarcodeMappingSchema])
def get_barcodemappings(
    repo: BarcodeMappingRepository = Depends(get_barcode_mapping_repo),
):
    return repo.get_all()


@router.post("/", response_model=BarcodeMappingSchema)
def create_barcodemapping(
    item: BarcodeMappingSchema,
    repo: BarcodeMappingRepository = Depends(get_barcode_mapping_repo),
):
    created = repo.create(item)
    return created


@router.delete("/{item_id}")
def delete_barcodemapping(
    item_id: int, repo: BarcodeMappingRepository = Depends(get_barcode_mapping_repo)
):
    deleted = repo.delete(item_id)
    if deleted:
        return {"ok": True}
    raise HTTPException(status_code=404, detail="BarcodeMapping not found")
