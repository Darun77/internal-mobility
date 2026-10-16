# Day 5 — Skill-Gap Risk & Anomaly Detection

**Problem-statement objective:** *"Identify skill-gap and attrition
risks and abnormal patterns using training and performance and
monitoring data"* and *"Detect abnormal skill-gap and attrition-risk
patterns early."*

## ML Algorithm
**Isolation Forest** (unsupervised anomaly detection) — trained to
isolate employees whose feature pattern deviates from the general
population, with a **Z-score baseline** computed alongside it so HR
gets a transparent, explainable secondary signal.

## Features engineered per employee
| Feature | Source | Meaning |
|---|---|---|
| `Avg_Proficiency`, `Proficiency_Std` | Skill_Assessment | skill level & consistency |
| `Training_Count` | Training | upskilling activity |
| `Avg_Rating`, `Rating_Std` | Performance_Review | performance level & consistency |
| `Readiness_Score` | Mobility_Risk | existing HR-computed readiness signal |

## How to run
```bash
pip install pandas numpy scikit-learn matplotlib
python anomaly_detection.py
```

## Outputs (in `outputs/`)
- **`anomaly_flags.csv`** — every employee with `Is_Anomaly` (0/1), `Anomaly_Score`, and `Max_Zscore`
- **`anomaly_alerts.csv`** — just the flagged employees, sorted by severity (`Severity_Rank` = anomaly score × risk-category weight) — this is the actionable **alert list**
- **`anomaly_scatter.png`** — visualization of flagged vs normal employees (proficiency vs readiness)
- **`risk_assessment_report.md`** — short written summary of findings and recommended next steps

## How to read the results
Start with `anomaly_alerts.csv`, sorted highest severity first. A
"High" risk category combined with a high anomaly score is the
strongest signal (e.g. an employee with strong proficiency but a very
low readiness score — a mismatch worth investigating). Cross-check
flagged records against recent manager feedback before acting, since
some flags will simply reflect data-entry inconsistencies rather than
genuine risk.
