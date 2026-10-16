"""
DAY 9 - SMART WORKFORCE PLANNING INSIGHTS & RECOMMENDATION SYSTEM
================================================================
Learning Outcome (from problem statement):
    Develop an AI-driven recommendation system for actionable workforce planning insights.

Deliverables Generated:
    1. AI Recommendation Dashboard (AI_Recommendation_Dashboard.md)
    2. Final Power BI Dashboard Spec (Final_Power_BI_Dashboard_Spec.md)
    3. Complete Project Report (Project_Report.md)
    4. Project Presentation PPT Outline (Project_Presentation.md)
    5. Role Matching Recommendations Export (role_matching_recommendations.csv)
"""

import os
import shutil
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SHARED_DATA_DIR = os.path.join(PROJECT_ROOT, "shared_data")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

TABLE_NAMES = [
    "Employee", "Role", "Open_Position", "Skill_Assessment",
    "Performance_Review", "Training", "Mobility_Risk"
]

def sync_data():
    for tbl in TABLE_NAMES:
        src = os.path.join(SHARED_DATA_DIR, f"{tbl}.csv")
        dst = os.path.join(DATA_DIR, f"{tbl}.csv")
        if os.path.exists(src):
            shutil.copy(src, dst)

def run_recommendation_engine():
    print("=== Running Day 9 Smart Workforce Planning Recommendation System ===")
    sync_data()

    emp = pd.read_csv(os.path.join(DATA_DIR, "Employee.csv"))
    roles = pd.read_csv(os.path.join(DATA_DIR, "Role.csv"))
    open_pos = pd.read_csv(os.path.join(DATA_DIR, "Open_Position.csv"))
    skills = pd.read_csv(os.path.join(DATA_DIR, "Skill_Assessment.csv"))
    perf = pd.read_csv(os.path.join(DATA_DIR, "Performance_Review.csv"))
    risk = pd.read_csv(os.path.join(DATA_DIR, "Mobility_Risk.csv"))

    # Skill matching engine between employee skills and open position required skills
    recommendations = []

    # Map required skills per role
    role_skills = roles.set_index("Role_ID")["Required_Skills"].to_dict()
    role_titles = roles.set_index("Role_ID")["Role_Title"].to_dict()
    role_depts = roles.set_index("Role_ID")["Department"].to_dict()

    # Employee skill dictionary
    emp_skill_map = skills.groupby("Employee_ID").apply(
        lambda g: dict(zip(g["Skill_Name"], g["Proficiency_Score"]))
    ).to_dict()

    perf_map = perf.groupby("Employee_ID")["Rating"].mean().to_dict()
    readiness_map = risk.groupby("Employee_ID")["Readiness_Score"].mean().to_dict()

    for _, pos in open_pos.iterrows():
        pos_id = pos["Position_ID"]
        r_id = pos["Role_ID"]
        r_title = role_titles.get(r_id, "Unknown Role")
        r_dept = role_depts.get(r_id, "Unknown Dept")
        req_skills_str = role_skills.get(r_id, "")
        req_skills_list = [s.strip() for s in req_skills_str.split(",") if s.strip()]

        for _, e in emp.iterrows():
            e_id = e["Employee_ID"]
            e_name = e["Employee_Name"]
            e_dept = e["Department"]
            e_skills = emp_skill_map.get(e_id, {})
            e_rating = perf_map.get(e_id, 3.0)
            e_readiness = readiness_map.get(e_id, 50.0)

            # Match score computation
            if req_skills_list:
                scores = [e_skills.get(s, 0) for s in req_skills_list]
                skill_match_pct = np.mean(scores)
            else:
                skill_match_pct = 50.0

            # Composite Recommendation Score (0-100)
            composite_score = (0.50 * skill_match_pct) + (0.30 * e_readiness) + (0.20 * (e_rating / 5 * 100))

            if composite_score >= 65:
                recommendations.append({
                    "Position_ID": pos_id,
                    "Target_Role": r_title,
                    "Role_Department": r_dept,
                    "Employee_ID": e_id,
                    "Employee_Name": e_name,
                    "Employee_Department": e_dept,
                    "Skill_Match_%": round(skill_match_pct, 1),
                    "Readiness_Score": round(e_readiness, 1),
                    "Performance_Rating": round(e_rating, 2),
                    "Recommendation_Score": round(composite_score, 1),
                    "Suggested_Upskilling": ", ".join([s for s in req_skills_list if e_skills.get(s, 0) < 60]) or "None (Ready)"
                })

    rec_df = pd.DataFrame(recommendations)
    rec_df = rec_df.sort_values("Recommendation_Score", ascending=False)
    rec_df.to_csv(os.path.join(OUT_DIR, "role_matching_recommendations.csv"), index=False)

    generate_reports(rec_df)
    print("Day 9 Smart Workforce Planning Recommendation System completed successfully!")

