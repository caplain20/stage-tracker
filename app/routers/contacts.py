from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Company, Contact
from app.schemas import ContactCreate, ContactRead, ContactUpdate

router = APIRouter()


@router.post("/companies/{company_id}/contacts", response_model=ContactRead, status_code=201)
def create_contact_for_company(company_id: int, payload: ContactCreate, db: Session = Depends(get_db)):
    """Ajoute un contact rattaché à une entreprise existante."""
    if db.get(Company, company_id) is None:
        raise HTTPException(status_code=404, detail="Entreprise introuvable")
    contact = Contact(**payload.model_dump(), company_id=company_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.post("/contacts", response_model=ContactRead, status_code=201)
def create_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    """Crée un contact orphelin (sans entreprise — ex: recruteur LinkedIn)."""
    contact = Contact(**payload.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.get("/companies/{company_id}/contacts", response_model=list[ContactRead])
def list_contacts_of_company(company_id: int, db: Session = Depends(get_db)):
    """Liste les contacts d'une entreprise, par ordre alphabétique."""
    if db.get(Company, company_id) is None:
        raise HTTPException(status_code=404, detail="Entreprise introuvable")
    contacts = db.scalars(
        select(Contact).where(Contact.company_id == company_id).order_by(Contact.full_name)
    ).all()
    return contacts


@router.get("/contacts", response_model=list[ContactRead])
def list_contacts(db: Session = Depends(get_db)):
    """Liste tous les contacts (rattachés à une entreprise ou non)."""
    contacts = db.scalars(select(Contact).order_by(Contact.full_name)).all()
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactRead)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact introuvable")
    return contact


@router.patch("/contacts/{contact_id}", response_model=ContactRead)
def update_contact(contact_id: int, payload: ContactUpdate, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact introuvable")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact introuvable")
    db.delete(contact)
    db.commit()
