import joblib
from sklearn.linear_model import LinearRegression
import numpy as np


X = np.array([
    [2, 1], [5, 2], [1, 1], [8, 3], [3, 2], [10, 4], [4, 1], [6, 3]
])
y = np.array([15, 25, 10, 40, 20, 50, 18, 35])

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "delivery_time_model.joblib")
print("Model saved as delivery_time_model.joblib")