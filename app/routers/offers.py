"""Module M2 — Offres : saisie (EXG-004) + candidature créée automatiquement (EXG-005)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Application, ApplicationStatus, Company, Offer
from app.schemas import OfferCreate, OfferRead

router = APIRouter(prefix="/offers", tags=["offers"])


@router.post("", response_model=OfferRead, status_code=status.HTTP_201_CREATED)
def create_offer(payload: OfferCreate, db: Session = Depends(get_db)):
    """Une seule transaction : l'offre et sa candidature naissent ensemble, ou pas du tout."""
    if db.get(Company, payload.company_id) is None:
        raise HTTPException(status_code=404, detail="Entreprise introuvable")

    offer = Offer(**payload.model_dump())
    application = Application(status=ApplicationStatus.WISHLIST)

    db.add(offer)
    db.flush()  # écrit dans la transaction pour obtenir offer.id, sans committer
    application.offer_id = offer.id
    db.add(application)
    db.commit()
    db.refresh(offer)
    return offer


@router.get("", response_model=list[OfferRead])
def list_offers(db: Session = Depends(get_db)):
    """Les offres les plus récentes d'abord."""
    return db.scalars(select(Offer).order_by(Offer.created_at.desc())).all()


@router.get("/{offer_id}", response_model=OfferRead)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.get(Offer, offer_id)
    if offer is None:
        raise HTTPException(status_code=404, detail="Offre introuvable")
    return offer
