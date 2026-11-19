
import os
import logging

from pymongo import MongoClient
from pymongo.errors import PyMongoError


logger = logging.getLogger(__name__)

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=2000
)

database = client["maintenance_audit"]
audit_collection = database["audit_events"]


def log_event(event_type, model_name, object_id, details=None):
    """
    Записывает событие в журнал аудита MongoDB.
    """

    event = {
        "event_type": event_type,
        "model": model_name,
        "object_id": str(object_id),
        "details": details or {},
    }

    try:
        audit_collection.insert_one(event)
    except PyMongoError:
        logger.exception(
            "Не удалось записать событие в MongoDB."
        )
