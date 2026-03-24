"""Print full equipment catalog with console IDs."""
import sys, struct
from pathlib import Path
sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")
from core.binary_parser import PluginFile

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")
esp = PluginFile(str(FNV_DATA / "MnehmosMojave.esp"))
LO = "10"

print("=" * 64)
print("  MNEHMOS MOJAVE - COMPLETE CATALOG  (player.additem <ID> 1)")
print("=" * 64)

# WEAPONS
weapons = []
for r in esp.get_records("WEAP"):
    srs = r.parse_subrecords()
    eid = name = ""
    dmg = clip = 0
    for sr in srs:
        if sr.type == "EDID": eid = sr.data.rstrip(b"\x00").decode()
        if sr.type == "FULL": name = sr.data.rstrip(b"\x00").decode()
        if sr.type == "DATA" and len(sr.data) == 15:
            dmg = struct.unpack("<h", sr.data[12:14])[0]
            clip = sr.data[14]
    if name and not eid.startswith("NVDLC"):
        low = r.id & 0x00FFFFFF
        fid = LO + format(low, "06X")
        weapons.append((name, dmg, clip, fid))

weapons.sort(key=lambda x: x[1])
print("\n--- WEAPONS (" + str(len(weapons)) + " total) ---")
print("Name".ljust(36) + "Dmg".rjust(5) + " Clip".rjust(5) + "  Console ID")
print("-" * 64)
for name, dmg, clip, fid in weapons:
    c = str(clip) if clip > 0 else "-"
    print(name.ljust(36) + str(dmg).rjust(5) + c.rjust(5) + "  " + fid)

# ARMOR
armor_items = []
for r in esp.get_records("ARMO"):
    srs = r.parse_subrecords()
    eid = name = ""
    dt = 0
    for sr in srs:
        if sr.type == "EDID": eid = sr.data.rstrip(b"\x00").decode()
        if sr.type == "FULL": name = sr.data.rstrip(b"\x00").decode()
        if sr.type == "DNAM" and len(sr.data) >= 8:
            dt = struct.unpack("<f", sr.data[4:8])[0]
    if name:
        low = r.id & 0x00FFFFFF
        fid = LO + format(low, "06X")
        armor_items.append((name, int(dt), fid))

armor_items.sort(key=lambda x: x[1], reverse=True)
print("\n--- ARMOR (" + str(len(armor_items)) + " total) ---")
print("Name".ljust(36) + " DT".rjust(4) + "  Console ID")
print("-" * 56)
for name, dt, fid in armor_items:
    print(name.ljust(36) + str(dt).rjust(4) + "  " + fid)

# AMMO
print("\n--- AMMO ---")
try:
    for r in esp.get_records("AMMO"):
        srs = r.parse_subrecords()
        eid = name = ""
        for sr in srs:
            if sr.type == "EDID": eid = sr.data.rstrip(b"\x00").decode()
            if sr.type == "FULL": name = sr.data.rstrip(b"\x00").decode()
        if name:
            low = r.id & 0x00FFFFFF
            print(name.ljust(36) + LO + format(low, "06X"))
except:
    print("(none)")

print("\n" + "=" * 64)
print("Weapons: " + str(len(weapons)) + "  Armor: " + str(len(armor_items)))
print("=" * 64)
