import logging
from datetime import UTC, datetime

from pythonjsonlogger import jsonlogger

from app.config import settings

logger = logging.getLogger()

logHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(module)s %(funcName)s %(message)s"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)
