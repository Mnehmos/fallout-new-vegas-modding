"""
World & Atmosphere Overhaul — 4 mods in 1 ESP

1. Night Terrors: Apex predators spawn 3x more at night (Deathclaws, Cazadors, Nightstalkers)
2. Caravan Routes: More merchant/trader groups on roads
3. Faction War Zones: NCR/Legion/Fiend patrols boosted in contested territory
4. Mojave Alive: General civilian/prospector/traveler density increase
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")


def boost_lvl_list(builder, esm, edid, count_mult=2, add_calc_each=True):
    """Find a leveled list by EditorID and boost its counts."""
    for r in esm.get_records(r.type if hasattr(r, 'type') else 'LVLC'):
        pass  # need different approach


def find_and_boost(esm, builder, record_type, edid_contains, count_add=1, force_calc_each=True):
    """Find all leveled lists matching a keyword and boost them."""
    boosted = 0
    for r in esm.get_records(record_type):
        srs = r.parse_subrecords()
        eid = ''
        for sr in srs:
            if sr.type == 'EDID':
                eid = sr.data.rstrip(b'\x00').decode()

        if not any(kw.lower() in eid.lower() for kw in edid_contains):
            continue

        entry_count = sum(1 for sr in srs if sr.type == 'LVLO')
        if entry_count == 0:
            continue

        rec = RecordBuilder(record_type, r.id)
        for sr in srs:
            if sr.type == 'LVLF' and force_calc_each:
                old = sr.data[0]
                rec.add(SR.from_bytes('LVLF', struct.pack('<B', old | 0x03)))
            elif sr.type == 'LVLO' and len(sr.data) >= 10:
                level = struct.unpack('<h', sr.data[:2])[0]
                unused1 = struct.unpack('<H', sr.data[2:4])[0]
                fid = struct.unpack('<I', sr.data[4:8])[0]
                count = struct.unpack('<h', sr.data[8:10])[0]
                unused2 = struct.unpack('<H', sr.data[10:12])[0] if len(sr.data) >= 12 else 0
                new_count = count + count_add
                rec.add_bytes('LVLO', struct.pack('<hHIhH', level, unused1, fid, new_count, unused2))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_raw_record(record_type, rec.build())
        boosted += 1
    return boosted


def main():
    print("=== World & Atmosphere Overhaul ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))

    builder = ESPBuilder(author="Mnehmos", description="World & Atmosphere - Night Terrors, Patrols, Faction Wars")
    builder.add_master("FalloutNV.esm")

    # ══════════════════════════════════════════
    # 1. NIGHT TERRORS — Apex predator boost
    # ══════════════════════════════════════════
    print("-- Night Terrors --")

    # Deathclaws: +2 per spawn
    n = find_and_boost(esm, builder, 'LVLC',
        ['Deathclaw', 'DeathClaw'], count_add=2)
    print("  Deathclaw lists boosted: " + str(n))

    # Cazadors: +2 per spawn
    n = find_and_boost(esm, builder, 'LVLC',
        ['Cazador'], count_add=2)
    print("  Cazador lists boosted: " + str(n))

    # Nightstalkers: +2 per spawn
    n = find_and_boost(esm, builder, 'LVLC',
        ['NightStalker'], count_add=2)
    print("  Nightstalker lists boosted: " + str(n))

    # Super Mutants: +1 per spawn
    n = find_and_boost(esm, builder, 'LVLC',
        ['SuperMutant', 'Nightkin'], count_add=1)
    print("  Super Mutant lists boosted: " + str(n))

    # ══════════════════════════════════════════
    # 2. CARAVAN ROUTES — More traders & guards
    # ══════════════════════════════════════════
    print("\n-- Caravan Routes --")

    # Boost merchant/caravan NPC encounter lists
    n = find_and_boost(esm, builder, 'LVLN',
        ['Merchant', 'Caravan', 'Trader', 'Prospector'], count_add=1)
    print("  Merchant/Caravan LVLN boosted: " + str(n))

    # Also boost the creature-level lists that include caravans
    n = find_and_boost(esm, builder, 'LVLC',
        ['Caravan'], count_add=1)
    print("  Caravan LVLC boosted: " + str(n))

    # ══════════════════════════════════════════
    # 3. FACTION WAR ZONES — More patrols
    # ══════════════════════════════════════════
    print("\n-- Faction War Zones --")

    # NCR patrols: +1
    n = find_and_boost(esm, builder, 'LVLN',
        ['NCR', 'Trooper', 'Ranger'], count_add=1)
    print("  NCR patrol LVLN boosted: " + str(n))

    # Legion: +1
    n = find_and_boost(esm, builder, 'LVLN',
        ['Legion', 'Legionary', 'Decanus', 'Vexillarius'], count_add=1)
    print("  Legion LVLN boosted: " + str(n))

    # Fiends: +1
    n = find_and_boost(esm, builder, 'LVLN',
        ['Fiend'], count_add=1)
    print("  Fiend LVLN boosted: " + str(n))

    # Powder Gangers: +1
    n = find_and_boost(esm, builder, 'LVLN',
        ['PowderGanger', 'Raider'], count_add=1)
    print("  Raider/Powder Ganger LVLN boosted: " + str(n))

    # Brotherhood: +1
    n = find_and_boost(esm, builder, 'LVLN',
        ['Brotherhood'], count_add=1)
    print("  Brotherhood LVLN boosted: " + str(n))

    # Great Khans: +1
    n = find_and_boost(esm, builder, 'LVLN',
        ['GreatKhan', 'Khan'], count_add=1)
    print("  Great Khan LVLN boosted: " + str(n))

    # ══════════════════════════════════════════
    # 4. MOJAVE ALIVE — General encounter density
    # ══════════════════════════════════════════
    print("\n-- Mojave Alive --")

    # Wasteland encounter master lists
    n = find_and_boost(esm, builder, 'LVLC',
        ['EncWasteland'], count_add=1)
    print("  Wasteland encounter LVLC boosted: " + str(n))

    # Civilian/prospector groups
    n = find_and_boost(esm, builder, 'LVLN',
        ['Civilian', 'Prospector', 'Traveler', 'Gambler'], count_add=1)
    print("  Civilian LVLN boosted: " + str(n))

    # Robot patrols
    n = find_and_boost(esm, builder, 'LVLC',
        ['Robot', 'Securitron'], count_add=1)
    print("  Robot LVLC boosted: " + str(n))

    # ══════════════════════════════════════════
    # SAVE
    # ══════════════════════════════════════════
    outpath = FNV_DATA / "WorldAtmosphere.esp"
    builder.save(str(outpath))

    import os
    sz = os.path.getsize(str(outpath))
    print("\nSaved: " + str(outpath) + " (" + str(sz) + " bytes)")


if __name__ == "__main__":
    main()
