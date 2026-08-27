# H1-GP: Encounter-zone gameplay consumption

**Status:** open
**Runtime:** not ready; no gameplay consumer has been established
**Parent:** H1 split from `H1-encounter-spawn-resolution.md`
**Question:** where does gameplay turn a CELL/reference context into an
effective encounter zone, read zone properties, select leveled actors/lists,
and decide whether to spawn?

## Explicit boundary from H1-SL

No static evidence from the recovered save/load chain reaches encounter
selection or spawning. H1-SL ends at persistence/rebinding:

```text
serialized zone ID -> ExtraDataList::LoadGame -> ExtraEncounterZone +0x0C
                   -> rebind/remove-on-failure
```

A successful H1-SL runtime test must not be reported as gameplay validation.

## Search direction

Attack the problem from both ends and look for an intersection:

```text
BGSEncounterZone readers  ---------+
                                   +--> shared consumer/context
spawn and leveled-list callers ----+
```

### ECZN-side frontier

Search non-save/load functions for:

- reads of `BGSEncounterZone` state, especially `+0x18` DATA and its flag
  dwords;
- uses of `ExtraEncounterZone` descriptor `0x01184CF4` and its `+0x0C` result,
  excluding the H1-SL load/rebind path and the `0x00432E90` comparator;
- `TESObjectCELL` descriptor `0x01183FB4`, `TESObjectREFR` descriptor
  `0x011841CC`, and `TESWorldSpace` descriptor `0x01183FD0` near those reads;
- branches or calls that consume actor-count, level, encounter, or region
  state. Keep every semantic name at the confidence-policy tier supported by
  independent evidence.

Known ECZN-related functions are starting points, not the gameplay answer:

| Address | Current interpretation | Exclude/include |
|---|---|---|
| `0x00525D40` | `BGSEncounterZone::Load` candidate | exclude as record parsing |
| `0x00525E70` | `BGSEncounterZone::Save` candidate | exclude as save parsing |
| `0x00525F00` | ECZN owner-form `InitItem` candidate | inspect, but not yet gameplay |
| `0x005845E0` | worldspace owner-form `InitItem` candidate | inspect its downstream helper |
| `0x00432E90` | `ExtraEncounterZone::Compare` candidate | exclude as comparator |
| `0x00428150` | `ExtraDataList::LoadGame` | remove from gameplay frontier |

### Spawn-side frontier

Identify functions/classes associated with:

- `LVLC`/`LVLN` record traversal and leveled-actor eligibility;
- actor level selection, player-level or process-level decisions;
- encounter scheduling, cell attach/restore, or exterior spawn generation;
- references to `TESObjectCELL`, region/worldspace, encounter-zone state, or
  the effective zone pointer.

Work backward from those consumers, using `re_decompiled`, `re_xrefs`,
`re_atlas_pc`, `re_nvse_xrefs`, and callgraph evidence. Use atlas labels only
as candidates. The encrypted Steam `.text` means the plaintext GOG artifact
or a verified function match is required for negative xref conclusions.

## Initial consumer-side reconnaissance (2026-08-27)

The first pass narrowed the search frontier but did not recover a shared
consumer:

- `mnehmos.re` form-type lookup identified `ECZN` as type `98`, `LVLC` as
  `45`, `LVLN` as `46`, `CELL` as `58`, `ACHR` as `60`, `WRLD` as `66`,
  `NPC_` as `43`, and `CREA` as `44`. These are useful search anchors, not
  gameplay semantics.
- `mnehmos.re` string search on the intact Steam string layer found change
  records for encounter-zone game data and flags (`0x0107DF44`,
  `0x0107DF70`), leveled actors (`0x0107E51C`), and leveled-reference
  inventory (`0x0107E7FC`), plus encounter-zone lookup failures
  (`0x01014788`, `0x01031D10`, `0x01031D54`), a leveled-actor label
  (`0x0107E538`), and cell respawn timing (`0x0102F4BC`). The local string
  corpus independently contains the same frontiers, including
  `CHANGE_REFR_EXTRA_ENCOUNTER_ZONE`.
- `re_decompiled`, `re_xrefs`, `re_atlas_pc`, `re_nvse_xrefs`, and the current
  callgraph artifacts did not yet produce a verified ECZN-reader/leveled-
  selection intersection. Steam xrefs remain unusable for a negative result
  because its encrypted/CEG-wrapped `.text` is not the plaintext analysis
  artifact. The atlas class sweep was stopped after it remained in the
  external atlas process; it yielded no result to promote.

No KB symbol was updated from names, form types, or strings alone. The
negative result is local to the recovered artifacts: it does not establish
that encounter-zone gameplay consumers do not exist elsewhere in the engine.

## First deliverable

Produce one measured intersection of the two frontiers:

```text
CELL/reference context
  -> effective encounter-zone lookup
  -> zone DATA/flags read
  -> leveled actor/list selection
  -> spawn decision
```

If the intersection does not exist in the recovered artifacts, record the
coverage gap and keep the path open. Do not promote a function merely because
its name contains `encounter`, `zone`, `level`, or `spawn`.

## Runtime boundary

H1-GP has no runtime prediction yet. After a gameplay consumer is statically
identified, design the smallest paired manipulation that changes one ECZN
property or effective-zone input while holding cell, actor, player level, and
load order constant. The expected before/after spawn or selection delta must
be derived from that consumer's branch, not from H1-SL.
