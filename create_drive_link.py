import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import logging

logging.basicConfig(filename='share_drive.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



SCOPES = ["https://www.googleapis.com/auth/drive.file"]
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'drive/credentials.json'

def create_service():
    """Creates the Drive v3 API service using service account credentials."""
    creds = Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scopes=SCOPES)
    return build("drive", "v3", credentials=creds)

def create_folder(service, folder_name):
    """Creates a folder in Google Drive and returns the folder ID."""
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id,webViewLink').execute()
    logging.info(f'Folder ID: {folder.get("id")}')
    return folder.get('id'), folder.get('webViewLink')

def upload_images_to_folder(service, folder_id, images_path):
    """Uploads images to the specified folder in Google Drive."""
    try:
        for image in os.listdir(images_path):
            image_path = os.path.join(images_path, image)
            if os.path.isfile(image_path):
                file_metadata = {
                    'name': os.path.basename(image),
                    'parents': [folder_id]
                }
                media = MediaFileUpload(image_path, mimetype='image/jpeg')
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                logging.info(f'Uploaded {image} with ID: {file.get("id")}')
    except HttpError as error:
        logging.error(f"An error occurred: {error}")

def make_folder_public(service, folder_id):
    """Makes the folder accessible to anyone with the link."""
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(
        fileId=folder_id,
        body=permission,
        fields='id'
    ).execute()
    logging.info("Folder is now public")


BRAND = 'MeetMeInSantorini'
if __name__ == "__main__":
    service = create_service()
    folder_id, folder_link = create_folder(service, f'{BRAND}Uploaded Images')
    upload_images_to_folder(service, folder_id, 'data/images')
    make_folder_public(service, folder_id)
    logging.info(f"Access the uploaded folder here: {folder_link}")


