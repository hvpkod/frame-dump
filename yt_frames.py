import argparse
import json
import os
import re
import string

import cv2
import imageio.v2 as imageio
from yt_dlp import YoutubeDL


def download_youtube_video(url, output_path):
    """
    Downloads a YouTube video given its URL.

    Args:
        url (str): The YouTube video URL.
        output_path (str): The path to save the downloaded video.

    Returns:
        str: The file name of the downloaded video.

    """

    try:
        ydl_opts = {
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info_dict)
        return file_name
    except Exception as e:
        print("Error occurred while downloading the video:", str(e))
        return None


def extract_frames(video_path, start_time, end_time, output_path, frame_interval):
    """
    Extracts frames from a video between the specified start and end times.

    Args:
        video_path (str): The path to the video file.
        start_time (str): The start time in the format "mm:ss" for frame extraction.
        end_time (str): The end time in the format "mm:ss" for frame extraction.
        output_path (str): The path to save the extracted frames.
        frame_interval (int): The interval between extracted frames.

    """
    video = cv2.VideoCapture(video_path)
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    start_frame = convert_time_to_frame(start_time, frame_rate)
    end_frame = convert_time_to_frame(end_time, frame_rate)

    frame_count = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break

        if (
            start_frame <= frame_count <= end_frame
            and frame_count % frame_interval == 0
        ):
            frame_file = os.path.join(output_path, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_file, frame)
            print("Processing", frame_file, frame_count)

        frame_count += 1

        if frame_count > end_frame:
            break

    video.release()


def convert_time_to_frame(time, frame_rate):
    """
    Converts time in the format "mm:ss" or "mm:ss.ss" to the corresponding frame number.

    Args:
        time (str): Time in the format "mm:ss" or "mm:ss.ss".
        frame_rate (float): Frame rate of the video.

    Returns:
        int: Frame number corresponding to the given time.

    """
    pattern = r"(\d+):(\d+)(\.\d+)?"
    match = re.match(pattern, time)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        milliseconds = int((float(match.group(3)) if match.group(3) else 0) * 1000)
        total_seconds = minutes * 60 + seconds + milliseconds / 1000
        frame_number = int(total_seconds * frame_rate)
        return frame_number
    else:
        raise ValueError("Invalid time format. Expected mm:ss or mm:ss.ss")


def create_output_folder(video_title):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    folder_name = "".join(c for c in video_title if c in valid_chars)
    return folder_name


def save_meta_file(output_path, url, start_time, end_time, frame_interval):
    meta = {
        "URL": url,
        "Start Time": start_time,
        "End Time": end_time,
        "Frame Interval": frame_interval,
    }
    meta_file_path = os.path.join(output_path, "meta.json")
    with open(meta_file_path, "w") as f:
        json.dump(meta, f, indent=4)
    print("Meta file saved successfully:", meta_file_path)


def generate_gif(frames_folder, output_path, gif_duration):
    frames = []
    for frame_file in sorted(os.listdir(frames_folder)):
        if frame_file.endswith(".jpg"):
            frame_path = os.path.join(frames_folder, frame_file)
            frames.append(imageio.imread(frame_path))

    frame_duration = gif_duration / len(frames)  # Calculate duration for each frame

    gif_file = os.path.join(output_path, "frames.gif")
    imageio.mimsave(gif_file, frames, duration=frame_duration, loop=0)
    print("GIF created successfully:", gif_file)


def main():
    parser = argparse.ArgumentParser(description="YouTube Video Frame Extractor")
    parser.add_argument("url", type=str, help="YouTube video URL")
    parser.add_argument("start_time", type=str, help="Start time in mm:ss format")
    parser.add_argument("end_time", type=str, help="End time in mm:ss format")
    parser.add_argument(
        "--frame_interval",
        type=int,
        default=None,
        help="Frame interval (default: maximum framerate)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output folder for extracted frames and GIF",
    )
    parser.add_argument(
        "--remove_clip",
        action="store_true",
        help="Remove the downloaded video clip after extracting frames",
    )
    parser.add_argument(
        "--save_meta",
        action="store_true",
        help="Save a meta file with video details",
    )
    parser.add_argument(
        "--create_gif",
        action="store_true",
        help="Generate a GIF from the extracted frames",
    )
    args = parser.parse_args()

    url = args.url
    start_time = args.start_time
    end_time = args.end_time
    frame_interval = args.frame_interval
    output_folder = args.output
    remove_clip = args.remove_clip
    save_meta = args.save_meta
    create_gif = args.create_gif

    if output_folder is None:
        try:
            yt = YoutubeDL().extract_info(url, download=False)
            video_title = yt.get("title", None)
            if video_title is not None:
                output_folder = create_output_folder(video_title)
            else:
                output_folder = "frames"
        except Exception as e:
            print("Failed to fetch video information:", str(e))
            print("Using default output folder.")
            output_folder = "frames"

    output_path = os.path.join(os.getcwd(), output_folder)
    os.makedirs(output_path, exist_ok=True)

    video_file = os.path.join(output_path, download_youtube_video(url, output_path))

    if frame_interval is None:
        frame_interval = 1

    extract_frames(video_file, start_time, end_time, output_path, frame_interval)

    if remove_clip:
        os.remove(video_file)

    if save_meta:
        save_meta_file(output_path, url, start_time, end_time, frame_interval)

    if create_gif:
        generate_gif(output_path, output_path, 100)


if __name__ == "__main__":
    main()
