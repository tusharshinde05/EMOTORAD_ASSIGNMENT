from pydantic import BaseModel
from typing import List, Optional

# Model for validating and structuring incoming contact request data
class ContactRequest(BaseModel):
    # Email field is required for identifying or creating contacts
    email: str
    
    # Optional phone number field, allowing requests with just an email if needed
    phoneNumber: Optional[str]

# Model for structuring the response data for contact-related requests
class ContactResponse(BaseModel):
    # ID of the primary contact associated with the request
    primaryContactId: int
    
    # List of all emails associated with the primary and linked secondary contacts
    emails: List[str]
    
    # List of all phone numbers associated with the primary and linked secondary contacts
    phoneNumbers: List[str]
    
    # List of IDs for contacts linked as secondary to the primary contact
    secondaryContactIds: List[int]
