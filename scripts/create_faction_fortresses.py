"""
Faction Fortresses — All major faction bases get reinforced.

Every faction LVLN list: +2 count per entry + CalcEach for variety.
Makes Red Rock Canyon, Hidden Valley, Vault 3, Camp McCarran,
The Fort, and NCRCF genuinely dangerous to assault.
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")


def boost_faction_lists(builder, esm, keywords, count_add, faction_name):
    """Boost all LVLN lists matching keywords."""
    boosted = 0
    for r in esm.get_records("LVLN"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        if not any(kw in eid for kw in keywords):
            continue

        entry_count = sum(1 for sr in srs if sr.type == "LVLO")
        if entry_count == 0:
            continue

        rec = RecordBuilder("LVLN", r.id)
        for sr in srs:
            if sr.type == "LVLF":
                old = sr.data[0]
                rec.add(SR.from_bytes("LVLF", struct.pack("<B", old | 0x03)))
            elif sr.type == "LLCT":
                rec.add(SR.from_bytes("LLCT", sr.data))
            elif sr.type == "LVLO" and len(sr.data) >= 10:
                level = struct.unpack("<h", sr.data[:2])[0]
                unused1 = struct.unpack("<H", sr.data[2:4])[0]
                fid = struct.unpack("<I", sr.data[4:8])[0]
                count = struct.unpack("<h", sr.data[8:10])[0]
                unused2 = struct.unpack("<H", sr.data[10:12])[0] if len(sr.data) >= 12 else 0
                new_count = count + count_add
                rec.add_bytes("LVLO", struct.pack("<hHIhH", level, unused1, fid, new_count, unused2))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_raw_record("LVLN", rec.build())
        boosted += 1
    return boosted


def main():
    print("=== Faction Fortresses ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "WorldAtmosphere.esp"))

    # Great Khans — Red Rock Canyon
    print("-- Great Khans (Red Rock Canyon) --")
    n = boost_faction_lists(builder, esm,
        ["GreatKhan", "VRRCGreatKhan", "VHDGreatKhan", "Khan"],
        count_add=2, faction_name="Great Khans")
    print("  Boosted " + str(n) + " lists (+2 per entry)")

    # Fiends — Vault 3 / Outer Vegas
    print("\n-- Fiends (Vault 3 / Outer Vegas) --")
    n = boost_faction_lists(builder, esm,
        ["Fiend", "VarFiend", "EncFiend", "OVFiend"],
        count_add=2, faction_name="Fiends")
    print("  Boosted " + str(n) + " lists (+2 per entry)")

    # Brotherhood of Steel — Hidden Valley
    print("\n-- Brotherhood of Steel (Hidden Valley) --")
    n = boost_faction_lists(builder, esm,
        ["Brotherhood", "VarBrotherhood", "EncBrotherhood", "HVBrotherhood", "VHDBrotherhood", "HVPaladin"],
        count_add=2, faction_name="Brotherhood")
    print("  Boosted " + str(n) + " lists (+2 per entry)")

    # NCR — Camp McCarran / Hoover Dam / Outposts
    print("\n-- NCR (McCarran / Hoover / Outposts) --")
    n = boost_faction_lists(builder, esm,
        ["VarNCR", "EncNCR", "VHDNCRTrooper", "VHDNCRRanger", "VHDNCREngineer",
         "NCRHeavy", "NCRRanger", "NCRTrooper"],
        count_add=2, faction_name="NCR")
    print("  Boosted " + str(n) + " lists (+2 per entry)")

    # Legion — The Fort / Cottonwood Cove / Nelson
    print("\n-- Caesar's Legion (The Fort / Cottonwood / Nelson) --")
    n = boost_faction_lists(builder, esm,
        ["Legion", "VarLegion", "EncVHDCL", "VHDCLLegionary", "FortLegionary",
         "LegateCamp", "VarVanGraffLegion"],
        count_add=2, faction_name="Legion")
    print("  Boosted " + str(n) + " lists (+2 per entry)")

    # Powder Gangers — NCRCF / Primm
    print("\n-- Powder Gangers (NCRCF / Primm) --")
    n = boost_faction_lists(builder, esm,
        ["PowderGanger", "VarPowderGanger", "GoodspringsPowder", "NCRCFPowder"],
        count_add=2, faction_name="Powder Gangers")
    print("  Boosted " + str(n) + " lists (+2 per entry)")

    # Save
    builder.save(str(FNV_DATA / "WorldAtmosphere.esp"))
    import os
    print("\nSaved WorldAtmosphere.esp (" + str(os.path.getsize(str(FNV_DATA / "WorldAtmosphere.esp"))) + " bytes)")


if __name__ == "__main__":
    main()
