# Day 3 Deliverable: Cluster Analysis Report

## Method & Algorithm
- **Algorithm**: K-Means Clustering
- **Feature Normalization**: StandardScaler (Z-Score scaling)
- **Features Used**: Tenure_Years, Avg_Proficiency, Skill_Count, Training_Count, Avg_Rating
- **Dimensionality Reduction**: Principal Component Analysis (PCA 2D) for visual mapping
- **Silhouette Scores by K**: {2: 0.165, 3: 0.148, 4: 0.155, 5: 0.162, 6: 0.164}

## Optimal Cluster Selection
- Evaluated K ranging from 2 to 6 clusters using WCSS (Inertia) and Silhouette Scores.
- **K = 4** selected as optimal balance between statistical cluster compactness and actionable HR business interpretation.

## Cluster Profile Matrix

```
         Tenure_Years  Avg_Proficiency  Skill_Count  Training_Count  Avg_Rating                                Segment
Cluster                                                                                                               
0            3.872056        71.849776     3.684564        1.838926    3.065884             Steady / Stable Performers
1            2.762770        60.828238     5.331210        1.847134    3.765817     Early Career - Actively Upskilling
2            8.162231        59.077405     4.020134        1.718121    3.659843  Skill Gap - Needs Targeted Upskilling
3            6.911733        65.456207     5.289655        3.531034    3.131264             Steady / Stable Performers
```
