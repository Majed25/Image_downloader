import os
from excel_handler import get_image_urls
from downloader import download_image

def main():
    file_path = 'data/input.xlsx'
    save_path = 'data/images'
    os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists
    urls = get_image_urls(file_path)
    for style in urls.keys():
        for i, url in enumerate(urls[style]):
            download_image(url, save_path, f'{style}_img{i+1}.jpg')


if __name__ == "__main__":
    main()