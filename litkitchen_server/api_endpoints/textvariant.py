from fastapi import APIRouter, HTTPException

from fastapi import Depends
from litkitchen_server.api.schemas import TextVariantSchema
from fastapi import Query
from litkitchen_server.domain.repository import (
    IDrinkStyleRepository,
    IMainDishTextRepository,
    ISideDishMediaRepository,
    ITextVariantRepository,
)
from litkitchen_server.infrastructure.printer import PrintJobParams, get_printer_worker
from litkitchen_server.infrastructure.text_variant_repository import (
    TextVariantRepository,
)
from litkitchen_server.infrastructure.repository_provider import (
    get_drink_style_repo,
    get_main_dish_text_repo,
    get_side_dish_media_repo,
    get_text_variant_repo,
)

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


@router.get("/print/{main_dish_text_id}/{side_dish_media_id}/{drink_style_id}")
def print_count_pick_best(
    main_dish_text_id: int,
    side_dish_media_id: int,
    drink_style_id: int,
    repo: ITextVariantRepository = Depends(get_text_variant_repo),
    main_dish_repo: IMainDishTextRepository = Depends(get_main_dish_text_repo),
    side_dish_media_repo: ISideDishMediaRepository = Depends(get_side_dish_media_repo),
    drink_style_repo: IDrinkStyleRepository = Depends(get_drink_style_repo),
    printer_worker=Depends(get_printer_worker),
):
    """
    根據三個 id，選出 print_count、id 最小的最佳 textvariant。
    若無符合則回傳 404。
    """
    candidates = repo.query(
        main_dish_text_id=main_dish_text_id,
        side_dish_media_id=side_dish_media_id,
        drink_style_id=drink_style_id,
    )
    if not candidates:
        raise HTTPException(status_code=404, detail="No matching textvariant found")

    # 先找 print_count 最小值
    min_print_count = min(tv.print_count for tv in candidates)
    min_candidates = [tv for tv in candidates if tv.print_count == min_print_count]

    # 再於這些中找 id 最小
    chosen = min(min_candidates, key=lambda tv: tv.id)

    main_dish_text = main_dish_repo.get(main_dish_text_id)
    side_dish_media = side_dish_media_repo.get(side_dish_media_id)
    drink_style = drink_style_repo.get(drink_style_id)

    # 印表機列印
    ok = printer_worker.submit_print(
        PrintJobParams(
            result_text=chosen.content,
            option_a_label=main_dish_text.build_label(),
            option_b_label=side_dish_media.media_type,
            option_c_label=drink_style.style,
        )
    )
    return {"ok": ok}
