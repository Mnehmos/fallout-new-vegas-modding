# Fallout New Vegas — Complete Modding Surface Map

## 465,016 records across 88 record types

### Status Key
- **PROVEN** = We've built and shipped mods using this record type
- **READY** = We can read, modify, and write — untested in-game
- **PARTIAL** = Can read and modify some fields, not all
- **READ-ONLY** = Can read and analyze but can't write reliably
- **BLOCKED** = Requires GECK, NVSE scripting, or unsolved binary format issues

---

## Items & Equipment

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| WEAP | Weapon | 261 | All weapon stats, models, sounds, mods | Clone, modify DMG/crit/rate/AP/spread/clip/proj count | **PROVEN** |
| ARMO | Armor | 389 | Armor DT, weight, value, enchantments | Clone, modify DT/value/weight, link ENCH | **PROVEN** |
| AMMO | Ammunition | 92 | Ammo damage mult, DT bypass, weight, value | Read + modify via xEdit | **READY** |
| ALCH | Ingestibles | 189 | Food, drink, chems, stimpaks — healing, duration, addiction | Read + modify magnitude/duration | **READY** |
| MISC | Misc Items | 507 | Junk, components, quest items | Clone + modify | **READY** |
| KEYM | Keys | 283 | Keys for locks and doors | Read | **READ-ONLY** |
| BOOK | Books | 27 | Skill books, readable books | Clone + modify text | **READY** |
| NOTE | Notes/Holotapes | 894 | Note text (TNAM field), holotape audio | Clone + modify TNAM | **PROVEN** |
| IMOD | Weapon Mods | 50 | Suppressors, scopes, extended mags | Read; linking to WEAP WMI fields needs testing | **PARTIAL** |
| INGR | Ingredients | 1 | Crafting ingredient (unused in FNV) | N/A | N/A |

## Characters & Creatures

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| NPC_ | NPC | 3,816 | Stats, appearance, factions, inventory, AI, dialogue | Read all stats; override via xEdit; clone partially | **PARTIAL** |
| CREA | Creature | 1,578 | Creature stats, aggression, abilities, XP | Read + XP boost via xEdit | **PROVEN** |
| LVLN | Leveled NPC | 365 | NPC spawn pools, count, level scaling | Boost counts, CalcEach flag | **PROVEN** |
| LVLC | Leveled Creature | 343 | Creature spawn pools, count, level scaling | Boost counts, CalcEach flag | **PROVEN** |
| RACE | Race | 22 | Race stats, body data, abilities | Read | **READ-ONLY** |
| CLAS | Class | 74 | NPC class (stat weights, tag skills) | Read + modify | **READY** |
| HAIR | Hair | 67 | Hair models | Read | **READ-ONLY** |
| EYES | Eyes | 12 | Eye textures | Read | **READ-ONLY** |
| HDPT | Head Part | 61 | Facial features | Read | **READ-ONLY** |
| VTYP | Voice Type | 100 | Voice type assignments | Read | **READ-ONLY** |
| BPTD | Body Part Data | 49 | Limb health, dismemberment | Read | **PARTIAL** |

## World & Placement

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| WRLD | Worldspace | 232,553 | Worldspace definitions + all placed refs | Read all; exterior REFR placement via clone+retarget | **PROVEN** |
| CELL | Cell | 146,361 | Interior/exterior cell definitions | Read; override causes crashes on complex cells | **PARTIAL** |
| REFR | Placed Object | (in WRLD/CELL) | Objects placed in the world | Clone existing REFR + retarget Cell ownership | **PROVEN** (with limitations) |
| ACHR | Placed NPC | (in WRLD/CELL) | NPCs placed in the world | Clone causes cell crashes; needs more research | **BLOCKED** |
| ACRE | Placed Creature | (in WRLD/CELL) | Creatures placed in the world | Untested; likely same issues as ACHR | **BLOCKED** |
| NAVM | NavMesh | (in CELL) | NPC pathfinding geometry | Cannot create; would need procedural generation | **BLOCKED** |
| LAND | Landscape | (in WRLD) | Terrain heightmap, texture layers | Read-only; modification is GECK territory | **BLOCKED** |
| NAVI | Navigation Info | 1 | Global navigation data | Read-only | **BLOCKED** |
| STAT | Static Object | 6,785 | Non-interactable geometry (walls, rocks, etc.) | Read; used as base objects for REFR placement | **READY** |
| FURN | Furniture | 234 | Sittable/usable objects | Read; placeable as REFR | **READY** |
| DOOR | Door | 320 | Doors with teleport destinations | Read; XTEL linking needs testing | **PARTIAL** |
| TREE | Tree | 3 | Tree objects | Read | **READ-ONLY** |
| GRAS | Grass | 24 | Grass definitions | Read | **READ-ONLY** |
| LIGH | Light | 501 | Light sources | Read; placeable as REFR | **READY** |
| ACTI | Activator | 1,143 | Switches, buttons, triggers | Read; placeable as REFR | **READY** |
| TACT | Talking Activator | 87 | Radio speakers, intercoms | Read | **PARTIAL** |
| CONT | Container | 2,478 | Containers with inventory (CNTO) | Clone + add CNTO entries + place as REFR | **PROVEN** |
| MSTT | Moveable Static | 241 | Physics-enabled statics | Read | **READY** |
| PWAT | Placeable Water | 29 | Water planes | Read | **READ-ONLY** |
| SCOL | Static Collection | 98 | Grouped statics | Read | **READ-ONLY** |

