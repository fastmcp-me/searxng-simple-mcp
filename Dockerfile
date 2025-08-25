# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Fix for Windows Docker Desktop symlink issues
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_PIP_COMPATIBLE=1

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app

RUN uv sync --locked --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Uses the transport protocol specified by TRANSPORT_PROTOCOL env var (defaults to stdio)
CMD ["sh", "-c", "fastmcp run src/searxng_simple_mcp/server.py --transport ${TRANSPORT_PROTOCOL:-stdio}"]
