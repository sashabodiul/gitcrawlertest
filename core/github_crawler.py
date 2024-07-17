# core/github_crawler.py

from typing import Dict
from enum import Enum
from bs4 import BeautifulSoup
from core.gitrequests import GithubRequest
from core.proxies import ProxyManager
from utils.decorators import timing_decorator
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import RequestException

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

    def _search_keyword(self, keyword: str):
        url = f'{self.BASE_URL}?q={keyword}&type={self.search_type}'
        proxy = self.proxy_manager.get_random_proxy()
        GithubRequest.set_proxies({'http': proxy, 'https': proxy})
        response = GithubRequest.get(url)
        if response and response.status_code == 200:
            return self._parse_results(response.text)
        else:
            print(f"Failed to retrieve search results for '{keyword}': status code {response.status_code if response else 'None'}")
            return []

    @timing_decorator
    def parse_repo(self, urls):
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:  # Задайте количество потоков по вашему выбору
            futures = []
            for url_info in urls:
                url = url_info['url']
                futures.append(executor.submit(self.process_url, url))

            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    print(f"Exception occurred: {e}")

        return results

    def process_url(self, url):
        try:
            response = self.github_request.get(url)
            if response.status_code == 200:
                html = response.text
                owner = self.get_owner(html)
                language_stats = self.get_language_stats(html)
                return {
                    "url": url,
                    "owner": owner,
                    "language_stats": language_stats
                }
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
        except RequestException as e:
            print(f"Request error for {url}: {e}")
        except TypeError as e:
            print(f"Error processing {url}: {e}")
        return None
    
    @timing_decorator
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
    
    def get_language_stats(self, html) -> Dict:
        soup = BeautifulSoup(html, 'html.parser')
        langs = soup.select("div.Layout-sidebar ul.list-style-none li.d-inline a.Link--secondary")
        values = []
        for lang in langs:
            values.append([span.text.strip() for span in lang.select("span")])
        return dict(values)
    
    def get_owner(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        span = soup.select_one("span.author a")
        if span and span.text:
            return span.text.strip()