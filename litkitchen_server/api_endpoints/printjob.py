import time
from typing import List

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

router = APIRouter()


# --- PrintJob CRUD ---
@router.get("/printjob", response_model=List[PrintJobSchema])
def get_printjobs(repo: PrintJobRepository = Depends(get_print_job_repo)):
    return repo.get_all()


@router.post("/printjob", response_model=PrintJobSchema)
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
    created = printjob_repo.create(item)
    return created


@router.get("/printjob/{item_id}", response_model=PrintJobSchema)
def get_print_job(item_id: int, repo: PrintJobRepository = Depends(get_print_job_repo)):
    item = repo.get(item_id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="PrintJob not found")


@router.put("/printjob/{item_id}", response_model=PrintJobSchema)
def update_print_job(
    item_id: int,
    item: PrintJobSchema,
    repo: PrintJobRepository = Depends(get_print_job_repo),
):
    updated = repo.update(item_id, item)
    if updated:
        return item
    raise HTTPException(status_code=404, detail="PrintJob not found")


@router.delete("/printjob/{item_id}")
def delete_print_job(
    item_id: int, repo: PrintJobRepository = Depends(get_print_job_repo)
):
    deleted = repo.delete(item_id)
    if deleted:
        return {"ok": True}
    raise HTTPException(status_code=404, detail="PrintJob not found")


# --- Printer Status ---
@router.get("/printer/status")
def get_printer_status():
    return {"status": printer.get_status()}


# --- System State (reset, etc) ---
SYSTEM_STATE = {"state": "idle", "last_reset": time.time()}


@router.get("/state")
def get_system_state():
    return SYSTEM_STATE


@router.post("/state/reset")
def reset_system_state():
    SYSTEM_STATE["state"] = "idle"
    SYSTEM_STATE["last_reset"] = time.time()
    return {"ok": True, "state": SYSTEM_STATE["state"]}
