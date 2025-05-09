import time
from typing import List

from fastapi import APIRouter, HTTPException

from litkitchen_server.infrastructure import printer
from litkitchen_server.repository import _db
from litkitchen_server.schemas import PrintJobSchema

router = APIRouter()


# --- PrintJob CRUD ---
@router.get("/printjob", response_model=List[PrintJobSchema])
def list_print_jobs():
    return _db["printjobs"]


@router.post("/printjob", response_model=PrintJobSchema)
def create_print_job(item: PrintJobSchema):
    # print_count +1 on related TextVariant
    for tv in _db["textvariants"]:
        if tv.id == item.text_variant_id:
            tv.print_count += 1
            break
    _db["printjobs"].append(item)
    return item


@router.get("/printjob/{item_id}", response_model=PrintJobSchema)
def get_print_job(item_id: int):
    for item in _db["printjobs"]:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="PrintJob not found")


@router.put("/printjob/{item_id}", response_model=PrintJobSchema)
def update_print_job(item_id: int, item: PrintJobSchema):
    for idx, orig in enumerate(_db["printjobs"]):
        if orig.id == item_id:
            _db["printjobs"][idx] = item
            return item
    raise HTTPException(status_code=404, detail="PrintJob not found")


@router.delete("/printjob/{item_id}")
def delete_print_job(item_id: int):
    for idx, orig in enumerate(_db["printjobs"]):
        if orig.id == item_id:
            del _db["printjobs"][idx]
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
