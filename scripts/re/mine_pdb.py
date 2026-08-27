"""Mine the NVSE PDB for engine-address references.

Usage:
    python mine_pdb.py [nvse_dll] [--out research/re/nvse_xrefs.json] [--json]

NVSE is a human-written annotation layer over FalloutNV internals: its
functions wrap engine addresses with meaningful names. This tool turns that
into structured evidence:

    PDB symbols (dbghelp)  +  capstone sweep of nvse_1_4.dll
        -> every reference into the FalloutNV.exe image range
        -> engine VA + containing NVSE symbol + instruction kind
        -> research/re/nvse_xrefs.json  (candidate engine symbols)

Provenance class for these hits: nvse_semantic_reference / nvse_hardcoded_reference
(see research/re/confidence-policy.md — static cap 0.60).
"""
from __future__ import annotations

import argparse
import bisect
import ctypes
import json
import struct
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pefile

from pe_utils import DEFAULT_GAME_DIR, RESEARCH_RE, emit, exec_sections, load_pe, resolve_target, iter_insns

# SYMOPT_UNDNAME | SYMOPT_NO_PROMPTS | SYMOPT_DEFERRED_LOADS
SYM_OPTS = 0x2 | 0x80000 | 0x4

SYM_TAGS = {5: "func", 7: "data", 10: "public", 11: "label"}


class SYMBOL_INFOW(ctypes.Structure):
    _fields_ = [
        ("SizeOfStruct", ctypes.c_ulong),
        ("TypeIndex", ctypes.c_ulong),
        ("Reserved", ctypes.c_ulonglong * 2),
        ("Index", ctypes.c_ulong),
        ("Size", ctypes.c_ulong),
        ("ModBase", ctypes.c_ulonglong),
        ("Flags", ctypes.c_ulong),
        ("Value", ctypes.c_ulonglong),
        ("Address", ctypes.c_ulonglong),
        ("Register", ctypes.c_ulong),
        ("Scope", ctypes.c_ulong),
        ("Tag", ctypes.c_ulong),
        ("NameLen", ctypes.c_ulong),
        ("MaxNameLen", ctypes.c_ulong),
        ("Name", ctypes.c_wchar * 2048),
    ]


