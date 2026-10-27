"""Étape 1.4 : connexion OK + les 7 modèles compilent leur DDL PostgreSQL."""
from sqlalchemy import text
from sqlalchemy.schema import CreateTable

from app import models  # noqa: F401
from app.database import Base, engine

with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar()
    print("Connexion OK :", version.split(" on ")[0])

    for table in Base.metadata.sorted_tables:
        CreateTable(table).compile(dialect=engine.dialect)
        print(f"  DDL valide : {table.name:<14} ({len(table.columns)} colonnes)")

print(f"\n7 tables attendues -> {len(Base.metadata.tables)} déclarées.")
