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

    ### System section ###

        super().__init__()
        self.title('Baixar músicas do YouTube')
        self.geometry("900x500")
        self.configure(background='#FFFFFF')

        self.output_path = None
        self.urls = {}
        self.list_of_urls = None

        self.audio_formats = {
            'Selecione formato desejado...': 0,
            '.flac': 'flac',
            '.mp3': 'mp3',
            '.wav': 'wav',
            '.aac': 'aac',
            '.m4a': 'm4a',
        }

        self.start_paths()
        self.render_url_input()

    def start_paths(self):

        if os.path.isfile(f'./default_output_path.txt'):
            self.output_path = open("default_output_path.txt", "r").read()

    def store_output_path(self):

        self.output_path = filedialog.askdirectory(
            title="Selecione a pasta de saída: ")

        if self.output_path is not None and self.output_path != "":
            open("default_output_path.txt", "w").write(self.output_path)
        else:
            if os.path.isfile(f'./default_output_path.txt'):
                self.output_path = open("default_output_path.txt", "r").read()

    ### Events section ###

    def add_url(self, event):

        if self.url.get() != "":  # Check if the url is not empty

            if self.url.get().startswith("https://www.youtube.com/watch?v="):  # Check if the url is a valid youtube url

                if self.url.get() not in self.urls:  # Check if the url is not already in the list

                    # Check if the url is valid
                    if requests.get(self.url.get()).status_code == 200:

                        video_name = return_video_name(self.url.get())

                        # Add the url to the list
                        self.urls[self.url.get()] = video_name

                        # Show a message to the user
                        messagebox.showinfo(
                            'Sucesso', f'Link para o vídeo "{video_name}" adicionado!')

                        if len(self.urls) > 0:

                            self.links_title = Label(self, text="Links adicionados:", bg="white").grid(row=4, column=0, padx=10, pady=10, sticky="W")
                            self.list_of_urls = Listbox(self.links_title, height=10, width=60, highlightbackground = "black", highlightthickness = 2, listvariable=self.urls, selectmode=SINGLE)
                            self.list_of_urls.bind('<Button-3>', self.remove_url)
                            
                            for url in self.urls.values():
                                self.list_of_urls.insert(END, url)
                            self.list_of_urls.grid(
                                row=5, column=0, padx=10, pady=10, sticky="W")
                            self.list_of_urls.configure(background="#ffffff")
                    else:
                        messagebox.showerror('Erro', 'Link inválido!')
                else:
                    messagebox.showerror('Erro', 'Link já adicionado!')
            else:
                messagebox.showerror('Erro', 'Link inválido!')

    def remove_url(self, event):

        if messagebox.askokcancel("Confirmação", "Deseja remover o link?"):
            if self.list_of_urls.curselection() != ():
                removed = self.list_of_urls.get(self.list_of_urls.curselection())
                self.list_of_urls.delete(self.list_of_urls.curselection())
                del self.urls[list(self.urls.keys())[list(self.urls.values()).index(removed)]]

    ### Render section ###

    def render_buttons(self):

        self.out_dir = Button(self, text=f"Selecione a pasta de saída...{chr(10) + chr(10) + 'Atual --> ' + self.output_path if self.output_path is not None and self.output_path != '' else ''}", command=self.store_output_path, height=6, width=60, borderwidth=0)
        self.out_dir.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.out_dir.configure(background="#ff6e6c")

        self.format_selected = Combobox(self, values=list(self.audio_formats.keys()), state="readonly", width=60)
        self.format_selected.set("Selecione formato desejado...")
        self.format_selected.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.format_selected.configure(background="#ff6e6c")

        self.open_output_dir = Button(self, text="Abrir pasta de downloads", command=lambda: os.startfile(self.output_path), height=6, width=60, borderwidth=0)
        self.open_output_dir.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.open_output_dir.configure(background="#ff6e6c")

        self.execute_action = Button(self, text="Baixar músicas", command=lambda: download(self.urls, self.audio_formats[self.format_selected.get()], self.output_path), height=6, width=60, borderwidth=0)
        self.execute_action.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.execute_action.configure(background="#ff6e6c")

    def render_url_input(self):

        self.url = StringVar()
        self.url.set("")

        self.enter_videos = Entry(self, width=60, borderwidth=3, textvariable=self.url)
        self.enter_videos.bind('<Return>', self.add_url)
        self.enter_videos.grid(row=0, column=0, pady=10, padx=10, columnspan=1, sticky="W")

        self.render_buttons()

        self.resizable(width="false", height="true")

if __name__ == "__main__":
    app = App()
    app.mainloop()
