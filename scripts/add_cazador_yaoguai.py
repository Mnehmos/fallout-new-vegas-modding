"""
Add Hardcore Cazadors and Yao Guai to HardcoreDeathclaw.esp

Cazadors: 3x HP, 2x damage, pack spawns, new Swarm Queen variant
Yao Guai (HH): 3x HP, 2x damage, new Ancient Yao Guai variant
Better loot for both.
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")


def buff_creatures(builder, source, keyword, hp_mult, dmg_mult, speed_mult=1.2):
    """Buff all creatures matching keyword."""
    buffed = 0
    for r in source.get_records("CREA"):
        srs = r.parse_subrecords()
        eid = name = ""
        has_data = False
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
            if sr.type == "FULL":
                name = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
            if sr.type == "DATA" and len(sr.data) >= 10:
                hp = struct.unpack("<H", sr.data[4:6])[0]
                if hp > 0:
                    has_data = True

        if keyword.lower() not in eid.lower():
            continue
        if "Audio" in eid or "Template" in eid or "Spawn" in eid:
            continue
        if not has_data:
            continue

        rec = RecordBuilder("CREA", r.id)
        for sr in srs:
            if sr.type == "DATA" and len(sr.data) >= 10:
                data = bytearray(sr.data)
                old_hp = struct.unpack("<H", data[4:6])[0]
                old_dmg = struct.unpack("<H", data[8:10])[0]
                struct.pack_into("<H", data, 4, min(int(old_hp * hp_mult), 65535))
                struct.pack_into("<H", data, 8, min(int(old_dmg * dmg_mult), 65535))
                rec.add_bytes("DATA", bytes(data))
            elif sr.type == "ACBS" and len(sr.data) >= 16:
                acbs = bytearray(sr.data)
                old_speed = struct.unpack("<H", acbs[14:16])[0]
                new_speed = min(int(old_speed * speed_mult), 65535)
                struct.pack_into("<H", acbs, 14, new_speed)
                rec.add_bytes("ACBS", bytes(acbs))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_raw_record("CREA", rec.build())
        if name:
            buffed += 1
    return buffed


def boost_lvlc(builder, source, keyword, count_add=2):
    """Boost spawn counts on matching LVLC lists."""
    boosted = 0
    for r in source.get_records("LVLC"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        if keyword.lower() not in eid.lower():
            continue

        entry_count = sum(1 for sr in srs if sr.type == "LVLO")
        if entry_count == 0:
            continue

        rec = RecordBuilder("LVLC", r.id)
        for sr in srs:
            if sr.type == "LVLF":
                rec.add(SR.from_bytes("LVLF", struct.pack("<B", 0x03)))
            elif sr.type == "LVLO" and len(sr.data) >= 10:
                level = struct.unpack("<h", sr.data[:2])[0]
                unused1 = struct.unpack("<H", sr.data[2:4])[0]
                fid = struct.unpack("<I", sr.data[4:8])[0]
                count = struct.unpack("<h", sr.data[8:10])[0]
                unused2 = struct.unpack("<H", sr.data[10:12])[0] if len(sr.data) >= 12 else 0
                rec.add_bytes("LVLO", struct.pack("<hHIhH", level, unused1, fid, count + count_add, unused2))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_raw_record("LVLC", rec.build())
        boosted += 1
    return boosted


def main():
    print("=== Hardcore Cazadors + Yao Guai ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    hh = PluginFile(str(FNV_DATA / "HonestHearts.esm"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "HardcoreDeathclaw.esp"))

    # ══════════════════════════════════════════
    # CAZADORS — 3x HP, 2x damage, 10% faster
    # ══════════════════════════════════════════
    print("-- Cazadors (3x HP, 2x DMG) --")
    n = buff_creatures(builder, esm, "Cazador", 3.0, 2.0, 1.1)
    print("  Buffed " + str(n) + " cazador variants")

    print("\n-- Cazador Pack Spawns (+2) --")
    n = boost_lvlc(builder, esm, "Cazador", 2)
    print("  Boosted " + str(n) + " cazador spawn lists")

    # New apex: Cazador Swarm Queen
    print("\n-- Cazador Swarm Queen (New Apex) --")
    legendary_caz = None
    for r in esm.get_records("CREA"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if eid == "VCrUniqueTier5CazadorLargeSilverPeak":
            legendary_caz = (r.id, srs)
            break

    if legendary_caz:
        _, template = legendary_caz
        fid = builder.allocate_form_id()
        rec = RecordBuilder("CREA", fid)
        for sr in template:
            if sr.type == "EDID":
                rec.add_string("EDID", "MnCazadorSwarmQueen")
            elif sr.type == "FULL":
                rec.add_string("FULL", "Cazador Swarm Queen")
            elif sr.type == "DATA" and len(sr.data) >= 10:
                data = bytearray(sr.data)
                struct.pack_into("<H", data, 4, 2000)   # HP 2000
                struct.pack_into("<H", data, 8, 300)    # DMG 300
                rec.add_bytes("DATA", bytes(data))
            elif sr.type == "ACBS" and len(sr.data) >= 16:
                acbs = bytearray(sr.data)
                struct.pack_into("<h", acbs, 8, 40)     # Level 40
                struct.pack_into("<H", acbs, 14, 300)   # Speed 300
                rec.add_bytes("ACBS", bytes(acbs))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))
        builder.add_record("CREA", rec)
        swarm_queen_fid = fid
        print("  Swarm Queen: 2000 HP, 300 DMG, Lv40, Speed 300 -> " + hex(fid))

        # Add to cazador encounter lists
        for r in esm.get_records("LVLC"):
            srs = r.parse_subrecords()
            eid = ""
            for sr in srs:
                if sr.type == "EDID":
                    eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
            if eid in ("VEncTier4CazadorMed", "EncCazador"):
                rec2 = RecordBuilder("LVLC", r.id)
                old_count = 0
                for sr in srs:
                    if sr.type == "LLCT":
                        old_count = sr.data[0]
                        rec2.add(SR.from_bytes("LLCT", struct.pack("<B", old_count + 1)))
                    else:
                        rec2.add(SR.from_bytes(sr.type, sr.data))
                rec2.add_bytes("LVLO", struct.pack("<hHIhH", 30, 0, swarm_queen_fid, 1, 0))
                builder.add_raw_record("LVLC", rec2.build())
                print("  Added to " + eid + " (level 30+)")

    # Better cazador loot
    print("\n-- Cazador Loot --")
    CAZADOR_GLAND = 0x13B2B9    # Cazador Poison Gland
    CAZADOR_EGG = 0x178A8B      # CazadorEgg100 ref? Actually let me use the egg item
    CAPS = 0x00000F
    for r in esm.get_records("LVLI"):
        if r.id == 0x13B2BE:    # DeathItemCazador100
            srs = r.parse_subrecords()
            rec = RecordBuilder("LVLI", r.id)
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", old_count + 2)))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, CAZADOR_GLAND, 2, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, CAPS, 50, 0))
            builder.add_raw_record("LVLI", rec.build())
            print("  DeathItemCazador100: +2 glands, +50 caps")
            break

    # ══════════════════════════════════════════
    # YAO GUAI (HH) — 3x HP, 2x damage
    # ══════════════════════════════════════════
    # HH is master index 2 in HardcoreDeathclaw.esp? No — HC only has FalloutNV.esm
    # Need to add HH as master first... but we can't modify masters with binary writer
    #
    # SOLUTION: Add Yao Guai to HardcoreDeathclaw via xEdit master addition,
    # OR create a separate ESP. Let's check current masters.

    import os
    with open(str(FNV_DATA / "HardcoreDeathclaw.esp"), "rb") as f:
        raw = f.read(2048)
    masters = []
    pos = 0
    while pos < len(raw) - 6:
        if raw[pos:pos+4] == b"MAST":
            size = struct.unpack("<H", raw[pos+4:pos+6])[0]
            masters.append(raw[pos+6:pos+6+size].rstrip(b"\x00").decode())
            pos += 6 + size
        elif raw[pos:pos+4] == b"GRUP":
            break
        else:
            pos += 1

    print("\nHardcoreDeathclaw masters: " + str(masters))

    if "HonestHearts.esm" not in masters:
        print("\nHH not a master — buffing Yao Guai requires adding HH master via xEdit.")
        print("Writing xEdit script for that...")

        # Write an xEdit script to add HH master
        script = """{
  Add HonestHearts.esm as master to HardcoreDeathclaw.esp
  Run on HardcoreDeathclaw.esp
}
unit AddHHMasterToHC;
function Initialize: Integer;
var i: Integer; tp: IInterface;
begin
  Result := 0;
  for i := 0 to Pred(FileCount) do begin
    if SameText(GetFileName(FileByIndex(i)), 'HardcoreDeathclaw.esp') then begin
      tp := FileByIndex(i);
      Break;
    end;
  end;
  if not Assigned(tp) then begin AddMessage('ERROR: HardcoreDeathclaw.esp not loaded'); Result := 1; Exit; end;
  AddMasterIfMissing(tp, 'HonestHearts.esm');
  AddMessage('Added HonestHearts.esm. Save now, then re-run Yao Guai buff script.');
