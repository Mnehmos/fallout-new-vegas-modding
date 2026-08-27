# H1: Exterior encounter-zone resolution — first end-to-end scientific test

**Status:** split into H1-SL and H1-GP; this file is the historical evidence ledger
**Canonical static target:** `fnv-gog-1.4.0.525` (plaintext analysis artifact)
**Runtime validation target:** Steam install (`fnv-steam-1.4.0.525`)
**Motivation:** PopulationDensity needs the true engine path that decides when
an exterior encounter zone instantiates its leveled lists. See
`research/population/encounter-zones.md`.

> Correction record: Update 8 below supersedes the earlier interpretation of
> `0x00428150` as a gameplay zone resolver and of `0x00432E90` as a zone
> get/attach visitor. Those roles are retracted; the earlier measurements are
> retained as provenance and contradiction history.

Canonical investigations:

- [`H1-SL: Encounter-zone save/load lifecycle`](H1-SL-encounter-zone-save-load-lifecycle.md)
  - static chain recovered; runtime verification pending.
- [`H1-GP: Encounter-zone gameplay consumption`](H1-GP-encounter-zone-gameplay-consumption.md)
  - open; no gameplay consumer has been established.

## Success criterion

> Starting only from `ECZN` and known plugin semantics, recover and
> experimentally validate **at least one engine function** involved in
> resolving an actor's encounter zone.

Not the whole spawning system. One function, from anchor to manipulation.

## Bottom-up ontology chain (the method)

Do NOT start from "find spawn enemies." Reconstruct the ontology from the
bottom upward — each link is a separate, falsifiable step:

```text
4CC "ECZN"
  → record descriptor entry        (anchor already measured: 0x0101C364, Steam data layer)
  → record constructor/factory     (code xrefs to the descriptor — requires CEG-free .text)
  → record loader                  (parse path: TES4 dispatch → ECZN-specific parser)
  → in-memory class                (struct layout reconstruction → research/re/structures/)
  → field accessors                (level range, flags, CELL linkage)
  → CELL/reference processing      (consumers of TESObjectCELL ↔ ECZN relationship)
  → encounter-zone lookup          (given a reference, which ECZN governs it?)
  → actor/level-list evaluation
  → spawn behavior                 (H1's original question, now with provenance)
```

## Sub-hypotheses

### H1.1 — ECZN record constructor/parser
Find the function(s) that construct the in-memory ECZN object from plugin
data. Evidence chain: descriptor 0x0101C364 → xrefs → factory → parser.
Evidence classes: `record_descriptor_xref` (+ decompilation consistency).

### H1.2 — ECZN-from-CELL/reference lookup
Find code retrieving the governing ECZN given a CELL or reference context.
Expected shape: iterates an extra-data list or world/cell structure, compares
zone formIDs, returns EncounterZone*.

### H1.3 — caller in actor initialization / encounter processing
Identify one H1.2 caller in actor-init or encounter processing. This is the
candidate function for the success criterion.

