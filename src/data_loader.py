import json
import pandas as pd
from pathlib import Path

_RENAMES = {
    "ts": "timestamp",
    "master_metadata_track_name": "track_name",
    "master_metadata_album_artist_name": "artist",
    "master_metadata_album_album_name": "album",
    "conn_country": "country",
}

_WEEKDAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]


def load_data(data_dir="data") -> pd.DataFrame:
    data_dir = Path(data_dir)
    json_files = sorted(data_dir.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(
            f"No JSON files found in {data_dir.resolve()}\n"
            "Place your Spotify history JSON files inside the data/ directory."
        )

    records = []
    for path in json_files:
        with open(path, encoding="utf-8") as f:
            chunk = json.load(f)
        records.extend(chunk if isinstance(chunk, list) else [chunk])

    df = pd.DataFrame(records)

    rename_map = {k: v for k, v in _RENAMES.items() if k in df.columns}
    df = df.rename(columns=rename_map)

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["year_month"] = df["timestamp"].dt.to_period("M").astype(str)
    df["weekday"] = pd.Categorical(
        df["timestamp"].dt.day_name(), categories=_WEEKDAY_ORDER, ordered=True
    )
    df["hour"] = df["timestamp"].dt.hour

    # drop podcast entries (no track name)
    df = df[df["track_name"].notna()].copy()

    df["minutes_played"] = df["ms_played"] / 60_000
    df["hours_played"] = df["ms_played"] / 3_600_000

    if "skipped" not in df.columns:
        df["skipped"] = False
    else:
        df["skipped"] = df["skipped"].fillna(False).astype(bool)

    return df.reset_index(drop=True)
