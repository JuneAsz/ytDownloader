# ytDownloader
A simple youtube downloader, uses pytube, ffmpy (to autoconvert mp4 to mp3) and tkinter ^_^ (needs ffmpeg, can get it from here: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z), add /bin/ to PATH

Guide:

open terminal in directory:

1. python -m pip install -r requirements.txt
2. python main.py

set download directory -> put in link -> press download mp3/mp4 (works with shorts, singular videos and playlists)
if you want - you can use pyinstaller (pip install pyinstaller) and build it into .exe (pyinstaller main.py) - in same directory, take exe from /dist/
