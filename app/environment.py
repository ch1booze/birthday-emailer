import os

from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///./database.sqlite")
