# Tool Setup Guide — Fallout New Vegas Modding

Install in this exact order. Each tool builds on the previous.

---

## 1. Fallout: New Vegas (Steam / GOG)

- Install to a **non-UAC path** — NOT `C:\Program Files\`. Use something like `D:\Games\Fallout New Vegas\`
- UAC-protected paths cause constant permission headaches with modding tools
- Run the game once to generate INI files before installing anything else

---

## 2. Mod Organizer 2 (MO2)

**What it does:** Virtual file system — mods never touch the actual game folder. Essential.

- Download: ModOrganizer2 on GitHub (ModOrganizer2/ModOrganizer2 releases)
- Install to its own folder: `D:\ModOrganizer2\` (not inside the game dir)
- On first launch, point it at your FNV installation
- Set up a profile called `Dev` for testing your own mods

---

## 3. New Vegas Script Extender (NVSE)

**What it does:** Extends the game engine's scripting capabilities. Required by ~90% of modern mods.

- Search: "NVSE New Vegas Script Extender" on nvse.silverlock.org
- Install: Copy `nvse_loader.exe` and DLLs into your FNV root folder
- Launch the game through `nvse_loader.exe` (or MO2 will handle this)
- Test: Open console in-game, type `GetNVSEVersion` — should return a number

---

## 4. FNVEdit (xEdit for New Vegas)

**What it does:** The primary tool for viewing/editing ESP/ESM plugin files. Used for perk editing.

- Search: "FNVEdit" or "xEdit" on Nexus Mods
- Rename the exe to `FNVEdit.exe` if it's named `xEdit.exe`
- On first run: loads all your installed plugins so you can browse/edit records
- Key for us: Perk records live under `PERK` in the record tree

### Setting up FNVEdit for scripting
Create a shortcut with `-script` flag to enable Pascal script execution:
```
FNVEdit.exe -script
```

---

## 5. GECK (Garden of Eden Construction Kit)

**What it does:** Bethesda's official editor. Needed for complex scripting, dialogue, and world editing.

- Search: "GECK New Vegas" — available on Nexus or through Bethesda's older tools
- **GECK Powerup** patch is highly recommended — fixes crashes and adds features
- The GECK is unstable; save often, use version control

---

## 6. NifSkope

**What it does:** View and edit .nif 3D mesh files used by the engine.

- Search: "NifSkope" on GitHub (niftools/nifskope)
- Used for: attaching armor/weapon meshes, fixing mesh issues, inspecting existing assets

---

## 7. Blender + Niftools Addon

**What it does:** Full 3D modeling. Export .nif files for the game engine.

- Blender: blender.org (use 3.6 LTS for best plugin compatibility)
- Niftools addon: Search "Blender Nif Plugin" on GitHub (niftools/blender-niftools-addon)
- Workflow: Model in Blender → Export as .nif → Import into NifSkope for final fixes

---

## 8. GIMP + DDS Plugin (or Photoshop + Intel Texture Works)

**What it does:** Create/edit textures in DDS format (what FNV uses).

- GIMP: gimp.org (free)
- DDS plugin for GIMP: Search "GIMP DDS plugin"
- Alternative: Paint.NET with DDS plugin (simpler for basic work)

---

## 9. Audacity

**What it does:** Record/edit audio. We'll use OpenAI TTS for generation, Audacity for cleanup.

- audacityteam.org
- Install the FFmpeg library for Audacity (enables MP3/WAV conversion)

---

## 10. Python 3.11+

**What it does:** Our automation layer — batch editing, TTS integration, data processing.

- python.org
- After install: `pip install -r scripts/requirements.txt`

---

## Recommended Load Order for MO2 Profiles

```
FalloutNV.esm          ← Master
DeadMoney.esm
HonestHearts.esm
OldWorldBlues.esm
LonesomeRoad.esm
GunRunnersArsenal.esm
ClassicPack.esm
MercenaryPack.esm
TribalPack.esm
CaravanPack.esm
---
[Your mods here]
---
PerkOverhaul.esp       ← Our mod, loads last to override
```

---

## Quick Sanity Check

After installing everything, verify:

```bash
# In your FNV root, you should see:
nvse_loader.exe         ✓
nvse_1_4.dll            ✓
FalloutNV.exe           ✓

# In MO2 you should see all DLCs listed as active
# FNVEdit should load without errors
```
