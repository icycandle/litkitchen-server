from litkitchen_server.infrastructure.models import DrinkStyleOrm
from litkitchen_server.domain.models import DrinkStyle
from sqlmodel import Session, select


class DrinkStyleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[DrinkStyle]:
        orm_list = self.session.exec(select(DrinkStyleOrm)).all()
        return [orm.to_domain() for orm in orm_list]

    def get(self, item_id: int) -> DrinkStyle | None:
        orm = self.session.get(DrinkStyleOrm, item_id)
        return orm.to_domain() if orm else None

    def create(self, item: DrinkStyle) -> DrinkStyle:
        orm = DrinkStyleOrm(
            style=item.style,
            drink=item.drink,
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm.to_domain()

    def update(self, item_id: int, item: DrinkStyle) -> bool:
        db_item = self.session.get(DrinkStyleOrm, item_id)
        if not db_item:
            return False
        db_item.style = item.style
        db_item.drink = item.drink
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return True

    def delete(self, item_id: int) -> bool:
        db_item = self.session.get(DrinkStyleOrm, item_id)
        if not db_item:
            return False
        self.session.delete(db_item)
        self.session.commit()
        return True
