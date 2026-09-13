from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import engine, Base, get_db
from .models import Employee
from .generator import generate_bulk_synthetic_data, get_live_gemini_analysis
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="People Analytics API - Pro Version")

class FeedbackRequest(BaseModel):
    feedback: str

@app.post("/api/generate")
def trigger_data_generation(num_records: int = 10000, db: Session = Depends(get_db)):
    return generate_bulk_synthetic_data(db, num_records)

@app.post("/api/analyze-live")
def analyze_live_feedback(req: FeedbackRequest):
    """Exposes Gemini directly for the frontend Live Demo tab."""
    score, theme = get_live_gemini_analysis(req.feedback)
    return {"sentiment_score": score, "key_theme": theme}

@app.get("/api/analytics/aggregates")
def get_aggregated_stats(db: Session = Depends(get_db)):
    """
    PRODUCTION UPGRADE: Instead of sending 100,000+ rows to the frontend,
    we perform aggregations on the backend SQL level for instant performance.
    """
    total_emps = db.query(Employee).count()
    if total_emps == 0:
        return {"total_employees": 0}
        
    avg_sentiment = db.query(func.avg(Employee.sentiment_score)).scalar()
    high_risk_count = db.query(Employee).filter(Employee.flight_risk == "High").count()
    
    # Department risk aggregations
    dept_stats = db.query(
        Employee.department, 
        Employee.flight_risk, 
        func.count(Employee.id)
    ).group_by(Employee.department, Employee.flight_risk).all()
    
    # Theme aggregations
    theme_stats = db.query(
        Employee.key_theme,
        func.count(Employee.id)
    ).group_by(Employee.key_theme).all()
    
    return {
        "total_employees": total_emps,
        "average_sentiment": round(avg_sentiment, 2),
        "high_risk_count": high_risk_count,
        "department_stats": [{"department": d, "risk": r, "count": c} for d, r, c in dept_stats],
        "theme_stats": [{"theme": t, "count": c} for t, c in theme_stats]
    }

@app.get("/api/employees/sample")
def get_employee_sample(limit: int = 1000, db: Session = Depends(get_db)):
    """Returns a paginated/limited sample for the data table to prevent browser crashes."""
    return db.query(Employee).limit(limit).all()
