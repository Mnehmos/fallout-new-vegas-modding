# Confidence Policy for Recovered Symbols

Mechanical rules for assigning confidence to entries in `research/re/symbols.json`.
Confidence is **evidence-class-driven, never vibe-driven**: a tier may only be
claimed when the listed evidence classes are mechanically present in the
symbol entry. An LLM's judgment that decompiled code "looks obvious" never
exceeds the static cap.

## Tiers

| Tier | Name | Requires (mechanically) |
|------|------|--------------------------|
| 0.20 | structural guess | a single structural signal (e.g. adjacent to a known anchor, plausible call-graph position) |
| 0.40 | static semantic evidence | one measured evidence class: `string_xref`, `record_descriptor_xref`, or `nvse_semantic_reference` with disassembly context |
| 0.60 | multi-source static | ≥2 independent static evidence classes agreeing (e.g. NVSE reference + string xref), or decompilation consistent with all recorded evidence |
| 0.80 | static + runtime correlation | a runtime trace (breakpoint hit with expected arguments/flow) matching the static claim |
| 0.95 | experimentally verified | behavior **changed** by controlled manipulation (INI/record/state change) and reproduced ≥2× as predicted |
| 1.00 | authoritative source | reserved for the engine's own symbols (PDB/source) — effectively unreachable for FNV; treated as ceiling notation |

## Hard caps by provenance

- LLM-only judgment (no runtime evidence): **≤ 0.60**. No exceptions for
  "obvious" decompilation.
- `community_source_symbol` / `nvse_semantic_reference` alone: ≤ 0.60 —
  community knowledge and NVSE's naming are strong hints, not measurements.
- `source_atlas_accepted` alone: ≤ 0.60 (see `external-sources.md`; also
  note common-ancestor rule — Xbox-PDB-derived claims are not independent
  of each other).
- Anything ≥ 0.80 must cite a concrete runtime artifact (log line, trace
  file, manipulation recipe + observed deltas) in its `evidence` list.

## Provenance vocabulary

| Class | Meaning |
|-------|---------|
| `structural_guess` | position/plausibility argument only |
| `string_xref` | code references a string recovered from the binary |
| `record_descriptor_xref` | code references a 4CC/descriptor-table entry |
| `nvse_pdb` | name/evidence comes from an NVSE PDB symbol |
| `nvse_hardcoded_reference` | NVSE code/data contains the engine address |
| `nvse_semantic_reference` | NVSE function semantics (its own name/logic) implies the engine address's role |
| `community_source_symbol` | from community docs/source (xEdit, NVSE source, GECK wiki); always tagged `source: community-docs` |
| `source_atlas_candidate` | candidate/hypothesis link from fnv-source-atlas (see `external-sources.md`); cap 0.40, only with our own concurrence |
| `source_atlas_accepted` | passed the atlas's human-review layer, hash-gated to PC build identity; strongest static class, cap 0.60 |
| `dynamic_trace` | observed under debugger/trace at runtime |
| `experimental_manipulation` | predicted-and-verified behavior change |
| `authoritative_source` | engine PDB/source (does not exist for FNV) |

## Build identity

Every symbol is stored per-build (`build_id`), **RVA-first**. A VA is always
derived from the build's recorded image base, never written by hand.
Cross-build equivalence lives in `equivalences` (see
`scripts/re/match_functions.py`), never by reusing one build's address in
another build's entry.
