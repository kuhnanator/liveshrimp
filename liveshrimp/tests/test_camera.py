import argparse
import cv2
import picamera
import picamera.array
import time

def pi_cam_to_monitor():
    """Display live feed from the Pi Camera on the monitor."""
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        with picamera.array.PiRGBArray(camera) as output:
            for frame in camera.capture_continuous(output, format="bgr", use_video_port=True):
                image = frame.array
                cv2.imshow("Pi Camera - Monitor", image)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit on 'q' key press
                    break
                output.truncate(0)
    cv2.destroyAllWindows()

def pi_cam_to_stream():
    """Stream live feed from the Pi Camera to a server."""
    # Placeholder for streaming logic (e.g., using FFmpeg or RTMP setup)
    print("Pi Camera streaming is not yet implemented.")
    # Future: Integrate with FFmpeg or a streaming library.

def other_cam_to_monitor(camera_index=0):
    """Display live feed from an external camera (e.g., USB webcam) on the monitor."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open the external camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame from external camera.")
            break
        cv2.imshow("External Camera - Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit on 'q' key press
            break
    cap.release()
    cv2.destroyAllWindows()

def other_cam_to_stream(camera_index=0):
    """Stream live feed from an external camera (e.g., USB webcam) to a server."""
    # Placeholder for streaming logic (e.g., using FFmpeg or RTMP setup)
    print("External camera streaming is not yet implemented.")
    # Future: Integrate with FFmpeg or a streaming library.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test different camera modes.")
    parser.add_argument(
        "mode", 
        choices=["pi_cam_monitor", "pi_cam_stream", "other_cam_monitor", "other_cam_stream"],
        help="Select the camera test mode."
    )
    parser.add_argument(
        "--camera_index", 
        type=int, 
        default=0, 
        help="Index of the external camera (default is 0)."
    )
    args = parser.parse_args()

    if args.mode == "pi_cam_monitor":
        pi_cam_to_monitor()
    elif args.mode == "pi_cam_stream":
        pi_cam_to_stream()
    elif args.mode == "other_cam_monitor":
        other_cam_to_monitor(args.camera_index)
    elif args.mode == "other_cam_stream":
        other_cam_to_stream(args.camera_index)
    else:
        print("Invalid mode selected.")
