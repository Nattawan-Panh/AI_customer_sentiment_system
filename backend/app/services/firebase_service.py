import os
import json
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv


load_dotenv()

_app = None


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def init_firebase():
    global _app

    if _app:
        return _app

    database_url = os.getenv("FIREBASE_DATABASE_URL")
    if not database_url:
        raise RuntimeError("FIREBASE_DATABASE_URL is missing")

    service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    service_account_path = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT",
        "serviceAccountKey.json"
    )

    try:
        if service_account_json:
            service_account_info = json.loads(service_account_json)

            if "private_key" in service_account_info:
                service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")

            cred = credentials.Certificate(service_account_info)
        else:
            if not os.path.exists(service_account_path):
                raise FileNotFoundError(
                    f"Firebase service account file not found: {service_account_path}"
                )

            cred = credentials.Certificate(service_account_path)

        _app = firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": database_url
            }
        )

        return _app

    except json.JSONDecodeError:
        raise RuntimeError(
            "FIREBASE_SERVICE_ACCOUNT_JSON is not valid JSON"
        )

    except Exception as e:
        raise RuntimeError(
            f"Firebase initialization failed: {str(e)}"
        )


def validate_path(path):
    path = str(path or "").strip()
    if not path:
        raise ValueError("Firebase database path is required")
    return path


def db_ref(path):
    init_firebase()
    return db.reference(validate_path(path))


def db_get(path):
    return db_ref(path).get()


def db_push(path, data):
    if not isinstance(data, dict):
        raise ValueError("Firebase push data must be a dictionary")
    return db_ref(path).push(data)


def db_update(path, data):
    if not isinstance(data, dict):
        raise ValueError("Firebase update data must be a dictionary")
    return db_ref(path).update(data)


def db_set(path, data):
    return db_ref(path).set(data)