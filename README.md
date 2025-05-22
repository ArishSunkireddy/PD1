# Playlist Personality

A Spotify-powered app that analyzes your music taste to uncover your personality traits using OpenAI's GPT model.

This project lets users paste a Spotify playlist URL into a visually branded GUI (styled like Spotify), fetches song titles from the playlist using the Spotify API, and sends them to OpenAI's API for personality analysis. The result is a uniquely human, introspective breakdown of your musical identity.

---

## Features

- GUI styled with Spotify's theme (Tkinter + Pillow)
- Paste Spotify playlist URL directly
- Fetches tracks automatically via Spotipy (Spotify API)
- Uses OpenAI GPT to generate personality insights
- Displays full analysis in-app
- Uses `.env` file to securely load API keys

---

## 📥 How It Works

1. **Paste** your Spotify playlist URL into the app
2. The app **fetches song titles + artists** using Spotipy
3. It sends the list to OpenAI GPT with a custom prompt
4. You get a **GPT-generated personality breakdown** based on your musical taste