import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.models.anomaly_detector import FraudAnomalyDetector

app = FastAPI(title="Neuro-Wall Fusion Ingestion Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = FraudAnomalyDetector()

class TelemetryPayload(BaseModel):
    time_delta: float
    amount: float
    is_vpn: bool

@app.post("/api/v1/ingest")
async def ingest_traffic(payload: TelemetryPayload):
    try:
        risk_score = detector.calculate_risk(
            time_delta=payload.time_delta,
            amount=payload.amount,
            is_vpn=payload.is_vpn
        )
        return {
            "status": "processed",
            "risk_score": risk_score,
            "action": "BLOCK" if risk_score > 75.0 else "ALLOW"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
