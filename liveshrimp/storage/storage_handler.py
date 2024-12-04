import os
import shutil
from datetime import datetime

# Directory structure for storing videos
STORAGE_DIR = "video_storage"

def initialize_storage():
    """
    Initialize the storage directory structure.
    Creates the base directory if it doesn't exist.
    """
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
    print(f"Storage initialized at: {STORAGE_DIR}")

def save_video_segment(segment_data, filename=None):
    """
    Save a video segment to the storage directory.

    Args:
        segment_data (bytes): The video data to save.
        filename (str): The name of the file (default: timestamp-based).

    Returns:
        str: The path of the saved file.
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.mp4"

    file_path = os.path.join(STORAGE_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(segment_data)
    print(f"Video segment saved: {file_path}")
    return file_path

def get_all_files():
    """
    Get a list of all files in the storage directory.

    Returns:
        list: List of file paths in the storage directory.
    """
    return [os.path.join(STORAGE_DIR, f) for f in os.listdir(STORAGE_DIR) if os.path.isfile(os.path.join(STORAGE_DIR, f))]

def delete_oldest_file():
    """
    Delete the oldest file in the storage directory to free up space.

    Returns:
        str: The path of the deleted file.
    """
    files = get_all_files()
    if not files:
        print("No files to delete.")
        return None

    oldest_file = min(files, key=os.path.getctime)
    os.remove(oldest_file)
    print(f"Deleted oldest file: {oldest_file}")
    return oldest_file

def check_storage_limit(max_storage_mb):
    """
    Check if the total storage exceeds a limit and delete old files if necessary.

    Args:
        max_storage_mb (int): Maximum allowed storage in megabytes.

    Returns:
        None
    """
    total_size = sum(os.path.getsize(f) for f in get_all_files()) / (1024 * 1024)  # Convert bytes to MB
    print(f"Current storage usage: {total_size:.2f} MB")

    while total_size > max_storage_mb:
        delete_oldest_file()
        total_size = sum(os.path.getsize(f) for f in get_all_files()) / (1024 * 1024)

def get_storage_stats():
    """
    Get storage statistics including total, used, and free space.

    Returns:
        dict: A dictionary with storage stats.
    """
    total, used, free = shutil.disk_usage(STORAGE_DIR)
    return {
        "total": total / (1024 * 1024),  # Convert bytes to MB
        "used": used / (1024 * 1024),
        "free": free / (1024 * 1024)
    }
