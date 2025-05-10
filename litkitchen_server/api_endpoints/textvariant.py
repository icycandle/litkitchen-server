from typing import List

from fastapi import APIRouter, HTTPException

from fastapi import Depends
from litkitchen_server.api.schemas import TextVariantSchema
from fastapi import Query
from litkitchen_server.infrastructure.text_variant_repository import (
    TextVariantRepository,
)
from litkitchen_server.infrastructure.repository_provider import get_text_variant_repo

router = APIRouter()


@router.get("/text-variants/filter", response_model=List[TextVariantSchema])
def filter_text_variants(
    main_dish_text_id: int = Query(...),
    side_dish_media_id: int = Query(...),
    drink_style_id: int = Query(...),
    repo: TextVariantRepository = Depends(get_text_variant_repo),
):
    # 取得所有符合條件的 textvariants
    all_tv = repo.get_all()
    candidates = [
        tv
        for tv in all_tv
        if tv.main_dish_text_id == main_dish_text_id
        and tv.side_dish_media_id == side_dish_media_id
        and tv.drink_style_id == drink_style_id
    ]
    if not candidates:
        return []
    chosen = min(candidates, key=lambda tv: (tv.print_count, tv.id))
    return [chosen]


@router.get("/text-variants/{item_id}", response_model=TextVariantSchema)
def get_text_variant(
    item_id: int, repo: TextVariantRepository = Depends(get_text_variant_repo)
):
    item = repo.get(item_id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="TextVariant not found")
