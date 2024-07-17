# core/requests.py

import requests
from core.headers import HeadersManager

class GithubRequest:
    PROXIES = {}
    
    def __init__(self):
        self.headers_manager = HeadersManager()

    @classmethod
    def set_proxies(cls, proxies):
        cls.PROXIES = proxies

    def get(self, url):
        headers = self.headers_manager.get_headers()
        try:
            response = requests.get(url, headers=headers, proxies=self.PROXIES, timeout=10)
            return response
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None