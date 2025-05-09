from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PrintJobStatus(str, Enum):
    queued = "queued"
    printing = "printing"
    done = "done"
    failed = "failed"


class MainDishTextSchema(BaseModel):
    id: int
    author_name: str
    work_title: str
    main_dish: str
    publisher: str
    genre: str
    description: Optional[str] = ""


class SideDishMediaSchema(BaseModel):
    id: int
    media_type: str
    side_dish: str


class DrinkStyleSchema(BaseModel):
    id: int
    style: str
    drink: str


class TextVariantSchema(BaseModel):
    id: int
    main_dish_text_id: int
    side_dish_media_id: int
    drink_style_id: int
    content: str
    variant_index: int = 0
    length: int = 0
    approved: bool = False
    created_at: datetime
    print_count: int = 0


class PrintJobSchema(BaseModel):
    id: int
    text_variant_id: int
    status: PrintJobStatus
    created_at: datetime
    printed_at: Optional[datetime] = None


class BarcodeMappingSchema(BaseModel):
    id: int
    barcode: str
    drink_style_id: int
    created_at: datetime
