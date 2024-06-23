import requests
import os
import logging

def download_image(url, save_path, file_name):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        with open(os.path.join(save_path, file_name), 'wb') as f:
            f.write(response.content)
        logging.info(f"Downloaded {url} to {os.path.join(save_path, file_name)}")
        return True
    except requests.RequestException as e:
        logging.error(f"Failed to download {url}: {str(e)}")
        return False

