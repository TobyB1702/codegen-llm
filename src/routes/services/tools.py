from typing import Any, Dict, List, Optional
import os
import sys

import pandas as pd
from langchain_core.tools import tool


def _get_data_path() -> str:
    # sys.frozen is set by Nuitka (standalone/onefile) — exe dir holds the data folder
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), "data", "top_rated_2000webseries.csv")
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "top_rated_2000webseries.csv")
    )


_df_cache: Optional[pd.DataFrame] = None


def _load_df() -> pd.DataFrame:
    global _df_cache
    if _df_cache is None:
        _df_cache = pd.read_csv(
            _get_data_path(), parse_dates=["premiere_date"], encoding="utf-8", low_memory=False
        )
        _df_cache.columns = [c.strip() for c in _df_cache.columns]
    return _df_cache


@tool
def get_column_names() -> List[str]:
    """Return the column names available in the TV shows dataset."""
    return _load_df().columns.tolist()


@tool
def average_rating() -> Dict[str, Any]:
    """Compute the average rating across all TV shows in the dataset."""
    df = _load_df()
    ratings = pd.to_numeric(df["rating"], errors="coerce").dropna()
    if ratings.empty:
        return {"error": "no valid ratings found"}
    return {"average_rating": round(float(ratings.mean()), 3), "count": int(len(ratings))}


@tool
def search_shows(query: str) -> List[Dict[str, Any]]:
    """Search for TV shows by title or genre. Returns up to 5 matching shows."""
    df = _load_df()
    mask = df["title"].str.contains(query, case=False, na=False) | df["genre"].str.contains(
        query, case=False, na=False
    )
    return (
        df[mask]
        .head(5)[["title", "genre", "rating", "premiere_date", "overview"]]
        .to_dict("records")
    )


@tool
def top_shows(n: int = 10) -> List[Dict[str, Any]]:
    """Return the top N highest-rated TV shows. Defaults to top 10."""
    df = _load_df()
    return (
        df.nlargest(n, "rating")[["title", "genre", "rating", "country_origin"]]
        .to_dict("records")
    )
