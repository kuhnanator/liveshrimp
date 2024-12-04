import os
import time
import subprocess
import requests
from schedule import every, run_pending

def check_connectivity(url="http://google.com", timeout=5):
    """
    Check internet connectivity by pinging a URL.

    Args:
        url (str): URL to test connectivity. Default is Google.
        timeout (int): Timeout for the request in seconds.

    Returns:
        bool: True if connected, False otherwise.
    """
    try:
        requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def start_live_stream(camera_stream_url, restreamer_url):
    """
    Start live streaming to a given URL using FFmpeg.

    Args:
        camera_stream_url (str): Local stream URL of the camera (e.g., Pi camera).
        restreamer_url (str): Destination URL for live streaming.

    Returns:
        subprocess.Popen: A subprocess running the FFmpeg command.
    """
    command = [
        "ffmpeg",
        "-i", camera_stream_url,  # Input stream from the camera
        "-c:v", "libx264",  # Encode video with H.264 codec
        "-preset", "veryfast",  # FFmpeg encoding preset
        "-f", "flv",  # Output format
        restreamer_url  # Destination for live stream
    ]
    return subprocess.Popen(command)

def upload_video(file_path, upload_url):
    """
    Upload a video file to a specified URL.

    Args:
        file_path (str): Path to the video file to be uploaded.
        upload_url (str): URL where the video will be uploaded.

    Returns:
        bool: True if upload was successful, False otherwise.
    """
    try:
        with open(file_path, 'rb') as video_file:
            response = requests.post(upload_url, files={"file": video_file})
            response.raise_for_status()
        print(f"Uploaded: {file_path}")
        return True
    except requests.RequestException as e:
        print(f"Upload failed for {file_path}: {e}")
        return False

def upload_offline_videos(video_folder, upload_url):
    """
    Upload all locally saved video segments when connectivity is available.

    Args:
        video_folder (str): Path to the folder containing video files.
        upload_url (str): URL where the videos will be uploaded.
    """
    for file_name in sorted(os.listdir(video_folder)):
        if file_name.endswith(".mp4"):
            file_path = os.path.join(video_folder, file_name)
            if upload_video(file_path, upload_url):
                os.remove(file_path)  # Delete the file after successful upload
                print(f"Deleted: {file_path}")
            else:
                print(f"Retry needed for: {file_path}")
                break

def manage_network(camera_stream_url, restreamer_url, video_folder, upload_url, check_interval=10):
    """
    Manage live streaming and video uploads based on network status.

    Args:
        camera_stream_url (str): Local stream URL of the camera (e.g., Pi camera).
        restreamer_url (str): Destination URL for live streaming.
        video_folder (str): Path to the folder containing offline video files.
        upload_url (str): URL for uploading video files.
        check_interval (int): Interval (in seconds) to check network connectivity.
    """
    is_streaming = False
    ffmpeg_process = None

    while True:
        if check_connectivity():
            if not is_streaming:
                print("Starting live stream...")
                ffmpeg_process = start_live_stream(camera_stream_url, restreamer_url)
                is_streaming = True

            # Upload offline videos in the background
            upload_offline_videos(video_folder, upload_url)
        else:
            if is_streaming:
                print("Stopping live stream due to lost connectivity...")
                if ffmpeg_process:
                    ffmpeg_process.terminate()
                    ffmpeg_process = None
                is_streaming = False

        time.sleep(check_interval)

# Scheduled task to retry offline uploads
def schedule_offline_uploads(video_folder, upload_url):
    """
    Schedule uploads of offline videos to run periodically.

    Args:
        video_folder (str): Path to the folder containing offline video files.
        upload_url (str): URL for uploading video files.
    """
    every(10).minutes.do(upload_offline_videos, video_folder, upload_url)
    while True:
        run_pending()
        time.sleep(1)
