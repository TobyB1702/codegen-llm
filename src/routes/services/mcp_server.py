# ...existing code...
from typing import Any, List, Optional, Dict
from mcp.server.fastmcp import FastMCP
import pandas as pd
import os

# Initialize FastMCP server
mcp = FastMCP("MovieAnalysis")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "top_rated_2000webseries.csv")
DATA_PATH = os.path.normpath(DATA_PATH)

# lazy-loaded dataframe cache
_df_cache: Optional[pd.DataFrame] = None

def _load_df() -> pd.DataFrame:
    global _df_cache
    if _df_cache is None:
        _df_cache = pd.read_csv(DATA_PATH, parse_dates=["premiere_date"], encoding="utf-8", low_memory=False)
        # normalize column names
        _df_cache.columns = [c.strip() for c in _df_cache.columns]
    return _df_cache

@mcp.tool()
def get_column_names() -> List[str]:
    """
    Return the column names from the dataset as a list of strings.
    """
    df = _load_df()
    return [str(c) for c in df.columns.tolist()]

@mcp.tool()
def average_rating() -> Dict[str, Any]:
    """
    Compute the average of the 'rating' column and return it with the count of valid ratings.
    """
    df = _load_df()
    if 'rating' not in df.columns:
        return {"error": "column 'rating' not found"}
    ratings = pd.to_numeric(df['rating'], errors='coerce').dropna()
    if ratings.empty:
        return {"error": "no valid ratings"}
    avg = float(ratings.mean())
    return {"average_rating": round(avg, 3), "count": int(ratings.count())}



if __name__ == "__main__":
    mcp.run(transport='stdio')