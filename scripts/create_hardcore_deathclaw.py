"""
Hardcore Deathclaw — The Mojave Becomes Terrifying

- All deathclaw HP x3
- All deathclaw damage x2
- Deathclaw LVLC lists boosted: packs of 4-6 instead of 1-2
- Deathclaw loot massively improved: rare weapons, high-value hides, eggs
- New apex variant: "Primordial Deathclaw" (2000 HP, 500 dmg, level 50)
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")


def main():
    print("=== Hardcore Deathclaw ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))

    builder = ESPBuilder(author="Mnehmos", description="Hardcore Deathclaw - 3x HP, 2x DMG, pack spawns, better loot")
    builder.add_master("FalloutNV.esm")

    # ══════════════════════════════════════════
    # 1. BUFF ALL DEATHCLAWS — 3x HP, 2x DMG
    # ══════════════════════════════════════════
    print("-- Buffing Deathclaws (3x HP, 2x DMG) --")

    buffed = 0
    for r in esm.get_records("CREA"):
        srs = r.parse_subrecords()
        eid = name = ""
        has_data = False
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
            if sr.type == "FULL":
                name = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
            if sr.type == "DATA" and len(sr.data) >= 10:
                has_data = True

        if not ("deathclaw" in eid.lower() or "DeathClaw" in eid):
            continue
        if "Audio" in eid or "Template" in eid:
            continue
        if not has_data:
            continue

        # Override the creature with buffed stats
        rec = RecordBuilder("CREA", r.id)
        for sr in srs:
            if sr.type == "DATA" and len(sr.data) >= 10:
                data = bytearray(sr.data)
                # HP at offset 4 (uint16)
                old_hp = struct.unpack("<H", data[4:6])[0]
                new_hp = min(old_hp * 3, 65535)
                struct.pack_into("<H", data, 4, new_hp)
                # Damage at offset 8 (uint16)
                old_dmg = struct.unpack("<H", data[8:10])[0]
                new_dmg = min(old_dmg * 2, 65535)
                struct.pack_into("<H", data, 8, new_dmg)
                rec.add_bytes("DATA", bytes(data))
            elif sr.type == "ACBS" and len(sr.data) >= 16:
                # Boost speed by 20%
                acbs = bytearray(sr.data)
                old_speed = struct.unpack("<H", acbs[14:16])[0]
                new_speed = min(int(old_speed * 1.2), 65535)
                struct.pack_into("<H", acbs, 14, new_speed)
                rec.add_bytes("ACBS", bytes(acbs))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_raw_record("CREA", rec.build())
        if name:
            buffed += 1

    print("  Buffed " + str(buffed) + " deathclaw variants")

    # ══════════════════════════════════════════
    # 2. PACK SPAWNS — More per encounter
    # ══════════════════════════════════════════
    print("\n-- Pack Spawns (count +2-3) --")

    pack_boosted = 0
    for r in esm.get_records("LVLC"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        if not ("deathclaw" in eid.lower() or "DeathClaw" in eid):
            continue

        entry_count = sum(1 for sr in srs if sr.type == "LVLO")
        if entry_count == 0:
            continue

        rec = RecordBuilder("LVLC", r.id)
        for sr in srs:
            if sr.type == "LVLF":
                # Enable CalcAll + CalcEach
                rec.add(SR.from_bytes("LVLF", struct.pack("<B", 0x03)))
            elif sr.type == "LVLO" and len(sr.data) >= 10:
                level = struct.unpack("<h", sr.data[:2])[0]
                unused1 = struct.unpack("<H", sr.data[2:4])[0]
                fid = struct.unpack("<I", sr.data[4:8])[0]
                count = struct.unpack("<h", sr.data[8:10])[0]
                unused2 = struct.unpack("<H", sr.data[10:12])[0] if len(sr.data) >= 12 else 0
                # Add 2-3 more per entry
                new_count = count + 3
                rec.add_bytes("LVLO", struct.pack("<hHIhH", level, unused1, fid, new_count, unused2))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_raw_record("LVLC", rec.build())
        pack_boosted += 1

    print("  Boosted " + str(pack_boosted) + " deathclaw spawn lists (+3 per entry)")

    # ══════════════════════════════════════════
    # 3. BETTER LOOT — Deathclaw drops improved
    # ══════════════════════════════════════════
    print("\n-- Better Loot --")

    # Override DeathItemDeathClaw100 (0x5329F) — add more items
    # Original has 3 entries. Add: Deathclaw Hand (always), more eggs, caps
    DEATHCLAW_HAND = 0x160FF8   # DeathclawHand misc item
    DEATHCLAW_EGG = 0x1735EB    # DeathclawEgg
    CAPS_001 = 0x00000F          # Caps

    for r in esm.get_records("LVLI"):
        if r.id == 0x5329F:  # DeathItemDeathClaw100
            srs = r.parse_subrecords()
            rec = RecordBuilder("LVLI", r.id)
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    # Add 3 more entries
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", old_count + 3)))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))

            # Deathclaw Hand (100% drop, was 15-35%)
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, DEATHCLAW_HAND, 2, 0))
            # Extra egg
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, DEATHCLAW_EGG, 1, 0))
            # Caps (50-150)
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, CAPS_001, 100, 0))

            builder.add_raw_record("LVLI", rec.build())
            print("  DeathItemDeathClaw100: +2 hands, +1 egg, +100 caps")
            break

    # Override DeathItemDeathClawMother100 (0x17B5C9) — mother drops more
    for r in esm.get_records("LVLI"):
        if r.id == 0x17B5C9:
            srs = r.parse_subrecords()
            rec = RecordBuilder("LVLI", r.id)
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", old_count + 3)))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))

            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, DEATHCLAW_HAND, 3, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, DEATHCLAW_EGG, 3, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, CAPS_001, 200, 0))

            builder.add_raw_record("LVLI", rec.build())
            print("  DeathItemDeathClawMother100: +3 hands, +3 eggs, +200 caps")
            break

    # ══════════════════════════════════════════
    # 4. PRIMORDIAL DEATHCLAW — New apex variant
    # ══════════════════════════════════════════
    print("\n-- Primordial Deathclaw (New Apex) --")

    # Clone from Legendary Deathclaw (0x167EFF)
    legendary = None
    for r in esm.get_records("CREA"):
        if r.id == 0x167EFF:
            legendary = r.parse_subrecords()
            break

    if legendary:
        fid = builder.allocate_form_id()
        rec = RecordBuilder("CREA", fid)

        for sr in legendary:
            if sr.type == "EDID":
                rec.add_string("EDID", "MnPrimordialDeathclaw")
            elif sr.type == "FULL":
                rec.add_string("FULL", "Primordial Deathclaw")
            elif sr.type == "DATA" and len(sr.data) >= 17:
                data = bytearray(sr.data)
                # HP: 3000
                struct.pack_into("<H", data, 4, 3000)
                # Damage: 500
                struct.pack_into("<H", data, 8, 500)
                # Max SPECIAL
                for i in range(7):
                    data[10 + i] = 10
                rec.add_bytes("DATA", bytes(data))
            elif sr.type == "ACBS" and len(sr.data) >= 24:
                acbs = bytearray(sr.data)
                # Level 50
                struct.pack_into("<h", acbs, 8, 50)
                # Speed 200
                struct.pack_into("<H", acbs, 14, 200)
                rec.add_bytes("ACBS", bytes(acbs))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_record("CREA", rec)
        print("  Primordial Deathclaw: 3000 HP, 500 DMG, Level 50, Speed 200")
        print("  FormID: " + hex(fid))

        # Add to tier 5 deathclaw lists
        for r in esm.get_records("LVLC"):
            srs = r.parse_subrecords()
            eid = ""
            for sr in srs:
                if sr.type == "EDID":
                    eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
            if eid in ("VEncTier4DeathclawMed", "VEncDeathclawTier1"):
                rec2 = RecordBuilder("LVLC", r.id)
                old_count = 0
                for sr in srs:
                    if sr.type == "LLCT":
                        old_count = sr.data[0]
                        rec2.add(SR.from_bytes("LLCT", struct.pack("<B", old_count + 1)))
                    else:
                        rec2.add(SR.from_bytes(sr.type, sr.data))
                rec2.add_bytes("LVLO", struct.pack("<hHIhH", 35, 0, fid, 1, 0))
                builder.add_raw_record("LVLC", rec2.build())
                print("  Added to " + eid + " (level 35+)")

    # ══════════════════════════════════════════
    # SAVE
    # ══════════════════════════════════════════
    outpath = FNV_DATA / "HardcoreDeathclaw.esp"
    builder.save(str(outpath))

    import os
    sz = os.path.getsize(str(outpath))
    print("\nSaved: " + str(outpath) + " (" + str(sz) + " bytes)")
    print("\nAdd to plugins.txt: HardcoreDeathclaw.esp")


if __name__ == "__main__":
    main()
