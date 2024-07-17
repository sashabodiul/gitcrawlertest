# tests/test_requests.py

import unittest
from core.gitrequests import GithubRequest
from core.proxies import ProxyManager

class TestGithubRequest(unittest.TestCase):

    def setUp(self):
        proxy = ProxyManager.get_random_proxy()
        GithubRequest.set_proxies({"http": proxy, "https": proxy})
        self.github_request = GithubRequest()

    def test_get_request(self):
        url = 'https://github.com/search?q=nova&type=repositories'
        response = self.github_request.get(url)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()