# core/github_crawler.py

from enum import Enum
from bs4 import BeautifulSoup
from core.gitrequests import GithubRequest
from core.proxies import ProxyManager
from utils.decorators import timing_decorator
from concurrent.futures import ThreadPoolExecutor, as_completed

class SearchType(Enum):
    REPOSITORIES = "Repositories"
    ISSUES = "Issues"
    WIKIS = "Wikis"

class GitHubCrawler:
    def __init__(self, keywords, search_type):
        self.keywords = keywords
        self.search_type = search_type
        self.github_request = GithubRequest()
        self.proxy_manager = ProxyManager()

    @timing_decorator
    def search(self):
        results = []
        for keyword in self.keywords:
            url = f'https://github.com/search?q={keyword}&type={self.search_type}'
            response = self.github_request.get(url)
            
            # Debug: Print status code and part of response content
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                divs = soup.find_all('div', class_='search-title')
                for div in divs:
                    a_tag = div.select_one('a')
                    if a_tag and 'href' in a_tag.attrs:
                        results.append({
                            "url": 'https://github.com' + a_tag.attrs['href']
                        })
                return results

    def _search_keyword(self, keyword):
        url = f'{self.BASE_URL}?q={keyword}&type={self.search_type}'
        proxy = self.proxy_manager.get_random_proxy()
        GithubRequest.set_proxies({'http': proxy, 'https': proxy})
        response = GithubRequest.get(url)
        if response and response.status_code == 200:
            return self._parse_results(response.text)
        else:
            print(f"Failed to retrieve search results for '{keyword}': status code {response.status_code if response else 'None'}")
            return []

    def _parse_results(self, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', class_='search-title')
        for div in divs:
            a_tag = div.select_one('a')
            if a_tag and 'href' in a_tag.attrs:
                results.append({
                    "url": 'https://github.com' + a_tag.attrs['href']
                })
        return results