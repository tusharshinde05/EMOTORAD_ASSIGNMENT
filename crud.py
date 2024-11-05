from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_matching_contact(db: Session, email: str, phoneNumber: str):
    """
    Fetches the first contact in the database that matches either the email or phone number provided.
    """
    return db.query(models.Contact).filter(
        (models.Contact.email == email) | (models.Contact.phoneNumber == phoneNumber)
    ).first()

def create_or_update_contact(db: Session, email: str, phoneNumber: str):
    """
    Creates a new contact if no matching contact exists; if a match is found, 
    updates the contact as needed or creates a secondary linked contact.
    """
    # Retrieve any existing contact that matches the email or phone number
    existing_contact = get_matching_contact(db, email, phoneNumber)

    if existing_contact:
        # Check if the matching contact has the same email and phone number as provided
        if existing_contact.email == email and existing_contact.phoneNumber == phoneNumber:
            # If exact match, create a secondary contact linked to the existing one
            secondary_contact = models.Contact(
                email=email,
                phoneNumber=phoneNumber,
                linkedId=existing_contact.id,  # Link to the primary contact
                linkPrecedence="secondary",  # Mark as secondary
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )
            db.add(secondary_contact)
            db.commit()
            db.refresh(secondary_contact)
            return secondary_contact
        else:
            # If either email or phone matches, but not both, update contact as secondary if needed
            if existing_contact.linkPrecedence == "primary":
                # Change existing contact's precedence to secondary
                existing_contact.linkPrecedence = "secondary"
                db.commit()  # Commit changes to update precedence

                # Create a new contact as primary with provided email and phone number
                new_contact = models.Contact(
                    email=email,
                    phoneNumber=phoneNumber,
                    linkedId=existing_contact.id,  # Link to the former primary contact
                    linkPrecedence="primary",  # Set this new entry as primary
                    createdAt=datetime.now(),
                    updatedAt=datetime.now()
                )
                db.add(new_contact)
                db.commit()
                db.refresh(new_contact)
                return new_contact
            else:
                # If existing contact is already marked as secondary, return it without changes
                return existing_contact
    else:
        # No matching contact found, so create a new primary contact
        new_contact = models.Contact(
            email=email,
            phoneNumber=phoneNumber,
            linkedId=None,  # No linked ID as this is a standalone contact
            linkPrecedence="primary",  # Mark as primary
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact
