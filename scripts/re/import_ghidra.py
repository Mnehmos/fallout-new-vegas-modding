"""Ghidra headless runner: import + auto-analyze + export artifacts.

Usage:
    python import_ghidra.py [path] [--project FNVRE] [--post postscript.py]
    python import_ghidra.py FalloutNV.exe

Wrappers analyzeHeadless (found via GHIDRA_INSTALL_DIR env var, `ghidra` on
PATH, or scoop shim). After analysis it runs the postscript
tools/re/ghidra/postscripts/export_artifacts.py which dumps:

    research/re/functions/functions.json   (name, entry, size, namespace)
    research/re/functions/calls.json       (caller -> callee edges + imports)
    research/re/strings.json               (defined strings with VAs)

Those JSON dumps are the authoritative cross-reference + decompilation-input
source; the pattern scripts exist only for fast iteration between Ghidra runs.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POSTSCRIPT_DIR = REPO / "tools" / "re" / "ghidra" / "postscripts"
OUTPUT_DIR = REPO / "research" / "re"


def find_analyzeheadless() -> Path:
    candidates = []
    env = os.environ.get("GHIDRA_INSTALL_DIR")
    if env:
        candidates.append(Path(env) / "support" / "analyzeHeadless.bat")
    on_path = shutil.which("analyzeHeadless") or shutil.which("analyzeHeadless.bat")
    if on_path:
        candidates.append(Path(on_path))
    candidates.append(Path(r"C:\Program Files\ghidra\support\analyzeHeadless.bat"))
    candidates.append(Path(r"C:\Tools\ghidra_11.2.1_PUBLIC\support\analyzeHeadless.bat"))
    for c in candidates:
        if c.exists():
            return c
    raise SystemExit("error: analyzeHeadless not found — set GHIDRA_INSTALL_DIR or install Ghidra (see tools/re/README.md)")


def main() -> None:
    sys.path.insert(0, str(Path(__file__).parent))
    from pe_utils import resolve_target

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", help="PE file (absolute, or relative to FNV game dir)")
    ap.add_argument("--project", default="FNVRE", help="Ghidra project name (default FNVRE)")
    ap.add_argument("--post", default="export_artifacts.py", help="postScript to run after analysis")
    ap.add_argument("--also-post", action="append", default=[], help="additional postscripts to run")
    ap.add_argument("--fresh", action="store_true", help="delete project first (full re-import)")
    ap.add_argument("--project-dir", default=str(REPO / "tools" / "re" / "ghidra" / "projects"),
                    help="Ghidra project directory")
    args = ap.parse_args()

    target = resolve_target(args.path)
    if not target.exists():
        raise SystemExit(f"error: not found: {target}")

    post = POSTSCRIPT_DIR / args.post
    if not post.exists():
        raise SystemExit(f"error: postscript not found: {post}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    proj_dir = Path(args.project_dir)
    proj_dir.mkdir(parents=True, exist_ok=True)

    # forward decompile targets (one per line, '#' comments ok) to postscripts
    targets = []
    targets_file = POSTSCRIPT_DIR / "decompile_targets.txt"
    if targets_file.exists():
        for line in targets_file.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                targets.append(line)

    # reuse the analyzed project unless --fresh: postscript iterations stay cheap
    mode = ["-import", str(target)]
    if not args.fresh and (proj_dir / f"{args.project}.gpr").exists():
        mode = ["-process", target.name, "-noanalysis"]

    cmd = [
        str(find_analyzeheadless()),
        str(proj_dir), args.project,
        *mode,
        "-processor", "x86:LE:32:default",
        "-cspec", "windows",
        "-postScript", str(post), str(OUTPUT_DIR), *targets,
    ]
    for extra in args.also_post:
        extra_path = POSTSCRIPT_DIR / extra if not Path(extra).is_absolute() else Path(extra)
        if not extra_path.exists():
            raise SystemExit(f"error: postscript not found: {extra_path}")
        cmd += ["-postScript", str(extra_path), str(OUTPUT_DIR), *targets]
    if args.fresh:
        cmd.append("-deleteProject")
    print("# " + " ".join(cmd), file=sys.stderr)
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
