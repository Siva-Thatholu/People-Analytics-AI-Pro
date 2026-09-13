from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    department = Column(String)
    tenure_years = Column(Float)
    salary = Column(Integer)
    performance_score = Column(Float)
    survey_feedback = Column(Text)
    sentiment_score = Column(Float)
    key_theme = Column(String)
    flight_risk = Column(String)
