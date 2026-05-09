import pandas as pd


def summary_stats(df: pd.DataFrame) -> dict:
    total_ms = df["ms_played"].sum()
    skip_count = int(df["skipped"].sum())
    total = len(df)

    stats = {
        "total_streams": total,
        "total_hours": total_ms / 3_600_000,
        "total_days": total_ms / 86_400_000,
        "unique_artists": int(df["artist"].nunique()),
        "unique_tracks": int(df["track_name"].nunique()),
        "unique_albums": int(df["album"].nunique()) if "album" in df.columns else 0,
        "skip_count": skip_count,
        "skip_rate": skip_count / total * 100 if total else 0,
        "date_range_start": df["timestamp"].min().strftime("%Y-%m-%d"),
        "date_range_end": df["timestamp"].max().strftime("%Y-%m-%d"),
        "shuffle_rate": df["shuffle"].mean() * 100 if "shuffle" in df.columns else None,
    }
    return stats
