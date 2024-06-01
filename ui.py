from tkinter import ttk, filedialog, StringVar
from tkinter import *
import os
import time

class DownloaderUi:
    def __init__(self, downloader):
        self.downloader = downloader

        # Create main window
        root = Tk()

        self.root = root
        root.title("YtDownloader")
        root.geometry("900x600")
        root.configure(bg="#2b2b2b")
        root.resizable(False, False)

        # Set custom styles
        style = ttk.Style()
        style.theme_use("clam")


        style.configure("TLabel", foreground="white", background="#2b2b2b", font=("Roboto", 14))
        style.configure("TButton", foreground="white", background="#4a4a4a", font=("Roboto", 12), padding=6)
        style.configure("TEntry", foreground="black", background="#3a3a3a", font=("Roboto", 12), padding=6)
        style.configure("blue.Horizontal.TProgressbar", foreground="green", background="blue")
         
        

        # Title label
        title_label = ttk.Label(root, text="YtDownloader", font=("Roboto", 20, "bold"), anchor="center")
        title_label.pack(pady=10)

        # URL entry
        self.link_entry_var = StringVar()
        self.link_entry = ttk.Entry(root, textvariable=self.link_entry_var, style="TEntry")
        self.link_entry.pack(pady=20, padx=40, fill='x')

        # Set placeholder text
        self.link_entry_var.set("Put YouTube link here...")
        self.link_entry.bind("<FocusIn>", self.clear_placeholder)
        self.link_entry.bind("<FocusOut>", self.set_placeholder)

        # Button frame
        button_frame = Frame(root, bg="#2b2b2b")
        button_frame.pack(pady=10)

        # Common button width
        button_width = 20

        # Directory button
        directory_button = ttk.Button(button_frame, text="Set Directory", command=self.set_directory, style="TButton", width=button_width)
        directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Open downloads button
        open_downloads_button = ttk.Button(button_frame, text="Open Downloads Folder", command=self.open_downloads_folder, style="TButton", width=button_width)
        open_downloads_button.grid(row=0, column=1, padx=5, pady=5)

        # Download MP3 button
        download_mp3_button = ttk.Button(button_frame, text="Download MP3", command=self.download_mp3, style="TButton", width=button_width)
        download_mp3_button.grid(row=1, column=0, padx=5, pady=5)

        # Download MP4 button
        download_mp4_button = ttk.Button(button_frame, text="Download MP4", command=self.download_mp4, style="TButton", width=button_width)
        download_mp4_button.grid(row=1, column=1, padx=5, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress["style"] = "blue.Horizontal.TProgressbar"
        self.progress.pack(pady=20)

        # Message label
        self.message_label = ttk.Label(root, text="", style="TLabel", anchor="center", font=("Roboto", 12))
        self.message_label.pack(pady=10)

        # Download finished label
        self.finished_label = ttk.Label(root, text="", style="TLabel", anchor="center")
        self.finished_label.pack(pady=10)

        root.mainloop()

    def clear_placeholder(self, event):
        if self.link_entry_var.get() == "Put YouTube link here...":
            self.link_entry_var.set("")
            self.link_entry.configure(foreground="black")

    def set_placeholder(self, event):
        if self.link_entry_var.get() == "":
            self.link_entry_var.set("Put YouTube link here...")
            self.link_entry.configure(foreground="black")

    def set_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.downloader.set_path(directory)
            self.show_message(f"Download directory set to: {directory}", "info")

    def open_downloads_folder(self):
        if self.downloader.path:
            os.startfile(self.downloader.path)
        else:
            self.show_message("Download directory not set.", "error")

    def download_mp3(self):
        url = self.link_entry_var.get()
        if url:
            self.progress["value"] = 0
            self.finished_label.config(text="")
            try:
                if "playlist?list=" in url:
                    self.downloader.download_playlist_mp3(url, self.update_progress)
                else:
                    self.downloader.download_mp3(url, self.update_progress)
                self.finished_label.config(text="Download finished!")
                # Schedule clearing of progress bar after 2 seconds
                
            except Exception as e:
                self.show_message(str(e), "error")
        else:
            self.show_message("No URL provided.", "error")
        time.sleep(1)
        self.progress["value"] = 0
        
    def download_mp4(self):
        url = self.link_entry_var.get()
        if url:
            self.progress["value"] = 0
            self.finished_label.config(text="")
            try:
                if "playlist?list=" in url:
                    self.downloader.download_playlist_mp4(url, self.update_progress)
                else:
                    self.downloader.download_mp4(url, self.update_progress)
                self.finished_label.config(text="Download finished!")
                # Schedule clearing of progress bar after 2 seconds
                
            except Exception as e:
                self.show_message(str(e), "error")
        else:
            self.show_message("No URL provided.", "error")
        time.sleep(1)
        self.progress["value"] = 0

    def update_progress(self, stream=None, chunk=None, bytes_remaining=None):
        if bytes_remaining is not None and stream is not None:
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / total_size * 100
            self.progress["value"] = percentage_of_completion
            self.progress.update()
            

    def show_message(self, message, msg_type="info"):
        if msg_type == "info":
            self.message_label.config(text=message, foreground="white")
        elif msg_type == "error":
            self.message_label.config(text=message, foreground="red")
