"""
Firebase Cloud Messaging (FCM) push notification service.

Setup:
1. Create a Firebase project at https://console.firebase.google.com
2. Download the service account JSON key
3. Set FIREBASE_CREDENTIALS_PATH in .env to the path of the JSON file

For Phase 0: if no Firebase credentials are configured, notifications
are logged to console (same as email).
"""
import json
import logging
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

_firebase_app = None


def _init_firebase():
    """Lazy-initialize Firebase Admin SDK."""
    global _firebase_app
    if _firebase_app is not None:
        return True

    creds_path = getattr(settings, "FIREBASE_CREDENTIALS_PATH", "")
    if not creds_path or not Path(creds_path).exists():
        logger.warning("Firebase credentials not configured — push notifications will be logged only")
        return False

    try:
        import firebase_admin
        from firebase_admin import credentials
        cred = credentials.Certificate(creds_path)
        _firebase_app = firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialized")
        return True
    except Exception as e:
        logger.error("Failed to init Firebase: %s", e)
        return False


def send_push_notification(fcm_token: str, title: str, body: str, data: dict | None = None) -> bool:
    """Send a push notification to a single device.

    Returns True if sent (or logged in dev mode).
    """
    if not fcm_token:
        return False

    if not _init_firebase():
        # Fallback: log to console
        logger.info(
            "\n🔔 PUSH NOTIFICATION (console mode)\n"
            f"   To token: {fcm_token[:20]}...\n"
            f"   Title: {title}\n"
            f"   Body: {body}\n"
            f"   Data: {data}\n"
        )
        return True

    try:
        from firebase_admin import messaging

        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            token=fcm_token,
        )
        response = messaging.send(message)
        logger.info("FCM sent: %s", response)
        return True
    except Exception as e:
        logger.error("FCM send failed: %s", e)
        return False


def send_push_to_user(user, title: str, body: str, data: dict | None = None) -> bool:
    """Convenience: send push to a User model instance."""
    if not user.fcm_token:
        logger.debug("No FCM token for user %s — skipping push", user.name)
        return False
    return send_push_notification(user.fcm_token, title, body, data)
