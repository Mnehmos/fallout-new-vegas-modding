"""
MnemoScript Compiler — main entry point.

Usage:
  python compiler.py input.mns                    # compile and print hex dump
  python compiler.py input.mns --output out.bin   # compile to raw SCPT subrecords
  python compiler.py input.mns --inject target.esp # compile and inject into ESP
"""
from __future__ import annotations
import sys
import os
import struct
import argparse

# Add script dir to path for sibling imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import tokenize, LexError
from parser import parse, ParseError
from emitter import compile_script, EmitError


def compile_file(path: str) -> dict:
    """Compile a .mns file to SCPT subrecord data."""
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    return compile_source(source)


def compile_source(source: str) -> dict:
    """Compile MnemoScript source text to SCPT subrecord data."""
    tokens = tokenize(source)
    ast = parse(tokens)
    return compile_script(ast, source)


def dump_hex(data: bytes, label: str = '', width: int = 16):
    """Pretty-print hex dump of bytes."""
    if label:
        print(f"\n--- {label} ({len(data)} bytes) ---")
    for offset in range(0, len(data), width):
        chunk = data[offset:offset+width]
        hex_part = ' '.join(f'{b:02X}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f'  {offset:04X}: {hex_part:<{width*3}}  {ascii_part}')


def build_scpt_record(subrecords: dict) -> bytes:
    """Build a complete SCPT record from compiled subrecords.

    Returns the full record including header, ready for ESP injection.
    """
    # Build subrecord chain
    data = bytearray()

    # EDID
    edid_data = subrecords['EDID']
    data += b'EDID'
    data += struct.pack('<H', len(edid_data))
    data += edid_data

    # SCHR
    schr_data = subrecords['SCHR']
    data += b'SCHR'
    data += struct.pack('<H', len(schr_data))
    data += schr_data

    # SCDA
    scda_data = subrecords['SCDA']
    data += b'SCDA'
    data += struct.pack('<H', len(scda_data))
    data += scda_data

    # SCTX (source text — optional but useful for GECK display)
    if subrecords['SCTX']:
        sctx_data = subrecords['SCTX']
        data += b'SCTX'
        data += struct.pack('<H', len(sctx_data))
        data += sctx_data

    # SLSD + SCVR pairs
    for slsd, scvr in subrecords['SLSD_SCVR']:
        data += b'SLSD'
        data += struct.pack('<H', len(slsd))
        data += slsd
        data += b'SCVR'
        data += struct.pack('<H', len(scvr))
        data += scvr

    # SCRO
    for scro in subrecords['SCRO']:
        data += b'SCRO'
        data += struct.pack('<H', len(scro))
        data += scro

    # Record header: 'SCPT' + dataSize(4) + flags(4) + formID(4) + revision(4) + version(2) + unknown(2)
    # For injection, the caller assigns FormID. We use placeholder 0.
    record_header = b'SCPT'
    record_header += struct.pack('<I', len(data))  # data size
    record_header += struct.pack('<I', 0)          # flags
    record_header += struct.pack('<I', 0)          # formID (placeholder)
    record_header += struct.pack('<I', 0)          # revision
    record_header += struct.pack('<H', 15)         # version (FNV = 15)
    record_header += struct.pack('<H', 0)          # unknown

    return bytes(record_header + data)


def main():
    ap = argparse.ArgumentParser(description='MnemoScript Compiler for Fallout New Vegas')
    ap.add_argument('input', help='Input .mns file')
    ap.add_argument('--output', '-o', help='Output binary file')
    ap.add_argument('--inject', help='Target ESP to inject SCPT into')
    ap.add_argument('--quiet', '-q', action='store_true', help='Suppress hex dump')
    args = ap.parse_args()

    try:
        subrecords = compile_file(args.input)
    except (LexError, ParseError, EmitError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"=== MnemoScript Compiler ===")
        print(f"Script: {subrecords['EDID'].rstrip(b'\\x00').decode()}")
        print(f"Variables: {len(subrecords['SLSD_SCVR'])}")
        print(f"References: {len(subrecords['SCRO'])}")
        print(f"Bytecode: {len(subrecords['SCDA'])} bytes")

        dump_hex(subrecords['SCHR'], 'SCHR')
        dump_hex(subrecords['SCDA'], 'SCDA (bytecode)')

    if args.output:
        record = build_scpt_record(subrecords)
        with open(args.output, 'wb') as f:
            f.write(record)
        print(f"\nWrote {len(record)} bytes to {args.output}")

    if args.inject:
        print(f"\n[TODO] ESP injection into {args.inject} — use esp_binary_writer.py")

    return subrecords


if __name__ == '__main__':
    main()
