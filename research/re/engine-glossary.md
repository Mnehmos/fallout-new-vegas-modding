# FNV Engine RE Glossary & Findings Wiki

Self-reference for the engine RE effort: target binaries, tool behaviors, confirmed
identities, and per-bug address findings. Append as work progresses; keep claims
labeled by confidence (CONFIRMED / LIKELY / GUESS).

---

## 1. Target binaries

| Binary | Path | Role |
|--------|------|------|
| GOG 1.4.0.525 (CEG-free) | `E:\GOG Galaxy\Games\Fallout New Vegas\FalloutNV.exe` | PRIMARY static-analysis target. `.text` entropy 6.561, 7 sections, no warnings. sha256 `89e7020...11dd0fe`. |
| Steam on-disk | `H:\01_Games\Steam\steamapps\common\Fallout New Vegas\FalloutNV.exe` | PACKED (`.text`/`.bind` entropy 8.0). Disassembly/xrefs/callgraphs meaningless. Data-layer only (strings/imports). Never analyze statically. |

- Both share pe_timestamp `0x4e0d50ed` and identical section layout; community hex
  addresses (GECKWiki, NVSE docs) are VAs with image base 0x400000 and apply to the
  GOG exe. GOG adds `GalaxyWrp.dll` import, drops `steam_api.dll` — code layout is
  the same 1.4.0.525 image.
- Runtime work (BUG-001) previously targeted the Steam install; static RE uses GOG.
- Launcher observed: `"E:\GOG Galaxy\GalaxyClient.exe" /command=runGame /gameId=1454587428 /path="E:\GOG Galaxy\Games\Fallout New Vegas"`.

## 2. Tooling notes (remcp MCP + scripts)

- remcp `binary` param: absolute path; spaces fine. Use the GOG path everywhere.
- **First touch cost:** first analysis call builds the code index (~4.13M instructions)
  and can exceed the 30s MCP timeout — the cache survives; just retry the same call.
- `re_strings`: gamesetting/editor-name strings live in `.rdata` ASCII. Exact-name regex
  can miss because a stray preceding char glues on ("CiSneakLevelBonus") — search by
  distinctive substring. UTF-16 exists for UI strings; settings are ASCII.
- `re_xrefs` with `is_string=true` takes the string TEXT (e.g. `iSneakLevelBonus`),
  not an address. Returns code_refs (imm:push sites) + data_refs (ptr32 scans).
- `re_xrefs` on a code VA returns the direct caller list — use it to pin function
  entry points and callers (e.g. 0x642ED0 has exactly one caller).
- remcp has NO native PE decompiler. For C output use the Ghidra pipeline
  (`scripts/re/import_ghidra.py`, postscripts in `tools/re/ghidra/postscripts/`).
  Naming: Ghidra exports are `FUN_XXXXXX`; record community/PDB-derived names alongside.
- Default gamesetting lookup is name-hashed at runtime; static identification is via
  the `.rdata` name strings referenced by the giant settings-init function (~0xF5Cxxx).
- Gamesetting getter idioms (CONFIRMED by use):
  - `call 0x403E20` with `ecx = Setting*` → returns ptr to float value (`fld [eax]` follows).
  - `call 0x43D4D0` with `ecx = Setting*` → returns ptr to int value.
  - Setting object layout (NVSE-known): `name*` +0x0, `type` +0x4, `value` +0x8, `next*` +0xC.

## 3. Engine knowledge base

### 3.1 FNV-BUG-002 — iSneakLevelBonus sneak inversion (RE MAPPING, near root-cause)

**Function 0x642ED0** = sneak/detection-value accumulator (wiki-cited). Sole caller:
call site `0x8A152D` inside a large detection updater (CFG tool misreads 0x8A152D as a
function start; true enclosing prologue not yet located).

**Settings used by 0x642ED0 (all CONFIRMED via ctor thunks → name strings):**

| Setting obj | Name | Default | Ctor thunk |
|-------------|------|---------|------------|
| 0x11CD7E4 | fSneakBaseValue | −25.0 | 0xF59420 |
| 0x11CD8C0 | iSneakStartBonus | 50 | 0xF5CC20 |
| 0x11CD13C | iSneakLevelBonus | 5 | 0xF5CBF0 |
| 0x11CD4C0 | iSneakStartBonusLevelPen | 10 | 0xF5CC50 |
| 0x11CDBF8 | fSneakAmbushTargetMod | (float bits @0x10184F4) | 0xF5A650 |
| 0x11CD1E0 | fSneakAmbushNonTargetMod | (float bits @0x104FD68) | 0xF5A680 |
| 0x11CDF04 | fSneakPerceptionSkillMin | (float bits @0x1017B78) | 0xF59720 |
| 0x11CDD9C | fSneakPerceptionSkillMax | (float bits @0x10249D8) | 0xF59750 |
| (also read) | 0x11CDFC0, 0x11CD774, 0x11CDBD4, 0x11CDCBC, 0x11CD7D8, 0x11CD304 — names not yet pulled | — | — |

