# Aspirations — Things We Could Build

Ideas that go beyond the current mod projects. Organized by feasibility and ambition.

---

## Tier 1: Near-Term (We Have the Tech)

### MnemoScript DSL Compiler
- **Status:** DONE — 17/17 tests passing, integrated into fnvedit-mcp as `compile_script` tool
- Custom language → GECK bytecode. Eliminates GECK as a dependency.
- Compiles inline source or .mns files. Outputs SCPT records. Injects directly into ESP.
- Supports: variables, if/else, Begin blocks, all vanilla opcodes, FormID references.
- Live in MCP: `compile_script(source="script Foo...")` → bytecode in seconds.

### Full ESP Decompiler / Disassembler
- We can already parse all 88 record types and 465k records.
- Add SCDA bytecode disassembly → human-readable pseudocode for every script in the game.
- Use case: reverse-engineer any mod's scripts without GECK. Audit for bugs. Learn patterns.

### Automated Mod Conflict Detector
- Load two ESPs, diff every overlapping record at the subrecord level.
- Already have `diff_plugins` in fnvedit-mcp. Extend to: auto-generate compatibility patches.
- Could generate xEdit merge scripts automatically.

### Voice Pipeline v2 — Emotional TTS with Audacity Post-Processing
- Current: OpenAI TTS → WAV → Data folder.
- Next: Chain audacity-mcp for reverb, EQ, and noise matching to vanilla voice lines.
- Match the specific "radio filter" and "intercom" voice types in FNV.
- Auto-generate LIP files for facial animation sync.

### Procedural Leveled List Generator
- Input: "I want more wildlife in the Mojave, especially at night"
- Output: Modified LVLC/LVLN records with time-of-day conditions, scaled counts, CalcEach tuning.
- Already proven the tech with PopulationDensity, Zion, and Lonesome Road overhauls.

---

## Tier 2: Medium-Term (Needs Research)

### mnehmos.bethesda.mcp — Universal Bethesda Modding Framework
- Abstract our binary parser + ESP writer + MnemoScript to work across:
  - Fallout 3 (nearly identical format)
  - Oblivion (same bytecode engine, different record types)
  - Fallout 4 (Papyrus scripts, different binary format)
  - Skyrim SE/AE (Papyrus, similar to FO4)
- The SCPT bytecode format is shared between TES4/FO3/FNV. Our compiler ports with minimal changes.
- Papyrus (FO4/Skyrim) needs a separate compiler but the same architectural pattern.

### Natural Language → ESP Pipeline
- **Status:** LARGELY BUILT — fnvedit-mcp tools + mnehmos.nls.lang (NLS compiler)
- "Make a shotgun that does 80 damage, has 8 shells, and looks like the Hunting Shotgun"
- LLM parses intent → calls fnvedit-mcp clone_record → sets fields → injects into ESP.
- NLS compiler (F:\Github\mnehmos.nls.lang) provides the formal "intent → code" bridge.
- The planning layer IS the LLM + MCP tool chain. Already working for weapons, armor, perks, scripts.

### AI Dungeon Master for FNV
- Use mnehmos.rpg.mcp's combat/spatial engine but with FNV game state as input.
- Read save game → extract player stats, inventory, quest progress.
- Generate contextual quests, dialogue, and encounters based on actual playthrough.
- Write ESP patches in real-time that inject content into the player's current game.

### Procedural Interior Generator
- Input: "Create a raider hideout with 3 rooms, a locked terminal, and a boss"
- Generate CELL records with REFR placements, NAVM (navmesh is the hard part), lighting.
- NAVM generation is the unsolved problem. Could use simple rectangular navmesh templates.

### Mod Quality Scoring Engine
- Load any ESP → run our 10-sweep audit → score on:
  - Balance (weapon DPS within ranges, armor DT curves)
  - Completeness (all records have names, descriptions, proper flags)
  - Compatibility (no wild edits, proper master dependencies)
  - Polish (no placeholder values, no missing textures)
- Output a "mod health report" with specific fix recommendations.

---

## Tier 3: Long-Term (Pushing Limits)

