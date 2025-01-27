import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import Any, List
from colorama import Fore, Style, init

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
        return file_extension in allowed_extensions

    for pattern in patterns:
        if pattern.startswith("*.") and file_name.endswith(pattern[1:]):
            return True
        if pattern == file_name:
            return True
    return False


def is_valid_file_url(url: str, allowed_extensions: set) -> bool:
    return any(url.lower().endswith(ext) for ext in allowed_extensions)


def download_files(base_url: str, patterns: List[str], directory: str, allowed_extensions: set) -> None:
    if not check_if_dir_exist(directory):
        os.makedirs(directory)

    visited = set() 
    stack = [base_url]

    parsed_start_url = urlparse(base_url)
    base_domain = parsed_start_url.netloc
    base_path = parsed_start_url.path.rstrip('/')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    while stack:
        current_url = stack.pop()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            print(f"{Fore.CYAN}Processing: {current_url}")
            response = requests.get(current_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)

                parsed_url = urlparse(full_url)
                if parsed_url.netloc != base_domain or not parsed_url.path.startswith(base_path):
                    continue

                file_name = os.path.basename(full_url)
                file_extension = os.path.splitext(file_name)[-1].lower()

                if is_valid_file_url(full_url, allowed_extensions) and should_download_file(file_name, patterns, allowed_extensions):
                    extension_dir = os.path.join(directory, file_extension.lstrip('.'))
                    os.makedirs(extension_dir, exist_ok=True)

                    file_path = os.path.join(extension_dir, file_name)
                    if os.path.exists(file_path):
                        print(f"{Fore.YELLOW}File already exists: {file_path}")
                        continue

                    try:
                        with requests.get(full_url, stream=True, headers=headers, timeout=10) as r:
                            r.raise_for_status()
                            with open(file_path, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=8192):
                                    f.write(chunk)
                        print(f"{Fore.GREEN}Downloaded: {file_name} to {extension_dir}")
                    except Exception as e:
                        print(f"{Fore.RED}Failed to download {full_url}: {e}")

                elif href.endswith('/'):
                    if full_url not in visited:
                        stack.append(full_url)

            for css_link in soup.find_all('link', {'rel': 'stylesheet'}, href=True):
                full_url = urljoin(current_url, css_link['href'])
                print(f"{Fore.CYAN}Processing CSS: {full_url}")
                response = requests.get(full_url, headers=headers, timeout=10)
                response.raise_for_status()

                for line in response.text.splitlines():
                    if 'url(' in line:
                        start = line.find('url(') + 4
                        end = line.find(')', start)
                        if start > 3 and end > start:
                            file_url = line[start:end]
                            full_file_url = urljoin(current_url, file_url)
                            if is_valid_file_url(full_file_url, allowed_extensions):
                                file_name = os.path.basename(full_file_url)
                                if should_download_file(file_name, patterns, allowed_extensions):
                                    print(f"{Fore.GREEN}Downloading background image: {full_file_url}")
                                    download_files(full_file_url, patterns, directory, allowed_extensions)

        except requests.RequestException as e:
            print(f"{Fore.RED}Failed to process {current_url}: {e}")
        except Exception as e:
            print(f"{Fore.RED}Unexpected error with {current_url}: {e}")


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
        '.json', '.yaml', '.xml', '.ini', '.csv', '.sql', '.db', '.sqlite', '.tar.gz',
    }

    pattern_list = patterns.split('|')
    download_files(path, pattern_list, directory, allowed_extensions)


if __name__ == '__main__':
    main()
