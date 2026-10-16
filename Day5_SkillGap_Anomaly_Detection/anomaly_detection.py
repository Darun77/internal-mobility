"""
DAY 5 - SKILL-GAP RISK & ANOMALY DETECTION
============================================
Learning Outcome (from problem statement):
    Identify skill-gap and attrition risks and abnormal patterns using
    training, performance, and monitoring data.

ML Algorithm Used: Isolation Forest (unsupervised anomaly detection)
Also demonstrates: Z-score based statistical outlier check as a
cross-validation baseline against the ML model, and alert generation.

Deliverables Generated:
    1. Monitoring Dashboard (Monitoring_Dashboard.md)
    2. Analytics Dashboard (Analytics_Dashboard.md)
    3. Risk Assessment Report (Risk_Assessment_Report.md)
    4. Anomaly Flags Master (anomaly_flags.csv)
    5. Severity Alert List (anomaly_alerts.csv)
    6. Anomaly Detection Scatter Plot (anomaly_scatter.png)
"""

import os
import shutil
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SHARED_DATA_DIR = os.path.join(PROJECT_ROOT, "shared_data")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

TABLE_NAMES = [
    "Employee", "Training", "Performance_Review",
    "Skill_Assessment", "Mobility_Risk"
]

def sync_data():
    for tbl in TABLE_NAMES:
        src = os.path.join(SHARED_DATA_DIR, f"{tbl}.csv")
        dst = os.path.join(DATA_DIR, f"{tbl}.csv")
        if os.path.exists(src):
            shutil.copy(src, dst)

def load_data():
    sync_data()
    employee = pd.read_csv(os.path.join(DATA_DIR, "Employee.csv"))
    training = pd.read_csv(os.path.join(DATA_DIR, "Training.csv"))
    performance = pd.read_csv(os.path.join(DATA_DIR, "Performance_Review.csv"))
    skills = pd.read_csv(os.path.join(DATA_DIR, "Skill_Assessment.csv"))
    risk = pd.read_csv(os.path.join(DATA_DIR, "Mobility_Risk.csv"))
    return employee, training, performance, skills, risk

def engineer_features(employee, training, performance, skills, risk):
    skill_agg = skills.groupby("Employee_ID").agg(
        Avg_Proficiency=("Proficiency_Score", "mean"),
        Proficiency_Std=("Proficiency_Score", "std")
    ).reset_index()
    skill_agg["Proficiency_Std"] = skill_agg["Proficiency_Std"].fillna(0)

    train_agg = training.groupby("Employee_ID").size().reset_index(name="Training_Count")

    perf_agg = performance.groupby("Employee_ID").agg(
        Avg_Rating=("Rating", "mean"),
        Rating_Std=("Rating", "std")
    ).reset_index()
    perf_agg["Rating_Std"] = perf_agg["Rating_Std"].fillna(0)

    df = employee[["Employee_ID", "Employee_Name", "Department", "Designation"]] \
        .merge(skill_agg, on="Employee_ID", how="left") \
        .merge(train_agg, on="Employee_ID", how="left") \
        .merge(perf_agg, on="Employee_ID", how="left") \
        .merge(risk[["Employee_ID", "Readiness_Score", "Risk_Category"]], on="Employee_ID", how="left")

    df = df.fillna(0)
    return df