**Reconstructed logic (instruction-exact so far):**

```
A = arg2                                            // seed accumulator [ebp-0x5C]
A += (arg24 − arg23) × iSneakLevelBonus             // 0x642F10–0x642F1C — SIGNED, UNCLAMPED  ← BUG SITE
A += max(0, iSneakStartBonus − arg24 × iSneakStartBonusLevelPen)   // 0x642F1F–0x642F48, max = 0x647B70
A −= arg25                                          // 0x642F4B–0x642F51
perceptionSkill = fSneakPerceptionSkillMin + (Max−Min) × (arg1 / [dbl @0x1020758])   // 0x642FF3–0x643004
factor = (1 + ambushMod + setting(0x11CDFC0)×flag(+0x3C) + setting(0x11CD774)×flag(+0x38) + setting(0x11CDBD4)×flag(+0x4C))   // flags→bools at 0x642F69–0x642F96, factor at 0x643007–0x643076
result feeds distance/lighting tail (0x643079+): flags +0x14/+0x24/+0x10/+0x30/+0x34/+0x2C/+0x48, settings 0x11CDCBC/0x11CD7D8/0x11CD304, ratio (x−arg5)/x, helper 0x404010
```

**Bug signature (wiki-matched):** `(arg24 − arg23) × iSneakLevelBonus` is the only
unclamped signed term; every sibling level term is `max(0, ...)`. When the player
out-levels the actor, this term goes negative and the wiki reports the net effect is
harder sneaking. YUP's reverted GMST workaround failed because the sign/structure, not
the magnitude, is wrong.

**Candidate fixes (pick after arg mapping + runtime test):**
1. Swap sub operands at 0x642F10/0x642F13 (`mov edx,[ebp+0x64]; sub edx,[ebp+0x60]` → reversed).
2. Clamp term1 ≥ 0 like term2 (max-style branch after 0x642F16).

**Remaining for root cause:** map caller args arg23/arg24/arg25 to player/actor levels
(follow the 25-push sequence at 0x8A14E0–0x8A152D upward to source locals); locate true
enclosing function start of the caller; confirm sign direction against Xbox/FO3 symbol
names; runtime A/B test.

**Identity aids:** float getter `0x403E20` (ecx=Setting* → ptr to float), int getter
`0x43D4D0` (→ ptr to int), int max `0x647B70(a,b)`, Setting ctor `0x40C150` (int) /
`0x40E0B0` (float), register `0xEC658F(sectionString)`; name strings cluster in
.rdata 0x104Fxxx–0x1051xxx; ctor thunks are standalone `push typeOrDefault; push name;
mov ecx,obj; call ctor; push sectionStr; call 0xEC658F; ret` fragments.

### 3.2 Carried over from FNV-BUG-001 (VATS grenade 0%) — established facts

- `VATSMenu` RTTI `.?AVVATSMenu@@` COL @ 0x01118558; PC `FUN_007EC810` = Xbox
  `VATSMenu::DoIdle` (per-frame), contains zero-chance gate `0x007EEA2D` (reads
  entry+0x28) / `0x007EEA5B` (blocks queue on 0.0). `DoClick` = PC `0x7EECB0`.
- Grenade entry creation: `FUN_007F52C0`; live chance update path `FUN_007F1290`
  calls resolver `FUN_00646F70` @ 0x007F158E.
- Root cause: body-part lookup `FUN_00800A00` rejects body-part index −1 @ 0x007F4544,
  branch 0x007F454E skips the live chance call. Fallback multiplier pointer at
  0x00800A7D pointed at 0x01012054; fix redirects to plugin-owned 0.2f.
- Thrown-weapon formula (same resolver, non-target branch) + live gamesetting values
  are recorded in bugs.json `superseded_thrown_weapon_analysis` — still valid reference
  for VATS grenade math.
- Skill helpers: `FUN_00646880` skill calc 1, `FUN_0066EF50` __thiscall skill calc 2,
  `FUN_00446390` skill-arg derivation, `FUN_004C0BF0` thrown-weapon classification.

### 3.3 Prior subsystem maps (do not re-derive)

- Encounter zones: `research/re/encounter_zone_subsystem.md` (BGSEncounterZone layout,
  XZEN link, registry readers).
- Population levers: `research/population/encounter-zones.md` (iNumberActors* settings
  with live values + reader sites).
- General pipeline/commands: `docs/re-pipeline.md`.

## 4. Open questions / watch list

- Community address library / symbol DB for FNV (xNVSE-side): research batch A is
  hunting for a public address→name database. If found, record URL + format here and
  prefer its names over FUN_XXXXXX in all future notes.
- Xbox 360 PDB-derived vtable names were used in BUG-001 (`atlas_findings` in
  bugs.json); the source of those names should be captured here when batch A reports.
