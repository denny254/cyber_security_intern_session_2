# Task4_Credit_Card_Fraud_Detection.py

# 1. Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, roc_curve, 
    precision_score, recall_score, f1_score, accuracy_score, precision_recall_curve
)
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

# 2. Load data
data = pd.read_csv('creditcard.csv')

# 3. Exploratory Data Analysis
print("Data shape:", data.shape)
print(data.head())
print(data.describe())
print(data['Class'].value_counts())

# Visualize class imbalance
plt.figure(figsize=(6,4))
sns.countplot(x='Class', data=data)
plt.title('Class Distribution')
plt.show()

# Check for missing values
print("Missing values:\n", data.isnull().sum())

# 4. Feature Engineering
# Scale 'Amount' and 'Time'
scaler = StandardScaler()
data['Amount_Scaled'] = scaler.fit_transform(data['Amount'].values.reshape(-1,1))
data['Time_Scaled'] = scaler.fit_transform(data['Time'].values.reshape(-1,1))

# Drop original 'Amount' and 'Time'
data = data.drop(['Amount', 'Time'], axis=1)

# 5. Correlation Analysis
corr = data.corr()
plt.figure(figsize=(12,8))
sns.heatmap(corr, cmap='coolwarm', vmax=0.3, center=0, square=True, linewidths=.5)
plt.title('Correlation Matrix')
plt.show()

# 6. Prepare data for modeling
X = data.drop('Class', axis=1)
y = data['Class']

# 7. Handle class imbalance with SMOTE
print("Before SMOTE:", y.value_counts())
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)
print("After SMOTE:", pd.Series(y_res).value_counts())

# 8. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
)

# 9. Model Training and Comparison
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
    'GradientBoosting': GradientBoostingClassifier(random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]
    results[name] = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_proba)
    }
    print(f"\n{name} Classification Report:\n", classification_report(y_test, y_pred))
    print(f"{name} Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 10. Visualize ROC Curves
plt.figure(figsize=(8,6))
for name, model in models.items():
    y_proba = model.predict_proba(X_test)[:,1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.plot(fpr, tpr, label=f'{name} (AUC={roc_auc_score(y_test, y_proba):.2f})')
plt.plot([0,1],[0,1],'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves')
plt.legend()
plt.show()

# 11. Feature Importance (Random Forest)
rf = models['RandomForest']
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(12,6))
plt.title("Feature Importances (Random Forest)")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)
plt.tight_layout()
plt.show()

# 12. Hyperparameter Tuning (Random Forest)
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5]
}
grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring='f1', n_jobs=-1)
grid.fit(X_train, y_train)
print("Best RandomForest Params:", grid.best_params_)
best_rf = grid.best_estimator_
y_pred_best = best_rf.predict(X_test)
print("Tuned RandomForest F1:", f1_score(y_test, y_pred_best))

# 13. Precision-Recall Curve
y_scores = best_rf.predict_proba(X_test)[:,1]
precision, recall, thresholds = precision_recall_curve(y_test, y_scores)
plt.figure(figsize=(8,6))
plt.plot(recall, precision, marker='.')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.show()

# 14. Cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(best_rf, X_res, y_res, cv=cv, scoring='f1')
print("Cross-validated F1 scores:", cv_scores)
print("Mean F1:", np.mean(cv_scores))

# 15. Save the model
import joblib
joblib.dump(best_rf, 'credit_card_fraud_model.pkl')

# 16. Load and test saved model
loaded_model = joblib.load('credit_card_fraud_model.pkl')
sample_pred = loaded_model.predict(X_test[:5])
print("Sample predictions:", sample_pred)

# 17. Predict on new data (example)
def predict_new_transaction(model, transaction):
    transaction_scaled = scaler.transform(np.array(transaction).reshape(1, -1))
    return model.predict(transaction_scaled)

# 18. Summary of Results
print("\nModel Comparison Results:")
for name, metrics in results.items():
    print(f"{name}: {metrics}")

# 19. Additional: Under-sampling for comparison
rus = RandomUnderSampler(random_state=42)
X_rus, y_rus = rus.fit_resample(X, y)
X_train_rus, X_test_rus, y_train_rus, y_test_rus = train_test_split(
    X_rus, y_rus, test_size=0.2, random_state=42, stratify=y_rus
)
rf_rus = RandomForestClassifier(random_state=42)
rf_rus.fit(X_train_rus, y_train_rus)
y_pred_rus = rf_rus.predict(X_test_rus)
print("\nRandomForest with UnderSampling F1:", f1_score(y_test_rus, y_pred_rus))

# 20. End of pipeline
print("\nPipeline complete. Fraud detection model is ready.")