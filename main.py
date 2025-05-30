# ============================
# PWDEJOB-RECOMENDING SYSTEM
# VERSION: 1.3.0
# Author: The Totemn
# ===========================

import pandas as pd
import numpy as np

# job = pd.read_csv("job_data_pwd.csv", na_values=['NA'], header=0)
# print("Columns after stripping:", job.columns.tolist())

# skills_and_category = pd.read_csv("skills_category_data.csv", na_values=['NA'], header=0)
# print(skills_and_category.head())
# print(job.head())

from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MultiLabelBinarizer

def prepare_model(csv_path="job_data_pwd.csv", num_iterations=5): # FOR DECISION TREE 
    df = pd.read_csv(csv_path)

    # Process skills into a single list column
    df['all_skills'] = df[['Skill 1', 'Skill 2', 'Skill 3', 'Skill 4', 'Skill 5']].apply(
        lambda row: [str(skill).strip().lower() for skill in row], axis=1
    )

    mlb = MultiLabelBinarizer()
    skill_matrix = mlb.fit_transform(df['all_skills'])

    # Create feature matrix
    X = np.hstack([
        skill_matrix,
        df[['Experience (Years)', 'PWD Friendly']].fillna(0).to_numpy()
    ])
    y = df['Title']

    # Train multiple models and keep the best one
    best_model = None
    best_score = 0

    for i in range(num_iterations):
        clf = DecisionTreeClassifier(max_depth=10)
        clf.fit(X, y)

        score = clf.score(X, y)
        # print(f"[D-TREE Training {i+1}] Accuracy: {score:.2f}")

        if score > best_score:
            best_score = score
            best_model = clf

    return best_model, mlb

def decision_tree_recommendation(user_skills, experience, is_pwd, clf, mlb):
    user_skills = [skill.strip().lower() for skill in user_skills]
    
    user_skill_vec = mlb.transform([user_skills])
    user_vector = np.hstack([user_skill_vec, [[experience, is_pwd]]])
    
    # Predict and sort
    probs = clf.predict_proba(user_vector)[0]
    job_probs = sorted(zip(clf.classes_, probs), key=lambda x: -x[1])
    
    return job_probs[:5] 
        
def contentBasedAlgo(user_skills, user_experience, user_has_disability, csv_path="job_data_pwd.csv"):
    # Load and convert jobs
    df = pd.read_csv(csv_path)
    jobs = df.to_dict(orient="records")

    # Filter jobs based on PWD-friendliness
    if user_has_disability:
        filtered_jobs = []
        for job in jobs:
            if job.get("PWD Friendly", 0) == 1:
                filtered_jobs.append(job)
    else:
        filtered_jobs = jobs

    # Prepare user skill set
    user_skills_set = set()
    for skill in user_skills:
        user_skills_set.add(skill.strip().lower())

    recommendations = []

    for job in filtered_jobs:
        # Check experience requirement
        job_experience_required = job.get("Experience (Years)", 0)

        if pd.isna(job_experience_required):
            job_experience_required = 0

        if user_experience < job_experience_required:
            continue  # Skip jobs that require more experience than the user has

        # Extract job skills
        job_skills = []
        for i in range(1, 6):
            skill = str(job.get(f"Skill {i}", "")).lower()
            if skill:
                job_skills.append(skill)

        job_skills_set = set(job_skills)

        # Calculate skill match score
        matched_skills_set = user_skills_set & job_skills_set
        matched_skills = len(matched_skills_set)

        if len(job_skills_set) > 0:
            skill_match_score = matched_skills / len(job_skills_set)
        else:
            skill_match_score = 0

        job_title = job.get("Title", "Unknown Job")
        recommendations.append((job_title, skill_match_score))

    # Sort results by skill match
    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations[:5]

