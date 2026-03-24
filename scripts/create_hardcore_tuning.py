"""
Hardcore Tuning Overhaul

DESIGN:
  Chems: 2x potency, 2x addiction chance, nastier withdrawals
  Stimpaks: Heal 50% less (15 HP instead of 30), still over time
  Super Stimpaks: Heal more (100 HP) but debuff is brutal (-4 STR, -4 AGL for 60s)
  Food: Heals more to compensate for stimpak nerf
  Alcohol: Bigger buffs (+3 STR instead of +1), bigger INT penalty (-3 instead of -1)

PHILOSOPHY:
  Chems should feel like a real gamble - massive power at massive risk.
  Healing should come from food/rest, not stimpak spam.
  Alcohol should be genuinely tempting AND genuinely dangerous.
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")


def override_alch(builder, esm, editor_id, efit_changes):
    """Override an ALCH record, modifying specific EFIT values.

    efit_changes: list of (effect_index, new_magnitude, new_duration) or None to skip
    """
    for r in esm.get_records("ALCH"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if eid != editor_id:
            continue

        rec = RecordBuilder("ALCH", r.id)
        efit_idx = 0
        for sr in srs:
            if sr.type == "EFIT" and len(sr.data) >= 12:
                if efit_idx < len(efit_changes) and efit_changes[efit_idx] is not None:
                    new_mag, new_dur = efit_changes[efit_idx]
                    area = struct.unpack("<I", sr.data[4:8])[0]
                    new_efit = struct.pack("<III", new_mag, area, new_dur)
                    rec.add_bytes("EFIT", new_efit)
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
                efit_idx += 1
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_raw_record("ALCH", rec.build())
        return True
    return False


def main():
    print("=== Hardcore Tuning Overhaul ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))

    builder = ESPBuilder(author="Mnehmos", description="Hardcore Tuning - Chems hit harder, healing hits softer")
    builder.add_master("FalloutNV.esm")

    # ══════════════════════════════════════════
    # STIMPAKS — Nerfed healing
    # ══════════════════════════════════════════
    print("-- Stimpaks (nerfed) --")

    # Stimpak: was 5HP/6s + 6HP/6s = ~36HP. Now 2HP/6s + 3HP/6s = ~15HP
    # Effects: RestoreHealth 5/6s, RestoreHealth 6/6s, RestoreHealthStimpak 30, RestoreHealthStimpak 36
    if override_alch(builder, esm, "Stimpak", [
        (2, 6),    # RestoreHealth 2/6s (was 5)
        (3, 6),    # RestoreHealth 3/6s (was 6)
        (15, 0),   # RestoreHealthStimpak 15 (was 30)
        (18, 0),   # RestoreHealthStimpak 18 (was 36)
    ]):
        print("  Stimpak: 15-18 HP (was 30-36)")

    # Super Stimpak: Bigger heal but worse debuff
    # Was: 20HP/3s + 24HP/3s + debuff 30s. Now: 40HP/3s + 48HP/3s + debuff 60s
    if override_alch(builder, esm, "SuperStimpak", [
        (40, 3),   # RestoreHealth 40/3s (was 20)
        (48, 3),   # RestoreHealth 48/3s (was 24)
        (0, 60),   # SuperStimpakEffect debuff for 60s (was 30s)
        (100, 0),  # RestoreHealthStimpak 100 (was 60)
        (120, 0),  # RestoreHealthStimpak 120 (was 72)
    ]):
        print("  Super Stimpak: 100-120 HP (was 60-72), debuff 60s (was 30s)")

    # Doctor's Bag: More effective
    if override_alch(builder, esm, "DoctorsBag", [
        (60, 0),   # RestoreLimbs 60 (was 36)
        (75, 0),   # RestoreLimbs 75 (was 45)
        (1, 0),    # RestoreAllLimbs (keep)
    ]):
        print("  Doctor's Bag: 60-75 limb restore (was 36-45)")

    # ══════════════════════════════════════════
    # CHEMS — 2x potency, longer addiction window
    # ══════════════════════════════════════════
    print("\n-- Chems (buffed potency, nastier addiction) --")

    # Buffout: +4 STR, +5 END, +100 HP (was +2/+3/+60)
    if override_alch(builder, esm, "Buffout", [
        (4, 240),     # STR +4 (was +2)
        (5, 240),     # END +5 (was +3)
        (100, 240),   # HP +100 (was +60)
        (50, 108000), # Addiction chance 50% (was 30%)
    ]):
        print("  Buffout: +4 STR, +5 END, +100 HP (was +2/+3/+60)")

    # Jet: +30 AP (was +15)
    if override_alch(builder, esm, "Jet", [
        (30, 240),    # AP +30 (was +15)
        (50, 108000), # Addiction 50% (was 30%)
    ]):
        print("  Jet: +30 AP (was +15)")

    # Psycho: Effect is via PsychoMagicEffect (script-based +25% dmg)
    # We can boost the duration
    if override_alch(builder, esm, "Psycho", [
        (0, 360),     # PsychoMagicEffect for 360s (was 240s)
        (50, 108000), # Addiction 50% (was 30%)
    ]):
        print("  Psycho: duration 360s (was 240s), addiction 50%")

    # Med-X: +40 DR (was +25)
    if override_alch(builder, esm, "MedX", [
        (40, 240),    # DR +40 (was +25)
        (50, 108000), # Addiction 50% (was 30%)
    ]):
        print("  Med-X: +40 DR (was +25)")

    # Turbo: 6 seconds (was 3-4s)
    if override_alch(builder, esm, "Turbo", [
        (1, 6),  # TurboEffect 6s (was 3)
        (1, 8),  # TurboEffect 8s (was 4)
    ]):
        print("  Turbo: 6-8s slow-mo (was 3-4s)")

    # Steady: Duration 120s (was 60s)
    if override_alch(builder, esm, "Steady", [
        (50, 108000), # Addiction 50% (was 30%)
        (0, 120),     # SteadyEffect 120s (was 60s)
    ]):
        print("  Steady: 120s (was 60s)")

    # Slasher: Psycho + 40 DR for 120s (was +25 DR for 60s)
    if override_alch(builder, esm, "Slasher", [
        (0, 120),     # PsychoMagicEffect 120s (was 60s)
        (50, 108000), # Addiction 50%
        (40, 120),    # DR +40 for 120s (was +25/60s)
    ]):
        print("  Slasher: +40 DR for 120s (was +25/60s)")

    # Cateye: Duration 240s (was 120s)
    if override_alch(builder, esm, "Cateye", [
        (0, 240),  # CateyeEffect 240s (was 120s)
    ]):
        print("  Cateye: 240s night vision (was 120s)")

    # Rebound: Duration 120s (was 60s)
    if override_alch(builder, esm, "Rebound", [
        (50, 108000), # Addiction 50%
        (5, 120),     # ReboundEffect 120s (was 60s)
    ]):
        print("  Rebound: 120s (was 60s)")

    # ══════════════════════════════════════════
    # ALCOHOL — Bigger buffs, bigger penalties
    # ══════════════════════════════════════════
    print("\n-- Alcohol (amplified) --")

    # Whiskey: +3 STR, -3 INT (was +1 STR, -1 INT)
    if override_alch(builder, esm, "Whiskey", [
        (3, 240),   # STR +3 (was +1)
        (3, 240),   # INT -3 (was -1)
        (50, 0),    # Dehydration 50 (was 25)
    ]):
        print("  Whiskey: +3 STR, -3 INT (was +1/-1)")

    # Beer: +2 STR, -2 INT (was +1 STR, -1 INT)
    if override_alch(builder, esm, "Beer", [
        (2, 240),
        (2, 240),
        (35, 0),
    ]):
        print("  Beer: +2 STR, -2 INT (was +1/-1)")

    # Vodka: +3 STR, -3 INT
    if override_alch(builder, esm, "Vodka", [
        (3, 240),
        (3, 240),
        (50, 0),
    ]):
        print("  Vodka: +3 STR, -3 INT")

    # Wine: +2 STR, -2 INT
    if override_alch(builder, esm, "Wine", [
        (2, 240),
        (2, 240),
        (35, 0),
    ]):
        print("  Wine: +2 STR, -2 INT")

    # Scotch: +3 CHA, -3 INT
    if override_alch(builder, esm, "Scotch", [
        (3, 240),
        (3, 240),
        (50, 0),
    ]):
        print("  Scotch: +3 CHA, -3 INT")

    # Moonshine: +4 STR, -4 INT (strongest)
    if override_alch(builder, esm, "Moonshine", [
        (4, 240),
        (4, 240),
        (75, 0),
    ]):
        print("  Moonshine: +4 STR, -4 INT (strongest)")

    # ══════════════════════════════════════════
    # RADIATION MEDS — Slightly more effective
    # ══════════════════════════════════════════
    print("\n-- Radiation Meds --")

    # RadAway: Faster rad removal
    if override_alch(builder, esm, "RadAway", [
        (100, 8),  # Remove 100 rads over 8s (vanilla varies)
    ]):
        print("  RadAway: 100 rads over 8s")

    # Rad-X: +50 rad resist (was +25) for 240s
    if override_alch(builder, esm, "RadX", [
        (50, 240),
    ]):
        print("  Rad-X: +50 rad resist (was +25)")

    # ══════════════════════════════════════════
    # SAVE
    # ══════════════════════════════════════════
    outpath = FNV_DATA / "HardcoreTuning.esp"
    builder.save(str(outpath))

    import os
    sz = os.path.getsize(str(outpath))
    print("\nSaved: " + str(outpath) + " (" + str(sz) + " bytes)")
    print("\nAdd to plugins.txt: HardcoreTuning.esp")
    print("\nSUMMARY:")
    print("  Stimpaks: 50% less healing (food matters now)")
    print("  Super Stimpaks: Stronger heal but brutal 60s debuff")
    print("  All chems: ~2x potency, 50% addiction chance (was 30%)")
    print("  Turbo: 6-8s slow-mo (was 3-4s) — game changer")
    print("  Alcohol: 2-3x stat swings (real risk/reward)")
    print("  Rad meds: More effective (QoL)")


if __name__ == "__main__":
    main()
