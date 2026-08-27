"""Shared helpers for the scripts/re/ PE analysis tools.

All scripts accept a binary path (FalloutNV.exe, NVSE plugin DLLs, ...) and
default to the Steam install via FNV_GAME_DIR / the hardcoded fallback.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

DEFAULT_GAME_DIR = Path(
    os.environ.get(
        "FNV_GAME_DIR",
        r"H:\01_Games\Steam\steamapps\common\Fallout New Vegas",
    )
)

RESEARCH_RE = Path(__file__).resolve().parents[2] / "research" / "re"


def resolve_target(path: str | None, default_name: str = "FalloutNV.exe") -> Path:
    """Resolve a CLI-supplied path against the game directory."""
    if path:
        p = Path(path)
        if not p.exists() and not p.is_absolute():
            candidate = DEFAULT_GAME_DIR / path
            if candidate.exists():
                return candidate
        return p
    return DEFAULT_GAME_DIR / default_name


def rva_to_offset(pe, rva: int) -> int | None:
    """Translate an RVA to a raw file offset using section headers."""
    for sec in pe.sections:
        start = sec.VirtualAddress
        end = start + max(sec.Misc_VirtualSize, sec.SizeOfRawData)
        if start <= rva < end:
            delta = rva - start
            if delta < sec.SizeOfRawData:
                return sec.PointerToRawData + delta
            return None
    if rva < len(pe.__data__):  # headers
        return rva
    return None


def image_base(pe) -> int:
    return pe.OPTIONAL_HEADER.ImageBase


def va_to_rva(pe, va: int) -> int:
    return va - image_base(pe)


def parse_int(text: str) -> int:
    """Parse '0x...' as hex, anything else as int."""
    return int(text, 16) if text.lower().startswith(("0x", "-0x")) else int(text, 0)


def exec_sections(pe):
    """Sections flagged executable."""
    return [s for s in pe.sections if s.Characteristics & 0x20000000]


def load_pe(path: Path):
    import pefile

    try:
        return pefile.PE(str(path), fast_load=False)
    except pefile.PEFormatError as e:
        raise SystemExit(f"error: {path} is not a valid PE file: {e}")


def iter_insns(blob: bytes, va: int):
    """Resilient 32-bit x86 linear sweep: resumes after undecodable bytes."""
    import capstone

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    pos = 0
    while pos < len(blob):
        last = pos
        for insn in md.disasm(blob[pos:], va + pos):
            last = insn.address - va + insn.size
            yield insn
        if last == pos:
            pos += 1
        else:
            pos = last


def build_identity(path: Path) -> dict:
    """Full build identity: the key against which every recovered symbol is stored."""
    import hashlib

    import pefile

    data = path.read_bytes()
    pe = pefile.PE(str(path), fast_load=True)
    return {
        "file": path.name,
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "pe_timestamp": f"0x{pe.FILE_HEADER.TimeDateStamp:08X}",
        "image_base": f"0x{pe.OPTIONAL_HEADER.ImageBase:08X}",
        "size_of_image": f"0x{pe.OPTIONAL_HEADER.SizeOfImage:X}",
        "machine": "i386" if pe.FILE_HEADER.Machine == 0x14C else hex(pe.FILE_HEADER.Machine),
    }


def warn_if_encrypted(pe, path) -> None:
    """Flag exec sections whose entropy suggests encrypted/packed code.

    The Steam FalloutNV.exe carries CEG-style protection: .text is encrypted
    at rest (entropy ~8.0) and decrypted at launch by a stub in .bind. Static
    code analysis on such an image produces garbage — get a CEG-free exe
    (GoG) or dump the process after unpacking. Data sections (.rdata
    strings, record tables) remain readable either way.
    """
    for s in pe.sections:
        if s.Characteristics & 0x20000000 and s.get_entropy() > 7.5:
            name = s.Name.rstrip(b"\x00").decode(errors="replace")
            print(
                f"# warning: exec section {name} in {path} has entropy "
                f"{s.get_entropy():.2f} — code is likely encrypted/packed; "
                "disassembly/xref results will be garbage",
                file=sys.stderr,
            )


def emit(data, as_json: bool, human_renderer):
    if as_json:
        print(json.dumps(data, indent=2, default=str))
    else:
        human_renderer(data)
