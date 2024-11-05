# EMOTORAD_ASSIGNMENT
This is a FastAPI application for managing contacts, which includes functionalities to create, update, and manage primary and secondary contacts.
## Features
- Create and update contacts
- Store and manage primary and secondary contact entries
- Handle duplicate contact information
- Return contact details in a structured format
## Prerequisites
- Python 3.7 or higher
- A virtual environment (recommended)
- PostgreSQL or any other database for storage
## Installation
Follow these steps to set up the project locally:
1. **Clone the repository:**
   git clone https://github.com/<your-username>/EMOTORAD.git
   cd EMOTORAD
2. **Create a Virtual Environment:**
   ### If you haven't installed virtualenv, you can do so via pip:
   pip install virtualenv
   ### Then create and activate a virtual environment:
   virtualenv venv
   ### On Windows
   venv\Scripts\activate
   ### On macOS/Linux
   source venv/bin/activate
3. **Install dependencies::**
   ### Install the required Python packages using pip:
   pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic
   fastapi: The web framework for building APIs.
   uvicorn: ASGI server for serving the FastAPI application.
   sqlalchemy: ORM for database interactions.
   psycopg2-binary: PostgreSQL adapter for Python.
   pydantic: Data validation and settings management.
4. **Set up your database:**
   Create a PostgreSQL database and update your database connection settings in the
   application code (usually in the get_db function in main.py).
5. **Run the application:**
   uvicorn app.main:app --reload
The API will be accessible at http://127.0.0.1:8000/docs


   
   
