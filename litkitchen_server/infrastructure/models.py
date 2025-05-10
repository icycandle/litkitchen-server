from datetime import datetime
from sqlmodel import SQLModel, Field
from litkitchen_server.domain.models import (
    MainDishText,
    SideDishMedia,
    DrinkStyle,
    TextVariant,
    PrintJob,
    PrintJobStatus,
    BarcodeMapping,
)


class MainDishTextOrm(SQLModel, table=True):
    __tablename__ = "maindishtexts"
    id: int = Field(default=None, primary_key=True)
    author_name: str
    work_title: str
    main_dish: str
    publisher: str
    genre: str
    description: str = ""

    def to_domain(self) -> MainDishText:
        return MainDishText(
            id=self.id,
            author_name=self.author_name,
            work_title=self.work_title,
            main_dish=self.main_dish,
            publisher=self.publisher,
            genre=self.genre,
            description=self.description,
        )


class SideDishMediaOrm(SQLModel, table=True):
    __tablename__ = "sidedishmedias"
    id: int = Field(default=None, primary_key=True)
    media_type: str
    side_dish: str

    def to_domain(self) -> SideDishMedia:
        return SideDishMedia(
            id=self.id,
            media_type=self.media_type,
            side_dish=self.side_dish,
        )


class DrinkStyleOrm(SQLModel, table=True):
    __tablename__ = "drinkstyles"
    id: int = Field(default=None, primary_key=True)
    style: str
    drink: str

    def to_domain(self) -> DrinkStyle:
        return DrinkStyle(
            id=self.id,
            style=self.style,
            drink=self.drink,
        )


class TextVariantOrm(SQLModel, table=True):
    __tablename__ = "textvariants"
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

    def to_domain(self) -> TextVariant:
        return TextVariant(
            id=self.id,
            main_dish_text_id=self.main_dish_text_id,
            side_dish_media_id=self.side_dish_media_id,
            drink_style_id=self.drink_style_id,
            content=self.content,
            variant_index=self.variant_index,
            length=self.length,
            approved=self.approved,
            created_at=self.created_at,
            print_count=self.print_count,
        )


class PrintJobOrm(SQLModel, table=True):
    __tablename__ = "printjobs"
    id: int = Field(default=None, primary_key=True)
    text_variant_id: int
    status: str = "queued"
    created_at: datetime = Field(default_factory=datetime.now)
    printed_at: datetime | None = None

    def to_domain(self) -> PrintJob:
        return PrintJob(
            id=self.id,
            text_variant_id=self.text_variant_id,
            status=PrintJobStatus(self.status),
            created_at=self.created_at,
            printed_at=self.printed_at,
        )


class BarcodeMappingOrm(SQLModel, table=True):
    __tablename__ = "barcodemappings"
    id: int = Field(default=None, primary_key=True)
    barcode: str
    main_dish_text_id: int
    side_dish_media_id: int
    drink_style_id: int
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.now)

    def to_domain(self) -> BarcodeMapping:
        return BarcodeMapping(
            id=self.id,
            barcode=self.barcode,
            main_dish_text_id=self.main_dish_text_id,
            side_dish_media_id=self.side_dish_media_id,
            drink_style_id=self.drink_style_id,
            description=self.description,
            created_at=self.created_at,
        )
