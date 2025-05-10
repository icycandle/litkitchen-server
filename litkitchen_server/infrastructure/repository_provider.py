import os
from sqlmodel import create_engine, Session
from fastapi import Depends
from litkitchen_server.infrastructure.main_dish_text_repository import (
    MainDishTextRepository,
)
from litkitchen_server.infrastructure.side_dish_media_repository import (
    SideDishMediaRepository,
)
from litkitchen_server.infrastructure.drink_style_repository import DrinkStyleRepository
from litkitchen_server.infrastructure.text_variant_repository import (
    TextVariantRepository,
)
from litkitchen_server.infrastructure.print_job_repository import PrintJobRepository
from litkitchen_server.infrastructure.barcode_mapping_repository import (
    BarcodeMappingRepository,
)

DB_PATH = os.environ.get(
    "LITKITCHEN_DB_PATH",
    os.path.join(os.path.dirname(__file__), "../db.sqlite3"),
)
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    with Session(engine) as session:
        yield session


def get_main_dish_text_repo(session=Depends(get_session)):
    return MainDishTextRepository(session)


def get_side_dish_media_repo(session=Depends(get_session)):
    return SideDishMediaRepository(session)


def get_drink_style_repo(session=Depends(get_session)):
    return DrinkStyleRepository(session)


def get_text_variant_repo(session=Depends(get_session)):
    return TextVariantRepository(session)


def get_print_job_repo(session=Depends(get_session)):
    return PrintJobRepository(session)


def get_barcode_mapping_repo(session=Depends(get_session)):
    return BarcodeMappingRepository(session)
