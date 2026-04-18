from mcp.server.fastmcp import FastMCP

from src.routes.services.tools import _load_df

mcp = FastMCP("MovieAnalysis")


@mcp.tool()
def get_column_names() -> list[str]:
    """Return the column names available in the TV shows dataset."""
    return _load_df().columns.tolist()


@mcp.tool()
def average_rating() -> dict:
    """Compute the average rating across all TV shows in the dataset."""
    import pandas as pd
    df = _load_df()
    ratings = pd.to_numeric(df["rating"], errors="coerce").dropna()
    if ratings.empty:
        return {"error": "no valid ratings found"}
    return {"average_rating": round(float(ratings.mean()), 3), "count": int(len(ratings))}


@mcp.tool()
def search_shows(query: str) -> list[dict]:
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


@mcp.tool()
def top_shows(n: int = 10) -> list[dict]:
    """Return the top N highest-rated TV shows. Defaults to top 10."""
    df = _load_df()
    return (
        df.nlargest(n, "rating")[["title", "genre", "rating", "country_origin"]]
        .to_dict("records")
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
