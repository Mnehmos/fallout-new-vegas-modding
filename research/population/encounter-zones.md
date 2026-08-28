# Encounter Zone Research — Population Density Mod

## Key Areas for Population Overhaul

### Priority 1 — The Interstate Corridor (Highway 95 / Route 93)
The main artery of the Mojave. Should be the busiest road in the game.

**Current state:** Sparse. A few raider groups, some dead bodies, one or two caravans.
**Target state:** A living road. Caravans every 3–4 in-game hours. NCR patrols. Random travelers.

Spawn zones to create:
- Goodsprings → Primm stretch (Route 93 south)
- Primm → Nipton (survivors, powder gangers, NCR)
- Nipton → Boulder City (Legion scout territory bleeds west)
- Boulder City → New Vegas approach (NCR heavy presence)

### Priority 2 — The Contested Frontier (Nelson / Forlorn Hope)
**Current state:** Nelson has Legion, Forlorn Hope has NCR, nothing actually happens between them.
**Target state:** Active front line. Skirmishes happen. Patrols clash.

Battle event trigger:
- Every 48 in-game hours: roll for a Legion assault on Forlorn Hope
- Every 72 hours: roll for NCR counter-attack toward Nelson
- Winner takes no ground (preserve quest states) but leaves combat aftermath

### Priority 3 — The Wilderness (Crescent Canyon / Broc Flower Cave region)
**Current state:** Nearly empty in mid-map.
**Target state:** Active predator corridors. Nightstalker packs. Cazador migration routes.

### Priority 4 — The Strip Approaches (Freeside / NCR Sharecropper Farms)
**Current state:** Freeside is medium density. Farmland feels empty.
**Target state:** More desperate settlers near farms, more Freeside gangers, caravan activity near east gate.

---

## Enemy Pack Compositions (Draft)

### Nightstalker Pack
- 1 Alpha Nightstalker (higher HP, flanks)
- 2–3 Nightstalkers (standard)
- 0–1 pup (fast, low damage, distracting)
- Behavior: Alpha circles while pack engages from front

### Cazador Swarm
- 5–12 Cazadores
- Scale: increase numbers with player level (via LVLA lists)
- Behavior: mass frontal assault, no tactics (they're bugs)
- Event trigger: migrations occur along pre-defined corridors in a 7-day cycle

### Raider War Band
- 1 War Chief (melee, heavy armor, aggressive)
- 3–5 Raiders (mixed weapons)
- 1–2 Thugs (melee, flankers)
- 1 Sniper if elevation available
- Behavior: War Chief engages, snipers suppress, thugs flank

### Legion Patrol
- 1 Decanus (leader, veteran stats)
- 3–4 Legionary soldiers
- Behavior: disciplined advance, cover each other, retreat to defensive position if 50% casualties

### NCR Patrol
- 1 Sergeant (rifle, takes cover)
- 2–3 Troopers (mixed)
- Behavior: suppress from cover, call for backup (trigger nearby patrol if within 500 units)

---

## Caravan Routes (Draft)

### Route A: Crimson Caravan Main Line
`Crimson Caravan HQ → Camp McCarran gate → Boulder City → Hoover Dam approach`
- Schedule: departs every 72 in-game hours
- Composition: 2 brahmin, 3 guards, 1 merchant, 1 hired caravan hand
- Threat: Powder Gangers ambush in Primm corridor if BoS faction variable low

### Route B: Followers of the Apocalypse Medical Run
`Followers Outpost (88) → Old Mormon Fort (Freeside) → Camp Forlorn Hope`
- Schedule: every 96 hours
- Composition: 1 brahmin (medical supplies), 2 Followers armed guards, 1 doctor
- Event: if Forlorn Hope is under attack, Followers caravan turns back and triggers a "supply cut" flag

### Route C: Independent Trader
`Mojave Outpost → Novac → Boulder City`
- Random schedule (every 48–120 hours, randomized)
- Composition: 1 trader, 1–2 guards (poorly equipped)
- High-risk: can be attacked by Legion scouts east of Nipton

### Route D: Great Khans Supply Run
`Red Rock Canyon → Boulder City → Freeside (back alley entrance)`
- Only active if player has not yet triggered the Great Khans quest conclusion
- Composition: 2–3 Khans with brahmin
- Carries: chems, some weapons

---

## NPC Daily Schedule Templates

### Settler (Town Resident)
```
06:00 — Wake, eat (sandbox near home)
08:00 — Work (farm / repair / trade — sandbox near work marker)
12:00 — Eat (sandbox near food source)
13:00 — Work
18:00 — Relax (sandbox near town common area)
21:00 — Return home, sleep
```

### Guard (Merchant or Town)
```
06:00 — Wake
07:00 — Patrol (follow patrol path)
13:00 — Rest at guard post (sandox, eat)
14:00 — Patrol
22:00 — Return to barracks/sleep point
```

### Refugee (Wanderer)
```
Random movement between waypoints
Will approach player if nearby and say a line
Moves toward nearest settlement over 2–3 in-game days then disappears (package: travel to ref, then disable)
```

---

## Engine Internals (RE) � Population Levers (mapped 2026-08-28)

RE-verified via the BUG-001 toolchain (see ../re/encounter_zone_subsystem.md).
Live values read from the running GOG 1.4.0.525 process; reader code sites located.

### Actor-density levers (the engine's own population knobs)

| Setting (console: setgs <name> <val>) | Live default | Function | Reader sites |
|---|---|---|---|
| iNumberActorsInCombatPlayer | 20 | max actors allowed in combat with the player simultaneously | 0x43D4CB, 0x40C14B, 0x4049FB |
| iNumberActorsAllowedToFollowPlayer | 6 | max actors that follow the player through transitions | 0x43D4CB (x8 sites) |
| iAINumberActorsComplexScene | 20 | max actors in complex scenes | 0x43D4CB, 0x40C14B, 0x4049FB |
| iNumberActorsGoThroughLoadDoorInCombat | 2 | max combat actors that pursue through load doors | 0x40C14B, 0x4049FB |

Setting objects (live addresses, base 0x00400000): 0x11CCFFC, 0x11CDAD0, 0x11CDE2C, 0x11D129C.
Layout: {type/vtable ptr, inline value (+4), name ptr (+8)}.

Mod usage: console setgs iNumberActorsInCombatPlayer 64 for instant testing;
permanent via plugin patch or Stewie's Tweaks equivalents.

### Encounter-zone attachment chain (RE-verified)

- TESWorldspace+0xD0 -> BGSEncounterZone* (savegame subrecord 'XZEN')
- BGSEncounterZone+0x18: owner formID -> resolved TESForm* at InitItem (FUN_00525F00)
- References: ExtraEncounterZone extra-data (consumer FUN_00432A70)
- Full map: ../re/encounter_zone_subsystem.md

### Spawn-tick (open)

The runtime consumer that reads encounter zones to scale/level spawns is not yet
located; leads: the 11 form-registry-reader functions (0x43A190..0x858330) and the
VATSMenu entry-builder cluster (0x7E9000-0x7F7000, 255 menu-global refs).
