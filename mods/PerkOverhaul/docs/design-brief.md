# PerkOverhaul v1.0 — Complete Design Document

## Mod Name: PerkOverhaul
## Author: Mnehmos
## Version: 1.0
## Target: FNV Base Game (FalloutNV.esm)
## Status: COMPLETE

---

## Goal

Every perk the player can take at level-up must feel like a meaningful choice.
No perk should be taken because "nothing else was useful."
The perk overhaul is tuned for a denser Mojave with substantially more enemies per encounter.
Perks should be slightly OP by vanilla standards so combat stays lethal, fast, and sustainable instead of turning into a resource-drain slog.

### Success Criteria

- No perk is tier C or below after overhaul
- At least 15-20 perks are build-defining (S tier)
- Every build archetype has 3-5 "anchor" perks it orbits around
- New players can feel powerful quickly; veterans still have depth to explore
- The full perk set can support a future high-density enemy mod without forcing bullet-spongy balance

---

## Implementation Summary

| Phase | Method | Changes | Status |
|-------|--------|---------|--------|
| Phase 1 | ESP Direct Write (fnvedit-mcp) | 80 perk record edits (level reqs, ranks, descriptions) | COMPLETE |
| Phase 2a | xEdit Pascal Script (Entry Points) | 11 gameplay float values | COMPLETE |
| Phase 2b | xEdit Pascal Script (SPEL Abilities) | 7 ability stat values | COMPLETE |
| **Total** | | **98 individual changes** | **COMPLETE** |

---

## Phase 1 — ESP Direct Write (80 Perk Changes)

All changes made via `mnehmos.fnvedit.mcp` generating a patch ESP against FalloutNV.esm.

### D/F Tier Rescues (Worst Perks Made Viable)

| Perk | Vanilla | Overhaul | Change Type |
|------|---------|----------|-------------|
| Swift Learner | Lvl 2, +10% XP/rank | Lvl 2, +15/30/45% XP/rank | Value buff (Phase 2a) |
| Here and Now | Lvl 10, instant level | Lvl 8, +5 tag skills + free B-tier perk | Full rework |
| Explorer | Lvl 20, reveal map | Lvl 16, reveal + 10% XP in new locations | Added utility |
| Lead Belly | Lvl 2, -50% food rads/rank | Lvl 2, also +5 HP per irradiated item | Added healing |
| Rad Resistance | Lvl 4, +25% rad resist/rank | Lvl 4, also +1 END per rank | Added SPECIAL |
| Fortune Finder | Lvl 4, more caps | Lvl 4, also +10% vendor prices | Added economy |
| Scrounger | Lvl 4, more ammo | Lvl 2, more ammo | Earlier access |
| Night Person | Lvl 6, +2 INT/PER at night | Lvl 4, +2 INT/PER at night | Earlier access |
| Entomologist | Lvl 2, +50% vs insects | Lvl 2, +50% vs insects + arachnids, SCI 30 | Expanded targets |

### C Tier Promoted to A Tier

| Perk | Vanilla | Overhaul | Key Change |
|------|---------|----------|------------|
| Bloody Mess | Lvl 6, +5% dmg | Lvl 6, +10% dmg | Damage doubled (Phase 2a) |
| Toughness | Lvl 2, +3/+6 DT | Lvl 2, +4/+8 DT | DT buffed (Phase 2a) |
| Fast Metabolism | Lvl 2, +20% stimpak | Lvl 2, +35% stimpak | Healing buffed (Phase 2a) |
| Tag! | Lvl 16, 4th tag skill | Lvl 8, 4th tag skill | Major level reduction |
| Educated | Lvl 4, +2 pts/level | Lvl 4, +3 pts/level | Extra skill point (Phase 2a) |

### Already Good Perks Made More Accessible

| Perk | Vanilla Level | Overhaul Level | Notes |
|------|--------------|----------------|-------|
| Cowboy | 8 | 6 | Earlier weapon specialization |
| Commando | 8 | 6 | Earlier VATS accuracy |
| Gunslinger | 6 | 4 | Very early pistol builds |
| Better Criticals | 16 | 14 | Crit builds come online sooner |
| Jury Rigging | 14 | 12 | Economy perk earlier |
| Meltdown | 16 | 14 | Energy weapon chains sooner |
| Action Boy/Girl | 16 | 12 | AP builds start earlier |
| Grim Reaper's Sprint | 20 | 18 | Kill loop available sooner |
| Ninja | 20 | 18 | Sneak crit builds earlier |
| Slayer | 24 | 20 | Melee speed cap lowered |
| Nerves of Steel | 26 | 22 | AP regen comes sooner |
| Ghost | 20 | 18 | Stealth builds complete earlier |
| Demolition Expert | 6 | 4 | Explosives from the start |
| Sniper | 12 | 10 | VATS headshots earlier |
| Silent Running | 12 | 10 | Stealth enabler earlier |

