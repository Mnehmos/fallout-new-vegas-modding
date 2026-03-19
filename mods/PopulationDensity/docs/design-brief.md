# PopulationDensity — Design Brief

## Working Title: "Living Mojave"
## Depends on: PerkOverhaul.esp (optional but recommended)

---

## Goal

The Mojave should feel populated and dangerous. Right now it's sparse — encounters happen, but they're isolated incidents. The overhaul makes the world feel like things are actually *happening* out there.

---

## Four Pillars

### 1. Enemy Pack Tactics & Swarms
Enemies don't fight alone unless they're loners by nature. Predators hunt in packs. Raiders have reinforcements.

**Planned changes:**
- Radscorpions, Cazadores, Nightstalkers: spawn in coordinated groups of 3–8
- Groups have a "leader" with higher stats and distinct behavior (flanking, covering fire)
- Distant gunfire events — hear a firefight, find a corpse pile or ongoing battle if you investigate
- Swarm events: periodic locust-style mass insect migrations across specific corridors
- Pack scaling: more enemies as player level increases (avoids early-game death zones)

### 2. Citizen Density
Towns and settlements feel empty. Merchants operate in ghost towns. Fix that.

**Planned changes:**
- Goodsprings: +4–6 residents with daily routines (farmers, scavengers, settlers)
- Novac: +3–5 travelers passing through; motel is actually full sometimes
- Boulder City: visible NCR logistics activity, supply runners
- Primm: when the town is secured, settlers actually return (scripted migration event)
- Random settler caravans traveling between towns (not merchants — just people moving)
- Refugees from Legion-controlled territory in the eastern Mojave

### 3. Caravan & Trade Traffic
The Mojave's economy is supposed to be held together by the Crimson Caravan, Gun Runners, and independent traders. You'd barely know it.

**Planned changes:**
- 3–5 caravan routes with visible pack brahmin, guards, and merchants traveling on schedule
- Each caravan has a unique roster and route (Crimson Caravan moves west → east, Followers moves toward medical outposts, etc.)
- Caravans can be attacked — spawn a dynamic ambush if reputation with certain factions is low
- Caravan survivors flee to nearest settlement and can be rescued
- Player can hire on as a caravan guard (quest hook, future scope)
- Gun Runners have visible transport wagons moving between the bazaar and stockpile

### 4. Faction Warfare
The NCR and Caesar's Legion are at war. You'd never know. The front line at Boulder City and Nelson should feel like a war zone.

**Planned changes:**
- Active patrol clashes — NCR rangers and Legion scouts fight on sight in contested territory
- Nelson area: visible Legion raids on NCR positions; NCR counter-patrols
- Cottonwood Cove: Legion staging activity, troop movements
- Camp Forlorn Hope: reinforcement caravans, wounded troopers returning, triage activity
- Random "battle aftermath" events — find a fresh combat site with loot and witnesses
- Mojave Outpost: actual supply line traffic coming through
- Great Khans territory: visible war parties, not just static NPCs
- Brotherhood of Steel outcast patrols in the western desert
- Powder Gangers: more roaming raider bands in early game Primm corridor

---

## Technical Approach

### Spawn System
Uses a combination of:
- **Static spawn markers** (placed in GECK) for fixed encounter zones
- **Leveled actor lists (LVLA)** for scaling enemy groups
- **Encounter zone scripts** for dynamic pack behavior
- **Timer-based scripts** (NVSE) for timed events like migrations and battles

### NPC Scheduling
- AI packages for daily routines (sandboxing, patrol, travel)
- Linked reference nodes for caravan routes
- Faction relations driving hostile vs. neutral behavior

### Performance Considerations
- Max concurrent spawns capped per region to avoid frame drops
- Distant spawns use culling distances
- Battle events have a 24-hour cooldown (no perpetual war noise)
- Option to configure density level via MCM (light / normal / heavy)

---

## Dependencies

- NVSE (required for timer scripts and extended conditions)
- JIP LN NVSE (required for extended AI package functions)
- Recommended: PerkOverhaul.esp (pack enemies more threatening with better perks on both sides)

---

## Compatibility Notes

- Will conflict with any mod that edits the same cell interior/exterior placements
- Provide a FNVEdit patch generator script for common conflict mods
- Use FormID ranges carefully — document all new FormIDs

---

## Release Plan

- v0.1 — Enemy pack spawns + caravan routes (no new NPCs, just rebalanced vanilla)
- v0.2 — Faction warfare patrols and battle events
- v0.3 — Citizen density + town population
- v1.0 — Full release with MCM density slider
