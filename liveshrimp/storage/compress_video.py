import os
import subprocess

def compress_video(input_file, output_file, resolution="640x360", bitrate="1M"):
    """
    Compress a video using FFmpeg.

    Args:
        input_file (str): Path to the input video file.
        output_file (str): Path to save the compressed video file.
        resolution (str): Target resolution (e.g., "640x360").
        bitrate (str): Target bitrate (e.g., "1M" for 1 Mbps).

    Returns:
        bool: True if compression is successful, False otherwise.
    """
    try:
        # Command to compress video using FFmpeg
        command = [
            "ffmpeg", "-i", input_file,
            "-vf", f"scale={resolution}",
            "-b:v", bitrate,
            "-c:v", "libx264",
            "-preset", "fast",
            "-c:a", "aac",
            "-strict", "experimental",
            "-movflags", "faststart",  # Optimize for streaming
            output_file
        ]
        # Run the command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Compressed: {input_file} -> {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to compress {input_file}: {e}")
        return False

def compress_all_videos(input_folder, output_folder, resolution="640x360", bitrate="1M"):
    """
    Compress all video files in a folder.

    Args:
        input_folder (str): Directory containing videos to compress.
        output_folder (str): Directory to save compressed videos.
        resolution (str): Target resolution (e.g., "640x360").
        bitrate (str): Target bitrate (e.g., "1M").

    Returns:
        None
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".mp4"):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, f"compressed_{file_name}")
            compress_video(input_file, output_file, resolution, bitrate)

def delete_original_files(input_folder):
    """
    Delete original video files after compression.

    Args:
        input_folder (str): Directory containing original videos.

    Returns:
        None
    """
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".mp4") and not file_name.startswith("compressed_"):
            os.remove(os.path.join(input_folder, file_name))
            print(f"Deleted original: {file_name}")
