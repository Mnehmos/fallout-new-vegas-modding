"""
All 10 Playstyle Paths — 80 New Perks via Binary Writer

Each path clones from the appropriate vanilla template perk to get
the right condition structure, then patches Entry Point + EPFD.

Templates used:
  Gunslinger  (func=108==4, pistol)         → Gunslinger path
  Commando    (func=108==5 OR 6, rifles)    → Rifleman path
  Slayer      (func=109==1 OR, melee)       → Brawler path
  Pyromaniac  (func=372==1, weapon type)    → Demolisher path (explosives)
  LaserCmdr   (func=372==1, weapon type)    → Scientist path (energy)
  Cowboy      (func=372==1, weapon type)    → (alt template)
  NinjaPerk   (sneak conditions)            → Shadow path
  Toughness   (no weapon filter)            → Survivor path
  Chemist     (no weapon filter)            → Doctor path
  BetterCriticals (no weapon filter)        → Diplomat path
  Gunslinger  (no weapon filter variant)    → Archivist path
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")


def load_template(esm, edid):
    """Load a perk's raw subrecords by EditorID."""
    for r in esm.get_records("PERK"):
        srs = r.parse_subrecords()
        for sr in srs:
            if sr.type == "EDID" and sr.data.rstrip(b"\x00").decode() == edid:
                return srs
    raise RuntimeError(f"Template perk not found: {edid}")


def build_perk(builder, template_srs, perk_def):
    """Build a PERK record by cloning template subrecords with patches."""
    fid = builder.allocate_form_id()
    rec = RecordBuilder("PERK", fid)

    effect_data_seen = False  # Track which DATA we're on (perk-level vs effect-level)

    for sr in template_srs:
        if sr.type == "EDID":
            rec.add_string("EDID", perk_def["edid"])
        elif sr.type == "FULL":
            rec.add_string("FULL", perk_def["name"])
        elif sr.type == "DESC":
            rec.add_string("DESC", perk_def["desc"])
        elif sr.type == "DATA" and len(sr.data) in (4, 5) and not effect_data_seen:
            # Perk-level DATA
            if len(sr.data) == 5:
                new_data = struct.pack("<5B", 0, perk_def["level"], 1, 1, 0)
            else:
                new_data = struct.pack("<4B", 0, perk_def["level"], 1, 1)
            rec.add_bytes("DATA", new_data)
        elif sr.type == "DATA" and len(sr.data) == 3:
            # Effect-level DATA: patch Entry Point, keep Function + TabCount
            effect_data_seen = True
            ep = perk_def["entry_point"]
            func = sr.data[1]  # Keep original function type
            tabs = sr.data[2]  # Keep original tab count
            rec.add_bytes("DATA", struct.pack("<3B", ep, func, tabs))
        elif sr.type == "EPFD":
            rec.add_float("EPFD", perk_def["epfd"])
        elif sr.type == "CTDA" and not effect_data_seen:
            # Perk-level conditions (skill requirements) — skip them
            # Our perks only require level, not skills
            continue
        elif sr.type == "PRKE":
            effect_data_seen = True
            rec.add(SR.from_bytes(sr.type, sr.data))
        else:
            rec.add(SR.from_bytes(sr.type, sr.data))

    builder.add_record("PERK", rec)
    return fid


# ══════════════════════════════════════════════════════════════
#  PATH DEFINITIONS
# ══════════════════════════════════════════════════════════════

# Path 1: Gunslinger (already created — skip)
# Template: Gunslinger (func=108==4, pistol)

