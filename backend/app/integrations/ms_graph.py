"""
Microsoft Graph API integration — reads emails from Office 365 (Amrita university mail).

Setup:
1. Go to https://portal.azure.com → Azure Active Directory → App registrations → New
   (Or use https://entra.microsoft.com if your uni uses Entra)
2. Name: "Planner Email Reader"
3. Supported account types: "Accounts in any organizational directory" (for university tenants)
4. Redirect URI: http://localhost (for device code flow)
5. After creation, note the Application (client) ID
6. Go to API permissions → Add → Microsoft Graph → Delegated → Mail.Read
7. Set MS_GRAPH_CLIENT_ID in .env

First run: the app will print a URL + code. Open the URL, enter the code,
sign in with your Amrita account. Token is cached locally after that.
"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

TOKEN_CACHE_PATH = Path(__file__).parent.parent.parent / ".ms_token_cache.json"

# Trusted sender domains — only emails from these domains appear in briefs
TRUSTED_DOMAINS = [
    "amrita.edu",
    "cb.amrita.edu",
    "am.amrita.edu",
    "microsoft.com",
    "google.com",
    "github.com",
    "coursera.org",
    "linkedin.com",
    "aws.amazon.com",
]


def _get_msal_app():
    """Get MSAL public client app for device code flow."""
    try:
        import msal
    except ImportError:
        logger.warning("msal not installed — run: pip install msal")
        return None

    client_id = getattr(settings, "MS_GRAPH_CLIENT_ID", "")
    if not client_id:
        return None

    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE_PATH.exists():
        cache.deserialize(TOKEN_CACHE_PATH.read_text())

    app = msal.PublicClientApplication(
        client_id,
        authority="https://login.microsoftonline.com/common",
        token_cache=cache,
    )
    return app


def _get_token():
    """Get access token (from cache or via device code flow)."""
    app = _get_msal_app()
    if not app:
        return None

    scopes = ["Mail.Read"]
    accounts = app.get_accounts()

    if accounts:
        result = app.acquire_token_silent(scopes, account=accounts[0])
        if result and "access_token" in result:
            _save_cache(app)
            return result["access_token"]

    # Need interactive login (device code flow)
    flow = app.initiate_device_flow(scopes=scopes)
    if "user_code" not in flow:
        logger.error("Failed to create device flow: %s", flow)
        return None

    logger.info(
        "\n"
        "=" * 60 + "\n"
        "🔐 MICROSOFT LOGIN REQUIRED\n"
        f"   Go to: {flow['verification_uri']}\n"
        f"   Enter code: {flow['user_code']}\n"
        "   Sign in with your Amrita email\n"
        "=" * 60
    )
    print(f"\n🔐 Go to {flow['verification_uri']} and enter code: {flow['user_code']}\n")

    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        _save_cache(app)
        return result["access_token"]

    logger.error("Token acquisition failed: %s", result.get("error_description"))
    return None


def _save_cache(app):
    """Save token cache to disk."""
    if app.token_cache.has_state_changed:
        TOKEN_CACHE_PATH.write_text(app.token_cache.serialize())


def _is_trusted_sender(email_address: str) -> bool:
    """Check if sender is from a trusted domain."""
    if not email_address:
        return False
    domain = email_address.split("@")[-1].lower()
    return any(domain.endswith(d) for d in TRUSTED_DOMAINS)


def fetch_important_emails(hours: int = 24, max_count: int = 10) -> list[dict]:
    """
    Fetch important unread emails from the last N hours.

    Returns list of dicts: {from, subject, received, preview}
    Only includes emails from trusted domains.
    """
    token = _get_token()
    if not token:
        logger.debug("No MS Graph token — skipping email fetch")
        return []

    try:
        import httpx
    except ImportError:
        logger.warning("httpx not available for Graph API calls")
        return []

    since = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")

    response = httpx.get(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "$filter": f"isRead eq false and receivedDateTime ge {since}",
            "$select": "from,subject,receivedDateTime,bodyPreview",
            "$top": str(max_count * 3),  # Fetch extra, filter locally
            "$orderby": "receivedDateTime desc",
        },
    )

    if response.status_code != 200:
        logger.error("Graph API error %d: %s", response.status_code, response.text[:200])
        return []

    messages = response.json().get("value", [])
    important = []

    for msg in messages:
        sender_email = msg.get("from", {}).get("emailAddress", {}).get("address", "")
        if _is_trusted_sender(sender_email):
            important.append({
                "from": msg["from"]["emailAddress"].get("name", sender_email),
                "from_email": sender_email,
                "subject": msg.get("subject", "(no subject)"),
                "received": msg.get("receivedDateTime", ""),
                "preview": msg.get("bodyPreview", "")[:150],
            })

        if len(important) >= max_count:
            break

    logger.info("Fetched %d important emails from %d total unread", len(important), len(messages))
    return important
