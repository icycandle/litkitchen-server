from datetime import datetime
from sqlmodel import SQLModel, Field


class MainDishText(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    author_name: str
    work_title: str
    main_dish: str
    publisher: str
    genre: str
    description: str = ""


class SideDishMedia(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    media_type: str
    side_dish: str


class DrinkStyle(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    style: str
    drink: str


class TextVariant(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    main_dish_text_id: int
    side_dish_media_id: int
    drink_style_id: int
    content: str
    variant_index: int = 0
    length: int = 0
    approved: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    print_count: int = 0


class PrintJob(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    text_variant_id: int
    status: str = "queued"
    created_at: datetime = Field(default_factory=datetime.now)
    printed_at: datetime | None = None


class BarcodeMapping(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    barcode: str
    main_dish_text_id: int
    side_dish_media_id: int
    drink_style_id: int
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
