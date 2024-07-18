# core/requests.py

import requests
from core.headers import HeadersManager
from typing import Optional

class GithubRequest:
    PROXIES: dict = {}  # Class variable to store proxies
    
    def __init__(self):
        """
        Initialize GithubRequest instance.
        """
        self.headers_manager = HeadersManager()

    @classmethod
    def set_proxies(cls, proxies: dict) -> None:
        """
        Class method to set proxies for requests.

        Args:
        - proxies (dict): Dictionary containing proxy settings.
        """
        cls.PROXIES = proxies

    def get(self, url: str) -> Optional[requests.Response]:
        """
        Perform a GET request using requests library.

        Args:
        - url (str): URL to send the GET request.

        Returns:
        - requests.Response object if successful, None if there's an error.
        """
        headers = self.headers_manager.get_headers()
        try:
            response = requests.get(url, headers=headers, proxies=self.PROXIES, timeout=10)
            return response
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None