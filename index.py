# import random
# import numpy as np
# from sklearn.preprocessing import MultiLabelBinarizer
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import f1_score

# # Step 1: Your job data
# jobs = [
#     {
#         "id": "job1", "title": "Frontend Developer",
#         "skills": ["JavaScript", "React", "CSS", "HTML"], "experience": 2
#     },
#     {
#         "id": "job2", "title": "Data Scientist",
#         "skills": ["Python", "Machine Learning", "Data Science", "Statistics"], "experience": 4
#     },
#     {
#         "id": "job3", "title": "Salesforce Administrator",
#         "skills": ["Salesforce", "CRM", "Excel"], "experience": 3
#     },
#     {
#         "id": "job4", "title": "Backend Developer",
#         "skills": ["Java", "Spring Boot", "AWS", "Microservices"], "experience": 5
#     },
#     {
#         "id": "job5", "title": "UI/UX Designer",
#         "skills": ["UI/UX Design", "Figma", "Prototyping"], "experience": 1
#     },
#     {
#         "id": "job6", "title": "DevOps Engineer",
#         "skills": ["Docker", "Kubernetes", "AWS", "CI/CD"], "experience": 3
#     },
#     {
#         "id": "job7", "title": "Mobile App Developer",
#         "skills": ["Flutter", "Dart", "Firebase"], "experience": 2
#     },
#     {
#         "id": "job8", "title": "Cybersecurity Analyst",
#         "skills": ["Cybersecurity", "Network Security", "Python", "SIEM"], "experience": 4
#     },
#     {
#         "id": "job9", "title": "AI Researcher",
#         "skills": ["Deep Learning", "Python", "TensorFlow", "Research"], "experience": 5
#     },
#     {
#         "id": "job10", "title": "Product Manager",
#         "skills": ["Product Management", "Agile", "JIRA", "Communication"], "experience": 3
#     }
# ]

# all_skills = list(set(skill for job in jobs for skill in job["skills"]))
# job_titles = [job["title"] for job in jobs]

# # Step 2: Simulate users
# def generate_user_data(num_users=100):
#     user_data = []
#     for _ in range(num_users):
#         job = random.choice(jobs)
#         job_skills = job["skills"]
#         num_skills = random.randint(2, len(job_skills))
#         user_skills = random.sample(job_skills, num_skills)
#         experience = job["experience"] + random.choice([-1, 0, 1])
#         experience = max(0, experience)  # no negative experience
#         user_data.append({
#             "skills": user_skills,
#             "experience": experience,
#             "job_title": job["title"]
#         })
#     return user_data

# users = generate_user_data()

# # Step 3: Encode skills and experience
# mlb = MultiLabelBinarizer()
# X_skills = mlb.fit_transform([u["skills"] for u in users])
# X_exp = np.array([[u["experience"]] for u in users])
# X = np.hstack((X_skills, X_exp))
# y = [u["job_title"] for u in users]

# # Step 4: Train/test split and train model
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# clf = DecisionTreeClassifier()
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)

# # Step 5: Evaluate
# score = f1_score(y_test, y_pred, average='macro')
# print(f"F1 Score: {score:.2f}")

# # Step 6: Recommend a job
# new_user_skills = ["Python", "CSS", "Statistics"]
# new_user_experience = 3

# user_vec = mlb.transform([new_user_skills])
# user_input = np.hstack((user_vec, [[new_user_experience]]))
# predicted_job = clf.predict(user_input)[0]

# print("Recommended Job:", predicted_job)

# Sample extended job data
jobs = [
    {"title": "Frontend Developer", "skills": ["JavaScript", "CSS", "HTML"], "job_type": "full-time", "disability_friendly": True},
    {"title": "Admin Assistant", "skills": ["Excel", "CSS", "Admin Systems"], "job_type": "part-time", "disability_friendly": True},
    {"title": "Data Entry Clerk", "skills": ["Typing", "Excel", "CRM"], "job_type": "remote", "disability_friendly": False},
    {"title": "Junior Web Developer", "skills": ["JavaScript", "HTML", "Typing"], "job_type": "part-time", "disability_friendly": True},
    {"title": "Graphic Designer", "skills": ["Photoshop", "Figma", "Creativity"], "job_type": "full-time", "disability_friendly": True},
    {"title": "Marketing Assistant", "skills": ["Social Media", "Copywriting", "Excel"], "job_type": "part-time", "disability_friendly": False},
    {"title": "Content Writer", "skills": ["Writing", "SEO", "Research"], "job_type": "remote", "disability_friendly": True},
    {"title": "Customer Support Agent", "skills": ["Communication", "Typing", "CRM"], "job_type": "full-time", "disability_friendly": True},
    {"title": "Product Tester", "skills": ["Detail-Oriented", "Typing", "Documentation"], "job_type": "part-time", "disability_friendly": True},
    {"title": "Project Coordinator", "skills": ["Organization", "Excel", "Communication"], "job_type": "remote", "disability_friendly": False}
]

# User input
user_skills = ["CSS", "Organization", "Excel"]
user_job_type = "part-time"
user_has_disability = True  # Set False if no disability

# Step 1: Filter jobs by disability
if user_has_disability:
    filtered_jobs = [job for job in jobs if job["disability_friendly"]]
else:
    filtered_jobs = jobs[:]  # all jobs included

# Step 2: Calculate skill matching and job type matching
recommendations = []

for job in filtered_jobs:
    matched_skills = len(set(user_skills) & set(job["skills"]))
    skill_match_score = matched_skills / len(job["skills"]) if job["skills"] else 0

    job_type_match = 1.0 if job["job_type"] == user_job_type else 0.0

    # Weights: skills dominant, job type secondary
    final_score = skill_match_score * 0.85 + job_type_match * 0.15

    recommendations.append((job["title"], final_score))

# Sort by final score descending
recommendations.sort(key=lambda x: x[1], reverse=True)

# Display results
print("Top Recommended Jobs:")
for title, score in recommendations:
    print(f"{title} (Score: {score:.2f})")


