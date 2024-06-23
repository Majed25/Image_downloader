import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

# configure logging
logging.basicConfig(filename='check_drive.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Define the scope
SCOPES = ["https://www.googleapis.com/auth/drive"]
# Path to your service account credentials file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'drive/credentials.json'  # Update this path



def create_service():
    """Creates the Drive v3 API service using service account credentials."""
    creds = Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scopes=SCOPES)
    return build("drive", "v3", credentials=creds)

def list_files(service, folder_id='root', indent=0):
    """Lists the files and folders in the specified folder."""
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            logging.debug(' ' * indent + 'No files found.')
        else:
            for item in items:
                logging.info(' ' * indent + f'{item["name"]} ({item["mimeType"]})')
                if item['mimeType'] == 'application/vnd.google-apps.folder':
                    list_files(service, item['id'], indent + 4)
    except HttpError as error:
        logging.error(f"An error occurred: {error}")


def find_and_delete_file(service, filename):
    """Finds and deletes a file by its name."""
    try:
        # Search for the file by name
        results = service.files().list(q=f"name='{filename}' and trashed=false", fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.debug(f"No file found with name: {filename}")
        else:
            for item in items:
                file_id = item['id']
                service.files().delete(fileId=file_id).execute()
                logging.info(f"Deleted file: {item['name']} (ID: {file_id})")
    except HttpError as error:
        logging.error(f"An error occurred: {error}")


def find_folder(service, folder_name):
    """Finds the folder by name and returns its ID and webViewLink."""
    try:
        results = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
                                       fields="files(id, name, webViewLink)").execute()
        items = results.get('files', [])
        if not items:
            logging.debug(f"Folder '{folder_name}' not found.")
            return None, None
        return items[0]['id'], items[0]['webViewLink']
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return None, None



if __name__ == "__main__":
    service = create_service()
    list_files(service)
    folder_name = 'Uploaded Images'
    folder_id, folder_url = find_folder(service, folder_name)
    if folder_id and folder_url:
        logging.info(f"Folder '{folder_name}' URL: {folder_url}")
    else:
        logging.debug(f"Folder '{folder_name}' not found.")

    #for filename in filenames_to_delete:
    #    find_and_delete_file(service, filename)
    #list_files(service)




