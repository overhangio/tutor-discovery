from .base import *

LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": "/openedx/data/logs/discovery.log",
    "formatter": "standard",
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
