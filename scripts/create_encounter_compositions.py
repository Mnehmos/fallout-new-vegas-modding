"""
Encounter Composition Framework — Designed pressure, not just more bodies.

Creates LVLN composition templates that nest existing Enc* building blocks
into tactically interesting squad compositions. Then injects those compositions
into regional encounter LVLC lists.

Design principles:
  - Every encounter has: anchor threat + pressure mechanic + complication
  - Factions feel doctrinally distinct
  - Creatures follow ecology (pack + alpha, swarm + queen, scouts + ambush)
  - Compositions scale via nested leveled lists, not HP inflation
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# ══════════════════════════════════════════════════════════════
#  BUILDING BLOCK FORMIDS (existing Enc* LVLN lists)
# ══════════════════════════════════════════════════════════════

# Fiends
FIEND_GUN = 0x0F1C83         # EncFiendGun (picks 1 random gun fiend)
FIEND_MELEE = 0x0F1C85       # EncFiendMelee (picks 1 random melee fiend)
FIEND_RIFLE = 0x0F1C89       # EncFiendRifle (picks 1 random rifle fiend)
FIEND_SPECIAL = 0x0F1C8A     # EncFiendSpecial (flamer/heavy)

# NCR
NCR_TROOPER = 0x0A46F8       # EncNCRTrooper (picks 1 random trooper)
NCR_TROOPER_GUN = 0x0A46F6   # EncNCRTrooperGun
NCR_TROOPER_GUN1 = 0x0A46F7  # EncNCRTrooperGun1 (wider pool)
NCR_TROOPER_GUN2 = 0x0A46F9  # EncNCRTrooperGun2

# Raiders / Powder Gangers
RAIDER_GUN = 0x029627        # EncRaiderGun
RAIDER_MELEE = 0x02F6E8      # EncRaiderMelee
RAIDER_RIFLE = 0x07F4E1      # EncRaiderRifle
RAIDER_SPECIAL = 0x02967A    # EncRaiderSpecial

# Brotherhood
BOS_GUN = 0x000A87           # EncBrotherhoodOfSteelGun
BOS_MELEE = 0x000A88         # EncBrotherhoodOfSteelMelee
BOS_SPECIAL = 0x000A89       # EncBrotherhoodOfSteelSpecial

# Super Mutants
SMUTANT_GUN = 0x02359F       # EncSuperMutantGun
SMUTANT_MELEE = 0x03A14A     # EncSuperMutantMelee
SMUTANT_MINIGUN = 0x092C53   # EncSuperMutantMinigun
SMUTANT_MISSILE = 0x092C50   # EncSuperMutantMissile
SMUTANT_NIGHTKIN_MELEE = 0x07EA2F  # EncSuperMutantNightkinMelee
SMUTANT_NIGHTKIN_GUN = 0x07EA2E    # EncSuperMutantNightkinGun

# Creatures (LVLC)
DEATHCLAW_SMALL = 0x15679E   # VEncTier3DeathclawSmall
DEATHCLAW_MED = 0x1567AB     # VEncTier4DeathclawMed
CAZADOR_SMALL = 0x15CE1A     # VEncCazadorTier1 — actually EncCazador
CAZADOR = 0x12A22D           # EncCazador
NIGHTSTALKER_SMALL = 0x156799  # Placeholder — need actual FormID
GHOUL = 0x0235A7             # EncFeralGhoul
GECKO = 0x0E5867             # EncWastelandNVGecko
RADSCORPION = 0x02359D       # EncRadScorpion
COYOTE = 0x104163            # EncCoyote


def create_composition(builder, edid, entries):
    """Create a LVLN composition list.

    entries: [(formid, count, level), ...]
    The formid can be another LVLN (nested composition) or an NPC_/CREA.
    """
    fid = builder.allocate_form_id()
    rec = RecordBuilder("LVLN", fid)
    rec.add_string("EDID", edid)
    rec.add(SR.from_bytes("OBND", b"\x00" * 12))
    rec.add(SR.from_bytes("LVLD", struct.pack("<B", 0)))     # Chance none = 0
    rec.add(SR.from_bytes("LVLF", struct.pack("<B", 0x01)))  # CalcAll (spawn ALL entries)
    rec.add(SR.from_bytes("LLCT", struct.pack("<B", len(entries))))

    for item_fid, count, level in entries:
        rec.add_bytes("LVLO", struct.pack("<hHIhH", level, 0, item_fid, count, 0))

    builder.add_record("LVLN", rec)
    return fid


def main():
    print("=== Encounter Composition Framework ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "WorldAtmosphere.esp"))

    compositions = {}

    # ══════════════════════════════════════════
    #  FIEND COMPOSITIONS — Chaotic, chem-fueled
    # ══════════════════════════════════════════
    print("-- Fiend Doctrine --")

    # Fiend Rush Squad: 2 melee rushers + 1 gunner (chaotic pressure)
    compositions["FiendRush"] = create_composition(builder, "MnCompFiendRush", [
        (FIEND_MELEE, 2, 1),    # 2 melee rushers
        (FIEND_GUN, 1, 1),      # 1 covering gunner
    ])
    print("  FiendRush: 2 melee + 1 gun")

    # Fiend Warband: 2 guns + 1 melee + 1 rifle (full mixed squad)
    compositions["FiendWarband"] = create_composition(builder, "MnCompFiendWarband", [
        (FIEND_GUN, 2, 1),      # 2 gunners (noise/suppression)
        (FIEND_MELEE, 1, 1),    # 1 melee closer
        (FIEND_RIFLE, 1, 5),    # 1 rifle (appears at level 5+)
    ])
    print("  FiendWarband: 2 gun + 1 melee + 1 rifle")

    # Fiend Heavy Squad: 1 special + 2 guns + 1 melee (the real fight)
    compositions["FiendHeavy"] = create_composition(builder, "MnCompFiendHeavy", [
        (FIEND_SPECIAL, 1, 10),  # 1 heavy (flamer/special)
        (FIEND_GUN, 2, 1),       # 2 gunner screen
        (FIEND_MELEE, 1, 1),     # 1 melee rusher
        (FIEND_RIFLE, 1, 8),     # 1 rifle support
    ])
    print("  FiendHeavy: 1 special + 2 gun + 1 melee + 1 rifle")

    # ══════════════════════════════════════════
    #  NCR COMPOSITIONS — Organized, ranged, defensive
    # ══════════════════════════════════════════
    print("\n-- NCR Doctrine --")

    # NCR Fire Team: 3 troopers (basic patrol)
    compositions["NCRFireTeam"] = create_composition(builder, "MnCompNCRFireTeam", [
        (NCR_TROOPER_GUN, 2, 1),  # 2 rifle troopers
        (NCR_TROOPER, 1, 1),      # 1 general trooper (varied loadout)
    ])
    print("  NCRFireTeam: 2 gun + 1 general")

    # NCR Squad: 4 troopers + varied weapons (organized response)
    compositions["NCRSquad"] = create_composition(builder, "MnCompNCRSquad", [
        (NCR_TROOPER_GUN1, 2, 1),  # 2 rifle line
        (NCR_TROOPER_GUN2, 1, 5),  # 1 marksman (higher tier)
        (NCR_TROOPER, 1, 1),       # 1 general
    ])
    print("  NCRSquad: 2 rifle + 1 marksman + 1 general")

    # NCR Heavy Patrol: troopers + heavy (dangerous patrol)
    compositions["NCRHeavy"] = create_composition(builder, "MnCompNCRHeavy", [
        (NCR_TROOPER_GUN1, 3, 1),  # 3 rifle line
        (NCR_TROOPER_GUN2, 1, 8),  # 1 heavy gunner
        (NCR_TROOPER, 1, 1),       # 1 leader
    ])
    print("  NCRHeavy: 3 rifle + 1 heavy + 1 leader")

    # ══════════════════════════════════════════
    #  RAIDER / POWDER GANGER — Desperate ambushers
    # ══════════════════════════════════════════
    print("\n-- Raider/Powder Ganger Doctrine --")

    # Raider Ambush: 1 rifle overwatch + 2 gun rushers
    compositions["RaiderAmbush"] = create_composition(builder, "MnCompRaiderAmbush", [
        (RAIDER_RIFLE, 1, 1),    # 1 rifle (overwatch)
        (RAIDER_GUN, 2, 1),      # 2 gun (rush from cover)
    ])
    print("  RaiderAmbush: 1 rifle + 2 gun")

    # Raider Gang: mixed desperation
    compositions["RaiderGang"] = create_composition(builder, "MnCompRaiderGang", [
        (RAIDER_GUN, 2, 1),      # 2 guns
        (RAIDER_MELEE, 1, 1),    # 1 melee (the brave/stupid one)
        (RAIDER_RIFLE, 1, 5),    # 1 rifle
        (RAIDER_SPECIAL, 1, 10), # 1 special (explosive/heavy)
    ])
    print("  RaiderGang: 2 gun + 1 melee + 1 rifle + 1 special")

    # ══════════════════════════════════════════
    #  BROTHERHOOD — Power armor discipline
    # ══════════════════════════════════════════
    print("\n-- Brotherhood Doctrine --")

    # BoS Patrol: 2 gun + 1 melee (power armor wall)
    compositions["BOSPatrol"] = create_composition(builder, "MnCompBOSPatrol", [
        (BOS_GUN, 2, 1),         # 2 energy weapon paladins
        (BOS_MELEE, 1, 1),       # 1 melee knight
    ])
    print("  BOSPatrol: 2 gun + 1 melee")

    # BoS Strike Team: full complement
    compositions["BOSStrike"] = create_composition(builder, "MnCompBOSStrike", [
        (BOS_GUN, 2, 1),         # 2 gunners
        (BOS_MELEE, 1, 1),       # 1 melee
        (BOS_SPECIAL, 1, 10),    # 1 heavy (gatling/missile)
    ])
    print("  BOSStrike: 2 gun + 1 melee + 1 heavy")

    # ══════════════════════════════════════════
    #  SUPER MUTANT — Brutal force
    # ══════════════════════════════════════════
    print("\n-- Super Mutant Doctrine --")

    # Mutant Pack: melee front + gun support
    compositions["MutantPack"] = create_composition(builder, "MnCompMutantPack", [
        (SMUTANT_MELEE, 2, 1),     # 2 melee brutes
        (SMUTANT_GUN, 1, 1),       # 1 gunner
    ])
    print("  MutantPack: 2 melee + 1 gun")

    # Mutant War Party: full escalation
    compositions["MutantWar"] = create_composition(builder, "MnCompMutantWar", [
        (SMUTANT_MELEE, 2, 1),     # 2 melee
        (SMUTANT_GUN, 1, 1),       # 1 gun
        (SMUTANT_MINIGUN, 1, 12),  # 1 minigun (appears lv12+)
        (SMUTANT_NIGHTKIN_MELEE, 1, 15),  # 1 nightkin (lv15+)
    ])
    print("  MutantWar: 2 melee + 1 gun + 1 minigun + 1 nightkin")

    # ══════════════════════════════════════════
    #  CREATURE ECOLOGY — Pack dynamics
    # ══════════════════════════════════════════
    print("\n-- Creature Ecology --")

    # Ghoul Swarm: wave of weak + 1 durable reaver
    compositions["GhoulSwarm"] = create_composition(builder, "MnCompGhoulSwarm", [
        (GHOUL, 3, 1),           # 3 feral ghouls (trash wave)
        (GHOUL, 1, 10),          # 1 more at higher level (tougher variant)
    ])
    print("  GhoulSwarm: 3 ferals + 1 tough")

    # Gecko Pack: juveniles + adult
    compositions["GeckoPack"] = create_composition(builder, "MnCompGeckoPack", [
        (GECKO, 3, 1),           # 3 geckos
        (GECKO, 1, 8),           # 1 tougher (fire gecko at higher level)
    ])
    print("  GeckoPack: 3 weak + 1 tough")

    # Coyote Pack: scouts + den mother
    compositions["CoyotePack"] = create_composition(builder, "MnCompCoyotePack", [
        (COYOTE, 3, 1),         # 3 coyotes
        (COYOTE, 1, 5),         # 1 tougher variant
    ])
    print("  CoyotePack: 3 + 1 alpha")

    # Radscorpion Nest: adults + giant
    compositions["ScorpionNest"] = create_composition(builder, "MnCompScorpionNest", [
        (RADSCORPION, 2, 1),    # 2 radscorpions
        (RADSCORPION, 1, 10),   # 1 giant variant
    ])
    print("  ScorpionNest: 2 normal + 1 giant")

    # ══════════════════════════════════════════
    #  INJECT INTO REGIONAL ENCOUNTER LISTS
    # ══════════════════════════════════════════
    print("\n-- Injecting into Regional Lists --")

    # Main wasteland encounter list — add our compositions as options
    # EncWastelandNV (0x0E5864) — the master list
    for r in esm.get_records("LVLC"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        if eid == "EncWastelandNV":
            rec = RecordBuilder("LVLC", r.id)
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    # We'll add fiend, raider, mutant, ghoul, gecko, scorpion, coyote
                    new_count = min(old_count + 7, 255)
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", new_count)))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))

            # Add compositions at appropriate levels
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 3, 0, compositions["RaiderAmbush"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 5, 0, compositions["GhoulSwarm"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 5, 0, compositions["CoyotePack"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 8, 0, compositions["GeckoPack"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 8, 0, compositions["FiendRush"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 10, 0, compositions["ScorpionNest"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 14, 0, compositions["MutantPack"], 1, 0))

            builder.add_raw_record("LVLC", rec.build())
            print("  EncWastelandNV: +7 composition encounters")
            break

    # Valley Road encounters — early-game compositions
    for r in esm.get_records("LVLC"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        if eid == "VEncVarTier2ValleyRoad":
            rec = RecordBuilder("LVLC", r.id)
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", min(old_count + 3, 255))))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))

            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, compositions["CoyotePack"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, compositions["GeckoPack"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, compositions["RaiderAmbush"], 1, 0))

            builder.add_raw_record("LVLC", rec.build())
            print("  VEncVarTier2ValleyRoad: +3 compositions")
            break

    # Tough encounters — add military compositions
    for r in esm.get_records("LVLC"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        if eid == "EncWastelandNVTough":
            rec = RecordBuilder("LVLC", r.id)
            old_count = 0
            for sr in srs:
                if sr.type == "LLCT":
                    old_count = sr.data[0]
                    rec.add(SR.from_bytes("LLCT", struct.pack("<B", min(old_count + 4, 255))))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))

            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, compositions["FiendHeavy"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, compositions["MutantWar"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, compositions["BOSStrike"], 1, 0))
            rec.add_bytes("LVLO", struct.pack("<hHIhH", 1, 0, compositions["NCRHeavy"], 1, 0))

            builder.add_raw_record("LVLC", rec.build())
            print("  EncWastelandNVTough: +4 military compositions")
            break

    # Save
    builder.save(str(FNV_DATA / "WorldAtmosphere.esp"))
    import os
    sz = os.path.getsize(str(FNV_DATA / "WorldAtmosphere.esp"))
    print("\nSaved WorldAtmosphere.esp (" + str(sz) + " bytes)")
    print("\nCompositions created: " + str(len(compositions)))
    print("\nEncounter design:")
    print("  Fiend: chaotic rush / mixed warband / heavy with screen")
    print("  NCR: fire team / organized squad / heavy patrol")
    print("  Raider: ambush overwatch / desperate gang")
    print("  Brotherhood: power armor patrol / strike team")
    print("  Super Mutant: brute pack / war party with nightkin")
    print("  Ghouls: trash swarm + durable threat")
    print("  Geckos: juvenile pack + adult")
    print("  Coyotes: scouts + alpha")
    print("  Scorpions: nest + giant")


if __name__ == "__main__":
    main()
