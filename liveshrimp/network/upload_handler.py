import os
import requests
import json

def upload_file(file_path, upload_url, metadata=None):
    """
    Upload a single file to a specified server.

    Args:
        file_path (str): Path to the file to upload.
        upload_url (str): URL of the server to upload to.
        metadata (dict): Optional metadata to send with the file.

    Returns:
        bool: True if upload was successful, False otherwise.
    """
    try:
        with open(file_path, 'rb') as video_file:
            files = {"file": video_file}
            data = {"metadata": json.dumps(metadata)} if metadata else {}
            response = requests.post(upload_url, files=files, data=data)
            response.raise_for_status()
        print(f"Uploaded: {file_path}")
        return True
    except requests.RequestException as e:
        print(f"Failed to upload {file_path}: {e}")
        return False

def upload_pending_files(video_folder, upload_url, metadata_callback=None):
    """
    Upload all pending video files in a folder.

    Args:
        video_folder (str): Directory containing video files.
        upload_url (str): URL of the server to upload to.
        metadata_callback (callable): Function to generate metadata for each file.

    Returns:
        None
    """
    for file_name in sorted(os.listdir(video_folder)):
        if file_name.endswith(".mp4"):
            file_path = os.path.join(video_folder, file_name)

            # Generate metadata if callback is provided
            metadata = metadata_callback(file_name) if metadata_callback else None

            if upload_file(file_path, upload_url, metadata):
                os.remove(file_path)  # Remove file after successful upload
                print(f"Deleted: {file_path}")
            else:
                print(f"Retry needed for: {file_path}")
                break

def generate_metadata(file_name):
    """
    Generate metadata for a given video file.

    Args:
        file_name (str): Name of the video file.

    Returns:
        dict: Metadata including filename, GPS, timestamp, etc.
    """
    # Example metadata
    metadata = {
        "filename": file_name,
        "timestamp": file_name.split('_')[0],  # Assuming filename starts with a timestamp
        "gps_coordinates": get_current_gps(),  # Stub function for GPS data
        "device_id": "raspberry_pi_4",  # Example device identifier
    }
    return metadata

def get_current_gps():
    """
    Stub function to fetch current GPS data.

    Returns:
        dict: GPS coordinates with latitude and longitude, or None if unavailable.
    """
    # Example GPS coordinates
    return {
        "latitude": 37.7749,
        "longitude": -122.4194
    }

def retry_failed_uploads(video_folder, upload_url, retry_limit=3, metadata_callback=None):
    """
    Retry uploading files in the event of previous failures.

    Args:
        video_folder (str): Directory containing video files.
        upload_url (str): URL of the server to upload to.
        retry_limit (int): Maximum number of retries for each file.
        metadata_callback (callable): Function to generate metadata for each file.

    Returns:
        None
    """
    for _ in range(retry_limit):
        pending_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]
        if not pending_files:
            print("All files uploaded successfully.")
            break
        upload_pending_files(video_folder, upload_url, metadata_callback)

