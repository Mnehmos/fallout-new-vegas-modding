"""
Add Mnehmos items to DLC vendor lists.

GRA vendor lists feed into every major vendor in the game.
We override GRA LVLI records to include our weapons.
Requires GunRunnersArsenal.esm as master.
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")


def collect_mnehmos_weapons(esp):
    """Collect all Mnehmos weapon FormIDs grouped by type."""
    weapons = {"all": [], "energy": [], "melee": [], "explosive": []}
    seen = set()

    for r in esp.get_records("WEAP"):
        srs = r.parse_subrecords()
        eid = name = ""
        animtype = 0
        for sr in srs:
            if sr.type == "EDID": eid = sr.data.rstrip(b"\x00").decode()
            if sr.type == "FULL": name = sr.data.rstrip(b"\x00").decode()
            if sr.type == "DNAM" and len(sr.data) >= 4:
                animtype = struct.unpack("<I", sr.data[0:4])[0]
        if not name or eid.startswith("NVDLC") or name in seen:
            continue
        seen.add(name)

        weapons["all"].append(r.id)

        is_energy = any(kw in eid for kw in [
            "Laser", "Plasma", "Tesla", "Gauss", "Recharger",
            "Epilogue", "Postscript", "Amendment", "Afterglow", "BrightIdea",
            "Eureka", "TotalRecall", "Bibliography", "Dissertation", "Axiom",
            "Abstract", "BigMT", "Mobius", "Sprtel", "Overexposure", "DejaVu",
            "Catharsis", "Anamnesis", "Stream", "ChristinesSilence", "ElijahsLegacy",
        ])
        is_explosive = any(kw in eid for kw in [
            "Grenade", "Categorical", "Parenthetical", "Missile", "Addendum", "RedGlare",
        ])

        if is_energy:
            weapons["energy"].append(r.id)
        elif is_explosive:
            weapons["explosive"].append(r.id)

    return weapons


def override_lvli(builder, source_esm, list_formid, new_items, level=1, count=1):
    """Override a DLC LVLI and append items."""
    for r in source_esm.get_records("LVLI"):
        if r.id == list_formid:
            srs = r.parse_subrecords()
            rec = RecordBuilder("LVLI", list_formid)
            old_count = 0

            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    new_total = min(old_count + len(new_items), 255)
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", new_total)))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))

            for fid in new_items:
                lvlo = struct.pack("<hHIhH", level, 0, fid, count, 0)
                rec.add_bytes("LVLO", lvlo)

            builder.add_raw_record("LVLI", rec.build())
            return True
    return False


def main():
    print("=== Adding Mnehmos Items to DLC Vendors ===\n")

    esp = PluginFile(str(FNV_DATA / "MnehmosMojave.esp"))
    gra = PluginFile(str(FNV_DATA / "GunRunnersArsenal.esm"))

    # Check if MnehmosMojave already has GRA as master
    with open(str(FNV_DATA / "MnehmosMojave.esp"), "rb") as f:
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

    print("Current masters: " + str(masters))

    if "GunRunnersArsenal.esm" not in masters:
        print("WARNING: GRA not a master of MnehmosMojave.esp")
        print("Adding GRA master requires rebuilding TES4 header.")
        print("Skipping DLC vendor injection for now.")
        print("")
        print("Alternative: Creating a separate bridge ESP...")

        # Create a bridge ESP that has both GRA and our ESP as context
        bridge = ESPBuilder(author="Mnehmos", description="DLC Vendor Bridge - Mnehmos items in DLC shops")
        bridge.add_master("FalloutNV.esm")
        bridge.add_master("GunRunnersArsenal.esm")
        bridge.add_master("MnehmosMojave.esp")

        weapons = collect_mnehmos_weapons(esp)
        print("Collected: " + str(len(weapons["all"])) + " weapons")
        print("  Energy: " + str(len(weapons["energy"])))
        print("  Explosive: " + str(len(weapons["explosive"])))

        # Pick a subset for each GRA vendor list (max 10 per list to not overwhelm)
        all_weap = weapons["all"][:20]  # Top 20
        energy = weapons["energy"][:10]

        # GRA Gun Runners weapon list (feeds into Gun Runners vendor)
        # FormID 0x1000A04 = NVDLC05VendorWeapListGunRunners (11 entries)
        # But this FormID has master index 01 in GRA, which maps to index 1 in our bridge
        # GRA is master index 1 in our bridge, so FormID high byte = 01
        gra_master_idx = 1  # GRA is second master (index 1) in bridge ESP

        # Remap GRA FormIDs: in GRA file they start with 0x01, in our bridge GRA is master 1
        # So 0x01000A04 in GRA -> 0x01000A04 in our bridge (same index, convenient)

        gra_gun_runners = (gra_master_idx << 24) | 0x000A04  # NVDLC05VendorWeapListGunRunners
        gra_van_graffs = (gra_master_idx << 24) | 0x000A01   # NVDLC05VendorWeapListVanGraffs
        gra_188_gr = (gra_master_idx << 24) | 0x000AAA       # NVDLC05VendorWeapList188GR
        gra_188_ncr = (gra_master_idx << 24) | 0x0009FC      # NVDLC05VendorWeapList188NCR
        gra_chet = (gra_master_idx << 24) | 0x0009FE         # NVDLC05VendorWeapListChet
        gra_lacey = (gra_master_idx << 24) | 0x0009FD        # NVDLC05VendorWeapListLacey
        gra_dale = (gra_master_idx << 24) | 0x000A00         # NVDLC05VendorWeapListDaleBarton75
        gra_cliff = (gra_master_idx << 24) | 0x000A02        # NVDLC05VendorWeapListCliffBriscoe
        gra_boomers = (gra_master_idx << 24) | 0x0009FF      # NVDLC05VendorWeapListBoomers
        gra_mick = (gra_master_idx << 24) | 0x000A03         # NVDLC05VendorWeapListMickAndRalph

        # Our weapons have master index 2 (MnehmosMojave.esp is third master)
        mn_idx = 2

        # Remap our weapon FormIDs to use master index 2
        def remap(fid):
            return (mn_idx << 24) | (fid & 0x00FFFFFF)

        remapped_all = [remap(f) for f in all_weap]
        remapped_energy = [remap(f) for f in energy]

        # Override each GRA vendor list
        results = []

        for list_fid, list_name, items in [
            (gra_gun_runners, "Gun Runners", remapped_all),
            (gra_van_graffs, "Van Graffs", remapped_energy),
            (gra_188_gr, "188 GR", remapped_all[:10]),
            (gra_188_ncr, "188 NCR", remapped_all[:8]),
            (gra_chet, "Chet", remapped_all[:6]),
            (gra_lacey, "Lacey", remapped_all[:6]),
            (gra_dale, "Dale Barton", remapped_all[:8]),
            (gra_cliff, "Cliff Briscoe", remapped_all[:6]),
            (gra_boomers, "Boomers", remapped_all[:5]),
            (gra_mick, "Mick & Ralph", remapped_all[:8]),
        ]:
            if override_lvli(bridge, gra, list_fid, items):
                results.append((list_name, len(items)))
                print("  " + list_name + ": +" + str(len(items)) + " items")
            else:
                print("  " + list_name + ": FAILED (FormID " + hex(list_fid) + " not found)")

        # Save bridge ESP
        outpath = FNV_DATA / "MnehmosDLCVendors.esp"
        bridge.save(str(outpath))

        import os
        print("\nSaved: " + str(outpath) + " (" + str(os.path.getsize(str(outpath))) + " bytes)")
        print("Add to plugins.txt: MnehmosDLCVendors.esp (after MnehmosMojave.esp)")
        return

    # If GRA is already a master, inject directly (won't reach here currently)
    print("GRA is a master - injecting directly")


if __name__ == "__main__":
    main()
