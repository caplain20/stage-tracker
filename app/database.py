"""Connexion à la base — point d'accès unique à PostgreSQL."""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Classe mère de tous les modèles ORM."""


def get_db():
    """Session de transaction par requête — dépendance FastAPI partagée."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
