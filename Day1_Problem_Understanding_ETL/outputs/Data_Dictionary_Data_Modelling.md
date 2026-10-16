# Day 1 Deliverable: Data Dictionary & Data Modelling

## Data Model Architecture
The data model uses a standard star/snowflake schema with central dimension tables (`Employee`, `Role`, `Manager`) linked to transactional fact tables via `Employee_ID` and `Role_ID`.

## Schema Table Definitions

### 1. Employee (Dimension Table)
- `Employee_ID` (PK, String): Unique identifier (e.g. EMP0001)
- `Employee_Name` (String): Full name of employee
- `Department` (String): Department division
- `Designation` (String): Job title level (Associate to Director)
- `Join_Date` (Date): Organization hire date

### 2. Role (Dimension Table)
- `Role_ID` (PK, String): Unique role identifier
- `Role_Title` (String): Title of job role
- `Department` (String): Department where role exists
- `Required_Skills` (String): Comma-separated required skills

### 3. Manager (Dimension Table)
- `Manager_ID` (PK, String): Unique manager ID
- `Manager_Name` (String): Full name of manager
- `Department` (String): Department managed

### 4. Training (Fact Table)
- `Training_ID` (PK, String): Unique training record ID
- `Employee_ID` (FK, String): Target employee
- `Course_Name` (String): Completed course title
- `Completion_Date` (Date): Course completion timestamp

### 5. Performance_Review (Fact Table)
- `Review_ID` (PK, String): Unique review record ID
- `Employee_ID` (FK, String): Evaluated employee
- `Review_Date` (Date): Review execution date
- `Rating` (Float, 1.0 - 5.0): Numerical performance rating

### 6. Skill_Assessment (Fact Table)
- `Assessment_ID` (PK, String): Unique skill assessment ID
- `Employee_ID` (FK, String): Assessed employee
- `Skill_Name` (String): Name of technical/soft skill
- `Proficiency_Score` (Integer, 0 - 100): Evaluated skill proficiency score

### 7. Mobility_Application (Fact Table)
- `Application_ID` (PK, String): Unique internal application ID
- `Employee_ID` (FK, String): Applying employee
- `Role_ID` (FK, String): Target open role
- `Application_Date` (Date): Date submitted
- `Status` (String): Application status (Applied, Under Review, Shortlisted, Selected, Rejected)

### 8. Open_Position (Fact Table)
- `Position_ID` (PK, String): Unique position posting ID
- `Role_ID` (FK, String): Associated role template
- `Department` (String): Hiring department
- `Open_Date` (Date): Requisition creation date

### 9. Mobility_Risk (Fact Table)
- `Risk_ID` (PK, String): Unique risk record ID
- `Employee_ID` (FK, String): Evaluated employee
- `Score_Date` (Date): Evaluation date
- `Readiness_Score` (Float, 0 - 100): Calculated readiness score
- `Risk_Category` (String): Risk categorization (Low, Medium, High)
