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

**Caller argument map (CONFIRMED, call site 0x8A152D — 25 args pushed in blocks
0x8A14B5–0x8A152D, last push = arg1):**

| Arg | Source at caller | Meaning (confidence) |
|-----|------------------|----------------------|
| arg24 | `[ebp-0x28]` = level of caller-arg `[ebp+0xC]` via +0xA4 → virtual +0x28 (movzx ax) | the *other* actor's level (CONFIRMED fetch pattern) |
| arg23 | `[ebp-0x5C]` = level of `[ebp-0x98]` via identical +0xA4 → virtual +0x28 pattern | the *detecting/subject* actor's level (CONFIRMED fetch pattern) |
| arg22 | `[ebp-0x68]` out-ptr; arg21 `[ebp-0x2C]` out-ptr; arg20 `[ebp-0x3C]` out-ptr | result slots (LIKELY out pointers — lea) |
| arg4 | float from helper `0x5E58F0(0x1F, actor, ...)` — actor-variable getter, player-redirect global `0x11DEA3C`, AV-74 guard `0x4A`; then × fSneakPerceptionSkillMin-ish scale @0x8A149B | sneak-skill term (CONFIRMED helper identity; exact AV index LIKELY=31) |
| arg1 | `[ebp-0x10]` (pushed 0x8A1529) | actor/process object (CONFIRMED last-push=arg1) |

**Decisive finding:** arg23 and arg24 are fetched with the *identical* +0xA4→vtable+0x28→
movzx ax level-getter pattern (0x8A1447 vs 0x8A146A) on two different actors. The
wiki-cited bug term `(arg24 − arg23) × iSneakLevelBonus` is therefore a raw signed
difference of two actor levels. Whether player-vs-NPC is inverted in the subtraction
order is the final open question: it requires either the Xbox PDB symbol for 0x642ED0
or a runtime two-actor A/B (player above vs below actor level, identical build). The
sibling start-bonus term is explicitly clamped (`max(0, …)` @0x647B70) while this one is
not — strong evidence the sign is a defect, not a design choice.

**Ghidra decompile CONFIRMS the root cause** (`decompiled/FUN_00642ed0_00642ed0.c`,
function is 26 params, `__cdecl`-style). The return value is
`fVar1 + fVar22 + local_34 + fVar2` where the sneak-detection magnitude is:
```
... - max(0, iSneakStartBonus - param_24*iSneakStartBonusLevelPen)
      - (int)((( (clampedTerm + (param_24 - param_23)*iSneakLevelBonus + param_2) - param_25) * ambushFlag))
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      the bug: (param_24 - param_23) is a SIGNED actor-level difference multiplied by
      iSneakLevelBonus (iVar13), UNCLAMPED. When param_24 (other actor level) < param_23
      (this actor level) the term goes negative, exactly as the wiki describes.
```
- Line 148 in the decompiled C is the single decisive expression. The neighboring
  `FUN_00647b70(iVar18 - param_24*penalty, 0)` at line 53 is the clamped sibling —
  the engine deliberately clamps that one and forgot the level-difference one.
- **Minimal patch candidates (now designable from the C, not raw bytes):**
  1. Clamp the term: wrap `(param_24 - param_23)*iVar13` with the same `FUN_00647b70(...,0)`
     max-0 helper — mirrors the existing start-bonus clamp (behavior-preserving when the
     bonus should only ever add).
  2. Absolute difference `abs(param_24 - param_23)*iVar13` if intent is magnitude.
  Pick after runtime A/B; candidate (1) is the conservative, self-consistent fix.
- arg23/arg24 semantic roles (player vs NPC) still need the runtime two-actor test to
  finalize, but the *defect* (missing clamp on the level-difference term) is now
  CONFIRMED at instruction and decompiled-C level.

**DIRECTION RESOLVED (caller FUN_008a0d10 decompiled, 2026-09-04):**
- `param_1_00` = the detecting NPC (`this`); confirmed at line 278 `param_1_00 == DAT_011dea3c`
  is tested against the player singleton (so param_1_00 is the NPC observer, param_2 the
  player target being sneaked-by).
- NPC level: `local_60 = (*(int*)(param_1_00 + 0xa4))->vtable[+0x28]()` masked to 16 bits.
- Player level: `local_2c = (*(int*)(param_2 + 0xa4))->vtable[+0x28]()` masked to 16 bits.
- Both packed via `FUN_00ec62c0(...)` into a 6-float result buffer, then passed to the
  19-arg `FUN_00642ed0`. The signed `(param_24 - param_23)` therefore encodes
  **(NPC_level - Player_level)** (order to be re-confirmed against the exact arg index at
  the 0x642F10 sub, but the two level sources and the player/NPC roles are now fixed).