# Path 2: Rifleman — Two-handed rifles
# Template: Commando (func=108==5 OR 6)
RIFLEMAN = [
    {"edid": "MnMarksman",       "name": "Marksman",        "desc": "Steady hands on the stock. Rifle spread reduced by 20%.",                    "level": 4,  "entry_point": 34, "epfd": 0.80},
    {"edid": "MnIronSights",     "name": "Iron Sights",     "desc": "You know exactly where the sights should sit. Rifle damage increased by 10%.", "level": 6,  "entry_point": 0,  "epfd": 1.10},
    {"edid": "MnSteadyAim",      "name": "Steady Aim",      "desc": "Controlled breathing. Rifle VATS accuracy increased by 25%.",                 "level": 8,  "entry_point": 8,  "epfd": 1.25},
    {"edid": "MnRapidCycle",     "name": "Rapid Cycle",     "desc": "Work the bolt like it owes you money. Rifle fire rate increased by 15%.",     "level": 10, "entry_point": 43, "epfd": 1.15},
    {"edid": "MnPrecisionShot",  "name": "Precision Shot",  "desc": "Aim small, miss small. Rifle critical damage increased by 40%.",              "level": 12, "entry_point": 2,  "epfd": 1.40},
    {"edid": "MnTacticalReload", "name": "Tactical Reload", "desc": "Mag changes are second nature. Rifle reload speed increased by 30%.",         "level": 14, "entry_point": 37, "epfd": 1.30},
    {"edid": "MnSuppressive",    "name": "Suppressive Fire", "desc": "Keep their heads down. Rifle VATS AP cost reduced by 15%.",                  "level": 16, "entry_point": 40, "epfd": 0.85},
    {"edid": "MnSharpshooter",   "name": "Sharpshooter",    "desc": "Master of the long gun. Rifle damage increased by 20%.",                     "level": 18, "entry_point": 0,  "epfd": 1.20},
]

# Path 3: Demolisher — Explosives
# Template: Pyromaniac (func=372==1, general weapon type filter)
DEMOLISHER = [
    {"edid": "MnBlastRadius",    "name": "Blast Radius",     "desc": "Your explosives have a wider kill zone. Explosive damage increased by 15%.",   "level": 6,  "entry_point": 0,  "epfd": 1.15},
    {"edid": "MnShortFuse",      "name": "Short Fuse",       "desc": "Quick hands with dangerous things. Explosive equip speed increased by 40%.",   "level": 8,  "entry_point": 38, "epfd": 1.40},
    {"edid": "MnShrapnel",       "name": "Shrapnel",         "desc": "Fragments find soft spots. Explosive critical damage increased by 50%.",        "level": 10, "entry_point": 2,  "epfd": 1.50},
    {"edid": "MnOrdnanceExpert", "name": "Ordnance Expert",  "desc": "You know your payloads. Explosive damage increased by 25%.",                   "level": 14, "entry_point": 0,  "epfd": 1.25},
    {"edid": "MnMineLayer",      "name": "Mine Layer",       "desc": "Mines detonate more reliably. Mine explosion chance greatly increased.",        "level": 12, "entry_point": 4,  "epfd": 1.0},
    {"edid": "MnQuickArm",       "name": "Quick Arm",        "desc": "Throw faster, think later. Explosive fire rate increased by 25%.",              "level": 16, "entry_point": 43, "epfd": 1.25},
    {"edid": "MnHeavyOrdnance",  "name": "Heavy Ordnance",   "desc": "AP efficiency with launchers. Explosive VATS AP cost reduced by 20%.",         "level": 18, "entry_point": 40, "epfd": 0.80},
    {"edid": "MnDemolitionMan",  "name": "Demolition Man",   "desc": "The art of destruction, perfected. Explosive damage increased by 30%.",        "level": 20, "entry_point": 0,  "epfd": 1.30},
]

