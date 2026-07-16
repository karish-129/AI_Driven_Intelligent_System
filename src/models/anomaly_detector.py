# src/models/anomaly_detector.py
import numpy as np
from sklearn.ensemble import IsolationForest

class FraudAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_trained = False

    def train_baseline(self):
        """Generates synthetic baseline profile vectors to initialize the engine."""
        # Features: [time_delta_seconds, transaction_amount, is_vpn_flag]
        normal_behavior = np.random.normal(loc=[600, 2000, 0], scale=[100, 500, 0.01], size=(100, 3))
        normal_behavior[:, 2] = np.clip(normal_behavior[:, 2], 0, 0) # Force clean flag boundaries
        
        self.model.fit(normal_behavior)
        self.is_trained = True

    def calculate_risk(self, time_delta: float, amount: float, is_vpn: bool) -> float:
        """Computes a composite anomaly signature metric scaled between 0 and 100."""
        if not self.is_trained:
            self.train_baseline()
            
        feature_vector = np.array([[time_delta, amount, 1.0 if is_vpn else 0.0]])
        raw_score = self.model.score_samples(feature_vector)[0]
        
        # Invert and scale to convert anomaly output to a 0-100 risk percentage
        risk_percentage = min(max(int((0.5 - raw_score) * 100), 0), 100)
        
        # Fail-safe strict override: High amount/immediate transfer behind a proxy
        if is_vpn and time_delta < 300:
            risk_percentage = max(risk_percentage, 90)
            
        return float(risk_percentage)