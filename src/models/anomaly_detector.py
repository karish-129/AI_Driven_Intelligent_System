import os

class FraudAnomalyDetector:
    def __init__(self):
        print("🛡️ Neuro-Wall Engine Security Core initialized.")

    def calculate_risk(self, time_delta: float, amount: float, is_vpn: bool) -> float:
        """Evaluates rapid transaction spikes alongside network metadata anomalies."""
        risk = 10.0
        
        # Factor 1: High transactional values
        if amount > 50000:
            risk += 35.0
        elif amount > 10000:
            risk += 15.0
            
        # Factor 2: High velocity execution context
        if time_delta < 60:
            risk += 25.0
            
        # Factor 3: Routing concealment masks
        if is_vpn:
            risk += 30.0
            
        return min(float(risk), 100.0)