# Path 4: Shadow — Stealth
# Template: Commando (no weapon filter, just universal bonuses for stealth play)
# These are universal — any weapon, rewarding sneaky playstyle
SHADOW = [
    {"edid": "MnGhostStep",     "name": "Ghost Step",      "desc": "Move like smoke. Sneak speed increased by 20%.",                              "level": 4,  "entry_point": 54, "epfd": 1.20},
    {"edid": "MnSilentKill",    "name": "Silent Kill",     "desc": "First strike from the shadows. Weapon damage increased by 10%.",               "level": 6,  "entry_point": 0,  "epfd": 1.10},
    {"edid": "MnVitalStrike",   "name": "Vital Strike",    "desc": "You know where it hurts. Critical hit damage increased by 40%.",               "level": 8,  "entry_point": 2,  "epfd": 1.40},
    {"edid": "MnPredatorEye",   "name": "Predator's Eye",  "desc": "Patience rewards precision. Critical hit chance increased by 10%.",            "level": 10, "entry_point": 1,  "epfd": 10.0},
    {"edid": "MnPhantom",       "name": "Phantom",         "desc": "Move through the world unseen. Sneak speed increased by 30%.",                 "level": 14, "entry_point": 54, "epfd": 1.30},
    {"edid": "MnExecutioner",   "name": "Executioner",     "desc": "Every shot is a death sentence. Critical damage increased by 60%.",             "level": 16, "entry_point": 2,  "epfd": 1.60},
    {"edid": "MnQuickEscape",   "name": "Quick Escape",    "desc": "Fast on your feet when things go wrong. Equip speed increased by 50%.",        "level": 12, "entry_point": 38, "epfd": 1.50},
    {"edid": "MnShadowMaster",  "name": "Shadow Master",   "desc": "The wasteland never sees you coming. Weapon damage increased by 20%.",         "level": 18, "entry_point": 0,  "epfd": 1.20},
]

# Path 5: Brawler — Melee/Unarmed
# Template: Slayer (func=109==1 OR, melee weapon type filter)
BRAWLER = [
    {"edid": "MnIronFist",       "name": "Iron Fist",        "desc": "Hardened knuckles. Melee damage increased by 15%.",                          "level": 4,  "entry_point": 0,  "epfd": 1.15},
    {"edid": "MnHeavyHands",     "name": "Heavy Hands",      "desc": "Swing harder, hit heavier. Melee critical damage increased by 40%.",         "level": 6,  "entry_point": 2,  "epfd": 1.40},
    {"edid": "MnRushdown",       "name": "Rushdown",         "desc": "Close the gap fast. Movement speed increased by 15%.",                        "level": 8,  "entry_point": 54, "epfd": 1.15},
    {"edid": "MnBoneBreaker",    "name": "Bone Breaker",     "desc": "Target the joints. Limb damage increased by 50%.",                           "level": 10, "entry_point": 6,  "epfd": 1.50},
    {"edid": "MnFlurry",         "name": "Flurry",           "desc": "A storm of blows. Melee attack speed increased by 25%.",                     "level": 12, "entry_point": 43, "epfd": 1.25},
    {"edid": "MnBrawlerGrit",    "name": "Brawler's Grit",   "desc": "Takes a beating, keeps swinging. Damage Threshold increased by 5.",          "level": 14, "entry_point": 56, "epfd": 5.0},
    {"edid": "MnHaymaker",       "name": "Haymaker",         "desc": "One good hit is all it takes. Melee damage increased by 25%.",                "level": 16, "entry_point": 0,  "epfd": 1.25},
    {"edid": "MnChampion",       "name": "Champion",         "desc": "Undisputed. Melee VATS AP cost reduced by 20%.",                             "level": 18, "entry_point": 40, "epfd": 0.80},
]

