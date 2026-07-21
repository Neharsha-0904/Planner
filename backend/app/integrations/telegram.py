"""
Telegram Bot notification integration.
Free, permanent, no token expiry.
"""
import logging
import httpx

logger = logging.getLogger(__name__)


def send_telegram(message: str, parse_mode: str = "HTML") -> bool:
    """Send a message via Telegram bot."""
    from app.config import settings

    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        logger.debug("Telegram not configured — skipping")
        return False

    try:
        r = httpx.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message, "parse_mode": parse_mode},
            timeout=10,
        )
        if r.status_code == 200:
            logger.info("Telegram sent: %s", message[:60])
            return True
        logger.error("Telegram error %d: %s", r.status_code, r.text[:200])
        return False
    except Exception as e:
        logger.error("Telegram send failed: %s", e)
        return False
