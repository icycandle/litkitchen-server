from fastapi import APIRouter
from fastapi import Depends
from litkitchen_server.infrastructure.printer import get_printer_worker
from litkitchen_server.api.schemas import PrintJobSchema
from litkitchen_server.infrastructure.print_job_repository import PrintJobRepository
from litkitchen_server.infrastructure.text_variant_repository import (
    TextVariantRepository,
)
from litkitchen_server.infrastructure.repository_provider import (
    get_print_job_repo,
    get_text_variant_repo,
)
from datetime import datetime
from litkitchen_server.domain.models import PrintJob, PrintJobStatus
from fastapi import HTTPException

router = APIRouter()


@router.post("/print-jobs", response_model=PrintJobSchema)
def create_print_job(
    item: PrintJobSchema,
    printjob_repo: PrintJobRepository = Depends(get_print_job_repo),
    textvariant_repo: TextVariantRepository = Depends(get_text_variant_repo),
):
    tv = textvariant_repo.get(item.text_variant_id)
    if not tv:
        raise HTTPException(status_code=400, detail="TextVariant not found")

    tv.print_count += 1
    textvariant_repo.update(tv.id, tv)

    created_at = item.created_at
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)

    domain_item = PrintJob(
        id=None,
        text_variant_id=item.text_variant_id,
        status=PrintJobStatus(item.status),
        created_at=created_at,
    )
    created = printjob_repo.create(domain_item)
    return PrintJobSchema.from_domain(created)


@router.get("/printer-status")
def get_printer_status(printer_worker=Depends(get_printer_worker)):
    return {
        "status": printer_worker.get_status().value,
        "description": printer_worker.get_status().description(),
    }


@router.post("/printer-direct-print")
def direct_print(text: str, printer_worker=Depends(get_printer_worker)):
    ok = printer_worker.submit_print(text)
    return {"ok": ok, "status": printer_worker.get_status().value}