- When the player OUT-levels the NPC, NPC_level - Player_level < 0 -> iSneakLevelBonus
  becomes a negative sneak modifier -> harder to sneak. This is the exact reported symptom.
- Final runtime confirmation still recommended, but the static evidence now fully supports
  the causal chain end-to-end.

**Reusable engine anchors discovered here:**
- Player singleton pointer stored at `0x11DEA3C` (used by the actor-variable getter's
  player-redirect path).
- Actor-variable getter `0x5E58F0(avType < 0x4A, actor, ...)` → vtable+0x4AC AV-info
  lookup → `0x6815C0` value read. Any "reads an actor value" call site routes here.
- Setting accessors: float `0x403E20`, int `0x43D4D0` (ecx=Setting*). Setting ctor
  thunks near 0xF5xxxx bind `.data` Setting objects (0x11CDxxx–0x11CFxxx range) to
  `.rdata` name strings (0x104Fxxx–0x1051xxx).
- Int helper `0x647B70(a,b)` = `max(a,b)` (plain cdecl, 16-byte body).

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

### 3.3 Console commands → engine handlers (BUG-003 root cause, CONFIRMED 2026-09-04)

| Command | Name string | Command struct (.data) | Execute handler |
|---------|-------------|------------------------|-----------------|
| RemoveAllItems | 0x1040B74 | 0x1192418 | 0x5B1570 (console parser/re-emitter) |
| RemoveAllTypedItems | 0x103E114 | 0x1196478 | **0x5B55A0** (bulk removal via shared 0x4CE340) |
| RemoveItem | 0x1041268 | 0x11915E0 | **0x5B4E90** (per-item + IsEquipped + unequip) |
| UnequipItem | 0x1040584 | 0x1192E68 | 0x5D0300 |
| SayToDone (BUG-012) | 0x1044584 | 0x118E408 | 0x5CA950 → core 0x5CA1C0 |

**BUG-003 root cause CONFIRMED** from Ghidra decompilation (2026-09-04):

- **RemoveItem** (0x5B4E90) calls `(**(code **)(*local_14 + 0xe4))` (IsEquipped check)
  → `FUN_008248e0(local_1c, 1)` (the engine unequip path) at line 115, **before** calling
  the vtable+0x17C remove function pointer (lines 98/117).
- **RemoveAllTypedItems** (0x5B55A0) and the RemoveAllItems→RemoveItem chain (parser
  0x5B1570 at line 85) call `FUN_004CE340` directly — the shared engine remove-from-
  inventory primitive — with **no IsEquipped check and no unequip call**. That function
  pointer slot is `local_230 + 0x1c`, not vtable+0xE4/+0x17C.
- The **OnUnequip/OnEquip script block** fires from the unequip function called by
  RemoveItem's vtable dispatch. Bulk path skips it entirely. Magic effects (enchantment,
  armor spells) are applied via the same equip/unequip lifecycle; the bulk remove leaves
  them active because the teardown never runs.

**Fix direction (design from C, minimal patch):**
- Patch RemoveAllTypedItems's `FUN_004CE340` call chain, or the shared inventory-remove
  helper it calls, to add the same IsEquipped→UnequipItem pre-pass that RemoveItem does.
- Alternatively, patch RemoveAllItems' parser 0x5B1570 to loop through equipped items
  and emit UnequipItem calls per item before calling the bulk remove.

**Next steps after pass 2 (identity corrections, 2026-09-04):**
- 0x575400 CONFIRMED `IsEquipped(refr, item)` — resolves equipment via 0x4BF220 and
  tests presence via 0x4BFDA0(item, 0); guarded by 0x55D310 (container non-null check).
- 0x8248E0(item, 1) is RemoveItem's equipped-entry teardown loop: walks a linked list
  (vtable+0x8) and calls 0x804210(flag) per matching node — the OnUnequip/effect path
  lives below 0x804210; that is the next trace hop for the fix design.
- 0x4CE340 is a THIN WRAPPER → 0x4CE380 (the real bulk primitive; next hop).
- **0x4CE380 CLOSED (2026-09-04):** the 6,816-byte inventory-removal core (48 callees)
  contains NO unequip machinery in its callee set (no 0x575400 / 0x8248E0 / 0x4BFDA0).
  Its caller set includes 0x5B5690 (RemoveAllItems exec slot). Therefore: the bulk
  primitive never unequips internally; RemoveItem (0x5B4E90) compensates by pre-running
  IsEquipped→teardown, and the bulk handlers do not. Root cause is the ABSENCE of the
  single-item pre-pass at the bulk call sites, not corruption inside 0x4CE380.
