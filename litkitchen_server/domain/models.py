from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class PrintJobStatus(str, Enum):
    queued = "queued"
    printing = "printing"
    done = "done"
    failed = "failed"


class MainDishText(BaseModel):
    id: int
    author_name: str
    work_title: str
    main_dish: str
    publisher: str
    genre: str
    description: str = ""


class SideDishMedia(BaseModel):
    id: int
    media_type: str
    side_dish: str


class DrinkStyle(BaseModel):
    id: int
    style: str
    drink: str


class TextVariant(BaseModel):
    id: int
    main_dish_text_id: int
    side_dish_media_id: int
    drink_style_id: int
    content: str
    variant_index: int = 0
    length: int = 0
    approved: bool = False
    created_at: datetime = datetime.now()
    print_count: int = 0


class PrintJob(BaseModel):
    id: int
    text_variant_id: int
    status: PrintJobStatus = PrintJobStatus.queued
    created_at: datetime = datetime.now()
    printed_at: datetime | None = None


class BarcodeMapping(BaseModel):
    id: int
    barcode: str
    main_dish_text_id: int
    side_dish_media_id: int
    drink_style_id: int
    description: str = ""
    created_at: datetime = datetime.now()
