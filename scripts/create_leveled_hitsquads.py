"""
Leveled Hit Squads — All factions scale with player level.

ACBS flags:
  bit 7 (0x80) = PC Level Mult (level field becomes multiplier x100)

When PC Level Mult is set:
  level=1000 means 1.0x player level
  level=1100 means 1.1x player level (leader is tougher)
  level=800 means 0.8x (weaker grunts)

Gear is delivered via LVLI leveled item lists that scale with level.
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# Vanilla weapon FormIDs by tier
TIER_LOW = [  # Level 1-10
    (0x08F217, 1),   # 9mm SMG
    (0x04321, 1),    # 10mm SMG
    (0x0FF576, 1),   # Grenade Rifle
]
TIER_MID = [  # Level 10-20
    (0x08F21A, 1),   # Marksman Carbine
    (0x08F219, 1),   # Hunting Shotgun
    (0x08F218, 1),   # Trail Carbine
    (0x1429D1, 1),   # 12.7mm SMG
]
TIER_HIGH = [  # Level 20-30
    (0x092966, 1),   # Anti-Materiel Rifle
    (0x0906DF, 1),   # Light Machine Gun
    (0x04432E, 1),   # Gatling Laser
    (0x08F21B, 1),   # Brush Gun
]
TIER_ELITE = [  # Level 30+
    (0x04432E, 1),   # Gatling Laser
    (0x00433F, 1),   # Minigun
    (0x004340, 1),   # Missile Launcher
    (0x090A6A, 1),   # Grenade Machinegun
]

# Ammo pools
AMMO_BALLISTIC = [
    (0x074ACC, 100),  # 5.56mm
    (0x074ACB, 100),  # 5mm
    (0x096C11, 40),   # 12ga
    (0x074AC8, 40),   # .308
    (0x096C16, 20),   # .50 MG
]
AMMO_ENERGY = [
    (0x074AD1, 200),  # Microfusion Cell
    (0x074AD4, 100),  # Small Energy Cell
    (0x074ACE, 100),  # Electron Charge Pack
]

# Armor by faction
LEGION_ARMOR = 0x0E32F3     # Centurion Armor
LEGION_HELM = 0x12D460      # Centurion Helmet
NCR_RANGER = 0x129254       # NCR Ranger Combat Armor (approximate)
BOS_POWER = 0x0006B466      # Brotherhood T-45d Power Armor


def set_pc_level_mult(acbs_data, multiplier_x100, calc_min=1, calc_max=0):
    """Set PC Level Mult flag and level multiplier on ACBS data."""
    acbs = bytearray(acbs_data)
    # Set PC Level Mult flag (bit 7 of flags byte 0)
    flags = struct.unpack("<I", acbs[0:4])[0]
    flags |= 0x00000080  # PC Level Mult
    struct.pack_into("<I", acbs, 0, flags)
    # Set level multiplier
    struct.pack_into("<h", acbs, 8, multiplier_x100)
    # Set calc min/max
    struct.pack_into("<h", acbs, 10, calc_min)
    struct.pack_into("<h", acbs, 12, calc_max)
    return bytes(acbs)


def create_leveled_weapon_list(builder, edid, tiers):
    """Create a LVLI that gives different weapons at different player levels."""
    fid = builder.allocate_form_id()
    rec = RecordBuilder("LVLI", fid)
    rec.add_string("EDID", edid)
    rec.add(SR.from_bytes("OBND", b"\x00" * 12))
    rec.add(SR.from_bytes("LVLD", struct.pack("<B", 0)))     # Chance none = 0
    rec.add(SR.from_bytes("LVLF", struct.pack("<B", 0x01)))  # CalcAll

    all_entries = []
    for tier_level, items in tiers:
        for item_fid, count in items:
            all_entries.append((tier_level, item_fid, count))

    rec.add(SR.from_bytes("LLCT", struct.pack("<B", len(all_entries))))
    for lvl, item_fid, count in all_entries:
        rec.add_bytes("LVLO", struct.pack("<hHIhH", lvl, 0, item_fid, count, 0))

    builder.add_record("LVLI", rec)
    return fid


def main():
    print("=== Leveled Hit Squads ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "UnlimitedLeveling.esp"))

    # ══════════════════════════════════════════
    # Create leveled weapon lists for each faction
    # ══════════════════════════════════════════
    print("-- Creating leveled weapon lists --")

    legion_weap_fid = create_leveled_weapon_list(builder, "MnLegionHitSquadWeapons", [
        (1, TIER_LOW), (10, TIER_MID), (20, TIER_HIGH), (30, TIER_ELITE),
    ])
    print("  Legion weapons: " + hex(legion_weap_fid))

    legion_ammo_fid = create_leveled_weapon_list(builder, "MnLegionHitSquadAmmo", [
        (1, AMMO_BALLISTIC),
    ])
    print("  Legion ammo: " + hex(legion_ammo_fid))

    ncr_weap_fid = create_leveled_weapon_list(builder, "MnNCRHitSquadWeapons", [
        (1, TIER_LOW), (10, TIER_MID), (20, TIER_HIGH), (30, TIER_ELITE),
    ])
    print("  NCR weapons: " + hex(ncr_weap_fid))

    bos_weap_fid = create_leveled_weapon_list(builder, "MnBOSHitSquadWeapons", [
        (1, [(0x04321, 1)]),     # 10mm SMG early
        (10, [(0x0432E, 1)]),    # Gatling Laser
        (20, [(0x04340, 1)]),    # Missile Launcher
        (30, TIER_ELITE),
    ])
    bos_ammo_fid = create_leveled_weapon_list(builder, "MnBOSHitSquadAmmo", [
        (1, AMMO_ENERGY), (1, [(0x029383, 5)]),  # Missiles
    ])
    print("  BOS weapons: " + hex(bos_weap_fid))

    # ══════════════════════════════════════════
    # LEGION — PC Level Mult + leveled gear
    # ══════════════════════════════════════════
    print("\n-- Legion Assassins (PC Level Mult) --")

    legion_npcs = {
        "VEFR02LegionThugLeaderCM": 1100,   # Leader: 1.1x player level
        "VEFR02LegionThugL01HM": 1000,      # 1.0x
        "VEFR02LegionThug02CM": 1000,        # 1.0x
        "VEFR02LegionThug03HM": 1000,        # 1.0x
        "VEFR02LegionThug04AAM": 900,        # 0.9x (weakest)
    }

    for r in esm.get_records("NPC_"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        if eid not in legion_npcs:
            continue

        mult = legion_npcs[eid]
        rec = RecordBuilder("NPC_", r.id)
        inv_done = False

        for sr in srs:
            if sr.type == "ACBS" and len(sr.data) >= 24:
                new_acbs = set_pc_level_mult(sr.data, mult, calc_min=5, calc_max=50)
                rec.add_bytes("ACBS", new_acbs)
            elif sr.type == "CNTO":
                rec.add(SR.from_bytes(sr.type, sr.data))
                if not inv_done:
                    # Add leveled weapon + ammo + armor
                    rec.add_bytes("CNTO", struct.pack("<Ii", legion_weap_fid, 1))
                    rec.add_bytes("CNTO", struct.pack("<Ii", legion_ammo_fid, 1))
                    rec.add_bytes("CNTO", struct.pack("<Ii", LEGION_ARMOR, 1))
                    rec.add_bytes("CNTO", struct.pack("<Ii", LEGION_HELM, 1))
                    rec.add_bytes("CNTO", struct.pack("<Ii", 0x015169, 3))  # 3 Stimpaks
                    inv_done = True
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_raw_record("NPC_", rec.build())
        print("  " + eid + ": " + str(mult/10) + "x player level, +leveled gear")

    # ══════════════════════════════════════════
    # NCR RANGER — PC Level Mult + leveled gear
    # ══════════════════════════════════════════
    print("\n-- NCR Ranger Hit Squad --")

    for r in esm.get_records("NPC_"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if eid != "VHDAssassinationNCRRanger1":
            continue

        rec = RecordBuilder("NPC_", r.id)
        inv_done = False
        for sr in srs:
            if sr.type == "ACBS" and len(sr.data) >= 24:
                new_acbs = set_pc_level_mult(sr.data, 1100, calc_min=10, calc_max=50)
                rec.add_bytes("ACBS", new_acbs)
            elif sr.type == "CNTO":
                rec.add(SR.from_bytes(sr.type, sr.data))
                if not inv_done:
                    rec.add_bytes("CNTO", struct.pack("<Ii", ncr_weap_fid, 1))
                    rec.add_bytes("CNTO", struct.pack("<Ii", legion_ammo_fid, 1))  # Same ammo pool
                    rec.add_bytes("CNTO", struct.pack("<Ii", 0x015169, 5))  # 5 Stimpaks
                    inv_done = True
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))
        builder.add_raw_record("NPC_", rec.build())
        print("  NCR Ranger: 1.1x player level, +leveled weapons, +5 stimpaks")
        break

    # ══════════════════════════════════════════
    # BROTHERHOOD — PC Level Mult + heavy energy
    # ══════════════════════════════════════════
    print("\n-- Brotherhood Paladin Hit Squad --")

    bos_npcs = ["HVPaladinHitSquad1", "HVPaladinHitSquad2", "HVPaladinHitSquad3",
                "HVPaladinHitSquad4", "HVPaladinHitSquadRandom"]

    for r in esm.get_records("NPC_"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        if eid not in bos_npcs:
            continue

        mult = 1100 if "Random" not in eid else 1200  # Random paladin is tougher
        rec = RecordBuilder("NPC_", r.id)
        inv_done = False

        for sr in srs:
            if sr.type == "ACBS" and len(sr.data) >= 24:
                new_acbs = set_pc_level_mult(sr.data, mult, calc_min=10, calc_max=50)
                rec.add_bytes("ACBS", new_acbs)
            elif sr.type == "CNTO":
                rec.add(SR.from_bytes(sr.type, sr.data))
                if not inv_done:
                    rec.add_bytes("CNTO", struct.pack("<Ii", bos_weap_fid, 1))
                    rec.add_bytes("CNTO", struct.pack("<Ii", bos_ammo_fid, 1))
                    rec.add_bytes("CNTO", struct.pack("<Ii", 0x015169, 5))
                    inv_done = True
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_raw_record("NPC_", rec.build())
        print("  " + eid + ": " + str(mult/10) + "x player level, +leveled energy weapons")

    # Save
    builder.save(str(FNV_DATA / "UnlimitedLeveling.esp"))
    import os
    print("\nSaved: " + str(os.path.getsize(str(FNV_DATA / "UnlimitedLeveling.esp"))) + " bytes")


if __name__ == "__main__":
    main()