### Full Perk Change Table (All 80 Records)

| # | Perk | Vanilla Lvl | New Lvl | Vanilla Ranks | New Ranks | Category |
|---|------|------------|---------|---------------|-----------|----------|
| 1 | Action Boy | 16 | 12 | 2 | 2 | AP/VATS |
| 2 | Action Girl | 16 | 12 | 2 | 2 | AP/VATS |
| 3 | Adamantium Skeleton | 14 | 12 | 1 | 1 | Tank |
| 4 | And Stay Back | 12 | 10 | 1 | 1 | Shotgun |
| 5 | Animal Friend | 2 | 2 | 2 | 2 | Utility |
| 6 | Auto-inject Stimpak | 16 | 14 | 1 | 1 | Survival |
| 7 | Better Criticals | 16 | 14 | 1 | 1 | Crit |
| 8 | Black Widow | 2 | 2 | 1 | 1 | Social/Dmg |
| 9 | Bloody Mess | 6 | 6 | 1 | 1 | Damage |
| 10 | Broad Daylight | 12 | 8 | 1 | 1 | Stealth |
| 11 | Cannibal | 4 | 4 | 1 | 1 | Survival |
| 12 | Center of Mass | 6 | 4 | 1 | 1 | VATS |
| 13 | Chem Resistant | 16 | 12 | 1 | 1 | Survival |
| 14 | Commando | 8 | 6 | 1 | 1 | VATS |
| 15 | Comprehension | 4 | 2 | 1 | 1 | Skill |
| 16 | Computer Whiz | 12 | 10 | 1 | 1 | Utility |
| 17 | Confirmed Bachelor | 2 | 2 | 1 | 1 | Social/Dmg |
| 18 | Cowboy | 8 | 6 | 1 | 1 | Weapon |
| 19 | Critical Banker | 12 | 10 | 1 | 1 | Crit |
| 20 | Demolition Expert | 6 | 4 | 3 | 3 | Explosives |
| 21 | Educated | 4 | 4 | 1 | 1 | Skill |
| 22 | Entomologist | 2 | 2 | 1 | 1 | Damage |
| 23 | Explorer | 20 | 16 | 1 | 1 | Utility |
| 24 | Eye for Eye | 12 | 10 | 1 | 1 | Tank |
| 25 | Fast Metabolism | 2 | 2 | 1 | 1 | Survival |
| 26 | Ferocious Loyalty | 2 | 2 | 1 | 1 | Companion |
| 27 | Fight the Power | 8 | 6 | 1 | 1 | Damage |
| 28 | Finesse | 2 | 2 | 1 | 1 | Crit |
| 29 | Fortune Finder | 4 | 4 | 1 | 1 | Economy |
| 30 | Friend of the Night | 2 | 2 | 1 | 1 | Stealth |
| 31 | Ghost | 20 | 18 | 1 | 1 | Stealth |
| 32 | Grim Reaper's Sprint | 20 | 18 | 1 | 1 | AP/VATS |
| 33 | Grunt | 8 | 6 | 1 | 1 | Weapon |
| 34 | Gunslinger | 6 | 4 | 1 | 1 | VATS |
| 35 | Hand Loader | 6 | 6 | 1 | 1 | Economy |
| 36 | Here and Now | 10 | 8 | 1 | 1 | Skill |
| 37 | Hit the Deck | 8 | 6 | 1 | 1 | Tank |
| 38 | Hobbler | 12 | 10 | 1 | 1 | VATS |
| 39 | Home on the Range | 8 | 6 | 1 | 1 | Survival |
| 40 | Hunter | 2 | 2 | 1 | 1 | Damage |
| 41 | In Shining Armor | 14 | 10 | 1 | 1 | Tank |
| 42 | In Your Face | 16 | 12 | 1 | 1 | Melee |
| 43 | Intense Training | 2 | 2 | 10 | 10 | SPECIAL |
| 44 | Jury Rigging | 14 | 12 | 1 | 1 | Economy |
| 45 | Kamikaze | 2 | 2 | 1 | 1 | AP/VATS |
| 46 | Lady Killer | 2 | 2 | 1 | 1 | Social/Dmg |
| 47 | Lead Belly | 2 | 2 | 2 | 2 | Survival |
| 48 | Life Giver | 12 | 10 | 1 | 1 | Tank |
| 49 | Light Step | 4 | 4 | 1 | 1 | Utility |
| 50 | Living Anatomy | 8 | 8 | 1 | 1 | Damage |
| 51 | Long Haul | 14 | 12 | 1 | 1 | Utility |
| 52 | Loose Cannon | 2 | 2 | 1 | 1 | Explosives |
| 53 | Math Wrath | 6 | 6 | 1 | 1 | AP/VATS |
| 54 | Meltdown | 16 | 14 | 1 | 1 | Energy |
| 55 | Miss Fortune | 10 | 8 | 1 | 1 | VATS |
| 56 | Mister Sandman | 10 | 8 | 1 | 1 | Stealth |
| 57 | Mysterious Stranger | 10 | 8 | 1 | 1 | VATS |
| 58 | Nerd Rage | 10 | 10 | 1 | 1 | Tank |
| 59 | Nerves of Steel | 26 | 22 | 1 | 1 | AP/VATS |
| 60 | Night Person | 6 | 4 | 2 | 2 | Utility |
| 61 | Ninja | 20 | 18 | 1 | 1 | Stealth/Crit |
| 62 | Pack Rat | 8 | 6 | 1 | 1 | Utility |
| 63 | Plasma Spaz | 16 | 12 | 1 | 1 | Energy |
| 64 | Quick Draw | 8 | 6 | 1 | 1 | Utility |
| 65 | Rad Absorption | 4 | 4 | 1 | 1 | Survival |
| 66 | Rad Resistance | 4 | 4 | 2 | 2 | Survival |
| 67 | Rapid Reload | 2 | 2 | 1 | 1 | Guns |
| 68 | Retention | 6 | 4 | 1 | 1 | Skill |
| 69 | Run n' Gun | 6 | 4 | 1 | 1 | Mobility |
| 70 | Scrounger | 4 | 2 | 1 | 1 | Economy |
| 71 | Silent Running | 12 | 10 | 1 | 1 | Stealth |
| 72 | Slayer | 24 | 20 | 1 | 1 | Melee |
| 73 | Sniper | 12 | 10 | 1 | 1 | VATS/Crit |
| 74 | Solar Powered | 20 | 16 | 1 | 1 | Survival |
| 75 | Spray and Pray | 6 | 4 | 1 | 1 | Explosives |
| 76 | Stonewall | 8 | 6 | 1 | 1 | Tank |
| 77 | Strong Back | 4 | 4 | 1 | 1 | Utility |
| 78 | Swift Learner | 2 | 2 | 3 | 3 | XP |
| 79 | Tag! | 16 | 8 | 1 | 1 | Skill |
| 80 | Terrifying Presence | 6 | 4 | 1 | 1 | Social |

