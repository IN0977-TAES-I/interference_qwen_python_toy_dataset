# base.py - API Client
import requests
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def fetch_data(self, endpoint, params=None):
        """Fetch data from API endpoint."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(
                url, params=params, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching {endpoint}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def post_data(self, endpoint, data):
        """Post data to API endpoint."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.post(
                url, json=data, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"POST failed: {e}")
            raise
    
    def close(self):
        """Close the session."""
        self.session.close()