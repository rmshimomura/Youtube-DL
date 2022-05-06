from tkinter import messagebox
import yt_dlp

def download(URLS, FORMAT, SAVE_PATH):

    ydl_opts = {

        'format': 'flac/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': f'{FORMAT}',
        }],
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)

    if error_code == 0:
        messagebox.showinfo("Download", "Download terminado!")
    else:
        messagebox.showerror("Download", "Erro no Download!")