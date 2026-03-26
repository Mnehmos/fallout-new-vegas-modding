"""
Tactical AI Overhaul — Faction-specific combat styles + AI tuning.

Creates custom CSTY records that give each faction distinct combat behavior:
- NCR: Disciplined, cover-heavy, long fire windows, slow to advance
- Legion: Aggressive, rushes cover, short waits, flanking
- Fiends: Erratic, barely uses cover, rushes blindly, high fire rate
- Brotherhood: Methodical, heavy cover, suppressive fire windows
- Raiders: Cowardly, takes cover, short engagements, flees when hurt
- Deathclaws: Zero cover, zero wait, pure aggression, fast close
- Cazadors: No cover, rapid attack, swarm behavior

Then overrides AIDT on key NPC templates for confidence/aggression tuning.
Also assigns combat styles via ZNAM on faction NPC templates.

CSSD fields (Simple - ranges and timing):
  0-3:   cover search radius (f32)
  4-7:   take cover chance (f32) — 0.0-1.0
  8-11:  wait timer min (f32) — time in cover before peeking
  12-15: wait timer max (f32)
  16-19: wait to fire timer min (f32) — time peeking before shooting
  20-23: wait to fire timer max (f32)
  24-27: fire timer min (f32) — how long they shoot per burst
  28-31: fire timer max (f32)
  32-35: ranged weapon range mult min (f32)
  36-39: unused
  40-43: weapon restrictions (u32)
  44-47: ranged weapon range mult max (f32)
  48-51: max targeting FOV (f32)
  52-55: combat radius (f32)
  56-59: semi-auto firing delay mult min (f32)
  60-63: semi-auto firing delay mult max (f32)
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# Vanilla combat style FormIDs to override
CS_NCR = 0x137AC1        # CSNCRTrooper
CS_LEGION = 0x137AC0      # CSLegionary
CS_DEFAULT = 0x3D          # DefaultCombatstyle


def build_cssd(cover_radius, cover_chance, wait_min, wait_max,
               wait_fire_min, wait_fire_max, fire_min, fire_max,
               range_mult_min, range_mult_max=0.0,
               combat_radius=0.0, semi_delay_min=1.0, semi_delay_max=1.0):
    """Build a CSSD (Simple combat style data) subrecord."""
    data = struct.pack("<ff", cover_radius, cover_chance)        # 0-7
    data += struct.pack("<ff", wait_min, wait_max)               # 8-15
    data += struct.pack("<ff", wait_fire_min, wait_fire_max)     # 16-23
    data += struct.pack("<ff", fire_min, fire_max)               # 24-31
    data += struct.pack("<f", range_mult_min)                    # 32-35
    data += struct.pack("<I", 0)                                 # 36-39 unused
    data += struct.pack("<I", 0)                                 # 40-43 weapon restrictions
    data += struct.pack("<f", range_mult_max)                    # 44-47
    data += struct.pack("<f", 0.0)                               # 48-51 max targeting FOV
    data += struct.pack("<f", combat_radius)                     # 52-55
    data += struct.pack("<ff", semi_delay_min, semi_delay_max)   # 56-63
    return data


def main():
    print("=== Tactical AI Overhaul ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    builder = ESPBuilder.load_existing(str(FNV_DATA / "WorldAtmosphere.esp"))

    styles = {}

    # ══════════════════════════════════════════
    # FACTION COMBAT STYLES
    # ══════════════════════════════════════════

    # NCR: Disciplined, cover-heavy, sustained fire, slow to move
    print("-- NCR Doctrine: Disciplined Ranged --")
    fid = builder.allocate_form_id()
    rec = RecordBuilder("CSTY", fid)
    rec.add_string("EDID", "MnCSNCRDisciplined")

    # Clone CSTD from vanilla NCR, modify dodge/block
    for r in esm.get_records("CSTY"):
        if r.id == CS_NCR:
            for sr in r.parse_subrecords():
                if sr.type == "CSTD":
                    cstd = bytearray(sr.data)
                    cstd[0] = 60    # dodge 60% (disciplined but not acrobatic)
                    cstd[36] = 20   # block 20%
                    cstd[37] = 50   # attack 50% (measured)
                    cstd[52] = 15   # power attack 15%
                    rec.add_bytes("CSTD", bytes(cstd))
                if sr.type == "CSAD":
                    rec.add(SR.from_bytes("CSAD", sr.data))
            break

    # NCR: high cover chance, long fire windows, stays at range
    rec.add_bytes("CSSD", build_cssd(
        cover_radius=1500.0,  cover_chance=0.9,     # Very cover-oriented
        wait_min=1.5,         wait_max=3.0,          # Patient in cover
        wait_fire_min=0.5,    wait_fire_max=1.5,     # Quick to aim
        fire_min=3.0,         fire_max=5.0,          # Long sustained bursts
        range_mult_min=1.2,   range_mult_max=1.5,    # Prefers range
    ))
    builder.add_record("CSTY", rec)
    styles["NCR"] = fid
    print("  Created: cover=90%, fire=3-5s, range x1.2-1.5")

    # Legion: Aggressive, low cover, fast close, flanking
    print("\n-- Legion Doctrine: Aggressive Rush --")
    fid = builder.allocate_form_id()
    rec = RecordBuilder("CSTY", fid)
    rec.add_string("EDID", "MnCSLegionAggressive")

    for r in esm.get_records("CSTY"):
        if r.id == CS_LEGION:
            for sr in r.parse_subrecords():
                if sr.type == "CSTD":
                    cstd = bytearray(sr.data)
                    cstd[0] = 40    # dodge 40% (charges through)
                    cstd[36] = 50   # block 50% (shield discipline)
                    cstd[37] = 70   # attack 70% (aggressive)
                    cstd[52] = 40   # power attack 40% (big swings)
                    rec.add_bytes("CSTD", bytes(cstd))
                if sr.type == "CSAD":
                    rec.add(SR.from_bytes("CSAD", sr.data))
            break

    rec.add_bytes("CSSD", build_cssd(
        cover_radius=500.0,   cover_chance=0.3,      # Barely uses cover
        wait_min=0.5,         wait_max=1.0,           # Short wait
        wait_fire_min=0.2,    wait_fire_max=0.5,      # Quick to engage
        fire_min=1.0,         fire_max=2.0,            # Short bursts then advance
        range_mult_min=0.6,   range_mult_max=0.8,     # Wants to close distance
    ))
    builder.add_record("CSTY", rec)
    styles["Legion"] = fid
    print("  Created: cover=30%, fire=1-2s, range x0.6-0.8, rush")

    # Fiend: Erratic, no discipline, sprays and charges
    print("\n-- Fiend Doctrine: Chemmed Chaos --")
    fid = builder.allocate_form_id()
    rec = RecordBuilder("CSTY", fid)
    rec.add_string("EDID", "MnCSFiendChaos")

    for r in esm.get_records("CSTY"):
        if r.id == CS_DEFAULT:
            for sr in r.parse_subrecords():
                if sr.type == "CSTD":
                    cstd = bytearray(sr.data)
                    cstd[0] = 20    # dodge 20% (too high to dodge)
                    cstd[36] = 5    # block 5% (no discipline)
                    cstd[37] = 85   # attack 85% (spray everything)
                    cstd[52] = 60   # power attack 60% (wild swings)
                    rec.add_bytes("CSTD", bytes(cstd))
                if sr.type == "CSAD":
                    rec.add(SR.from_bytes("CSAD", sr.data))
            break

    rec.add_bytes("CSSD", build_cssd(
        cover_radius=300.0,   cover_chance=0.15,     # Almost never takes cover
        wait_min=0.2,         wait_max=0.5,           # Barely waits
        wait_fire_min=0.1,    wait_fire_max=0.3,      # Instant aggro
        fire_min=2.0,         fire_max=6.0,            # Long spray (wasteful)
        range_mult_min=0.5,   range_mult_max=0.7,     # Charges in
    ))
    builder.add_record("CSTY", rec)
    styles["Fiend"] = fid
    print("  Created: cover=15%, fire=2-6s spray, range x0.5-0.7")

    # Brotherhood: Methodical, heavy cover, suppressive
    print("\n-- Brotherhood Doctrine: Power Armor Methodical --")
    fid = builder.allocate_form_id()
    rec = RecordBuilder("CSTY", fid)
    rec.add_string("EDID", "MnCSBOSMethodical")

    for r in esm.get_records("CSTY"):
        if r.id == CS_DEFAULT:
            for sr in r.parse_subrecords():
                if sr.type == "CSTD":
                    cstd = bytearray(sr.data)
                    cstd[0] = 30    # dodge 30% (power armor, dont need to dodge)
                    cstd[36] = 10   # block 10%
                    cstd[37] = 60   # attack 60%
                    cstd[52] = 20   # power attack 20%
                    rec.add_bytes("CSTD", bytes(cstd))
                if sr.type == "CSAD":
                    rec.add(SR.from_bytes("CSAD", sr.data))
            break

    rec.add_bytes("CSSD", build_cssd(
        cover_radius=2000.0,  cover_chance=0.7,      # Uses cover but not reliant
        wait_min=1.0,         wait_max=2.0,           # Measured timing
        wait_fire_min=0.5,    wait_fire_max=1.0,      # Aims carefully
        fire_min=4.0,         fire_max=7.0,            # Long suppressive bursts
        range_mult_min=1.0,   range_mult_max=1.3,     # Comfortable at range
    ))
    builder.add_record("CSTY", rec)
    styles["BOS"] = fid
    print("  Created: cover=70%, fire=4-7s suppress, range x1.0-1.3")

    # Raider/Powder Ganger: Cowardly, opportunistic
    print("\n-- Raider Doctrine: Cowardly Opportunist --")
    fid = builder.allocate_form_id()
    rec = RecordBuilder("CSTY", fid)
    rec.add_string("EDID", "MnCSRaiderCoward")

    for r in esm.get_records("CSTY"):
        if r.id == CS_DEFAULT:
            for sr in r.parse_subrecords():
                if sr.type == "CSTD":
                    cstd = bytearray(sr.data)
                    cstd[0] = 80    # dodge 80% (self-preservation)
                    cstd[36] = 10   # block 10%
                    cstd[37] = 35   # attack 35% (hesitant)
                    cstd[52] = 10   # power attack 10%
                    rec.add_bytes("CSTD", bytes(cstd))
                if sr.type == "CSAD":
                    rec.add(SR.from_bytes("CSAD", sr.data))
            break

    rec.add_bytes("CSSD", build_cssd(
        cover_radius=2000.0,  cover_chance=0.85,     # Hides a lot
        wait_min=2.0,         wait_max=4.0,           # Stays hidden
        wait_fire_min=1.0,    wait_fire_max=2.0,      # Slow to engage
        fire_min=1.0,         fire_max=2.0,            # Short bursts then hide
        range_mult_min=1.0,   range_mult_max=1.2,     # Stays back
    ))
    builder.add_record("CSTY", rec)
    styles["Raider"] = fid
    print("  Created: cover=85%, fire=1-2s peek, dodge=80%")

    # ══════════════════════════════════════════
    # APPLY STYLES TO FACTION NPCs
    # ══════════════════════════════════════════
    print("\n-- Applying Combat Styles to NPCs --")

    # Map faction keywords to combat style
    faction_styles = {
        "Fiend": styles["Fiend"],
        "Legion": styles["Legion"],
        "NCRTrooper": styles["NCR"],
        "NCRRanger": styles["NCR"],
        "Brotherhood": styles["BOS"],
        "Raider": styles["Raider"],
        "PowderGanger": styles["Raider"],
    }

    # Override AIDT + ZNAM on faction NPC_ templates
    applied = 0
    for r in esm.get_records("NPC_"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")

        # Match faction
        matched_style = None
        for keyword, style_fid in faction_styles.items():
            if keyword in eid:
                matched_style = style_fid
                break

        if not matched_style:
            continue

        # Skip dead/template/unique NPCs
        if any(skip in eid.lower() for skip in ["dead", "template", "unique", "audio", "corpse"]):
            continue

        # Build override with ZNAM (combat style) and tuned AIDT
        rec = RecordBuilder("NPC_", r.id)
        has_znam = False
        for sr in srs:
            if sr.type == "ZNAM":
                # Replace combat style
                rec.add_formid("ZNAM", matched_style)
                has_znam = True
            elif sr.type == "AIDT" and len(sr.data) >= 12:
                aidt = bytearray(sr.data)
                # Tune by faction
                if matched_style == styles["Legion"]:
                    aidt[0] = 2     # Very Aggressive
                    aidt[1] = 3     # Brave
                elif matched_style == styles["Fiend"]:
                    aidt[0] = 3     # Frenzied
                    aidt[1] = 4     # Foolhardy
                elif matched_style == styles["NCR"]:
                    aidt[0] = 1     # Aggressive (not frenzied)
                    aidt[1] = 2     # Average (retreats when hurt)
                elif matched_style == styles["BOS"]:
                    aidt[0] = 1     # Aggressive
                    aidt[1] = 3     # Brave (power armor confidence)
                elif matched_style == styles["Raider"]:
                    aidt[0] = 1     # Aggressive
                    aidt[1] = 1     # Cautious (runs when losing)
                rec.add_bytes("AIDT", bytes(aidt))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        if not has_znam:
            rec.add_formid("ZNAM", matched_style)

        builder.add_raw_record("NPC_", rec.build())
        applied += 1

    print("  Applied combat styles to " + str(applied) + " NPCs")

    # Save
    builder.save(str(FNV_DATA / "WorldAtmosphere.esp"))
    import os
    sz = os.path.getsize(str(FNV_DATA / "WorldAtmosphere.esp"))
    print("\nSaved WorldAtmosphere.esp (" + str(sz) + " bytes)")
    print("\nFaction AI Summary:")
    print("  NCR:     cover=90%, sustained fire 3-5s, stays at range, retreats when hurt")
    print("  Legion:  cover=30%, rushes in, short bursts, closes distance, brave")
    print("  Fiends:  cover=15%, sprays 2-6s, charges blindly, foolhardy, frenzied")
    print("  BoS:     cover=70%, suppressive fire 4-7s, methodical, brave in power armor")
    print("  Raiders: cover=85%, peeks 1-2s, high dodge, cautious, runs when losing")


if __name__ == "__main__":
    main()
