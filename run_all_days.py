"""
MASTER TRIAL RUNNER & VALIDATOR
===============================
Runs all 9 days sequentially for the Internal Mobility and Skill-Gap Analytics System.
Verifies clean execution with ZERO errors and validates generated deliverables.

Usage:
    python run_all_days.py
"""

import os
import sys
import subprocess
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DAY_STAGES = [
    {
        "Day": "Day 1",
        "Name": "Problem Understanding & Data Integration (ETL)",
        "Folder": "Day1_Problem_Understanding_ETL",
        "Script": "etl_pipeline.py",
        "Expected_Outputs": [
            "Problem_Statement_Document.md", "Data_Dictionary_Data_Modelling.md",
            "Schema_Diagram.md", "Power_Query_ETL_Documentation.md", "etl_validation_summary.csv"
        ]
    },
    {
        "Day": "Day 2",
        "Name": "Exploratory Data Analysis (EDA)",
        "Folder": "Day2_Exploratory_Data_Analysis",
        "Script": "eda_analysis.py",
        "Expected_Outputs": [
            "EDA_Report.md", "descriptive_statistics.csv", "histogram.png",
            "box_plot.png", "scatter_plot.png", "heat_map.png", "correlation_matrix.png"
        ]
    },
    {
        "Day": "Day 3",
        "Name": "Employee Segmentation",
        "Folder": "Day3_Employee_Segmentation",
        "Script": "employee_segmentation.py",
        "Expected_Outputs": [
            "Cluster_Analysis_Report.md", "Employee_Segmentation_Report.md",
            "employee_segments.csv", "cluster_profile_summary.csv",
            "elbow_method.png", "cluster_visualization.png"
        ]
    },
    {
        "Day": "Day 4",
        "Name": "Workforce Planning Performance Analysis",
        "Folder": "Day4_Workforce_Planning_Performance",
        "Script": "workforce_performance_analysis.py",
        "Expected_Outputs": [
            "Performance_Dashboard.md", "KPI_Report.md", "Analytical_Summary.md",
            "kpi_metrics.csv", "performance_trends.png"
        ]
    },
    {
        "Day": "Day 5",
        "Name": "Skill-Gap Risk & Anomaly Detection",
        "Folder": "Day5_SkillGap_Anomaly_Detection",
        "Script": "anomaly_detection.py",
        "Expected_Outputs": [
            "Monitoring_Dashboard.md", "Analytics_Dashboard.md", "Risk_Assessment_Report.md",
            "anomaly_flags.csv", "anomaly_alerts.csv", "anomaly_scatter.png"
        ]
    },
    {
        "Day": "Day 6",
        "Name": "Workforce Planning KPI Dashboard",
        "Folder": "Day6_Workforce_Planning_KPI_Dashboard",
        "Script": "kpi_dashboard_measures.py",
        "Expected_Outputs": [
            "Executive_Dashboard.md", "KPI_Dashboard.md", "Dashboard_Documentation.md",
            "dax_measures_reference.csv", "kpi_card_summary.png"
        ]
    },
    {
        "Day": "Day 7",
        "Name": "Interactive Dashboard Development",
        "Folder": "Day7_Interactive_Dashboard_Development",
        "Script": "interactive_dashboard_flow.py",
        "Expected_Outputs": [
            "Complete_Interactive_Dashboard_Spec.md", "Dashboard_Navigation_Flow.md",
            "interactive_dashboard_summary.csv", "navigation_flow_diagram.png"
        ]
    },
    {
        "Day": "Day 8",
        "Name": "Mobility-Readiness Prediction",
        "Folder": "Day8_Mobility_Readiness_Prediction",
        "Script": "mobility_readiness_prediction.py",
        "Expected_Outputs": [
            "Prediction_Report.md", "Model_Comparison_Report.md",
            "mobility_readiness_predictions.csv", "model_comparison_report.csv",
            "feature_importance.png", "confusion_matrix.png"
        ]
    },
    {
        "Day": "Day 9",
        "Name": "Smart Workforce Planning Insights & Recommendation System",
        "Folder": "Day9_Smart_Workforce_Planning_Insights",
        "Script": "recommendation_system.py",
        "Expected_Outputs": [
            "AI_Recommendation_Dashboard.md", "Final_Power_BI_Dashboard_Spec.md",
            "Project_Report.md", "Project_Presentation.md",
            "role_matching_recommendations.csv"
        ]
    }
]

def main():
    print("=" * 80)
    print("MASTER TRIAL RUN: Internal Mobility & Skill-Gap Analytics System (Day 1 - Day 9)")
    print("=" * 80)

    # 1. Generate fresh master data first
    print("\n[Step 0] Refreshing master data in shared_data/...")
    gen_script = os.path.join(PROJECT_ROOT, "shared_data", "generate_master_data.py")
    res_gen = subprocess.run([sys.executable, gen_script], capture_output=True, text=True)
    if res_gen.returncode != 0:
        print("CRITICAL ERROR generating master data:")
        print(res_gen.stderr)
        sys.exit(1)
    print("Master data refreshed successfully.\n")

    summary_results = []
    total_start = time.time()

    for stage in DAY_STAGES:
        day_tag = stage["Day"]
        name = stage["Name"]
        folder = os.path.join(PROJECT_ROOT, stage["Folder"])
        script_path = os.path.join(folder, stage["Script"])
        out_folder = os.path.join(folder, "outputs")

        print(f"[{day_tag}] Running {name}...")
        start_t = time.time()
        
        proc = subprocess.run([sys.executable, script_path], capture_output=True, text=True, cwd=PROJECT_ROOT)
        elapsed = time.time() - start_t

        status = "SUCCESS" if proc.returncode == 0 else "FAILED"
        
        # Verify outputs
        missing_files = []
        found_files = []
        for expected in stage["Expected_Outputs"]:
            f_path = os.path.join(out_folder, expected)
            if os.path.exists(f_path):
                found_files.append(expected)
            else:
                missing_files.append(expected)

        if missing_files or proc.returncode != 0:
            status = "FAILED / INCOMPLETE"

        summary_results.append({
            "Day": day_tag,
            "Stage": name,
            "Status": status,
            "Time_Sec": round(elapsed, 2),
            "Outputs_Verified": f"{len(found_files)}/{len(stage['Expected_Outputs'])}"
        })

        if status != "SUCCESS":
            print(f"   [ERROR] Output details for {day_tag}:")
            print("   STDOUT:", proc.stdout)
            print("   STDERR:", proc.stderr)
            if missing_files:
                print("   MISSING OUTPUT FILES:", missing_files)
        else:
            print(f"   [OK] Completed in {elapsed:.2f}s | Deliverables verified ({len(found_files)}/{len(stage['Expected_Outputs'])})")

    total_elapsed = time.time() - total_start

    print("\n" + "=" * 80)
    print("FINAL TRIAL RUN SUMMARY REPORT")
    print("=" * 80)
    import pandas as pd
    summary_df = pd.DataFrame(summary_results)
    print(summary_df.to_string(index=False))
    print(f"\nTotal Execution Time: {total_elapsed:.2f} seconds")

    failed_count = len([r for r in summary_results if "FAILED" in r["Status"]])
    if failed_count == 0:
        print("\nSUCCESS: All 9 Day Pipelines executed cleanly with ZERO errors and 100% verified deliverables!")
    else:
        print(f"\nWARNING: {failed_count} stage(s) failed or had missing outputs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
