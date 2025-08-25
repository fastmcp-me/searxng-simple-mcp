"""
SearxNG Simple MCP package.

This package provides a FastMCP server for SearxNG web search.
"""

# Import all modules from the package
from searxng_simple_mcp.config import DEFAULT_FORMAT, DEFAULT_LANGUAGE, Settings
from searxng_simple_mcp.searxng_client import SearxNGClient
from searxng_simple_mcp.server import logger, mcp, settings

# Define what should be available when importing from this package
__all__ = [
    "DEFAULT_FORMAT",
    "DEFAULT_LANGUAGE",
    "SearxNGClient",
    "Settings",
    "logger",
    "mcp",
    "settings",
]

# Version of the package
__version__ = "1.0.0"
