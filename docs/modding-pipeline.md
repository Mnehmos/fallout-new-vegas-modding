# Modding Pipeline — How We Work

This doc describes our end-to-end workflow from idea to playable mod.

---

## The Stack

```
LLM (Claude/GPT)          ← Design decisions, code generation, analysis
    ↓
Python Scripts            ← Automation, data processing, TTS
    ↓
FNVEdit Pascal Scripts    ← Batch edits to ESP records
    ↓
GECK                      ← Complex scripting, dialogue, world edits
    ↓
.ESP Plugin File          ← The actual mod artifact
    ↓
Mod Organizer 2           ← Testing and distribution
```

---

## Workflow by Task Type

### Perk / Record Editing
1. Open FNVEdit, load `FalloutNV.esm`
2. Navigate to the `PERK` record type
3. Right-click → "Copy as override into..." → create new `PerkOverhaul.esp`
4. Edit values directly in FNVEdit
5. For batch changes: use FNVEdit Pascal scripts (see `tools/xedit-scripts/`)
6. Save, test in MO2

### New Dialogue / TTS Audio
1. Write dialogue text in `audio/tts/scripts/`
2. Run `scripts/tts/generate_tts.py` → outputs .wav files
3. Import into GECK as new dialogue records
4. Attach to NPC/quest via condition functions

### Asset Creation (3D/Textures)
1. Model in Blender
2. Export as .nif via Niftools addon
3. Fix in NifSkope (collision, BSX flags)
4. Place DDS textures in `mods/{ModName}/assets/textures/`
5. Reference in GECK

### NVSE Scripting (Advanced)
1. Write scripts in GECK script editor
2. Use NVSE functions for extended functionality
3. Reference: GECK Wiki + NVSE docs

---

## File Naming Convention

```
PerkOverhaul.esp                    ← Main plugin
PerkOverhaul - Patch - [Mod].esp    ← Compatibility patches
```

Assets:
```
textures/interface/perks/perk_[name]_icon.dds
meshes/perks/[name].nif
sound/voice/perkovhaul.esp/[npc]/[line_id].wav
```

---

## Testing Protocol

1. Launch FNV via MO2 (with `PerkOverhaul.esp` active)
2. Open console: `coc goodsprings` to skip intro
3. Test perks: `player.addperk [FormID]`
4. Check: perk appears in Pip-Boy, effects apply correctly
5. Check: no visual glitches, no crashes

### Getting FormIDs
- In FNVEdit, the FormID is shown in the record header
- Or in-game console: `help [perkname] 4`

---

## Git Workflow

```bash
# Start a new feature
git checkout -b feat/perk-overhaul-combat

# After changes work in-game
git add mods/PerkOverhaul/
git commit -m "feat(perks): rebalance Finesse and Better Criticals"

# Push for backup
git push origin feat/perk-overhaul-combat
```

The `.esp` file IS the source. Commit it like code.

---

## LLM Assistance Patterns

### For record analysis
```
"Here is the FNVEdit export of all PERK records.
Analyze each one and rate it A/B/C/D tier based on
combat utility, build synergy, and opportunity cost."
```

### For script generation
```
"Write an FNVEdit Pascal script that sets the
requirement level of all C/D tier perks to -1
(removing them as player perks)."
```

### For dialogue writing
```
"Write 3 lines of NPC dialogue acknowledging the
player took the [PerkName] perk.
Match the tone of Fallout New Vegas — dry, dark humor."
```