## Quests & Dialogue

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| QUST | Quest | 436 | Quest stages, objectives, scripts | Create basic quest records (stages need GECK for triggers) | **PARTIAL** |
| DIAL | Dialogue Topic | 41,462 | Dialogue topics (greeting, topic, combat, etc.) | Create records; linking to NPCs needs GECK conditions | **PARTIAL** |
| INFO | Dialogue Response | (in DIAL) | Individual dialogue lines, conditions, links | Create records; conditions/scripts need GECK | **PARTIAL** |
| PACK | AI Package | 4,163 | NPC schedules, patrol routes, behaviors | Read; creation needs GECK | **BLOCKED** |
| IDLE | Idle Animation | 1,597 | Animation assignments | Read | **READ-ONLY** |
| IDLM | Idle Marker | 211 | Places NPCs idle at | Read | **READ-ONLY** |

## Magic & Effects

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| ENCH | Enchantment | 145 | Armor/weapon enchantments | Create + link to ARMO via EITM | **PROVEN** |
| SPEL | Spell/Ability | 270 | Abilities, permanent effects | Read + modify magnitude (for PERK abilities) | **PROVEN** |
| MGEF | Magic Effect | 289 | Base effect types (Increase PER, etc.) | Read; used as references by ENCH/SPEL | **PROVEN** (as reference) |
| PERK | Perk | 176 | Player perks — level, ranks, conditions, effects | Full read/write: level, ranks, desc, EPFD floats, SPEL values | **PROVEN** |
| EXPL | Explosion | 154 | Explosion effects | Read | **PARTIAL** |
| PROJ | Projectile | 95 | Projectile definitions (bullets, beams, etc.) | Read | **PARTIAL** |
| EFSH | Effect Shader | 35 | Visual effects on actors | Read | **READ-ONLY** |

## Economy & Crafting

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| LVLI | Leveled Item | 2,738 | Loot tables, vendor inventory | Add entries, modify counts | **PROVEN** |
| RCPE | Recipe | 105 | Crafting recipes (workbench, reloading bench, campfire) | Read + modify | **READY** |
| RCCT | Recipe Category | 10 | Recipe categories | Read | **READ-ONLY** |
| CSNO | Casino | 5 | Casino rules, payout, ban threshold | Full read/write: max winnings, payout ratio, decks | **PROVEN** |
| CHIP | Casino Chip | 5 | Chip currency definitions | Read | **READ-ONLY** |
| CCRD | Caravan Card | 270 | Caravan deck cards | Read | **PARTIAL** |
| CDCK | Caravan Deck | 13 | Caravan deck definitions | Read | **PARTIAL** |
| CMNY | Currency | 6 | Currency types | Read | **READ-ONLY** |
| REPU | Reputation | 13 | Faction reputation thresholds | Read + modify | **READY** |

## Scripting & Logic

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| SCPT | Script | 2,576 | Game scripts (compiled) | Read; cannot compile new scripts without GECK | **BLOCKED** |
| GLOB | Global Variable | 218 | Global game variables | Read + modify values | **READY** |
| GMST | Game Setting | 648 | Engine settings (XP rates, carry weight, timescale, etc.) | Read + modify | **READY** |
| FLST | Form List | 464 | Lists of FormIDs used by scripts/conditions | Read + modify | **READY** |
| CHAL | Challenge | 105 | Challenges (kill X, discover Y) | Read + modify | **READY** |
| AVIF | Actor Value Info | 64 | SPECIAL/skill definitions | Read | **READ-ONLY** |
| MESG | Message | 1,144 | UI messages, popups, tutorials | Read + modify text | **READY** |

## Environment & Atmosphere

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| WTHR | Weather | 63 | Weather types (fog, rain, clear, radiation) | Read + modify colors/density/wind | **READY** |
| CLMT | Climate | 31 | Climate zones (weather probability, sun position) | Read + modify | **READY** |
| REGN | Region | 276 | Map regions (weather, sound, grass assignment) | Read | **PARTIAL** |
| WATR | Water | 78 | Water properties (color, opacity, damage) | Read + modify | **READY** |
| IMGS | Image Space | 67 | Screen color grading, saturation, contrast | Read + modify | **READY** |
| IMAD | Image Space Modifier | 215 | Screen effects (blur, pulse, fade) | Read | **PARTIAL** |
| LGTM | Lighting Template | 31 | Interior cell lighting presets | Read | **PARTIAL** |
| LSCR | Load Screen | 208 | Loading screen images and tips | Read + modify text | **READY** |

