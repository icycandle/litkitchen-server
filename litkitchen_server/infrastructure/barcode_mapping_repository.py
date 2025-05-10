from litkitchen_server.infrastructure.models import BarcodeMappingOrm
from litkitchen_server.domain.models import BarcodeMapping
from sqlmodel import Session, select


class BarcodeMappingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[BarcodeMapping]:
        orm_list = self.session.exec(select(BarcodeMappingOrm)).all()
        return [orm.to_domain() for orm in orm_list]

    def get(self, item_id: int) -> BarcodeMapping | None:
        orm = self.session.get(BarcodeMappingOrm, item_id)
        return orm.to_domain() if orm else None

    def create(self, item: BarcodeMapping) -> BarcodeMapping:
        orm = BarcodeMappingOrm(
            barcode=item.barcode,
            main_dish_text_id=item.main_dish_text_id,
            side_dish_media_id=item.side_dish_media_id,
            drink_style_id=item.drink_style_id,
            description=item.description,
            created_at=item.created_at,
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm.to_domain()

    def update(self, item_id: int, item: BarcodeMapping) -> bool:
        db_item = self.session.get(BarcodeMappingOrm, item_id)
        if not db_item:
            return False
        db_item.barcode = item.barcode
        db_item.main_dish_text_id = item.main_dish_text_id
        db_item.side_dish_media_id = item.side_dish_media_id
        db_item.drink_style_id = item.drink_style_id
        db_item.description = item.description
        db_item.created_at = item.created_at
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return True

    def delete(self, item_id: int) -> bool:
        db_item = self.session.get(BarcodeMappingOrm, item_id)
        if not db_item:
            return False
        self.session.delete(db_item)
        self.session.commit()
        return True
