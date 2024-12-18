import requests
from bs4 import BeautifulSoup as BS
from typing import List
from utills import timer

def get_data(url: str) -> str:
    r = requests.get(url)
    return r.text

@timer
def get_url(url: str) -> List[str]:
    soup = BS(get_data(url), 'html.parser')

    result: List[str] = []
    for item in soup.find_all('img'):
        result.append(item['src'])
    return result