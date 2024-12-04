import cv2
import time

def add_overlay(frame, gps_data=None, speed=None, elevation=None):
    """
    Adds overlay information (GPS, speed, elevation, time) onto a video frame.

    Args:
        frame (numpy.ndarray): The current video frame.
        gps_data (tuple or None): GPS coordinates as (latitude, longitude).
        speed (float or None): Current speed in m/s.
        elevation (float or None): Current elevation in meters.

    Returns:
        numpy.ndarray: The video frame with overlay information.
    """
    # Font settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_color = (255, 255, 255)  # White text
    thickness = 1
    line_type = cv2.LINE_AA

    # Dynamic data
    overlay_text = []
    if gps_data:
        overlay_text.append(f"GPS: {gps_data[0]:.6f}, {gps_data[1]:.6f}")
    if speed is not None:
        overlay_text.append(f"Speed: {speed:.2f} m/s")
    if elevation is not None:
        overlay_text.append(f"Elevation: {elevation:.2f} m")

    # Add time of day
    overlay_text.append(f"Time: {time.strftime('%H:%M:%S')}")

    # Overlay text on the frame
    y_offset = 20  # Start position for overlay text
    for i, text in enumerate(overlay_text):
        y_position = y_offset + (i * 25)
        cv2.putText(frame, text, (10, y_position), font, font_scale, font_color, thickness, line_type)

    return frame

def apply_overlay_to_video(input_path, output_path, gps_func, speed_func, elevation_func):
    """
    Adds overlays to an existing video file and saves the output.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the output video with overlay.
        gps_func (callable): Function returning GPS data as (latitude, longitude).
        speed_func (callable): Function returning the current speed.
        elevation_func (callable): Function returning the current elevation.
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video file.")

    # Video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Get dynamic data
        gps_data = gps_func()
        speed = speed_func()
        elevation = elevation_func()

        # Add overlay
        frame = add_overlay(frame, gps_data, speed, elevation)
        out.write(frame)

    cap.release()
    out.release()

    print(f"Video with overlay saved to {output_path}")
