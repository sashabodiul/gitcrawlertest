# main.py
import sys
import os

# Get the current working directory
current_dir = os.path.dirname(os.path.realpath(__file__))
# Add the path to the project root directory to sys.path
sys.path.append(current_dir)

# Import classes from core
from core import GitHubCrawler, SearchType
import json

if __name__ == '__main__':
    # Define search parameters
    keywords = ["openstack", "nova", "css"]
    search_type = SearchType.REPOSITORIES

    # Initialize GitHubCrawler with search parameters
    crawler = GitHubCrawler(keywords, search_type.value)
    
    # Perform GitHub search
    results = crawler.search()
    
    # Print search results in JSON format
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Parse repositories from search results
    repo_result = crawler.parse_repo(results)
    
    # Print parsed repository results in JSON format
    print(json.dumps(repo_result, indent=4, ensure_ascii=False))