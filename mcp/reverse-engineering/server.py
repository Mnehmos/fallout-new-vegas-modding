"""mnehmos.re — Reverse-Engineering evidence engine MCP server.

Wraps scripts/re tooling + the research/re knowledge base as MCP tools.
Design contract: mcp/reverse-engineering/README.md.
Policy enforcement lives here: confidence tiers are validated mechanically
(research/re/confidence-policy.md), symbols are stored RVA-first, VAs are
derived from the build's image base and never accepted from the client.

Run: python mcp/reverse-engineering/server.py   (stdio)
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "re"))

from mcp.server.fastmcp import FastMCP  # noqa: E402

import pe_utils  # noqa: E402
from pe_utils import DEFAULT_GAME_DIR, RESEARCH_RE, build_identity, resolve_target  # noqa: E402

import correlate_records  # noqa: E402
import extract_strings  # noqa: E402
import find_xrefs  # noqa: E402
import fingerprint_functions  # noqa: E402
import inspect_pe  # noqa: E402
import match_functions  # noqa: E402

KB = RESEARCH_RE / "symbols.json"
NVSE_XREFS = RESEARCH_RE / "nvse_xrefs.json"
FORM_REGISTRY = RESEARCH_RE / "form_type_registry.json"
DECOMPiled_DIR = RESEARCH_RE / "functions" / "decompiled"

ATLAS_CLI_DIR = Path(r"C:\Tools\fnv-source-atlas\src")
ATLAS_DB = Path(r"E:\Tools\fnv-source-atlas-data-0.5.0\fnv-source-atlas.sqlite")

mcp = FastMCP("mnehmos.re")


def _load_kb() -> dict:
    return json.loads(KB.read_text(encoding="utf-8"))


def _save_kb(kb: dict) -> None:
    KB.write_text(json.dumps(kb, indent=2), encoding="utf-8")


def _resolve(binary: str | None, default: str = "FalloutNV.exe") -> Path:
    target = resolve_target(binary, default)
    if not target.exists() and DEFAULT_GAME_DIR.joinpath(binary or "").exists():
        target = DEFAULT_GAME_DIR / binary
    if not target.exists():
        raise ValueError(f"binary not found: {target}")
    return target


# ---------------------------------------------------------------- tools


@mcp.tool()
def re_inspect(binary: str) -> str:
    """PE structure: sections, imports, exports, entropy, build identity (sha256/timestamp)."""
    return json.dumps(inspect_pe.inspect(_resolve(binary)), indent=1)


@mcp.tool()
def re_build_identity(binary: str) -> str:
    """Canonical build identity for KB registration: sha256, PE timestamp, image base, size."""
    return json.dumps(build_identity(_resolve(binary)), indent=1)


@mcp.tool()
def re_strings(binary: str, pattern: str = "", min_len: int = 5, utf16: bool = True, limit: int = 100) -> str:
    """Extract strings (ASCII + UTF-16LE) with VAs; optional regex pattern filter."""
    rows = extract_strings.extract(_resolve(binary), min_len, utf16)
    if pattern:
        rx = re.compile(pattern, re.IGNORECASE)
        rows = [r for r in rows if rx.search(r["s"])]
    return json.dumps({"count": len(rows), "strings": rows[:limit]}, indent=1)


@mcp.tool()
def re_xrefs(binary: str, target: str, is_string: bool = False) -> str:
    """Cross-references to a VA (e.g. '0x00483370') or to an exact string's VA."""
    path = _resolve(binary)
    rows = find_xrefs.find_string_va(path, target) if is_string else [pe_utils.parse_int(target)]
    out = []
    for va in rows:
        out.extend(find_xrefs.find_xrefs(path, va))
    return json.dumps({"target_count": len(rows), "xrefs": out}, indent=1)


@mcp.tool()
def re_callgraph(binary: str, focus_va: str = "") -> str:
    """Static call graph (resilient capstone sweep). focus_va filters to one function's neighborhood."""
    graph = __import__("build_callgraph").build(_resolve(binary))
    if focus_va:
        va = pe_utils.parse_int(focus_va)
        key = f"0x{va:08X}"
        graph = {
            "focus": key,
            "callers": graph["callers"].get(key, []),
            "callees": graph["callees"].get(key, []),
        }
    return json.dumps(graph, indent=1)


