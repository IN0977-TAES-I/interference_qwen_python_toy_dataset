# merge.py - Batch Processor (MERGED - Has Semantic Conflict!)
from datetime import datetime, timedelta

class BatchProcessor:
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
        self.processed_count = 0
        self.skipped_count = 0
    
    def process_batch(self, items, start_date, end_date):
        """Process items within date range."""
        # TRAP: Uses left's inclusive end (<=) but the comment
        # says exclusive. The bug fix from right is LOST!
        filtered = [
            item for item in items
            if start_date <= item["date"] <= end_date  # Bug still present!
        ]
        
        results = []
        for i in range(0, len(filtered), self.batch_size):
            batch = filtered[i:i + self.batch_size]
            batch_result = self._process_single_batch(batch)
            results.extend(batch_result)
        
        self.processed_count += len(results)
        self.skipped_count += len(items) - len(filtered)
        return results
    
    def process_date_range(self, items, days_back=30):
        """Process items from last N days."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        # TRAP: Passes end_date as today, but process_batch uses <=
        # So it includes items from tomorrow if timezone issues exist!
        return self.process_batch(items, start_date, end_date)
    
    def _process_single_batch(self, batch):
        """Process a single batch with validation."""
        results = []
        for item in batch:
            if not self._validate_item(item):
                continue
            result = {
                "id": item["id"],
                "status": "processed",
                "processed_at": datetime.now().isoformat(),
                "amount": item.get("amount", 0),
                "batch_id": id(batch),  # From right branch
            }
            results.append(result)
        return results
    
    def _validate_item(self, item):
        """Validate item before processing."""
        required = ["id", "date"]
        return all(key in item for key in required)
    
    def get_summary(self):
        """Get processing summary."""
        return {
            "total_processed": self.processed_count,
            "total_skipped": self.skipped_count,
            "timestamp": datetime.now().isoformat(),
        }

# TRAP SCENARIO:
# Monthly billing runs on 1st of each month
# process_batch(items, date(2024,1,1), date(2024,2,1))
# With <= : includes Feb 1 items in January's batch (DOUBLE BILLING!)
# With <  : correctly excludes Feb 1 items
# The merge kept <= which causes financial errors!