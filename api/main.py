# api/main.py
from fastapi import FastAPI, HTTPException
from src.ingestion.schemas import TelemetryLog, TransactionLog
from src.pipeline.stream_processor import RealTimeBuffer
from src.models.anomaly_detector import FraudAnomalyDetector
from datetime import datetime

app = FastAPI(title="Neuro-Wall Fusion Engine", version="1.0.0")

# Instantiate working engine state
stream_buffer = RealTimeBuffer()
detector = FraudAnomalyDetector()
detector.train_baseline()  # Calibrate standard behaviors on launch

@app.post("/api/v1/telemetry", status_code=201)
async def ingest_telemetry(log: TelemetryLog):
    """Endpoint to receive streaming SIEM/Device network telemetry packets."""
    try:
        stream_buffer.add_telemetry(log.customer_id, log.model_dump())
        return {"status": "success", "message": "Telemetry event processed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/transaction")
async def process_transaction(tx: TransactionLog):
    """Endpoint to intercept ledger operations and run unified risk analysis."""
    # 1. Fetch concurrent cyber telemetry layers
    associated_logs = stream_buffer.fetch_correlated_telemetry(tx.customer_id)
    
    # Set default values if no telemetry exists within the time loop
    time_delta = 9999.0
    is_vpn_active = False
    
    # 2. Correlate attributes if overlapping items exist
    if associated_logs:
        latest_log = associated_logs[-1]
        time_delta = abs((tx.timestamp.replace(tzinfo=None) - latest_log['timestamp'].replace(tzinfo=None)).total_seconds())
        is_vpn_active = latest_log.get('is_vpn', False)
    
    # 3. Request evaluation from the AI Engine
    risk_score = detector.calculate_risk(
        time_delta=time_delta,
        amount=tx.amount,
        is_vpn=is_vpn_active
    )
    
    # 4. Return structural mitigation matrix
    action = "ALLOW"
    if risk_score >= 75:
        action = "BLOCK_TRANSACTION"
    elif risk_score >= 40:
        action = "TRIGGER_STEP_UP_OTP"
        
    return {
        "customer_id": tx.customer_id,
        "transaction_amount": tx.amount,
        "calculated_risk_score": risk_score,
        "recommended_action": action,
        "telemetry_matches_found": len(associated_logs)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)