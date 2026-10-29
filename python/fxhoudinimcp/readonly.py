"""Dedicated read-only server entry point.

Use ``python -m fxhoudinimcp.readonly`` or the
``fxhoudinimcp-readonly`` console script when the MCP client should never see
the authoring tool surface.
"""

from __future__ import annotations

import os


def main() -> None:
    """Start the normal server entry point with the read-only surface enabled."""

    os.environ["FXHOUDINIMCP_READ_ONLY"] = "1"
    from fxhoudinimcp.__main__ import main as server_main

    server_main()


if __name__ == "__main__":
    main()

