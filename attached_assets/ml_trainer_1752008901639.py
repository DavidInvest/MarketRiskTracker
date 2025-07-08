import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

class MLTrainer:
    def __init__(self):
        pass

    def generate_dummy_data(self):
        X = np.random.rand(1000, 5)
        y = (X[:, 0] + X[:, 1] > 1).astype(int)
        return X, y

    def train_model(self):
        X, y = self.generate_dummy_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        joblib.dump(model, "ml_model.pkl")
        print("✅ Model trained and saved.")