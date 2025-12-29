"""
Common HTTP client for inter-service communication
Each service will use this to call other services
"""
import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ServiceClient:
    """
    Base client for making HTTP requests to other services
    
    Example Usage:
        # Create client for inventory service
        inventory_client = ServiceClient('http://inventory-service:8002')
        
        # Make GET request
        response = inventory_client.get('/api/materials/123')
        material = response.json()
        
        # Make POST request
        response = inventory_client.post('/api/stock/reserve', 
                                         data={'quantity': 100})
    """
    
    def __init__(self, base_url: str, timeout: int = 5):
        """
        Initialize service client
        
        Args:
            base_url: Base URL of the service (e.g., 'http://auth-service:8001')
            timeout: Request timeout in seconds (default: 5)
        """
        self.base_url = base_url.rstrip('/')  # Remove trailing slash
        self.timeout = timeout
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[Any, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Make HTTP request to service
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., '/api/users/123')
            data: JSON data for POST/PUT requests
            headers: HTTP headers (e.g., Authorization token)
            params: Query parameters
            
        Returns:
            Response object
            
        Raises:
            requests.exceptions.RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()  # Raise error for 4xx/5xx status
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Service call failed: {method} {url} - {str(e)}")
            raise
    
    def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None, 
            params: Optional[Dict[str, Any]] = None):
        """GET request"""
        return self._make_request('GET', endpoint, headers=headers, params=params)
    
    def post(self, endpoint: str, data: Dict[Any, Any], 
             headers: Optional[Dict[str, str]] = None):
        """POST request"""
        return self._make_request('POST', endpoint, data=data, headers=headers)
    
    def put(self, endpoint: str, data: Dict[Any, Any], 
            headers: Optional[Dict[str, str]] = None):
        """PUT request"""
        return self._make_request('PUT', endpoint, data=data, headers=headers)
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None):
        """DELETE request"""
        return self._make_request('DELETE', endpoint, headers=headers)


# Pre-configured service URLs (Docker container names)
# These will be used when services run in Docker
AUTH_SERVICE_URL = 'http://auth-service:8001'
INVENTORY_SERVICE_URL = 'http://inventory-service:8002'
MANUFACTURING_SERVICE_URL = 'http://manufacturing-service:8003'
PROCESS_SERVICE_URL = 'http://process-service:8004'
QUALITY_SERVICE_URL = 'http://quality-service:8005'
FG_STORE_SERVICE_URL = 'http://fg-store-service:8006'
THIRD_PARTY_SERVICE_URL = 'http://third-party-service:8007'
NOTIFICATION_SERVICE_URL = 'http://notification-service:8008'


# Pre-configured clients ready to use
# Each service can import these directly
auth_client = ServiceClient(AUTH_SERVICE_URL)
inventory_client = ServiceClient(INVENTORY_SERVICE_URL)
manufacturing_client = ServiceClient(MANUFACTURING_SERVICE_URL)
process_client = ServiceClient(PROCESS_SERVICE_URL)
quality_client = ServiceClient(QUALITY_SERVICE_URL)
fg_store_client = ServiceClient(FG_STORE_SERVICE_URL)
third_party_client = ServiceClient(THIRD_PARTY_SERVICE_URL)
notification_client = ServiceClient(NOTIFICATION_SERVICE_URL)