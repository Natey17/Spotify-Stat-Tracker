import pandas as pd
from datetime import datetime

def tracks_to_df(items):
    rows=[]
    for rank, t in enumerate(items, 1):
        rows.append({
            "rank": rank,
            "track_id": t["id"],
            "track": t["name"],
            "artists": ", ".join(a["name"] for a in t["artists"]),
            "album": t["album"]["name"],
            "release_date": t["album"].get("release_date"),
            "popularity": t.get("popularity"),
            "duration_ms": t.get("duration_ms"),
            "url": t["external_urls"]["spotify"]
        })
    return pd.DataFrame(rows)

def artists_to_df(items):
    rows=[]
    for rank, a in enumerate(items, 1):
        rows.append({
            "rank": rank,
            "artist_id": a["id"],
            "artist": a["name"],
            "genres": ", ".join(a.get("genres", [])),
            "followers": a.get("followers",{}).get("total"),
            "popularity": a.get("popularity"),
            "url": a["external_urls"]["spotify"]
        })
    return pd.DataFrame(rows)

def recent_to_df(items):
    rows=[]
    for it in items:
        t=it["track"]
        rows.append({
            "played_at": it["played_at"],
            "track_id": t["id"],
            "track": t["name"],
            "artists": ", ".join(a["name"] for a in t["artists"]),
            "album": t["album"]["name"],
            "url": t["external_urls"]["spotify"]
        })
    return pd.DataFrame(rows)

def audio_to_df(items):
    import math
    rows=[]
    for f in items:
        rows.append({k:f.get(k) for k in [
            "id","danceability","energy","valence","tempo","loudness","speechiness","acousticness","instrumentalness","liveness","mode","key","time_signature"
        ]})
    return pd.DataFrame(rows)

def save(df, name_prefix):
    ts=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv=f"out/{name_prefix}_{ts}.csv"
    json=f"out/{name_prefix}_{ts}.json"
    df.to_csv(csv, index=False)
    df.to_json(json, orient="records", indent=2)
    return csv, json
