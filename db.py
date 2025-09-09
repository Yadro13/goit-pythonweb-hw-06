from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# Ініціалізація SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# Хелпер для сесій
from contextlib import contextmanager

@contextmanager
def session_scope():
    """Контекстний менеджер для безпечної роботи з сесією."""
    # Використовувати тільки timezone-aware дати в бізнес-логіці
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
