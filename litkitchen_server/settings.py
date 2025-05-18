# Application settings stub
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

PRINTER_POLL_INTERVAL = 5  # seconds
PRINTJOB_RETRY_LIMIT = 3
PRINTJOB_RETRY_INTERVAL = 10  # seconds
STATE_RESET_TIMEOUT = 60  # seconds
