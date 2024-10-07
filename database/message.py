from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define the path to your database file
DATABASE_PATH = 'E:/SNP-CC/database/messages.db'

# Define the SQLAlchemy engine
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=True)

# Define the base class for declarative class definitions
Base = declarative_base()

# Define the Message model
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(String(50), nullable=False)
    recipient = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

# Create the database and table
def create_db():
    Base.metadata.create_all(engine)
    print(f"Database '{DATABASE_PATH}' created with table 'messages'.")

if __name__ == '__main__':
    create_db()
