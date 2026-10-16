# Day 8 Deliverable: Mobility Readiness Prediction Report

## Executive Summary
Using supervised Machine Learning (Random Forest Classification & Regression), internal mobility readiness probability and readiness scores were predicted across **600 employees**.

## Top Mobility-Ready Talent (Highest Readiness Probability)
```
Employee_ID Employee_Name       Department      Designation  Predicted_Readiness_Score  Predicted_Readiness_Probability
    EMP0001    Employee_1 Customer Support        Team Lead                       69.1                            0.162
    EMP0002    Employee_2          Finance        Team Lead                       76.3                            0.654
    EMP0003    Employee_3          Product   Senior Manager                       57.2                            0.099
    EMP0004    Employee_4               HR        Associate                       60.7                            0.124
    EMP0005    Employee_5 Customer Support        Associate                       57.4                            0.020
    EMP0006    Employee_6            Legal   Senior Manager                       61.8                            0.115
    EMP0007    Employee_7        Marketing          Manager                       56.7                            0.073
    EMP0008    Employee_8 Customer Support Senior Associate                       59.0                            0.110
    EMP0009    Employee_9          Product        Team Lead                       64.8                            0.197
    EMP0010   Employee_10               HR        Associate                       58.2                            0.090
```

## Key Predictive Drivers
1. **Average Skill Proficiency Score**: Highest feature importance weight in predicting mobility readiness.
2. **Average Performance Rating**: Strong secondary predictor for role transfer eligibility.
3. **Training Completions**: Key catalyst for transition from Medium to Low risk categories.
