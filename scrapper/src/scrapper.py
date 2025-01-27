import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import Any, List
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

def timer(func: Any) -> Any:
    def wrapped(*args, **kwargs) -> Any:
        start_t: float = time.time()
        result: Any = func(*args, **kwargs)
        stop_t: float = time.time()
        print(f"{Fore.GREEN}Fetching data took: {stop_t - start_t:.2f} seconds.")
        return result
    return wrapped


def check_if_dir_exist(dir_name: str) -> bool:
    return os.path.exists(dir_name)


def should_download_file(file_name: str, patterns: List[str], allowed_extensions: set) -> bool:
    if '*' in patterns:
        file_extension = os.path.splitext(file_name)[-1].lower()
        if file_extension in allowed_extensions:
            return True

    for pattern in patterns:
        if pattern.startswith("*.") and file_name.endswith(pattern[1:]):
            return True
        if pattern == file_name:
            return True
    return False


def is_valid_file_url(url: str, allowed_extensions: set) -> bool:    
    return any(url.endswith(ext) for ext in allowed_extensions)


def download_files(url: str, patterns: List[str], directory: str, allowed_extensions: set) -> None:
    if not check_if_dir_exist(directory):
        os.makedirs(directory)
    
    visited = set()
    stack = [url]
    
    while stack:
        current_url = stack.pop()
        if current_url in visited:
            continue
        visited.add(current_url)
        try:
            print(f"{Fore.CYAN}Processing: {current_url}")
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)
                
                file_name = os.path.basename(full_url)
                
                if is_valid_file_url(full_url, allowed_extensions) and should_download_file(file_name, patterns, allowed_extensions):
                    file_path = os.path.join(directory, file_name)
                    try:
                        with requests.get(full_url, stream=True) as r:
                            r.raise_for_status()
                            with open(file_path, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=8192):
                                    f.write(chunk)
                        print(f"{Fore.GREEN}Downloaded: {file_name}")
                    except Exception as e:
                        print(f"{Fore.RED}Failed to download {full_url}: {e}")
                
                elif href.endswith('/'):
                    stack.append(full_url)

        except Exception as e:
            print(f"{Fore.RED}Failed to process {current_url}: {e}")


@timer
def main() -> None:
    import sys

    if len(sys.argv) < 4:
        print(f"{Fore.YELLOW}Usage: python scrapper.py <url> <extensions> <directory>")
        print('Example 1: python scrapper.py https://example.com "*" downloads/')
        print('Example 2: python scrapper.py https://example.com "*.jpg|logo.png" downloads/')
        return

    path: str = sys.argv[1]
    patterns: str = sys.argv[2]
    directory: str = sys.argv[3]

    allowed_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', 
        '.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.mpeg', '.wmv', '.ogv', '.3gp',
        '.pdf', '.txt', '.docx', '.xlsx', '.pptx', '.odt', '.rtf', '.tex', '.epub', '.md',
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma',
        '.zip', '.tar', '.rar', '.iso', '.7z', '.gz', '.bz2', '.xz',
        '.sh', '.bat', '.exe', '.jar', '.apk', '.ps1', '.cgi', '.pl', '.py', '.rb', '.php',
        '.c', '.cpp', '.cs', '.java', '.js', '.ts', '.html', '.css', '.go', '.swift', '.kt', '.lua', 
        '.rs', '.scala', '.h', '.m', '.v', '.pl', '.r', '.php', '.pas', '.vhdl', '.for', '.lisp', '.clj',
        '.bash', '.zsh', '.fish', '.dart', '.el', '.sh', '.nim', '.d', '.jl', '.sol', '.m4', '.vb', '.coffee',
        '.json', '.yaml', '.xml', '.ini', '.csv', '.sql', '.db', '.sqlite', '.tar.gz',
    }

    pattern_list = patterns.split('|')
    download_files(path, pattern_list, directory, allowed_extensions)


if __name__ == '__main__':
    main()
