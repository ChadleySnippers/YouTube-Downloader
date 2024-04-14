import os  
import requests  
from tqdm import tqdm  
from pytube import YouTube  
from pytube.exceptions import RegexMatchError, VideoUnavailable  

def download_video(url):
    if not url:
        print("Error: You did not enter a URL.")
        return False

    try:
        yt = YouTube(url)
    except (RegexMatchError, VideoUnavailable):
        print("Error: The provided URL does not correspond to a valid YouTube video.")
        return False

    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'ytDownloads')
    os.makedirs(download_folder, exist_ok=True)  

    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    if video is None:
        print("Error: No downloadable video found for this URL.")
        return False

    total_size = video.filesize  

    response = requests.get(video.url, stream=True)  
    with open(os.path.join(download_folder, f"{yt.title}.mp4"), 'wb') as f:  
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=yt.title, ncols=100) as pbar:  
            for chunk in response.iter_content(chunk_size=1024):  
                if chunk:
                    f.write(chunk)  
                    pbar.update(len(chunk))  

    print(f"Download complete. Video saved to: {download_folder}")  
    return True

if __name__ == "__main__":
    while True:
        url = input("Enter the YouTube video URL (or type 'exit' to quit): ")
        if url.lower() == 'exit':
            break
        if download_video(url):
            break