def enumerate_pdb_symbols(dll_path: Path) -> list[dict]:
    dbghelp = ctypes.WinDLL("dbghelp.dll")
    k32 = ctypes.WinDLL("kernel32.dll")
    HANDLE = ctypes.c_void_p
    k32.GetCurrentProcess.restype = HANDLE

    dbghelp.SymSetOptions.argtypes = [ctypes.c_ulong]
    dbghelp.SymInitializeW.argtypes = [HANDLE, ctypes.c_wchar_p, ctypes.c_bool]
    dbghelp.SymLoadModuleExW.argtypes = [HANDLE, HANDLE, ctypes.c_wchar_p, ctypes.c_wchar_p,
                                         ctypes.c_ulonglong, ctypes.c_ulong, ctypes.c_void_p, ctypes.c_ulong]
    dbghelp.SymEnumSymbolsW.argtypes = [HANDLE, ctypes.c_ulonglong, ctypes.c_wchar_p,
                                        ctypes.c_void_p, ctypes.c_void_p]
    dbghelp.SymCleanup.argtypes = [HANDLE]

    CALLBACK = ctypes.WINFUNCTYPE(
        ctypes.c_bool, ctypes.POINTER(SYMBOL_INFOW), ctypes.c_ulong, ctypes.c_void_p
    )

    dbghelp.SymSetOptions(SYM_OPTS)
    hproc = k32.GetCurrentProcess()

    search = str(dll_path.parent)
    if not dbghelp.SymInitializeW(hproc, search, False):
        raise SystemExit(f"error: SymInitializeW failed (err={ctypes.GetLastError()})")

    pe = pefile.PE(str(dll_path), fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    size = pe.OPTIONAL_HEADER.SizeOfImage

    loaded = dbghelp.SymLoadModuleExW(
        hproc, None, str(dll_path), None, base, size, None, 0
    )
    if not loaded:
        raise SystemExit(f"error: SymLoadModuleExW failed (err={ctypes.GetLastError()})")

    symbols: list[dict] = []

    @CALLBACK
    def on_symbol(si, sym_size, _ctx):
        try:
            name = si.contents.Name[: si.contents.NameLen]
            symbols.append({
                "va": int(si.contents.Address),
                "size": int(si.contents.Size),
                "tag": int(si.contents.Tag),
                "name": name,
            })
        except Exception:
            pass
        return True

    if not dbghelp.SymEnumSymbolsW(hproc, loaded, "*", on_symbol, None):
        if not symbols:
            print("# warning: SymEnumSymbolsW returned false and no symbols", file=sys.stderr)

    dbghelp.SymCleanup(hproc)
    symbols.sort(key=lambda s: s["va"])
    return symbols


def engine_image_map(exe_path: Path) -> dict:
    """Engine exe region map for tagging referenced engine VAs."""
    pe = pefile.PE(str(exe_path), fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    regions = []
    for s in pe.sections:
        name = s.Name.rstrip(b"\x00").decode(errors="replace")
        regions.append((base + s.VirtualAddress, base + s.VirtualAddress + s.Misc_VirtualSize, name))
    return {"base": base, "end": base + pe.OPTIONAL_HEADER.SizeOfImage, "regions": regions}


def engine_region(img: dict, va: int) -> str:
    if not (img["base"] <= va < img["end"]):
        return "outside"
    for lo, hi, name in img["regions"]:
        if lo <= va < hi:
            return name
    return "headers"


def containing_symbol(sorted_syms, addrs, va: int):
    i = bisect.bisect_right(addrs, va) - 1
    if i < 0:
        return None, "none"
    s = sorted_syms[i]
    if s["size"] and s["va"] <= va < s["va"] + s["size"]:
        return s, "exact"
    return s, "nearest"


def mine(dll_path: Path, exe_path: Path) -> dict:
    syms = enumerate_pdb_symbols(dll_path)
    print(f"# pdb symbols: {len(syms)}", file=sys.stderr)
    addrs = [s["va"] for s in syms]

    img = engine_image_map(exe_path)

    pe = load_pe(dll_path)
    base = pe.OPTIONAL_HEADER.ImageBase
    self_lo, self_hi = base, base + pe.OPTIONAL_HEADER.SizeOfImage
    data = dll_path.read_bytes()

    sites_by_engine_va = defaultdict(list)
    refs_by_nvse_symbol = defaultdict(set)

    def in_engine(va: int) -> bool:
        return img["base"] <= va < img["end"] and not (self_lo <= va < self_hi)

    def record(engine_va, dll_va, kind, sym, attribution):
        sname = sym["name"] if sym else None
        sites_by_engine_va[engine_va].append({
            "site": f"0x{dll_va:08X}",
            "kind": kind,
            "nvse_symbol": sname,
            "attribution": attribution,
        })
        if sname:
            refs_by_nvse_symbol[sname].add(engine_va)

    def try_record(target, dll_va, kind):
        if not in_engine(target):
            return
        sym, attr = containing_symbol(syms, addrs, dll_va)
        record(target, dll_va, kind, sym, attr)

    # 1. code sweep: immediates and memory displacements pointing into the engine image
    for sec in exec_sections(pe):
        sec_name = sec.Name.rstrip(b"\x00").decode(errors="replace")
        blob = data[sec.PointerToRawData:sec.PointerToRawData + sec.SizeOfRawData]
        for insn in iter_insns(blob, base + sec.VirtualAddress):
            for op in insn.operands:
                target = None
                if op.type == 2:  # IMM
                    target = op.imm & 0xFFFFFFFF
                    kind = f"{insn.mnemonic}_imm"
                elif op.type == 3 and insn.mnemonic != "lea":  # MEM disp (lea is our own addressing)
                    target = op.mem.disp & 0xFFFFFFFF
                    kind = f"{insn.mnemonic}_[disp]"
                if target is None:
                    continue
                try_record(target, insn.address, kind)

    # 2. raw data sweep: pointer tables / patch tables in initialized data
    for sec in pe.sections:
        if sec.Characteristics & 0x20000000:
            continue
        if not (sec.Characteristics & 0x40000000):  # must be readable
            continue
        sec_name = sec.Name.rstrip(b"\x00").decode(errors="replace")
        blob = data[sec.PointerToRawData:sec.PointerToRawData + sec.SizeOfRawData]
        for off in range(0, len(blob) - 3, 4):  # aligned: real pointer tables are 4-aligned
            v = struct.unpack_from("<I", blob, off)[0]
            if in_engine(v):
                try_record(v, base + sec.VirtualAddress + off, "data_ptr")

    # 3. aggregate — attribution quality matters: exact containment beats nearest-guess
    results = []
    for engine_va in sorted(sites_by_engine_va):
        sites = sites_by_engine_va[engine_va]
        exact_syms = sorted({s["nvse_symbol"] for s in sites if s["attribution"] == "exact" and s["nvse_symbol"]})
        nearest_syms = sorted({s["nvse_symbol"] for s in sites if s["attribution"] == "nearest" and s["nvse_symbol"]})
        kinds = sorted({s["kind"] for s in sites})
        results.append({
            "engine_va": f"0x{engine_va:08X}",
            "engine_rva": f"0x{engine_va - img['base']:08X}",
            "engine_region": engine_region(img, engine_va),
            "evidence_score": len(exact_syms) * 3 + len(nearest_syms) + len(kinds),
            "nvse_symbols": exact_syms or nearest_syms,
            "attribution": "exact" if exact_syms else "nearest",
            "kinds": kinds,
            "site_count": len(sites),
            "sites": sites[:20],
        })

    annotators = sorted(
        ((len(v), k) for k, v in refs_by_nvse_symbol.items()), reverse=True
    )[:40]

    return {
        "dll": str(dll_path),
        "engine_exe": str(exe_path),
        "engine_image_range": [f"0x{img['base']:08X}", f"0x{img['end']:08X}"],
        "pdb_symbol_count": len(syms),
        "referenced_engine_vas": len(results),
        "candidates": results,
        "top_annotator_symbols": [{"nvse_symbol": k, "distinct_engine_refs": n} for n, k in annotators],
    }


def human(data: dict) -> None:
    print(f"{data['dll']}")
    print(f"engine image: {data['engine_image_range'][0]}..{data['engine_image_range'][1]}")
    print(f"pdb symbols: {data['pdb_symbol_count']}   referenced engine VAs: {data['referenced_engine_vas']}")
    print("\ntop candidates by evidence score:")
    for c in sorted(data["candidates"], key=lambda r: -r["evidence_score"])[:25]:
        print(f"  {c['engine_va']} [{c['engine_region']:7s}] score={c['evidence_score']:3d}")
        for s in c["nvse_symbols"][:3]:
            print(f"      <- {s}")
    print("\ntop annotator symbols (NVSE functions mapping the engine):")
    for a in data["top_annotator_symbols"][:15]:
        print(f"  {a['distinct_engine_refs']:4d} refs  {a['nvse_symbol']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dll", nargs="?", default="nvse_1_4.dll",
                    help="NVSE DLL with a PDB (default nvse_1_4.dll)")
    ap.add_argument("--engine", default="FalloutNV.exe", help="engine exe defining the VA range")
    ap.add_argument("--out", default=str(RESEARCH_RE / "nvse_xrefs.json"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    dll_path = resolve_target(args.dll)
    exe_path = resolve_target(args.engine)
    if not dll_path.exists():
        raise SystemExit(f"error: not found: {dll_path}")
    if not exe_path.exists():
        raise SystemExit(f"error: not found: {exe_path}")

    data = mine(dll_path, exe_path)
    out = Path(args.out)
    out.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(f"# wrote {out}", file=sys.stderr)
    emit(data, args.json, human)


if __name__ == "__main__":
    main()
