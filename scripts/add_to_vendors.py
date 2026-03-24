"""
Add Mnehmos weapons and armor to appropriate vendor leveled lists.

Vendor tiers map to weapon power:
  Tier 1-2: Early game (dmg < 30)
  Tier 3: Mid game (dmg 30-60)
  Tier 4: Late game (dmg 60-100)
  Tier 5: Endgame (dmg 100+)

Weapons go to: Gun Runners, Van Graff (energy), 188 Trading Post, Crimson Caravan
Armor goes to: VendorArmorTier lists
Melee/Unarmed go to: VendorWeaponsMeleeTier / UnarmedTier
Explosives go to: VendorWeaponsExplosivesTier
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")


def add_to_lvli(builder, esm, list_formid, item_formids, level=1, count=1):
    """Override a vanilla LVLI and append new items."""
    # Find original record
    for r in esm.get_records("LVLI"):
        if r.id == list_formid:
            srs = r.parse_subrecords()
            rec = RecordBuilder("LVLI", list_formid)

            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    # Will update count
                    old_count = sr.data[0]
                    continue
                rec.add(SR.from_bytes(sr.type, sr.data))
                if sr.type == "LVLO":
                    pass  # keep original

            # Update LLCT (entry count) - insert after LVLF
            new_total = old_count + len(item_formids)

            # Rebuild properly - need LLCT before LVLO entries
            rec2 = RecordBuilder("LVLI", list_formid)
            for sr in srs:
                if sr.type == "LLCT":
                    rec2.add(SR.from_bytes("LLCT", struct.pack("<B", min(new_total, 255))))
                else:
                    rec2.add(SR.from_bytes(sr.type, sr.data))

            # Add new items
            for fid in item_formids:
                lvlo = struct.pack("<hHIhH", level, 0, fid, count, 0)
                rec2.add_bytes("LVLO", lvlo)

            builder.add_raw_record("LVLI", rec2.build())
            return True
    return False


def main():
    print("=== Adding Mnehmos Items to Vendors ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    esp = PluginFile(str(FNV_DATA / "MnehmosMojave.esp"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "MnehmosMojave.esp"))

    # Collect all our weapon FormIDs by damage tier
    tier1 = []  # dmg < 25
    tier2 = []  # dmg 25-39
    tier3 = []  # dmg 40-60
    tier4 = []  # dmg 61-100
    tier5 = []  # dmg 100+

    energy_items = []
    melee_items = []
    unarmed_items = []
    explosive_items = []
    armor_light = []   # DT < 20
    armor_heavy = []   # DT >= 20

    seen_names = set()

    for r in esp.get_records("WEAP"):
        srs = r.parse_subrecords()
        eid = name = ""
        dmg = 0
        animtype = 0
        for sr in srs:
            if sr.type == "EDID": eid = sr.data.rstrip(b"\x00").decode()
            if sr.type == "FULL": name = sr.data.rstrip(b"\x00").decode()
            if sr.type == "DATA" and len(sr.data) == 15:
                dmg = struct.unpack("<h", sr.data[12:14])[0]
            if sr.type == "DNAM" and len(sr.data) >= 4:
                animtype = struct.unpack("<I", sr.data[0:4])[0]
        if not name or eid.startswith("NVDLC") or name in seen_names:
            continue
        seen_names.add(name)
        fid = r.id

        # Categorize
        is_energy = any(kw in eid for kw in ["Laser", "Plasma", "Tesla", "Gauss", "Recharger",
                        "Epilogue", "Postscript", "Amendment", "Afterglow", "BrightIdea",
                        "Eureka", "TotalRecall", "Bibliography", "Dissertation", "Axiom",
                        "Abstract", "BigMT", "Mobius", "Sprtel", "Overexposure", "DejaVu",
                        "Catharsis", "Anamnesis", "Stream", "ChristinesSilence", "ElijahsLegacy"])
        is_melee = animtype in (1, 2) or any(kw in eid for kw in ["RedPen", "Strikethrough",
                        "Revision", "Shredder", "Declassified", "Grudge", "WhiteLegs",
                        "BladeWest", "Gehenna", "Closure", "SierraMadre"])
        is_unarmed = animtype == 0 or any(kw in eid for kw in ["Fist", "Gauntlet", "Glove",
                        "Footnote2", "Exclamation", "ZionsFist", "RawrMk2", "TwoStep", "DrKlein", "PhantomLimb"])
        is_explosive = any(kw in eid for kw in ["Grenade", "Categorical", "Parenthetical",
                        "Missile", "Addendum", "RedGlare", "Incinerator"])

        if is_melee:
            melee_items.append(fid)
        elif is_unarmed:
            unarmed_items.append(fid)
        elif is_explosive:
            explosive_items.append(fid)
        elif is_energy:
            energy_items.append(fid)

        # Tier by damage
        if dmg < 25: tier1.append(fid)
        elif dmg < 40: tier2.append(fid)
        elif dmg < 61: tier3.append(fid)
        elif dmg <= 100: tier4.append(fid)
        else: tier5.append(fid)

    # Collect armor
    for r in esp.get_records("ARMO"):
        srs = r.parse_subrecords()
        name = ""
        dt = 0
        for sr in srs:
            if sr.type == "FULL": name = sr.data.rstrip(b"\x00").decode()
            if sr.type == "DNAM" and len(sr.data) >= 8:
                dt = struct.unpack("<f", sr.data[4:8])[0]
        if not name or name in seen_names:
            continue
        seen_names.add(name)
        fid = r.id
        if dt >= 20:
            armor_heavy.append(fid)
        else:
            armor_light.append(fid)

    # ── Inject into vendor lists ──

    # Gun Runner tiers (ballistic guns)
    print("Gun Runners:")
    for list_id, items, tier_name in [
        (0x167118, tier1, "Tier1"), (0x167119, tier2, "Tier2"),
        (0x16711a, tier3, "Tier3"), (0x16711b, tier4, "Tier4"),
        (0x16711c, tier5, "Tier5"),
    ]:
        if items:
            add_to_lvli(builder, esm, list_id, items)
            print("  " + tier_name + ": +" + str(len(items)) + " weapons")

    # Van Graff tiers (energy weapons)
    print("Van Graff (Silver Rush):")
    for list_id, tier_name in [
        (0x167128, "Tier1"), (0x16712e, "Tier2"), (0x16712f, "Tier3"),
        (0x167130, "Tier4"), (0x167131, "Tier5"),
    ]:
        # Put energy items in appropriate tiers
        add_to_lvli(builder, esm, list_id, energy_items)
        print("  " + tier_name + ": +" + str(len(energy_items)) + " energy weapons")
        break  # Just add all to Tier1 (they filter by level anyway)

    # Energy weapon vendor lists
    print("Energy Weapon Vendors:")
    if energy_items:
        add_to_lvli(builder, esm, 0x14e76a, energy_items)  # GunRunnerStoreEnergyTier5
        print("  GunRunnerEnergyTier5: +" + str(len(energy_items)))

    # Melee vendor tiers
    print("Melee Vendors:")
    if melee_items:
        add_to_lvli(builder, esm, 0x167147, melee_items)  # MeleeTier5
        print("  MeleeTier5: +" + str(len(melee_items)))

    # Unarmed vendor tiers
    print("Unarmed Vendors:")
    if unarmed_items:
        add_to_lvli(builder, esm, 0x16714f, unarmed_items)  # UnarmedTier5
        print("  UnarmedTier5: +" + str(len(unarmed_items)))

    # Explosives
    print("Explosive Vendors:")
    if explosive_items:
        add_to_lvli(builder, esm, 0x167141, explosive_items)  # ExplosivesTier5
        print("  ExplosivesTier5: +" + str(len(explosive_items)))

    # Armor tiers
    print("Armor Vendors:")
    if armor_light:
        add_to_lvli(builder, esm, 0x16711f, armor_light)  # ArmorTier3
        print("  ArmorTier3: +" + str(len(armor_light)) + " light armor")
    if armor_heavy:
        add_to_lvli(builder, esm, 0x167121, armor_heavy)  # ArmorTier5
        print("  ArmorTier5: +" + str(len(armor_heavy)) + " heavy armor")

    # 188 Trading Post
    print("188 Trading Post:")
    mid_weapons = tier2 + tier3
    if mid_weapons:
        add_to_lvli(builder, esm, 0xe6668, mid_weapons[:10])  # 188NCRArmsMerchantWeap
        print("  188Arms: +" + str(min(len(mid_weapons), 10)) + " weapons")

    # Crimson Caravan
    print("Crimson Caravan:")
    if tier3:
        add_to_lvli(builder, esm, 0x1758e4, tier3[:8])  # CrimsonCaravanStoreWeapons
        print("  CCWeapons: +" + str(min(len(tier3), 8)) + " weapons")

    # Save
    builder.save(str(FNV_DATA / "MnehmosMojave.esp"))
    import os
    sz = os.path.getsize(str(FNV_DATA / "MnehmosMojave.esp"))
    print("\nSaved MnehmosMojave.esp (" + str(sz) + " bytes)")


if __name__ == "__main__":
    main()
