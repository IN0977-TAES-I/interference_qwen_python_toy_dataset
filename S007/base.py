# base.py - Data Processor
import csv
from io import StringIO

class DataProcessor:
    def __init__(self):
        self.results = []
    
    def process_row(self, row, transformations=None):
        """Process a single data row."""
        result = dict(row)
        if transformations:
            for transform in transformations:
                result = transform(result)
        self.results.append(result)
        return result
    
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
        return str(self.results)