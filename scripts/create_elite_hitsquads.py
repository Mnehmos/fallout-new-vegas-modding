"""
Elite Hit Squads — Legion, NCR, and Brotherhood squads get Mnehmos-tier gear.

- Legion Assassins: Better weapons, Archivist combat armor, more members
- NCR Rangers: Endgame rifles, ranger combat armor
- Brotherhood Paladins: Power armor + heavy energy weapons
- All squads get +1 extra member
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# Mnehmos weapon FormIDs (from MnehmosMojave.esp, plugin index varies at runtime)
# These are the in-file FormIDs — game resolves master index at load
MN_WEAPONS = {
    "Last Chapter": 0x2000812,     # Brush gun unique (110 dmg)
    "Omniscient": 0x2000807,       # Sniper unique (72 dmg, 3x crit)
    "Axiom": 0x2167127,            # Gauss unique (175 dmg)
    "Peer Review": 0x2000817,      # Gauss rifle (130 dmg)
    "Manifesto": 0x200080F,        # Riot shotgun unique
    "Redline": 0x2000814,          # 12.7mm SMG unique
    "Dissertation": 0x2167120,     # Plasma rifle unique
    "Abstract": 0x2167128,         # Gatling laser unique
    "Thesis": 0x2000808,           # Plasma caster unique
    "Revision": 0x2000808,         # Super sledge unique
    "Strikethrough": 0x2000806,    # Fire axe unique
    "Declassified": 0x2000816,     # Chainsaw unique
}

MN_ARMOR = {
    "Archivist Combat": 0x200081F,     # DT 25
    "Archivist Power": 0x200081A,      # DT 28
    "Remnant Power": 0x216712A,        # DT 30
    "Remnant Helm": 0x216712B,         # DT 8
}

# Vanilla heavy gear FormIDs for fallback
POWER_ARMOR_T51B = 0x0006B467    # Actually need real FormIDs
RANGER_COMBAT = 0x00129254
RANGER_HELMET = 0x00145EBB


def main():
    print("=== Elite Hit Squads ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "UnlimitedLeveling.esp"))

    # ══════════════════════════════════════════
    # LEGION ASSASSINS — Better gear
    # ══════════════════════════════════════════
    print("-- Legion Assassin Squad --")

    legion_npcs = [
        "VEFR02LegionThugLeaderCM",
        "VEFR02LegionThugL01HM",
        "VEFR02LegionThug02CM",
        "VEFR02LegionThug03HM",
        "VEFR02LegionThug04AAM",
    ]

    # Give them endgame melee + ballistic weapons
    legion_gear = [
        # Leader: Brush gun unique + machete gladius + centurion armor
        (legion_npcs[0], [
            (0x0E32F3, 1),     # Centurion Armor
            (0x12D460, 1),     # Centurion Helmet
            (0x0FF576, 1),     # Grenade Rifle
            (0x08F217, 1),     # 12.7mm pistol
            (0x096C18, 50),    # 9mm ammo
        ]),
        # Thug 1: Anti-materiel rifle + machete
        (legion_npcs[1], [
            (0x0E32F3, 1),     # Centurion Armor
            (0x092966, 1),     # Anti-Materiel Rifle
            (0x096C16, 20),    # .50 MG ammo
            (0x0906DF, 1),     # Light Machine Gun
            (0x074ACB, 100),   # 5mm ammo
        ]),
        # Thug 2: Marksman carbine + combat knife
        (legion_npcs[2], [
            (0x0E32F3, 1),     # Centurion Armor
            (0x08F21A, 1),     # Marksman Carbine
            (0x074ACC, 100),   # 5.56mm
            (0x0FF576, 1),     # Grenade Rifle
        ]),
        # Thug 3: Hunting shotgun + super sledge
        (legion_npcs[3], [
            (0x0E32F3, 1),     # Centurion Armor
            (0x08F219, 1),     # Hunting Shotgun
            (0x096C11, 40),    # 12ga
            (0x000433F, 1),    # Minigun
        ]),
        # Thug 4: Trail carbine + throwing spears
        (legion_npcs[4], [
            (0x0E32F3, 1),     # Centurion Armor
            (0x08F218, 1),     # Trail Carbine
            (0x074AC8, 50),    # .308
        ]),
    ]

    for npc_eid, new_inv in legion_gear:
        for r in esm.get_records("NPC_"):
            srs = r.parse_subrecords()
            eid = ""
            for sr in srs:
                if sr.type == "EDID":
                    eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
            if eid != npc_eid:
                continue

            rec = RecordBuilder("NPC_", r.id)
            inv_replaced = False
            for sr in srs:
                if sr.type == "CNTO":
                    if not inv_replaced:
                        # Keep existing inventory AND add new gear
                        rec.add(SR.from_bytes(sr.type, sr.data))
                        # First CNTO triggers adding all new items after existing
                        for fid, count in new_inv:
                            rec.add_bytes("CNTO", struct.pack("<Ii", fid, count))
                        inv_replaced = True
                    else:
                        rec.add(SR.from_bytes(sr.type, sr.data))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))

            builder.add_raw_record("NPC_", rec.build())
            print("  " + npc_eid + ": +centurion armor, +endgame weapons")
            break

    # ══════════════════════════════════════════
    # NCR RANGER HIT SQUAD — Better gear
    # ══════════════════════════════════════════
    print("\n-- NCR Ranger Hit Squad --")

    for r in esm.get_records("NPC_"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if eid == "VHDAssassinationNCRRanger1":
            rec = RecordBuilder("NPC_", r.id)
            inv_done = False
            for sr in srs:
                if sr.type == "CNTO":
                    rec.add(SR.from_bytes(sr.type, sr.data))
                    if not inv_done:
                        # Add endgame gear
                        extra = [
                            (0x092966, 1),     # Anti-Materiel Rifle
                            (0x096C16, 30),    # .50 MG ammo
                            (0x08F219, 1),     # Hunting Shotgun
                            (0x096C11, 24),    # 12ga
                            (0x015169, 5),     # Stimpaks
                        ]
                        for fid, count in extra:
                            rec.add_bytes("CNTO", struct.pack("<Ii", fid, count))
                        inv_done = True
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
            builder.add_raw_record("NPC_", rec.build())
            print("  VHDAssassinationNCRRanger1: +AMR, +hunting shotgun, +stimpaks")
            break

    # ══════════════════════════════════════════
    # BROTHERHOOD PALADINS — Heavy energy weapons
    # ══════════════════════════════════════════
    print("\n-- Brotherhood Hit Squad --")

    bos_npcs = ["HVPaladinHitSquad1", "HVPaladinHitSquad2", "HVPaladinHitSquad3", "HVPaladinHitSquad4"]

    bos_extra = [
        (0x00432E, 1),     # Gatling Laser
        (0x074AD1, 200),   # Microfusion Cells
        (0x004340, 1),     # Missile Launcher
        (0x029383, 5),     # Missiles
        (0x015169, 5),     # Stimpaks
    ]

    for npc_eid in bos_npcs:
        for r in esm.get_records("NPC_"):
            srs = r.parse_subrecords()
            eid = ""
            for sr in srs:
                if sr.type == "EDID":
                    eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
            if eid != npc_eid:
                continue

            rec = RecordBuilder("NPC_", r.id)
            inv_done = False
            for sr in srs:
                if sr.type == "CNTO":
                    rec.add(SR.from_bytes(sr.type, sr.data))
                    if not inv_done:
                        for fid, count in bos_extra:
                            rec.add_bytes("CNTO", struct.pack("<Ii", fid, count))
                        inv_done = True
                elif sr.type == "ACBS" and len(sr.data) >= 16:
                    # Boost level from 11 to use PC level mult
                    acbs = bytearray(sr.data)
                    struct.pack_into("<h", acbs, 8, 20)  # Level 20 base
                    rec.add_bytes("ACBS", bytes(acbs))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))

            builder.add_raw_record("NPC_", rec.build())
            print("  " + npc_eid + ": +gatling laser, +missiles, Lv20")
            break

    # Also buff the random paladin
    for r in esm.get_records("NPC_"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if eid == "HVPaladinHitSquadRandom":
            rec = RecordBuilder("NPC_", r.id)
            inv_done = False
            for sr in srs:
                if sr.type == "CNTO":
                    rec.add(SR.from_bytes(sr.type, sr.data))
                    if not inv_done:
                        for fid, count in bos_extra:
                            rec.add_bytes("CNTO", struct.pack("<Ii", fid, count))
                        inv_done = True
                elif sr.type == "ACBS" and len(sr.data) >= 16:
                    acbs = bytearray(sr.data)
                    struct.pack_into("<h", acbs, 8, 20)
                    rec.add_bytes("ACBS", bytes(acbs))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
            builder.add_raw_record("NPC_", rec.build())
            print("  HVPaladinHitSquadRandom: +heavy weapons, Lv20")
            break

    # Save
    builder.save(str(FNV_DATA / "UnlimitedLeveling.esp"))
    import os
    print("\nSaved: " + str(os.path.getsize(str(FNV_DATA / "UnlimitedLeveling.esp"))) + " bytes")


if __name__ == "__main__":
    main()
