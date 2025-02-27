from flask import Flask, render_template, redirect
import requests
import random
import webbrowser

app = Flask(__name__)

CLIENT_ID = "98c8a35b87514e709ffa381a13f5ae3c"
CLIENT_SECRET = "0996439dc4ca4c80b5cf612e0be22454"

def get_spotify_token():
    AUTH_URL = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(AUTH_URL, {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    return auth_response.json().get("access_token")

def get_random_song():
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    playlist_id = "3Ir5YWemOTGRRfXgROrsDV"  # ID playlist K-pop
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = requests.get(playlist_url, headers=headers)
    
    if response.status_code == 200:
        tracks = response.json().get("items", [])
        if tracks:
            random_track = random.choice(tracks)["track"]
            return random_track["name"], random_track["external_urls"]["spotify"]
    return None, None

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/random-song")
def random_song():
    track_name, track_url = get_random_song()
    if track_url:
        return redirect(track_url)
    return "Gagal mengambil lagu."

if __name__ == "__main__":
    app.run(debug=True)
