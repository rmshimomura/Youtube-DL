from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import requests
from downloader import download
from utils import return_video_name
from tkinter.ttk import Combobox
import os


class App(Tk):

    def __init__(self):

        super().__init__()
        self.title('Gerar relatórios das clínicas')
        self.geometry("900x460")
        self.configure(background='#FFFFFF')

        self.output_path = None
        self.urls = {}

        self.audio_formats = {
            '.flac': 'flac',
            '.mp3': 'mp3',
            '.wav': 'wav',
            '.aac': 'aac',
            '.m4a': 'm4a',
        }

        self.start_paths()
        self.render_widgets()

    def start_paths(self):

        if os.path.isfile(f'./default_output_path.txt'):
            self.output_path = open("default_output_path.txt", "r").read()

        if self.output_path is not None:
            self.current_output_path = Label(
                self, text=f"Pastas de saída: {self.output_path}", bg="white")
            self.current_output_path.grid(
                row=3, column=0, pady=10, columnspan=3, sticky="W")

    def store_output_path(self):

        self.output_path = filedialog.askdirectory(
            title="Selecione a pasta de saída: ")

        if self.output_path is not None and self.output_path != "":
            open("default_output_path.txt", "w").write(self.output_path)
        else:
            if os.path.isfile(f'./default_output_path.txt'):
                self.output_path = open("default_output_path.txt", "r").read()

        if self.output_path is not None and self.output_path != "":
            self.current_output_path = Label(
                self, text=f"Pasta de saída: {self.output_path}", bg="white")
            self.current_output_path.grid(
                row=3, column=0, pady=10, columnspan=3, sticky="W")

    def addURL(self, event):

        if self.url.get() != "": # Check if the url is not empty

            if self.url.get() not in self.urls: # Check if the url is not already in the list

                if self.url.get().startswith("https://www.youtube.com/watch?v="): # Check if the url is a valid youtube url

                    if requests.get(self.url.get()).status_code == 200: # Check if the url is valid

                        video_name = return_video_name(self.url.get())

                        self.urls[self.url.get()] = video_name # Add the url to the list

                        messagebox.showinfo('Sucesso', f'Link para o vídeo "{video_name}" adicionado!') # Show a message to the user

    def render_buttons(self):

        self.out_dir = Button(self, text="Selecione a pasta de saída...",
                              command=self.store_output_path, height=6, width=60, borderwidth=0)
        self.out_dir.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.out_dir.configure(background="#ff6e6c")

        self.format_selected = Combobox(self, values=list(
            self.audio_formats.keys()), state="readonly", width=60)
        self.format_selected.set("Selecione formato desejado...")
        self.format_selected.grid(
            row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.format_selected.configure(background="#ff6e6c")

        self.open_output_dir = Button(self, text="Abrir pasta de downloads", command=lambda: os.startfile(
            self.output_path), height=6, width=60, borderwidth=0)
        self.open_output_dir.grid(
            row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.open_output_dir.configure(background="#ff6e6c")
        
        self.execute_action = Button(self, text="Baixar músicas", command=lambda: download(
            self.urls.keys(), self.audio_formats[self.format_selected.get()], self.output_path), height=6, width=60, borderwidth=0)
        self.execute_action.grid(
            row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.execute_action.configure(background="#ff6e6c")

    def render_widgets(self):

        self.url = StringVar()
        self.url.set("")

        self.enter_videos = Entry(
            self, width=60, borderwidth=3, textvariable=self.url)
        self.enter_videos.bind('<Return>', self.addURL)
        self.enter_videos.grid(row=0, column=0, pady=10,
                               padx=10, columnspan=1, sticky="W")

        self.render_buttons()

        self.resizable(width="false", height="false")

if __name__ == "__main__":
    app = App()
    app.mainloop()
