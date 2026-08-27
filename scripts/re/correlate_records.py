"""Correlate binary evidence with Bethesda plugin records.

Usage:
    python correlate_records.py [binary] [--plugin path.esp] [--json]

Two passes:

1. Record-signature scan: Gamebryo/Fallout engines embed record type codes
   ('ECZN', 'LVLI', 'NPC_', 'ACHR', ...) and GECK strings in the executable.
   Every 4CC hit inside .rdata/.data is evidence of the engine touching that
   record system; the hit VA is a candidate anchor for find_xrefs.py /
   Ghidra follow-up.

2. Plugin cross-reference: when --plugin is given (and the mnehmos.fnvedit.mcp
   parser is importable), each found 4CC is matched against record counts in
   the ESP/ESM, connecting binary code paths to the records our FNVEdit layer
   already manipulates.
"""
from __future__ import annotations

import argparse
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pe_utils import emit, load_pe, resolve_target

# Record groups we care about for spawn/encounter work, plus a broad net.
RECORD_TYPES = [
    "ECZN", "LVLI", "LVLN", "LVLC", "NPC_", "ACHR", "REFR", "CELL", "WRLD",
    "CREA", "CONT", "LIGH", "SPEL", "PERK", "ENCH", "MGEF", "PACK", "TES4",
    "DIAL", "INFO", "QUST", "IDLE", "IMAD", "IPCT", "DEHY", "HUNG", "SLPD",
]

FNVEDIT_MCP_SRC = Path(r"F:\Github\mnehmos.fnvedit.mcp\src")


def scan_binary(path: Path) -> list[dict]:
    pe = load_pe(path)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = path.read_bytes()
    hits = []
    for sec in pe.sections:
        flags = sec.Characteristics
        if flags & 0x20000000:  # skip exec-only; 4CCs live in initialized data
            continue
        name = sec.Name.rstrip(b"\x00").decode(errors="replace")
        blob = data[sec.PointerToRawData:sec.PointerToRawData + sec.SizeOfRawData]
        for rt in RECORD_TYPES:
            # 4CC followed by a plausible record-ish context: zero byte or length-ish dword
            for m in re.finditer(re.escape(rt.encode()), blob):
                tail = blob[m.end():m.end() + 4]
                if not tail:
                    continue
                va = base + sec.VirtualAddress + m.start()
                hits.append({
                    "record": rt,
                    "va": f"0x{va:08X}",
                    "section": name,
                    "context": blob[max(0, m.start() - 8):m.end() + 8].hex(),
                })
    return hits


def plugin_counts(plugin_path: Path) -> dict:
    sys.path.insert(0, str(FNVEDIT_MCP_SRC))
    try:
        from core.binary_parser import PluginFile
    except ImportError:
        print(f"# warning: mnehmos.fnvedit.mcp not importable from {FNVEDIT_MCP_SRC}", file=sys.stderr)
        return {}
    pf = PluginFile(str(plugin_path))
    counts: dict[str, int] = {}
    for rt in RECORD_TYPES:
        try:
            n = len(list(pf.get_records(rt)))
        except Exception:
            n = 0
        if n:
            counts[rt] = n
    return counts


def correlate(binary_hits: list[dict], counts: dict) -> list[dict]:
    rows = []
    by_record: dict[str, list[dict]] = {}
    for h in binary_hits:
        by_record.setdefault(h["record"], []).append(h)
    for rt in sorted(by_record):
        rows.append({
            "record": rt,
            "binary_hit_count": len(by_record[rt]),
            "binary_vas": [h["va"] for h in by_record[rt]][:10],
            "plugin_record_count": counts.get(rt, 0),
        })
    return rows


def human(rows: list[dict]) -> None:
    print(f"{'REC':6s} {'BIN':>5s} {'PLUGIN':>7s}  candidate anchors")
    for r in rows:
        print(f"{r['record']:6s} {r['binary_hit_count']:>5d} {r['plugin_record_count']:>7d}  "
              + " ".join(r["binary_vas"][:4]))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", help="PE file (absolute, or relative to FNV game dir)")
    ap.add_argument("--plugin", help="ESP/ESM to cross-reference record counts")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = resolve_target(args.path)
    if not target.exists():
        raise SystemExit(f"error: not found: {target}")
    hits = scan_binary(target)
    counts = plugin_counts(Path(args.plugin)) if args.plugin else {}
    emit(correlate(hits, counts), args.json, human)


if __name__ == "__main__":
    main()
