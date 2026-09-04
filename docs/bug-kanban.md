# Engine Bug Investigation Kanban

Tracking board for the GECKWiki "Engine Bugs (Fallout New Vegas)" RE effort.
Source of truth for per-bug detail: `docs/data/bugs.json` (IDs here match its `id` fields).
When a bug advances a column, update its `status`/`next` in bugs.json AND move it here.

Last updated: 2026-09-04 (session 3: 8 root-caused entries / 6 defects)

---

## DONE — verified & closed

| Bug | Title | Note |
|-----|-------|------|
| FNV-BUG-001 | VATS-targetable grenades always show 0% hit chance | FNVBug001Fix v4 runtime-verified in-session; v4 DLL installed. Owed: one post-restart verification that the xNVSE-loaded module owns the two patches and a queued grenade shot executes. |

## RE MAPPING — static analysis under way

| Bug | Title | Current state |
|-----|-------|---------------|
| FNV-BUG-009 | Ballistic projectiles ignore water impact decals | Ballistic path picker = sole reader 0x9A7141 of Setting 0x11CFD7C (iBallisticProjectilePathPickSegments); water-impact branch expected in/near it; pass-3 decompile queued |
| FNV-BUG-014 | Multibound culling flicker | 'Update Multibound Visibility' label push 0xF38B97 inside the culling fn; ToggleMultiboundCheck console cmd for runtime repro |
| FNV-BUG-015 | Talking activators no attenuation | SetTalkingActivatorActor exec 0x5D4CC0; trace forward into dialogue audio consumption |
| FNV-BUG-017 | Once a Day flag inconsistent | Class fully identified: extra type 0x73, ctors 0x437440/0x437510, vtable 0x1015F3C, per-day heap obj +0xC; consult site = GetExtraData(0x73) consumers, next |
| FNV-BUG-005 | Leveled actor template bias | PlaceLeveledActorAtMe exec 0x5D9810; leveling settings cluster @0x1016214+ |
| FNV-BUG-007 | CAUTION/combat stuck | '[CAUTION]' state code @0xF6F0C3 |
| FNV-BUG-011 | Loop sounds survive transitions | ExtraActivateLoopSound vtable 0x1015F18 recovered |
| FNV-BUG-019 | Aggro radius suppresses packages | Violation check @0x5A4FF2 with debug strings |
| FNV-BUG-030 | Disabled loop-sound objects play | Shares ExtraActivateLoopSound with BUG-011 |
| FNV-BUG-006 | AI off-screen package processing | ExtraProcessMiddleLow TD @0x1183C64 - the process-level extra itself |

## RESEARCH IN FLIGHT — 4 web-research batches (all 29 open bugs covered)

| Batch | Bugs | Scope |
|-------|------|-------|
| A: inventory/scripting | 002, 003, 004, 008, 028, 029 | + deliverable: locate the community FNV address library / symbol DB |
| B: AI/packages | 005, 006, 007, 016, 017, 018, 019 | process levels, package scheduler, combat-state aggregate |
| C: world/physics/render | 009, 010, 014, 020, 021, 022, 026 | Havok bounds, restitution, multibounds, ballistic decals |
| D: audio/dialogue/combat/assets | 011, 012, 013, 015, 023, 024, 025, 027, 030 | SayToDone, Stonewall, StartCombatResponse, looping sounds, EGM |

On completion: merge findings into each bug's entry in `docs/data/bugs.json` (new fields:
`research` summary, candidate RE entry points, community-fix references), then move bugs
from this column to BACKLOG-for-RE or straight to RE MAPPING if a site address is known.

## BACKLOG FOR RE — researched, awaiting static analysis

_(empty — fills as research batches land; expected early RE targets: BUG-002 (address in hand),
BUG-003/028/029 (NVSE command-table strings lead straight to handlers), BUG-024 (perk entry point).)_

## ROOT CAUSE CONFIRMED

| FNV-BUG-004 | NPC enchant stacking on load | Equip handler FUN_008c48d0 has type-only gates (form 6, enchant cast, +0x34==2) and NO active-effect dedupe; NPC load re-runs equip path | Runtime stack-count repro; dedupe patch prototype |
| FNV-BUG-006 | Off-screen AI package stall | MiddleLow migration FUN_0092ca70 is 9 lines vs 177-line MiddleHigh sibling - state dropped on re-bucket | Runtime package timestamps; extended-migration patch |

| Bug | Title | Evidence | Outstanding for FIX SHIPPED |
|-----|-------|----------|------------------------------|
| FNV-BUG-002 | iSneakLevelBonus can invert the sneak modifier | Ghidra C line `(max-clamped sibling) + (L2−L1)*iSneakLevelBonus` unclamped signed term in FUN_00642ed0 (0x642ED0); all 8 settings bound; caller arg map complete | Runtime A/B for sign direction; clamp-patch design; plugin build |
| FNV-BUG-003 | RemoveAllItems skips unequip lifecycle | Bulk handler 0x5B55A0 calls 0x4CE340 directly; single-item 0x5B4E90 proves the missing IsEquipped(0x575400)→unequip(0x8248E0)→vtable+0x17C sequence; decompiled C for all four handlers | Runtime repro (scripted armor + OnUnequip); patch prototype |

| FNV-BUG-012 | SayToDone fails off-cell | Completion marker FUN_00579160 works but is a table callback (0x102F69C) dispatched only on the processed-speaker path; SayTo exec gates on vtable+0x22C | Two-cell repro; vtable+0x22C identity; hook prototype |
| FNV-BUG-027 | Hit-bark sounds have no cooldown | Combat-dialogue processor FUN_009839b0 switch arms 0/1/3/4/5 only — no case 2 (hit), no Hit GMST exists; only a global 1500ms gate | Bark-count repro; case-2 cooldown patch |

Shared-mechanism siblings: FNV-BUG-028 and FNV-BUG-029 share the BUG-003 root cause.

## FIX SHIPPED

_(empty — BUG-001 fix lives in `mcp/debugger/FNVBug001Fix.cpp`)_

---

## Working conventions

- **Definition of done (column exits):** RE MAPPING → ROOT CAUSE requires a confirmed,
  instruction-level causal story backed by disassembly addresses (hypothesis + evidence),
  not just a plausible read. ROOT CAUSE → FIX SHIPPED requires a minimal patch design
  (NVSE plugin detour or data redirect) following the BUG-001 pattern. FIX SHIPPED → DONE
  requires in-game verification and a bugs.json `fix_verified` note.
- Record every falsified hypothesis in the bug's `falsification_trail` (bugs.json) —
  see FNV-BUG-001 for the format.
- RE binary: GOG FalloutNV.exe (see glossary). Never analyze the packed Steam exe statically.
- Wiki re-sync: live page "Bugs remaining" matched bugs.json 1:1 on 2026-09-04 (30 items,
  BUG-001 closed). Re-check if geckwiki updates.
