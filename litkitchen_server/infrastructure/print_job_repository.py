from litkitchen_server.infrastructure.models import PrintJobOrm
from litkitchen_server.domain.models import PrintJob
from sqlmodel import Session, select


class PrintJobRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[PrintJob]:
        orm_list = self.session.exec(select(PrintJobOrm)).all()
        return [orm.to_domain() for orm in orm_list]

    def get(self, item_id: int) -> PrintJob | None:
        orm = self.session.get(PrintJobOrm, item_id)
        return orm.to_domain() if orm else None

    def create(self, item: PrintJob) -> PrintJob:
        orm = PrintJobOrm(
            text_variant_id=item.text_variant_id,
            status=item.status.value,
            created_at=item.created_at,
            printed_at=item.printed_at,
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm.to_domain()

    def update(self, item_id: int, item: PrintJob) -> bool:
        db_item = self.session.get(PrintJobOrm, item_id)
        if not db_item:
            return False
        db_item.text_variant_id = item.text_variant_id
        db_item.status = item.status.value
        db_item.created_at = item.created_at
        db_item.printed_at = item.printed_at
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return True

    def delete(self, item_id: int) -> bool:
        db_item = self.session.get(PrintJobOrm, item_id)
        if not db_item:
            return False
        self.session.delete(db_item)
        self.session.commit()
        return True
