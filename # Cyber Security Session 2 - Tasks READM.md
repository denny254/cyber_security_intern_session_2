# Cyber Security Session 2 - Tasks README

## Overview

This repository contains solutions for two practical cybersecurity/data science tasks:

1. **Task 3: Lost Data Retrieval**  
   Simulate accidental file deletion and perform data recovery using forensic tools.

2. **Task 4: Credit Card Fraud Detection**  
   Build and evaluate a machine learning model to detect fraudulent credit card transactions.

---

## Task 3: Lost Data Retrieval

**Objective:**  
Simulate a scenario where files are accidentally deleted from a storage device (e.g., USB drive) and attempt to recover them using data recovery tools.

**Steps:**
1. Prepare a USB drive (formatted as NTFS or FAT32).
2. Create test files (e.g., `test1.txt`, `photo.jpg`) and delete them.
3. Use a tool like **TestDisk** (or Recuva) to scan the drive for deleted files.
4. Attempt to recover the deleted files and document the process.
5. Analyze the results and discuss factors affecting recovery.

**Files:**
- `Lost_Data_Retrieval_Report.md`  
  Contains a detailed report of the scenario, recovery steps, tools used, results, and best practices.

**Requirements:**
- TestDisk or Recuva installed on your system.
- A USB drive or virtual disk for safe testing.

---

## Task 4: Credit Card Fraud Detection

**Objective:**  
Build a machine learning model to detect fraudulent credit card transactions using a dataset with features such as transaction amount, time, and anonymized variables.

**Steps:**
1. Load and explore the dataset (`creditcard.csv`).
2. Preprocess data (handle missing values, scale features).
3. Address class imbalance using SMOTE or under-sampling.
4. Split data into training and test sets.
5. Train multiple classification models (Random Forest, Logistic Regression, Gradient Boosting).
6. Evaluate models using metrics like accuracy, precision, recall, F1-score, ROC-AUC.
7. Visualize results (confusion matrix, ROC curve, feature importance).
8. Tune hyperparameters and save the best model.

**Files:**
- `# Task4_Credit_Card_Fraud_Detection.py` or `Task4_Credit_Card_Fraud_Detection.ipynb`  
  Contains the full code for data loading, preprocessing, modeling, evaluation, and visualization.

**Requirements:**
- Python 3.x
- Required libraries: pandas, numpy, scikit-learn, imbalanced-learn, matplotlib, seaborn, joblib

**Dataset:**
- `creditcard.csv` (Kaggle: [Credit Card Fraud Detection Dataset](https://www.kaggle.com/mlg-ulb/creditcardfraud))

---

## How to Run

### Task 3
- Read the `Lost_Data_Retrieval_Report.md` for step-by-step instructions.
- Follow the documented process in a safe, test environment.

### Task 4
1. Ensure all dependencies are installed:
   ```
   pip install pandas numpy scikit-learn imbalanced-learn matplotlib seaborn joblib
   ```
2. Place `creditcard.csv` in the project directory.
3. Run the Python script or Jupyter notebook:
   ```
   python "# Task4_Credit_Card_Fraud_Detection.py"
   ```
   or open and run all cells in the notebook.

---

## Notes

- **Task 3** is a documentation/reporting task; no code execution is required.
- **Task 4** is a data science task; code execution and dataset are required.
- For screenshots or additional documentation, refer to the respective report or notebook.

---

## Authors

- Dennis Kinanga

---