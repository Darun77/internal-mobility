"""
DAY 6 - WORKFORCE PLANNING KPI DASHBOARD
========================================
Learning Outcome (from problem statement):
    Design executive dashboards summarizing workforce planning performance.

Deliverables Generated:
    1. Executive Dashboard (Executive_Dashboard.md)
    2. KPI Dashboard (KPI_Dashboard.md)
    3. Dashboard Documentation (Dashboard_Documentation.md)
    4. DAX Measures Reference Export (dax_measures_reference.csv)
    5. Visual KPI Card Summary (kpi_card_summary.png)
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

def run_kpi_dashboard():
    print("=== Running Day 6 Workforce Planning KPI Dashboard ===")
    sync_data()

    # Define DAX Measures for Power BI Implementation
    dax_measures = [
        {"Measure_Name": "Total Headcount", "DAX_Formula": "COUNT(Employee[Employee_ID])", "Category": "Workforce Size"},
        {"Measure_Name": "Avg Rating", "DAX_Formula": "AVERAGE(Performance_Review[Rating])", "Category": "Performance"},
        {"Measure_Name": "Avg Skill Score", "DAX_Formula": "AVERAGE(Skill_Assessment[Proficiency_Score])", "Category": "Skills"},
        {"Measure_Name": "Total Trainings", "DAX_Formula": "COUNT(Training[Training_ID])", "Category": "Upskilling"},
        {"Measure_Name": "Mobility Applications", "DAX_Formula": "COUNT(Mobility_Application[Application_ID])", "Category": "Mobility"},
        {"Measure_Name": "Mobility Rate %", "DAX_Formula": "DIVIDE([Mobility Applications], [Total Headcount], 0) * 100", "Category": "Mobility"},
        {"Measure_Name": "High Risk Count", "DAX_Formula": "CALCULATE(COUNT(Mobility_Risk[Risk_ID]), Mobility_Risk[Risk_Category] = \"High\")", "Category": "Risk"},
        {"Measure_Name": "Readiness Score Index", "DAX_Formula": "AVERAGE(Mobility_Risk[Readiness_Score])", "Category": "Readiness"}
    ]

    dax_df = pd.DataFrame(dax_measures)
    dax_df.to_csv(os.path.join(OUT_DIR, "dax_measures_reference.csv"), index=False)

    # Compute Actual Calculated Metric Values from Data
    emp = pd.read_csv(os.path.join(DATA_DIR, "Employee.csv"))
    perf = pd.read_csv(os.path.join(DATA_DIR, "Performance_Review.csv"))
    skills = pd.read_csv(os.path.join(DATA_DIR, "Skill_Assessment.csv"))
    trn = pd.read_csv(os.path.join(DATA_DIR, "Training.csv"))
    mob = pd.read_csv(os.path.join(DATA_DIR, "Mobility_Application.csv"))
    risk = pd.read_csv(os.path.join(DATA_DIR, "Mobility_Risk.csv"))

    val_headcount = len(emp)
    val_rating = perf["Rating"].mean()
    val_skill = skills["Proficiency_Score"].mean()
    val_trainings = len(trn)
    val_mob_apps = len(mob)
    val_readiness = risk["Readiness_Score"].mean()

    # Generate KPI Summary Card Plot
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis("off")

    card_text = f"""
    ========================================================================================
                               WORKFORCE PLANNING KPI DASHBOARD CARDS
    ========================================================================================
     [ TOTAL HEADCOUNT ]     [ AVG PERFORMANCE ]     [ AVG SKILL SCORE ]    [ READINESS INDEX ]
           {val_headcount}                {val_rating:.2f} / 5.0             {val_skill:.1f} / 100            {val_readiness:.1f} / 100
    ----------------------------------------------------------------------------------------
     [ TOTAL TRAININGS ]     [ MOBILITY APPLICATIONS ] [ MOBILITY RATE ]   [ ACTIVE DEPARTMENTS ]
           {val_trainings}                   {val_mob_apps}                 {(val_mob_apps/val_headcount)*100:.1f}%                {emp['Department'].nunique()}
    ========================================================================================
    """
    ax.text(0.5, 0.5, card_text, fontsize=10, family="monospace", va="center", ha="center",
            bbox=dict(boxstyle="round,pad=1", facecolor="aliceblue", edgecolor="navy"))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "kpi_card_summary.png"), dpi=150)
    plt.close()

    generate_reports(val_headcount, val_rating, val_skill, val_trainings, val_mob_apps, val_readiness, dax_df)
    print("Day 6 Workforce Planning KPI Dashboard completed successfully!")

def generate_reports(val_headcount, val_rating, val_skill, val_trainings, val_mob_apps, val_readiness, dax_df):
    # 1. Executive Dashboard Spec
    ed_doc = f"""# Day 6 Deliverable: Executive Dashboard Specification

## Executive Summary Visual Cards
- **Total Headcount**: {val_headcount}
- **Workforce Performance Rating**: {val_rating:.2f} / 5.0
- **Skill Proficiency Score**: {val_skill:.1f} / 100
- **Readiness Score Index**: {val_readiness:.1f} / 100
- **Total Completed Trainings**: {val_trainings}
- **Mobility Applications**: {val_mob_apps}

## Power BI Dashboard Layout
1. **Header Cards**: KPI metric summary cards formatted with conditional color indicators.
2. **Filters / Slicers**: Slicers for Department, Designation, and Skill Category.
3. **Executive Charts**:
   - Skill Gap by Department (Grouped Bar Chart)
   - Performance vs Readiness (Scatter Chart)
   - Upskilling Completion Trend (Line Chart)
"""
    with open(os.path.join(OUT_DIR, "Executive_Dashboard.md"), "w") as f:
        f.write(ed_doc)

    # 2. KPI Dashboard
    kd_doc = f"""# Day 6 Deliverable: KPI Dashboard Specification

## Power BI DAX Measures Reference
```
{dax_df.to_string(index=False)}
```

## Conditional Formatting Rules
- **Readiness Score >= 70**: Green (High Readiness)
- **Readiness Score 45 - 69**: Yellow (Moderate Readiness)
- **Readiness Score < 45**: Red (Skill Gap / High Risk)
"""
    with open(os.path.join(OUT_DIR, "KPI_Dashboard.md"), "w") as f:
        f.write(kd_doc)

    # 3. Dashboard Documentation
    dd_doc = """# Day 6 Deliverable: Dashboard Documentation

## Implementation & Navigation Guide
- Data Model Connection: DirectImport / Import mode linking 9 star-schema tables via `Employee_ID` and `Role_ID`.
- User Interactivity: Cross-filtering enabled between Department slicers and KPI summary visuals.
- Drill-Through: Click on any department bar to drill through to individual employee skill-gap profiles.
"""
    with open(os.path.join(OUT_DIR, "Dashboard_Documentation.md"), "w") as f:
        f.write(dd_doc)

if __name__ == "__main__":
    run_kpi_dashboard()
