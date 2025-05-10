from typing import List

from fastapi import APIRouter

from litkitchen_server.repository import _db
from litkitchen_server.api.schemas import (
    DrinkStyleSchema,
    MainDishTextSchema,
    SideDishMediaSchema,
)

router = APIRouter()


@router.get("/maindish", response_model=List[MainDishTextSchema])
def list_main_dishes():
    return _db["maindishtexts"]


@router.get("/sidedish", response_model=List[SideDishMediaSchema])
def list_side_dishes():
    return _db["sidedishmedias"]


@router.get("/drinkstyle", response_model=List[DrinkStyleSchema])
def list_drink_styles():
    return _db["drinkstyles"]
