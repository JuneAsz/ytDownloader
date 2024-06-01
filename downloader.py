from pytube import YouTube, Playlist
from converter import convert
import os
import re

class Downloader:
    def __init__(self):
        self.url = None
        self.path = None
        
    def set_path(self, path: str):
        self.path = path
        self.check_and_create_path()

    def check_and_create_path(self):
        if self.path and not os.path.exists(self.path):
            os.makedirs(self.path)
            print(f"Path '{self.path}' created.")
        elif self.path:
            print(f"Path '{self.path}' already exists.")
        else:
            print("No path set.")

    def clean_file_name(self, filename: str):
        cleaned_filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        return cleaned_filename


    def download_mp3(self, url: str, progress_callback=None):
        try:
            yt = YouTube(url, on_progress_callback=progress_callback)
            audio_stream = yt.streams.filter(only_audio=True).first()

            # Modify title to remove invalid characters
            modified_title = self.clean_file_name(yt.title)

            mp4_file_path = os.path.join(self.path, f"{modified_title}.{audio_stream.subtype}")
            mp3_file_path = os.path.join(self.path, f"{modified_title}.mp3")
            
            if os.path.isfile(mp3_file_path):
                print(f"File '{modified_title}' already exists.")
                raise FileExistsError(f"File already exists at: {mp3_file_path}")
            
            audio_stream.download(output_path=self.path, filename=f"{modified_title}.{audio_stream.subtype}")
            convert(mp4_file_path, mp3_file_path)
        except Exception as e:
            print(f"Error: {e}")

    def download_mp4(self, url: str, progress_callback=None):
        try:
            yt = YouTube(url, on_progress_callback=progress_callback)
            # Modify title to remove invalid characters
            modified_title = self.clean_file_name(yt.title)

            mp4_file_path = os.path.join(self.path, f"{modified_title}.mp4")
            
            if os.path.exists(mp4_file_path):
                print(f"File '{modified_title}' already exists.")
                return

            yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").first().download(output_path=self.path, filename=f"{modified_title}.mp4")
        except Exception as e:
            print(f"Error: {e}")

    def download_playlist_mp3(self, url: str, progress_callback=None):
        try:
            playlist = Playlist(url)
            total_videos = len(playlist.videos)
            for index, video in enumerate(playlist.videos):
                modified_title = self.clean_file_name(video.title)

                mp3_file_path = os.path.join(self.path, f"{modified_title}.mp3")
                
                if os.path.exists(mp3_file_path):
                    print(f"File '{modified_title}' already exists.")
                    continue

                audio_stream = video.streams.filter(only_audio=True).first()
                audio_stream.download(output_path=self.path, filename=f"{modified_title}.{audio_stream.subtype}")
                mp4_file_path = os.path.join(self.path, f"{modified_title}.{audio_stream.subtype}")
                convert(mp4_file_path, mp3_file_path)

                if progress_callback:
                    progress_callback(index+1 / total_videos * 100)

        except Exception as e:
            print(f"Error: {e}")

    def download_playlist_mp4(self, url: str, progress_callback=None):
        try:
            playlist = Playlist(url)
            for video in playlist.videos:
                # Modify title to remove invalid characters
                modified_title = self.clean_file_name(video.title)

                mp4_file_path = os.path.join(self.path, f"{modified_title}.mp4")
                
                if os.path.exists(mp4_file_path):
                    print(f"File '{modified_title}' already exists.")
                    continue

                video.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").first().download(output_path=self.path, filename=f"{modified_title}.mp4")
        except Exception as e:
            print(f"Error: {e}")

        