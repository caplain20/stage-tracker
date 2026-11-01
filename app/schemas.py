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

# ------------------------------------------------------------------ M2 : offres et candidatures
from app.models import ApplicationStatus  # noqa: E402 — les 7 statuts, source unique (RG-01)


class OfferCreate(BaseModel):
    """EXG-004 : saisie d'une offre par copier-coller du texte brut."""

    company_id: int
    title: str = Field(min_length=1, max_length=300)
    raw_text: str = Field(min_length=1)  # RG-06 : conservé tel quel
    url: str | None = Field(default=None, max_length=500)
    location: str | None = Field(default=None, max_length=200)
    contract_type: str | None = Field(default=None, max_length=50)  # stage / alternance / cdi


class OfferRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    title: str
    raw_text: str
    url: str | None
    location: str | None
    contract_type: str | None
    created_at: datetime


class ApplicationUpdate(BaseModel):
    """EXG-006 / EXG-008 : transition de statut et/ou prochaine action datée."""

    status: ApplicationStatus | None = None
    next_action: str | None = Field(default=None, max_length=300)
    next_action_date: datetime | None = None
    notes: str | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    offer_id: int
    status: ApplicationStatus
    next_action: str | None
    next_action_date: datetime | None
    applied_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
# ---------- Contacts (M3) ----------

class ContactCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    role: str | None = Field(default=None, max_length=200)
    email: str | None = Field(default=None, max_length=300)
    phone: str | None = Field(default=None, max_length=300)
    linkedin_url: str | None = Field(default=None, max_length=300)
    source: str | None = Field(default=None, max_length=300)
    notes: str | None = None


class ContactUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    role: str | None = Field(default=None, max_length=200)
    email: str | None = Field(default=None, max_length=300)
    phone: str | None = Field(default=None, max_length=300)
    linkedin_url: str | None = Field(default=None, max_length=300)
    source: str | None = Field(default=None, max_length=300)
    notes: str | None = None


class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int | None
    full_name: str
    role: str | None 
    email: str | None
    phone: str | None
    linkedin_url: str | None
    source: str | None
    notes: str | None
    created_at: datetime
