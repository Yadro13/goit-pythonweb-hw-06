import os
from dotenv import load_dotenv

load_dotenv()

# Використовується SQLAlchemy URL
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres",
)
