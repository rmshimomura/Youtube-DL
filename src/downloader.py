from tkinter import messagebox
import yt_dlp

def download(URLS, FORMAT, SAVE_PATH):

    keys = URLS.keys()

    if len(keys) == 0:
        messagebox.showerror("Erro", "Nenhuma URL foi selecionada")
        return

    if FORMAT == 0:
        messagebox.showerror("Erro", "Nenhum formato foi selecionado")
        return
    
    if SAVE_PATH is None:
        messagebox.showerror("Erro", "Nenhum caminho foi selecionado")
        return

    ydl_opts = {

        'format': f'{FORMAT}/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': f'{FORMAT}',
        }],
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
        
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(keys)

    if error_code == 0:
        messagebox.showinfo("Download", "Download terminado!")
        
    else:
        messagebox.showerror("Download", "Erro no Download!")