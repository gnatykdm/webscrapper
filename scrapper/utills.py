import time
from typing import Any
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import os

def timer(func: Any) -> Any:
    def wrapped(*args, **kwargs) -> Any:
        start: float = time.time()
        result: Any = func(*args, **kwargs)
        finish: float = time.time()
        print(f"Function - {func.__name__} worked: {finish - start:.3f}s")
        return result
    return wrapped

def save_img(url: str, directory: str, filename: str) -> None:
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        if not os.path.exists(directory):
            os.makedirs(directory)
        img.save(os.path.join(directory, filename))
    except requests.RequestException as e:
        print(f"Failed to download image from {url}: {e}")
    except UnidentifiedImageError:
        print(f"Cannot identify image file from {url}")
    except Exception as e:
        print(f"Failed to save image {filename}: {e}")