## Audio

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| SOUN | Sound | 3,190 | Sound effect definitions | Read; WAV file placement for voice | **PROVEN** (TTS pipeline) |
| MUSC | Music | 20 | Music track assignments | Read | **PARTIAL** |
| ASPC | Acoustic Space | 113 | Reverb/echo settings for cells | Read | **READ-ONLY** |
| ALOC | Audio Location | 89 | Where sounds play | Read | **READ-ONLY** |
| MSET | Music Set | 140 | Music playlists | Read | **PARTIAL** |

## Visual & Models

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| TXST | Texture Set | 493 | Texture assignments | Read | **READ-ONLY** |
| LTEX | Landscape Texture | 89 | Terrain texture assignments | Read | **READ-ONLY** |
| ARMA | Armor Addon | 131 | Armor model parts (1st/3rd person) | Read | **READ-ONLY** |
| ANIO | Animated Object | 152 | Animation assignments for objects | Read | **READ-ONLY** |
| CAMS | Camera Shot | 276 | VATS camera angles | Read | **PARTIAL** |
| DEBR | Debris | 6 | Destruction debris models | Read | **READ-ONLY** |
| RGDL | Ragdoll | 38 | Ragdoll physics settings | Read | **READ-ONLY** |
| CPTH | Camera Path | 418 | Cinematic camera paths | Read | **READ-ONLY** |

## Combat & AI

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| CSTY | Combat Style | 84 | NPC combat behavior (aggressive, cautious, etc.) | Read + modify | **READY** |
| FACT | Faction | 682 | Faction definitions, relations, crime settings | Read; creation needs testing | **PARTIAL** |
| ECZN | Encounter Zone | 17 | Area difficulty scaling | Read + modify level ranges | **READY** |
| IPCT | Impact | 125 | Bullet impact effects | Read | **READ-ONLY** |
| IPDS | Impact Dataset | 60 | Impact effect assignments by material | Read | **READ-ONLY** |
| ADDN | Addon Node | 37 | VFX attachment points | Read | **READ-ONLY** |

## FNV-Specific

| Record | Name | Count | What It Controls | Modding Capability | Status |
|--------|------|-------|-----------------|-------------------|--------|
| DEHY | Dehydration | 5 | Hardcore dehydration stages | Read + modify | **READY** |
| HUNG | Hunger | 5 | Hardcore hunger stages | Read + modify | **READY** |
| SLPD | Sleep Deprivation | 5 | Hardcore sleep stages | Read + modify | **READY** |
| RADS | Radiation Stage | 5 | Radiation sickness thresholds | Read + modify | **READY** |
| AMEF | Ammo Effect | 54 | Special ammo effects (AP, HP, explosive) | Read + modify | **READY** |
| TERM | Terminal | 344 | Hackable terminals (text, options, scripts) | Read text; script linkage needs GECK | **PARTIAL** |
| MICN | Menu Icon | 12 | Pip-Boy menu icons | Read | **READ-ONLY** |
| DOBJ | Default Object | 1 | Default object manager | Read | **READ-ONLY** |

---

## Summary by Capability

| Status | Record Types | Count | What We Can Do |
|--------|-------------|-------|----------------|
| **PROVEN** | WEAP, ARMO, NOTE, CONT, ENCH, SPEL, MGEF, PERK, LVLC, LVLN, LVLI, CSNO, CREA, WRLD/REFR, SOUN/TTS | 15 | Full create/modify/place pipeline |
| **READY** | AMMO, ALCH, MISC, BOOK, STAT, FURN, LIGH, ACTI, GLOB, GMST, FLST, CHAL, MESG, WTHR, CLMT, WATR, IMGS, RCPE, REPU, CSTY, ECZN, DEHY, HUNG, SLPD, RADS, AMEF, CLAS, LSCR, MSTT | 29 | Can modify but haven't shipped a mod with these |
| **PARTIAL** | NPC_, QUST, DIAL, INFO, IMOD, FACT, BPTD, DOOR, TACT, REGN, IMAD, LGTM, TERM, PROJ, EXPL, MUSC, MSET, CAMS, CCRD, CDCK | 20 | Can read/partially modify, some fields need GECK |
| **READ-ONLY** | RACE, HAIR, EYES, HDPT, VTYP, KEYM, TREE, GRAS, PWAT, SCOL, IDLE, IDLM, ANIO, TXST, LTEX, ARMA, ASPC, ALOC, DEBR, RGDL, CPTH, EFSH, IPCT, IPDS, ADDN, RCCT, CHIP, CMNY, MICN, DOBJ, LSCT, AVIF | 32 | Can read and analyze only |
| **BLOCKED** | SCPT, PACK, ACHR/ACRE placement, NAVM, LAND, NAVI, CELL override | 7 | Requires GECK, NVSE, or unsolved format issues |

### What We Can Build Reliably Today: 44 record types
### What We'll Be Able To Build Soon: 64 record types (adding PARTIAL)
### What Needs GECK Forever: 7 record types (scripts, AI packages, navmesh, landscape)
