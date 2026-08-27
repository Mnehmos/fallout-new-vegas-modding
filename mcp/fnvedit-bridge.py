"""Launcher bridge: run the mnehmos.fnvedit.mcp server (src/server.py) without
cwd assumptions. Registered in .mcp.json as server 'fnvedit'."""
import sys

sys.path.insert(0, r"F:\Github\mnehmos.fnvedit.mcp")

from src.server import main  # noqa: E402

if __name__ == "__main__":
    main()
