# Application settings stub
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

PRINTER_POLL_INTERVAL = 5  # seconds
PRINTJOB_RETRY_LIMIT = 3
PRINTJOB_RETRY_INTERVAL = 10  # seconds
STATE_RESET_TIMEOUT = 60  # seconds

# Sentry config
SENTRY_DSN = os.environ.get(
    "SENTRY_DSN",
    "https://feb53cf10f1d0aba11f80c947de05d9b@o4509343248220161.ingest.us.sentry.io/4509343249465344",
)
SENTRY_SEND_DEFAULT_PII = True
