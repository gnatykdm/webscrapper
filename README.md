# WebScrapper

WebScrapper is a Python-based tool to scrape and save images from a given website. It downloads images, saves them to a specified directory, and optionally resizes them.

## Features

- Scrape images from a specified URL.
- Save images to a specified directory.
- Resize images to specified dimensions.
- Supports multiple image formats.

## Requirements

- Python 3.6+
- See [requirements.txt](requirements.txt) for the list of dependencies.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/gnatykdm/webscrapper.git
    cd WebScrapper

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To scrape and save images from a website, run the following command:
```sh
python main.py <URL> [--directory <directory>] [--width <width>] [--height <height>]