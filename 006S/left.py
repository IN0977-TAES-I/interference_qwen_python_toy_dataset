# left.py - API Client (Resilience Branch)
import requests
import logging
import time

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url, timeout=30, max_retries=3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
    
    def fetch_data(self, endpoint, params=None):
        """Fetch data from API endpoint with retries."""
        url = f"{self.base_url}/{endpoint}"
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url, params=params, timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:  # TRAP: Catches EVERYTHING
                last_error = e
                logger.warning(
                    f"Attempt {attempt + 1} failed for {endpoint}: {e}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                continue
        
        logger.error(f"All retries exhausted for {endpoint}")
        raise last_error
    
    def post_data(self, endpoint, data):
        """Post data to API endpoint with retries."""
        url = f"{self.base_url}/{endpoint}"
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.post(
                    url, json=data, timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:  # TRAP: Catches EVERYTHING
                last_error = e
                logger.warning(f"POST attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                continue
        
        raise last_error
    
    def close(self):
        """Close the session."""
        self.session.close()