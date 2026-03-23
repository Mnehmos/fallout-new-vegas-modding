"""
Gunslinger Path — 8 New Pistol Perks via Binary Writer

Bypasses xEdit's wbStructSK sort-key lock on Entry Point fields.
Clones Gunslinger's raw subrecords, patches Entry Point ID + EPFD value,
writes new PERK records directly into PerkOverhaul.esp.
"""

import sys
import struct
from pathlib import Path

# Add MCP core to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "fnvedit-mcp" / "src"))
sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# ── Gunslinger template bytes ──
# Index 6: DATA (effect-level) = 08 03 03
#   byte 0 = Entry Point ID (08 = VATS accuracy)
#   byte 1 = Function (03 = Add Range To Value)
#   byte 2 = Tab Count (03 = has conditions)
#
# Index 8: CTDA = func 108 == 4.0 (pistol animation type)
# Index 10: EPFD = 0000a03f = 1.25 float

PERKS = [
    {
        "edid": "MnQuickDraw",
        "name": "Quick Draw (Gunslinger)",
        "desc": "Lightning reflexes let you draw and holster pistols 50% faster.",
        "level": 4,
        "entry_point": 38,  # Equip Speed
        "epfd": 1.50,
    },
    {
        "edid": "MnPointBlank",
        "name": "Point Blank",
        "desc": "Up close and personal. Pistols deal 15% more damage.",
        "level": 6,
        "entry_point": 0,  # Calculate Weapon Damage
        "epfd": 1.15,
    },
    {
        "edid": "MnFanTheHammer",
        "name": "Fan the Hammer",
        "desc": "Work the action like a pro. Pistol fire rate increased by 20%.",
        "level": 8,
        "entry_point": 43,  # Attack Speed
        "epfd": 1.20,
    },
    {
        "edid": "MnHipShooter",
        "name": "Hip Shooter",
        "desc": "Steady hands, tight groups. Pistol spread reduced by 25% from the hip.",
        "level": 10,
        "entry_point": 34,  # Gun Spread
        "epfd": 0.75,
    },
    {
        "edid": "MnDeadEye",
        "name": "Dead Eye",
        "desc": "Every shot finds the weak point. Pistol critical damage increased by 50%.",
        "level": 12,
        "entry_point": 2,  # Calc My Crit Damage
        "epfd": 1.50,
    },
    {
        "edid": "MnSnapShot",
        "name": "Snap Shot",
        "desc": "Instinctive targeting. Pistols cost 15% less AP in V.A.T.S.",
        "level": 14,
        "entry_point": 40,  # Action Point Cost
        "epfd": 0.85,
    },
    {
        "edid": "MnHairTrigger",
        "name": "Hair Trigger",
        "desc": "Muscle memory takes over. Pistol reload speed increased by 35%.",
        "level": 16,
        "entry_point": 37,  # Reload Speed
        "epfd": 1.35,
    },
    {
        "edid": "MnDuelist",
        "name": "Duelist",
        "desc": "One weapon. One hand. Total mastery. Pistol damage increased by 25%.",
        "level": 18,
        "entry_point": 0,  # Calculate Weapon Damage
        "epfd": 1.25,
    },
]


def load_gunslinger_template():
    """Load Gunslinger perk and return its raw subrecords."""
    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    for r in esm.get_records("PERK"):
        srs = r.parse_subrecords()
        for sr in srs:
            if sr.type == "EDID" and sr.data.rstrip(b"\x00").decode() == "Gunslinger":
                return srs
    raise RuntimeError("Gunslinger perk not found in FalloutNV.esm")


