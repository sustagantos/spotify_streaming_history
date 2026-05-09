# Spotify Streaming History Analysis

Analyses your complete Spotify extended streaming history and generates a markdown report with listening insights.

## Setup
Get your Spotify Streaming History data from https://www.spotify.com/br-pt/account/privacy/

```bash
pip install -r requirements.txt
```

## Usage

1. Place your Spotify JSON history files (e.g. `Streaming_History_Audio_2022.json`, `Streaming_History_Video_2022.json`, …) in the `data/` directory.
2. Run the analyser:

```bash
python main.py
```

This prints a summary to the console and writes a full report to `output/report_<timestamp>.md`.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--top N` | 10 | Number of entries in top-N tables |
| `--data-dir PATH` | `data/` | Directory containing JSON files |
| `--output-dir PATH` | `output/` | Directory for the generated report |

Example:

```bash
python main.py --top 20
```

## Report sections

- **Overview** — total hours, unique artists/tracks/albums, skip rate, shuffle rate
- **Top Artists / Songs / Albums** — ranked by total listening time
- **Day of Week & Hour of Day** — when you listen most
- **Monthly Trend** — listening hours per month
- **Platform Breakdown** — phone vs. desktop vs. web
- **Country Breakdown** — where streams originated

## Project structure

```
spotify_streaming_history/
├── data/                  # Your JSON files (gitignored)
├── output/                # Generated reports (gitignored)
├── src/
│   ├── data_loader.py     # Loads and normalises all JSON files
│   └── analysis/
│       ├── overview.py    # Summary statistics
│       ├── artists.py     # Top artists
│       ├── songs.py       # Top songs
│       ├── albums.py      # Top albums
│       └── trends.py      # Time-based aggregations
├── main.py
└── requirements.txt
```

## Getting your data from Spotify

1. Go to **Settings → Privacy → Download your data**
2. Request the **Extended streaming history** (not the basic version — it has fewer fields)
3. Spotify emails a download link within ~30 days
4. Extract and copy the `endsong_*.json` files into `data/`
