# Application service layer stub (use case coordination, state management)
import threading
import time

from litkitchen_server.domain import PrintJobStatus
from litkitchen_server.infrastructure import printer
from litkitchen_server.repository import get_printjobs


class SystemState:
    # Simple state machine for demo
    state = "idle"  # idle, param1, param2, param3, printing, done
    last_action_time = time.time()
    lock = threading.Lock()

    @classmethod
    def set_state(cls, new_state):
        with cls.lock:
            cls.state = new_state
            cls.last_action_time = time.time()

    @classmethod
    def get_state(cls):
        with cls.lock:
            return cls.state

    @classmethod
    def check_timeout_and_reset(cls, timeout=60):
        with cls.lock:
            if time.time() - cls.last_action_time > timeout:
                cls.state = "idle"


# Background worker for print jobs (demo)
def printjob_worker():
    while True:
        jobs = get_printjobs()
        for job in jobs:
            if job.status == PrintJobStatus.queued:
                SystemState.set_state("printing")
                job.status = PrintJobStatus.printing
                # TODO: fetch text from TextVariant
                printer.print_text("sample text")
                job.status = PrintJobStatus.done
                SystemState.set_state("done")
        SystemState.check_timeout_and_reset()
        time.sleep(2)


# Start background worker thread (in production, use a proper task queue)
threading.Thread(target=printjob_worker, daemon=True).start()
