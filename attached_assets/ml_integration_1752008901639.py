import joblib
import numpy as np

class MLIntegration:
    def __init__(self):
        self.model = joblib.load("ml_model.pkl")

    def predict(self, features):
        features = np.array(features).reshape(1, -1)
        return self.model.predict_proba(features)