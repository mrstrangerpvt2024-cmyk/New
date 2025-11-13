"""
Get video attributes and thumbnail
Optimized for lightweight and fast processing
"""

import subprocess


def get_video_attributes(file_path: str):
    """
    Returns video duration (seconds), width, height
    """
    try:
        # Run ffprobe to get video info
        cmd = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().splitlines()
        
        if len(output) >= 3:
            width = int(output[0])
            height = int(output[1])
            duration = float(output[2])
            return {"width": width, "height": height, "duration": duration}
        else:
            return {"width": 0, "height": 0, "duration": 0.0}

    except subprocess.CalledProcessError as e:
        print(f"Error getting video info: {e.output.decode()}")
        return {"width": 0, "height": 0, "duration": 0.0}


def get_video_thumbnail(file_path: str, thumbnail_path: str, time: float = 1.0):
    """
    Extracts a thumbnail from the video at the given time (in seconds)
    """
    try:
        cmd = [
            "ffmpeg",
            "-y",  # overwrite output
            "-i", file_path,
            "-ss", str(time),
            "-vframes", "1",
            thumbnail_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return thumbnail_path
    except subprocess.CalledProcessError:
        return None
