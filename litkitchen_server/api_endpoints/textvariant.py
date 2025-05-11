from fastapi import APIRouter, HTTPException

from fastapi import Depends
from litkitchen_server.api.schemas import TextVariantSchema
from fastapi import Query
from litkitchen_server.infrastructure.text_variant_repository import (
    TextVariantRepository,
)
from litkitchen_server.infrastructure.repository_provider import get_text_variant_repo

router = APIRouter()


@router.get("/pick-best", response_model=TextVariantSchema)
def pick_best_text_variant(
    main_dish_text_id: int = Query(...),
    side_dish_media_id: int = Query(...),
    drink_style_id: int = Query(...),
    repo: TextVariantRepository = Depends(get_text_variant_repo),
):
    """
    根據三個 id，選出 print_count、id 最小的最佳 textvariant。
    若無符合則回傳 404。
    """
    all_tv = repo.get_all()
    candidates = [
        tv
        for tv in all_tv
        if tv.main_dish_text_id == main_dish_text_id
        and tv.side_dish_media_id == side_dish_media_id
        and tv.drink_style_id == drink_style_id
    ]
    if not candidates:
        raise HTTPException(status_code=404, detail="No matching textvariant found")
    # 先找 print_count 最小值
    min_print_count = min(tv.print_count for tv in candidates)
    min_candidates = [tv for tv in candidates if tv.print_count == min_print_count]
    # 再於這些中找 id 最小
    chosen = min(min_candidates, key=lambda tv: tv.id)
    return TextVariantSchema.from_domain(chosen)


@router.get("/{item_id}", response_model=TextVariantSchema)
def get_text_variant(
    item_id: int, repo: TextVariantRepository = Depends(get_text_variant_repo)
):
    item = repo.get(item_id)
    if item:
        return TextVariantSchema.from_domain(item)
    raise HTTPException(status_code=404, detail="TextVariant not found")
