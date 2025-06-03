from litkitchen_server.domain.repository import ITextVariantRepository
from litkitchen_server.infrastructure.models import TextVariantOrm
from litkitchen_server.domain.models import TextVariant
from sqlmodel import Session, select


class TextVariantRepository(ITextVariantRepository):
    def __init__(self, session: Session):
        self.session = session

    def query(
        self,
        main_dish_text_id: int,
        side_dish_media_id: int,
        drink_style_id: int,
    ) -> list[TextVariant]:
        """
        filter by
        `main_dish_text_id`
        `side_dish_media_id`
        `drink_style_id`
        """
        query = select(TextVariantOrm).where(
            TextVariantOrm.main_dish_text_id == main_dish_text_id,
            TextVariantOrm.side_dish_media_id == side_dish_media_id,
            TextVariantOrm.drink_style_id == drink_style_id,
        )
        orm_list = self.session.exec(query).all()
        return [orm.to_domain() for orm in orm_list]

    def get_all(self) -> list[TextVariant]:
        orm_list = self.session.exec(select(TextVariantOrm)).all()
        return [orm.to_domain() for orm in orm_list]

    def get(self, item_id: int) -> TextVariant | None:
        orm = self.session.get(TextVariantOrm, item_id)
        return orm.to_domain() if orm else None

    def get_textvariant(self, item_id: int) -> TextVariant | None:
        return self.get(item_id)

    def create(self, item: TextVariant) -> TextVariant:
        orm = TextVariantOrm(
            main_dish_text_id=item.main_dish_text_id,
            side_dish_media_id=item.side_dish_media_id,
            drink_style_id=item.drink_style_id,
            content=item.content,
            variant_index=item.variant_index,
            length=item.length,
            approved=item.approved,
            created_at=item.created_at,
            print_count=item.print_count,
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm.to_domain()

    def create_textvariant(self, item: TextVariant) -> TextVariant:
        return self.create(item)

    def update(self, item_id: int, item: TextVariant) -> bool:
        db_item = self.session.get(TextVariantOrm, item_id)
        if not db_item:
            return False
        db_item.main_dish_text_id = item.main_dish_text_id
        db_item.side_dish_media_id = item.side_dish_media_id
        db_item.drink_style_id = item.drink_style_id
        db_item.content = item.content
        db_item.variant_index = item.variant_index
        db_item.length = item.length
        db_item.approved = item.approved
        db_item.created_at = item.created_at
        db_item.print_count = item.print_count
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return True

    def delete(self, item_id: int) -> bool:
        db_item = self.session.get(TextVariantOrm, item_id)
        if not db_item:
            return False
        self.session.delete(db_item)
        self.session.commit()
        return True
