"""
Client for interacting with SearxNG search API.
"""

import logging
from typing import Any

import httpx
from pydantic import AnyHttpUrl

# Configure logging
logger = logging.getLogger(__name__)


class SearxNGClient:
    """Client for interacting with SearxNG search API."""

    def __init__(self, base_url: AnyHttpUrl, timeout: int) -> None:
        """
        Initialize the SearxNG client.

        Args:
            base_url: URL of the SearxNG instance to use
            timeout: HTTP request timeout in seconds

        """
        self.base_url = str(base_url).rstrip("/")
        self.timeout = timeout

    async def search(
        self,
        query: str,
        categories: list[str] | None = None,
        language: str | None = None,
        time_range: str | None = None,
    ) -> dict[str, Any]:
        """
        Performs a web search using the SearxNG API.

        Returns search results in a dictionary format containing the results
        and metadata such as number of total results found.

        Args:
            query: The search query string to look for on the web
            categories: Categories to search (e.g., "general", "images", "news")
            language: Language code for results (e.g., "all", "en", "ru")
            time_range: Time range (options: "day", "week", "month", "year")

        Returns:
            Dictionary containing search results and metadata

        """
        # Build search parameters
        params = {
            "q": query,
            "format": "json",
        }

        # Add optional parameters if provided
        if categories:
            params["categories"] = ",".join(categories)

        if time_range:
            params["time_range"] = time_range

        # Handle language parameter - always pass language
        if language:
            params["language"] = language

        try:
            # Make the API request
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params,
                    timeout=self.timeout,
                )

                # Raise an exception for HTTP errors
                response.raise_for_status()

                logger.info(f"Response: {response.text[:100]}...")

                # Parse the JSON response
                return response.json()

        except Exception as e:
            logger.exception("Unexpected error occurred")
            msg = f"Error during search: {e}"
            raise ValueError(msg) from e

    def format_results(self, data: dict[str, Any]) -> str:
        """
        Format search results as a readable string.

        Args:
            data: Search results from the search() method

        Returns:
            Formatted string of search results

        """
        results = data.get("results", [])

        if not results:
            return "No results found."

        # Extract information about the search
        search_info = []
        if "query" in data:
            search_info.append(f"Query: {data['query']}")

        # Add information about the number of results
        if "number_of_results" in data and data["number_of_results"] > 0:
            search_info.append(
                f"Found approximately {data['number_of_results']} results"
            )

        # Format individual results
        formatted_results = []
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            content = result.get("content", "No description")

            result_text = f"{i}. {title}\n   URL: {url}\n   {content}"

            # Add optional metadata if available
            if "publishedDate" in result:
                result_text += f"\n   Date: {result['publishedDate']}"
            if "score" in result:
                result_text += f"\n   Score: {result['score']:.2f}"

            formatted_results.append(result_text)

        # Combine search info and results
        search_info_text = "\n".join(search_info)
        results_text = "\n\n".join(formatted_results)

        return f"{search_info_text}\n\n{results_text}"
