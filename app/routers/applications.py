"""Module M2 — Pipeline des candidatures : transitions manuelles (EXG-006),
prochaine action datée (EXG-008), filtrage (EXG-009)."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Application, ApplicationStatus
from app.schemas import ApplicationRead, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", response_model=list[ApplicationRead])
def list_applications(
    status_filter: ApplicationStatus | None = None,
    db: Session = Depends(get_db),
):
    """Toutes les candidatures, ou filtrées par statut : /applications?status_filter=applied"""
    query = select(Application).order_by(Application.updated_at.desc())
    if status_filter is not None:
        query = query.where(Application.status == status_filter)
    return db.scalars(query).all()


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Candidature introuvable")
    return application


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    """Transition manuelle de statut (EXG-006) et/ou prochaine action datée (EXG-008)."""
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Candidature introuvable")

    changes = payload.model_dump(exclude_unset=True)

    if "status" in changes:
        application.status = changes["status"]
        if changes["status"] == ApplicationStatus.APPLIED and application.applied_at is None:
            application.applied_at = datetime.now(timezone.utc)  # horodatage automatique

    for field in ("next_action", "next_action_date", "notes"):
        if field in changes:
            setattr(application, field, changes[field])

    db.commit()
    db.refresh(application)
    return application
