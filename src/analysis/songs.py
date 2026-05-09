import pandas as pd


def top_songs(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    result = (
        df.groupby(["track_name", "artist"], dropna=True)
        .agg(
            plays=("ms_played", "count"),
            total_ms=("ms_played", "sum"),
            skips=("skipped", "sum"),
        )
        .reset_index()
    )
    result["hours"] = (result["total_ms"] / 3_600_000).round(2)
    result["skip_rate"] = (result["skips"] / result["plays"] * 100).round(1)
    return (
        result.nlargest(n, "total_ms")[["track_name", "artist", "hours", "plays", "skip_rate"]]
        .reset_index(drop=True)
    )
