"""Generate reusable function fingerprints for a 32-bit x86 PE.

Modes:

1. Single function (default):
    python fingerprint_functions.py <binary> --fn 0x00842F10

2. Whole-binary database (--all): multi-fingerprint every candidate function
   for cross-build equivalence matching (see match_functions.py).
    python fingerprint_functions.py <binary> --all --build-id nvse-1.4-runtime

Independent fingerprints collected per function:
  exact bytes | masked IDA signature | mnemonic sequence hash |
  mnemonic 3-grams | call targets/degree | referenced image constants |
  referenced strings | referenced record 4CCs

No single fingerprint is trusted alone; match_functions.py triangulates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pe_utils import (
    RESEARCH_RE, emit, exec_sections, iter_insns, load_pe, parse_int,
    resolve_target, rva_to_offset, warn_if_encrypted,
)

PROLOGUES = (b"\x55\x8B\xEC", b"\x55\x89\xE5", b"\x8B\xFF\x55\x8B\xEC")
RECORD_TYPES = [
    "ECZN", "LVLI", "LVLN", "LVLC", "NPC_", "ACHR", "REFR", "CELL", "WRLD",
    "CREA", "CONT", "LIGH", "SPEL", "PERK", "ENCH", "MGEF", "PACK", "TES4",
    "DIAL", "INFO", "QUST", "IDLE", "IMAD", "IPCT",
]
import re as _re

STRING_RE = _re.compile(rb"[\x20-\x7e]{4,}")


def function_extent(blob: bytes, off: int, hard_max: int = 4096) -> int:
    i = off + 3
    while i < min(off + hard_max, len(blob) - 1):
        b = blob[i]
        if b == 0xC3 and blob[i + 1] in (0x90, 0xCC, 0xC3, 0xE9, 0x55, 0x8B):
            return i + 1 - off
        if b == 0xCC and blob[i - 1] == 0xCC:
            return i - 1 - off
        i += 1
    return min(hard_max, len(blob) - off)


def mask_sig(insns_iter, blob_len: int, cap: int = 64) -> tuple[str, list, list]:
    """Walk one function: masked signature + immediate references."""
    sig_parts: list = []
    mnemonics: list = []
    imm_consts: list = []
    call_targets: list = []
    string_refs: list = []
    fourcc_refs: list = []
    used = 0

    for insn in insns_iter:
        if used >= cap:
            break
        mnemonics.append(insn.mnemonic)
        fixed = len(insn.bytes)
        op = insn.op_str
        if insn.mnemonic in ("call", "jmp") and op.startswith("0x"):
            fixed = 1
            try:
                call_targets.append(int(op, 16))
            except ValueError:
                pass
        elif "0x" in op:
            fixed = min(fixed, len(insn.bytes))
            # capture immediates that look like in-image addresses/4CCs
            try:
                tail = op.rsplit(",", 1)[-1].strip()
                if tail.startswith("0x"):
                    v = int(tail, 16)
                    if v > 0x10000:
                        imm_consts.append(v)
            except ValueError:
                pass
        sig_parts.append(insn.bytes[:fixed])
        sig_parts.append([None] * (len(insn.bytes) - fixed))
        used += len(insn.bytes)

    flat = [b for chunk in sig_parts for b in chunk]
    sig_str = " ".join(f"{b:02X}" if b is not None else "??" for b in flat)
    return sig_str, mnemonics, {
        "imm_consts": imm_consts,
        "call_targets": call_targets,
        "string_refs": string_refs,
        "fourcc_refs": fourcc_refs,
    }


def single_fingerprint(path: Path, fn_va: int, max_bytes: int) -> dict:
    pe = load_pe(path)
    warn_if_encrypted(pe, path)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = path.read_bytes()

    sec = None
    for s in exec_sections(pe):
        if s.VirtualAddress <= fn_va - base < s.VirtualAddress + s.Misc_VirtualSize:
            sec = s
            break
    if sec is None:
        raise SystemExit(f"error: VA {fn_va:#010x} not inside an executable section")

    off = rva_to_offset(pe, fn_va - base)
    length = min(function_extent(data, off), max_bytes)
    fn_bytes = data[off:off + length]

    sig_str, mnemonics, _refs = mask_sig(iter_insns(fn_bytes, fn_va), len(fn_bytes), cap=max_bytes)
    mnem_hash = hashlib.sha256(" ".join(mnemonics).encode()).hexdigest()[:16]
    return {
        "file": str(path),
        "function_va": f"0x{fn_va:08X}",
        "function_rva": f"0x{fn_va - base:08X}",
        "length": length,
        "ida_signature": sig_str,
        "mnemonic_hash": mnem_hash,
        "instruction_count": len(mnemonics),
    }


def collect_function_starts(pe, data: bytes, base: int) -> list[int]:
    starts = set()
    for sec in exec_sections(pe):
        blob = data[sec.PointerToRawData:sec.PointerToRawData + sec.SizeOfRawData]
        for pl in PROLOGUES:
            i = blob.find(pl)
            while i != -1:
                starts.add(base + sec.VirtualAddress + i)
                i = blob.find(pl, i + 1)
        for insn in iter_insns(blob, base + sec.VirtualAddress):
            if insn.mnemonic == "call" and insn.op_str.startswith("0x"):
                try:
                    t = int(insn.op_str, 16)
                    if base + sec.VirtualAddress <= t < base + sec.VirtualAddress + sec.Misc_VirtualSize:
                        starts.add(t)
                except ValueError:
                    pass
    return sorted(starts)


def fingerprint_all(path: Path, build_id: str, out_path: Path | None) -> dict:
    pe = load_pe(path)
    warn_if_encrypted(pe, path)
    base = pe.OPTIONAL_HEADER.ImageBase
    img_end = base + pe.OPTIONAL_HEADER.SizeOfImage
    data = path.read_bytes()

    string_vas = {base + m.start() for m in STRING_RE.finditer(data)}
    fourcc_ints = {struct.unpack("<I", rt.encode())[0]: rt for rt in RECORD_TYPES}

    starts = collect_function_starts(pe, data, base)
    print(f"# {len(starts)} candidate function starts", file=sys.stderr)

    starts_by_sec = []
    for sec in exec_sections(pe):
        lo = base + sec.VirtualAddress
        hi = lo + sec.Misc_VirtualSize
        ss = [s for s in starts if lo <= s < hi]
        starts_by_sec.append((sec, ss))

    functions = []
    for sec, ss in starts_by_sec:
        blob = data[sec.PointerToRawData:sec.PointerToRawData + sec.SizeOfRawData]
        sec_lo = base + sec.VirtualAddress
        for i, va in enumerate(ss):
            end = ss[i + 1] if i + 1 < len(ss) else va + 8192
            off = va - sec_lo
            fn_bytes = blob[off:off + min(end - va, 8192)]
            sig_str, mnemonics, refs = mask_sig(iter_insns(fn_bytes, va), len(fn_bytes), cap=64)

            grams = {" ".join(mnemonics[j:j + 3]) for j in range(len(mnemonics) - 2)}
            gram_hashes = sorted(hashlib.sha1(g.encode()).hexdigest()[:8] for g in grams)

            consts = sorted({r - base for r in refs["imm_consts"] if base <= r < img_end})
            strs = sorted({r - base for r in refs["imm_consts"] if r in string_vas})
            fccs = sorted({fourcc_ints[r] for r in refs["imm_consts"] if r in fourcc_ints})
            calls = sorted({t - base for t in refs["call_targets"] if base <= t < img_end})

            functions.append({
                "rva": f"0x{va - base:08X}",
                "size": min(end - va, 8192),
                "exact_head16": fn_bytes[:16].hex(" "),
                "masked_sig": sig_str,
                "mnemonic_hash": hashlib.sha256(" ".join(mnemonics).encode()).hexdigest()[:16],
                "ngram3": gram_hashes[:512],
                "out_degree": len(calls),
                "call_targets_rva": [f"0x{c:08X}" for c in calls[:64]],
                "imm_const_rvas": [f"0x{c:08X}" for c in consts[:64]],
                "string_ref_rvas": [f"0x{s:08X}" for s in strs[:32]],
                "record_4cc_refs": fccs,
            })

    db = {
        "schema": 1,
        "build_id": build_id,
        "file": str(path),
        "function_count": len(functions),
        "functions": functions,
    }
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(db, indent=0), encoding="utf-8")
        print(f"# wrote {out_path}", file=sys.stderr)
    return db


def human(fp: dict) -> None:
    if "functions" in fp:
        print(f"{fp['build_id']}: {fp['function_count']} functions fingerprinted")
        return
    print(f"function {fp['function_va']}  ({fp['length']} bytes, {fp['instruction_count']} insns)")
    print(f"mnemonic hash : {fp['mnemonic_hash']}")
    print(f"IDA signature : {fp['ida_signature']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", help="PE file (absolute, or relative to FNV game dir)")
    ap.add_argument("--fn", help="single-function mode: function VA, e.g. 0x00842F10")
    ap.add_argument("--all", action="store_true", help="database mode: fingerprint all functions")
    ap.add_argument("--build-id", help="build id for --all mode (e.g. nvse-1.4-runtime)")
    ap.add_argument("--out", help="output path for --all mode")
    ap.add_argument("--max-bytes", type=int, default=96, help="single-mode signature cap")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = resolve_target(args.path)
    if not target.exists():
        raise SystemExit(f"error: not found: {target}")

    if args.all:
        if not args.build_id:
            raise SystemExit("error: --all requires --build-id")
        default_out = RESEARCH_RE / "signatures" / f"{args.build_id}.fnprints.json"
        db = fingerprint_all(target, args.build_id, Path(args.out or default_out))
        emit(db, args.json, human)
    else:
        if not args.fn:
            raise SystemExit("error: give --fn VA or --all")
        emit(single_fingerprint(target, parse_int(args.fn), args.max_bytes), args.json, human)


if __name__ == "__main__":
    main()
