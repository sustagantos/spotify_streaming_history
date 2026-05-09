import argparse
from datetime import datetime
from pathlib import Path

from src.data_loader import load_data
from src.analysis.overview import summary_stats
from src.analysis.artists import top_artists
from src.analysis.songs import top_songs
from src.analysis.albums import top_albums
from src.analysis import trends


def _md_table(df) -> str:
    return df.to_markdown(index=False, floatfmt=".2f")


def _build_report(df, top_n: int) -> str:
    stats = summary_stats(df)
    lines = []

    lines.append("# Spotify Streaming History Report")
    lines.append(f"_Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")

    lines.append("## Overview\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Date range | {stats['date_range_start']} → {stats['date_range_end']} |")
    lines.append(f"| Total streams | {stats['total_streams']:,} |")
    lines.append(f"| Total listening time | {stats['total_hours']:.1f} h ({stats['total_days']:.1f} days) |")
    lines.append(f"| Unique artists | {stats['unique_artists']:,} |")
    lines.append(f"| Unique tracks | {stats['unique_tracks']:,} |")
    lines.append(f"| Unique albums | {stats['unique_albums']:,} |")
    lines.append(f"| Skipped streams | {stats['skip_count']:,} ({stats['skip_rate']:.1f}%) |")
    if stats.get("shuffle_rate") is not None:
        lines.append(f"| Shuffle rate | {stats['shuffle_rate']:.1f}% |")
    lines.append("")

    lines.append(f"## Top {top_n} Artists by Listening Time\n")
    a = top_artists(df, top_n).rename(
        columns={"artist": "Artist", "hours": "Hours", "plays": "Plays", "skip_rate": "Skip %"}
    )
    lines.append(_md_table(a))
    lines.append("")

    lines.append(f"## Top {top_n} Songs by Listening Time\n")
    s = top_songs(df, top_n).rename(
        columns={
            "track_name": "Track", "artist": "Artist",
            "hours": "Hours", "plays": "Plays", "skip_rate": "Skip %",
        }
    )
    lines.append(_md_table(s))
    lines.append("")

    lines.append(f"## Top {top_n} Albums by Listening Time\n")
    al = top_albums(df, top_n).rename(
        columns={"album": "Album", "artist": "Artist", "hours": "Hours", "plays": "Plays"}
    )
    lines.append(_md_table(al))
    lines.append("")

    lines.append("## Listening by Day of Week\n")
    lines.append(_md_table(trends.by_weekday(df).rename(columns={"weekday": "Day", "hours": "Hours"})))
    lines.append("")

    lines.append("## Listening by Hour of Day\n")
    lines.append(_md_table(trends.by_hour(df).rename(columns={"hour": "Hour", "hours": "Hours"})))
    lines.append("")

    lines.append("## Monthly Listening Trend\n")
    lines.append(_md_table(trends.by_month(df).rename(columns={"month": "Month", "hours": "Hours"})))
    lines.append("")

    platform_df = trends.by_platform(df)
    if not platform_df.empty:
        lines.append("## Platform Breakdown\n")
        lines.append(_md_table(platform_df.rename(
            columns={"platform": "Platform", "hours": "Hours", "plays": "Plays"}
        )))
        lines.append("")

    country_df = trends.by_country(df)
    if not country_df.empty:
        lines.append("## Country Breakdown\n")
        lines.append(_md_table(country_df.rename(
            columns={"country": "Country", "hours": "Hours"}
        )))
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Spotify streaming history analyzer")
    parser.add_argument("--data-dir", default="data", help="Directory with JSON files (default: data/)")
    parser.add_argument("--output-dir", default="output", help="Report output directory (default: output/)")
    parser.add_argument("--top", type=int, default=10, metavar="N", help="Top-N entries per table (default: 10)")
    args = parser.parse_args()

    print(f"Loading data from '{args.data_dir}/'...")
    df = load_data(args.data_dir)
    print(f"Loaded {len(df):,} music streams.\n")

    stats = summary_stats(df)
    print("=== OVERVIEW ===")
    print(f"  Date range     : {stats['date_range_start']} → {stats['date_range_end']}")
    print(f"  Total streams  : {stats['total_streams']:,}")
    print(f"  Listening time : {stats['total_hours']:.1f} hours  ({stats['total_days']:.1f} days)")
    print(f"  Unique artists : {stats['unique_artists']:,}")
    print(f"  Unique tracks  : {stats['unique_tracks']:,}")
    print(f"  Skip rate      : {stats['skip_rate']:.1f}%")
    print()

    print(f"=== TOP {args.top} ARTISTS ===")
    print(top_artists(df, args.top).to_string(index=False))
    print()

    print(f"=== TOP {args.top} SONGS ===")
    print(top_songs(df, args.top).to_string(index=False))
    print()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path.write_text(_build_report(df, args.top), encoding="utf-8")
    print(f"Full report saved to: {report_path}")


if __name__ == "__main__":
    main()
