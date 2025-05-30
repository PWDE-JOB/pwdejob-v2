# PWDE JOB - Job Recommendation System (Testing Version)

## Overview
PWDE JOB is a job recommendation system designed to help Persons with Disabilities (PWD) find suitable employment opportunities. This version is a testing/dummy system that demonstrates the core functionality of the larger PWDE JOB project.

## System Architecture
The system implements three different recommendation algorithms:

1. **Content-Based Filtering**
   - Matches user skills directly with job requirements
   - Considers experience level and PWD-friendliness
   - Calculates skill match scores based on exact skill matches

2. **Decision Tree Model**
   - Uses machine learning to predict job matches
   - Trains on historical job data
   - Considers skills, experience, and PWD status as features

3. **Hybrid Recommendation System**
   - Combines collaborative filtering with content-based filtering
   - Uses user history to find similar jobs
   - Weights both historical preferences and skill matches

## Installation and Setup

1. Ensure Python 3.x is installed
2. Install required dependencies:
   ```bash
   pip install pandas numpy scikit-learn
   ```
3. Place all CSV files in the project directory:
   - job_data_pwd.csv
   - job_data_pwd_for_cola.csv
   - user_history.csv
   - skills_category_data.csv
   - interaction_matrix.csv

## Usage Instructions

1. Run the main script:
   ```bash
   python main.py
   ```

2. Follow the interactive prompts:
   - Enter your name
   - Select a user history (1-3)
   - Input your 5 skills
   - Specify years of experience
   - Indicate PWD status (1 for yes, 0 for no)

3. The system will display three sets of recommendations:
   - Content-based recommendations
   - Decision tree model recommendations
   - Hybrid recommendations

## Algorithm Explanations

### Decision Tree Results
The decision tree model sometimes highlights only one job because:
- It's trained on a small dataset
- The model makes binary decisions based on feature thresholds
- Limited depth (max_depth=10) may not capture all variations
- The probability distribution might be highly skewed

### Hybrid System (Collaborative + Content-based)
The hybrid system combines both approaches because:
- Collaborative filtering alone requires extensive user data
- Content-based filtering provides immediate recommendations
- The combination improves accuracy by considering both:
  - Historical user preferences (collaborative)
  - Current skill matches (content-based)
- Weighted scoring (40% history, 60% skill match) balances both approaches

## System Limitations and Considerations

### Small User Base (Current Testing Version)
Pros:
- Faster processing and response times
- Easier to debug and modify
- Lower computational resource requirements
- Quick to implement changes

Cons:
- Limited recommendation diversity
- Less accurate collaborative filtering
- May miss potential job matches
- Higher risk of overfitting

### Large-Scale Implementation
Pros:
- More diverse and accurate recommendations
- Better collaborative filtering results
- Improved pattern recognition
- More robust decision tree model

Cons:
- Higher computational requirements
- More complex maintenance
- Need for better data management
- Potential privacy concerns
- Requires more sophisticated infrastructure

## Algorithm Performance Ratings

Based on the goal of accurately recommending jobs to users, here are the performance ratings for each algorithm:

### Decision Tree Model
- **Current Testing Version Rating: 4/10**
  - **Strengths:**
    - Quick to train and make predictions
    - Can handle both categorical and numerical features
    - Works well with structured data
  - **Weaknesses:**
    - Limited by small dataset size
    - Often produces skewed results (one job getting highlighted)
    - Less accurate in capturing complex skill relationships
  - **Rating Explanation:** The low rating is due to the model's tendency to overfit on the small dataset and produce less diverse recommendations. The binary nature of decision trees makes it less suitable for nuanced job matching.

- **Potential Version Rating: 6/10**
  - **Expected Improvements:**
    - Better performance with larger datasets
    - More diverse recommendations
    - Improved accuracy with more training data
  - **Remaining Challenges:**
    - Still limited by binary decision nature
    - May struggle with complex skill relationships
    - Requires careful tuning for optimal performance

### Content-Based Algorithm
- **Current Testing Version Rating: 7/10**
  - **Strengths:**
    - Direct skill matching provides relevant results
    - Works well with limited user data
    - Considers PWD-specific requirements
  - **Weaknesses:**
    - May miss jobs that require similar but different skills
    - Doesn't learn from user preferences
    - Limited by the quality of skill matching
  - **Rating Explanation:** The higher rating reflects its reliability in providing relevant job matches based on direct skill matching. It's particularly effective for the testing version as it doesn't require extensive user data.

- **Potential Version Rating: 8/10**
  - **Expected Improvements:**
    - Better skill matching with larger job database
    - More sophisticated skill similarity matching
    - Enhanced PWD-specific filtering
  - **Remaining Challenges:**
    - Still lacks personalization
    - May need additional features for better matching
    - Requires regular skill database updates

### Hybrid System
- **Current Testing Version Rating: 8/10**
  - **Strengths:**
    - Combines best of both approaches
    - More diverse recommendations
    - Learns from user history
  - **Weaknesses:**
    - Requires more computational resources
    - Dependent on quality of user history data
    - May be less effective with limited user data
  - **Rating Explanation:** The highest rating is due to its balanced approach, combining immediate skill matching with learned preferences. The weighted scoring system (40% history, 60% skill match) provides more reliable and diverse recommendations.

- **Potential Version Rating: 9/10**
  - **Expected Improvements:**
    - More accurate with larger user base
    - Better personalization through extensive user history
    - Improved recommendation diversity
    - More sophisticated weighting system
  - **Remaining Challenges:**
    - Requires significant computational resources
    - Needs robust data management system
    - Must handle privacy concerns effectively

## Future Improvements
1. Add real-time job data integration
2. Improve user history tracking
3. Enhance PWD-specific job matching
4. Implement user feedback system

## Note
This is a testing version of the PWDE JOB system. The actual production system will have more features, better data handling, and improved recommendation algorithms. 