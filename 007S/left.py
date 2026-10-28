# left.py - Data Processor (Convenience Branch)
import csv
from io import StringIO

class DataProcessor:
    def __init__(self):
        self.results = []
        self.errors = []
    
    def process_row(self, row, transformations=[]):
        """Process a single data row with default transforms."""
        # Add default cleanup transform
        default_transforms = [self._clean_whitespace]
        all_transforms = default_transforms + transformations
        # TRAP: transformations=[] is a mutable default!
        # Each call without arg SHARES the same list!
        
        result = dict(row)
        try:
            for transform in all_transforms:
                result = transform(result)
            self.results.append(result)
        except Exception as e:
            self.errors.append({"row": row, "error": str(e)})
        return result
    
    def _clean_whitespace(self, row):
        """Remove leading/trailing whitespace from values."""
        return {k: v.strip() if isinstance(v, str) else v 
                for k, v in row.items()}
    
    def process_file(self, content, delimiter=","):
        """Process CSV content."""
        reader = csv.DictReader(
            StringIO(content), delimiter=delimiter
        )
        for row in reader:
            self.process_row(row)
        return self.results
    
    def filter_results(self, key, value):
        """Filter results by key-value pair."""
        return [r for r in self.results if r.get(key) == value]
    
    def get_errors(self):
        """Get all processing errors."""
        return self.errors
    
    def export_results(self, format_type="csv"):
        """Export results in specified format."""
        if format_type == "csv":
            if not self.results:
                return ""
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)
            return output.getvalue()
        elif format_type == "json":
            import json
            return json.dumps(self.results, indent=2)
        return str(self.results)