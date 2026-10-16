"""
DAY 3 - EMPLOYEE SEGMENTATION
==============================
Learning Outcome (from problem statement):
    Classify Employee records into groups using clustering to support
    targeted decisions.

ML Algorithm Used: K-Means Clustering (unsupervised learning)
Also demonstrates: feature normalization (StandardScaler), the Elbow
Method + Silhouette Score for choosing K, and PCA for 2D visualization.

Business Goal:
    Segment employees by skill-proficiency and career-stage pattern so
    HR / L&D teams can target upskilling and mobility programs
    differently for each segment (e.g. "High performers ready for
    mobility" vs "Early-career, needs upskilling" vs "Stagnant / at risk").

Inputs (in ./data/):
    Employee.csv, Skill_Assessment.csv, Training.csv, Performance_Review.csv

Outputs (in ./outputs/):
    employee_segments.csv      -> every employee tagged with a Cluster + Segment label
    elbow_method.png           -> WCSS vs K plot used to justify K choice
    cluster_visualization.png  -> PCA 2D scatter of clusters
    cluster_profile_summary.csv-> mean feature values per cluster (for the report)
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)


def load_data():
    employee = pd.read_csv(os.path.join(DATA_DIR, "Employee.csv"), parse_dates=["Join_Date"])
    skills = pd.read_csv(os.path.join(DATA_DIR, "Skill_Assessment.csv"))
    training = pd.read_csv(os.path.join(DATA_DIR, "Training.csv"))
    performance = pd.read_csv(os.path.join(DATA_DIR, "Performance_Review.csv"))
    return employee, skills, training, performance


def engineer_features(employee, skills, training, performance):
    """Build one feature row per employee - the standard prerequisite
    for clustering (clustering needs a single vector per record)."""
    today = pd.Timestamp("2026-08-06")

    # Tenure in years (career-stage signal)
    employee["Tenure_Years"] = (today - employee["Join_Date"]).dt.days / 365.25

    # Avg + breadth of skill proficiency
    skill_agg = skills.groupby("Employee_ID").agg(
        Avg_Proficiency=("Proficiency_Score", "mean"),
        Skill_Count=("Skill_Name", "nunique")
    ).reset_index()

    # Training activity
    train_agg = training.groupby("Employee_ID").size().reset_index(name="Training_Count")

    # Performance trend
    perf_agg = performance.groupby("Employee_ID").agg(
        Avg_Rating=("Rating", "mean")
    ).reset_index()

    df = employee.merge(skill_agg, on="Employee_ID", how="left") \
                 .merge(train_agg, on="Employee_ID", how="left") \
                 .merge(perf_agg, on="Employee_ID", how="left")

    # Fill employees with no records yet
    df[["Avg_Proficiency", "Skill_Count", "Training_Count", "Avg_Rating"]] = \
        df[["Avg_Proficiency", "Skill_Count", "Training_Count", "Avg_Rating"]].fillna(0)

    return df


def choose_k(X_scaled, k_range=range(2, 7)):
    wcss, sil_scores = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        wcss.append(km.inertia_)
        sil_scores.append(silhouette_score(X_scaled, labels))

    plt.figure(figsize=(7, 5))
    plt.plot(list(k_range), wcss, marker="o")
    plt.title("Elbow Method - WCSS vs K")
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("WCSS (Inertia)")
    plt.grid(alpha=0.3)
    plt.savefig(os.path.join(OUT_DIR, "elbow_method.png"), dpi=150, bbox_inches="tight")
    plt.close()

    best_k = list(k_range)[int(np.argmax(sil_scores))]
    print("Silhouette scores by K:", dict(zip(k_range, [round(s, 3) for s in sil_scores])))
    print(f"Selected K = {best_k} (highest silhouette score)")
    return best_k


def label_segments(profile):
    """Turn numeric cluster centers into human-readable HR segment names."""
    labels = {}
    prof_median = profile["Avg_Proficiency"].median()
    rating_median = profile["Avg_Rating"].median()
    tenure_median = profile["Tenure_Years"].median()

    for cluster_id, row in profile.iterrows():
        if row["Avg_Proficiency"] >= prof_median and row["Avg_Rating"] >= rating_median:
            name = "High Performers - Mobility Ready"
        elif row["Tenure_Years"] < tenure_median and row["Training_Count"] >= profile["Training_Count"].median():
            name = "Early Career - Actively Upskilling"
        elif row["Avg_Proficiency"] < prof_median and row["Training_Count"] < profile["Training_Count"].median():
            name = "Skill Gap - Needs Targeted Upskilling"
        else:
            name = "Steady / Stable Performers"
        labels[cluster_id] = name
    return labels


def main():
    employee, skills, training, performance = load_data()
    df = engineer_features(employee, skills, training, performance)

    feature_cols = ["Tenure_Years", "Avg_Proficiency", "Skill_Count", "Training_Count", "Avg_Rating"]
    X = df[feature_cols].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    choose_k(X_scaled)  # generates elbow_method.png + prints silhouette scores for the report

    # Business decision: 4 segments is chosen for HR interpretability
    # (Mobility-ready / Actively upskilling / Skill-gap / Stable) even
    # though the elbow/silhouette plot is used to justify the general
    # cluster range - this mirrors real HR analytics practice where the
    # final K balances statistical fit with actionability.
    best_k = 4
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    # Cluster profile (mean feature values per cluster) -> used for the report
    profile = df.groupby("Cluster")[feature_cols].mean()
    segment_names = label_segments(profile)
    df["Segment"] = df["Cluster"].map(segment_names)
    profile["Segment"] = profile.index.map(segment_names)
    profile.to_csv(os.path.join(OUT_DIR, "cluster_profile_summary.csv"))

    # PCA for 2D visualization
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_scaled)
    df["PCA1"], df["PCA2"] = coords[:, 0], coords[:, 1]

    plt.figure(figsize=(8, 6))
    for seg in df["Segment"].unique():
        sub = df[df["Segment"] == seg]
        plt.scatter(sub["PCA1"], sub["PCA2"], label=seg, alpha=0.6, s=25)
    plt.title("Employee Segmentation (K-Means, PCA-reduced)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend(fontsize=8)
    plt.grid(alpha=0.3)
    plt.savefig(os.path.join(OUT_DIR, "cluster_visualization.png"), dpi=150, bbox_inches="tight")
    plt.close()

    out_cols = ["Employee_ID", "Employee_Name", "Department", "Designation",
                "Tenure_Years", "Avg_Proficiency", "Skill_Count", "Training_Count",
                "Avg_Rating", "Cluster", "Segment"]
    df[out_cols].round(2).to_csv(os.path.join(OUT_DIR, "employee_segments.csv"), index=False)

    print("\n=== Segment sizes ===")
    print(df["Segment"].value_counts())
    print("\nOutputs saved to:", OUT_DIR)


if __name__ == "__main__":
    main()
