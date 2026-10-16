# Day 3 — Employee Segmentation

**Problem-statement objective:** *"Classify Employee records into
groups using clustering to support targeted decisions"* and *"Segment
employees by skill-proficiency and career-stage pattern."*

## ML Algorithm
**K-Means Clustering** (unsupervised learning), with:
- **Elbow Method** (WCSS vs K) and **Silhouette Score** to statistically justify the cluster range
- **StandardScaler** to normalize features before distance-based clustering
- **PCA** to compress features to 2D for visualization

## Features engineered per employee
| Feature | Source | Meaning |
|---|---|---|
| `Tenure_Years` | Employee.Join_Date | career-stage signal |
| `Avg_Proficiency` | Skill_Assessment | overall skill level |
| `Skill_Count` | Skill_Assessment | breadth of skills assessed |
| `Training_Count` | Training | upskilling activity |
| `Avg_Rating` | Performance_Review | performance signal |

## How to run
```bash
pip install pandas numpy scikit-learn matplotlib
python employee_segmentation.py
```

## Outputs (in `outputs/`)
- **`employee_segments.csv`** — every employee tagged with `Cluster` and a readable `Segment` name (e.g. "High Performers - Mobility Ready", "Skill Gap - Needs Targeted Upskilling")
- **`elbow_method.png`** — WCSS vs K plot used to justify the chosen number of clusters
- **`cluster_visualization.png`** — PCA-reduced 2D scatter plot of the segments
- **`cluster_profile_summary.csv`** — mean feature values per cluster, for the write-up / report

## How to read the results
Each segment maps to a distinct HR action:
- **High Performers - Mobility Ready** → prioritize for open-role matching
- **Early Career - Actively Upskilling** → keep on current training track, revisit in 6–12 months
- **Skill Gap - Needs Targeted Upskilling** → route into L&D remediation programs
- **Steady / Stable Performers** → monitor, no urgent action needed

The exact segment count and labels can change slightly on real data —
re-run `employee_segmentation.py` and re-check `elbow_method.png` /
console silhouette scores if you swap in real company data.
