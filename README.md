# YouTube Video Frame Extractor

This script allows you to extract frames from a YouTube video between the specified start and end times. It also provides options to generate a GIF from the extracted frames and save a meta file with video information.

## Requirements

- Python 3.x
- OpenCV (cv2)
- imageio
- yt_dlp

Install the required dependencies using the following command:

pip install opencv-python imageio yt_dlp

## Usage

python yt_frames.py <youtube_url> <start_time> <end_time> [--frame_interval <interval>] [--remove_video] [--generate_gif] [--gif_duration <duration>] [--save_meta]

- `<youtube_url>`: The URL of the YouTube video.
- `<start_time>`: The start time in the format `mm:ss` or `mm:ss.ss`.
- `<end_time>`: The end time in the format `mm:ss` or `mm:ss.ss`.
- `--frame_interval <interval>` (optional): The interval between extracted frames. Default is the maximum framerate.
- `--remove_video` (optional): Remove the downloaded video after processing.
- `--generate_gif` (optional): Create a GIF from the extracted frames.
- `--gif_duration <duration>` (optional): Duration (in milliseconds) per frame in the GIF. Default is 100 milliseconds.
- `--save_meta` (optional): Save a meta file with video information.

The extracted frames will be saved in a folder named `frames` by default. If the video title can be fetched, the output folder will be named after the video title.

## Examples

Extract frames from a YouTube video between 00:01 and 00:10:

    python yt_frames.py https://www.youtube.com/watch?v=<video_id> 00:01 00:10

Extract frames with a frame interval of 2:

    python yt_frames.py https://www.youtube.com/watch?v=<video_id> 00:00 01:00 --frame_interval 2

Create a GIF from the extracted frames:

    python yt_frames.py https://www.youtube.com/watch?v=<video_id> 00:00 00:10 --generate_gif

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
