"""
Master Data Generator
======================
Generates realistic synthetic data for ALL 9 tables defined in the
Internal Mobility and Skill-Gap Analytics System problem statement:

  1. Employee
  2. Role
  3. Training
  4. Performance_Review
  5. Skill_Assessment
  6. Mobility_Application
  7. Open_Position
  8. Manager
  9. Mobility_Risk

All tables are linked primarily through Employee_ID (and Role_ID where
relevant), matching the multi-table schema described in the problem
statement PDF. Run this once to populate shared_data/, then each
Day-folder copies the subset of tables it needs.

Usage:
    python generate_master_data.py
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

np.random.seed(42)

N_EMPLOYEES = 600
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

DEPARTMENTS = ["Engineering", "Sales", "Marketing", "Finance", "HR",
               "Operations", "Customer Support", "Product", "Data & Analytics", "Legal"]

DESIGNATIONS = ["Associate", "Senior Associate", "Team Lead", "Manager",
                "Senior Manager", "Director"]

ROLE_TITLES = ["Data Analyst", "Software Engineer", "Sales Executive",
               "Marketing Specialist", "Financial Analyst", "HR Business Partner",
               "Operations Manager", "Product Manager", "Business Analyst",
               "DevOps Engineer", "Customer Success Manager", "Legal Counsel"]

SKILLS_POOL = ["Python", "SQL", "Power BI", "Excel", "Communication",
               "Leadership", "Data Modelling", "Machine Learning", "Cloud Computing",
               "Negotiation", "Project Management", "Stakeholder Management",
               "Statistics", "Domain Knowledge", "Agile/Scrum"]

COURSES = ["Advanced SQL", "Python for Data Science", "Power BI Mastery",
           "Leadership Essentials", "Effective Communication", "ML Foundations",
           "Cloud Fundamentals", "Agile Practices", "Negotiation Skills",
           "Project Management Professional", "Excel Advanced Analytics",
           "Stakeholder Management 101"]

RISK_CATEGORIES = ["Low", "Medium", "High"]
APPLICATION_STATUS = ["Applied", "Under Review", "Shortlisted", "Rejected", "Selected"]


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=np.random.randint(0, max(delta.days, 1)))


def main():
    today = datetime(2026, 8, 6)
    hire_start = datetime(2016, 1, 1)

    # ---------------------------------------------------------------
    # 1. Employee table
    # ---------------------------------------------------------------
    employee_ids = [f"EMP{str(i).zfill(4)}" for i in range(1, N_EMPLOYEES + 1)]
    employees = pd.DataFrame({
        "Employee_ID": employee_ids,
        "Employee_Name": [f"Employee_{i}" for i in range(1, N_EMPLOYEES + 1)],
        "Department": np.random.choice(DEPARTMENTS, N_EMPLOYEES),
        "Designation": np.random.choice(DESIGNATIONS, N_EMPLOYEES,
                                         p=[0.30, 0.25, 0.20, 0.15, 0.07, 0.03]),
        "Join_Date": [random_date(hire_start, today - timedelta(days=30)) for _ in range(N_EMPLOYEES)],
    })
    employees["Join_Date"] = employees["Join_Date"].dt.strftime("%Y-%m-%d")

    # ---------------------------------------------------------------
    # 2. Manager table
    # ---------------------------------------------------------------
    managers = []
    mid = 1
    for dept in DEPARTMENTS:
        for _ in range(np.random.randint(2, 4)):
            managers.append({
                "Manager_ID": f"MGR{str(mid).zfill(3)}",
                "Manager_Name": f"Manager_{mid}",
                "Department": dept
            })
            mid += 1
    managers = pd.DataFrame(managers)

    # ---------------------------------------------------------------
    # 3. Role table
    # ---------------------------------------------------------------
    roles = []
    rid = 1
    for dept in DEPARTMENTS:
        n_roles = np.random.randint(2, 4)
        for _ in range(n_roles):
            title = np.random.choice(ROLE_TITLES)
            req_skills = ", ".join(np.random.choice(SKILLS_POOL, size=np.random.randint(2, 5), replace=False))
            roles.append({
                "Role_ID": f"ROLE{str(rid).zfill(3)}",
                "Role_Title": title,
                "Department": dept,
                "Required_Skills": req_skills
            })
            rid += 1
    roles = pd.DataFrame(roles)

    # ---------------------------------------------------------------
    # 4. Open_Position table
    # ---------------------------------------------------------------
    open_positions = []
    pid = 1
    n_open = int(len(roles) * 0.6)
    for _, r in roles.sample(n_open, random_state=1).iterrows():
        open_positions.append({
            "Position_ID": f"POS{str(pid).zfill(3)}",
            "Role_ID": r["Role_ID"],
            "Department": r["Department"],
            "Open_Date": random_date(today - timedelta(days=180), today).strftime("%Y-%m-%d")
        })
        pid += 1
    open_positions = pd.DataFrame(open_positions)

    # ---------------------------------------------------------------
    # 5. Training table (multiple trainings per employee)
    # ---------------------------------------------------------------
    training_rows = []
    tid = 1
    for emp in employee_ids:
        n_trainings = np.random.poisson(2.2)
        for _ in range(n_trainings):
            training_rows.append({
                "Training_ID": f"TRN{str(tid).zfill(5)}",
                "Employee_ID": emp,
                "Course_Name": np.random.choice(COURSES),
                "Completion_Date": random_date(hire_start, today).strftime("%Y-%m-%d")
            })
            tid += 1
    training = pd.DataFrame(training_rows)

    # ---------------------------------------------------------------
    # 6. Performance_Review table (yearly reviews per employee)
    # ---------------------------------------------------------------
    perf_rows = []
    rvid = 1
    for emp in employee_ids:
        n_reviews = np.random.randint(1, 4)
        base_rating = np.random.normal(3.4, 0.7)
        for _ in range(n_reviews):
            rating = np.clip(base_rating + np.random.normal(0, 0.4), 1, 5)
            perf_rows.append({
                "Review_ID": f"REV{str(rvid).zfill(5)}",
                "Employee_ID": emp,
                "Review_Date": random_date(hire_start, today).strftime("%Y-%m-%d"),
                "Rating": round(rating, 1)
            })
            rvid += 1
    performance_review = pd.DataFrame(perf_rows)

    # ---------------------------------------------------------------
    # 7. Skill_Assessment table (multiple skills per employee)
    # ---------------------------------------------------------------
    skill_rows = []
    aid = 1
    for emp in employee_ids:
        n_skills = np.random.randint(3, 7)
        chosen_skills = np.random.choice(SKILLS_POOL, size=n_skills, replace=False)
        for sk in chosen_skills:
            skill_rows.append({
                "Assessment_ID": f"ASM{str(aid).zfill(5)}",
                "Employee_ID": emp,
                "Skill_Name": sk,
                "Proficiency_Score": int(np.clip(np.random.normal(65, 20), 5, 100))
            })
            aid += 1
    skill_assessment = pd.DataFrame(skill_rows)

    # ---------------------------------------------------------------
    # 8. Mobility_Application table
    # ---------------------------------------------------------------
    mobility_app_rows = []
    apid = 1
    applicants = np.random.choice(employee_ids, size=int(N_EMPLOYEES * 0.4), replace=False)
    for emp in applicants:
        role = roles.sample(1).iloc[0]
        mobility_app_rows.append({
            "Application_ID": f"APP{str(apid).zfill(4)}",
            "Employee_ID": emp,
            "Role_ID": role["Role_ID"],
            "Application_Date": random_date(today - timedelta(days=365), today).strftime("%Y-%m-%d"),
            "Status": np.random.choice(APPLICATION_STATUS, p=[0.15, 0.20, 0.25, 0.25, 0.15])
        })
        apid += 1
    mobility_application = pd.DataFrame(mobility_app_rows)

    # ---------------------------------------------------------------
    # 9. Mobility_Risk table (readiness score + risk category per employee)
    #    Built from a weighted combination of avg proficiency, avg rating,
    #    and training count so downstream ML tasks have realistic signal.
    # ---------------------------------------------------------------
    avg_prof = skill_assessment.groupby("Employee_ID")["Proficiency_Score"].mean()
    avg_rating = performance_review.groupby("Employee_ID")["Rating"].mean()
    train_count = training.groupby("Employee_ID").size()

    risk_rows = []
    for i, emp in enumerate(employee_ids):
        prof = avg_prof.get(emp, 50)
        rating = avg_rating.get(emp, 3.0)
        tcount = train_count.get(emp, 0)

        # Weighted readiness score (0-100), plus noise for realism
        readiness = (0.45 * prof) + (0.35 * (rating / 5 * 100)) + (0.20 * min(tcount, 5) / 5 * 100)
        readiness = np.clip(readiness + np.random.normal(0, 6), 0, 100)

        if readiness >= 70:
            category = "Low"
        elif readiness >= 45:
            category = "Medium"
        else:
            category = "High"

        # inject a small number of anomalous records (data-entry errors /
        # genuinely abnormal patterns) for the Day 5 anomaly detection task
        if np.random.rand() < 0.04:
            readiness = np.random.choice([np.random.uniform(0, 5), np.random.uniform(95, 100)])
            category = "High" if readiness < 50 else "Low"

        risk_rows.append({
            "Risk_ID": f"RSK{str(i+1).zfill(4)}",
            "Employee_ID": emp,
            "Score_Date": today.strftime("%Y-%m-%d"),
            "Readiness_Score": round(readiness, 1),
            "Risk_Category": category
        })
    mobility_risk = pd.DataFrame(risk_rows)

    # ---------------------------------------------------------------
    # Save all tables
    # ---------------------------------------------------------------
    tables = {
        "Employee": employees,
        "Manager": managers,
        "Role": roles,
        "Open_Position": open_positions,
        "Training": training,
        "Performance_Review": performance_review,
        "Skill_Assessment": skill_assessment,
        "Mobility_Application": mobility_application,
        "Mobility_Risk": mobility_risk,
    }

    for name, df in tables.items():
        path = os.path.join(OUT_DIR, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"Saved {name}.csv -> {len(df)} rows")

    print("\nAll 9 tables generated successfully in:", OUT_DIR)


if __name__ == "__main__":
    main()