# Path 6: Scientist — Energy Weapons
# Template: LaserCommander (func=372==1, energy weapon type check)
SCIENTIST = [
    {"edid": "MnOvercharge",     "name": "Overcharge",       "desc": "Push the cells harder. Energy weapon damage increased by 10%.",               "level": 4,  "entry_point": 0,  "epfd": 1.10},
    {"edid": "MnFocusedBeam",    "name": "Focused Beam",     "desc": "Tighter beam, tighter grouping. Energy weapon spread reduced by 25%.",       "level": 6,  "entry_point": 34, "epfd": 0.75},
    {"edid": "MnCapacitorBoost", "name": "Capacitor Boost",  "desc": "Faster energy cycling. Energy weapon fire rate increased by 15%.",            "level": 8,  "entry_point": 43, "epfd": 1.15},
    {"edid": "MnIonization",     "name": "Ionization",       "desc": "Destabilize at the molecular level. Energy crit damage increased by 50%.",   "level": 10, "entry_point": 2,  "epfd": 1.50},
    {"edid": "MnQuickCharge",    "name": "Quick Charge",     "desc": "Swap cells in a heartbeat. Energy weapon reload speed increased by 30%.",    "level": 12, "entry_point": 37, "epfd": 1.30},
    {"edid": "MnPlasmaCore",     "name": "Plasma Core",      "desc": "Maximum energy output. Energy weapon damage increased by 20%.",               "level": 14, "entry_point": 0,  "epfd": 1.20},
    {"edid": "MnPhotonLock",     "name": "Photon Lock",      "desc": "Light-speed targeting. Energy VATS AP cost reduced by 15%.",                  "level": 16, "entry_point": 40, "epfd": 0.85},
    {"edid": "MnSingularity",    "name": "Singularity",      "desc": "Energy weapon mastery. Critical hit chance increased by 10%.",                "level": 18, "entry_point": 1,  "epfd": 10.0},
]

# Path 7: Survivor — Defense & Endurance
# Template: Toughness (no weapon filter, EP 56 = DT)
SURVIVOR = [
    {"edid": "MnThickSkin",     "name": "Thick Skin",       "desc": "Hard to hurt. Damage Threshold increased by 3.",                              "level": 4,  "entry_point": 56, "epfd": 3.0},
    {"edid": "MnSecondWind",    "name": "Second Wind",      "desc": "You keep going when others drop. Movement speed increased by 10%.",            "level": 6,  "entry_point": 54, "epfd": 1.10},
    {"edid": "MnHardTarget",    "name": "Hard Target",      "desc": "Harder to pin down. Enemy crit chance reduced by 15%.",                       "level": 8,  "entry_point": 36, "epfd": 0.85},
    {"edid": "MnIronBelly",     "name": "Iron Belly",       "desc": "Shrug it off. Damage Threshold increased by 5.",                              "level": 10, "entry_point": 56, "epfd": 5.0},
    {"edid": "MnResilience",    "name": "Resilience",       "desc": "Pain is just information. Movement speed increased by 15%.",                   "level": 12, "entry_point": 54, "epfd": 1.15},
    {"edid": "MnBulletSponge",  "name": "Bullet Sponge",   "desc": "They can't put you down. Damage Threshold increased by 8.",                    "level": 14, "entry_point": 56, "epfd": 8.0},
    {"edid": "MnLastStand",     "name": "Last Stand",       "desc": "Defiance in the face of death. Weapon damage increased by 15%.",               "level": 16, "entry_point": 0,  "epfd": 1.15},
    {"edid": "MnUnbreakable",   "name": "Unbreakable",      "desc": "Nothing stops you. Damage Threshold increased by 12.",                        "level": 20, "entry_point": 56, "epfd": 12.0},
]

