from datetime import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session, select

from .database import engine
from .environment import BREVO_API_KEY
from .models import Birthday

scheduler = BackgroundScheduler()


def send_birthday_email(name, email):
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY,
    }
    data = {
        "sender": {
            "name": "Birthday Emailer",
            "email": "victoramomodu@gmail.com",
        },
        "to": [{"email": email, "name": name}],
        "subject": f"Happy Birthday, {name}!",
        "htmlContent": """
        <!DOCTYPE html>
        <html>
        <head>
          <title>Happy Birthday</title>
        </head>
        <body>
          <h1>Happy Birthday!</h1>
          <p>Wishing you a wonderful day filled with joy and surprises.</p>
        </body>
        </html>
        """,
    }

    requests.post(
        url=url,
        headers=headers,
        json=data,
    )


def birthday_cron():
    with Session(engine) as session:
        today = datetime.today().date()
        found_birthdays = session.exec(
            select(Birthday).where(Birthday.birthday == today)
        ).all()
        for birthday in found_birthdays:
            send_birthday_email(birthday.name, birthday.email)


scheduler.add_job(
    birthday_cron,
    trigger="cron",
    hour=8,
    minute=0,
    id="birthday_daily_job",
    replace_existing=True,
)
