# Binary RE Pipeline

The layer underneath the modding pipeline: asking the executable how New Vegas
works, then persisting the answer next to the record-layer knowledge.

The end state is not "RE tooling" — it is a **machine-readable executable
specification of New Vegas**: three independent representations cross-checked
against each other.

```text
ESM/ESP world representation        (mnehmos.fnvedit.mcp: what the records say)
NVSE community-engineering layer    (what experienced modders believed internals meant)
FalloutNV native implementation     (what the executable actually does)
```

Every recovered claim sits on an epistemic ladder:

```text
community says X  →  plugin format suggests X  →  static binary evidence
suggests X  →  runtime behavior confirms X
```

Confidence is governed mechanically by `research/re/confidence-policy.md`;
LLM judgment alone never exceeds 0.60.

## Canonical build policy

| Role | Build | Notes |
|------|-------|-------|
| **Canonical static-analysis target** | GOG 1.4.0.525 (`fnv-gog-1.4.0.525`) | plaintext `.text`; pending acquisition (see H1 prerequisites) |
| Runtime-validation target | Steam install (`fnv-steam-1.4.0.525`) | CEG-wrapped code; data layer usable |
| Semantic annotation layer | `nvse-1.4-runtime` + PDB | mined via `scripts/re/mine_pdb.py` |

Rule: recover symbols against the canonical build's RVAs; map to other builds
only through `scripts/re/match_functions.py` equivalences. Never fight the
Steam wrapper — this stays a game-understanding project, not a DRM project.

## Evidence sources (the epistemic engine)

```text
NVSE PDB (nvse_semantic_reference)     scripts/re/mine_pdb.py
fnv-source-atlas (Xbox PDB atlas)      research/re/external-sources.md — query-only
GOG executable (static ground truth)   Ghidra + capstone + RTTI
Steam install (runtime validation)     x64dbg / NVSE logging
plugin records (fnvedit.mcp)           what the records say
community docs                         corroboration only
        ↓
research/re/symbols.json   (mechanical confidence policy)
```

Field context: `fnv-source-atlas` answers "which PC function corresponds to
this Xbox-debug-symbol function"; `New-New-Vegas` applies Ghidra+MCP to an
unpacked exe; BinDiff/BSim established cross-build matching; REFORGE argues
for exactly the provenance/ambiguity discipline our policy encodes. What
remains distinctive here: an agent driving from a *gameplay question* to a
*runtime-verified explanation*, with the confidence gate refusing static
claims above 0.60.

## Position in the stack

```
FalloutNV.exe / NVSE DLL / plugin DLL
        ↓
binary identification        scripts/re/inspect_pe.py
        ↓
PE structure + imports + strings    scripts/re/inspect_pe.py, extract_strings.py
        ↓
disassembly / headless decompilation   scripts/re/import_ghidra.py (Ghidra)
        ↓
function/symbol/signature database    scripts/re/build_callgraph.py,
                                      fingerprint_functions.py,
                                      research/re/
        ↓
semantic annotations            research/re/symbols.json + hypotheses/
        ↓
LLM tool interface              mcp/reverse-engineering/ (design)
        ↓
hypothesis-driven questions     "where is actor spawn logic?"
        ↓
static evidence + runtime verification   x64dbg / NVSE logging (human-driven)
        ↓
reusable RE knowledge base      research/re/
```

## Why PE, not ELF tooling

FalloutNV.exe and every NVSE plugin are 32-bit Windows PE/COFF images.
`readelf`/`objdump` ELF defaults are the wrong foundation; the standard tools
here are `llvm-readobj`, `llvm-objdump`, Ghidra, and `pefile`/`capstone` from
Python (all wired up in `tools/re/`).

## Critical environment fact: the Steam exe is CEG-wrapped

Measured on the installed copy (see `research/re/hypotheses/H1-encounter-spawn-resolution.md`):

- `.text` (12.4 MB) has entropy ~8.0 and decodes as garbage at every sampled
  offset — code is **encrypted at rest**
- the entry point lands in a nonstandard executable section `.bind`
  (entropy 7.995) holding the decryptor stub; `FalloutNV_backup.exe` is
  wrapped the same way
- `.rdata`/`.data`/imports stay plaintext — strings, the record-type
  descriptor table, and game-setting names are all readable and already
  yielded anchors

Therefore:

| Target | Static code analysis |
|--------|---------------------|
| Steam FalloutNV.exe (on-disk) | data layer only (strings/4CC/imports) |
| GoG / CEG-free 1.4.0.525 exe | full analysis — preferred for `FalloutNV.exe` work |
| Running process (post-unpack dump via x64dbg + pe-sieve/Scylla) | full analysis, per-machine ASLR fixed to image base |
| NVSE DLLs (nvse_1_4.dll, JIP, etc.) | full analysis today — plaintext, and `nvse_1_4.pdb` ships alongside |

The scripts detect this automatically: exec-section entropy > 7.5 triggers a
warning instead of silently returning garbage results.

## The scripts

| Script | What it answers |
|--------|-----------------|
| `inspect_pe.py` | What is this binary? Sections, imports, exports, sha256/md5, build identity |
| `extract_strings.py` | ASCII + UTF-16 strings with VAs (feed xrefs) |
| `find_xrefs.py` | Who references this VA / this string? |
| `build_callgraph.py` | Callers/callees; DOT export for focused subgraphs |
| `fingerprint_functions.py` | Single signatures, or `--all` multi-fingerprint DB (n-grams, refs, degrees) |
| `match_functions.py` | Cross-build function equivalence (triangulated, no single signal trusted) |
| `mine_pdb.py` | NVSE PDB → engine-VA references with named NVSE context (`research/re/nvse_xrefs.json`) |
| `import_ghidra.py` | Headless Ghidra: analyze + dump functions/calls/strings |
| `correlate_records.py` | Which Bethesda record 4CCs live where in the binary; optionally cross-referenced against a plugin's records via the FNVEdit parser |

All support `--json` for LLM consumption. Set `FNV_GAME_DIR` to override the
default Steam path.

## Worked example: finding exterior spawn logic

Goal of seed hypothesis `research/re/hypotheses/H1-encounter-spawn-resolution.md`:

```powershell
# anchors: where does the exe touch encounter-zone records?
python scripts/re/correlate_records.py FalloutNV.exe

# terminology sweep
python scripts/re/extract_strings.py FalloutNV.exe --min 6 --utf16 > research/re/strings_all.txt
Select-String -Path research/re/strings_all.txt -Pattern "encounter|spawn"

# walk references to a promising string VA (requires a CEG-free image
# for the exe — on the Steam exe the code layer is encrypted, see above)
python scripts/re/find_xrefs.py FalloutNV.exe --string "EncounterZone"

# authoritative analysis + decompilation inputs
python scripts/re/import_ghidra.py FalloutNV.exe

# subgraph around a candidate
python scripts/re/build_callgraph.py FalloutNV.exe --dot research/re/callgraph.dot --fn 0x00842F10
```

Result format for a recovered function (goes to `symbols.json`):

```text
0x00842F10
candidate: EncounterZone::ResolveSpawn
confidence: 0.81

Evidence:
- reads ECZN-associated structure
- called from exterior-cell loading path
- accesses actor base-form collection
- branches on player level
- writes spawned reference list
```

## Verification policy

Static convergence is *not* confirmation. A symbol reaches 0.9+ confidence
only after runtime verification (x64dbg breakpoint + observed behavior, or an
NVSE-side probe). Until then every entry carries its evidence so a later pass
can re-derive or refute it.
