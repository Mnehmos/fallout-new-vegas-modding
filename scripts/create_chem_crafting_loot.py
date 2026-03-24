"""
Add crafting recipes and NPC loot drops for Archivist chems.

RCPE structure:
  EDID - Editor ID
  FULL - Display name
  CTDA - Conditions (optional, e.g. skill requirement)
  DATA - 16 bytes: skillReq(4) + skillLevel(4) + category(4) + subcategory(4)
  RCIL + RCQY pairs - Ingredients (FormID + quantity)
  RCOD + RCQY - Output item (FormID + quantity)

Categories:
  WorkbenchRecipes = 0x13B2C1
  CampfireRecipes = 0x13B2C0
  ChemsSubRecipes = 0x1613CF

Also injects chems into NPC drug loot lists so enemies drop them.
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# Known FormIDs
CAMPFIRE = 0x13B2C0
WORKBENCH = 0x13B2C1
CHEMS_SUB = 0x1613CF

# Ingredient FormIDs (from FalloutNV.esm)
BROC_FLOWER = 0x0FAFCA     # Broc Flower
XANDER_ROOT = 0x0FAFCB     # Xander Root
EMPTY_SYRINGE = 0x0250A8   # Empty Syringe
SURGICAL_TUBING = 0x13B2BA # Surgical Tubing
RADSCORPION_POISON = 0x13B2B0  # Radscorpion Poison Gland
CAZADOR_POISON = 0x13B2B9  # Cazador Poison Gland
NIGHTSTALKER_BLOOD = 0x13B2B6  # Nightstalker Blood
MUTFRUIT = 0x02F3ED        # Mutfruit
BUFFOUT_ITEM = 0x015163    # Buffout
JET_ITEM = 0x015164        # Jet
PSYCHO_ITEM = 0x015166     # Psycho
MENTATS_ITEM = 0x015165    # Mentats
TURBO_ITEM = 0x120D81      # NVTurbo
MEDX_ITEM = 0x050F8F       # Morphine (Med-X)
RADAWAY_ITEM = 0x015167    # RadAway
STIMPAK_ITEM = 0x015169    # Stimpak
NUKA_COLA = 0x0284F7       # Nuka-Cola
PURIFIED_WATER = 0x0151A3  # Purified Water
WONDERGLUE = 0x02F3EF      # Wonderglue
SCRAP_ELECTRONICS = 0x06B207  # Scrap Electronics
SCRAP_METAL = 0x031944     # Scrap Metal


def main():
    print("=== Chem Crafting + Loot Drops ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    esp = PluginFile(str(FNV_DATA / "HardcoreTuning.esp"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "HardcoreTuning.esp"))

    # Find our custom chem FormIDs
    chem_fids = {}
    for r in esp.get_records("ALCH"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if eid.startswith("MnChem"):
            chem_fids[eid] = r.id

    print("Found chems: " + str(list(chem_fids.keys())))

    # ══════════════════════════════════════════
    # CRAFTING RECIPES
    # ══════════════════════════════════════════
    print("\n-- Crafting Recipes (Workbench, Science 50+) --")

    # DATA format: skillReq(u32) + skillLevel(u32) + category(u32) + subcategory(u32)
    # skillReq: 40 = Science (ActorValue index)
    # skillLevel: required level

    recipes = [
        # Clarity: Mentats + Cateye + Empty Syringe (Science 50)
        ("RecipeMnClarity", "Clarity", "MnChemClarity", 50, [
            (MENTATS_ITEM, 1),
            (NIGHTSTALKER_BLOOD, 1),
            (EMPTY_SYRINGE, 1),
        ]),
        # Overdrive: Psycho + Jet + Surgical Tubing (Science 60)
        ("RecipeMnOverdrive", "Overdrive", "MnChemOverdrive", 60, [
            (PSYCHO_ITEM, 1),
            (JET_ITEM, 1),
            (SURGICAL_TUBING, 1),
        ]),
        # Fortify: Buffout + Stimpak + Mutfruit (Science 50)
        ("RecipeMnFortify", "Fortify", "MnChemFortify", 50, [
            (BUFFOUT_ITEM, 1),
            (STIMPAK_ITEM, 1),
            (MUTFRUIT, 2),
        ]),
        # Reflex: Turbo + Jet + Nuka-Cola (Science 75)
        ("RecipeMnReflex", "Reflex", "MnChemReflex", 75, [
            (TURBO_ITEM, 2),
            (JET_ITEM, 1),
            (NUKA_COLA, 1),
        ]),
        # Aegis: Med-X + RadAway + Wonderglue (Science 60)
        ("RecipeMnAegis", "Aegis", "MnChemAegis", 60, [
            (MEDX_ITEM, 1),
            (RADAWAY_ITEM, 1),
            (WONDERGLUE, 1),
        ]),
    ]

    for recipe_eid, recipe_name, chem_eid, skill_level, ingredients in recipes:
        if chem_eid not in chem_fids:
            print("  SKIP: " + chem_eid + " not found in ESP")
            continue

        output_fid = chem_fids[chem_eid]
        fid = builder.allocate_form_id()
        rec = RecordBuilder("RCPE", fid)

        rec.add_string("EDID", recipe_eid)
        rec.add_string("FULL", recipe_name)

        # DATA: Science skill (AV 40), level, workbench category, chems subcategory
        data = struct.pack("<IIII", 40, skill_level, WORKBENCH, CHEMS_SUB)
        rec.add_bytes("DATA", data)

        # Ingredients
        for ing_fid, qty in ingredients:
            rec.add_formid("RCIL", ing_fid)
            rec.add_uint32("RCQY", qty)

        # Output
        rec.add_formid("RCOD", output_fid)
        rec.add_uint32("RCQY", 1)

        builder.add_record("RCPE", rec)
        ing_str = " + ".join(str(q) + "x" + hex(f)[-5:] for f, q in ingredients)
        print("  " + recipe_name + " (Science " + str(skill_level) + "): " + ing_str)

    # ══════════════════════════════════════════
    # LOOT DROPS — Add to NPC drug loot lists
    # ══════════════════════════════════════════
    print("\n-- NPC Loot Drops --")

    # Add our chems to the main drug loot lists
    # LootChemsNVDrugs100 (0xCCF8A) — most common drug drop, 11 entries
    # LootChemsNVDrugs75 (0xCCF8B) — 9 entries
    # LootChemsNVDrugs25 (0xFD78E) — 11 entries
    # LootChemsDrugs100 (0x37829) — 11 entries
    # LootChemsDrugs75 (0x3782A) — 11 entries

    all_chem_fids = list(chem_fids.values())

    loot_lists = [
        (0xCCF8A, "LootChemsNVDrugs100"),
        (0xCCF8B, "LootChemsNVDrugs75"),
        (0xFD78E, "LootChemsNVDrugs25"),
        (0x37829, "LootChemsDrugs100"),
        (0x3782A, "LootChemsDrugs75"),
    ]

    for list_fid, list_name in loot_lists:
        for r in esm.get_records("LVLI"):
            if r.id == list_fid:
                srs = r.parse_subrecords()
                rec = RecordBuilder("LVLI", list_fid)
                old_count = 0

                for sr in srs:
                    if sr.type == "LLCT":
                        old_count = sr.data[0]
                        new_total = min(old_count + len(all_chem_fids), 255)
                        rec.add(SR.from_bytes("LLCT", struct.pack("<B", new_total)))
                    else:
                        rec.add(SR.from_bytes(sr.type, sr.data))

                # Add each chem with level 10 requirement
                for cfid in all_chem_fids:
                    lvlo = struct.pack("<hHIhH", 10, 0, cfid, 1, 0)
                    rec.add_bytes("LVLO", lvlo)

                builder.add_raw_record("LVLI", rec.build())
                print("  " + list_name + ": +" + str(len(all_chem_fids)) + " chems")
                break

    # ══════════════════════════════════════════
    # VENDOR LISTS — Add to chem vendors
    # ══════════════════════════════════════════
    print("\n-- Chem Vendors --")

    # VendorChemsDrugs100 (0x544A2) — main drug vendor list
    # VendorChemsDrugs75 (0x5449C)
    vendor_lists = [
        (0x544A2, "VendorChemsDrugs100"),
        (0x5449C, "VendorChemsDrugs75"),
    ]

    for list_fid, list_name in vendor_lists:
        for r in esm.get_records("LVLI"):
            if r.id == list_fid:
                srs = r.parse_subrecords()
                rec = RecordBuilder("LVLI", list_fid)
                old_count = 0

                for sr in srs:
                    if sr.type == "LLCT":
                        old_count = sr.data[0]
                        new_total = min(old_count + len(all_chem_fids), 255)
                        rec.add(SR.from_bytes("LLCT", struct.pack("<B", new_total)))
                    else:
                        rec.add(SR.from_bytes(sr.type, sr.data))

                for cfid in all_chem_fids:
                    lvlo = struct.pack("<hHIhH", 1, 0, cfid, 1, 0)
                    rec.add_bytes("LVLO", lvlo)

                builder.add_raw_record("LVLI", rec.build())
                print("  " + list_name + ": +" + str(len(all_chem_fids)) + " chems")
                break

    # Save
    builder.save(str(FNV_DATA / "HardcoreTuning.esp"))
    import os
    print("\nSaved: " + str(os.path.getsize(str(FNV_DATA / "HardcoreTuning.esp"))) + " bytes")


if __name__ == "__main__":
    main()
