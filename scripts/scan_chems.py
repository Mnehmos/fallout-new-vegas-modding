"""Scan all chems, stimpaks, food, drink with full effect details."""
import sys, struct
from pathlib import Path
sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")
from core.binary_parser import PluginFile

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")
esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))

# Build MGEF lookup
mgef_names = {}
for r in esm.get_records("MGEF"):
    srs = r.parse_subrecords()
    eid = ""
    for sr in srs:
        if sr.type == "EDID":
            eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
    mgef_names[r.id] = eid

targets = ["Stimpak", "Psycho", "Buffout", "Jet", "Turbo", "MedX", "Med-X",
           "Steady", "Slasher", "Rebound", "Cateye", "Hydra", "RadAway",
           "RadX", "Antivenom", "Fixer", "Whiskey", "Beer", "Vodka", "Wine",
           "Scotch", "Moonshine", "Rum", "Dixon", "SuperStimpak", "DoctorBag",
           "NukaCola", "Sunset", "PurifiedWater", "DirtyWater", "Absinthe",
           "Atomic", "Battle", "Party", "Weapon"]

categories = {
    "HEALING": ["Stimpak", "SuperStimpak", "DoctorBag", "Hydra", "Antivenom"],
    "CHEMS": ["Psycho", "Buffout", "Jet", "Turbo", "MedX", "Med-X", "Steady",
              "Slasher", "Rebound", "Cateye", "Fixer", "Dixon", "Weapon", "Battle", "Party"],
    "RADIATION": ["RadAway", "RadX"],
    "ALCOHOL": ["Whiskey", "Beer", "Vodka", "Wine", "Scotch", "Moonshine", "Rum", "Absinthe",
                "Atomic", "Jake"],
    "DRINKS": ["NukaCola", "Sunset", "PurifiedWater", "DirtyWater"],
}

all_items = {}
for r in esm.get_records("ALCH"):
    srs = r.parse_subrecords()
    eid = name = ""
    effects = []
    value = 0
    for sr in srs:
        if sr.type == "EDID":
            eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if sr.type == "FULL":
            name = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if sr.type == "DATA" and len(sr.data) >= 4:
            value = struct.unpack("<i", sr.data[0:4])[0]
        if sr.type == "EFID" and len(sr.data) == 4:
            effects.append({"mgef": struct.unpack("<I", sr.data)[0]})
        if sr.type == "EFIT" and len(sr.data) >= 12 and effects:
            mag = struct.unpack("<I", sr.data[0:4])[0]
            area = struct.unpack("<I", sr.data[4:8])[0]
            dur = struct.unpack("<I", sr.data[8:12])[0]
            effects[-1].update({"mag": mag, "area": area, "dur": dur})

    if not name:
        continue
    if not any(kw.lower() in name.lower() or kw.lower() in eid.lower() for kw in targets):
        continue

    # Determine category
    cat = "OTHER"
    for c, kws in categories.items():
        if any(kw.lower() in eid.lower() or kw.lower() in name.lower() for kw in kws):
            cat = c
            break

    if cat not in all_items:
        all_items[cat] = []

    eff_strs = []
    for e in effects:
        mgef_name = mgef_names.get(e["mgef"], hex(e["mgef"]))
        mag = e.get("mag", 0)
        dur = e.get("dur", 0)
        eff_strs.append(mgef_name + " " + str(mag) + ("/" + str(dur) + "s" if dur else ""))

    all_items[cat].append((name, eid, hex(r.id), value, eff_strs))

for cat in ["HEALING", "CHEMS", "RADIATION", "ALCOHOL", "DRINKS", "OTHER"]:
    if cat not in all_items:
        continue
    print("\n=== " + cat + " ===")
    for name, eid, fid, value, effs in sorted(all_items[cat], key=lambda x: x[0]):
        print(fid.ljust(12) + name.ljust(28) + str(value).rjust(5) + " caps")
        for e in effs:
            print("             " + e)
