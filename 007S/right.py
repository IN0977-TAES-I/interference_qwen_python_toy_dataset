# right.py - Data Processor (Safety Branch)
import csv
from io import StringIO

class DataProcessor:
    def __init__(self):
        self.results = []
        self._processing_log = []
    
    def process_row(self, row, transformations=None):
        """Process a single data row (safe defaults)."""
        result = dict(row)
        if transformations is None:
            transformations = []
        
        for transform in transformations:
            result = transform(result)
        
        self.results.append(result)
        self._processing_log.append({
            "action": "process_row",
            "row_keys": list(row.keys()),
        })
        return result
    
    def process_file(self, content, delimiter=",", skip_errors=False):
        """Process CSV content with error handling option."""
        reader = csv.DictReader(
            StringIO(content), delimiter=delimiter
        )
        for row in reader:
            try:
                self.process_row(row)
            except Exception as e:
                if not skip_errors:
                    raise
                self._processing_log.append({
                    "action": "error",
                    "error": str(e),
                    "row": row,
                })
        return self.results
    
    def filter_results(self, key, value, operator="eq"):
        """Filter results with configurable operator."""
        ops = {
            "eq": lambda a, b: a == b,
            "ne": lambda a, b: a != b,
            "gt": lambda a, b: a > b,
            "lt": lambda a, b: a < b,
            "contains": lambda a, b: b in str(a),
        }
        op_func = ops.get(operator, ops["eq"])
        return [r for r in self.results if op_func(r.get(key), value)]
    
    def get_log(self):
        """Get processing log."""
        return self._processing_log
    
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
        elif format_type == "tsv":
            if not self.results:
                return ""
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=self.results[0].keys(), delimiter="\t")
            writer.writeheader()
            writer.writerows(self.results)
            return output.getvalue()
        return str(self.results)