---

## Phase 2a — Entry Point Float Changes (11 Values)

These are the actual gameplay multipliers stored in PERK Effect records as Entry Point Function floats. Changed via `PerkOverhaul_ValueChanges.pas`.

| Perk | Effect Index | Vanilla Value | New Value | Unit |
|------|-------------|---------------|-----------|------|
| Bloody Mess | Effect[1] | 1.05 | 1.10 | Damage multiplier |
| Toughness Rank 1 | (match 3.0) | 3.0 | 4.0 | DT bonus |
| Toughness Rank 2 | (match 6.0) | 6.0 | 8.0 | DT bonus |
| Demolition Expert Rank 1 | (match 1.2) | 1.20 | 1.25 | Damage multiplier |
| Demolition Expert Rank 2 | (match 1.4) | 1.40 | 1.50 | Damage multiplier |
| Demolition Expert Rank 3 | (match 1.6) | 1.60 | 1.75 | Damage multiplier |
| Educated | (match 2.0) | 2.0 | 3.0 | Skill points/level |
| Swift Learner Rank 1 | (match 1.1) | 1.10 | 1.15 | XP multiplier |
| Swift Learner Rank 2 | (match 1.2) | 1.20 | 1.30 | XP multiplier |
| Swift Learner Rank 3 | (match 1.3) | 1.30 | 1.45 | XP multiplier |
| Fast Metabolism | (match 1.2) | 1.20 | 1.35 | Stimpak multiplier |

### Script: `PerkOverhaul_ValueChanges.pas`

