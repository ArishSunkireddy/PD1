import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from dotenv import load_dotenv
import os
from openai import OpenAI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading

# Load API keys
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-read-private"
))

# Core logic
def get_songs(playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id)
    return "\n".join(
        f"'{item['track']['name']}' by {item['track']['artists'][0]['name']}"
        for item in results['items']
    )

def analyze_persona(songs):
    prompt = (
        "You are a personality psychologist and cultural analyst. "
        "Analyze the user's personality based on this playlist:\n\n" + songs
    )
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful personality analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return completion.choices[0].message.content.strip()

# Submit handler
def on_submit():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Missing URL", "Please paste a Spotify playlist URL.")
        return

    result_label.config(text="Analyzing...")
    analyze_button.config(state="disabled")

    def process():
        try:
            songs = get_songs(url)
            result = analyze_persona(songs)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, result)
            result_label.config(text="Analysis Complete:")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            analyze_button.config(state="normal")

    threading.Thread(target=process).start()

# GUI setup
root = tk.Tk()
root.title("Playlist Personality")
root.geometry("600x500")

# Load and display background image
try:
    bg_image = Image.open("spotify_ui.png")
    bg_image = bg_image.resize((600, 500), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relx=0.5, rely=0.5, anchor="center")
    bg_label.lower()  # send to back
except Exception as e:
    print("Background image not loaded:", e)

# Overlay UI elements
header = tk.Label(root, text="Playlist Personality", font=("Helvetica", 22, "bold"), bg="#1DB954", fg="white")
header.place(relx=0.5, y=30, anchor="center")

tk.Label(root, text="Paste your Spotify playlist URL:",
         font=("Helvetica", 12), bg="#1DB954", fg="white").place(relx=0.5, y=80, anchor="center")

url_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
url_entry.place(relx=0.5, y=110, anchor="center")

analyze_button = tk.Button(root, text="Analyze", bg="black", fg="white",
                           font=("Helvetica", 12, "bold"), command=on_submit)
analyze_button.place(relx=0.5, y=150, anchor="center")

result_label = tk.Label(root, text="", bg="#1DB954", fg="white", font=("Helvetica", 12, "bold"))
result_label.place(relx=0.5, y=190, anchor="center")

result_text = tk.Text(root, wrap=tk.WORD, height=15, width=70, font=("Helvetica", 10))
result_text.place(x=30, y=220)

root.mainloop()
