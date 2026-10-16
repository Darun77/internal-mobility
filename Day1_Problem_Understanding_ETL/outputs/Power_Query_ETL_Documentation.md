# Day 1 Deliverable: Power Query / Pandas ETL Documentation

## Step-by-Step ETL Transformation Pipeline

### 1. Data Ingestion & Source Connection
- Source datasets imported from CSV files into Pandas DataFrames / Power BI Data Model.
- Automated path handling and delimiter parsing applied.

### 2. Data Cleaning & Type Casting
- Trimmed whitespace across string columns (`Employee_ID`, `Department`, `Designation`, `Course_Name`, `Skill_Name`).
- Converted date columns (`Join_Date`, `Completion_Date`, `Review_Date`, `Application_Date`, `Open_Date`, `Score_Date`) into Standard ISO YYYY-MM-DD timestamps.
- Clipped numerical ranges (`Rating` between 1.0 and 5.0, `Proficiency_Score` between 0 and 100).

### 3. Duplicate Removal & Key Validation
- Deduplicated all primary keys (`Employee_ID`, `Role_ID`, `Training_ID`, `Review_ID`, `Assessment_ID`, `Application_ID`, `Position_ID`, `Risk_ID`).
- Verified zero nulls across mandatory primary key fields.

### 4. Integrity Validation Results

| Table | Rows | Nulls | PK | PK Unique |
|---|---|---|---|---|
| Employee | 600 | 0 | Employee_ID | True |
| Manager | 24 | 0 | Manager_ID | True |
| Role | 24 | 0 | Role_ID | True |
| Open_Position | 14 | 0 | Position_ID | True |
| Training | 1332 | 0 | Training_ID | True |
| Performance_Review | 1199 | 0 | Review_ID | True |
| Skill_Assessment | 2752 | 0 | Assessment_ID | True |
| Mobility_Application | 240 | 0 | Application_ID | True |
| Mobility_Risk | 600 | 0 | Risk_ID | True |

