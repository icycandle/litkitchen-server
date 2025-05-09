from typing import List

from fastapi import APIRouter, HTTPException

from litkitchen_server.repository import _db
from litkitchen_server.schemas import BarcodeMappingSchema

router = APIRouter()


@router.get("/", response_model=List[BarcodeMappingSchema])
def list_barcodemappings():
    return _db["barcodemappings"]


@router.post("/", response_model=BarcodeMappingSchema)
def create_barcodemapping(item: BarcodeMappingSchema):
    _db["barcodemappings"].append(item)
    return item


@router.delete("/{item_id}")
def delete_barcodemapping(item_id: int):
    for idx, orig in enumerate(_db["barcodemappings"]):
        if orig.id == item_id:
            del _db["barcodemappings"][idx]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="BarcodeMapping not found")