# Path 8: Diplomat — Social & XP
# Template: Chemist (no weapon filter, universal effect)
DIPLOMAT = [
    {"edid": "MnSilverTongue",  "name": "Silver Tongue",    "desc": "Words are weapons too. XP gain increased by 10%.",                            "level": 2,  "entry_point": 9,  "epfd": 1.10},
    {"edid": "MnQuickStudy",    "name": "Quick Study",      "desc": "Learn from every encounter. XP gain increased by 15%.",                       "level": 6,  "entry_point": 9,  "epfd": 1.15},
    {"edid": "MnOpportunist",   "name": "Opportunist",      "desc": "Strike when they least expect it. Weapon damage increased by 10%.",            "level": 8,  "entry_point": 0,  "epfd": 1.10},
    {"edid": "MnFastTalker",    "name": "Fast Talker",      "desc": "Quick wits, quick hands. Equip speed increased by 30%.",                      "level": 10, "entry_point": 38, "epfd": 1.30},
    {"edid": "MnWorldlyWise",   "name": "Worldly Wise",     "desc": "Experience is the best teacher. XP gain increased by 20%.",                    "level": 12, "entry_point": 9,  "epfd": 1.20},
    {"edid": "MnNegotiator",    "name": "Negotiator",       "desc": "Everything has a price. Reload speed increased by 20%.",                       "level": 14, "entry_point": 37, "epfd": 1.20},
    {"edid": "MnCharismatic",   "name": "Charismatic",      "desc": "People underestimate you. Critical damage increased by 30%.",                  "level": 16, "entry_point": 2,  "epfd": 1.30},
    {"edid": "MnAmbassador",    "name": "Ambassador",       "desc": "You've seen it all. XP gain increased by 30%.",                                "level": 20, "entry_point": 9,  "epfd": 1.30},
]

# Path 9: Doctor — Medicine & Healing
# Template: Chemist (no weapon filter, EP 25 = chem duration)
DOCTOR = [
    {"edid": "MnFieldMedic",    "name": "Field Medic",      "desc": "Fast with a stimpak. Chem duration increased by 25%.",                        "level": 4,  "entry_point": 25, "epfd": 1.25},
    {"edid": "MnSteadyHand",    "name": "Steady Hand",      "desc": "Surgeon's precision. Weapon spread reduced by 15%.",                          "level": 6,  "entry_point": 34, "epfd": 0.85},
    {"edid": "MnAdrenaline",    "name": "Adrenaline Rush",  "desc": "Pain sharpens focus. Attack speed increased by 10%.",                          "level": 8,  "entry_point": 43, "epfd": 1.10},
    {"edid": "MnTriage",        "name": "Triage",           "desc": "Keep yourself together. Damage Threshold increased by 4.",                     "level": 10, "entry_point": 56, "epfd": 4.0},
    {"edid": "MnPharmacist",    "name": "Pharmacist",       "desc": "Maximum potency. Chem duration increased by 50%.",                             "level": 12, "entry_point": 25, "epfd": 1.50},
    {"edid": "MnCombatMedic",   "name": "Combat Medic",     "desc": "Heal under fire. Movement speed increased by 10%.",                            "level": 14, "entry_point": 54, "epfd": 1.10},
    {"edid": "MnNerveStrike",   "name": "Nerve Strike",     "desc": "Know the anatomy. Critical damage increased by 30%.",                          "level": 16, "entry_point": 2,  "epfd": 1.30},
    {"edid": "MnMiracleWorker", "name": "Miracle Worker",   "desc": "You've cheated death before. Chem duration doubled.",                          "level": 18, "entry_point": 25, "epfd": 2.00},
]

