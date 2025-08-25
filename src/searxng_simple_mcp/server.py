#!/usr/bin/env python3
"""
SearxNG MCP Server - Main server implementation using FastMCP.

This module implements a FastMCP server that provides web search capabilities
using SearxNG as the backend. It offers tools for searching the web and
fetching content from URLs.

Example:
    To run the server directly:

    $ python -m src.run_server

"""

# Standard library imports
import logging
from typing import Any, Literal

# Third-party imports
from fastmcp import Context, FastMCP
from pydantic import Field

# Local imports
from searxng_simple_mcp.config import Settings
from searxng_simple_mcp.searxng_client import SearxNGClient, SearxngResult

# Constants
# Module-level Field constants to avoid calling Field() in function signatures
_QUERY_FIELD = Field(description="The search query string to look for on the web")
_RESULT_COUNT_FIELD = Field(
    default=Settings().default_result_count,
    description="Maximum number of results to return",
    gt=0,
)
_CATEGORIES_FIELD = Field(
    default=None,
    description="Categories to filter by (e.g., 'general', 'images', 'news', 'videos')",
)
_LANGUAGE_FIELD = Field(
    default=Settings().default_language,
    description="Language code for results (e.g., 'all', 'en', 'ru', 'fr')",
)
_TIME_RANGE_FIELD = Field(default=None, description="Time restriction for results")
_RESULT_FORMAT_FIELD = Field(
    default=Settings().default_format,
    description="Output format - 'text' for human-readable, 'json' for structured data",
)

# Configure logging
logger = logging.getLogger(__name__)

# Create configuration
settings = Settings()

# Create FastMCP server
mcp = FastMCP(
    "SearxNG Search",
    instructions="Provides web search capabilities using SearxNG",
    log_level=settings.log_level,
)

# Initialize SearxNG client
searxng_client = SearxNGClient(settings.searxng_url, settings.timeout)


@mcp.tool()
async def web_search(
    query: str = _QUERY_FIELD,
    result_count: int = _RESULT_COUNT_FIELD,
    categories: list[str] | None = _CATEGORIES_FIELD,
    language: str | None = _LANGUAGE_FIELD,
    time_range: Literal["day", "week", "month", "year"] | None = _TIME_RANGE_FIELD,
    result_format: Literal["text", "json"] = _RESULT_FORMAT_FIELD,
    ctx: Context | None = None,
) -> str | list[SearxngResult]:
    """
    Perform a web search using SearxNG and return formatted results.

    Results are returned in either text format (human-readable) or JSON format
    depending on the result_format parameter selected.

    """
    try:
        # Inform about the search operation
        if ctx:
            await ctx.info("Starting web search...")

        # Validate inputs
        if result_count <= 0:
            raise ValueError("result_count must be greater than 0")

        # Perform the search using SearxNG
        response = await searxng_client.search(
            query=query,
            categories=categories,
            language=language,
            time_range=time_range,
        )

        results = response.results[:result_count]

        # Format results according to requested format
        if result_format == "json":
            # Return JSON-formatted results
            return results
        else:
            # Return human-readable text
            formatted_results = []
            for i, result in enumerate(results, 1):
                title = result.title
                url = result.url
                content = result.content[:200] + "..."
                formatted_results.append(f"{i}. [{title}]({url})\n   {content}")

            return "\n\n".join(formatted_results)

    except Exception as e:
        logger.error(f"Error during web search: {e}")
        if ctx:
            await ctx.info(f"Error during search: {e}")
        raise


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()
