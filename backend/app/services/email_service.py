from abc import ABC, abstractmethod
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class EmailService(ABC):
    """Abstract email service interface. Implement for each provider."""

    @abstractmethod
    def send(self, to: str | list[str], subject: str, body: str, html: str | None = None) -> bool:
        """Send an email. Returns True if successful."""
        ...


class ConsoleEmailBackend(EmailService):
    """Logs emails to console. Used in dev when SMTP is not configured."""

    def send(self, to: str | list[str], subject: str, body: str, html: str | None = None) -> bool:
        recipients = to if isinstance(to, list) else [to]
        logger.info(
            "\n"
            "=" * 60 + "\n"
            f"📧 EMAIL TO: {', '.join(recipients)}\n"
            f"   SUBJECT: {subject}\n"
            "─" * 60 + "\n"
            f"{body}\n"
            "=" * 60
        )
        return True


class SmtpEmailBackend(EmailService):
    """Send real emails via SMTP (Gmail App Password recommended)."""

    def __init__(self, host: str, port: int, user: str, password: str, from_name: str = "Planner"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.from_name = from_name

    def send(self, to: str | list[str], subject: str, body: str, html: str | None = None) -> bool:
        recipients = to if isinstance(to, list) else [to]
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = f"{self.from_name} <{self.user}>"
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))
            if html:
                msg.attach(MIMEText(html, "html"))

            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.user, recipients, msg.as_string())

            logger.info("Email sent to %s: %s", ", ".join(recipients), subject)
            return True
        except Exception as e:
            logger.error("SMTP send failed: %s", e)
            return False


def get_email_service() -> EmailService:
    """Factory: returns SMTP backend if configured, else console."""
    from app.config import settings

    if settings.EMAIL_BACKEND == "smtp" and settings.SMTP_USER and settings.SMTP_PASSWORD:
        return SmtpEmailBackend(
            host=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            user=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            from_name=settings.SMTP_FROM_NAME,
        )
    return ConsoleEmailBackend()
