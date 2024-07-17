# main.py
import sys
import os

# Получение текущего рабочего каталога
current_dir = os.path.dirname(os.path.realpath(__file__))
# Добавление пути к корневому каталогу проекта в sys.path
sys.path.append(current_dir)

# Импорт классов из core
from core import GitHubCrawler, SearchType
import json

if __name__ == '__main__':
    keywords = ["openstack", "nova", "css"]
    search_type = SearchType.REPOSITORIES

    crawler = GitHubCrawler(keywords, search_type.value)
    results = crawler.search()

    print(json.dumps(results, indent=2, ensure_ascii=False))