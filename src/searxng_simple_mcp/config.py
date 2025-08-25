"""
Configuration settings for the SearxNG MCP server.

This module defines the configuration settings for the SearxNG MCP server
using Pydantic for validation and environment variable loading.
"""

from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings

# Default values as constants for better maintainability
DEFAULT_SEARXNG_URL = "https://paulgo.io/"
DEFAULT_TIMEOUT = 10
DEFAULT_RESULT_COUNT = 10
DEFAULT_LANGUAGE = "all"
DEFAULT_FORMAT = "text"
DEFAULT_LOG_LEVEL = "ERROR"


class Settings(BaseSettings):
    """
    Configuration settings for the SearxNG MCP server.

    Attributes:
        searxng_url: URL of the SearxNG instance to use
        timeout: HTTP request timeout in seconds
        max_results: Maximum number of search results to return
        result_count: Default number of results to return in searches
        language: Language code for search results
        format: Default format for search results
        log_level: Logging level for the application

    """

    # SearxNG instance URL
    searxng_url: AnyHttpUrl = Field(
        default=DEFAULT_SEARXNG_URL, description="URL of the SearxNG instance to use"
    )

    # HTTP request settings
    timeout: int = Field(
        default=DEFAULT_TIMEOUT,
        description="HTTP request timeout in seconds",
        gt=0,  # Must be greater than 0
    )

    default_result_count: int = Field(
        default=DEFAULT_RESULT_COUNT,
        description="Default number of results to return in searches",
        gt=0,  # Must be greater than 0
    )

    # Language settings
    default_language: str | None = Field(
        default=DEFAULT_LANGUAGE,
        description="Language code for search results (e.g., 'en', 'ru', 'all')",
        min_length=1,  # Cannot be empty
    )

    # Format settings
    default_format: Literal["text", "json"] = Field(
        default=DEFAULT_FORMAT,
        description="Default format for search results ('text', 'json')",
        min_length=1,  # Cannot be empty
    )

    # Logging settings
    log_level: str = Field(
        default=DEFAULT_LOG_LEVEL,
        description="Logging level for the application (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')",
    )

    class Config:
        """Pydantic configuration for environment variables."""

        env_prefix = "SEARXNG_MCP_"
        env_file = None
        case_sensitive = False

        # Enable better error messages
        validate_assignment = True