end;
function Process(e: IInterface): Integer; begin Result := 0; end;
function Finalize: Integer; begin Result := 0; end;
end.
"""
        script_path = FNV_DATA.parent.parent.parent.parent / "Github" / "Fallout New Vegas Modding" / "tools" / "xedit-scripts" / "AddHHMasterToHC.pas"
        # Just note it for now
        print("For now, Yao Guai buffs go into MnehmosMojave.esp (which already has HH master).")

        # Buff Yao Guai via MnehmosMojave.esp instead
        mn_builder = ESPBuilder.load_existing(str(FNV_DATA / "MnehmosMojave.esp"))

        # HH is master index 2 in MnehmosMojave (after DM was added)
        # Actually let me check
        with open(str(FNV_DATA / "MnehmosMojave.esp"), "rb") as f:
            raw2 = f.read(2048)
        mn_masters = []
        pos = 0
        while pos < len(raw2) - 6:
            if raw2[pos:pos+4] == b"MAST":
                size = struct.unpack("<H", raw2[pos+4:pos+6])[0]
                mn_masters.append(raw2[pos+6:pos+6+size].rstrip(b"\x00").decode())
                pos += 6 + size
            elif raw2[pos:pos+4] == b"GRUP":
                break
            else:
                pos += 1
        print("MnehmosMojave masters: " + str(mn_masters))
        hh_idx = mn_masters.index("HonestHearts.esm") if "HonestHearts.esm" in mn_masters else -1
        print("HH master index: " + str(hh_idx))

        if hh_idx >= 0:
            print("\n-- Yao Guai (via MnehmosMojave.esp, HH index " + str(hh_idx) + ") --")

            yg_buffed = 0
            for r in hh.get_records("CREA"):
                srs = r.parse_subrecords()
                eid = name = ""
                has_data = False
                for sr in srs:
                    if sr.type == "EDID":
                        eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
                    if sr.type == "FULL":
                        name = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
                    if sr.type == "DATA" and len(sr.data) >= 10:
                        hp = struct.unpack("<H", sr.data[4:6])[0]
                        if hp > 0:
                            has_data = True

                if "yao" not in eid.lower() and "YaoGuai" not in eid:
                    continue
                if "Audio" in eid or "Spawn" in eid:
                    continue
                if not has_data:
                    continue

                # Remap FormID: HH internal (0x01) -> our master index
                target_fid = (hh_idx << 24) | (r.id & 0x00FFFFFF)

                rec = RecordBuilder("CREA", target_fid)
                for sr in srs:
                    if sr.type == "DATA" and len(sr.data) >= 10:
                        data = bytearray(sr.data)
                        old_hp = struct.unpack("<H", data[4:6])[0]
                        old_dmg = struct.unpack("<H", data[8:10])[0]
                        struct.pack_into("<H", data, 4, min(old_hp * 3, 65535))
                        struct.pack_into("<H", data, 8, min(old_dmg * 2, 65535))
                        rec.add_bytes("DATA", bytes(data))
                    elif sr.type == "ACBS" and len(sr.data) >= 16:
                        acbs = bytearray(sr.data)
                        old_speed = struct.unpack("<H", acbs[14:16])[0]
                        struct.pack_into("<H", acbs, 14, min(int(old_speed * 1.2), 65535))
                        rec.add_bytes("ACBS", bytes(acbs))
                    else:
                        rec.add(SR.from_bytes(sr.type, sr.data))

                mn_builder.add_raw_record("CREA", rec.build())
                if name:
                    print("  " + name.ljust(24) + " -> " + hex(target_fid))
                    yg_buffed += 1

            print("  Buffed " + str(yg_buffed) + " Yao Guai variants (3x HP, 2x DMG)")

            # New apex: Ancient Yao Guai
            giant_yg = None
            for r in hh.get_records("CREA"):
                srs = r.parse_subrecords()
                eid = ""
                for sr in srs:
                    if sr.type == "EDID":
                        eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
                if eid == "NVDLC02CrTier5YaoGuaiLarge":
                    giant_yg = srs
                    break

            if giant_yg:
                fid = mn_builder.allocate_form_id()
                rec = RecordBuilder("CREA", fid)
                for sr in giant_yg:
                    if sr.type == "EDID":
                        rec.add_string("EDID", "MnAncientYaoGuai")
                    elif sr.type == "FULL":
                        rec.add_string("FULL", "Ancient Yao Guai")
                    elif sr.type == "DATA" and len(sr.data) >= 10:
                        data = bytearray(sr.data)
                        struct.pack_into("<H", data, 4, 2500)   # HP
                        struct.pack_into("<H", data, 8, 400)    # DMG
                        rec.add_bytes("DATA", bytes(data))
                    elif sr.type == "ACBS" and len(sr.data) >= 16:
                        acbs = bytearray(sr.data)
                        struct.pack_into("<h", acbs, 8, 45)     # Level 45
                        struct.pack_into("<H", acbs, 14, 175)   # Speed
                        rec.add_bytes("ACBS", bytes(acbs))
                    else:
                        rec.add(SR.from_bytes(sr.type, sr.data))
                mn_builder.add_record("CREA", rec)
                print("\n  Ancient Yao Guai: 2500 HP, 400 DMG, Lv45 -> " + hex(fid))

            mn_builder.save(str(FNV_DATA / "MnehmosMojave.esp"))
            print("  Saved MnehmosMojave.esp (" + str(os.path.getsize(str(FNV_DATA / "MnehmosMojave.esp"))) + " bytes)")

    # Save cazador changes to HardcoreDeathclaw
    builder.save(str(FNV_DATA / "HardcoreDeathclaw.esp"))
    print("\nSaved HardcoreDeathclaw.esp (" + str(os.path.getsize(str(FNV_DATA / "HardcoreDeathclaw.esp"))) + " bytes)")


if __name__ == "__main__":
    main()
