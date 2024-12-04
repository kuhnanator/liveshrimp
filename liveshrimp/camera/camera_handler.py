import cv2
import time
import logging
from pathlib import Path

# Set up logging
logger = logging.getLogger(__name__)

def start_camera(resolution=(1920, 1080), output_dir="segments/"):
    """
    Initializes the camera and ensures the output directory exists.

    Args:
        resolution (tuple): Video resolution (width, height).
        output_dir (str): Directory to save video files.

    Returns:
        cv2.VideoCapture: The camera object.
    """
    # Ensure the output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Initialize the camera
    camera = cv2.VideoCapture(0)  # Use Pi camera or default camera
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
    camera.set(cv2.CAP_PROP_FPS, 30)  # Set frame rate

    if not camera.isOpened():
        logger.error("Failed to open the camera.")
        raise RuntimeError("Camera initialization failed.")

    logger.info("Camera initialized successfully.")
    return camera

def stop_camera(camera):
    """
    Safely releases the camera resource.

    Args:
        camera (cv2.VideoCapture): The camera object to release.
    """
    if camera:
        camera.release()
        cv2.destroyAllWindows()
        logger.info("Camera stopped and resources released.")

def record_segment(camera, output_dir="segments/", duration=60):
    """
    Records a video segment and saves it to the output directory.

    Args:
        camera (cv2.VideoCapture): The camera object.
        output_dir (str): Directory to save the video.
        duration (int): Duration of the video segment in seconds.

    Returns:
        str: The filepath of the saved video.
    """
    # Generate unique filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepath = f"{output_dir}/segment_{timestamp}.mp4"

    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MPEG-4 codec
    fps = 30
    resolution = (
        int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )
    out = cv2.VideoWriter(filepath, fourcc, fps, resolution)

    logger.info(f"Recording video segment: {filepath}")

    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = camera.read()
        if not ret:
            logger.error("Failed to read frame from camera.")
            break
        out.write(frame)

    out.release()
    logger.info(f"Video segment saved: {filepath}")
    return filepath