@mcp.tool()
def re_fingerprint(binary: str, fn_va: str, max_bytes: int = 96) -> str:
    """Masked IDA signature + mnemonic hash for one function (version-proof ID)."""
    return json.dumps(fingerprint_functions.single_fingerprint(
        _resolve(binary), pe_utils.parse_int(fn_va), max_bytes), indent=1)


@mcp.tool()
def re_match_builds(db_a: str, db_b: str, min_score: float = 0.55) -> str:
    """Cross-build function equivalence between two fingerprint databases (research/re/signatures/*.fnprints.json)."""
    a = match_functions.load_db(Path(db_a) if Path(db_a).exists() else RESEARCH_RE / "signatures" / db_a)
    b = match_functions.load_db(Path(db_b) if Path(db_b).exists() else RESEARCH_RE / "signatures" / db_b)
    m = match_functions.match(a, b, min_score, 5)
    m["matches"] = m["matches"][:40]
    return json.dumps(m, indent=1)


@mcp.tool()
def re_nvse_xrefs(engine_va: str = "", nvse_symbol: str = "", limit: int = 20) -> str:
    """Query mined NVSE->engine references (research/re/nvse_xrefs.json) by engine VA or NVSE symbol substring."""
    d = json.loads(NVSE_XREFS.read_text(encoding="utf-8"))
    if engine_va:
        for c in d["candidates"]:
            if c["engine_va"] == engine_va:
                return json.dumps(c, indent=1)
        return json.dumps({"found": False})
    if nvse_symbol:
        hits = [c for c in d["candidates"]
                if any(nvse_symbol.lower() in s.lower() for s in c["nvse_symbols"])]
        return json.dumps({"count": len(hits), "candidates": hits[:limit]}, indent=1)
    return json.dumps({"referenced_engine_vas": d["referenced_engine_vas"],
                       "top_annotators": d["top_annotator_symbols"][:20]}, indent=1)


@mcp.tool()
def re_mine_pdb(dll: str = "nvse_1_4.dll") -> str:
    """Re-run the NVSE PDB miner (slow: full symbol enumeration + code sweep). Updates nvse_xrefs.json."""
    d = __import__("mine_pdb").mine(resolve_target(dll), resolve_target("FalloutNV.exe"))
    NVSE_XREFS.write_text(json.dumps(d, indent=1), encoding="utf-8")
    return json.dumps({"ok": True, "referenced_engine_vas": d["referenced_engine_vas"],
                       "pdb_symbol_count": d["pdb_symbol_count"]})


@mcp.tool()
def re_search_records(binary: str) -> str:
    """Scan a binary for Bethesda record-type 4CC anchors (descriptor table discovery)."""
    hits = correlate_records.scan_binary(_resolve(binary))
    return json.dumps(correlate_records.correlate(hits, {}), indent=1)


@mcp.tool()
def re_form_type(query: str = "") -> str:
    """Engine form-type registry (ordinal <-> 4CC). query = ordinal number or 4CC; empty = full map."""
    reg = json.loads(FORM_REGISTRY.read_text(encoding="utf-8"))
    if not query:
        return json.dumps(reg, indent=1)
    if query.isdigit():
        return json.dumps({"ordinal": int(query), "record": reg.get(str(int(query)))})
    matches = {o: r for o, r in reg.items() if r == query.upper()}
    return json.dumps(matches, indent=1)


@mcp.tool()
def re_lookup_symbol(query: str, build_id: str = "") -> str:
    """Query the recovered-symbol KB by (substring of) name. Optional build_id filter."""
    kb = _load_kb()
    hits = [s for s in kb["symbols"]
            if query.lower() in s["name"].lower()
            and (not build_id or s["build_id"] == build_id)]
    return json.dumps({"count": len(hits), "symbols": hits}, indent=1)


