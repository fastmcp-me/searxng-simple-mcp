#!/usr/bin/env python3
"""
Wrapper script to run the SearxNG MCP server.

This script can be run directly without import issues.
"""

import logging
import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the server
from searxng_simple_mcp.server import mcp, settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)

# Main entrypoint
if __name__ == "__main__":
    print(f"Starting SearxNG MCP server with instance: {settings.searxng_url}")
    mcp.run()
