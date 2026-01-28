# Practice Questions for Machine Learning Models

## Instructions

These practice questions are designed to test your understanding of the material covered in the Machine Learning Models lecture. Work through each question carefully and show your reasoning.

---

## Part 1: True/False Questions

**Question 1:** In supervised machine learning, a model is a mathematical mapping that transforms a feature vector into its corresponding predicted label.

**Question 2:** Parametric machine learning models have a fixed number of parameters that is independent of the number of training examples.

**Question 3:** In linear regression, the equation y = x^T w + w_0 represents a hyperplane in the space defined by the response y and the feature vector x.

**Question 4:** A linear classification model with high training accuracy on data that is not linearly separable will always perform well on test data.

**Question 5:** Non-parametric models have no parameters at all, which is why they are called "non-parametric."

---

## Part 2: Explanatory Questions

**Question 6:** Explain the relationship between model parameters and model inputs in the context of linear models. How do they differ in their roles during training versus prediction?

**Question 7:** Compare and contrast parametric and non-parametric machine learning models. What are the key differences in how they represent the relationship between features and labels?

**Question 8:** Describe the geometric interpretation of a linear classification model in a 2-dimensional feature space. What does the equation x^T w + w_0 = 0 represent, and how does it relate to class predictions?

**Question 9:** Explain what is meant by the statement "All models are wrong, but some are useful." How does this apply to linear models specifically, and what limitations do linear models have?

**Question 10:** In training a simple linear regression model, the weights w_1 and w_0 are chosen to minimize the sum of squared vertical distances between observations and the fitted line. Explain what these vertical distances represent and why minimizing them is a reasonable objective.

---

## Part 3: Coding Question

**Question 11: Implement Simple Linear Regression from Scratch**

Implement a simple linear regression model from scratch using only NumPy. Your implementation should find the optimal weights w_1 (slope) and w_0 (intercept) that minimize the sum of squared errors between predictions and actual values.

**Steps:**
1. Create a function that computes predictions given weights, intercept, and feature values
2. Implement a function that computes the mean squared error (MSE) for given weights
3. Use the closed-form solution (normal equation) to find optimal weights: for simple linear regression, w_1 = Σ((x_i - x_mean)(y_i - y_mean)) / Σ((x_i - x_mean)^2) and w_0 = y_mean - w_1 * x_mean
4. Test your implementation on sample data and compare predictions with actual values

**Function Signature:**
```python
import numpy as np

def simple_linear_regression(X, y):
    """
    Fit a simple linear regression model using the closed-form solution.
    
    Args:
        X: numpy array of shape (n,) containing feature values
        y: numpy array of shape (n,) containing response values
    
    Returns:
        tuple: (w_1, w_0) where w_1 is the slope and w_0 is the intercept
    """
    pass

def predict(X, w_1, w_0):
    """
    Make predictions using the linear model.
    
    Args:
        X: numpy array of shape (n,) containing feature values
        w_1: slope parameter
        w_0: intercept parameter
    
    Returns:
        numpy array of shape (n,) containing predictions
    """
    pass
```

**Example:**
```python
# Input
X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 6])

w_1, w_0 = simple_linear_regression(X, y)
predictions = predict(X, w_1, w_0)

# Output
print(f"Slope (w_1): {w_1:.4f}")
print(f"Intercept (w_0): {w_0:.4f}")
print(f"Predictions: {predictions}")
# Expected output approximately:
# Slope (w_1): 0.8
# Intercept (w_0): 1.6
# Predictions: [2.4 3.2 4.0 4.8 5.6]
```

**Hints:**
- Remember that X_mean and y_mean are the average values of X and y respectively
- The numerator for w_1 involves computing covariance-like terms
- The denominator for w_1 is essentially the variance of X
- Once you have w_1, computing w_0 is straightforward using the means

---

## Part 4: Use Case Application

**Question 12: Predicting Student Admission with Linear Classification**

**Scenario:**

You are working as a data analyst for a university admissions office. The office wants to build a predictive model to help identify which applicants are likely to be admitted based on their test scores. You have historical data on students' GRE scores (Graduate Record Examination) and CGPA (Cumulative Grade Point Average), along with whether they were admitted (1) or not admitted (0).

**Data:**

Generate sample admission data to work with:

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic admission data
n_samples = 200

# Generate GRE scores (normally distributed, mean 310, std 15)
gre_scores = np.random.normal(310, 15, n_samples)

# Generate CGPA (normally distributed, mean 8.0, std 0.8)
cgpa = np.random.normal(8.0, 0.8, n_samples)

# Create admission label based on a linear relationship with some noise
# Higher GRE and CGPA increase admission probability
admission_score = 0.02 * gre_scores + 2.5 * cgpa - 25 + np.random.normal(0, 1, n_samples)
admitted = (admission_score > 0).astype(int)

# Create DataFrame
data = pd.DataFrame({
    'GRE_Score': gre_scores,
    'CGPA': cgpa,
    'Admitted': admitted
})

print(data.head(10))
print(f"\nAdmission rate: {admitted.mean():.2%}")
```

**Task:**

Build and evaluate a linear classification model to predict student admission based on GRE scores and CGPA.

**Requirements:**
- Split the data into training (70%) and testing (30%) sets
- Standardize/normalize the features before training (important for many linear models)
- Train a logistic regression model (a linear classification model) on the training data
- Evaluate the model's accuracy on both training and test sets
- Visualize the decision boundary (the line x^T w + w_0 = 0) along with the data points
- Interpret the learned weights: which feature has a stronger influence on admission prediction?

**Hints:**
- Use `StandardScaler` from sklearn to normalize features - this puts features on the same scale
- The decision boundary can be plotted using the model's coefficients (weights) and intercept
- For a 2D feature space, the decision boundary line equation is: x_2 = -(w_1/w_2) * x_1 - (w_0/w_2)
- Color-code the data points by their actual admission status and observe how well the linear boundary separates the classes
- Remember that this is a simplification - real admission decisions involve many more factors and ethical considerations
