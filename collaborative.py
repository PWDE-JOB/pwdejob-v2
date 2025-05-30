# ============================
# PWDEJOB-RECOMENDING SYSTEM (Collaborative FIltering algorithm)
# VERSION: 1.0.0
# Author: The Totemn
# ===========================

import numpy as np
import pandas as pd

# Load job data and user history data
job_data = pd.read_csv("job_data_pwd_for_cola.csv")
user_history = pd.read_csv("user_history.csv")

merged_data = pd.merge(user_history, job_data, left_on="job id", right_on="Job ID")


# Create user-job interaction matrix
interaction_matrix = merged_data.pivot_table(
    index="user id",    # rows: users
    columns="job id",   # columns: jobs
    values="applied",   # value: whether user applied
    fill_value=0        # if no record, assume 0
)

# print(interaction_matrix.head())

interaction_matrix.to_csv("interaction_matrix.csv")

