"""Scan all food/drink items across base game + all DLCs."""
import sys, struct
from pathlib import Path
sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")
from core.binary_parser import PluginFile

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

mgef_names = {}
esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
for r in esm.get_records("MGEF"):
    srs = r.parse_subrecords()
    for sr in srs:
        if sr.type == "EDID":
            mgef_names[r.id] = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

food_keywords = ["food", "meat", "steak", "stew", "soup", "gecko", "brahmin", "bighorn",
    "mole", "deathclaw", "bloat", "grilled", "squirrel", "coyote", "lakelurk",
    "cazador", "ant", "mantis", "nightstalker", "dog", "iguana", "pork", "mac",
    "salisbury", "fancy", "instamash", "sugar", "cram", "dandy", "bubblegum",
    "cake", "pie", "crispy", "biscuit", "yao", "banana", "caravan", "lunch",
    "mutfruit", "barrel", "cactus", "maize", "xander", "agave", "prickly",
    "nevada", "datura", "broc", "potato", "flour", "jalapeno", "bean",
    "nuka", "sunset", "purified", "dirty", "water", "sarsaparilla", "atomic",
    "ruby", "wasteland", "omelet", "jerky", "thin", "cloud", "sierra",
    "spore", "salient", "blood", "mushroom", "cave", "fungus"]

plugins = [
    ("FalloutNV.esm", "BASE"),
    ("DeadMoney.esm", "DM"),
    ("HonestHearts.esm", "HH"),
    ("OldWorldBlues.esm", "OWB"),
    ("LonesomeRoad.esm", "LR"),
    ("GunRunnersArsenal.esm", "GRA"),
]

all_food = []
for plugin_file, tag in plugins:
    try:
        p = PluginFile(str(FNV_DATA / plugin_file))
        for r in p.get_records("ALCH"):
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
                    effects[-1].update({
                        "mag": struct.unpack("<I", sr.data[0:4])[0],
                        "dur": struct.unpack("<I", sr.data[8:12])[0],
                    })

            if not name:
                continue
            if not any(kw in eid.lower() or kw in name.lower() for kw in food_keywords):
                continue

            # Check if it has RestoreHealth or food-like effects
            has_heal = False
            heal_total = 0
            for e in effects:
                mname = mgef_names.get(e["mgef"], "")
                if "restore" in mname.lower() or "heal" in mname.lower() or "food" in mname.lower():
                    has_heal = True
                    mag = e.get("mag", 0)
                    dur = e.get("dur", 0)
                    if dur > 0:
                        heal_total += mag * dur
                    else:
                        heal_total += mag

            eff_strs = []
            for e in effects:
                mname = mgef_names.get(e["mgef"], hex(e["mgef"]))
                mag = e.get("mag", 0)
                dur = e.get("dur", 0)
                if dur:
                    eff_strs.append(mname + " " + str(mag) + "/" + str(dur) + "s")
                else:
                    eff_strs.append(mname + " " + str(mag))

            all_food.append((tag, name, eid, hex(r.id), heal_total, eff_strs))
    except Exception as e:
        print("Error " + plugin_file + ": " + str(e))

# Sort by source then heal total
all_food.sort(key=lambda x: (x[0], -x[4]))

current_tag = ""
for tag, name, eid, fid, heal, effs in all_food:
    if tag != current_tag:
        print("\n=== " + tag + " ===")
        current_tag = tag
    try:
        print(fid.ljust(12) + name.ljust(30) + "HP~" + str(heal).rjust(5) + "  " + eid)
        for e in effs:
            print("             " + e)
    except:
        pass
