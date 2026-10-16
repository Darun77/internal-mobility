# Day 8 — Mobility-Readiness Prediction

**Problem-statement objective:** *"Develop ML models to predict
internal-mobility readiness probability from historical data"* —
covering the day's activities: prepare training data, feature
engineering, train/compare models, evaluate performance, generate
forecasts.

## ML Algorithms
Both **classification** and **regression** are implemented, matching
the problem statement's requirement for "classification/regression
machine learning":

| Task | Main model | Baseline compared against |
|---|---|---|
| Predict `Risk_Category` (Low/Medium/High) + readiness **probability** | Random Forest Classifier | Logistic Regression |
| Predict continuous `Readiness_Score` | Random Forest Regressor | Linear Regression |

## Features engineered per employee
`Tenure_Years`, `Avg_Proficiency`, `Skill_Count`, `Avg_Rating`,
`Training_Count`, `Past_Applications` (from Mobility_Application) —
built from Employee, Skill_Assessment, Performance_Review, Training
and Mobility_Application, with `Mobility_Risk` used as the training
label source.

## How to run
```bash
pip install pandas numpy scikit-learn matplotlib
python mobility_readiness_prediction.py
```

## Outputs (in `outputs/`)
- **`mobility_readiness_predictions.csv`** — every employee with their `Predicted_Readiness_Probability` (0–1, probability of being mobility-ready / low risk), `Predicted_Risk_Category`, and `Predicted_Readiness_Score` — sorted highest-probability first. **This is the main deliverable HR would act on.**
- **`model_comparison_report.csv`** — Accuracy / F1 / Precision / Recall for the classifiers, and R² / MAE for the regressors, so you can see the main model beats the baseline (the "Model Comparison Report" deliverable).
- **`feature_importance.png`** — which features drive the prediction most (useful for the write-up/report and for HR to understand *why* someone is or isn't mobility-ready).
- **`confusion_matrix.png`** — detailed classifier performance breakdown by risk category.

## How to read the results
Sort `mobility_readiness_predictions.csv` by
`Predicted_Readiness_Probability` descending — the top rows are the
employees the model considers most ready for an internal move right
now. Compare `Readiness_Score` (actual, from HR's existing
Mobility_Risk table) against `Predicted_Readiness_Score` to sanity
check the model before trusting it on new employees who don't have a
Mobility_Risk record yet.
