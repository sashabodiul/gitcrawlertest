# tests/test_proxies.py

import unittest
from core.proxies import ProxyManager

class TestProxyManager(unittest.TestCase):

    def test_get_random_proxy(self):
        """
        Test case for ProxyManager.get_random_proxy().

        This test verifies that the proxy returned by get_random_proxy()
        belongs to the list of known proxies in ProxyManager.PROXIES.
        """
        proxy_manager = ProxyManager()
        proxy = proxy_manager.get_random_proxy()
        self.assertIn(proxy, ProxyManager.PROXIES)

if __name__ == '__main__':
    unittest.main()