- **Fix site decision:** patching the call sites (0x5B5690 / 0x5B55A0) to route equipped
  entries through the 0x575400→0x8248E0 sequence first is safer than editing 0x4CE380,
  which has three callers including engine paths (0x54B5B0) that may legitimately skip
  unequipping. An NVSE-plugin approach (stewie-style) can hook the two console execs.
- 0x41AB70 is NOT the unequip core — it toggles an extra-data/type-0x3E marker
  (0x40FE80/0x410140/0x40FF60 family, cf. the encounter-zone extra work). Correction to
  the earlier note above.
- SayToDone: 0x5CA950 exec → resolver 0x5ACCB0 + 0x5CA1C0; 0x5CA1C0 is only a
  topic/speaker availability predicate (returns 1.0f/0.0f). The speech-completion event
  firing mechanism is still un-anchored — next hop is what consumes the script event
  queue (search for the 'DoneTalking'/Say topic completion strings and the audio
  conversation owner class).

**Runtime verification owed (BUG-003 family):** craft an armor with a measurable
OnUnequip block + a permanent magic effect, equip it on the player, then RemoveAllItems;
assert the OnUnequip block never fires and the effect remains. After a patch mirroring
the 0x575400→0x8248E0→0x804210 teardown sequence, re-run the repro.

- All four command structs share layout: +0x0 name ptr, +0x4 alt ptr (0x01011584 = empty),
  +0x8 id (0x10AD/0x1249/0x1052/0x10EF), +0xC help (empty), +0x10 params ptr, +0x14
  mod ptr (0x5B1BA0 for the three inventory commands; 0x5B1BA0 is shared).
- 0x5B1570 calls 0x5AF5F0 then a single 0x228-byte stack buffer path; 0x5B4E90 and
  0x5D0300 are the corresponding single-item handlers to compare against.
- **Retracted:** "0x5B1590 is an NVSE hook stub". The jump decoded at 0x5B1590 was a
  mid-prologue linear-decode artifact; the on-disk GOG exe is clean. Lesson recorded.
- **Retracted:** 0x44A670 is *not* the engine bulk-remove — it has 170 callers and only
  calls the CRT allocator 0xEC6130; it is an allocation helper (likely operator new).
- Open: find the shared engine remove/unequip core via 0x5D0300 and 0x5B4E90 callee
  diff vs 0x5B1570's bulk path.

### 3.4 Cluster anchors from the pass-3 sweep (2026-09-04)

| Bug | Anchor | Meaning |
|-----|--------|---------|
| BUG-009 | Setting 0x11CFD7C = iBallisticProjectilePathPickSegments (ctor 0xF5E41A); sole runtime reader **0x9A7141** | ballistic path picker for non-hitscan projectiles; water-impact decal branch expected in/near it |
| BUG-012 | SayTo exec **0x5C9100** (struct slot 0x1191130); SayToDone exec 0x5CA950; predicate 0x5CA1C0 | speech initiation → completion event chain |
| BUG-013 | EGM path build **0x6535A3** ('%s%s.egm' @0x6535B5, '%s.egm' @0x6535D7, race-dir table [edx*4+0x119B734]) | BSFaceGenManager loose/BSA resolution |
| BUG-013 (pass-3 CLOSED CHAIN) | decompiled FUN_00653520: strips extension, appends `.egm` (+ NoHat variant via table 0x119B734), then calls **FUN_004037f0(path, 0)** — that single callee is the archive-vs-loose file resolver; the BSA-only behavior lives inside it | next decompile hop |
| BUG-017 (vtable recovered) | ExtraSayTopicInfoOnceADay: TypeDescriptor 0x1185214 → COL 0x1105054 → vtable **0x1015F3C**; slots: dtor 0x4374E0, 0x8D0370, 0x10150A0, 0x41B680/0x40F700 (shared extra-data save/load, already in corpus); instantiated at 0x43747C / 0x43754C / 0x4375EB | constructor/consult sites |
| BUG-014 | 'Update Multibound Visibility' label push **0xF38B97** | multibound culling/visibility updater; ToggleMultiboundCheck cmd + bUseMultibounds ini for repro |
| BUG-015 | SetTalkingActivatorActor exec **0x5D4CC0** (struct slot 0x11942B8, id 0x1171) | talking-activator actor assignment |
| BUG-017 | RTTI TypeDescriptor '.?AVExtraSayTopicInfoOnceADay@@' @0x118521C (descriptor base 0x1185210) | say-once-a-day extra-data class; recover COL→vtable for methods |
| (support) | BGSImpactDataSet RTTI 0x11862E4; DefaultImpactDataSet str 0x1033374; BSMultiBound* RTTI 0x11885E4+; CheckWithinMultiBoundTask 0x118B6D4 | cluster identification aids |

### 3.5 Prior subsystem maps (do not re-derive)

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
