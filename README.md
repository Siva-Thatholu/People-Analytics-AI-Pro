# 🧠 AI-Driven People Analytics & Attrition Forecasting

## 📌 Project Overview
High employee turnover costs enterprises millions in recruitment and lost productivity. Traditional HR metrics (salary, tenure) fail to capture the human element of *why* people leave. 

This full-stack Data Analytics project utilizes **Python, FastAPI, SQLite, and the Google Gemini 1.5 LLM** to analyze unstructured employee survey data, score sentiment, extract key themes (e.g., Burnout, Compensation), and predict flight risk at scale.

## 💼 Business Impact & Data Analyst Portfolio Highlights
This project was built to demonstrate production-level data engineering and analysis skills for Data Analyst roles:
*   **Big Data Handling:** Capable of generating, ingesting, and querying **100,000+ synthetic records** using SQL bulk operations and optimized database interactions.
*   **API Optimization:** Designed aggregation endpoints in FastAPI to compute complex statistics on the server-side via SQL `GROUP BY` clauses, preventing massive data payloads from crashing the frontend.
*   **Actionable ROI:** Includes a financial dashboard that calculates the "Cost of Turnover," translating data insights directly into dollar-value business impact.
*   **LLM Integration:** Demonstrates applied AI skills by using Gemini 1.5 Flash to transform qualitative, unstructured text data into quantitative, structured analytical features.

## 🛠️ Tech Stack
*   **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy (SQLite)
*   **Frontend:** Streamlit, Pandas, Plotly Express
*   **AI/NLP:** Google Generative AI (Gemini 1.5 Flash)
*   **Data Gen:** Python Faker

## 🚀 Setup Instructions
1.  **Clone & Environment:** Create a virtual environment `python -m venv venv` and activate it.
2.  **Install Dependencies:** `pip install -r requirements.txt` (If on Windows, use `pip install greenlet --only-binary :all:` before installing the rest).
3.  **API Key:** Replace `your_actual_api_key_here` in `.env` with a real Google Gemini API key.
4.  **Run Backend:** `uvicorn backend.main:app --reload`
5.  **Run Frontend (New Terminal):** `streamlit run frontend/app.py`
