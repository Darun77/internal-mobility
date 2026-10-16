# Day 6 Deliverable: KPI Dashboard Specification

## Power BI DAX Measures Reference
```
         Measure_Name                                                                     DAX_Formula       Category
      Total Headcount                                                    COUNT(Employee[Employee_ID]) Workforce Size
           Avg Rating                                             AVERAGE(Performance_Review[Rating])    Performance
      Avg Skill Score                                    AVERAGE(Skill_Assessment[Proficiency_Score])         Skills
      Total Trainings                                                    COUNT(Training[Training_ID])     Upskilling
Mobility Applications                                     COUNT(Mobility_Application[Application_ID])       Mobility
      Mobility Rate %                     DIVIDE([Mobility Applications], [Total Headcount], 0) * 100       Mobility
      High Risk Count CALCULATE(COUNT(Mobility_Risk[Risk_ID]), Mobility_Risk[Risk_Category] = "High")           Risk
Readiness Score Index                                         AVERAGE(Mobility_Risk[Readiness_Score])      Readiness
```

## Conditional Formatting Rules
- **Readiness Score >= 70**: Green (High Readiness)
- **Readiness Score 45 - 69**: Yellow (Moderate Readiness)
- **Readiness Score < 45**: Red (Skill Gap / High Risk)
