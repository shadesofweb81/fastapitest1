from sqlmodel import SQLModel, create_engine, Session
import os

# PostgreSQL connection URL with psycopg3
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:password@localhost:5432/db1")

# SQLAlchemy engine for SQLModel
engine = create_engine(DATABASE_URL, echo=True)

# Function to create database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency to get a session
def get_session():
    with Session(engine) as session:
        yield session
