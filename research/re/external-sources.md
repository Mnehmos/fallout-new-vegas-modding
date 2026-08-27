# External Evidence Sources — Consumption Rules

## fnv-source-atlas (amarkham23)

Evidence-backed map between the FNV PC executable and the Xbox 360 debug
build (PDB-derived names, CodeView types/layouts, vtables, SDK prototypes,
candidate PC↔Xbox links, human review layer).

| | |
|--|--|
| Version in use | v0.5.0, SQLite schema 8 |
| Database sha256 | `2d4713502310a4ba00872ceb260e5f04c1b41e19291e381540183e27c4af07a9` |
| Local copy | `C:\Tools\fnv-source-atlas\` (CLI, MIT) + `C:\Tools\fnv-source-atlas-data-0.5.0\` (release DB) |
| License | MIT covers project code/docs **only**; database redistribution rights explicitly unresolved |

### Consumption rules (binding)

1. **Query locally, never fork the data.** The atlas database is queried
   read-only in place. Bulk derived records (types, layouts, procedure
   bodies, mappings) are **never copied into this repository**. Only small,
   cited conclusions enter `symbols.json` — same as any other evidence
   source.
2. **Provenance classes.** Atlas-derived evidence is recorded as:
   - `source_atlas_candidate` — a candidate/hypothesis PC↔Xbox link. Cap
     **0.40**, and only when our own static evidence concurs.
   - `source_atlas_accepted` — passed the atlas's human review layer
     (accepted-only export, hash-gated to the PC executable identity).
     Cap **0.60**: the strongest static corroboration class we recognize,
     but still static — runtime tiers stay gated as always.
3. **Identity gate.** Atlas queries are only meaningful against the PC
   executable identity it was built for. Before consuming, verify the atlas
   recognizes our canonical build (`fnv-gog-1.4.0.525`,
   sha256 `89e70204...`); if the atlas targets a different PC build, its
   addresses are evidence for `match_functions.py`, not direct anchors.
4. **Independence is directional.** The atlas derives from Xbox PDB + PC
   inventory — it is independent of NVSE's plugin ecosystem but NOT
   independent of other Xbox-PDB-derived community sources. Two agreeing
   claims with a common Xbox-PDB ancestor count as **one** evidence class
   for tier purposes.
5. **No name laundering.** An atlas name attached to an address does not
   let an LLM assert more than the atlas does. Ambiguity in the atlas
   (alternatives, fold bundles) is copied verbatim into our evidence text.

## NVSE PDBs (`nvse_1_4.pdb` etc.)

Local artifacts of the installed NVSE build. Mined via
`scripts/re/mine_pdb.py` → `nvse_xrefs.json`. Provenance:
`nvse_pdb`, `nvse_semantic_reference` (policy caps apply).

## Community documentation (GECK wiki, xEdit internals, forums)

`community_source_symbol` — corroboration only, cap 0.60, always tagged
`source: community-docs`.