### H1.4 — behavioral prediction
From the candidate's decompilation, write a concrete, falsifiable prediction
(e.g. "an actor at the boundary of ECZN X with `iNumberActors*` set to N
will/won't spawn because branch at RVA Y takes player level < Z").

### H1.5 — runtime verification
Test the prediction on the Steam install: x64dbg breakpoint / NVSE log /
controlled game-state manipulation. Record the artifact (log line, trace,
manipulation recipe + observed deltas).

### H1.6 — promotion
Promote the verified symbol into `symbols.json` with provenance
`dynamic_trace` / `experimental_manipulation` (tier 0.80/0.95 per
`confidence-policy.md`) and save a version-proof signature to
`signatures/` (GOG RVA ↔ Steam runtime equivalence via `match_functions.py`).

## Prerequisites

1. ~~**Canonical static image.**~~ **DONE 2026-08-27** — GOG build acquired
   and registered as `fnv-gog-1.4.0.525`: sha256 `89e70204...dd0fe`,
   `.text` entropy 6.561 (plaintext), no `.bind` section, entry inside
   `.text`. Data sections byte-identical to Steam — all prior anchors carry
   over at identical VAs.
2. ~~**Ghidra import** of the GOG exe.~~ **DONE 2026-08-27** — the
   plaintext GOG decompilation and call export are present under
   `research/re/decompiled/`, `research/re/functions.json`, and
   `research/re/calls.json`. Live xrefs/callgraph
   against the encrypted Steam image remain a coverage limitation, not a
   negative result.

## Findings (updated 2026-08-27 — first three links of the chain closed)

**The form-type registry** — the structural heart of record handling:

```text
4CC "ECZN"
  → descriptor entry        0x0101C364 (identical VAs on both builds)
  → form-type registry      0x01187004, stride 12, {descriptor_ptr, 0, ordinal}, 121 entries
                            ECZN = ordinal 98, slot 0x01187490
  → 4CC→ordinal lookup      0x00483370 (loop i < 0x79, byte-packs descriptor 4CC)
  → ordinal accessor        0x0043A590 (singleton-getter → registry index; pushes 0x01183028)
```

Full 120-ordinal → 4CC map decoded and saved:
`research/re/form_type_registry.json` (2:TES4 … 43:NPC_ … 58:CELL …
98:ECZN … 120:HUNG) — a first genuine piece of the machine-readable
executable specification.

**How each link was measured:**

| Anchor | What | Class |
|--------|------|-------|
| 0x0101C2AC–0x0101C664 | record-type descriptor block in `.rdata` (ECZN at 0x0101C364); 87 `.text` refs to other entries; 127 `.data` pointer refs | `record_descriptor_xref` |
| 0x01187004–0x01187598 | form-type registry, stride 12, ordinals 0..120; decoded via registry walk + RTTI class names adjacent in `.data` | `structural-analysis` |
| 0x00483370 | 4CC→ordinal lookup: `i < 0x79` loop over registry, byte-packs descriptor[0..3] | `structural-analysis` (consistent with registry) |
| 0x0043A590 | ordinal accessor: singleton-getter (`call 0x7AF430` → `call 0x401170`), `imul 0xC` registry index, pushes 0x01183028 + 0x011841CC | `structural-analysis` |
| 0x01014788 | "Unable to find encounter zone %08X..." — ECZN resolve/load path | `string_xref` |
| 0x01050048 / 0x01050064 / 0x01050A30 | `iNumberActorsInCombatPlayer` / `iNumberActorsAllowedToFollowPlayer` / `iAINumberActorsComplexScene` game-setting names | `string_xref` |

**Cross-layer triangulation confirmed:** DataHandler-region candidate
`0x01183028` is referenced independently by (a) NVSE's faction-command
family (PDB-derived, from `nvse_xrefs.json`) and (b) GOG function
0x0043A590's disassembly. Two independent static sources agree →
0.40 → 0.60 per confidence policy. This is the architecture working as
designed: community-engineering layer and native implementation
cross-validating each other.

**Still true (Steam build):** CEG-wrapped `.text` (entropy 8.0, `.bind`
stub) — Steam stays the runtime-validation target for H1.5.

## Findings (update 2, 2026-08-27 — class ontology + atlas triangulation)

**RTTI class ontology recovered** (1,852 decorated class names in the image);
the zone subsystem: `BGSEncounterZone`, `ExtraEncounterZone`,
`BGSZoneTargetListener`, `ZoneEntry`, `TESChildCell`, `WaterZone`.

**BGSEncounterZone class surface closed:**

```text
RTTI type descriptor     0x011840DC (.data)
Complete Object Locator  0x0110CB40 (sig=0, typeDesc match)
vtable                   0x0102CBBC, 78 slots (our COL decode, our slot dump)
atlas alignment          Xbox vftable 0x8202632C → PC 0x102CBBC, 78 slots
                         (independent lineage: Xbox debug PDB; unassessed candidate)
named slots (atlas)      5:InitializeData  8:Load  11:Save  21:SaveGame
                         23:LoadGame  28:Revert  34:InitItem  66:Copy  67:Compare
                         + inherited TESForm::* ontology; 78-target slots = folds, unresolved
```

Full slot map: `research/re/structures/bgsencounterzone-vtable.json`.

**H1.1 parser candidate:** PC `0x00525D40` = vtable slot 8 =
`BGSEncounterZone::Load` (source_atlas_candidate, 0.40 — awaits our Ghidra
decompilation for concurrence).

**Milestone check — "first function whose behavior specifically depends on
an object being ECZN":** the six `.text` sites referencing the type
descriptor (0x00417D3C, 0x00429F12, 0x00525FAC, 0x0052600C, 0x005847A3,
0x005B213E — dynamic_cast idiom confirmed at two: `push 0; push 0x11840dc`)
plus `ExtraEncounterZone`'s descriptor ref at 0x00432E9C (the
attach-a-zone-to-a-reference path = H1.2's mechanism). Classification of
these six is the Ghidra pass's first deliverable.

**Caller structure (pattern scan, pre-Ghidra):** lookup 0x00483370 has 65
call sites (record readers asking the type question); accessor 0x0043A590
has exactly ONE caller: 0x00416DC1 — a specialized helper whose context is
now a priority decompile target.

**fnv-source-atlas integrated as evidence source** (query-only, no data
forked into the repo; consumption rules + provenance classes
`source_atlas_candidate` (≤0.40) / `source_atlas_accepted` (≤0.60) in
`external-sources.md` + `confidence-policy.md`). Probe results: it knows
0x00483370 as an unambiguous function entry (size 620, no name — its
discipline) and independently aligns our vtable. Its strength: Xbox-side
names for PC code; our strength: runtime-gated gameplay semantics.

## Update 7 (2026-08-27) — caller tree above the bridge

`0x00428150` has exactly **2 direct callers** (jmp-scan + call-scan):
- `0x004BEF31` inside fn `0x004BEE00` (342 bytes)
- `0x005624AB` inside fn `0x005623D0` (648 bytes)

Both enclosing functions are atlas-confirmed unambiguous entries (no
names/alternatives yet). Neither `0x00428150` nor `0x8648A0` is
address-taken anywhere — direct-call plumbing, not virtual dispatch.
Ghidra calls.json will walk upward from `0x004BEE00`/`0x005623D0` toward
the cell-load path.

## Update 6 (2026-08-27) — second falsification; the zone-resolution bridge located

**Retraction 2: `0x01183028` is the `TESForm` RTTI type descriptor** —
name field reads `.?AVTESForm@@` (measured). It was never a
"DataHandler-region global": the NVSE faction commands were pushing it as
the SOURCE descriptor of RTTI casts (TESForm* -> target class), and the
same address appears at `0x00429F16` as srcDesc casting to
`BGSEncounterZone`. All three "handles" in the visitor cluster
(`0x01183B2C` BSExtraData, `0x01183028` TESForm, `0x011841CC`
TESObjectREFR) are type descriptors — the visitor cluster operates on
RTTI, not raw globals. KB entry replaced; correction trail kept.

**The zone-resolution bridge (H1.2/H1.3 candidate):** function
`0x00428150` (large dispatcher, no direct callers found — dispatched):

```text
0x00429E9B  operator new(0x10)
0x00429EC1  visitor ctor 0x00432E60          (vtable 0x1015C54, the 0x74-byte class)
0x00429EF8  run visitor: call 0x40FF60(this, visitor)
0x00429F0F  dynamic_cast<BGSEncounterZone*>(
              TESForm* form = 0x4839C0( 0x8648A0(arg) ))   ; lookup form, downcast
0x00429F3D  store casted zone into visitor result [+0xC]
```

Reading: the engine looks up a form from a cell/reference context and
downcasts it to BGSEncounterZone — then feeds the visitor. This is the
"which zone belongs to this cell/reference" resolution path. The second
ctor caller `0x00421CC9` sits in a sibling dispatcher.

Status: H1.1 solved (static). H1.2 = this bridge; pending Ghidra
decompilation of `0x00428150` + the visitor pair to confirm the lookup
source (`0x8648A0`/`0x4839C0` semantics) and pin H1.3's gameplay caller.

## H1.2 openings (update 4, 2026-08-27)

**Save symmetry** — `BGSEncounterZone::Save` (0x00525E70, atlas slot 11)
executes `WriteSubrecord('DATA', this+0x18, 8)` — the exact write
symmetric to Load's read. Field offset `+0x18` now has independent
read-side AND write-side proof.

**Field-A nuance (honest correction):** `[this+0x18]` dword A is treated
as a *nullable handle*: Save null-checks it, transforms non-null values
via 0x84E3A0 before writing, and InitItem (0x00525F00) passes it into
lookup machinery (`0x485D50`/`0x4839C0`/virtual `+0x130`). Vanilla A=0
everywhere, so the branch is cold in vanilla data. DATA layout best read
as `{u32 nullable handle-or-id, u32 flags}` — dword A's exact semantic is
open (Ghidra decompile of InitItem will settle it).

**0xEC43FB role identified — second NVSE↔GOG triangulation.** The NVSE
mining's #1 engine candidate (score 857) is called at 0x00432EA5 with the
five-arg `__RTDynamicCast` signature `{obj, vtoff, srcDesc=BSExtraData,
dstDesc=ExtraEncounterZone, isRef}`. The engine's cast primitive is the
same helper every NVSE script command uses. 0.40 → 0.60.

**H1.2 core mechanism — REFRAMED (update 5):** `0x00432E90` casts an
extra-data entry `BSExtraData → ExtraEncounterZone` and compares
`[+0xC]` handles via `0x4D9780` — but its address is TAKEN (not called)
at 0x01015C58, slot 1 of vtable `0x01015C54` (ctor `0x00432E60`, class
size 0x74). The `0x01015C30`–`0x01015C9C` region is a cluster of
visitor-class vtables interleaved with extra-data COLs (EEZ COL
@ 0x01104474, RagDoll @ 0x01104428, UsedMarkers @ 0x011044C0), and
neighboring `0x00432DD0` casts to **ExtraRagDollData** — per-type match
functions. The earlier "EEZ get/attach" framing is RETRACTED; row-to
-class attribution is unresolved. First Ghidra decompile target: this
visitor cluster — it is where "which zone applies to this cell/reference"
gets answered, but the exact wiring needs decompilation, not dword
alignment guesses.

Open: what `[+0xC]` fields mean on both sides; the dispatch entry into
the visitor cluster (who constructs the 0x74-byte visitor and walks the
extra-data list — Ghidra calls.json will answer directly); flag-bit
semantics for dword B (bit 8/9/10/11/16... vary in vanilla).

## H1.1 — CONCURRENCE ACHIEVED (update 3, 2026-08-27)

`BGSEncounterZone::Load` @ `0x00525D40` independently verified against
plugin bytes. Capstone disassembly (0x00525D40–0x00525E5A) shows a textbook
TESForm::Load override:

- entry tag check `cmp eax, 0x61` ('a' — plugin form tag), early-out
- subrecord loop (`call 0x4726b0` → tag, `call 0x4726f0` → has-more)
- switch on exactly `'DATA'` / `'EDID'` / `'OBND'` — matching plugin ground
  truth (17 vanilla ECZNs = `EDID + DATA(8B)`; OBND inherited from TESObject)
- **DATA branch: `ReadBytes(this+0x18, 8)`** — the 8-byte DATA field lands
  at `this+0x18`, then `call 0x503210` post-processes it
- EDID branch: `ReadBytes(buf, 0x200)` → virtual `vtable+0x134` (editor-ID
  setter); OBND branch: virtual `vtable+0xE0` (inherited)

Confidence: `source_atlas_candidate` (0.40) + independent structural
concurrence → **0.60** (static cap; runtime tier still gated).
First recovered struct field: `BGSEncounterZone+0x18 = {u32 fieldA,
u32 flags}` (fieldA = 0 in all 17 vanilla records; flags bits 8–16 vary).

**H1.2 entry points identified:**

- `0x00432E90`: function doing `push 0; push 0x1184cf4` — dynamic_cast to
  `ExtraEncounterZone` on a `this` object (get/attach-zone-on-reference
  pattern — the CELL/reference ↔ ECZN binding mechanism)
- accessor's sole caller `0x00416DC1`: method reads `[this+0xC]`, gates on
  a bool, calls accessor `0x0043A590` with an arg, tests bool result,
  `push 1` fallback branch — a conditional resolve/validate query

Ghidra headless import of the GOG exe is running in the background; its
decompilation + call graph will refine all of the above (pseudocode for
Load, the six cast sites, 0x00416DC1's enclosing function).

## Next steps for H1.1 → H1.2

1. Ghidra headless import of the GOG exe — real decompilation for
   0x00483370 / 0x0043A590 plus callers/callees of the lookup function.
2. From the lookup's callers: the plugin-load path (record 4CC → ordinal →
   descriptor → constructor via descriptor vtable) — H1.1 completion.
3. H1.2 entry: callers of the accessor in CELL/reference processing — the
   caller that resolves an ECZN *for* a reference is the H1.3 candidate.

NVSE annotation-layer mining (`research/re/nvse_xrefs.json`, via
`scripts/re/mine_pdb.py`) maps 1,264 engine VAs to named NVSE
functions. Cross-reference that file for any engine VA
recovered here — `nvse_semantic_reference` evidence strengthens every step.

## Candidate functions (historical snapshot; superseded by Update 8)

| VA (build) | Candidate meaning | Confidence | Evidence |
|------------|-------------------|------------|----------|
| gog 0x00525D40 | **BGSEncounterZone::Load** — ECZN record parser (H1.1 SOLVED at static tier) | 0.60 | atlas slot 8 + subrecord disassembly concurrence (symbols.json) |
| gog 0x00483370 | FormTypeRegistry 4CC→ordinal lookup | 0.60 | registry decode + instruction semantics (symbols.json) |
| gog 0x0043A590 | Registry accessor by ordinal, singleton preamble | 0.40 | structural: registry index + DataHandler-candidate pushes |
| gog 0x00432E90 | ExtraEncounterZone get/attach on reference (H1.2 entry) | 0.20 | dynamic_cast idiom to ExtraEncounterZone descriptor; role unconfirmed |
| gog 0x01187004 | form-type registry structure | 0.60 accepted-structure | 121-entry walk + RTTI corroboration |
| gog 0x01183028 | DataHandler-region global | 0.60 | NVSE faction-cmd refs + GOG accessor push (independent) |

## Update 8 (2026-08-27) - H1-SL static boundary and runtime handoff

This section supersedes the earlier `0x00428150` resolver description and the
earlier `0x00432E90` get/attach description. The old text is retained above as
an auditable correction history; both semantic claims are retracted.

### Updated chain

```text
ECZN form type ordinal 98
  -> record descriptor 0x0101C364
  -> BGSEncounterZone RTTI descriptor 0x011840DC
  -> BGSEncounterZone vtable 0x0102CBBC
  -> vtable slot 8, 0x00525D40 (Load candidate; parses ECZN subrecords)

save/load path
  0x005623D0 (TESObjectREFR::LoadGame candidate)
      -> 0x00428150 (ExtraDataList::LoadGame; void)
          -> serialized extra-data type 0x74
          -> 0x00432E60 (construct/reuse 0x74-byte ExtraEncounterZone,
                         vtable 0x01015C54)
          -> 0x0040FF60 (BaseExtraList::AddExtra candidate; attach to list)
          -> 0x008648A0 (load-buffer form-ID read candidate)
          -> 0x004839C0 (opaque form/handle lookup helper)
          -> RTDynamicCast, source 0x01183028 (TESForm),
             destination 0x011840DC (BGSEncounterZone)
          -> store the cast result at ExtraEncounterZone +0x0C

  0x004BEE00 (unresolved bound-object/nested extra-data load context)
      -> 0x00428150

  0x00416BE0 (extra-data rebind/cleanup path)
      -> reload saved zone form identifier from the ExtraEncounterZone slot
      -> cast to BGSEncounterZone
      -> store at the same +0x0C slot, or remove the extra if missing
```

The two direct call sites into `0x00428150` are `0x004BEF31` in
`0x004BEE00` and `0x005624AB` in `0x005623D0`. The exported GOG call graph
records the two direct edges. It does not list every helper visible in the
decompiler's `case 0x74` body (`0x00432E60`, `0x008648A0`, and `0x004839C0`),
so those edges remain a decompiler/export contradiction rather than a reason
to infer a different semantic chain.

### Answers to the H1 questions

1. **Object/context entering the resolver.** There is no gameplay resolver at
   `0x00428150`. Its context is a `BaseExtraList`/`ExtraDataList` receiver plus a
   save-game load-buffer argument. The function walks serialized extra-data
   type codes; the `0x74` case is the `ExtraEncounterZone` restoration case.
   `0x005623D0` supplies a reference-load context, while `0x004BEE00` supplies
   a nested bound-object/item-change-like load context. The exact class name of
   `0x004BEE00` is not established.

2. **Source of the `TESForm*`.** The load buffer supplies a serialized form
   identifier through `0x008648A0` (atlas candidate: load-buffer `LoadFormID`).
   `0x004839C0` is an opaque lookup/handle helper whose exact return type is
   unresolved; its decompilation returns a value through `0x00853130`, while
   the atlas label for `0x004839C0` is contradictory and is not promoted.
   The value entering the cast is nevertheless explicitly treated as a
   `TESForm*`: source descriptor `0x01183028` is cast to destination descriptor
   `0x011840DC` (`BGSEncounterZone`).

3. **Storage/return.** `0x00428150` returns `void`. The successful cast result
   is written to offset `+0x0C` of the `ExtraEncounterZone` extra-data object
   constructed by `0x00432E60`. `0x00416BE0` later rebinds that slot from the
   saved form identifier and removes the extra-data object when the zone is
   missing. This slot is distinct from `BGSEncounterZone +0x18`, the ECZN DATA
   payload recovered in H1.1.

4. **Consumers.** On the requested chain, the direct consumers are the two
   load contexts above. `0x00432E90` consumes `ExtraEncounterZone` objects as a
   virtual comparison method: it casts `BSExtraData` to `ExtraEncounterZone`
   and compares `+0x0C`; it is not a resolver. Separate static ECZN consumers
   exist in `0x00525F00` (ECZN owner-form initialization) and `0x005845E0`
   (worldspace owner-form initialization), but neither is downstream of
   `0x00428150` and neither reaches spawning in the recovered artifacts.

5. **Downstream gameplay.** No traced consumer reaches a CELL/reference
   encounter-zone lookup, leveled-list selection, actor level selection, or
   spawn generation. `0x005623D0` is reference *load* processing, not evidence
   of an actor encounter-generation path. The worldspace path at `0x005845E0`
   resolves an owner ECZN pointer and stops at a worldspace helper. This is a
   bounded negative result for the traced chain, not a claim that those systems
   do not exist elsewhere in the engine.

### Evidence and contradictions

| Question | Independent evidence | Result / limitation |
|---|---|---|
| `0x00428150` role | `re_decompiled` body and self-identifying `ExtraDataList::LoadGame` error string | save/load dispatcher; case `0x74` is the zone extra-data case |
| Direct parents | `re_decompiled` for `0x004BEE00` and `0x005623D0`; `research/re/calls.json` | two direct callers; `0x005623D0` is a LoadGame candidate, `0x004BEE00` remains unnamed |
| Zone object | `re_decompiled` `0x00432E60`, `0x00432E90`, `0x0040FF60`; RTTI strings and vtable structure | constructor/attach/vtable and `+0x0C` comparator relationship are strong; resolver/visitor interpretation retracted |
| Form source | `re_decompiled` `0x008648A0`, `0x004839C0`; atlas PC candidate labels | serialized ID and lookup path are established; which helper returns the final `TESForm*` is unresolved |
| ECZN class surface | `re_decompiled` `0x00525D40`, `0x00525E70`, `0x00525F00`; `bgsencounterzone-vtable.json` | parser, DATA field, and owner-form initialization are separate from savegame binding |
| Atlas | `re_atlas_pc`/PC atlas records for the relevant addresses | labels are candidate mappings with `not_semantic_truth`; `0x004839C0`'s atlas label conflicts with its observed use |
| Static xrefs | `re_xrefs` against Steam | empty results are unusable negative evidence because Steam `.text` is CEG-wrapped/encrypted |
| Callgraph | `re_callgraph` against Steam; GOG `calls.json` | Steam rebuild timed out; GOG export is useful for measured edges but omits some decompiler-visible helper calls |
| NVSE layer | `re_nvse_xrefs` for the key VAs | no named NVSE corroboration; this does not prove no native callers |
| Record truth | `fnvedit`: ordinal 98 = ECZN, 17 records in the configured master | record count/type corroborate the anchor, but current output has Fallout 3-like EditorIDs and exposes no DATA fields; plugin purity/field truth remains a gap |

### Smallest runtime test

H1 is ready for runtime verification at the save/load boundary. Since no
static gameplay consumer was reached, the smallest useful experiment tests the
recovered pointer lifecycle rather than claiming a spawn result.

1. Use the Steam executable with debugger breakpoints expressed as module RVA
   (the static GOG VAs are `0x00028150`, `0x001623D0`, `0x00016BE0`, and
   `0x004648A0` for `0x00428150`, `0x005623D0`, `0x00416BE0`, and `0x008648A0`
   respectively). First confirm the GOG-to-Steam function match before using
   the addresses as breakpoints.
2. Load a save that naturally contains an `ExtraEncounterZone` extra-data
   entry. At the `0x74` branch, log the load-buffer argument, serialized form
   identifier, lookup result, dynamic-cast result, and the value written to
   `ExtraEncounterZone +0x0C`. A passive trace is the baseline.
3. Repeat with the referenced ECZN unavailable, or use a debugger-only
   conditional manipulation that makes the lookup/cast result null for this
   entry. The predicted result is a null `+0x0C` slot followed by
   `0x00416BE0`'s existing missing-zone message and removal of the extra-data
   object. Do not modify the installed master as part of the baseline test.
4. Confirmation requires the two expected outcomes: an available zone leaves
   the extra-data object with a non-null pointer to the expected ECZN, while a
   missing zone takes the cleanup path. Repeating the pair is the route to a
   higher experimental confidence tier. This experiment confirms save/load
   restoration only; it cannot confirm leveled-list, actor-level, or spawn
   behavior.

If no natural save reaches type `0x74`, stop rather than manufacture a
gameplay conclusion. The next runtime task would be to identify how a test
save acquires that extra-data record, then repeat the same passive trace.

### Unresolved questions

- Which exact helper (`0x008648A0`, `0x004839C0`, or the helper beneath
  `0x00853500`) returns the final `TESForm*`, versus a form ID or handle?
- Is extra-data type code `0x74` independently documented by a record/enum
  source, or only established here by constructor, vtable, and RTTI concordance?
- What is the exact class and semantic role of `0x004BEE00`, and what do its
  callers `0x004D4160`, `0x0095A3B0`, and `0x009C52F0` represent?
- Where is the actual runtime CELL/reference encounter-zone lookup used by
  leveled-list or spawn generation? It is not on this save/load chain.
- Is the configured `fnvedit` master a clean FNV source? Its ECZN output mixes
  FNV-looking and Fallout 3-like EditorIDs and does not expose the DATA bytes.
- What is the verified Steam runtime address mapping after CEG unpacking or
  function matching?
