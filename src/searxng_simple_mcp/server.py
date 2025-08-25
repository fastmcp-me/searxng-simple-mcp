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
from searxng_simple_mcp.searxng_client import SearxNGClient

# Constants

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
    query: str = Field(description="The search query string to look for on the web"),
    result_count: int = Field(
        default=settings.default_result_count,
        description="Maximum number of results to return",
        gt=0,
    ),
    categories: list[str] | None = Field(
        default=None,
        description="Categories to filter by (e.g., 'general', 'images', 'news', 'videos')",
    ),
    language: str | None = Field(
        default=settings.default_language,
        description="Language code for results (e.g., 'all', 'en', 'ru', 'fr')",
    ),
    time_range: Literal["day", "week", "month", "year"] | None = Field(
        default=None, description="Time restriction for results"
    ),
    result_format: Literal["text", "json"] = Field(
        default=settings.default_format,
        description="Output format - 'text' for human-readable or 'json' for structured data",
    ),
    ctx: Context = None,
) -> str | dict[str, Any]:
    """
    Performs a web search using SearxNG and returns formatted results.

    Results are returned in either text format (human-readable) or JSON format
    depending on the result_format parameter selected.
    """
    try:
        # Inform about the search operation
        if ctx:
            ctx.info(f"Searching for: {query}")

        # Perform the search
        results = await searxng_client.search(
            query,
            categories=categories,
            language=language,
            time_range=time_range,
        )

        # Limit the results based on the requested count
        if "results" in results and len(results["results"]) > result_count:
            results["results"] = results["results"][:result_count]

        # Format the results based on result_format using ternary operator
        result = (
            results
            if result_format == "json"
            else searxng_client.format_results(results)
        )

        if ctx:
            ctx.info(f"Found {len(results.get('results', []))} results")
    except Exception as e:
        error_msg = f"Unexpected error during search: {e}"
        logger.exception(error_msg)
        if ctx:
            ctx.error(error_msg)
        return error_msg
    else:
        return result


# Define a resource for server information
@mcp.resource("server://info")
def get_server_info() -> str:
    """Get information about the SearxNG server configuration."""
    return f"""
SearxNG MCP Server Information:
------------------------------
SearxNG Instance: {settings.searxng_url}
Timeout: {settings.timeout} seconds
Default Result Count: {settings.default_result_count}
Default Language: {settings.default_language}
Default Format: {settings.default_format}
Log Level: {settings.log_level}
    """
