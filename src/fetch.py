import os, time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SCOPES = ["user-top-read", "user-read-recently-played"]

def client():
    load_dotenv()
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8080/callback"),
        scope=" ".join(SCOPES),
        open_browser=True,
        cache_path=".cache"
    ))

def get_top(sp, item_type="tracks", time_range="short_term", limit=50):
    assert item_type in {"tracks","artists"}
    res = sp.current_user_top_tracks(limit=limit, time_range=time_range) if item_type=="tracks" \
          else sp.current_user_top_artists(limit=limit, time_range=time_range)
    return res.get("items", [])

def get_recent(sp, limit=50):
    return sp.current_user_recently_played(limit=limit).get("items", [])

def get_audio_features(sp, track_ids):
    feats = sp.audio_features(track_ids)
    return [f for f in feats if f]
