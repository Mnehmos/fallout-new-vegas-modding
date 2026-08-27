"""PE structure inspector for FalloutNV.exe / NVSE plugin DLLs.

Usage:
    python inspect_pe.py [path] [--json]
    python inspect_pe.py nvse_1.dll --json

Reports machine type, section table, timestamp, imports (DLL + functions),
exports, and TLS usage — the "what am I looking at" first pass.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pe_utils import emit, load_pe, resolve_target

MACHINE = {0x14C: "i386 (32-bit x86)", 0x8664: "AMD64 (64-bit x64)", 0x1C0: "ARM"}


def inspect(path: Path) -> dict:
    pe = load_pe(path)
    oh = pe.OPTIONAL_HEADER

    sections = []
    for s in pe.sections:
        sections.append(
            {
                "name": s.Name.rstrip(b"\x00").decode(errors="replace"),
                "va": f"0x{pe.OPTIONAL_HEADER.ImageBase + s.VirtualAddress:08X}",
                "vsize": s.Misc_VirtualSize,
                "rawsize": s.SizeOfRawData,
                "entropy": round(s.get_entropy(), 3),
                "flags": {
                    "exec": bool(s.Characteristics & 0x20000000),
                    "read": bool(s.Characteristics & 0x40000000),
                    "write": bool(s.Characteristics & 0x80000000),
                },
            }
        )

    imports = {}
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll = entry.dll.decode(errors="replace")
            funcs = []
            for imp in entry.imports:
                funcs.append(imp.name.decode(errors="replace") if imp.name else f"ord#{imp.ordinal}")
            imports[dll] = funcs

    exports = []
    if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            exports.append(exp.name.decode(errors="replace") if exp.name else f"ord#{exp.ordinal}")

    md5 = hashlib.md5(path.read_bytes()).hexdigest()

    return {
        "file": str(path),
        "size": path.stat().st_size,
        "md5": md5,
        "machine": MACHINE.get(pe.FILE_HEADER.Machine, hex(pe.FILE_HEADER.Machine)),
        "subsystem": "GUI" if oh.Subsystem == 2 else f"0x{oh.Subsystem:X}",
        "image_base": f"0x{oh.ImageBase:08X}",
        "entry_point_rva": f"0x{oh.AddressOfEntryPoint:08X}",
        "timestamp_utc": pe.FILE_HEADER.TimeDateStamp,
        "is_dll": bool(pe.FILE_HEADER.Characteristics & 0x2000),
        "sections": sections,
        "import_count": sum(len(v) for v in imports.values()),
        "imports": imports,
        "exports": exports,
        "has_tls": hasattr(pe, "DIRECTORY_ENTRY_TLS"),
    }


def human(data: dict) -> None:
    print(f"== {Path(data['file']).name} ==")
    print(f"  {data['machine']}, {'DLL' if data['is_dll'] else 'EXE'}, subsystem {data['subsystem']}")
    print(f"  md5 {data['md5']}  size {data['size']:,}")
    print(f"  image base {data['image_base']}  entry RVA {data['entry_point_rva']}")
    print(f"  TLS: {'yes' if data['has_tls'] else 'no'}")
    print("\n  Sections:")
    for s in data["sections"]:
        flags = ("".join(["x" if s["flags"]["exec"] else "-",
                          "w" if s["flags"]["write"] else "-",
                          "r" if s["flags"]["read"] else "-"]))
        print(f"    {s['name']:10s} {s['va']}  vsize={s['vsize']:>9,}  [{flags}]  entropy={s['entropy']}")
    print(f"\n  Imports: {data['import_count']} functions from {len(data['imports'])} DLLs")
    for dll, funcs in data["imports"].items():
        print(f"    {dll}: {len(funcs)}")
        for f in funcs[:5]:
            print(f"        {f}")
        if len(funcs) > 5:
            print(f"        ... +{len(funcs) - 5} more")
    if data["exports"]:
        print(f"\n  Exports ({len(data['exports'])}):")
        for e in data["exports"][:20]:
            print(f"    {e}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", help="PE file (absolute, or relative to FNV game dir)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    target = resolve_target(args.path)
    if not target.exists():
        raise SystemExit(f"error: not found: {target}")
    emit(inspect(target), args.json, human)


if __name__ == "__main__":
    main()
