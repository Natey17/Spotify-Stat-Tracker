import os
os.makedirs("out", exist_ok=True)

from fetch import client, get_top, get_recent, get_audio_features
from export import tracks_to_df, artists_to_df, recent_to_df, audio_to_df, save

def run():
    sp = client()

    for rng in ["short_term","medium_term","long_term"]:
        top_tracks = get_top(sp, "tracks", rng, 50)
        top_artists = get_top(sp, "artists", rng, 50)

        tdf = tracks_to_df(top_tracks)
        adf = artists_to_df(top_artists)
        save(tdf, f"top_tracks_{rng}")
        save(adf, f"top_artists_{rng}")

        ids = [t["id"] for t in top_tracks if t.get("id")]
        if ids:
            feats = audio_to_df(get_audio_features(sp, ids))
            save(feats, f"audio_features_{rng}")

    recent = recent_to_df(get_recent(sp, 50))
    save(recent, "recent_plays")

if __name__ == "__main__":
    run()
