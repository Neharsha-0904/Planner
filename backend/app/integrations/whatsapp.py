"""
WhatsApp Cloud API integration — send reminders via WhatsApp.

FREE: 1000 business-initiated conversations/month.

Setup:
1. Go to https://developers.facebook.com/apps → Create App → WhatsApp use case
2. Get your Phone Number ID + Access Token from API Setup page
3. Add your WhatsApp number as a test recipient
4. Set WA_PHONE_NUMBER_ID and WA_ACCESS_TOKEN in .env
"""
import logging
import httpx

from app.config import settings

logger = logging.getLogger(__name__)

WA_API_URL = "https://graph.facebook.com/v21.0"


def send_whatsapp_message(to_phone: str, message: str) -> bool:
    """
    Send a WhatsApp text message.

    Args:
        to_phone: recipient phone with country code, no + (e.g. "919876543210")
        message: text body to send
    """
    phone_id = getattr(settings, "WA_PHONE_NUMBER_ID", "")
    token = getattr(settings, "WA_ACCESS_TOKEN", "")

    if not phone_id or not token:
        logger.info(
            "\n📱 WHATSAPP (console mode — not configured)\n"
            f"   To: {to_phone}\n"
            f"   Message: {message[:200]}\n"
        )
        return True  # Don't fail if not configured

    try:
        response = httpx.post(
            f"{WA_API_URL}/{phone_id}/messages",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_phone,
                "type": "text",
                "text": {"body": message},
            },
            timeout=10,
        )

        if response.status_code == 200:
            logger.info("WhatsApp sent to %s", to_phone)
            return True
        else:
            logger.error("WhatsApp API error %d: %s", response.status_code, response.text[:200])
            return False
    except Exception as e:
        logger.error("WhatsApp send failed: %s", e)
        return False


def send_whatsapp_template(to_phone: str, template_name: str = "hello_world") -> bool:
    """Send a pre-approved template message (for first contact / outside 24hr window)."""
    phone_id = getattr(settings, "WA_PHONE_NUMBER_ID", "")
    token = getattr(settings, "WA_ACCESS_TOKEN", "")

    if not phone_id or not token:
        logger.info("WhatsApp not configured — skipping template send")
        return True

    try:
        response = httpx.post(
            f"{WA_API_URL}/{phone_id}/messages",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "messaging_product": "whatsapp",
                "to": to_phone,
                "type": "template",
                "template": {"name": template_name, "language": {"code": "en_US"}},
            },
            timeout=10,
        )
        return response.status_code == 200
    except Exception as e:
        logger.error("WhatsApp template send failed: %s", e)
        return False
