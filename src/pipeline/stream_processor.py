# src/pipeline/stream_processor.py
from datetime import datetime
from config.settings import TEMPORAL_WINDOW_SECONDS

class RealTimeBuffer:
    def __init__(self):
        # In-memory window cache grouped by customer_id
        self.telemetry_cache = {}

    def add_telemetry(self, customer_id: str, telemetry_data: dict):
        """Appends a network/device log to the user's active tracking queue."""
        if customer_id not in self.telemetry_cache:
            self.telemetry_cache[customer_id] = []
        
        # Ensure standard python datetime format
        if isinstance(telemetry_data.get('timestamp'), str):
            telemetry_data['timestamp'] = datetime.fromisoformat(telemetry_data['timestamp'].replace('Z', ''))
            
        self.telemetry_cache[customer_id].append(telemetry_data)
        self.clean_expired_logs(customer_id)

    def clean_expired_logs(self, customer_id: str):
        """Purges telemetry logs that fall outside the active temporal window configuration."""
        if customer_id not in self.telemetry_cache:
            return
            
        now = datetime.now()
        self.telemetry_cache[customer_id] = [
            log for log in self.telemetry_cache[customer_id]
            if (now - log['timestamp']).total_seconds() <= TEMPORAL_WINDOW_SECONDS
        ]

    def fetch_correlated_telemetry(self, customer_id: str) -> list:
        """Retrieves all non-expired network telemetry logs linked to the target customer."""
        self.clean_expired_logs(customer_id)
        return self.telemetry_cache.get(customer_id, [])