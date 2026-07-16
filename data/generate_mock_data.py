# data/generate_mock_data.py
import json
import random
from datetime import datetime, timedelta

def generate_dataset(num_users=10):
    telemetry_stream = []
    transaction_stream = []
    base_time = datetime.now()
    
    for i in range(num_users):
        cust_id = f"CUST_{1000 + i}"
        dev_id = f"DEV_{random.randint(5000, 9999)}"
        
        # Standard Transactions
        timestamp = base_time + timedelta(minutes=i * 10)
        telemetry_stream.append({
            "customer_id": cust_id, "device_id": dev_id,
            "ip_address": f"192.168.1.{random.randint(2, 254)}",
            "is_vpn": False, "timestamp": timestamp.isoformat()
        })
        transaction_stream.append({
            "customer_id": cust_id, "amount": round(random.uniform(500, 4000), 2),
            "channel": "UPI", "beneficiary_id": f"ACC_{random.randint(8888, 9999)}",
            "timestamp": (timestamp + timedelta(seconds=45)).isoformat()
        })

    # Injected Attack Vector (The Plagiarism-Free Unique Use Case)
    fraud_cust = "CUST_9999"
    attack_time = base_time + timedelta(hours=5)
    
    telemetry_stream.append({
        "customer_id": fraud_cust, "device_id": "ROGUE_DEV_X",
        "ip_address": "45.223.19.89", "is_vpn": True, "timestamp": attack_time.isoformat()
    })
    transaction_stream.append({
        "customer_id": fraud_cust, "amount": 95000.00,
        "channel": "IMPS", "beneficiary_id": "MULE_ACC_666",
        "timestamp": (attack_time + timedelta(minutes=2)).isoformat()
    })

    with open("data/cyber_telemetry.json", "w") as f:
        json.dump(telemetry_stream, f, indent=4)
    with open("data/transactions.json", "w") as f:
        json.dump(transaction_stream, f, indent=4)
        
    print("✅ Testing dataset successfully populated into data/")

if __name__ == "__main__":
    generate_dataset()