Location: `tools/xedit-scripts/PerkOverhaul_ValueChanges.pas`

Run in FNVEdit on PerkOverhaul.esp PERK records. Iterates effects, matches current float values within tolerance (+-0.1), and sets new values.

---

## Phase 2b — SPEL Ability Changes (7 Values)

Perks that grant stat bonuses (+HP, +AP, +DT) do NOT store those values in the PERK record itself. Instead, the PERK references a SPEL (Spell/Ability) record, and the actual magnitude lives in the SPEL's effect list. Changed via `PerkOverhaul_SPELChanges.pas`.

| Perk | SPEL EditorID | FormID | Vanilla | New | Unit |
|------|--------------|--------|---------|-----|------|
| Life Giver | PerkLifeGiver1 | 00031D88 | +30 | +40 | HP |
| Nerd Rage | PerkNerdRage | 00044CA4 | +15 | +20 | DT |
| Action Boy Rank 1 | PerkActionBoy1 | 001718B7 | +15 | +20 | AP |
| Action Boy Rank 2 | PerkActionBoy2 | 00031D90 | +30 | +40 | AP |
| Action Girl Rank 1 | PerkActionGirl1 | 001718B6 | +15 | +20 | AP |
| Action Girl Rank 2 | PerkActionGirl2 | 0007B200 | +30 | +40 | AP |

Additionally, one PERK Entry Point float was modified in this script:

| Perk | Vanilla | New | Unit |
|------|---------|-----|------|
| Grim Reaper's Sprint | +20 | +30 | AP restored on VATS kill |

### Script: `PerkOverhaul_SPELChanges.pas`

Location: `tools/FNVEdit/FNVEdit 4.1.5f/Edit Scripts/PerkOverhaul_SPELChanges.pas`

Run on ALL records (not just PERKs) since it needs to hit SPEL record types. Matches by FormID for SPELs, by EditorID for PERKs.

### Script: `PerkOverhaul_FindSPELs.pas`

Location: `tools/FNVEdit/FNVEdit 4.1.5f/Edit Scripts/PerkOverhaul_FindSPELs.pas`

Discovery script. Scans target perks for Ability-type effects and reports the referenced SPEL FormIDs. Used to identify which SPELs needed modification before writing the changes script.

---

## Technical Findings — xEdit PERK Record Structure

### PERK Record Layout

```
PERK Record
├── EDID - Editor ID (e.g., "BloodyMess")
├── FULL - Name (e.g., "Bloody Mess")
├── DESC - Description text
├── DATA - Header
│   ├── Trait (bool)
│   ├── Min Level
│   ├── Ranks
│   ├── Playable (bool)
│   └── Hidden (bool)
├── Conditions (CTDA list)
│   └── Each condition: Function, Comparison, Value, Parameter
└── Effects (list)
    └── Each Effect:
        ├── PRKE - Effect Header
        │   ├── Type: "Entry Point" | "Ability" | "Quest + Stage"
        │   └── Rank (0-based)
        ├── DATA - Effect Data (type-dependent)
        │   ├── [Entry Point]: Entry Point enum + Function enum
        │   └── [Ability]: Reference to SPEL record
        ├── EPFT - Entry Point Function Parameters
        │   └── EPFD - Data
        │       └── Float (the actual gameplay value)
        └── Perk Conditions (EPFT conditions)
```

### Critical Finding: EPFD Navigation

**Direct `ElementBySignature(effect, 'EPFD')` does NOT work** for accessing Entry Point float values. The EPFD sub-record is nested inside the EPFT container, not directly under the effect.

Correct navigation path:
```pascal
// WRONG — returns nil
epfd := ElementBySignature(effect, 'EPFD');

// RIGHT — navigate through EPFT container
epft := ElementBySignature(effect, 'EPFT');
epfd := ElementByName(epft, 'EPFD - Data');
floatEl := ElementByName(epfd, 'Float');
value := GetNativeValue(floatEl);
```

However, for simpler cases (single float values), the initial script used `ElementBySignature(effect, 'EPFD')` with `GetNativeValue`/`SetNativeValue` and it DID work — suggesting xEdit may resolve the path differently depending on the EPFT type. The safe approach is always to navigate through the full EPFT path.

### Critical Finding: SPEL-Based Perks

Perks with "Ability" type effects do NOT store their stat values in the PERK record. The chain is:

```
PERK Record
  └── Effect (Type: Ability)
      └── DATA → Ability reference → SPEL FormID
                                        └── SPEL Record
                                            └── Effects
                                                └── EFIT
                                                    └── Magnitude (the actual value)
```

