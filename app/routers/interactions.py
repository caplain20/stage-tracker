from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Application, Contact, Interaction
from app.schemas import InteractionCreate, InteractionRead, InteractionUpdate

router = APIRouter()


@router.post("/applications/{application_id}/interactions", response_model=InteractionRead, status_code=201)
def create_interaction(application_id: int, payload: InteractionCreate, db: Session = Depends(get_db)):
    """Logge un échange dans le journal d'une candidature."""
    if db.get(Application, application_id) is None:
        raise HTTPException(status_code=404, detail="Candidature introuvable")
    if payload.contact_id is not None and db.get(Contact, payload.contact_id) is None:
        raise HTTPException(status_code=404, detail="Contact introuvable")
    data = payload.model_dump(exclude_unset=True)
    if data.get("occurred_at") is None:
        data.pop("occurred_at", None)  # laisser le server_default horodater par la base
    interaction = Interaction(application_id=application_id, **data)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("/applications/{application_id}/interactions", response_model=list[InteractionRead])
def list_interactions_of_application(application_id: int, db: Session = Depends(get_db)):
    """Journal d'une candidature, du plus récent au plus ancien."""
    if db.get(Application, application_id) is None:
        raise HTTPException(status_code=404, detail="Candidature introuvable")
    interactions = db.scalars(
        select(Interaction)
        .where(Interaction.application_id == application_id)
        .order_by(Interaction.occurred_at.desc())
    ).all()
    return interactions


@router.get("/interactions/{interaction_id}", response_model=InteractionRead)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.get(Interaction, interaction_id)
    if interaction is None:
        raise HTTPException(status_code=404, detail="Interaction introuvable")
    return interaction


@router.patch("/interactions/{interaction_id}", response_model=InteractionRead)
def update_interaction(interaction_id: int, payload: InteractionUpdate, db: Session = Depends(get_db)):
    interaction = db.get(Interaction, interaction_id)
    if interaction is None:
        raise HTTPException(status_code=404, detail="Interaction introuvable")
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("contact_id") is not None and db.get(Contact, changes["contact_id"]) is None:
        raise HTTPException(status_code=404, detail="Contact introuvable")
    if changes.get("occurred_at") is None:
        changes.pop("occurred_at", None)
    for field, value in changes.items():
        setattr(interaction, field, value)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.delete("/interactions/{interaction_id}", status_code=204)
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.get(Interaction, interaction_id)
    if interaction is None:
        raise HTTPException(status_code=404, detail="Interaction introuvable")
    db.delete(interaction)
    db.commit()
