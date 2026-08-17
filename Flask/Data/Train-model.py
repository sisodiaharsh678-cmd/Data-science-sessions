import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# 1. Load small CSV dataset
df = pd.read_csv('students.csv')

# 2. Split features (X) and target (y)
X = df[['study_hours', 'attendance']]
y = df['pass']

# 3. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 4. Train a small Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# 5. Check accuracy
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)
print(f"Test Accuracy: {acc:.2f}")

# 6. Save model as .pkl file
joblib.dump(model, 'pass_predictor.pkl')