# Path 10: Archivist — Our custom faction path
# Template: Toughness (no weapon filter, universal)
ARCHIVIST = [
    {"edid": "MnDataMiner",     "name": "Data Miner",       "desc": "Knowledge is power. XP gain increased by 15%.",                                "level": 2,  "entry_point": 9,  "epfd": 1.15},
    {"edid": "MnFieldAgent",    "name": "Field Agent",      "desc": "Archivist training kicks in. Equip speed increased by 30%.",                   "level": 6,  "entry_point": 38, "epfd": 1.30},
    {"edid": "MnAnalytical",    "name": "Analytical Mind",  "desc": "Study your enemy. Critical hit chance increased by 5%.",                        "level": 8,  "entry_point": 1,  "epfd": 5.0},
    {"edid": "MnPreservation",  "name": "Preservation",     "desc": "Protect what matters. Damage Threshold increased by 5.",                       "level": 10, "entry_point": 56, "epfd": 5.0},
    {"edid": "MnReclamation",   "name": "Reclamation",      "desc": "Waste nothing. Reload speed increased by 25%.",                                "level": 12, "entry_point": 37, "epfd": 1.25},
    {"edid": "MnIndexer",       "name": "Indexer",          "desc": "Catalogue every weakness. Critical damage increased by 40%.",                   "level": 14, "entry_point": 2,  "epfd": 1.40},
    {"edid": "MnArchivistElite","name": "Archivist Elite",  "desc": "Peak efficiency. Weapon damage increased by 15%.",                              "level": 16, "entry_point": 0,  "epfd": 1.15},
    {"edid": "MnCurator",       "name": "Curator",          "desc": "Master of the archive. Damage increased by 25%, DT increased by 8.",           "level": 20, "entry_point": 0,  "epfd": 1.25},
]

# ══════════════════════════════════════════════════════════════
#  BUILD ALL PATHS
# ══════════════════════════════════════════════════════════════

ALL_PATHS = [
    # (path_name, perk_list, template_edid)
    ("Rifleman",    RIFLEMAN,    "Commando"),
    ("Demolisher",  DEMOLISHER,  "Pyromaniac"),
    ("Shadow",      SHADOW,      "Commando"),      # Universal bonuses, no weapon filter needed
    ("Brawler",     BRAWLER,     "Slayer"),
    ("Scientist",   SCIENTIST,   "LaserCommander"),
    ("Survivor",    SURVIVOR,    "Toughness"),
    ("Diplomat",    DIPLOMAT,    "Chemist"),
    ("Doctor",      DOCTOR,      "Chemist"),
    ("Archivist",   ARCHIVIST,   "Toughness"),
]


def main():
    print("=== All Playstyle Paths — Perk Generator ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))

    # Load PerkOverhaul.esp (already has Gunslinger perks)
    esp_path = FNV_DATA / "PerkOverhaul.esp"
    if esp_path.exists():
        builder = ESPBuilder.load_existing(str(esp_path))
        print(f"Loaded {esp_path.name} ({esp_path.stat().st_size} bytes)")
    else:
        builder = ESPBuilder(author="MnemoScript", description="Perk Overhaul — playstyle paths")
        builder.add_master("FalloutNV.esm")
        print(f"Created new {esp_path.name}")

    total = 0

    for path_name, perks, template_edid in ALL_PATHS:
        print(f"\n--{path_name} Path ({template_edid} template) --")
        template = load_template(esm, template_edid)

        for perk_def in perks:
            fid = build_perk(builder, template, perk_def)
            print(f"  + {perk_def['name']:22s} Lv{perk_def['level']:2d} EP={perk_def['entry_point']:2d} x{perk_def['epfd']:.2f}")
            total += 1

    # Save
    try:
        builder.save(str(esp_path))
        print(f"\nSaved: {esp_path} ({esp_path.stat().st_size} bytes)")
    except PermissionError:
        temp_path = Path("f:/tmp/PerkOverhaul.esp")
        builder.save(str(temp_path))
        print(f"\nLocked — saved to: {temp_path} ({temp_path.stat().st_size} bytes)")
        print(f"Copy to: {esp_path}")

    print(f"Total new perks: {total} (+ 8 Gunslinger = {total + 8})")

    # Verify
    print("\n=== Verification ===")
    verify_path = esp_path if esp_path.exists() else Path("f:/tmp/PerkOverhaul.esp")
    esp = PluginFile(str(verify_path))
    mn_count = 0
    for r in esp.get_records("PERK"):
        srs = r.parse_subrecords()
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode()
                if eid.startswith("Mn"):
                    mn_count += 1
                break
    print(f"Mn* perks in ESP: {mn_count}")


if __name__ == "__main__":
    main()
