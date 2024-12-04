import cv2
import time
import json
import os
import schedule
import threading
from camera_handler import start_camera, stop_camera
from gps_utils import get_gps_data
from battery_monitor import check_battery
from storage_handler import save_video_segment, manage_storage
from network_handler import check_network_connection, upload_video
from compress_video import compress_video
from overlay import overlay_gps_data, overlay_battery_status

# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize global variables
camera = None
video_writer = None
video_segment_count = 0
is_recording = False
gps_data = ""
battery_status = ""
video_storage_path = "/home/pi/videos/"

# Initialize camera
def initialize_camera():
    global camera
    camera = start_camera()

# Check battery status and network connection
def check_device_status():
    global battery_status
    battery_status = check_battery()  # Returns battery percentage or status (e.g., charging/discharging)

    # If network is available, upload the videos
    if check_network_connection():
        print("Network connected, uploading video...")
        upload_video(video_storage_path)
    else:
        print("No network connection. Saving videos locally.")

# Capture video
def capture_video():
    global video_writer, video_segment_count, is_recording
    print("Starting video capture...")

    # Set up video file
    video_segment_count += 1
    output_file = f"{video_storage_path}/video_segment_{video_segment_count}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for .mp4 files
    video_writer = cv2.VideoWriter(output_file, fourcc, 30.0, (1920, 1080))

    # Capture frames from the camera
    while is_recording:
        ret, frame = camera.read()
        if not ret:
            break

        # Get GPS data and overlay it on the video
        gps_data = get_gps_data()
        frame_with_overlay = overlay_gps_data(frame, gps_data)

        # Add battery status overlay
        frame_with_overlay = overlay_battery_status(frame_with_overlay, battery_status)

        # Write the frame with overlays to video file
        video_writer.write(frame_with_overlay)

        # Check device status periodically
        check_device_status()

    # Release resources
    video_writer.release()

# Stop video capture
def stop_video_capture():
    global is_recording
    is_recording = False
    print("Stopping video capture...")

# Schedule periodic tasks (e.g., checking battery, storage management)
def schedule_tasks():
    schedule.every(5).minutes.do(manage_storage)  # Manage storage every 5 minutes
    schedule.every(10).minutes.do(check_device_status)  # Check battery and network every 10 minutes

    while True:
        schedule.run_pending()
        time.sleep(1)

# Main function to start the process
def main():
    # Initialize camera
    initialize_camera()

    # Start recording video (by default, it starts recording on launch)
    global is_recording
    is_recording = True
    video_thread = threading.Thread(target=capture_video)
    video_thread.start()

    # Start scheduled tasks (battery check, storage management, etc.)
    schedule_thread = threading.Thread(target=schedule_tasks)
    schedule_thread.start()

    try:
        # Keep running the main loop while recording is active
        while is_recording:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Terminating the video recording...")
        stop_video_capture()
        camera.release()

if __name__ == "__main__":
    main()
