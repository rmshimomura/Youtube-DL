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

    return 1 if error_code == 0 else -1