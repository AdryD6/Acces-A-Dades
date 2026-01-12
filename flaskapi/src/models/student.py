from sqlalchemy import Column, Integer, String
from src.config import db

class Student(db.Base):
    __tablename__ = 'students'

    # Definición de columnas
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    spec = Column(String)  # Especialidad