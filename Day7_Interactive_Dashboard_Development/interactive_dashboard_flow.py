"""
DAY 7 - INTERACTIVE DASHBOARD DEVELOPMENT
========================================
Learning Outcome (from problem statement):
    Develop an interactive analytical dashboard supporting decision-making.

Deliverables Generated:
    1. Complete Interactive Dashboard Spec (Complete_Interactive_Dashboard_Spec.md)
    2. Dashboard Navigation Flow (Dashboard_Navigation_Flow.md)
    3. Interactive Dashboard Summary Export (interactive_dashboard_summary.csv)
    4. Visual Navigation Flow Diagram (navigation_flow_diagram.png)
"""

import os
import shutil
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SHARED_DATA_DIR = os.path.join(PROJECT_ROOT, "shared_data")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

TABLE_NAMES = [
    "Employee", "Role", "Training", "Performance_Review",
    "Skill_Assessment", "Mobility_Application", "Mobility_Risk"
]

def sync_data():
    for tbl in TABLE_NAMES:
        src = os.path.join(SHARED_DATA_DIR, f"{tbl}.csv")
        dst = os.path.join(DATA_DIR, f"{tbl}.csv")
        if os.path.exists(src):
            shutil.copy(src, dst)

def run_interactive_dashboard():
    print("=== Running Day 7 Interactive Dashboard Development ===")
    sync_data()

    emp = pd.read_csv(os.path.join(DATA_DIR, "Employee.csv"))
    roles = pd.read_csv(os.path.join(DATA_DIR, "Role.csv"))
    trn = pd.read_csv(os.path.join(DATA_DIR, "Training.csv"))
    perf = pd.read_csv(os.path.join(DATA_DIR, "Performance_Review.csv"))
    skills = pd.read_csv(os.path.join(DATA_DIR, "Skill_Assessment.csv"))
    mob = pd.read_csv(os.path.join(DATA_DIR, "Mobility_Application.csv"))

    # Build Module Summaries
    module_summary = [
        {"Module": "Employee Overview", "Target_Audience": "HR Leadership", "Primary_Visuals": "Headcount Card, Dept Distribution Donut, Tenure Histogram"},
        {"Module": "Role Requirements Matrix", "Target_Audience": "Talent Acquisition", "Primary_Visuals": "Open Roles Table, Skill Gap Bar Chart, Requisition Aging"},
        {"Module": "Training & Upskilling", "Target_Audience": "L&D Team", "Primary_Visuals": "Course Completion Leaderboard, Training vs Rating Scatter"},
        {"Module": "Performance Evaluation", "Target_Audience": "Department Managers", "Primary_Visuals": "Rating Boxplots, Review Timeline, High-Performer Grid"},
        {"Module": "Skill Assessment Analytics", "Target_Audience": "HRBPs", "Primary_Visuals": "Skill Heatmap, Proficiency Radar Chart, Competency Matrix"},
        {"Module": "Mobility & Readiness", "Target_Audience": "Workforce Planning", "Primary_Visuals": "Readiness Funnel, Candidate Ranking Grid, Risk Category Pie"}
    ]

    mod_df = pd.DataFrame(module_summary)
    mod_df.to_csv(os.path.join(OUT_DIR, "interactive_dashboard_summary.csv"), index=False)

    # Visual Navigation Flow Diagram
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")

    flow_text = """
    ===================================================================================
                             INTERACTIVE DASHBOARD NAVIGATION FLOW
    ===================================================================================

       [ DAY 6 EXECUTIVE OVERVIEW ]  ---> Main Landing Page (KPI Summaries & Slicers)
                 |
                 +---> [ MODULE 1: EMPLOYEE PROFILES ]  (Drill-down by ID / Dept)
                 |
                 +---> [ MODULE 2: ROLE MATCHING MATRIX ] (Required Skills vs Current Skills)
                 |
                 +---> [ MODULE 3: TRAINING & UPSKILLING ] (Course Completions & ROI)
                 |
                 +---> [ MODULE 4: PERFORMANCE ANALYTICS ] (Ratings & Evaluation History)
                 |
                 +---> [ MODULE 5: MOBILITY & READINESS ] (ML Readiness Scores & Risk Alerts)
                 |
                 v
       [ DAY 9 AI RECOMMENDATION SYSTEM ] ---> Automated Role Recommendation & Action Plan

    ===================================================================================
    """
    ax.text(0.5, 0.5, flow_text, fontsize=9, family="monospace", va="center", ha="center",
            bbox=dict(boxstyle="round,pad=1", facecolor="lightcyan", edgecolor="teal"))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "navigation_flow_diagram.png"), dpi=150)
    plt.close()

    generate_reports(mod_df)
    print("Day 7 Interactive Dashboard Development completed successfully!")

def generate_reports(mod_df):
    # 1. Complete Interactive Dashboard Spec
    cid_doc = f"""# Day 7 Deliverable: Complete Interactive Dashboard Specification

## Interactive Dashboard Architecture
The interactive multi-page Power BI dashboard consists of **6 specialized analytical modules** designed for HRBPs, L&D managers, and workforce planners.

## Dashboard Modules Reference
```
{mod_df.to_string(index=False)}
```

## Interactive Features & Drill-Throughs
1. **Dynamic Cross-Filtering**: Selecting any department in Module 1 automatically updates all visual cards across all 6 pages.
2. **Employee Drill-Through**: Right-click on any employee in the grid to view their complete 360-degree profile (Training history, performance reviews, skill assessments, mobility applications).
3. **Role-Matching Tooltip**: Hovering over open positions displays real-time candidate availability matching required skills.
"""
    with open(os.path.join(OUT_DIR, "Complete_Interactive_Dashboard_Spec.md"), "w") as f:
        f.write(cid_doc)

    # 2. Dashboard Navigation Flow
    dnf_doc = """# Day 7 Deliverable: Dashboard Navigation Flow

## Navigation Hierarchy
- **Page 1: Executive Overview**: High-level KPI indicators and organization-wide summary.
- **Page 2: Talent Pool & Skills Matrix**: Deep-dive into technical proficiencies and departmental skill gaps.
- **Page 3: Upskilling & L&D Tracker**: Training completion velocity and course effectiveness.
- **Page 4: Internal Mobility Pipeline**: Application funnel, candidate shortlists, and readiness prediction scores.

## User Flow Diagram
```mermaid
graph TD
    A[Executive Overview Page] --> B[Talent Pool & Skills Matrix]
    A --> C[Upskilling & L&D Tracker]
    A --> D[Internal Mobility Pipeline]
    B --> E[Employee 360 Drill-Through Profile]
    D --> E
```
"""
    with open(os.path.join(OUT_DIR, "Dashboard_Navigation_Flow.md"), "w") as f:
        f.write(dnf_doc)

if __name__ == "__main__":
    run_interactive_dashboard()
