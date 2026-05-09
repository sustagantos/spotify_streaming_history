import pandas as pd

_WEEKDAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]


def by_month(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("year_month")["hours_played"]
        .sum()
        .reset_index()
        .rename(columns={"year_month": "month", "hours_played": "hours"})
        .sort_values("month")
        .assign(hours=lambda x: x["hours"].round(2))
    )


def by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("weekday", observed=True)["hours_played"]
        .sum()
        .reindex(_WEEKDAY_ORDER)
        .reset_index()
        .rename(columns={"hours_played": "hours"})
    )
    result["hours"] = result["hours"].round(2)
    return result


def by_hour(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("hour")["hours_played"]
        .sum()
        .reindex(range(24), fill_value=0)
        .reset_index()
        .rename(columns={"hours_played": "hours"})
    )
    result["hours"] = result["hours"].round(2)
    return result


def by_platform(df: pd.DataFrame) -> pd.DataFrame:
    if "platform" not in df.columns:
        return pd.DataFrame(columns=["platform", "hours", "plays"])
    result = (
        df.groupby("platform", dropna=True)
        .agg(hours=("hours_played", "sum"), plays=("ms_played", "count"))
        .reset_index()
        .sort_values("hours", ascending=False)
    )
    result["hours"] = result["hours"].round(2)
    return result.reset_index(drop=True)


def by_country(df: pd.DataFrame) -> pd.DataFrame:
    if "country" not in df.columns:
        return pd.DataFrame(columns=["country", "hours"])
    result = (
        df.groupby("country", dropna=True)["hours_played"]
        .sum()
        .reset_index()
        .rename(columns={"hours_played": "hours"})
        .sort_values("hours", ascending=False)
    )
    result["hours"] = result["hours"].round(2)
    return result.reset_index(drop=True)
