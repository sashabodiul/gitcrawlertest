# GitHub Crawler

## Description

This script implements a GitHub search crawler that returns all links from search results. The script supports proxy and authentication.

## Requirements

- Python 3.12
- requests
- beautifulsoup4
- aiohttp
- json

## Setup

Install the required dependencies:
```bash
pyenv install 3.12
pyenv local 3.12
poetry shell
poetry install
```

### To run crawler

```bash
python3 main.py
```

## To run tests:

```bash
python3 -m unittest discover -s tests
```