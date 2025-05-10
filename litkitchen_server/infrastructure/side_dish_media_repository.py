from litkitchen_server.infrastructure.models import SideDishMediaOrm
from litkitchen_server.domain.models import SideDishMedia
from sqlmodel import Session, select


class SideDishMediaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[SideDishMedia]:
        orm_list = self.session.exec(select(SideDishMediaOrm)).all()
        return [orm.to_domain() for orm in orm_list]

    def get(self, item_id: int) -> SideDishMedia | None:
        orm = self.session.get(SideDishMediaOrm, item_id)
        return orm.to_domain() if orm else None

    def create(self, item: SideDishMedia) -> SideDishMedia:
        orm = SideDishMediaOrm(
            media_type=item.media_type,
            side_dish=item.side_dish,
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm.to_domain()

    def update(self, item_id: int, item: SideDishMedia) -> bool:
        db_item = self.session.get(SideDishMediaOrm, item_id)
        if not db_item:
            return False
        db_item.media_type = item.media_type
        db_item.side_dish = item.side_dish
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return True

    def delete(self, item_id: int) -> bool:
        db_item = self.session.get(SideDishMediaOrm, item_id)
        if not db_item:
            return False
        self.session.delete(db_item)
        self.session.commit()
        return True
