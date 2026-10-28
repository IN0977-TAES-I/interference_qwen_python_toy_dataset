# merge.py - API Client (MERGED - Has Semantic Conflict!)
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
        """Fetch data from API endpoint with retries and precise handling."""
        url = f"{self.base_url}/{endpoint}"
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url, params=params, timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.ConnectionError as e:
                # TRAP: Right's narrow handling inside left's retry loop
                # DNS errors will be retried 3 times (wasting time!)
                if "timeout" in str(e).lower():
                    last_error = TimeoutError(f"Connection timed out")
                elif "dns" in str(e).lower():
                    logger.critical(f"DNS failed: {endpoint}")
                    raise  # TRAP: Raises immediately, bypassing retry logic
                    # But caller expects TimeoutError, not ConnectionError!
                else:
                    last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                continue
            except requests.exceptions.Timeout:
                last_error = TimeoutError(f"Request timed out")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                continue
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code
                if status == 404:
                    # TRAP: Returns None inside retry loop!
                    # Retry logic is bypassed for 404s (correct)
                    # But caller might retry on None thinking it failed
                    return None
                elif status >= 500:
                    last_error = e
                    if attempt < self.max_retries - 1:
                        time.sleep(2 ** attempt)
                    continue
                else:
                    raise ValueError(f"API error {status}")
            except Exception as e:
                # TRAP: This broad catch from left catches things
                # like KeyboardInterrupt, SystemExit!
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                continue
        
        raise last_error
    
    def post_data(self, endpoint, data):
        """Post data with retries and precise error handling."""
        url = f"{self.base_url}/{endpoint}"
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.post(
                    url, json=data, timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 409:
                    raise ConflictError("Resource conflict")
                    # TRAP: ConflictError is not defined!
                    # Was it supposed to be imported?
                last_error = e
            except Exception as e:
                last_error = e
            if attempt < self.max_retries - 1:
                time.sleep(2 ** attempt)
        
        raise last_error
    
    def close(self):
        """Close the session."""
        self.session.close()