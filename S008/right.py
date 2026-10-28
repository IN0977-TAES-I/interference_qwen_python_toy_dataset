# right.py - Batch Processor (Bug Fix Branch)
from datetime import datetime, timedelta

class BatchProcessor:
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
        self.processed_count = 0
    
    def process_batch(self, items, start_date, end_date):
        """Process items within date range (exclusive end - bug fix)."""
        # BUG FIX: end_date should be exclusive to prevent
        # processing items from the next period
        filtered = [
            item for item in items
            if start_date <= item["date"] < end_date  # Changed to <
        ]
        
        results = []
        for i in range(0, len(filtered), self.batch_size):
            batch = filtered[i:i + self.batch_size]
            batch_result = self._process_single_batch(batch)
            results.extend(batch_result)
        
        self.processed_count += len(results)
        return results
    
    def _process_single_batch(self, batch):
        """Process a single batch of items."""
        results = []
        for item in batch:
            result = {
                "id": item["id"],
                "status": "processed",
                "timestamp": datetime.now().isoformat(),
                "batch_id": id(batch),  # Track batch origin
            }
            results.append(result)
        return results
    
    def get_summary(self):
        """Get processing summary."""
        return {
            "total_processed": self.processed_count,
            "timestamp": datetime.now().isoformat(),
        }