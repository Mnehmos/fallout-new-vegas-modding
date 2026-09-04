# Engine Bug Investigation Kanban

Tracking board for the GECKWiki "Engine Bugs (Fallout New Vegas)" RE effort.
Source of truth for per-bug detail: `docs/data/bugs.json` (IDs here match its `id` fields).
When a bug advances a column, update its `status`/`next` in bugs.json AND move it here.

Last updated: 2026-09-04

---

## DONE — verified & closed

| Bug | Title | Note |
|-----|-------|------|
| FNV-BUG-001 | VATS-targetable grenades always show 0% hit chance | FNVBug001Fix v4 runtime-verified in-session; v4 DLL installed. Owed: one post-restart verification that the xNVSE-loaded module owns the two patches and a queued grenade shot executes. |

## RE MAPPING — static analysis under way

| Bug | Title | Current state |
|-----|-------|---------------|
| FNV-BUG-002 | iSneakLevelBonus can invert the sneak modifier | Bug site pinned: unclamped signed term `(arg24 − arg23) × iSneakLevelBonus` @ 0x642F10–0x642F1C in the detection accumulator 0x642ED0; all 8 gamesettings named; two candidate patches (operand swap vs clamp). Remaining: bind arg23/arg24 to player/actor levels via caller push-map, then runtime A/B. See glossary 3.1. |

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

_(empty)_

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
