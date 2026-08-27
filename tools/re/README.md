# Binary Reverse-Engineering Toolchain (RE Layer)

CLI-first binary archaeology for FalloutNV.exe, NVSE plugin DLLs, and any other
PE32/PE32+ binaries in the modding stack. This is the layer *underneath* the
xEdit/record pipeline: instead of reading community docs, we ask the executable
how the game works.

FNV targets are **32-bit Windows PE/COFF**, not ELF. `readelf` is the wrong
tool here — everything below is PE-aware.

## Layout

| Directory | Tool | Purpose |
|-----------|------|---------|
| `ghidra/` | Ghidra headless | The heavy lifter: import, auto-analyze, decompile, export symbols/call graphs (see `postscripts/`) |
| `rizin/` | rizin / radare2 | Quick scripted reversing, interactive inspection, ZIGNATURES |
| `llvm/` | llvm-objdump, llvm-readobj | PE section tables, imports, disassembly (drop-in binaries, no MSVC needed) |
| `capa/` | capa | Capability detection: "does this DLL touch files, registry, network, process?" |
| `floss/` | FLOSS | Stack-string / obfuscated-string recovery where `strings` misses |

## Installation (Windows, CLI-pure)

```powershell
# Ghidra (needs Java 17+; then set GHIDRA_INSTALL_DIR)
scoop install ghidra          # or download from https://ghidra-sre.org

# rizin + rz-ghidra plugin (optional decompiler)
scoop install rizin

# LLVM binutils: llvm-objdump, llvm-readobj
scoop install llvm

# capa + FLOSS (Mandiant, pip-installable)
pip install flare-capa
pip install flare-floss

# Python PE parsing used by scripts/re/
pip install pefile capstone
```

Everything is also drivable through `scripts/re/` wrappers, which produce JSON
artifacts sized for LLM consumption (see `docs/re-pipeline.md`).

## What lives where

```
tools/re/            <- tool config, Ghidra postscripts, signatures
scripts/re/          <- CLI entry points (inspect, strings, xrefs, callgraph, ...)
research/re/         <- recovered knowledge base (symbols, structures, hypotheses)
mcp/reverse-engineering/ <- MCP tool-surface design for the agent loop
```

## Ground rules

1. **Static first, dynamic second.** Ghidra/capstone answer "what does this
   look like"; x64dbg/WinDbg (manual, outside this repo tree) answer "what does
   it actually do at runtime". A hypothesis is only *confirmed* after runtime
   verification.
2. **Canonical build discipline.** Symbols are recovered against the GOG
   build's RVAs (plaintext code) and mapped to other builds via
   `match_functions.py`. The Steam exe is a runtime-validation target only —
   its `.text` is CEG-encrypted at rest; never fight the wrapper.
3. **Every recovered symbol gets evidence.** Nothing enters
   `research/re/symbols.json` without evidence classes and a policy-tiered
   confidence (`research/re/confidence-policy.md`).
4. **Never patch the running game from these scripts.** Read-only analysis;
   mods ship as ESP/ESM + NVSE plugins, not binary edits.
