import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube
from moviepy.editor import VideoFileClip

def download_video(url, output_path, audio_only=False):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=audio_only).first() if audio_only else yt.streams.get_highest_resolution()
    output_file = video.download(output_path)
    
    if audio_only:
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)
        return new_file
    return output_file

def convert_to_audio(video_path):
    video = VideoFileClip(video_path)
    audio_path = video_path.rsplit('.', 1)[0] + '.mp3'
    video.audio.write_audiofile(audio_path)
    video.close()
    return audio_path

def start_download():
    url = url_entry.get()
    output_path = filedialog.askdirectory()
    if not url or not output_path:
        messagebox.showerror("Erro", "Por favor, preencha a URL e selecione o diretório de saída.")
        return
    audio_only = audio_only_var.get()
    try:
        downloaded_video = download_video(url, output_path, audio_only)
        if not audio_only:
            convert_to_audio(downloaded_video)
        messagebox.showinfo("Sucesso", "Download concluído!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

app = tk.Tk()
app.title("Downloader de Vídeos")
app.geometry("650x300")

# Define a cor de fundo
background_color = "#e1f5fe"
highlight_color = "#00e676"
text_color = "#212121"
entry_bg_color = "#f5f5f5"
border_color = "#bdbdbd"

# Estilo
style = ttk.Style()
style.configure("TLabel", padding=6, font=("Helvetica", 12))
style.configure("TButton", padding=6, font=("Helvetica", 12))
style.configure("TEntry", padding=6, font=("Helvetica", 12))

# Layout
frame = ttk.Frame(app, padding="10 10 10 10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
frame.configure(style="TFrame")


# Widgets
title = ttk.Label(frame, text="URL do Vídeo:").grid(column=1, row=1, sticky=tk.W, pady=(0, 10))
url_entry = ttk.Entry(frame, width=50)
url_entry.grid(column=2, row=1, sticky=(tk.W, tk.E), pady=(0, 10))

audio_only_var = tk.BooleanVar()
audio_only_checkbutton = ttk.Checkbutton(frame, text="Apenas Áudio (MP3)", variable=audio_only_var)
audio_only_checkbutton.grid(column=2, row=2, sticky=tk.W, pady=(0, 10))

download_button = ttk.Button(frame, text="Baixar", command=start_download)
download_button.grid(column=2, row=3, pady=20)

# Ajuste de espaçamento
for child in frame.winfo_children():
    child.grid_configure(padx=10, pady=5)


app.mainloop()
