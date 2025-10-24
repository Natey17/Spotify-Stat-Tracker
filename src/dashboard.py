from flask import Flask, render_template_string
import pandas as pd
from glob import glob

app = Flask(__name__)

TPL = """
<!doctype html><title>Spotify Stats</title>
<h1>Top Tracks ({{term_label}})</h1>
<table border=1 cellpadding=6>
  <tr>
    <th>rank</th><th>track</th><th>artists</th><th>album</th><th>popularity</th><th>release_date</th>
  </tr>
  {% for _,row in tracks.iterrows() %}
  <tr>
    <td>{{row["rank"]}}</td>
    <td>{{row["track"]}}</td>
    <td>{{row["artists"]}}</td>
    <td>{{row["album"]}}</td>
    <td>{{row["popularity"]}}</td>
    <td>{{row["release_date"]}}</td>
  </tr>
  {% endfor %}
</table>
"""

def latest(pattern):
    files = sorted(glob(pattern))
    return files[-1] if files else None

def select_columns(df):
    df = df.copy()
    # Desired order without: track_id, duration_ms, url
    cols = ["rank", "track", "artists", "album", "popularity", "release_date"]
    cols = [c for c in cols if c in df.columns]
    return df[cols]

@app.get("/")
def index():
    tfile = latest("out/top_tracks_short_term_*.csv")
    term_label = "short_term (≈ past 4 weeks)" if tfile else "N/A"
    if not tfile:
        return "<p>No top_tracks_short_term CSV found in out/</p>"

    tracks = pd.read_csv(tfile)
    tracks = select_columns(tracks)
    return render_template_string(TPL, tracks=tracks, term_label=term_label)

if __name__ == "__main__":
    app.run(port=5050, debug=True)