def generate_reports(rec_df):
    # 1. AI Recommendation Dashboard
    ard_doc = f"""# Day 9 Deliverable: AI Recommendation Dashboard Specification

## Recommendation Engine Architecture
- **Skill Alignment Matching**: Calculates weighted overlap between employee demonstrated proficiencies and open position required skill sets.
- **Composite Score Formula**:
  `Composite_Score = (50% * Skill_Match_%) + (30% * Readiness_Score) + (20% * Performance_Rating_Index)`

## Recommended Match Summary
- Total High-Match Candidate Recommendations Generated: {len(rec_df)}
- Top Recommended Role Matches:
```
{rec_df[['Target_Role', 'Employee_Name', 'Employee_Department', 'Recommendation_Score', 'Suggested_Upskilling']].head(8).to_string(index=False)}
```
"""
    with open(os.path.join(OUT_DIR, "AI_Recommendation_Dashboard.md"), "w") as f:
        f.write(ard_doc)

    # 2. Final Power BI Dashboard Spec
    fpb_doc = """# Day 9 Deliverable: Final Power BI Dashboard Specification

## Master Workspace Layout
- **Page 1: Executive Workforce Planning Command Center**
- **Page 2: Skill-Gap & Anomaly Risk Monitoring**
- **Page 3: Employee Segmentation & Mobility Ready Cohorts**
- **Page 4: Predictive Internal Mobility & AI Role-Matching Engine**

## Governance & Security
- Role-Level Security (RLS) configured by Department for HR Business Partners.
"""
    with open(os.path.join(OUT_DIR, "Final_Power_BI_Dashboard_Spec.md"), "w") as f:
        f.write(fpb_doc)

    # 3. Complete Project Report
    pr_doc = """# Day 9 Deliverable: Complete Project Report

# Internal Mobility and Skill-Gap Analytics System

## Executive Summary
This project delivers an end-to-end predictive analytics and machine learning solution for workforce planning, internal mobility optimization, and skill-gap remediation across **600 employees** and **9 integrated relational tables**.

## Key Stages Summary (Day 1 - Day 9)
1. **Day 1 (ETL Pipeline)**: Ingested, cleaned, and validated relational integrity across all 9 data tables.
2. **Day 2 (EDA)**: Analyzed statistical distributions, department skill gaps, and feature correlation matrices.
3. **Day 3 (Employee Segmentation)**: Clustered workforce into 4 actionable cohorts using K-Means and PCA.
4. **Day 4 (Workforce Performance)**: Measured departmental upskilling allocation efficiency and KPIs.
5. **Day 5 (Anomaly Detection)**: Flagged 36 high-risk/anomalous skill profiles using Isolation Forest.
6. **Day 6 (KPI Dashboard)**: Created standard DAX measures and executive visual indicators.
7. **Day 7 (Interactive Dashboards)**: Architected complete 6-module interactive Power BI dashboard navigation flow.
8. **Day 8 (Mobility Readiness Prediction)**: Trained Random Forest models predicting readiness score (R²) and readiness category probability (Accuracy/F1).
9. **Day 9 (Smart Recommendation Engine)**: Deployed composite role-matching algorithm with personalized upskilling suggestions.
"""
    with open(os.path.join(OUT_DIR, "Project_Report.md"), "w") as f:
        f.write(pr_doc)

    # 4. Project Presentation PPT Outline
    ppt_doc = """# Day 9 Deliverable: Project Presentation Outline (PPT)

## Slide Deck Architecture (10 Slides)

- **Slide 1**: Title Slide – Internal Mobility and Skill-Gap Analytics System
- **Slide 2**: Problem Statement – Transitioning from Reactive HR to Predictive Intelligence
- **Slide 3**: Relational Data Model – Multi-table Schema (9 Tables)
- **Slide 4**: Exploratory Data Analysis & Skill Distribution Insights
- **Slide 5**: Employee Segmentation (K-Means Clustering & 4 Key Cohorts)
- **Slide 6**: Skill-Gap Risk & Anomaly Detection (Isolation Forest Results)
- **Slide 7**: Machine Learning Mobility Readiness Prediction (Random Forest Models)
- **Slide 8**: Power BI Executive & Interactive Dashboard Suite
- **Slide 9**: AI Role-Matching & Upskilling Recommendation Engine
- **Slide 10**: Business ROI, Recommendations, & Implementation Roadmap
"""
    with open(os.path.join(OUT_DIR, "Project_Presentation.md"), "w") as f:
        f.write(ppt_doc)

if __name__ == "__main__":
    run_recommendation_engine()
