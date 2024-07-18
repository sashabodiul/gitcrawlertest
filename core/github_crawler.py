# core/github_crawler.py

from typing import Dict, List, Union
from enum import Enum
from bs4 import BeautifulSoup
from core.gitrequests import GithubRequest
from core.proxies import ProxyManager
from utils.decorators import timing_decorator
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import Response, RequestException

class SearchType(Enum):
    REPOSITORIES: str = "Repositories"
    ISSUES: str = "Issues"
    WIKIS: str = "Wikis"

class GitHubCrawler:
    def __init__(self, keywords: List[str], search_type: SearchType):
        """
        Initialize GitHubCrawler instance.

        Args:
        - keywords (List[str]): List of keywords to search on GitHub.
        - search_type (SearchType): Type of search (Repositories, Issues, or Wikis).
        """
        self.keywords = keywords
        self.search_type = search_type
        self.github_request = GithubRequest()
        self.proxy_manager = ProxyManager()

    @timing_decorator
    def search(self) -> List[Dict[str, str]]:
        """
        Perform GitHub search based on keywords and search type.

        Returns:
        - List of dictionaries containing URLs found in search results.
        """
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

    def _search_keyword(self, keyword: str) -> List[Dict[str, str]]:
        """
        Perform a search for a specific keyword using GitHub search API.

        Args:
        - keyword (str): Keyword to search on GitHub.

        Returns:
        - List of dictionaries containing parsed results from the search.
        """
        url = f'https://github.com/search?q={keyword}&type={self.search_type.value}'
        proxy = self.proxy_manager.get_random_proxy()
        GithubRequest.set_proxies({'http': proxy, 'https': proxy})
        response = GithubRequest.get(url)
        if response and response.status_code == 200:
            return self._parse_results(response.text)
        else:
            print(f"Failed to retrieve search results for '{keyword}': status code {response.status_code if response else 'None'}")
            return []

    @timing_decorator
    def parse_repo(self, urls: List[Dict[str, str]]) -> List[Dict[str, Union[str, Dict[str, Union[float, int]]]]]:
        """
        Parse repositories from a list of URLs concurrently.

        Args:
        - urls (List[Dict[str, str]]): List of dictionaries containing URLs to parse.

        Returns:
        - List of dictionaries containing parsed repository information.
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:  # Set the number of threads as per your choice
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

    def process_url(self, url: str) -> Union[Dict[str, Union[str, Dict[str, Union[float, int]]]], None]:
        """
        Process a single GitHub repository URL to extract owner and language statistics.

        Args:
        - url (str): URL of the GitHub repository.

        Returns:
        - Dictionary containing URL, owner, and language statistics if successful, otherwise None.
        """
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
    def _parse_results(self, html: str) -> List[Dict[str, str]]:
        """
        Parse HTML content to extract GitHub repository URLs.

        Args:
        - html (str): HTML content of the GitHub search results page.

        Returns:
        - List of dictionaries containing parsed repository URLs.
        """
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
    
    def get_language_stats(self, html: str) -> Dict[str, Union[float, int]]:
        """
        Extract language statistics from the HTML content of a GitHub repository page.

        Args:
        - html (str): HTML content of the GitHub repository page.

        Returns:
        - Dictionary mapping programming languages to their percentage usage in the repository.
        """
        soup = BeautifulSoup(html, 'html.parser')
        langs = soup.select("div.Layout-sidebar ul.list-style-none li.d-inline a.Link--secondary")
        values = []
        for lang in langs:
            values.append([span.text.strip() for span in lang.select("span")])
        return dict(values)
    
    def get_owner(self, html: str) -> str:
        """
        Extract the owner username from the HTML content of a GitHub repository page.

        Args:
        - html (str): HTML content of the GitHub repository page.

        Returns:
        - Owner username of the GitHub repository.
        """
        soup = BeautifulSoup(html, 'html.parser')
        span = soup.select_one("span.author a")
        if span and span.text:
            return span.text.strip()