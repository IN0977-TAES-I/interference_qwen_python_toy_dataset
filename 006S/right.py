# right.py - API Client (Precision Error Handling Branch)
import requests
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def fetch_data(self, endpoint, params=None):
        """Fetch data from API endpoint with precise error handling."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(
                url, params=params, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            # Only handle specific connection issues
            if "timeout" in str(e).lower():
                logger.error(f"Connection timeout: {endpoint}")
                raise TimeoutError(f"Connection to {endpoint} timed out")
            elif "dns" in str(e).lower():
                logger.critical(f"DNS resolution failed: {endpoint}")
                raise  # DNS failures should NOT be retried
            else:
                logger.error(f"Connection error: {e}")
                raise
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout: {endpoint}")
            raise TimeoutError(f"Request to {endpoint} timed out")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            if status == 404:
                logger.info(f"Resource not found: {endpoint}")
                return None  # 404 is not an error, return None
            elif status >= 500:
                logger.error(f"Server error {status}: {endpoint}")
                raise
            else:
                logger.error(f"Client error {status}: {endpoint}")
                raise ValueError(f"API error {status} for {endpoint}")
    
    def post_data(self, endpoint, data):
        """Post data with precise error handling."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.post(
                url, json=data, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                logger.warning(f"Conflict: {endpoint}")
                raise ConflictError("Resource conflict")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def close(self):
        """Close the session."""
        self.session.close()