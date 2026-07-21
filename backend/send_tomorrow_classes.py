"""Send tomorrow's class schedule via email + WhatsApp."""
import sys
from datetime import date, timedelta, time

sys.path.insert(0, ".")

from app.database import SessionLocal
from app.models.user import User
from app.models.class_slot import ClassSlot
from app.services.email_service import get_email_service
from app.integrations.whatsapp import send_whatsapp_message
from app.integrations.telegram import send_telegram
from app.config import settings

db = SessionLocal()
user = db.query(User).first()

# Tomorrow's day of week (0=Mon)
tomorrow = date.today() + timedelta(days=1)
dow = tomorrow.weekday()
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Get classes
slots = (
    db.query(ClassSlot)
    .filter(ClassSlot.user_id == user.id, ClassSlot.day_of_week == dow, ClassSlot.active == True)
    .order_by(ClassSlot.start_time)
    .all()
)

if not slots:
    print(f"No classes tomorrow ({day_names[dow]})")
    db.close()
    exit()

# Build message
lines = [
    f"TOMORROW'S CLASSES — {day_names[dow]}, {tomorrow.strftime('%B %d')}",
    f"{len(slots)} class(es) scheduled:",
    "",
]

for s in slots:
    lines.append(f"  {s.start_time.strftime('%H:%M')}–{s.end_time.strftime('%H:%M')}  {s.name}")
    lines.append(f"      Room: {s.location}")
    lines.append("")

body = "\n".join(lines)
subject = f"[Planner] Tomorrow's Classes — {day_names[dow]}, {tomorrow.strftime('%b %d')}"

print(body)
print("---")

# Send email
email = get_email_service()
email_ok = email.send(to=settings.SMTP_USER, subject=subject, body=body)
print(f"Email: {'SENT' if email_ok else 'FAILED'}")

# Send Telegram
tg_body = "\n".join([
    f"<b>{subject}</b>",
    "",
] + [
    f"<b>{s.start_time.strftime('%H:%M')}–{s.end_time.strftime('%H:%M')}</b>  {s.name}\n    {s.location}"
    for s in slots
])
tg_ok = send_telegram(tg_body)
print(f"Telegram: {'SENT' if tg_ok else 'FAILED'}")

# Send WhatsApp
if settings.WA_MY_PHONE:
    wa_ok = send_whatsapp_message(settings.WA_MY_PHONE, f"*{subject}*\n\n{body}")
    print(f"WhatsApp: {'SENT' if wa_ok else 'FAILED'}")

db.close()
