import pandas as pd


def top_albums(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if "album" not in df.columns:
        return pd.DataFrame(columns=["album", "artist", "hours", "plays"])

    result = (
        df.groupby(["album", "artist"], dropna=True)
        .agg(
            plays=("ms_played", "count"),
            total_ms=("ms_played", "sum"),
        )
        .reset_index()
    )
    result["hours"] = (result["total_ms"] / 3_600_000).round(2)
    return (
        result.nlargest(n, "total_ms")[["album", "artist", "hours", "plays"]]
        .reset_index(drop=True)
    )
