from typing import List

from fastapi import APIRouter

from fastapi import Depends
from litkitchen_server.api.schemas import (
    DrinkStyleSchema,
    MainDishTextSchema,
    SideDishMediaSchema,
)
from litkitchen_server.infrastructure.main_dish_text_repository import (
    MainDishTextRepository,
)
from litkitchen_server.infrastructure.side_dish_media_repository import (
    SideDishMediaRepository,
)
from litkitchen_server.infrastructure.drink_style_repository import DrinkStyleRepository
from litkitchen_server.infrastructure.repository_provider import (
    get_main_dish_text_repo,
    get_side_dish_media_repo,
    get_drink_style_repo,
)

router = APIRouter()


@router.get("/maindish", response_model=List[MainDishTextSchema])
def get_maindishtexts(repo: MainDishTextRepository = Depends(get_main_dish_text_repo)):
    return repo.get_all()


@router.get("/sidedish", response_model=List[SideDishMediaSchema])
def get_sidedishmedias(
    repo: SideDishMediaRepository = Depends(get_side_dish_media_repo),
):
    return repo.get_all()


@router.get("/drinkstyle", response_model=List[DrinkStyleSchema])
def get_drinkstyles(repo: DrinkStyleRepository = Depends(get_drink_style_repo)):
    return repo.get_all()
