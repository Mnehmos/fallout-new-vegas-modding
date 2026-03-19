# Fallout New Vegas Modding

Workspace for FNV mod development. LLM-assisted, full-stack modding from record editing to asset creation to voiced dialogue.

## Current Project: Perk Overhaul

**Goal:** Redesign all player perks to be A or B tier minimum. No more filler.

See [mods/PerkOverhaul/docs/design-brief.md](mods/PerkOverhaul/docs/design-brief.md)

## Quick Links

- [Tool Setup Guide](docs/tool-setup.md)
- [Modding Pipeline](docs/modding-pipeline.md)
- [Perk Database](research/perks/perk-database.md)
- [Tier Framework](research/perks/perk-tier-framework.md)

## Structure

```
mods/PerkOverhaul/     ← Active mod project
research/perks/        ← Perk analysis and tier ratings
tools/xedit-scripts/   ← FNVEdit Pascal scripts for batch edits
scripts/tts/           ← OpenAI TTS dialogue generator
docs/                  ← Tooling and pipeline documentation
audio/tts/             ← Dialogue scripts and generated audio
```

## Setup

```bash
# Python tools
pip install -r scripts/requirements.txt

# Copy and fill in your API key
cp .env.example .env
```

See [docs/tool-setup.md](docs/tool-setup.md) for the full game tool installation guide.
