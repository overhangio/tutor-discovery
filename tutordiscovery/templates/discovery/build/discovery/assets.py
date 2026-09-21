from .base import *

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# Get rid of the "local" handler
LOGGING["handlers"].pop("local", None)
for logger in LOGGING["loggers"].values():
    if "local" in logger.get("handlers", []):
        logger["handlers"].remove("local")
