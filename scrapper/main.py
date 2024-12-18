from urllib.parse import urljoin
from parse import get_url
from utills import save_img
from requests.exceptions import MissingSchema, InvalidURL
from PIL import UnidentifiedImageError, Image
import os
from tqdm import tqdm
import argparse
from colorama import init, Fore

init(autoreset=True)

def resize_image(image_path, size):
    try:
        with Image.open(image_path) as img:
            img = img.resize(size, Image.LANCZOS)
            img.save(image_path)
    except UnidentifiedImageError:
        print(Fore.RED + f"Cannot resize image file: {image_path}")

def main():
    parser = argparse.ArgumentParser(description="Scrape and save images from a website.")
    parser.add_argument("url", type=str, help="The URL of the website to scrape images from.")
    parser.add_argument("--directory", type=str, default="images", help="The directory to save images. Default is 'images'.")
    parser.add_argument("--width", type=int, default=800, help="The width to resize images to. Default is 800.")
    parser.add_argument("--height", type=int, default=600, help="The height to resize images to. Default is 600.")
    
    args = parser.parse_args()

    img_urls = get_url(args.url)

    for i, img_url in tqdm(enumerate(img_urls), desc="Saving images", unit="image"):
        try:
            absolute_url = urljoin(args.url, img_url)
            img_extension = os.path.splitext(img_url)[1] or '.jpg'
            filename = f"image_{i+1}{img_extension}"
            save_img(absolute_url, args.directory, filename)
            if img_extension.lower() not in ['.svg', '.gif']:
                resize_image(os.path.join(args.directory, filename), (args.width, args.height))
            print(Fore.GREEN + f"Saved {filename}")
        except (MissingSchema, InvalidURL):
            print(Fore.RED + f"Invalid URL: {img_url}")
        except UnidentifiedImageError:
            print(Fore.RED + f"Cannot identify image file: {img_url}")
        except FileNotFoundError:
            print(Fore.RED + f"File not found: {filename}")

if __name__ == "__main__":
    main()