# `mnehmos.re.mcp` — Reverse-Engineering MCP Server

**Status: implemented** (`server.py`, this directory). Registered in
`.mcp.json` as `mnehmos-re` (stdio). The historical design notes remain
below the tool table.

Run standalone: `python mcp/reverse-engineering/server.py`

## Implemented tool surface (17 tools, wire-tested)

| Tool | Purpose |
|------|---------|
| `re_inspect` | PE structure: sections, imports, exports, entropy, md5 |
| `re_build_identity` | Canonical build identity (sha256/timestamp/image base) for KB registration |
| `re_strings` | ASCII+UTF-16 strings with VAs, regex filter |
| `re_xrefs` | Refs to a VA or an exact string's VA |
| `re_callgraph` | Resilient capstone sweep; `focus_va` neighborhood mode |
| `re_fingerprint` | Masked signature + mnemonic hash for one function |
| `re_match_builds` | Cross-build equivalence between fnprints databases |
| `re_nvse_xrefs` | Query mined NVSE→engine references by engine VA or NVSE symbol |
| `re_mine_pdb` | Recompute nvse_xrefs.json (slow) |
| `re_search_records` | Record-type 4CC anchor scan |
| `re_form_type` | Engine form-type registry (ordinal ↔ 4CC) |
| `re_lookup_symbol` | Query the symbol KB by name (+build filter) |
| `re_save_symbol` | **Policy-gated KB write** (see below) |
| `re_hypotheses` | List hypothesis files + status lines |
| `re_decompiled` | Read/list cached Ghidra decompilations |
| `re_atlas_pc` | fnv-source-atlas PC address probe (query-only, per external-sources.md) |
| `re_atlas_class` | fnv-source-atlas class/vtable/slots query |

## Policy enforcement in the server (verified)

`re_save_symbol` mechanically enforces `research/re/confidence-policy.md`:

- unknown `build_id` → rejected
- `va` is always **derived** from the build's image base + supplied `rva`
- `confidence > 0.60` without `dynamic_trace` / `experimental_manipulation`
  / `authoritative_source` → **rejected**
- `confidence > 0.80` without runtime classes → rejected
- `> 0.95` rejected outright; downgrades recorded with `previous_confidence`

Wire test (2026-08-27): initialize → 17 tools → `re_form_type("98")` →
ECZN → `re_lookup_symbol("BGSEncounterZone::Load")` → 0.60. Passed.

## Historical design notes

Sibling server to `mnehmos.fnvedit.mcp` (separate repo, same pattern:
`F:/Github/mnehmos.re.mcp`). This file is the committed tool-surface contract
so the LLM agent loop has a stable interface while implementation evolves.

## Design principles

1. **Read-only over game binaries.** No patching, no injection. Runtime work
   goes through debuggers explicitly driven by the human.
2. **Everything returns evidence.** Each tool response carries VAs, binary
   md5, and the method used — never bare claims.
3. **KB-backed.** Lookups read/write `research/re/` (symbols, hypotheses,
   signatures) so recovered knowledge persists across sessions.
4. **JSON-first.** Output shaped for token-efficient LLM consumption.

## Tool surface

| Tool | Purpose |
|------|---------|
| `re_inspect` | PE header/sections/imports/exports + build identity (sha256, timestamp) for a target binary |
| `re_strings` | ASCII+UTF-16 string search with VAs, regex supported |
| `re_xrefs` | References to a VA or to a string's VA (pattern + Ghidra-backed modes) |
| `re_decompile` | Ghidra headless pseudocode for one function (cached) |
| `re_disasm` | Capstone window at a VA |
| `re_callgraph` | Callers/callees around a function from the Ghidra export |
| `re_search_records` | 4CC/GECK-term anchors in the binary, correlated with plugin records |
| `re_nvse_xrefs` | Query the mined NVSE→engine reference map (`research/re/nvse_xrefs.json`): given an engine VA, return named NVSE context; given an NVSE symbol, return engine VAs it touches |
| `re_lookup_symbol` | Query `research/re/symbols.json` by (build_id, rva) or name |
| `re_save_symbol` | Add/revise a symbol — **requires** build_id, rva (never a naked VA), provenance classes, and a policy-tiered confidence; the server computes VA from the build's image base and rejects confidence tiers whose evidence classes are absent |
| `re_hypothesis` | Create/update hypothesis files; list open ones |
| `re_fingerprint_db` | Run/refresh `fingerprint_functions.py --all` for a build |
| `re_match_builds` | Cross-build equivalence: GOG RVA ↔ Steam runtime ↔ NVSE-known address triangulation |
| `re_capability` | capa results for a DLL (useful for auditing NVSE plugins) |

## Policy enforcement in the tool layer

The server is the enforcement point for `research/re/confidence-policy.md`:

- LLM-supplied confidence > 0.60 without a `dynamic_trace` or
  `experimental_manipulation` evidence class is **rejected**, not warned.
- Symbols are stored RVA-first per build; VAs are derived, never typed in.
- `equivalences` between builds may only cite a `re_match_builds` result, not
  an LLM's assertion that two functions "look the same."

## Agent loop (what the server exists to serve)

```
observe binary (re_inspect, re_strings)
→ find candidate anchors (re_search_records, re_strings)
→ trace references (re_xrefs)
→ inspect callers/callees (re_callgraph, re_decompile)
→ propose function meaning (LLM)
→ gather corroborating evidence (re_disasm, community docs)
→ persist (re_save_symbol, re_hypothesis)
→ [human-assisted] runtime verification via x64dbg
→ confidence upgrade, signature saved (re_save_symbol + signatures/)
```

## Relationship to existing stack

```
mnehmos.re.mcp      binary semantics  (this design)
mnehmos.fnvedit.mcp record layer      (ESM/ESP read + ESP write)
blender/gimp/audacity-mcp             assets
                                      ↓
                      mod generation + runtime NVSE scripting
```

The bridge tool of interest is `re_search_records`: a recovered function that
reads ECZN can immediately be cross-referenced against the ECZN records the
FNVEdit server already knows how to edit — closing the loop between "how the
engine consumes records" and "which records we generate."
