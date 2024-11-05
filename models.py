from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Define the Contact model, mapped to the 'contacts' table in the database
class Contact(Base):
    __tablename__ = "contacts"  # Define table name in the database
    
    # Unique identifier for each contact, set as the primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Contact's phone number, indexed for faster lookups; can be nullable
    phoneNumber = Column(String, index=True, nullable=True)
    
    # Contact's email address, also indexed and can be nullable
    email = Column(String, index=True, nullable=True)
    
    # Self-referential foreign key to link secondary contacts to a primary contact
    # 'linkedId' refers to the 'id' of another contact within the same table
    linkedId = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    
    # Field indicating if a contact is a 'primary' or 'secondary' contact in the linked group
    linkPrecedence = Column(String, default="primary")  # Defaults to "primary"
    
    # Timestamp of when the contact was created, automatically set to the current time
    createdAt = Column(DateTime, default=func.now())
    
    # Timestamp of the last update to the contact, automatically updated on each change
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Timestamp for when the contact is marked as deleted, if applicable; initially nullable
    deletedAt = Column(DateTime, nullable=True)
    
    # Self-referential relationship to link to the 'linkedId' contact
    # 'remote_side' specifies the column on the "other side" of the relationship
    linked_contact = relationship("Contact", remote_side=[id])
