import os
import sys
import pyfiglet
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore
from typing import Dict, List, Set
from urllib.parse import urljoin

init(autoreset=True)

HEADERS: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept-Language": "en-US,en;q=0.9",
}

ALLOWED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp',
    '.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.mpeg', '.wmv', '.ogv', '.3gp',
    '.pdf', '.txt', '.docx', '.xlsx', '.pptx', '.odt', '.rtf', '.tex', '.epub', '.md',
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma',
    '.zip', '.tar', '.rar', '.iso', '.7z', '.gz', '.bz2', '.xz',
    '.sh', '.bat', '.exe', '.jar', '.apk', '.ps1', '.cgi', '.pl', '.py', '.rb', '.php',
    '.c', '.cpp', '.cs', '.java', '.js', '.ts', '.html', '.css', '.go', '.swift', '.kt', '.lua',
    '.json', '.yaml', '.xml', '.ini', '.csv', '.sql', '.db', '.sqlite', '.tar.gz', '.deb',
}

def is_dir_exist(dir: str) -> None:
    if dir is None:
        raise ValueError(f"[{Fore.RED}BAD{Fore.RESET}] -- Dir can't be null.")
    if not os.path.exists(dir):
        os.mkdir(dir)

def make_request(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        return None

def url_endpoint(url: str) -> str:
    if url is None:
        print(f"[{Fore.RED}BAD{Fore.RESET}] -- Url can't be null.")
        return ""
    
    enpoint: str = ""
    for i in (len(url) - 2, 0):
        if url[i] != "/":
            enpoint = "".join(url[i])
        else:
            continue
    return "/" + enpoint[::-1] + "/"

def get_links(url: str) -> List[str]:
    if not url:
        raise ValueError(f"[{Fore.RED}BAD{Fore.RESET}] -- Url can't be null.")
    response = make_request(url)
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            link = a.get('href')
            if link.endswith("/") and link != url_endpoint(link):
                links.append(link)
        return links
    else:
        return []

def get_file_extension(file_name: str) -> str:
    _, extension = os.path.splitext(file_name)
    return extension.lstrip('.')

def download_file(file_url: str, save_directory: str) -> None:
    if file_url is None:
        print(f"[{Fore.RED}BAD{Fore.RESET}] -- Pattern or file url can't be empty.")
        return
    if not file_url.startswith("http"):
        print(f"[{Fore.RED}BAD{Fore.RESET}] -- Invalid URL: {file_url}")
        return
    response = requests.get(file_url, headers=HEADERS, stream=True)
    if response.status_code == 200:
        extension = get_file_extension(file_url)
        is_dir_exist(save_directory)
        directory = os.path.join(save_directory, extension)
        is_dir_exist(directory)
        file_name = os.path.basename(file_url)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[{Fore.GREEN}OK{Fore.RESET}] -- File: {file_url} saved to: {file_path}")
    else:
        print(f"[{Fore.RED}BAD{Fore.RESET}] -- Failed to download file. HTTP status code: {response.status_code}")

def search_files(pattern: List[str], url: str, save_directory: str) -> None:
    if len(pattern) == 0 or not url:
        print(f"[{Fore.RED}BAD{Fore.RESET}] -- Pattern or URL can't be empty")
        return
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if "*" in pattern:
            print(f"[{Fore.GREEN}INFO{Fore.RESET}] -- Searching for all files...")
            files = soup.find_all('a', href=True)
            for file in files:
                file_url = file['href']
                if not file_url.startswith("http"):
                    file_url = urljoin(url, file_url)
                print(f"[{Fore.GREEN}INSTALLING{Fore.RESET}] -- {file_url}")
                download_file(file_url, save_directory)
        else:
            print(f"[{Fore.GREEN}INFO{Fore.RESET}] -- Searching for files matching patterns: {Fore.CYAN}{pattern}{Fore.RESET}")
            files = soup.find_all('a', href=True)
            for file in files:
                file_url = file['href']
                if not file_url.startswith("http"):
                    file_url = urljoin(url, file_url)
                if any(file_url.endswith(ext) for ext in pattern):
                    print(f"[{Fore.GREEN}INSTALLING{Fore.RESET}] -- {file_url}")
                    download_file(file_url, save_directory)
    else:
        print(f"[{Fore.RED}BAD{Fore.RESET}] -- Failed to retrieve URL. Status code: {response.status_code}")

def deep_search(url: str, visited: Set[str], save_directory: str, pattern: List[str], base_url: str) -> Set[str]:
    if not url or url in visited:
        return visited
    
    visited.add(url)
    print(f"[{Fore.GREEN}INFO{Fore.RESET}] -- Visiting: {url}")

    if not url.startswith(base_url):
        print(f"[{Fore.GREEN}INFO{Fore.RESET}] -- Skipping out-of-scope URL: {url}")
        return visited
    search_files(pattern, url, save_directory)

    links = get_links(url)
    for link in links:
        full_url = urljoin(url, link)  
    
        if full_url not in visited:
            visited = deep_search(full_url, visited, save_directory, pattern, base_url)

    return visited

def main() -> None:
    if len(sys.argv) < 4:
        print(f"\n[{Fore.RED}BAD{Fore.RESET}] -- Missing URL argument.\n")
        print(f"[{Fore.CYAN}USAGE{Fore.RESET}] -- python scrapper.py <url> <extensions> <directory>")
        print(f'[{Fore.CYAN}EXAMPLE 1{Fore.RESET}] -- python scrapper.py https://example.com "*" downloads/')
        print(f'[{Fore.CYAN}EXAMPLE 2{Fore.RESET}] -- python scrapper.py https://example.com "jpg|deb" downloads/\n')
        sys.exit(1)

    basic_url: str = sys.argv[1]
    patterns: List[str] = sys.argv[2].split("|")
    directory: str = sys.argv[3]

    basic_url = basic_url.rstrip('/') + '/'
    ascii_art = pyfiglet.figlet_format("WebScrapper")

    print("\n\t" + Fore.WHITE + " " * 3 + ascii_art)
    print(f"\n[{Fore.GREEN}STARTING{Fore.RESET}] -- Start scrapping from: {basic_url}\n")

    visited_urls: Set[str] = deep_search(basic_url, set(), directory, patterns, basic_url)

if __name__ == '__main__':
    main()
