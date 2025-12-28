import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time

try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None

def get_headers():
    """Returns advanced headers to mimic a real browser and avoid 403 errors."""
    if UserAgent:
        ua = UserAgent()
        user_agent = ua.random
    else:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    return {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Connection": "keep-alive"
    }

def get_soup(url):
    """Fetches a URL and returns a BeautifulSoup object."""
    try:
        time.sleep(random.uniform(2, 5)) # Sleep to appear human
        response = requests.get(url, headers=get_headers(), timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"⚠️  Access Denied (403) for {url}. Anti-scraping protection active.")
            return "BLOCKED"
        print(f"Error fetching {url}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_date(date_string):
    """Parses date strings from various formats."""
    if not date_string:
        return None
    formats = ["%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%d %B %Y"]
    cleaned_date = date_string.strip()
    for fmt in formats:
        try:
            return datetime.strptime(cleaned_date, fmt)
        except ValueError:
            continue
    return None