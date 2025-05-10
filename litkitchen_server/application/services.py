from litkitchen_server.domain.repository import (
    TextVariantRepository,
    PrintJobRepository,
    MainDishTextRepository,
)
from litkitchen_server.domain.models import (
    TextVariant,
    PrintJob,
    MainDishText,
)


class TextVariantService:
    def __init__(self, repo: TextVariantRepository):
        self.repo = repo

    def create_textvariant(self, item: TextVariant) -> TextVariant:
        return self.repo.create_textvariant(item)

    def get_textvariant(self, item_id: int) -> TextVariant | None:
        return self.repo.get_textvariant(item_id)


class PrintJobService:
    def __init__(self, repo: PrintJobRepository):
        self.repo = repo

    def create_printjob(self, item: PrintJob) -> PrintJob:
        return self.repo.create_printjob(item)

    def get_printjob(self, item_id: int) -> PrintJob | None:
        return self.repo.get_printjob(item_id)


class MainDishTextService:
    def __init__(self, repo: MainDishTextRepository):
        self.repo = repo

    def create_maindishtext(self, item: MainDishText) -> MainDishText:
        return self.repo.create_maindishtext(item)

    def get_maindishtext(self, item_id: int) -> MainDishText | None:
        return self.repo.get_maindishtext(item_id)
