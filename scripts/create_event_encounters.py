"""
Event Encounters — Three-way clashes, tiered escalation, caravan events.

Three-way fights work because NPCs have faction affiliations.
Put NCR + Legion in the same LVLN → they spawn, see each other, fight.
Player walks into an ongoing battle.

Tiered escalation uses level-gated entries in CalcAll lists.
Low-level entries spawn always (bait), high-level entries only appear
when the player is strong enough (reinforcements/elites).
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# Building blocks (existing Enc* LVLN FormIDs)
FIEND_GUN = 0x0F1C83
FIEND_MELEE = 0x0F1C85
FIEND_RIFLE = 0x0F1C89
FIEND_SPECIAL = 0x0F1C8A
NCR_TROOPER = 0x0A46F8
NCR_TROOPER_GUN = 0x0A46F6
NCR_TROOPER_GUN1 = 0x0A46F7
NCR_TROOPER_GUN2 = 0x0A46F9
RAIDER_GUN = 0x029627
RAIDER_MELEE = 0x02F6E8
RAIDER_RIFLE = 0x07F4E1
BOS_GUN = 0x000A87
BOS_MELEE = 0x000A88
BOS_SPECIAL = 0x000A89
SMUTANT_MELEE = 0x03A14A
SMUTANT_GUN = 0x02359F
SMUTANT_MINIGUN = 0x092C53
SMUTANT_NIGHTKIN_MELEE = 0x07EA2F
GHOUL = 0x0235A7
GECKO = 0x0E5867
RADSCORPION = 0x02359D
DEATHCLAW_SMALL = 0x15679E
DEATHCLAW_MED = 0x1567AB
LEGION_ENC = 0x130C10       # EncVHDCLLegionary


def create_comp(builder, edid, entries):
    fid = builder.allocate_form_id()
    rec = RecordBuilder("LVLN", fid)
    rec.add_string("EDID", edid)
    rec.add(SR.from_bytes("OBND", b"\x00" * 12))
    rec.add(SR.from_bytes("LVLD", struct.pack("<B", 0)))
    rec.add(SR.from_bytes("LVLF", struct.pack("<B", 0x01)))
    rec.add(SR.from_bytes("LLCT", struct.pack("<B", len(entries))))
    for item_fid, count, level in entries:
        rec.add_bytes("LVLO", struct.pack("<hHIhH", level, 0, item_fid, count, 0))
    builder.add_record("LVLN", rec)
    return fid


def main():
    print("=== Event Encounters ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "WorldAtmosphere.esp"))

    events = {}

    # ── THREE-WAY CLASHES ──
    print("-- Three-Way Clashes --")

    events["NCRvsLegion"] = create_comp(builder, "MnEventNCRvsLegion", [
        (NCR_TROOPER_GUN, 2, 1),
        (NCR_TROOPER, 1, 1),
        (LEGION_ENC, 2, 1),
        (LEGION_ENC, 1, 8),
    ])
    print("  NCRvsLegion: 3 NCR vs 3 Legion")

    events["NCRvsLegionBattle"] = create_comp(builder, "MnEventNCRvsLegionBattle", [
        (NCR_TROOPER_GUN1, 3, 1),
        (NCR_TROOPER_GUN2, 1, 10),
        (NCR_TROOPER, 1, 1),
        (LEGION_ENC, 3, 1),
        (LEGION_ENC, 2, 10),
    ])
    print("  NCRvsLegionBattle: 5 NCR vs 5 Legion")

    events["FiendsvsNCR"] = create_comp(builder, "MnEventFiendsvsNCR", [
        (FIEND_MELEE, 2, 1),
        (FIEND_GUN, 2, 1),
        (NCR_TROOPER_GUN, 2, 1),
        (NCR_TROOPER, 1, 1),
    ])
    print("  FiendsvsNCR: 4 Fiends vs 3 NCR")

    events["RaidersvsWild"] = create_comp(builder, "MnEventRaidersvsWild", [
        (RAIDER_GUN, 2, 1),
        (RAIDER_MELEE, 1, 1),
        (GECKO, 3, 1),
    ])
    print("  RaidersvsWild: 3 raiders vs 3 geckos")

    events["BOSvsMutants"] = create_comp(builder, "MnEventBOSvsMutants", [
        (BOS_GUN, 2, 1),
        (BOS_MELEE, 1, 1),
        (SMUTANT_MELEE, 2, 1),
        (SMUTANT_GUN, 1, 1),
        (SMUTANT_MINIGUN, 1, 15),
    ])
    print("  BOSvsMutants: 3 BoS vs 4 super mutants")

    events["LegionvsFiends"] = create_comp(builder, "MnEventLegionvsFiends", [
        (LEGION_ENC, 3, 1),
        (LEGION_ENC, 1, 12),
        (FIEND_GUN, 2, 1),
        (FIEND_MELEE, 2, 1),
        (FIEND_SPECIAL, 1, 10),
    ])
    print("  LegionvsFiends: 4 Legion vs 5 Fiends")

    events["NCRvsBOS"] = create_comp(builder, "MnEventNCRvsBOS", [
        (NCR_TROOPER_GUN1, 3, 1),
        (NCR_TROOPER, 1, 1),
        (BOS_GUN, 2, 1),
        (BOS_SPECIAL, 1, 12),
    ])
    print("  NCRvsBOS: 4 NCR vs 3 BoS")

    # ── TIERED ESCALATION ──
    print("\n-- Tiered Escalation --")

    events["FiendEscalation"] = create_comp(builder, "MnEventFiendEscalation", [
        (FIEND_MELEE, 2, 1),
        (FIEND_GUN, 1, 1),
        (FIEND_RIFLE, 2, 8),
        (FIEND_SPECIAL, 1, 14),
    ])
    print("  FiendEscalation: bait(3) -> rifles(2) -> heavy(1)")

    events["GhoulHorror"] = create_comp(builder, "MnEventGhoulHorror", [
        (GHOUL, 4, 1),
        (GHOUL, 2, 8),
        (GHOUL, 1, 16),
    ])
    print("  GhoulHorror: 4 ferals -> 2 tough -> 1 reaver")

    events["DeathclawTerritory"] = create_comp(builder, "MnEventDeathclawTerritory", [
        (DEATHCLAW_SMALL, 2, 1),
        (DEATHCLAW_MED, 1, 12),
        (DEATHCLAW_MED, 1, 20),
    ])
    print("  DeathclawTerritory: 2 young -> 1 adult -> 1 more adult")

    events["MutantNightkin"] = create_comp(builder, "MnEventMutantNightkin", [
        (SMUTANT_MELEE, 2, 1),
        (SMUTANT_GUN, 1, 1),
        (SMUTANT_NIGHTKIN_MELEE, 2, 12),
    ])
    print("  MutantNightkin: 3 visible + 2 stealthed nightkin")

    events["ScorpionSwarm"] = create_comp(builder, "MnEventScorpionSwarm", [
        (RADSCORPION, 3, 1),
        (RADSCORPION, 2, 10),
        (RADSCORPION, 1, 18),
    ])
    print("  ScorpionSwarm: 3 normal -> 2 big -> 1 giant")

    # ── CARAVAN EVENTS ──
    print("\n-- Caravan Events --")

    events["CaravanAttack"] = create_comp(builder, "MnEventCaravanAttack", [
        (RAIDER_GUN, 3, 1),
        (RAIDER_RIFLE, 1, 5),
        (NCR_TROOPER, 2, 1),
    ])
    print("  CaravanAttack: 4 raiders vs 2 guards")

    events["LegionTradeAmbush"] = create_comp(builder, "MnEventLegionTradeAmbush", [
        (LEGION_ENC, 3, 1),
        (LEGION_ENC, 1, 10),
        (NCR_TROOPER_GUN, 2, 1),
    ])
    print("  LegionTradeAmbush: 4 legion vs 2 NCR escort")

    events["MutantCaravanRaid"] = create_comp(builder, "MnEventMutantCaravanRaid", [
        (SMUTANT_MELEE, 2, 1),
        (SMUTANT_GUN, 1, 1),
        (NCR_TROOPER, 2, 1),
        (RAIDER_GUN, 1, 1),
    ])
    print("  MutantCaravanRaid: 3 mutants vs 2 guards + 1 raider")

    # ── INJECT INTO ENCOUNTER LISTS ──
    print("\n-- Injecting Events --")

    # Main wasteland
    for r in esm.get_records("LVLC"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        if eid == "EncWastelandNV":
            rec = RecordBuilder("LVLC", r.id)
            new_events = [
                (8, events["NCRvsLegion"]),
                (5, events["FiendsvsNCR"]),
                (3, events["RaidersvsWild"]),
                (6, events["FiendEscalation"]),
                (8, events["GhoulHorror"]),
                (3, events["CaravanAttack"]),
                (10, events["LegionTradeAmbush"]),
                (12, events["LegionvsFiends"]),
                (10, events["ScorpionSwarm"]),
                (8, events["MutantCaravanRaid"]),
            ]
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", min(old_count + len(new_events), 255))))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
            for lvl, fid in new_events:
                rec.add_bytes("LVLO", struct.pack("<hHIhH", lvl, 0, fid, 1, 0))
            builder.add_raw_record("LVLC", rec.build())
            print("  EncWastelandNV: +" + str(len(new_events)) + " events")
            break

    # Tough encounters
    for r in esm.get_records("LVLC"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if eid == "EncWastelandNVTough":
            rec = RecordBuilder("LVLC", r.id)
            tough_events = [
                (1, events["NCRvsLegionBattle"]),
                (1, events["BOSvsMutants"]),
                (1, events["DeathclawTerritory"]),
                (1, events["NCRvsBOS"]),
            ]
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", min(old_count + len(tough_events), 255))))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
            for lvl, fid in tough_events:
                rec.add_bytes("LVLO", struct.pack("<hHIhH", lvl, 0, fid, 1, 0))
            builder.add_raw_record("LVLC", rec.build())
            print("  EncWastelandNVTough: +" + str(len(tough_events)) + " heavy events")
            break

    # Valley Road tier 3
    for r in esm.get_records("LVLC"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if eid == "VEncVarTier3ValleyRoad":
            rec = RecordBuilder("LVLC", r.id)
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", min(old_count + 2, 255))))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, events["MutantNightkin"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, events["NCRvsLegion"], 1, 0))
            builder.add_raw_record("LVLC", rec.build())
            print("  VEncVarTier3ValleyRoad: +2 events")
            break

    # Save
    builder.save(str(FNV_DATA / "WorldAtmosphere.esp"))
    import os
    sz = os.path.getsize(str(FNV_DATA / "WorldAtmosphere.esp"))
    print("\nSaved WorldAtmosphere.esp (" + str(sz) + " bytes)")
    print("Total event compositions: " + str(len(events)))


if __name__ == "__main__":
    main()
