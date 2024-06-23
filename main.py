import os
from excel_handler import get_image_urls
from downloader import download_image
import logging

logging.basicConfig(filename='download_images.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    file_path = 'data/input.xlsx'
    save_path = 'data/images'
    os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists
    urls = get_image_urls(file_path)
    for style in urls.keys():
        for i, url in enumerate(urls[style]):
            try:
                download_image(url, save_path, f'{style}_img{i+1}.jpg')
                logging.info(f'Downloaded image for style: {style}, image {i + 1}')
            except Exception as e:
                logging.error(f'Error downloading image for style: {style}, image {i+1}: {e}')


if __name__ == "__main__":
    main()