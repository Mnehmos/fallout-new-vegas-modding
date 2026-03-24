"""
Inject Mnehmos items into all DLC vendor lists.
Re-indexes HH and GRA vendor overrides after master list changed.
Adds items to OWB Sink and LR Commissary.

Master order: [0]FNV [1]DM [2]HH [3]LR [4]OWB [5]GRA
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# Master indices
HH_IDX = 2
LR_IDX = 3
OWB_IDX = 4
GRA_IDX = 5


def collect_weapons(esp):
    all_weap = []
    energy = []
    melee = []
    armor = []
    seen = set()

    for r in esp.get_records("WEAP"):
        srs = r.parse_subrecords()
        eid = name = ""
        animtype = 0
        for sr in srs:
            if sr.type == "EDID": eid = sr.data.rstrip(b"\x00").decode()
            if sr.type == "FULL": name = sr.data.rstrip(b"\x00").decode()
            if sr.type == "DNAM" and len(sr.data) >= 4:
                animtype = struct.unpack("<I", sr.data[0:4])[0]
        if not name or eid.startswith("NVDLC") or name in seen:
            continue
        seen.add(name)
        all_weap.append(r.id)
        if any(kw in eid for kw in ["Laser", "Plasma", "Tesla", "Gauss", "Recharger",
            "Epilogue", "Postscript", "Amendment", "Afterglow", "BrightIdea",
            "Eureka", "TotalRecall", "Bibliography", "Dissertation", "Axiom",
            "Abstract", "BigMT", "Mobius", "Sprtel", "Overexposure", "DejaVu",
            "Catharsis", "Anamnesis", "Stream", "ChristinesSilence", "ElijahsLegacy"]):
            energy.append(r.id)
        if animtype in (0, 1, 2):
            melee.append(r.id)

    for r in esp.get_records("ARMO"):
        srs = r.parse_subrecords()
        name = ""
        for sr in srs:
            if sr.type == "FULL": name = sr.data.rstrip(b"\x00").decode()
        if name and name not in seen:
            seen.add(name)
            armor.append(r.id)

    return all_weap, energy, melee, armor


def inject_list(builder, source_esm, target_fid, source_internal_fid, items):
    for r in source_esm.get_records("LVLI"):
        if r.id == source_internal_fid:
            srs = r.parse_subrecords()
            rec = RecordBuilder("LVLI", target_fid)
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    new_total = min(old_count + len(items), 255)
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", new_total)))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
            for fid in items:
                lvlo = struct.pack("<hHIhH", 1, 0, fid, 1, 0)
                rec.add_bytes("LVLO", lvlo)
            builder.add_raw_record("LVLI", rec.build())
            return old_count
    return -1


def main():
    esp = PluginFile(str(FNV_DATA / "MnehmosMojave.esp"))
    hh = PluginFile(str(FNV_DATA / "HonestHearts.esm"))
    owb = PluginFile(str(FNV_DATA / "OldWorldBlues.esm"))
    lr = PluginFile(str(FNV_DATA / "LonesomeRoad.esm"))
    gra = PluginFile(str(FNV_DATA / "GunRunnersArsenal.esm"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "MnehmosMojave.esp"))

    all_weap, energy, melee, armor = collect_weapons(esp)
    print("Weapons: " + str(len(all_weap)) + " Energy: " + str(len(energy)) +
          " Melee: " + str(len(melee)) + " Armor: " + str(len(armor)))

    # ── OWB: The Sink ──
    print("\n-- Old World Blues (The Sink) --")
    owb_lists = [
        ("VendorArmor", 0x01694F, armor[:10]),
        ("VendorArmorCommon", 0x016950, armor[:8]),
        ("VendorArmorCommon75", 0x016951, armor[:8]),
        ("VendorChestArmor", 0x01694E, armor[:6]),
        ("CraftingSuppliesGuns", 0x012303, all_weap[:12]),
    ]
    for name, low_fid, items in owb_lists:
        target = (OWB_IDX << 24) | low_fid
        internal = (0x01 << 24) | low_fid
        n = inject_list(builder, owb, target, internal, items)
        if n >= 0:
            print("  " + name + ": +" + str(len(items)))
        else:
            print("  " + name + ": NOT FOUND")

    # ── LR: Commissary ──
    print("\n-- Lonesome Road (Commissary) --")
    lr_lists = [
        ("VendorAmmoExplosives", 0x00E112, all_weap[:8]),
    ]
    for name, low_fid, items in lr_lists:
        target = (LR_IDX << 24) | low_fid
        internal = (0x01 << 24) | low_fid
        n = inject_list(builder, lr, target, internal, items)
        if n >= 0:
            print("  " + name + ": +" + str(len(items)))
        else:
            print("  " + name + ": NOT FOUND")

    # ── HH: Re-inject with corrected index ──
    print("\n-- Honest Hearts (corrected index " + str(HH_IDX) + ") --")
    hh_lists = [
        ("DanielVendorItems", 0x010C75, all_weap[:10]),
        ("VendorWeaponsModern", 0x00FA2A, all_weap[:8]),
        ("VendorWeaponsGunRunners", 0x0117C2, all_weap[:8]),
        ("VendorWeaponsGunsCommon", 0x0117BD, all_weap[:8]),
        ("VendorWeaponsMeleeHigh", 0x0117C0, melee[:6]),
        ("VendorWeaponsMeleeLow", 0x0117BF, melee[:6]),
    ]
    for name, low_fid, items in hh_lists:
        target = (HH_IDX << 24) | low_fid
        internal = (0x01 << 24) | low_fid
        n = inject_list(builder, hh, target, internal, items)
        if n >= 0:
            print("  " + name + ": +" + str(len(items)))
        else:
            print("  " + name + ": NOT FOUND")

    # ── GRA: Re-inject with corrected index ──
    print("\n-- GRA (corrected index " + str(GRA_IDX) + ") --")
    gra_lists = [
        ("GunRunners", 0x000A04, all_weap[:15]),
        ("VanGraffs", 0x000A01, energy[:12]),
        ("188GR", 0x000AAA, all_weap[:10]),
        ("188NCR", 0x0009FC, all_weap[:8]),
        ("Chet", 0x0009FE, all_weap[:8]),
        ("Lacey", 0x0009FD, all_weap[:8]),
        ("DaleBarton", 0x000A00, all_weap[:8]),
        ("CliffBriscoe", 0x000A02, all_weap[:8]),
        ("Boomers", 0x0009FF, all_weap[:6]),
        ("MickRalph", 0x000A03, all_weap[:8]),
    ]
    for name, low_fid, items in gra_lists:
        target = (GRA_IDX << 24) | low_fid
        internal = (0x01 << 24) | low_fid
        n = inject_list(builder, gra, target, internal, items)
        if n >= 0:
            print("  " + name + ": +" + str(len(items)))
        else:
            print("  " + name + ": NOT FOUND")

    builder.save(str(FNV_DATA / "MnehmosMojave.esp"))
    import os
    print("\nSaved: " + str(os.path.getsize(str(FNV_DATA / "MnehmosMojave.esp"))) + " bytes")


if __name__ == "__main__":
    main()