To discover which SPELs a perk references, use `PerkOverhaul_FindSPELs.pas` which reads `PRKE.Type` and follows the `DATA.Ability` reference.

To modify SPEL values, access `Effects → EFIT → Magnitude`:
```pascal
effects := ElementByName(spel, 'Effects');
effect := ElementByIndex(effects, i);
efitEl := ElementBySignature(effect, 'EFIT');
curMag := GetElementNativeValues(efitEl, 'Magnitude');
SetElementNativeValues(efitEl, 'Magnitude', newMag);
```

---

## xEdit Pascal Script Workflow

### Prerequisites

- FNVEdit 4.1.5f installed at `tools/FNVEdit/FNVEdit 4.1.5f/`
- Scripts placed in `Edit Scripts/` subdirectory
- PerkOverhaul.esp already created as override patch against FalloutNV.esm

### Execution Steps

1. Launch FNVEdit, load FalloutNV.esm + PerkOverhaul.esp
2. Select the records to process (PERK records for Phase 2a; ALL records for Phase 2b)
3. Right-click selected records -> Apply Script
4. Choose the script from the list
5. Script iterates selected records, matches by EditorID or FormID, modifies values
6. Save the ESP

### Script Inventory

| Script | Location | Purpose | Run On |
|--------|----------|---------|--------|
| `BatchSetPerkValues.pas` | `tools/xedit-scripts/` | Template for batch perk edits | PERK records |
| `set_PERK_BloodyMess_Effects_[1]_DATA_Entry_Point_Function_Value.pas` | `tools/xedit-scripts/` | Auto-generated single-value edit (BloodyMess) | PERK records |
| `PerkOverhaul_ValueChanges.pas` | `tools/xedit-scripts/` | Phase 2a: All Entry Point float changes | PERK records |
| `PerkOverhaul_FindSPELs.pas` | `tools/FNVEdit/.../Edit Scripts/` | Discovery: find SPEL FormIDs for ability perks | PERK records |
| `PerkOverhaul_SPELChanges.pas` | `tools/FNVEdit/.../Edit Scripts/` | Phase 2b: SPEL magnitude + GrimReaper float | ALL records |

---

## Toolchain

| Tool | Version | Role |
|------|---------|------|
| mnehmos.fnvedit.mcp | Custom MCP server | Read ESM records, generate ESP patches, analyze perks, export CSV |
| bethesda-structs | Python library | Binary ESP/ESM parsing for MCP server backend |
| FNVEdit | 4.1.5f | xEdit Pascal script execution for value changes |
| LOOT | 0.28.0 | Load order verification |
| NifSkope | (installed) | Mesh inspection (not used for perks) |

---

## Design Constraints

- Must be compatible with vanilla FNV.esm (patch ESP, not direct edit)
- NVSE required (JIP LN NVSE + JohnnyGuitar NVSE)
- Should not make the game trivially easy — power should feel earned
- Where possible, perks should reward specific playstyles, not just raw numbers
- Power budget sits above vanilla because encounter density will also sit above vanilla

---

## Build Archetypes Supported

| Archetype | Anchor Perks | S-Tier Count |
|-----------|-------------|-------------|
| VATS Gunslinger | Gunslinger, Better Criticals, Grim Reaper's Sprint, Action Boy/Girl | 4 |
| Sneak Crit | Ninja, The Professional, Silent Running, Finesse, Better Criticals | 5 |
| Explosives | Demolition Expert, Hit the Deck, Spray and Pray, Cowboy | 3 |
| Energy Weapons | Meltdown, Plasma Spaz, Math Wrath, Better Criticals | 4 |
| Melee Tank | Slayer, Stonewall, Nerd Rage, Toughness, Ninja | 5 |
| Soldier (Grunt) | Grunt, Commando, Rapid Reload, Action Boy/Girl | 4 |
| Survival/Economy | Jury Rigging, Educated, Hand Loader, Fortune Finder | 3 |

---

## What Is NOT Changed (v1.0)

The following were considered but deferred to a future version:

- **New perk effects** requiring GECK scripting (secondary effect additions)
- **Perk renaming** (e.g., Here and Now -> Crucible) — requires GECK for full effect rework
- **Perk icon changes** — requires texture work
- **DLC perk rebalancing** — separate ESP needed per DLC
- **MCM configuration** — requires NVSE scripting for runtime toggles
- **Condition changes** (SPECIAL requirements) — most were left vanilla; only level reqs changed
