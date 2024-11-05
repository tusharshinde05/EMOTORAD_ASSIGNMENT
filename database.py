from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for connection; using SQLite in this example (change as needed for other databases)
DATABASE_URL = "sqlite:///./test.db"  # Change this to your actual database URL

# Create a database engine which manages connections to the specified database
# Setting check_same_thread=False for SQLite to allow multiple threads to access the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal is a session factory that creates new Session objects for each database interaction
# autocommit=False: Transactions will not be committed automatically, allowing manual control
# autoflush=False: Changes will not be flushed to the database until explicitly committed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is a class that models can inherit from, enabling SQLAlchemy to map them to database tables
Base = declarative_base()

def init_db():
    """
    Initializes the database by creating all tables defined in the model classes
    that inherit from Base. It binds the tables to the engine specified.
    """
    Base.metadata.create_all(bind=engine)
