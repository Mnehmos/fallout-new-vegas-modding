# PerkOverhaul — Design Brief

## Mod Name: TBD (working title: "Perk Revival")
## Author: Mnehmos
## Target: FNV Base Game (DLC addons later)

---

## Goal

Every perk the player can take at level-up must feel like a meaningful choice.
No perk should be taken because "nothing else was useful."

### Success Criteria
- No perk is tier C or below after overhaul
- At least 15–20 perks are build-defining (S tier)
- Every build archetype has 3–5 "anchor" perks it orbits around
- New players can feel powerful quickly; veterans still have depth to explore

---

## Design Constraints

- Must be compatible with vanilla FNV.esm (patch ESP, not direct edit)
- NVSE required (JIP LN NVSE + JohnnyGuitar NVSE)
- Should not make the game trivially easy — power should feel earned
- Where possible, perks should reward specific playstyles, not just raw numbers

---

## Architecture of a "Build"

A good FNV build has:
1. **A weapon type** (cowboy guns, energy weapons, unarmed, etc.)
2. **A combat style** (stealth, VATS, aggressive, tanky)
3. **3–5 anchor perks** that synergize with both
4. **Support perks** that fill gaps

The overhaul should ensure every weapon type + style combination has at least 3 S-tier anchors.

---

## Release Plan

- v0.1 — Phase 1: Requirement tweaks + simple value buffs (FNVEdit only)
- v0.2 — Phase 2: Secondary effects on weak perks (GECK scripts)
- v0.3 — Phase 3: Full reworks on D-tier perks (GECK + NVSE)
- v1.0 — Full release with optional MCM configuration
