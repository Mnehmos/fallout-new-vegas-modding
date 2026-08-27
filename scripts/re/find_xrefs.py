"""Find cross-references to an address in 32-bit x86 PE code.

Usage:
    python find_xrefs.py <binary> <VA> [--json]
    python find_xrefs.py FalloutNV.exe 0x00FE1234
    python find_xrefs.py FalloutNV.exe --string "Population"

Finds occurrences of the target VA as a 32-bit immediate (push/mov/cmp ...) or
as a call/jmp rel32 target in executable sections, then reports site VA plus
opcode context. Quick-and-dirty by design — Ghidra's real xref engine
(scripts/re/import_ghidra.py) is the authoritative pass; this exists for fast
iteration straight from the CLI.
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pe_utils import emit, exec_sections, load_pe, parse_int, resolve_target, rva_to_offset, warn_if_encrypted

# opcodes that commonly precede an imm32 reference (push imm, mov r32 imm, cmp, test, lea-ish forms)
IMM_OPCODES = {
    0x68: "push imm32",
    0x3D: "cmp eax, imm32",
    0xA0: "mov al, [imm32]",
    0xB8: "mov eax, imm32", 0xB9: "mov ecx, imm32", 0xBA: "mov edx, imm32",
    0xBB: "mov ebx, imm32", 0xBC: "mov esp, imm32", 0xBD: "mov ebp, imm32",
    0xBE: "mov esi, imm32", 0xBF: "mov edi, imm32",
    0x05: "add eax, imm32", 0x2D: "sub eax, imm32",
}


def find_string_va(path: Path, needle: str) -> list[int]:
    """Locate the VA(s) of an exact ASCII string in the image."""
    data = path.read_bytes()
    pe = load_pe(path)
    base = pe.OPTIONAL_HEADER.ImageBase
    hits = []
    raw = needle.encode("ascii") + b"\x00"
    idx = data.find(raw)
    while idx != -1:
        for s in pe.sections:
            if s.PointerToRawData <= idx < s.PointerToRawData + s.SizeOfRawData:
                hits.append(base + s.VirtualAddress + (idx - s.PointerToRawData))
                break
        idx = data.find(raw, idx + 1)
    return hits


def find_xrefs(path: Path, target_va: int) -> list[dict]:
    pe = load_pe(path)
    warn_if_encrypted(pe, path)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = path.read_bytes()
    results = []

    pat = struct.pack("<I", target_va)

    for sec in exec_sections(pe):
        start = sec.PointerToRawData
        end = start + sec.SizeOfRawData
        blob = data[start:end]
        idx = blob.find(pat)
        while idx != -1:
            site_rva = sec.VirtualAddress + idx
            kind = "imm32"
            detail = "data/imm reference"
            prev = blob[idx - 1] if idx > 0 else None
            if prev in IMM_OPCODES:
                detail = IMM_OPCODES[prev]
            elif prev in (0xE8, 0xE9):
                # would only match if call/jmp rel32 landed exactly on target — handled below
                detail = "call/jmp tail"
                kind = "branch"
            results.append({
                "site_va": f"0x{base + site_rva:08X}",
                "section": sec.Name.rstrip(b"\x00").decode(errors="replace"),
                "kind": kind,
                "detail": detail,
            })
            idx = blob.find(pat, idx + 1)

        # rel32 call/jmp: opcode at i, target = next_instr_rva + rel
        i = 0
        while True:
            i = blob.find(b"\xE8", i + 1)
            if i == -1 or i + 5 > len(blob):
                break
            rel = struct.unpack_from("<i", blob, i + 1)[0]
            if sec.VirtualAddress + i + 5 + rel == target_va - base:
                results.append({
                    "site_va": f"0x{base + sec.VirtualAddress + i:08X}",
                    "section": sec.Name.rstrip(b"\x00").decode(errors="replace"),
                    "kind": "branch",
                    "detail": "call rel32",
                })
        i = 0
        while True:
            i = blob.find(b"\xE9", i + 1)
            if i == -1 or i + 5 > len(blob):
                break
            rel = struct.unpack_from("<i", blob, i + 1)[0]
            if sec.VirtualAddress + i + 5 + rel == target_va - base:
                results.append({
                    "site_va": f"0x{base + sec.VirtualAddress + i:08X}",
                    "section": sec.Name.rstrip(b"\x00").decode(errors="replace"),
                    "kind": "branch",
                    "detail": "jmp rel32",
                })

    return sorted(results, key=lambda r: int(r["site_va"], 16))


def human(rows: list[dict]) -> None:
    if not rows:
        print("no cross-references found")
    for r in rows:
        print(f"{r['site_va']}  {r['kind']:7s} {r['detail']:20s} [{r['section']}]")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", help="PE file (absolute, or relative to FNV game dir)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("va", nargs="?", help="target virtual address, e.g. 0x00FE1234")
    g.add_argument("--string", help="locate exact string, then xref its VA")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = resolve_target(args.path)
    if not target.exists():
        raise SystemExit(f"error: not found: {target}")

    if args.string:
        vas = find_string_va(target, args.string)
        if not vas:
            raise SystemExit(f"error: string not found: {args.string!r}")
        print(f"# string {args.string!r} at " + ", ".join(f"0x{v:08X}" for v in vas), file=sys.stderr)
        rows = []
        for va in vas:
            rows.extend(find_xrefs(target, va))
    else:
        rows = find_xrefs(target, parse_int(args.va))
    emit(rows, args.json, human)


if __name__ == "__main__":
    main()
