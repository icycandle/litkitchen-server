from enum import Enum
from typing import Optional

from pydantic import BaseModel
from litkitchen_server.domain.models import (
    MainDishText,
    SideDishMedia,
    DrinkStyle,
    PrintJob,
    BarcodeMapping,
    TextVariant,
)
from pydantic import field_serializer


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

    @classmethod
    def from_domain(cls, domain: MainDishText) -> "MainDishTextSchema":
        return cls(
            id=domain.id,
            author_name=domain.author_name,
            work_title=domain.work_title,
            main_dish=domain.main_dish,
            publisher=domain.publisher,
            genre=domain.genre,
            description=domain.description,
        )


class SideDishMediaSchema(BaseModel):
    id: int
    media_type: str
    side_dish: str

    @classmethod
    def from_domain(cls, domain: SideDishMedia) -> "SideDishMediaSchema":
        return cls(
            id=domain.id,
            media_type=domain.media_type,
            side_dish=domain.side_dish,
        )


class DrinkStyleSchema(BaseModel):
    id: int
    style: str
    drink: str

    @classmethod
    def from_domain(cls, domain: DrinkStyle) -> "DrinkStyleSchema":
        return cls(
            id=domain.id,
            style=domain.style,
            drink=domain.drink,
        )


class TextVariantSchema(BaseModel):
    id: int
    main_dish_text_id: int
    side_dish_media_id: int
    drink_style_id: int
    content: str
    variant_index: int = 0
    length: int = 0
    approved: bool = False
    created_at: str = ""
    print_count: int = 0

    @classmethod
    def from_domain(cls, domain: TextVariant) -> "TextVariantSchema":
        return cls(
            id=domain.id,
            main_dish_text_id=domain.main_dish_text_id,
            side_dish_media_id=domain.side_dish_media_id,
            drink_style_id=domain.drink_style_id,
            content=domain.content,
            variant_index=domain.variant_index,
            length=domain.length,
            approved=domain.approved,
            created_at=domain.created_at.isoformat()
            if hasattr(domain.created_at, "isoformat")
            else str(domain.created_at),
            print_count=domain.print_count,
        )


class PrintJobSchema(BaseModel):
    id: int | None = None
    text_variant_id: int
    status: str
    created_at: str = ""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "text_variant_id": 1,
                    "status": "queued",
                    "created_at": "2025-01-01T00:00:00",
                }
            ]
        }
    }

    def __init__(self, **data):
        # status: Enum or str
        status = data.get("status")
        if status and not isinstance(status, str):
            data["status"] = status.value
        # created_at: datetime or str
        for field in ("created_at",):
            v = data.get(field)
            if v and not isinstance(v, str):
                data[field] = v.isoformat()
        super().__init__(**data)

    @field_serializer("created_at", mode="plain")
    def serialize_dt(self, value):
        if value is None:
            return None
        return value.isoformat() if hasattr(value, "isoformat") else str(value)

    @classmethod
    def from_domain(cls, domain: PrintJob) -> "PrintJobSchema":
        return cls(
            id=domain.id,
            text_variant_id=domain.text_variant_id,
            status=domain.status,
            created_at=domain.created_at.isoformat() if domain.created_at else "",
        )


class BarcodeMappingSchema(BaseModel):
    id: int
    barcode: str
    main_dish_text_id: int | None = None
    side_dish_media_id: int | None = None
    drink_style_id: int | None = None
    description: Optional[str] = ""
    created_at: str = ""

    @classmethod
    def from_domain(cls, domain: BarcodeMapping) -> "BarcodeMappingSchema":
        return cls(
            id=domain.id,
            barcode=domain.barcode,
            main_dish_text_id=domain.main_dish_text_id,
            side_dish_media_id=domain.side_dish_media_id,
            drink_style_id=domain.drink_style_id,
            description=domain.description,
            created_at=domain.created_at.isoformat()
            if hasattr(domain.created_at, "isoformat")
            else str(domain.created_at),
        )


class BarcodeMappingCreateSchema(BaseModel):
    barcode: str
    main_dish_text_id: int | None = None
    side_dish_media_id: int | None = None
    drink_style_id: int | None = None
    description: Optional[str] = ""
