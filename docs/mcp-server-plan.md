# MCP Server Plan — FNV Modding Tools

## Installed MCP Servers

| Server | Status | What It Controls |
|--------|--------|-----------------|
| blender-mcp | Installed (pip) | Blender 3.6 — 3D modeling, NIF mesh creation |
| gimp-mcp | Installed (F:\Github\gimp-mcp) | GIMP — texture editing, DDS creation |
| audacity-mcp | Installed (F:\Github\an3-audacity-mcp) | Audacity — audio editing, TTS cleanup |

---

## MCP Servers To Build

These tools have no community MCP servers. We need to build them ourselves.

### 1. mnehmos.fnvedit.mcp — FNVEdit Record Editor

**Priority: HIGH** — This is the primary tool for our Perk Overhaul.

**Approach:** FNVEdit supports command-line scripting via Pascal `.pas` scripts launched with `-script` flag. We wrap this in an MCP server.

**Architecture:**
```
Claude → MCP Server (Node/Python)
         ↓
         FNVEdit CLI (-script mode)
         ↓
         .pas script execution
         ↓
         ESP/ESM record changes
```

**Tools to expose:**
| Tool | Description |
|------|-------------|
| `list_records` | List all records of a type (PERK, NPC_, WEAP, etc.) from a plugin |
| `get_record` | Get full details of a specific record by EditorID or FormID |
| `export_records_csv` | Export records to CSV for LLM analysis |
| `create_override` | Copy a record as override into a target ESP |
| `set_field` | Set a specific field value on a record in the target ESP |
| `set_condition` | Add/modify/remove a condition on a PERK or similar record |
| `batch_edit` | Apply a series of field edits across multiple records |
| `validate_plugin` | Run conflict detection on an ESP |
| `save_plugin` | Save the current working ESP |

**Key consideration:** FNVEdit's Pascal scripting is limited. For complex operations, we generate `.pas` scripts dynamically, execute them via CLI, and parse the output.

**Alternative approach:** Use xEdit's `-autoload` and `-script:` flags to run headless. Parse stdout for results.

---

### 2. mnehmos.geck.mcp — GECK Construction Kit

**Priority: MEDIUM** — Needed for Phase 2+ (scripts, dialogue, NPCs).

**Approach:** The GECK has no CLI mode. Two strategies:

**Strategy A: File-based bridge**
- MCP server generates GECK-compatible script files (.gek/.txt)
- User loads them manually into GECK
- Semi-automated: Claude writes the scripts, user clicks "compile"

**Strategy B: OODA-based automation**
- Use mnehmos.ooda.mcp (already installed) to control GECK via screen capture + keyboard/mouse automation
- Find UI elements via OCR, click menus, type values
- Fragile but fully automated

**Recommended: Start with Strategy A**, graduate to B for repetitive tasks.

**Tools to expose (Strategy A):**
| Tool | Description |
|------|-------------|
| `generate_script` | Generate a GECK script file (.gek) from a description |
| `generate_dialogue` | Create dialogue tree structure as importable data |
| `generate_quest` | Create quest stages and objectives as GECK-importable format |
| `list_scripts` | List all scripts in a plugin |
| `validate_script` | Syntax-check a GECK script without compiling |

---

### 3. mnehmos.nifskope.mcp — NIF Mesh Editor

**Priority: LOW** — Only needed when creating custom assets.

**Approach:** NifSkope has no scripting API. Two options:

**Option A: Python NIF library (pyffi)**
- Bypass NifSkope entirely
- Use `pyffi` Python library to read/write NIF files programmatically
- MCP server wraps pyffi operations

**Option B: OODA automation** (same as GECK Strategy B)

**Recommended: Option A (pyffi)** — much more reliable.

```bash
pip install pyffi
```

**Tools to expose:**
| Tool | Description |
|------|-------------|
| `inspect_nif` | Read a NIF file and return its block structure |
| `list_materials` | List all material/texture references in a NIF |
| `swap_texture` | Replace a texture path reference in a NIF |
| `set_bsx_flags` | Set BSX flags (collision, animation markers) |
| `export_collision` | Extract or modify collision geometry |
| `batch_nif_edit` | Apply the same edit across multiple NIF files |

---

### 4. mnehmos.mo2.mcp — Mod Organizer 2

**Priority: LOW** — Nice to have for testing automation.

**Approach:** MO2 has a Python plugin system and an IPC interface.

**Tools to expose:**
| Tool | Description |
|------|-------------|
| `list_mods` | List all installed mods and their enabled state |
| `toggle_mod` | Enable/disable a mod |
| `get_load_order` | Get the current plugin load order |
| `set_load_order` | Set the plugin load order |
| `launch_game` | Launch FNV through MO2 with NVSE |
| `get_conflicts` | Show file conflicts between mods |

---

### 5. mnehmos.loot.mcp — Load Order Optimization

**Priority: LOW** — LOOT has a CLI mode.

**Approach:** LOOT's CLI (`loot --game FalloutNV --sort`) outputs sorted load order.

**Tools to expose:**
| Tool | Description |
|------|-------------|
| `sort_load_order` | Run LOOT sort and return the recommended order |
| `get_warnings` | Get LOOT warnings/errors for current load order |
| `get_metadata` | Get LOOT's metadata for a specific plugin |

---

## Build Priority

```
Phase 1 (NOW):    blender-mcp, gimp-mcp, audacity-mcp  ← Installing
Phase 2 (NEXT):   mnehmos.fnvedit.mcp                  ← First custom build
Phase 3 (LATER):  mnehmos.geck.mcp (Strategy A)        ← When we need scripts/dialogue
Phase 4 (MAYBE):  mnehmos.nifskope.mcp (pyffi)         ← When we need custom assets
Phase 5 (NICE):   mnehmos.mo2.mcp, mnehmos.loot.mcp    ← Testing automation
```

---

## Note on Vortex vs MO2

If staying with Vortex instead of MO2, the mod manager MCP would need to target Vortex's extension API instead. Vortex uses Electron + Node.js internally, which is actually easier to hook into via MCP.
