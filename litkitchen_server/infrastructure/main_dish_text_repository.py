from litkitchen_server.domain.repository import IMainDishTextRepository
from litkitchen_server.infrastructure.models import MainDishTextOrm
from litkitchen_server.domain.models import MainDishText
from sqlmodel import Session, select


class MainDishTextRepository(IMainDishTextRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[MainDishText]:
        orm_list = self.session.exec(select(MainDishTextOrm)).all()
        return [orm.to_domain() for orm in orm_list]

    def get(self, item_id: int) -> MainDishText | None:
        orm = self.session.get(MainDishTextOrm, item_id)
        return orm.to_domain() if orm else None

    def create(self, item: MainDishText) -> MainDishText:
        orm = MainDishTextOrm(
            author_name=item.author_name,
            work_title=item.work_title,
            main_dish=item.main_dish,
            publisher=item.publisher,
            genre=item.genre,
            description=item.description,
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm.to_domain()

    def update(self, item_id: int, item: MainDishText) -> bool:
        db_item = self.session.get(MainDishTextOrm, item_id)
        if not db_item:
            return False
        db_item.author_name = item.author_name
        db_item.work_title = item.work_title
        db_item.main_dish = item.main_dish
        db_item.publisher = item.publisher
        db_item.genre = item.genre
        db_item.description = item.description
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return True

    def delete(self, item_id: int) -> bool:
        db_item = self.session.get(MainDishTextOrm, item_id)
        if not db_item:
            return False
        self.session.delete(db_item)
        self.session.commit()
        return True