### Save Game Parser + Live Mod Injection
- Parse FNV save game format (documented by community).
- Read player state, quest flags, world changes.
- Generate targeted ESP patches based on save state.
- Example: "The player has been doing NCR quests — generate a Legion assassination squad encounter."

### AI Companion System
- A fully scripted companion NPC that uses LLM for dialogue.
- MnemoScript compiles conversation routing logic.
- NVSE's string manipulation + file I/O could pipe prompts to an external LLM.
- The companion reacts to game events, remembers conversations, has opinions.

### Procedural Worldspace Generator
- Generate entirely new worldspaces with terrain, flora, structures.
- LAND records (heightmap), LTEX (textures), CELL/REFR (objects), NAVM (pathing).
- Would need: Blender MCP for terrain mesh → NIF export → LAND subrecord injection.
- The hardest possible thing to automate. Would be genuinely unprecedented.

### Cross-Mod Narrative Engine
- Track narrative state across multiple ESP mods.
- Mod A's quest outcome affects Mod B's NPC dialogue.
- Uses GLOB variables and cross-ESP condition checking.
- A shared "narrative bus" that mods can publish/subscribe to.

### FNV → Unreal/Godot Scene Converter
- Parse worldspace data → export as Unreal/Godot scene.
- Convert NIF meshes to modern formats.
- Preserve spatial relationships, lighting, object placement.
- Use case: rapid prototyping of game levels using FNV as a layout tool.

### Full GECK Replacement (GECK 2.0)
- Web-based editor using our binary parser as backend.
- Real-time ESP editing with visual record browser.
- MnemoScript editor with syntax highlighting and autocomplete.
- 3D viewport via Three.js for object placement.
- Eliminates the crashy, 15-year-old GECK entirely.
- This is the "build your own game editor" moonshot.

---

## Tier 4: Off-Topic But Intriguing

### mnehmos.bethesda-archive.mcp — BSA/BA2 Archive Tool
- Pack/unpack Bethesda archive formats programmatically.
- Extract textures, meshes, sounds from vanilla archives for analysis.
- Auto-package loose files into BSA for distribution.

### Mod Decompilation + Documentation Generator
- Load any ESP → generate full human-readable documentation.
- "This mod adds 15 weapons, modifies 3 perks, changes 8 leveled lists. Here's what each change does."
- Use the binary parser + script disassembler + LLM summarization.

### Fallout Lore Knowledge Graph
- Parse all DIAL/INFO records → extract every line of dialogue.
- Build a knowledge graph of characters, factions, locations, events.
- Query: "What does Caesar think about the NCR?" → all relevant dialogue lines.
- Cross-reference with quest stages and conditions.

### Speedrun Route Optimizer
- Parse NAVM + CELL data → build navigation graph.
- Calculate optimal paths between quest objectives.
- Factor in combat encounters, lock requirements, speech checks.
- Output: "Fastest route to complete the game with these constraints."

### Modding Tutorial Generator
- Given a mod concept, generate step-by-step instructions.
- "How to make a new companion" → generates CLAUDE.md-style instructions with exact record types, field paths, and xEdit steps.
- Uses our proven knowledge of field paths, gotchas (DT offset, TNAM vs DESC, multi-projectile damage).

---

## What We've Already Built (For Perspective)

| Tool/Asset | What It Does |
|------------|-------------|
| Custom ESP binary parser | Reads 465k records in 2 seconds, handles zlib compression |
| ESP binary writer | Creates/modifies ESP files from Python, clone+modify any record |
| mnehmos.fnvedit.mcp | 25+ MCP tools for record reading, searching, cloning, placing |
| 30+ xEdit Pascal scripts | Perk overhaul, population density, casino overhaul, item creation |
| 10-sweep ESP auditor | Validates weapons, armor, enchantments, NPCs, containers, dupes |
| TTS voice pipeline | OpenAI → WAV → FNV voice directory structure |
| Bytecode format spec | 700+ line reference doc covering all SCPT internals |
| MnemoScript compiler | (BUILDING) Custom DSL → GECK bytecode |

The modding surface map shows 45 record types we can reliably create/modify, covering items, characters, magic, economy, world placement, and soon scripting. Only 6 record types remain truly blocked (AI packages, NPC placement, navmesh, landscape, navigation).
