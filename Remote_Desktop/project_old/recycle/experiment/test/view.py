import os
import requests
import zipfile
from urllib.parse import urlparse

def download_and_extract_zip(url, extract_dir):
    # Parse the URL to get the filename
    url_components = urlparse(url)
    zip_filename = os.path.basename(url_components.path)

    # Create directory if it doesn't exist
    os.makedirs(extract_dir, exist_ok=True)

    # Download the zip file
    zip_file_path = os.path.join(extract_dir, zip_filename)
    try:
        print(f"Downloading {url}...")
        response = requests.get(url)
        with open(zip_file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {zip_file_path}")

        # Extract the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Extracted contents to {extract_dir}")

        # Optional: Delete the downloaded zip file
        os.remove(zip_file_path)
        print(f"Deleted {zip_file_path}")

        return True
    except Exception as e:
        print(f"Error downloading or extracting zip file: {e}")
        return False

# Example usage:
url = "https://github.com/GyanD/codexffmpeg/releases/download/2024-06-24-git-6ec22731ae/ffmpeg-2024-06-24-git-6ec22731ae-full_build.zip"
extract_dir = "extracted_contents"

if download_and_extract_zip(url, extract_dir):
    print("Download and extraction successful.")
else:
    print("Failed to download or extract the zip file.")
