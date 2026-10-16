# Internal Mobility and Skill-Gap Analytics System

This repository provides a complete end-to-end implementation of the **Internal Mobility and Skill-Gap Analytics System using Employee, Training, and Role Data** as specified in the project roadmap.

## 9-Day Analytics Suite Overview

| Folder | Day | Analytics / ML Task | Primary Deliverables & Outputs |
|---|---|---|---|
| [`Day1_Problem_Understanding_ETL/`](file:///Users/darunkumaran/Downloads/project/Day1_Problem_Understanding_ETL) | **Day 1** | **Data Integration & ETL** | `Problem_Statement_Document.md`, `Data_Dictionary_Data_Modelling.md`, `Schema_Diagram.md`, `Power_Query_ETL_Documentation.md`, Clean Datasets |
| [`Day2_Exploratory_Data_Analysis/`](file:///Users/darunkumaran/Downloads/project/Day2_Exploratory_Data_Analysis) | **Day 2** | **Exploratory Data Analysis (EDA)** | `EDA_Report.md`, `descriptive_statistics.csv`, Histograms, Box Plots, Scatter Plots, Heatmap, Correlation Matrix |
| [`Day3_Employee_Segmentation/`](file:///Users/darunkumaran/Downloads/project/Day3_Employee_Segmentation) | **Day 3** | **K-Means Clustering** | `Cluster_Analysis_Report.md`, `Employee_Segmentation_Report.md`, `employee_segments.csv`, Elbow Plot, PCA Cluster Scatter |
| [`Day4_Workforce_Planning_Performance/`](file:///Users/darunkumaran/Downloads/project/Day4_Workforce_Planning_Performance) | **Day 4** | **Workforce Performance Analysis** | `Performance_Dashboard.md`, `KPI_Report.md`, `Analytical_Summary.md`, `kpi_metrics.csv`, Performance Trends Plot |
| [`Day5_SkillGap_Anomaly_Detection/`](file:///Users/darunkumaran/Downloads/project/Day5_SkillGap_Anomaly_Detection) | **Day 5** | **Isolation Forest Anomaly Detection** | `Monitoring_Dashboard.md`, `Analytics_Dashboard.md`, `Risk_Assessment_Report.md`, `anomaly_flags.csv`, `anomaly_alerts.csv` |
| [`Day6_Workforce_Planning_KPI_Dashboard/`](file:///Users/darunkumaran/Downloads/project/Day6_Workforce_Planning_KPI_Dashboard) | **Day 6** | **KPI Dashboard & DAX Measures** | `Executive_Dashboard.md`, `KPI_Dashboard.md`, `Dashboard_Documentation.md`, `dax_measures_reference.csv`, KPI Summary Cards |
| [`Day7_Interactive_Dashboard_Development/`](file:///Users/darunkumaran/Downloads/project/Day7_Interactive_Dashboard_Development) | **Day 7** | **Interactive Dashboard Flow** | `Complete_Interactive_Dashboard_Spec.md`, `Dashboard_Navigation_Flow.md`, Navigation Diagram, Interactive Summary CSV |
| [`Day8_Mobility_Readiness_Prediction/`](file:///Users/darunkumaran/Downloads/project/Day8_Mobility_Readiness_Prediction) | **Day 8** | **Random Forest Readiness ML Model** | `Prediction_Report.md`, `Model_Comparison_Report.md`, `mobility_readiness_predictions.csv`, Feature Importance, Confusion Matrix |
| [`Day9_Smart_Workforce_Planning_Insights/`](file:///Users/darunkumaran/Downloads/project/Day9_Smart_Workforce_Planning_Insights) | **Day 9** | **AI Recommendation System** | `AI_Recommendation_Dashboard.md`, `Final_Power_BI_Dashboard_Spec.md`, `Project_Report.md`, `Project_Presentation.md`, `role_matching_recommendations.csv` |

---

## Shared Master Data Schema

Synthetically generated realistic multi-table relational schema containing **600 employees** across 9 linked tables in `shared_data/`:
1. `Employee.csv`
2. `Manager.csv`
3. `Role.csv`
4. `Open_Position.csv`
5. `Training.csv`
6. `Performance_Review.csv`
7. `Skill_Assessment.csv`
8. `Mobility_Application.csv`
9. `Mobility_Risk.csv`

---

## How to Run Master Trial Run

To execute the trial run across all 9 days sequentially and verify 100% deliverable generation with zero errors:

```bash
python3 run_all_days.py
```

Each stage operates on a self-contained local copy of its required `data/` tables and outputs all generated reports, CSV datasets, and PNG plots into its local `outputs/` directory.
