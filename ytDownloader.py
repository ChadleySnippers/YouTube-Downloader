import os  # Import the os module for interacting with the operating system
import requests  # Import the requests module for making HTTP requests
from tqdm import tqdm  # Import tqdm for displaying progress bars
from pytube import YouTube  # Import YouTube class from pytube library
from pytube.exceptions import RegexMatchError, VideoUnavailable  # Import specific exceptions from pytube library

def download_video(url):
    # Check if URL is provided
    if not url:
        print("Error: You did not enter a URL.")
        return False

    try:
        # Attempt to create a YouTube object using the provided URL
        yt = YouTube(url)
    except (RegexMatchError, VideoUnavailable):
        # Handle exceptions if the URL is invalid or video is unavailable
        print("Error: The provided URL does not correspond to a valid YouTube video.")
        return False

    # Define download folder path and ensure it exists
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'ytDownloads')
    os.makedirs(download_folder, exist_ok=True)

    # Select the best available video stream to download
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    if video is None:
        # Handle case when no downloadable video is found for this URL
        print("Error: No downloadable video found for this URL.")
        return False

    total_size = video.filesize  # Get total size of the video

    # Make a request to download the video in chunks
    response = requests.get(video.url, stream=True)
    with open(os.path.join(download_folder, f"{yt.title}.mp4"), 'wb') as f:
        # Write video chunks to file and display progress using tqdm
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=yt.title, ncols=100) as pbar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

    # Notify user upon successful download
    print(f"Download complete. Video saved to: {download_folder}")
    return True

if __name__ == "__main__":
    # Main loop to repeatedly prompt for YouTube video URL until 'exit' is entered
    while True:
        url = input("Enter the YouTube video URL (or type 'exit' to quit): ")
        if url.lower() == 'exit':
            break
        if download_video(url):
            break
