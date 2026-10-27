"""Contrats d'entrée/sortie de l'API — validation Pydantic."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    """Données acceptées à la création d'une fiche entreprise (EXG-001)."""

    name: str = Field(min_length=1, max_length=200)
    website: str | None = Field(default=None, max_length=300)
    sector: str | None = Field(default=None, max_length=120)
    notes: str | None = None


class CompanyUpdate(BaseModel):
    """Champs modifiables — tous optionnels (modification partielle)."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    website: str | None = Field(default=None, max_length=300)
    sector: str | None = Field(default=None, max_length=120)
    notes: str | None = None


class CompanyRead(BaseModel):
    """Ce que l'API renvoie — calqué sur la table companies."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    website: str | None
    sector: str | None
    notes: str | None
    created_at: datetime
