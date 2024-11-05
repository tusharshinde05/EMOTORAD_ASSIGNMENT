from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
from sqlalchemy.orm import sessionmaker

# Dependency to create a database session for each request and close it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the FastAPI application
app = FastAPI()

# Pydantic model to validate incoming request data
class ContactIn(BaseModel):
    email: str
    phoneNumber: str

# Pydantic model to structure the response data
class ContactOut(BaseModel):
    primaryContactId: int
    emails: list
    phoneNumbers: list
    secondaryContactIds: list

    class Config:
        orm_mode = True  # Enable ORM mode to work with ORM objects

@app.post("/identify", response_model=ContactOut)
def identify(contact: ContactIn, db: Session = Depends(get_db)):
    """
    Identifies or creates contact information based on the given email and phone number.
    If a matching contact exists, it creates a secondary contact and updates primary details as needed.
    If no match, creates a new primary contact.
    """
    # Check if any contact matches the provided email or phone number
    existing_contact = db.query(models.Contact).filter(
        (models.Contact.email == contact.email) | (models.Contact.phoneNumber == contact.phoneNumber)
    ).first()

    if existing_contact:
        # If a matching contact is found, create a secondary contact linked to the primary one
        new_contact = models.Contact(
            email=contact.email,
            phoneNumber=contact.phoneNumber,
            linkedId=existing_contact.id,  # Link to the primary contact
            linkPrecedence="secondary"  # Set as secondary contact
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        # Update the primary contact's email or phone number if it differs from the new contact's
        if existing_contact.email != contact.email:
            existing_contact.email = contact.email
        if existing_contact.phoneNumber != contact.phoneNumber:
            existing_contact.phoneNumber = contact.phoneNumber

        db.commit()
        db.refresh(existing_contact)

        # Retrieve all secondary contacts linked to the primary contact for response
        secondary_contacts = db.query(models.Contact).filter(
            models.Contact.linkedId == existing_contact.id, 
            models.Contact.linkPrecedence == "secondary"
        ).all()
        secondary_ids = [contact.id for contact in secondary_contacts]

        # Return the response with primary contact details and linked secondary contacts
        return {
            "primaryContactId": existing_contact.id,
            "emails": [existing_contact.email],
            "phoneNumbers": [existing_contact.phoneNumber],
            "secondaryContactIds": secondary_ids
        }
    else:
        # No existing contact found; create a new primary contact
        new_contact = models.Contact(
            email=contact.email,
            phoneNumber=contact.phoneNumber,
            linkPrecedence="primary"  # Set as primary contact
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        # Return response with the new primary contact details
        return {
            "primaryContactId": new_contact.id,
            "emails": [new_contact.email],
            "phoneNumbers": [new_contact.phoneNumber],
            "secondaryContactIds": []
        }
