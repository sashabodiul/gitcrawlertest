# tests/test_proxies.py

import unittest
from core.proxies import ProxyManager

class TestProxyManager(unittest.TestCase):

    def test_get_random_proxy(self):
        proxy_manager = ProxyManager()
        proxy = proxy_manager.get_random_proxy()
        self.assertIn(proxy, ProxyManager.PROXIES)

if __name__ == '__main__':
    unittest.main()