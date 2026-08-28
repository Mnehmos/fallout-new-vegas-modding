# Encounter Zone Engine Subsystem — RE Map

**Build:** FalloutNV.exe GOG 1.4.0.525 (sha256 89e70204…)
**Method:** xref-anchored static analysis (string anchors → E8 rel32 caller scans → Ghidra decompiles). Full falsification trail in `docs/data/bugs.json` (FNV-BUG-001 work) and this document.
**Status:** subsystem mapped; spawn-tick location still open (see Open Questions).

## Class

`BGSEncounterZone` (RTTI `.?AVBGSEncounterZone@@` — descriptor `0x011840DC`, COL `0x01118558`, **vtable `0x10251AC`, 78 slots**). Form type ECZN = registry ordinal 98 (form-type registry `0x01187004`, stride 12).

## Key functions (all addresses base-relative, FNV.exe + 0x…)

| Address (VA) | Role | Evidence |
|---|---|---|
| `0x00525D40` | `Load` (vtable slot 8) — reads 84-byte body into `this+0x18` | subrecord concurrence, atlas slot 8 |
| `0x00525AE0` | wrapper: `FUN_00525A90(this − 0xA4, …)` — embedded sub-object accessor | wrapper pattern |
| `0x00525A90` | effective-value lookup: `FUN_00525980(sub)` → fallback `*(parent+0x118)` | decompile |
| `0x00525F00` | `InitItem` (slot 34) — **resolves owner formID at `this+0x18` in-place to `TESForm*`** | decompile + owner-form error string @`0x0102CCF8` |
| `0x00584170` | TESWorldspace save/load subrecord writer — tags `XZEN`, `WNAM`, `PNAM`, `CNAM`, `NAM2` | tag constants in code |
| `0x005B17A0` | console/script zone parameter handler ("Invalid encounter zone '%s' for parameter %s") | error string xref |
| `0x004144A0` | savegame zone restoration ("Unable to find encounter zone %08X…") | error string xref |
| `0x0083F680` | savegame changelist registration: `CHANGE_ENCOUNTER_ZONE_GAME_DATA`, `CHANGE_ENCOUNTER_ZONE_FLAGS`, `CHANGE_REFR_EXTRA_ENCOUNTER_ZONE` | changelist name xrefs |
| `0x00FAAD00` | settings registration incl. `bEncounterZoneTargetRestrict:Combat` | string xref |
| `0x00432A70` | `ExtraEncounterZone` consumer (RTTi cast site, descriptor `0x01184CF4`) | descriptor xref |
| `0x00646F70` | ⚠ **DEAD on PC**: complete VATS-target chance calculator incl. grenade-target formula (`fVATSGrenadeTargetArea`, live value 1640.0) — zero callers/refs. Falsification note: an earlier E8 scan used absolute-address matching (bug); corrected rel32 scan found the single live caller `0x007F158E` in `FUN_007F1290`. Grenade-target entries never reach it. | rel32 scan + runtime patch |

## Structures (partial)

```c
// BGSEncounterZone runtime object (partial)
+0x000  vtable (0x10251AC)
+0x018  owner form: formID at load → resolved TESForm* at InitItem   // InitItem in-place resolve
+0x118  fallback field for FUN_00525A90 effective-lookup
+...    DATA blob (84 bytes read by Load) — exact sub-offsets TBD vs fnvedit dump

// TESWorldspace
+0x0D0  Encounter Zone pointer (BGSEncounterZone*) — saved as subrecord 'XZEN'

// VATSTargetData (from BUG-001 work — unrelated subsystem, same toolchain)
+0x000  screen coords (2 floats)
+0x008  world pos A (3 floats)
+0x014  world pos B (3 floats)
+0x020  0xFFFFFFFF
+0x028  chance float (live path writes 0.0 for grenade targets)
+0x030  target TESForm*/REFR*
```

## Form-type registry

Base `0x01187004`, 121 entries, stride 12: `{uint32 descriptor*, uint32 zero, uint32 ordinal}`. ECZN = ordinal 98, descriptor `0x0101C364`. Full map: `../research/re/form_type_registry.json` (this dir: `form_type_registry.json`).

## Settings (live, in-process)

| Setting | Live value |
|---|---|
| `fVATSGrenadeRangeMult` | 2.0 |
| `fVATSGrenadeRangeMin` | 128.0 |
| `fVATSGrenadeSkillFactor` | 0.4 |
| `fVATSSkillFactor` | 1.0 |
| `fVATSGrenadeChanceMult` | 1.0 |
| `fCrippledArm1HSpreadPenalty` | 0.2 |
| `bEncounterZoneTargetRestrict:Combat` | (registered @ `0x00FAAD00`; live value TBD) |

*(VATS settings — recorded during the BUG-001 detour; they live in the same Setting table the population tuning would use.)*

## Anchor strings (xref sources)

- `0x01014788` "Unable to find encounter zone %08X…" → savegame restore (`FUN_004144A0`)
- `0x0102CCF8` "Unable to find owner form (%08X) on encounter zone '%s' (%08X)." → InitItem (`FUN_00525F00`)
- `0x01031D10` / `0x01031D54` "Unable to find encounter zone (%08X) on owner worldspace…" → worldspace load (`FUN_00584170`)
- `0x01038D48` "Invalid encounter zone '%s' for parameter %s." → console handler (`FUN_005B17A0`)
- `0x0107DF44` / `0x0107DF70` / `0x0107E72C` → changelist names (`FUN_0083F680`)
- `0x01044750` "EncounterZone" literal — no .text refs (likely GECK/editor string)

## Open questions (next RE pass)

1. **Spawn tick**: where does the engine consume `BGSEencounterZone` at runtime (level scaling vs player, reset semantics)? Candidates: vtable consumers of the 78 slots (Xbox names from atlas: slots 6/7 = `Actor::UseSkill` candidates need re-attribution), or scan-side xrefs from the 11 registry-reader functions.
2. **DATA blob sub-offsets**: correlate the 84-byte Load body with the fnvedit ECZN DATA dump to name each byte (Level/Flags/Owner/Rank…).
3. **Worldspace zone list**: `TESWorldspace+0xD0` is a single zone pointer (XZEN); how do MULTIPLE ECZNs on one worldspace attach (cell-level? the `ExtraEncounterZone` extra-data path)? The `0x00432A70` consumer + `FUN_00432A90` cast site is the thread.
4. **Live instance discovery**: find runtime `BGSEencounterZone` instances via the form-list (registry ordinal 98) — enables live field dumps without new RE.