def hybridRecos(user_skills, experience, is_pwd, user_history, interaction_matrix, min_common_skills=2):
    # Load all required data
    df = pd.read_csv("job_data_pwd_for_cola.csv")
    user_history_df = pd.read_csv("user_history.csv")
    jobs = df.to_dict(orient="records")
    
    # Convert user skills to lowercase for easy comparison
    user_skills_set = {skill.strip().lower() for skill in user_skills}
    
    # Get jobs that the selected user has applied to (applied = 1)
    user_history_jobs = user_history_df[
        (user_history_df['user id'] == user_history) & 
        (user_history_df['applied'] == 1)
    ]['job id'].tolist()
    
    # Get the skills from jobs in user history
    history_jobs = [job for job in jobs if job['Job ID'] in user_history_jobs]
    history_skills = set()
    for job in history_jobs:
        for i in range(1, 6):
            skill = str(job.get(f"Skill {i}", "")).lower()
            if skill:
                history_skills.add(skill)
    
    # Step 2: Find jobs that share skills with history jobs
    similar_jobs = []
    for job in jobs:
        # Skip if job requires more experience than user has
        if job.get("Experience (Years)", 0) > experience:
            continue
            
        # Skip if user is PWD but job is not PWD friendly
        if is_pwd and not job.get("PWD Friendly", 0):
            continue
            
        # Get job skills
        job_skills = set()
        for i in range(1, 6):
            skill = str(job.get(f"Skill {i}", "")).lower()
            if skill:
                job_skills.add(skill)
        
        # Count how many skills this job shares with history jobs
        common_skills = len(job_skills & history_skills)
        
        # If enough common skills, add to similar jobs
        if common_skills >= min_common_skills:
            similar_jobs.append((job, common_skills))
    
    # Content-based filtering - filter similar jobs based on user's skills
    final_recommendations = []
    for job, history_score in similar_jobs:
        # Get job skills
        job_skills = set()
        for i in range(1, 6):
            skill = str(job.get(f"Skill {i}", "")).lower()
            if skill:
                job_skills.add(skill)
        
        # Calculate how many of user's skills match this job
        user_skill_matches = len(user_skills_set & job_skills)
        
        # Calculate final score (weighted combination of history similarity and user skill match)
        if len(job_skills) > 0:
            skill_match_ratio = user_skill_matches / len(job_skills)
            # Normalize history score by dividing by the maximum possible common skills (5)
            normalized_history_score = history_score / 5.0
            final_score = (normalized_history_score * 0.2) + (skill_match_ratio * 0.8)  # Weighted combination
            final_recommendations.append((job['Title'], final_score))
    
    # Sort by final score and return top 5
    final_recommendations.sort(key=lambda x: x[1], reverse=True)
    return final_recommendations[:5]

clf, mlb = prepare_model("job_data_pwd.csv", num_iterations=5)

# === MAIN MENU ===
while True:
    print("\n====== PWDE JOB Job Recommending  ======")
    cmd = input("Type 'start' to get recommendations or 'exit' to quit: ").strip().lower()
    if cmd == 'exit':
        break
    elif cmd == 'start':
        name = input("Enter Your Name: ")
        print("")
        print("[1] - User 1(Admin Guy also lil bit random)\n[2] - User 2 (Real ass full blown jack of all trades random)\n[3] - User 3 (Blue collar guy manual labor jobs)")
        user_history = int(input("Enter the user history here: "))
        print("\n====== WHAT ARE YOUR 5 SKILLS ======")
        user_skills = [input(f"Skill {i+1}: ").strip() for i in range(5)]
        experience = int(input("How many years of experience do you have? "))
        is_pwd = int(input("Are you a PWD? (1 - yes | 0 - no): "))

        print("\n--- Content-Based Recommendation ---")
        content_recs = contentBasedAlgo(user_skills, experience, is_pwd == 1)
        for title, score in content_recs:
            print(f"{title:<30} Score: {score:.2f}")

        print("\n--- Decision Tree Model Recommendation ---")
        dt_recs = decision_tree_recommendation(user_skills, experience, is_pwd, clf, mlb)
        for title, prob in dt_recs:
            print(f"{title:<30} Score: {prob:.2f}")

        print("\n--- Hybrid Recommendation (Collaborative + Content-based) ---")
        hybrid_recs = hybridRecos(user_skills, experience, is_pwd, user_history, None)
        for title, score in hybrid_recs:
            print(f"{title:<30} Score: {score:.2f}")

