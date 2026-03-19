# Fallout New Vegas Modding

Workspace for FNV mod development. LLM-assisted, full-stack modding from record editing to asset creation to voiced dialogue.

## Project Status

| Mod | Status | Description |
|-----|--------|-------------|
| **PerkOverhaul** | v1.0 COMPLETE | 80 perks rebalanced, 18 gameplay values changed |
| **PopulationDensity** | UP NEXT | Increase encounter density across the Mojave |

---

## Completed: PerkOverhaul v1.0

All vanilla perks rebalanced to B-tier minimum. No more filler picks.

- **80 perk records** edited (level requirements, ranks, descriptions)
- **11 Entry Point float values** changed (damage multipliers, DT, XP, skill points)
- **7 SPEL ability values** changed (HP, AP, DT bonuses)
- D/F tier perks rescued: Swift Learner, Here and Now, Explorer, Lead Belly, Rad Resistance, Fortune Finder, Scrounger, Night Person, Entomologist
- Key buffs: Bloody Mess 5%->10%, Toughness +3->+4 DT, Educated +2->+3 pts, Tag! Lvl 16->8

See [mods/PerkOverhaul/docs/design-brief.md](mods/PerkOverhaul/docs/design-brief.md) for the complete design document.

## Next Up: PopulationDensity

Increase enemy encounter density across the Mojave to work with the buffed perk set.

See [mods/PopulationDensity/docs/design-brief.md](mods/PopulationDensity/docs/design-brief.md)

---

## Toolchain

| Tool | Status | Purpose |
|------|--------|---------|
| FNVEdit 4.1.5f | Installed | Record editing, Pascal script execution |
| LOOT 0.28.0 | Installed | Load order optimization |
| NifSkope | Installed | Mesh inspection |
| mnehmos.fnvedit.mcp | Built | MCP server for ESM reading, ESP generation, perk analysis |
| bethesda-structs | Installed | Python library for binary ESP/ESM parsing |
| blender-mcp | Installed | 3D modeling via Blender |
| gimp-mcp | Installed | Texture editing via GIMP |
| audacity-mcp | Installed | Audio editing via Audacity |
| Mod Organizer 2 | Installed | Virtual filesystem mod management |
| NVSE + JIP LN + JohnnyGuitar | Installed | Script extender stack |
| lStewieAl's Tweaks | Staged | Engine fixes and QOL |

## Quick Links

- [PerkOverhaul Design Doc](mods/PerkOverhaul/docs/design-brief.md)
- [PopulationDensity Design Doc](mods/PopulationDensity/docs/design-brief.md)
- [Tool Setup Guide](docs/tool-setup.md)
- [Modding Pipeline](docs/modding-pipeline.md)
- [MCP Server Plan](docs/mcp-server-plan.md)
- [Perk Database](research/perks/perk-database.md)
- [Perk Tier Framework](research/perks/perk-tier-framework.md)

## Structure

```
mods/PerkOverhaul/         <- Complete — v1.0 perk rebalance
mods/PopulationDensity/    <- Next — encounter density mod
research/perks/            <- Perk analysis and tier ratings
research/population/       <- Encounter zone research
tools/FNVEdit/             <- FNVEdit 4.1.5f + custom Edit Scripts
tools/LOOT/                <- Load order optimization
tools/NifSkope/            <- Mesh viewer
tools/xedit-scripts/       <- Custom Pascal scripts for batch edits
tools/staging/             <- NVSE plugin staging (JIP, JohnnyGuitar, Stewie)
scripts/tts/               <- OpenAI TTS dialogue generator
docs/                      <- Tooling and pipeline documentation
audio/tts/                 <- Dialogue scripts and generated audio
```

## Setup

```bash
# Python tools
pip install -r scripts/requirements.txt

# Copy and fill in your API key
cp .env.example .env
```

See [docs/tool-setup.md](docs/tool-setup.md) for the full game tool installation guide.