def build_perk(builder: ESPBuilder, template_srs, perk_def: dict) -> int:
    """Build a new PERK record by cloning Gunslinger's subrecords with patches."""
    fid = builder.allocate_form_id()
    rec = RecordBuilder("PERK", fid)

    for sr in template_srs:
        if sr.type == "EDID":
            # Replace editor ID
            rec.add_string("EDID", perk_def["edid"])

        elif sr.type == "FULL":
            # Replace display name
            rec.add_string("FULL", perk_def["name"])

        elif sr.type == "DESC":
            # Replace description
            rec.add_string("DESC", perk_def["desc"])

        elif sr.type == "DATA" and len(sr.data) == 5:
            # Perk-level DATA: trait(1) + minLevel(1) + numRanks(1) + playable(1) + hidden(1)
            new_data = struct.pack("<5B", 0, perk_def["level"], 1, 1, 0)
            rec.add_bytes("DATA", new_data)

        elif sr.type == "DATA" and len(sr.data) == 3:
            # Effect-level DATA: EntryPoint(1) + Function(1) + TabCount(1)
            # Patch Entry Point ID, keep Function=3 and TabCount=3
            new_data = struct.pack("<3B", perk_def["entry_point"], 3, 3)
            rec.add_bytes("DATA", new_data)

        elif sr.type == "EPFD":
            # Replace effect float value
            rec.add_float("EPFD", perk_def["epfd"])

        else:
            # Copy all other subrecords verbatim (ICON, PRKE, PRKC, CTDA, EPFT, PRKF)
            rec.add(SR.from_bytes(sr.type, sr.data))

    builder.add_record("PERK", rec)
    return fid


def main():
    print("=== Gunslinger Path Perk Generator ===\n")

    # Load template
    print("Loading Gunslinger template from FalloutNV.esm...")
    template = load_gunslinger_template()
    print(f"  Template: {len(template)} subrecords\n")

    # Load or create PerkOverhaul.esp
    esp_path = FNV_DATA / "PerkOverhaul.esp"
    if esp_path.exists():
        print(f"Loading existing {esp_path.name}...")
        builder = ESPBuilder.load_existing(str(esp_path))
        print(f"  Loaded ({esp_path.stat().st_size} bytes)\n")
    else:
        print(f"Creating new {esp_path.name}...")
        builder = ESPBuilder(
            author="MnemoScript",
            description="Perk Overhaul — new playstyle perks"
        )
        builder.add_master("FalloutNV.esm")
        print("  Created with FalloutNV.esm master\n")

    # Build each perk
    print("Creating 8 Gunslinger Path perks:\n")
    for perk_def in PERKS:
        fid = build_perk(builder, template, perk_def)
        ep = perk_def["entry_point"]
        val = perk_def["epfd"]
        print(f"  + {perk_def['name']:30s} Lv{perk_def['level']:2d}  EP={ep:2d}  x{val:.2f}  -> {fid:#010x}")

    # Save — try primary location, fall back to temp if locked by xEdit
    try:
        builder.save(str(esp_path))
        size = esp_path.stat().st_size
    except PermissionError:
        import shutil
        temp_path = Path("f:/tmp/PerkOverhaul.esp")
        builder.save(str(temp_path))
        size = temp_path.stat().st_size
        print(f"\n  NOTE: {esp_path.name} locked (xEdit open?)")
        print(f"  Saved to: {temp_path}")
        print(f"  Close xEdit, then copy to: {esp_path}")
        esp_path = temp_path
    print(f"\nSaved: {esp_path} ({size} bytes)")
    print(f"Perks: {len(PERKS)} created")

    # Verify with our parser
    print("\n=== Verification ===")
    esp = PluginFile(str(esp_path))
    perk_count = 0
    for r in esp.get_records("PERK"):
        srs = r.parse_subrecords()
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode()
                if eid.startswith("Mn"):
                    perk_count += 1
                    # Find EP and EPFD
                    ep_id = None
                    epfd_val = None
                    for sr2 in srs:
                        if sr2.type == "DATA" and len(sr2.data) == 3:
                            ep_id = sr2.data[0]
                        if sr2.type == "EPFD" and len(sr2.data) == 4:
                            epfd_val = struct.unpack("<f", sr2.data)[0]
                    print(f"  {eid:30s} EP={ep_id}  EPFD={epfd_val:.4f}")
                break
    print(f"\nVerified: {perk_count} Mn* perks in ESP")


if __name__ == "__main__":
    main()
