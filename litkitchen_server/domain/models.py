from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class PrintJobStatus(str, Enum):
    queued = "queued"  # 等待列印
    ready = "ready"  # 印表機就緒
    printing = "printing"  # 列印中
    done = "done"  # 完成
    failed = "failed"  # 列印失敗
    error = "error"  # 裝置錯誤
    out_of_paper = "out_of_paper"  # 缺紙

    _description_map = {
        "queued": "等待列印",
        "ready": "印表機就緒",
        "printing": "列印中",
        "done": "列印完成",
        "failed": "列印失敗",
        "error": "裝置錯誤，請檢查印表機",
        "out_of_paper": "缺紙，請補充紙捲",
    }

    def description(self) -> str:
        return self._description_map.get(self.value, "未知狀態")


class MainDishText(BaseModel):
    id: int | None = None
    author_name: str
    work_title: str
    main_dish: str
    publisher: str
    genre: str
    description: str = ""


class SideDishMedia(BaseModel):
    id: int | None = None
    media_type: str
    side_dish: str


class DrinkStyle(BaseModel):
    id: int | None = None
    style: str
    drink: str


class TextVariant(BaseModel):
    id: int | None = None
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
    id: int | None = None
    text_variant_id: int
    status: PrintJobStatus = PrintJobStatus.queued
    created_at: datetime = datetime.now()


class BarcodeMapping(BaseModel):
    id: int | None = None
    barcode: str
    main_dish_text_id: int
    side_dish_media_id: int
    drink_style_id: int
    description: str = ""
    created_at: datetime = datetime.now()
