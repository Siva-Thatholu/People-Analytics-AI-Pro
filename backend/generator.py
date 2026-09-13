import os
import random
from faker import Faker
import google.generativeai as genai
from sqlalchemy.orm import Session
from .models import Employee
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

fake = Faker()
departments = ["Engineering", "Sales", "Marketing", "HR", "Operations", "Finance"]
themes = ["compensation", "burnout", "management", "growth", "culture", "work-life balance"]

def get_live_gemini_analysis(feedback: str):
    """Live integration with Gemini 1.5 Flash for real-time processing."""
    try:
        model = genai.GenerativeModel('gemini-3.6-flash')
        prompt = f"""
        You are an expert HR Data Analyst. Analyze this employee feedback: "{feedback}"
        Return exactly two values separated by a comma:
        1. A sentiment score between 0.0 (extremely negative) and 1.0 (extremely positive).
        2. The primary theme (choose one: compensation, burnout, management, growth, culture, work-life balance, other).
        Example output: 0.2, burnout
        """
        response = model.generate_content(prompt)
        parts = response.text.strip().split(',')
        if len(parts) >= 2:
            return float(parts[0].strip()), parts[1].strip().lower()
    except Exception as e:
        print(f"Gemini API error: {e}")
    return 0.5, "neutral"

def generate_bulk_synthetic_data(db: Session, num_records: int = 10000):
    """
    Generates large volumes of data (up to 100k+) efficiently.
    To avoid hitting the free-tier Gemini API rate limits (15 requests/min), 
    we simulate the realistic distributions of sentiment and themes based on department profiles,
    while leaving the live API available for single queries.
    """
    if db.query(Employee).count() > 0:
        db.query(Employee).delete()
        db.commit()

    employees = []
    
    for i in range(num_records):
        dept = random.choice(departments)
        
        # Simulate realistic HR data distributions
        if dept == "Engineering":
            theme = random.choices(themes, weights=[10, 40, 10, 20, 10, 10])[0]
            sentiment = random.uniform(0.3, 0.8) if theme != "burnout" else random.uniform(0.1, 0.4)
        elif dept == "Sales":
            theme = random.choices(themes, weights=[50, 20, 10, 10, 10, 0])[0]
            sentiment = random.uniform(0.4, 0.9) if theme != "compensation" else random.uniform(0.1, 0.5)
        else:
            theme = random.choice(themes)
            sentiment = random.uniform(0.2, 0.9)

        risk = "Low"
        if sentiment < 0.4 or (sentiment < 0.5 and theme in ["burnout", "compensation"]):
            risk = "High" if random.random() > 0.4 else "Medium"
        elif sentiment < 0.7:
            risk = "Medium"

        emp = Employee(
            employee_id=f"EMP-{fake.unique.random_number(digits=6)}",
            department=dept,
            tenure_years=round(random.uniform(0.5, 15.0), 1),
            salary=random.randint(45000, 180000),
            performance_score=round(random.uniform(1.0, 5.0), 1),
            survey_feedback=fake.paragraph(nb_sentences=2),
            sentiment_score=round(sentiment, 2),
            key_theme=theme,
            flight_risk=risk
        )
        employees.append(emp)
        
        # Batch commit every 10,000 records to handle 100k+ smoothly without RAM crash
        if len(employees) >= 10000:
            db.bulk_save_objects(employees)
            db.commit()
            employees = []

    # Commit any remaining
    if employees:
        db.bulk_save_objects(employees)
        db.commit()
        
    return {"message": f"Successfully generated and loaded {num_records} employee records into the data warehouse."}
