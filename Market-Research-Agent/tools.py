import os
import time
import requests
from typing import Any, Dict, List

YOU_SEARCH_URL = "https://ydc-index.io/v1/search"


def you_search(
    query: str,
    count: int = 5,
    retries: int = 2
) -> List[Dict[str, Any]]:
    """
    Read-only web search using the current You.com Search API.
    """

    # Support both names so your existing .env still works.
    api_key = (
        os.getenv("YDC_API_KEY", "").strip()
        or os.getenv("YOU_API_KEY", "").strip()
    )

    if not api_key:
        raise RuntimeError(
            "You.com API key is missing. "
            "Add YDC_API_KEY to your .env file."
        )

    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "query": query,
        "count": count,
    }

    last_error = None

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                YOU_SEARCH_URL,
                headers=headers,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            # Current You.com response may contain results
            # under several structures.
            results = []

            if isinstance(data, list):
                results = data

            elif isinstance(data, dict):

                if isinstance(data.get("results"), list):
                    results = data["results"]

                elif isinstance(data.get("hits"), list):
                    results = data["hits"]

                elif isinstance(data.get("results"), dict):
                    result_obj = data["results"]

                    # Web results
                    if isinstance(result_obj.get("web"), list):
                        results.extend(result_obj["web"])

                    # News results
                    if isinstance(result_obj.get("news"), list):
                        results.extend(result_obj["news"])

            if not results:
                raise RuntimeError(
                    f"You.com returned no usable results. "
                    f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'list'}"
                )

            return results[:count]

        except Exception as exc:
            last_error = exc

            if attempt < retries:
                time.sleep(1.2 * (attempt + 1))

    raise RuntimeError(
        f"Search failed after retries: {last_error}"
    )


def compact_search_results(
    results: List[Dict[str, Any]]
) -> str:

    rows = []

    for i, item in enumerate(results, 1):

        title = (
            item.get("title")
            or item.get("name")
            or "Untitled"
        )

        url = (
            item.get("url")
            or item.get("link")
            or ""
        )

        snippet = (
            item.get("description")
            or item.get("snippet")
            or item.get("text")
            or item.get("contents")
            or ""
        )

        # Some API responses can return structured content.
        if not isinstance(snippet, str):
            snippet = str(snippet)

        rows.append(
            f"[{i}] {title}\n"
            f"URL: {url}\n"
            f"Snippet: {snippet[:1200]}"
        )

    return "\n\n".join(rows)