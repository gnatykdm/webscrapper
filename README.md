# Web Scraper

A simple Python script to download files from a website recursively based on specified file extensions. It can download a variety of file types, including images, videos, documents, and more.

## Features

- Recursively scrape a website for downloadable files.
- Download files based on specified extensions (or all files if no extensions are specified).
- Support a wide range of file extensions (images, videos, documents, and more).
- Log download progress with color-coded messages for easy tracking.

## Requirements

- Python 3.x
- [`requests`](https://pypi.org/project/requests/) library
- [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/) library
- [`colorama`](https://pypi.org/project/colorama/) library

You can install the required libraries by running:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Syntax

```bash
python scrapper.py <URL> <extensions> <download_directory>
```

- `<URL>`: The URL of the website you want to scrape.
- `<extensions>`: A list of file extensions to download. Use `*` for all file types, or specify extensions like `*.jpg|*.png|*.pdf`.
- `<download_directory>`: The local directory where you want to save the downloaded files.

### Examples

#### Download All Files

```bash
python scrapper.py https://example.com "*" ./downloads
```

This command will download all files from the specified URL.

#### Download Specific Files (e.g., Images and Logos)

```bash
python scrapper.py https://example.com "*jpg|png" ./downloads
```

This command will download only `.jpg` images and files named `logo.png`.

## How It Works

- **Recursion**: The script uses recursion to follow links found on the website and scrape additional pages.
- **File Matching**: You can specify which files to download by using patterns. Use `*` as a wildcard for any extension.
- **Directory Management**: The script will create the download directory if it doesn't exist.
- **Error Handling**: The script logs any errors that occur during the downloading process and will skip files that cannot be downloaded.

## Notes

- The script processes HTML pages and looks for all links (`<a href="...">`), downloading files from them if they match the specified extensions.
- If no extensions are provided, the script will attempt to download all files it finds.
- The script is designed to be simple and easy to use, while also providing useful logging information.

## License

This project is licensed under the [MIT License](LICENSE).