import time

from fastapi import APIRouter, HTTPException

from litkitchen_server.infrastructure import printer
from fastapi import Depends
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

router = APIRouter()


# --- PrintJob CRUD ---
@router.get("/print-jobs", response_model=list[PrintJobSchema])
def list_print_jobs(repo: PrintJobRepository = Depends(get_print_job_repo)):
    return [PrintJobSchema.from_domain(job) for job in repo.get_all()]


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
    # 轉換 created_at/printed_at 為 datetime
    created_at = item.created_at
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    printed_at = item.printed_at
    if printed_at and isinstance(printed_at, str):
        printed_at = datetime.fromisoformat(printed_at)
    domain_item = PrintJob(
        id=None,
        text_variant_id=item.text_variant_id,
        status=PrintJobStatus(item.status),
        created_at=created_at,
        printed_at=printed_at,
    )
    created = printjob_repo.create(domain_item)
    return PrintJobSchema.from_domain(created)


@router.get("/print-jobs/{job_id}", response_model=PrintJobSchema)
def get_print_job(job_id: int, repo: PrintJobRepository = Depends(get_print_job_repo)):
    item = repo.get(job_id)
    if item:
        return PrintJobSchema.from_domain(item)
    raise HTTPException(status_code=404, detail="PrintJob not found")


@router.put("/print-jobs/{job_id}", response_model=PrintJobSchema)
def update_print_job(
    job_id: int,
    item: PrintJobSchema,
    repo: PrintJobRepository = Depends(get_print_job_repo),
):
    # 確保 created_at/printed_at 是 datetime
    created_at = item.created_at
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    printed_at = item.printed_at
    if printed_at and isinstance(printed_at, str):
        printed_at = datetime.fromisoformat(printed_at)
    domain_item = PrintJob(
        id=item.id,
        text_variant_id=item.text_variant_id,
        status=PrintJobStatus(item.status),
        created_at=created_at,
        printed_at=printed_at,
    )
    updated = repo.update(job_id, domain_item)
    if updated:
        return item
    raise HTTPException(status_code=404, detail="PrintJob not found")


@router.delete("/print-jobs/{job_id}")
def delete_print_job(
    job_id: int, repo: PrintJobRepository = Depends(get_print_job_repo)
):
    deleted = repo.delete(job_id)
    if deleted:
        return {"ok": True}
    raise HTTPException(status_code=404, detail="PrintJob not found")


@router.get("/printer-status")
def get_printer_status():
    return {"status": printer.get_status()}


SYSTEM_STATE = {"state": "idle", "last_reset": time.time()}


@router.get("/system-state")
def get_system_state():
    return SYSTEM_STATE


@router.post("/system-state/reset")
def reset_system_state():
    SYSTEM_STATE["state"] = "idle"
    SYSTEM_STATE["last_reset"] = time.time()
    return {"ok": True, "state": SYSTEM_STATE["state"]}
