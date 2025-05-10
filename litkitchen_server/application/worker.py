import time
import threading
from litkitchen_server.domain.models import PrintJobStatus
from litkitchen_server.application.state import SystemState
from litkitchen_server.infrastructure.printer import printer
from litkitchen_server.infrastructure.repository_sqlite import SqliteRepository


def printjob_worker():
    repo = SqliteRepository()
    while True:
        jobs = repo.get_printjobs()
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


threading.Thread(target=printjob_worker, daemon=True).start()
