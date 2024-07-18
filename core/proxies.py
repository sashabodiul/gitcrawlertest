# core/proxies.py

import random
from typing import List

class ProxyManager:
    PROXIES: List[str] = [
        'http://sashabodiul07:7UMNo7iRr6@91.124.86.145:50100',
        'http://sashabodiul07:7UMNo7iRr6@91.124.99.49:50100',
        'http://sashabodiul07:7UMNo7iRr6@91.124.87.70:50100',
        'http://sashabodiul07:7UMNo7iRr6@91.124.84.115:50100',
        'http://sashabodiul07:7UMNo7iRr6@91.124.95.74:50100',
        'http://sashabodiul07:7UMNo7iRr6@91.124.98.106:50100',
        'http://sashabodiul07:7UMNo7iRr6@91.124.97.133:50100',
        'http://sashabodiul07:7UMNo7iRr6@91.124.92.6:50100',
        'http://sashabodiul07:7UMNo7iRr6@91.124.96.5:50100',
        'http://sashabodiul07:7UMNo7iRr6@91.124.93.253:50100'
    ]

    @classmethod
    def get_random_proxy(cls) -> str:
        """
        Class method to retrieve a random proxy from the PROXIES list.

        Returns:
        - str: Random proxy URL from the list.
        """
        return random.choice(cls.PROXIES)