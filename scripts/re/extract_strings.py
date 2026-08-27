"""String extractor tuned for 32-bit Windows game binaries.

Usage:
    python extract_strings.py [path] [--min 5] [--utf16] [--offsets] [--json]
    python extract_strings.py FalloutNV.exe --min 6 > research/re/strings.txt

Extracts ASCII and UTF-16LE strings. Windows games use both encodings; plain
`strings -el` equivalents miss cross-encodings and give no VA mapping. Output
includes virtual addresses so hits can be fed straight into find_xrefs.py.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pe_utils import emit, load_pe, resolve_target


def compile_patterns(min_len: int):
    return (
        re.compile(rb"[\x20-\x7e]{%d,}" % min_len),
        re.compile(rb"(?:[\x20-\x7e]\x00){%d,}" % min_len),
    )


def extract(path: Path, min_len: int, utf16: bool) -> list[dict]:
    pe = load_pe(path)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = path.read_bytes()
    out = []
    ascii_re, utf16_re = compile_patterns(min_len)

    sec_map = []
    for s in pe.sections:
        sec_map.append((s.PointerToRawData, s.PointerToRawData + s.SizeOfRawData,
                        base + s.VirtualAddress, s.Name.rstrip(b"\x00").decode(errors="replace")))

    def va_of(offset: int) -> str:
        for raw_start, raw_end, va, name in sec_map:
            if raw_start <= offset < raw_end:
                return f"0x{va + (offset - raw_start):08X}"
        return "0x00000000"

    for m in ascii_re.finditer(data):
        out.append({"va": va_of(m.start()), "enc": "ascii",
                    "s": m.group().decode("ascii", errors="replace")})
    if utf16:
        for m in utf16_re.finditer(data):
            out.append({"va": va_of(m.start()), "enc": "utf16le",
                        "s": m.group().decode("utf-16-le", errors="replace")})
    out.sort(key=lambda r: int(r["va"], 16))
    return out


def human(strings: list[dict]) -> None:
    for r in strings:
        marker = "u" if r["enc"] == "utf16le" else "a"
        print(f"{r['va']} [{marker}] {r['s']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", help="PE file (absolute, or relative to FNV game dir)")
    ap.add_argument("--min", type=int, default=5, help="minimum string length (default 5)")
    ap.add_argument("--utf16", action="store_true", help="also extract UTF-16LE strings")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = resolve_target(args.path)
    if not target.exists():
        raise SystemExit(f"error: not found: {target}")
    result = extract(target, args.min, args.utf16)
    emit(result, args.json, human)


if __name__ == "__main__":
    main()
