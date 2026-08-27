"""Build a static call graph from 32-bit x86 PE code.

Usage:
    python build_callgraph.py [path] [--dot out.dot] [--json] [--fn 0xADDRESS]

Linear capstone sweep of executable sections: records direct `call rel32`
edges, resolves indirect `call [IAT entry]` to imported DLL!Function names,
and (best-effort) locates function starts via common prologues. Output feeds
the research/re/ knowledge base and downstream "walk callers/callees" queries.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pe_utils import emit, exec_sections, load_pe, parse_int, resolve_target, warn_if_encrypted

PROLOGUES = (b"\x55\x8B\xEC", b"\x55\x89\xE5", b"\x8B\xFF\x55\x8B\xEC")


def build(path: Path) -> dict:
    try:
        import capstone
    except ImportError:
        raise SystemExit("error: capstone not installed — pip install capstone")

    pe = load_pe(path)
    warn_if_encrypted(pe, path)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = path.read_bytes()

    iat = {}
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll = entry.dll.decode(errors="replace")
            for imp in entry.imports:
                if imp.address:
                    name = imp.name.decode(errors="replace") if imp.name else f"ord#{imp.ordinal}"
                    iat[imp.address] = f"{dll}!{name}"

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True

    def disasm_resilient(blob: bytes, va: int):
        """Linear sweep that resumes after undecodable bytes instead of stopping."""
        pos = 0
        while pos < len(blob):
            last = pos
            for insn in md.disasm(blob[pos:], va + pos):
                last = insn.address - va + insn.size
                yield insn
            if last == pos:  # zero progress: skip one bad byte
                pos += 1
            else:
                pos = last

    edges = []          # {caller, callee, kind, callee_name?}
    func_starts = set()

    for sec in exec_sections(pe):
        start = sec.PointerToRawData
        blob = data[start:start + sec.SizeOfRawData]
        sec_name = sec.Name.rstrip(b"\x00").decode(errors="replace")

        for pl in PROLOGUES:
            i = blob.find(pl)
            while i != -1:
                func_starts.add(base + sec.VirtualAddress + i)
                i = blob.find(pl, i + 1)

        for insn in disasm_resilient(blob, base + sec.VirtualAddress):
            if insn.mnemonic in ("call", "jmp"):
                op = insn.op_str
                if op.startswith("0x"):
                    try:
                        dst = int(op, 16)
                    except ValueError:
                        continue
                    if insn.mnemonic == "call":
                        edges.append({
                            "caller": f"0x{insn.address:08X}",
                            "callee": f"0x{dst:08X}",
                            "kind": "direct",
                        })
                elif op.startswith("dword ptr [0x"):
                    try:
                        slot = int(op[len("dword ptr ["):-1], 16)
                    except ValueError:
                        continue
                    if slot in iat and insn.mnemonic == "call":
                        edges.append({
                            "caller": f"0x{insn.address:08X}",
                            "callee": f"0x{slot:08X}",
                            "kind": "import",
                            "name": iat[slot],
                        })
        del sec_name

    callees: dict[str, set] = {}
    callers: dict[str, set] = {}
    for e in edges:
        callees.setdefault(e["caller"], set()).add(e["callee"])
        callers.setdefault(e["callee"], set()).add(e["caller"])

    graph = {
        "file": str(path),
        "function_count": len(func_starts),
        "edge_count": len(edges),
        "edges": [{**e} for e in edges],
        "callees": {k: sorted(v) for k, v in sorted(callees.items())},
        "callers": {k: sorted(v) for k, v in sorted(callers.items())},
    }
    graph["_func_starts"] = sorted(f"0x{a:08X}" for a in func_starts)
    return graph


def render_dot(graph: dict, focus: str | None) -> str:
    lines = ["digraph calls {", '  node [shape=box, fontname="Consolas"];']
    wanted = {focus} if focus else None
    if wanted:
        wanted |= set(graph["callers"].get(focus, []))
        wanted |= set(graph["callees"].get(focus, []))
    for e in graph["edges"]:
        if wanted and e["caller"] not in wanted and e["callee"] not in wanted:
            continue
        label = f' [label="{e["name"]}"]' if e.get("kind") == "import" else ""
        lines.append(f'  "{e["caller"]}" -> "{e["callee"]}"{label};')
    lines.append("}")
    return "\n".join(lines) + "\n"


def human(graph: dict) -> None:
    print(f"{graph['file']}: {graph['function_count']} candidate functions, {graph['edge_count']} call edges")
    print("top callers by out-degree:")
    ranked = sorted(graph["callees"].items(), key=lambda kv: -len(kv[1]))[:15]
    for va, outs in ranked:
        print(f"  {va} -> {len(outs)} callees")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", help="PE file (absolute, or relative to FNV game dir)")
    ap.add_argument("--dot", metavar="FILE", help="also write Graphviz .dot output")
    ap.add_argument("--fn", help="focus DOT output on one function VA, e.g. 0x00842F10")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = resolve_target(args.path)
    if not target.exists():
        raise SystemExit(f"error: not found: {target}")
    graph = build(target)
    if args.dot:
        Path(args.dot).write_text(render_dot(graph, args.fn), encoding="utf-8")
        print(f"# wrote {args.dot}", file=sys.stderr)
    emit(graph, args.json, human)


if __name__ == "__main__":
    main()
