from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Create the SQLAlchemy engine
DATABASE_URL = 'sqlite:///E:/SNP-CC/database/sessions.db'
engine = create_engine(DATABASE_URL, echo=True)

# Define the base class for declarative class definitions
Base = declarative_base()

# Define the Session model
class Session(Base):
    __tablename__ = 'sessions'
    
    # Columns definition
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incremented ID
    session_id = Column(String(255), unique=True, nullable=False)  # Unique session identifier
    data = Column(Text, nullable=False)  # Serialized session data
    expiry = Column(DateTime, default=func.now(), nullable=False)  # Expiration time

    def __repr__(self):
        return f"<Session(id={self.id}, session_id={self.session_id}, expiry={self.expiry})>"

# Create the database and table
Base.metadata.create_all(engine)

print("Database and session table created successfully.")
