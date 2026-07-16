# config/settings.py

# Time window in seconds for correlating cyber logs and transactions (5 Minutes)
TEMPORAL_WINDOW_SECONDS = 300

# Risk Threshold Categorization Lower Boundaries
RISK_THRESHOLD_HIGH = 75
RISK_THRESHOLD_MEDIUM = 40

# Static Risk Weights for Fallback/Deterministic Scoring Matrix
RISK_WEIGHTS = {
    "vpn_active": 30,
    "device_mismatch": 40,
    "high_volume_transfer": 20
}