def main():
    print("=== Running Day 5 Skill-Gap Risk & Anomaly Detection ===")
    employee, training, performance, skills, risk = load_data()
    df = engineer_features(employee, training, performance, skills, risk)

    feature_cols = ["Avg_Proficiency", "Proficiency_Std", "Training_Count",
                     "Avg_Rating", "Rating_Std", "Readiness_Score"]
    X = df[feature_cols].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Isolation Forest model
    iso = IsolationForest(
        n_estimators=200,
        contamination=0.06,
        random_state=42
    )
    df["Anomaly_Flag"] = iso.fit_predict(X_scaled)
    df["Anomaly_Score"] = -iso.score_samples(X_scaled)
    df["Is_Anomaly"] = (df["Anomaly_Flag"] == -1).astype(int)

    # Z-score statistical baseline
    z = np.abs((X - X.mean(axis=0)) / (X.std(axis=0) + 1e-9))
    df["Max_Zscore"] = z.max(axis=1).round(2)

    severity_map = {"High": 3, "Medium": 2, "Low": 1}
    df["Risk_Weight"] = df["Risk_Category"].map(severity_map).fillna(1)
    df["Severity_Rank"] = df["Anomaly_Score"] * df["Risk_Weight"]

    df.round(2).to_csv(os.path.join(OUT_DIR, "anomaly_flags.csv"), index=False)

    alerts = df[df["Is_Anomaly"] == 1].sort_values("Severity_Rank", ascending=False)
    alerts_out_cols = ["Employee_ID", "Employee_Name", "Department", "Designation",
                        "Avg_Proficiency", "Avg_Rating", "Training_Count",
                        "Readiness_Score", "Risk_Category", "Anomaly_Score", "Max_Zscore"]
    alerts[alerts_out_cols].round(2).to_csv(os.path.join(OUT_DIR, "anomaly_alerts.csv"), index=False)

    # Visualization
    plt.figure(figsize=(8, 6))
    normal = df[df["Is_Anomaly"] == 0]
    anomalous = df[df["Is_Anomaly"] == 1]
    plt.scatter(normal["Avg_Proficiency"], normal["Readiness_Score"],
                alpha=0.4, s=20, label="Normal", color="steelblue")
    plt.scatter(anomalous["Avg_Proficiency"], anomalous["Readiness_Score"],
                alpha=0.9, s=45, label="Anomaly (flagged)", color="crimson", edgecolor="black")
    plt.xlabel("Average Skill Proficiency")
    plt.ylabel("Mobility Readiness Score")
    plt.title("Skill-Gap / Attrition Risk Anomaly Detection (Isolation Forest)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(os.path.join(OUT_DIR, "anomaly_scatter.png"), dpi=150, bbox_inches="tight")
    plt.close()

    generate_reports(df, alerts)
    print(f"Flagged {len(alerts)} / {len(df)} employees as anomalous.")
    print("Day 5 Skill-Gap Risk & Anomaly Detection completed successfully!")

def generate_reports(df, alerts):
    n_total = len(df)
    n_anom = len(alerts)
    dept_breakdown = alerts["Department"].value_counts().to_dict()

    # 1. Monitoring Dashboard Spec
    md_doc = f"""# Day 5 Deliverable: Monitoring Dashboard Specification

## Active Anomaly Monitoring Console
- **Total Population Evaluated**: {n_total}
- **Active Anomaly Flags**: {n_anom} ({n_anom/n_total:.1%})
- **Top Affected Department**: {max(dept_breakdown, key=dept_breakdown.get) if dept_breakdown else 'N/A'}

## Operational Alert Rules
1. **Critical Skill Decay**: Proficiency score dropping > 25% below department mean.
2. **Mobility Mismatch**: Readiness score < 40 despite rating >= 4.0.
3. **Training Stagnation**: 0 completed trainings in 12+ months for senior designations.
"""
    with open(os.path.join(OUT_DIR, "Monitoring_Dashboard.md"), "w") as f:
        f.write(md_doc)

    # 2. Analytics Dashboard Spec
    ad_doc = f"""# Day 5 Deliverable: Analytics Dashboard Specification

## Anomaly Distribution Analytics
- **Algorithm**: Isolation Forest (Contamination = 6%)
- **Department Anomaly Distribution**:
{pd.DataFrame(list(dept_breakdown.items()), columns=['Department', 'Flagged_Count']).to_string(index=False)}

## Diagnostic Charts Included
- **Anomaly Scatter Matrix**: Proficiency Score vs Readiness Index.
- **Z-Score Cross Check**: Statistical baseline highlighting severe standard deviation spikes.
"""
    with open(os.path.join(OUT_DIR, "Analytics_Dashboard.md"), "w") as f:
        f.write(ad_doc)

    # 3. Risk Assessment Report
    rar_doc = f"""# Day 5 Deliverable: Risk Assessment Report

## Executive Summary
Using an **Isolation Forest ML model**, {n_anom} employees were flagged with abnormal skill/training/performance patterns that represent attrition risk or internal mobility misalignment.

## Flagged Anomalies Breakdown by Department
{pd.DataFrame(list(dept_breakdown.items()), columns=['Department', 'Anomalies']).to_string(index=False)}

## Recommended Mitigation Actions
1. HRBPs should conduct proactive one-on-one reviews for high-severity anomaly alerts.
2. L&D to re-evaluate upskilling course assignments for skill-gap flagged employees.
"""
    with open(os.path.join(OUT_DIR, "Risk_Assessment_Report.md"), "w") as f:
        f.write(rar_doc)

if __name__ == "__main__":
    main()