@mcp.tool()
def re_save_symbol(name: str, build_id: str, rva: str, provenance: list[str],
                   confidence: float, evidence: list[dict], status: str = "candidate") -> str:
    """Add/revise a symbol in the KB. Policy-enforced: rva mandatory (va derived from build), confidence tier must match evidence classes (LLM-only caps at 0.60; >0.80 needs dynamic_trace/experimental_manipulation; 1.00 rejected)."""
    kb = _load_kb()
    if build_id not in kb["builds"]:
        return json.dumps({"error": f"unknown build_id {build_id}", "known": list(kb["builds"])})
    build = kb["builds"][build_id]
    img_base = int(build["image_base"], 16)
    rva_int = int(rva, 16) if rva.lower().startswith("0x") else int(rva)

    RUNTIME_CLASSES = {"dynamic_trace", "experimental_manipulation", "authoritative_source"}
    prov = set(provenance)
    if confidence > 0.95 or confidence < 0.0:
        return json.dumps({"error": "confidence out of range; 1.00 reserved for authoritative_source-only entries"})
    if confidence > 0.80 and not (prov & RUNTIME_CLASSES):
        return json.dumps({"error": "confidence >0.80 requires dynamic_trace or experimental_manipulation evidence"})
    if confidence > 0.60 and not (prov & RUNTIME_CLASSES):
        return json.dumps({"error": "confidence >0.60 requires runtime evidence classes; static evidence caps at 0.60 (confidence-policy.md)"})

    entry = {
        "name": name,
        "build_id": build_id,
        "rva": f"0x{rva_int:08X}",
        "va": f"0x{img_base + rva_int:08X}",
        "provenance": sorted(prov),
        "confidence": confidence,
        "evidence": evidence,
        "equivalences": {},
        "status": status,
        "added": datetime.now(timezone.utc).date().isoformat(),
    }
    for s in kb["symbols"]:
        if s["name"] == name and s["build_id"] == build_id:
            prev = s.get("confidence", 0)
            entry["updated"] = entry["added"]
            entry["previous_confidence"] = prev
            if confidence < prev:
                entry["note"] = f"downgraded {prev} -> {confidence}"
            kb["symbols"].remove(s)
            break
    kb["symbols"].append(entry)
    _save_kb(kb)
    return json.dumps({"ok": True, "va": entry["va"], "confidence": confidence}, indent=1)


@mcp.tool()
def re_hypotheses() -> str:
    """List open hypothesis files with their Status lines."""
    out = []
    hdir = RESEARCH_RE / "hypotheses"
    for f in sorted(hdir.glob("*.md")):
        status = ""
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("**Status:"):
                status = line
                break
        out.append({"file": f.name, "status": status})
    return json.dumps(out, indent=1)


@mcp.tool()
def re_decompiled(va: str = "") -> str:
    """Read cached Ghidra decompilations (research/re/functions/decompiled/). Empty va = list files."""
    if not DECOMPiled_DIR.exists():
        return json.dumps({"files": [], "note": "no decompiled exports yet (run import_ghidra.py with decompile_targets postscript)"})
    if not va:
        return json.dumps({"files": sorted(f.name for f in DECOMPiled_DIR.glob("*.c"))})
    hits = [f for f in DECOMPiled_DIR.glob("*.c") if va.lower().replace("0x", "") in f.name.lower()]
    if not hits:
        return json.dumps({"error": f"no cached decompile contains {va}"})
    return hits[0].read_text(encoding="utf-8")


@mcp.tool()
def re_atlas_pc(pc_address: str) -> str:
    """Query fnv-source-atlas for a PC address (identity, names, Xbox alternatives, evidence). Read-only; consumption rules in research/re/external-sources.md."""
    env = dict(os.environ, PYTHONPATH=str(ATLAS_CLI_DIR))
    out = subprocess.run([sys.executable, "-m", "fnv_atlas", "pc", str(ATLAS_DB), pc_address, "--json"],
                         capture_output=True, text=True, env=env, timeout=300, cwd=str(ATLAS_CLI_DIR))
    if out.returncode != 0:
        return json.dumps({"error": out.stderr[-500:]})
    return out.stdout


@mcp.tool()
def re_atlas_class(class_name: str, exact: bool = True, slot_limit: int = 64) -> str:
    """Query fnv-source-atlas for an Xbox class: vtables, named slots, candidate PC alignments."""
    env = dict(os.environ, PYTHONPATH=str(ATLAS_CLI_DIR))
    cmd = [sys.executable, "-m", "fnv_atlas", "class", str(ATLAS_DB), class_name,
           "--slot-limit", str(slot_limit), "--json"]
    if exact:
        cmd.append("--exact")
    out = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300, cwd=str(ATLAS_CLI_DIR))
    if out.returncode != 0:
        return json.dumps({"error": out.stderr[-500:]})
    return out.stdout


if __name__ == "__main__":
    mcp.run()
