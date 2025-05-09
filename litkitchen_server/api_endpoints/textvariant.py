from typing import List

from fastapi import APIRouter, HTTPException

from litkitchen_server.repository import _db
from litkitchen_server.schemas import TextVariantSchema
from fastapi import Query

router = APIRouter()


@router.get("/text-variants/filter", response_model=List[TextVariantSchema])
def filter_text_variants(
    main_dish_text_id: int = Query(...),
    side_dish_media_id: int = Query(...),
    drink_style_id: int = Query(...),
):
    candidates = [
        tv
        for tv in _db["textvariants"]
        if tv.main_dish_text_id == main_dish_text_id
        and tv.side_dish_media_id == side_dish_media_id
        and tv.drink_style_id == drink_style_id
    ]
    if not candidates:
        return []
    # 找出 print_count 最小的那一筆（若有多筆同最小則取 id 最小）
    chosen = min(candidates, key=lambda tv: (tv.print_count, tv.id))
    return [chosen]


@router.get("/textvariant/{item_id}", response_model=TextVariantSchema)
def get_text_variant(item_id: int):
    for item in _db["textvariants"]:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="TextVariant not found")
