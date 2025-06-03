from typing import List

from fastapi import APIRouter

from fastapi import Depends
from litkitchen_server.api.schemas import (
    DrinkStyleSchema,
    MainDishTextSchema,
    SideDishMediaSchema,
)
from litkitchen_server.domain.repository import (
    IDrinkStyleRepository,
    IMainDishTextRepository,
    ISideDishMediaRepository,
)

from litkitchen_server.infrastructure.repository_provider import (
    get_main_dish_text_repo,
    get_side_dish_media_repo,
    get_drink_style_repo,
)

router = APIRouter()


@router.get("/maindish", response_model=List[MainDishTextSchema])
def get_maindishtexts(repo: IMainDishTextRepository = Depends(get_main_dish_text_repo)):
    return repo.get_all()


@router.get("/sidedish", response_model=List[SideDishMediaSchema])
def get_sidedishmedias(
    repo: ISideDishMediaRepository = Depends(get_side_dish_media_repo),
):
    return repo.get_all()


@router.get("/drinkstyle", response_model=List[DrinkStyleSchema])
def get_drinkstyles(repo: IDrinkStyleRepository = Depends(get_drink_style_repo)):
    return repo.get_all()
