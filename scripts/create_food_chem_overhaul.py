"""
Food & Custom Chem Overhaul

FOOD: 2x healing on all cooked food (compensates for stimpak nerf).
       Raw food unchanged (risk/reward: cook it or eat rads).

DLC FOOD: OWB blood sausages and HH datura boosted.
          LR Rushing Water improved.

CUSTOM CHEMS: 5 new Archivist-branded chems that synergize with perk paths.

Requires: FalloutNV.esm, HonestHearts.esm, OldWorldBlues.esm, LonesomeRoad.esm
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# MGEF FormIDs we need
RESTORE_HEALTH = 0x00015C  # RestoreHealth
RESTORE_HEALTH_STIMPAK = None  # will find
DAMAGE_RAD = None
RESTORE_STARVATION = None
RESTORE_DEHYDRATION = None
INC_STR = 0x01515C  # ChemIncSTBuffout uses this? No, these are MGEF records
# We'll clone effects from existing food items instead


def override_alch(builder, source, editor_id, efit_changes):
    """Override ALCH EFIT values by index."""
    for r in source.get_records("ALCH"):
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
                    rec.add_bytes("EFIT", struct.pack("<III", new_mag, area, new_dur))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
                efit_idx += 1
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))
        builder.add_raw_record("ALCH", rec.build())
        return True
    return False


def main():
    print("=== Food & Custom Chem Overhaul ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))

    builder = ESPBuilder.load_existing(str(FNV_DATA / "HardcoreTuning.esp"))

    # ══════════════════════════════════════════
    # COOKED FOOD — 2x healing
    # ══════════════════════════════════════════
    print("-- Cooked Food (2x healing) --")

    # (EditorID, effect_index_to_double, original_mag, original_dur)
    cooked_foods = [
        # Wasteland Omelet: 4/60s -> 8/60s (390->780 HP)
        ("WastelandOmeletNV", [(0, (8, 60))]),
        # Gecko Kabob: 1/40s -> 2/40s
        ("GeckoKebab", [(0, (2, 40))]),
        # Brahmin Wellington: 5/10s -> 10/10s
        ("NVBrahminWellington", [(0, (10, 10))]),
        # Bloatfly Slider: 3/15s -> 6/15s
        ("BloatflySlider", [(0, (6, 15))]),
        # Cook-Cook's Fiend Stew: 2/60s -> 4/60s
        ("CookCooksFiendStew", [(0, (4, 60))]),
        # Gecko Steak: 2/15s -> 4/15s
        ("NVGeckoSteak", [(0, (4, 15))]),
        # Grilled Mantis: 1/30s -> 2/30s
        ("NVGrilledMantis", [(0, (2, 30))]),
        # Bighorner Steak: 2/10s -> 4/10s
        ("BighornerSteak", [(0, (4, 10))]),
        # Mole Rat Stew: 2/30s -> 4/30s
        ("MoleRatStew", [(0, (4, 30))]),
        # Brahmin Steak: 2/15s -> 4/15s
        ("BrahminSteak", [(0, (4, 15))]),
        # Ruby's Casserole: 1/30s -> 2/30s
        ("PrimmSpicyCasserole", [(0, (2, 30))]),
        # Caravan Lunch: 3/15s -> 6/15s
        ("CaravanLunch", [(0, (6, 15))]),
    ]

    for eid, changes in cooked_foods:
        # Build efit_changes list matching effect order
        efit_list = [None] * 10  # Max effects
        for idx, vals in changes:
            efit_list[idx] = vals
        if override_alch(builder, esm, eid, efit_list):
            name = eid.replace("NV", "").replace("Kebab", " Kabob")
            print("  " + eid + ": 2x healing")

    # ══════════════════════════════════════════
    # DRINKS — Purified Water heals more
    # ══════════════════════════════════════════
    print("\n-- Drinks --")

    # Purified Water: 2/5s -> 5/5s (67->92 HP)
    if override_alch(builder, esm, "WaterPurified", [(5, 5)]):
        print("  Purified Water: 5/5s (was 2/5s)")

    # Nuka-Cola: 4/20s -> 8/20s
    if override_alch(builder, esm, "MS05IceNukaCola", [(8, 20)]):
        print("  Ice Cold Nuka-Cola: 8/20s (was 4/20s)")

    # Sunset Sarsaparilla: boost healing
    if override_alch(builder, esm, "NVSunsetSarsaparilla", [(4, 15)]):
        print("  Sunset Sarsaparilla: 4/15s")

    # ══════════════════════════════════════════
    # DLC FOOD
    # ══════════════════════════════════════════
    print("\n-- DLC Food --")

    # HH: Daturana - already strong, boost healing
    try:
        hh = PluginFile(str(FNV_DATA / "HonestHearts.esm"))
        # Daturana: RestoreHealth 15 -> 30
        # Effect order: ReduceAgility, RestoreHealth, RestoreSleep, IncUnarmed, RestoreLimbs
        if override_alch(builder, hh, "NVDLC02Daturana", [
            None,        # ReduceAgility (keep)
            (30, 0),     # RestoreHealth 30 (was 15)
            None,        # RestoreSleep (keep)
            None,        # IncUnarmed (keep)
            (250, 0),    # RestoreLimbs 250 (was 200)
        ]):
            print("  Daturana (HH): 30 HP (was 15)")

        # Blood Shield: 4/6s -> 8/6s
        if override_alch(builder, hh, "NVDLC02BloodShield", [
            (8, 6),     # RestoreHealth 8/6s (was 4/6s)
            None,       # PoisonResist (keep)
        ]):
            print("  Blood Shield (HH): 8/6s healing (was 4/6s)")

        # Large Wasteland Tequila: already strong, boost STR
        if override_alch(builder, hh, "NVDLC02WastelandTequilaLarge", [
            (4, 240),   # STR +4 (was +3)
            (4, 240),   # INT -4 (was -3)
            None, None, None, None,
        ]):
            print("  Large Wasteland Tequila (HH): +4 STR (was +3)")
    except Exception as e:
        print("  HH error: " + str(e))

    # OWB: Blood sausages - already great, just tweak
    try:
        owb = PluginFile(str(FNV_DATA / "OldWorldBlues.esm"))
        # Thin Red Paste: 2/30s -> 4/30s
        if override_alch(builder, owb, "NVDLC03ThinRedPaste", [
            (4, 30),    # RestoreHealth 4/30s (was 2/30s)
            (10, 240),  # IncreaseHealth 10/240s (was 5/240s)
        ]):
            print("  Thin Red Paste (OWB): 2x healing + HP boost")

        # Salient Green: 2/7s -> 5/7s
        if override_alch(builder, owb, "NVDLC03SalientGreen", [
            (5, 7),
            None,
        ]):
            print("  Salient Green (OWB): 5/7s (was 2/7s)")

        # Nightstalker Squeezins: +10 Sneak (was +5)
        if override_alch(builder, owb, "NVDLC03NightstalkerSqueezins", [
            (10, 240),  # Sneak +10 (was +5)
            (2, 240),   # PER +2 (was +1)
            None,       # Rad damage
            (4, 5),     # RestoreHealth 4/5s (was 2/5s)
            (10, 240),  # PoisonResist +10 (was +5)
        ]):
            print("  Nightstalker Squeezins (OWB): +10 Sneak, +2 PER")

        # Implant GRX: 4-5s (was 2-3s) to match our Turbo buff
        if override_alch(builder, owb, "NVDLC03ImplantGRX", [
            (1, 4),
            (1, 5),
        ]):
            print("  Implant GRX (OWB): 4-5s (was 2-3s)")
    except Exception as e:
        print("  OWB error: " + str(e))

    # LR: Rushing Water
    try:
        lr = PluginFile(str(FNV_DATA / "LonesomeRoad.esm"))
        # Rushing Water: 2/5s -> 5/5s healing
        if override_alch(builder, lr, "NVDLC04RushingWater", [
            (5, 5),     # RestoreHealth 5/5s (was 2/5s)
            None, None, None,
        ]):
            print("  Rushing Water (LR): 5/5s healing (was 2/5s)")
    except Exception as e:
        print("  LR error: " + str(e))

    # ══════════════════════════════════════════
    # CUSTOM CHEMS — 5 Archivist-branded
    # Clone from existing chems, change name + effects
    # ══════════════════════════════════════════
    print("\n-- Custom Chems (Archivist Pharmaceuticals) --")

    # Clone Jet as template for custom chems
    jet_template = None
    psycho_template = None
    buffout_template = None
    turbo_template = None
    medx_template = None
    for r in esm.get_records("ALCH"):
        srs = r.parse_subrecords()
        eid = ""
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode("utf-8", errors="replace")
        if eid == "Jet": jet_template = (r.id, srs)
        if eid == "Psycho": psycho_template = (r.id, srs)
        if eid == "Buffout": buffout_template = (r.id, srs)
        if eid == "NVTurbo": turbo_template = (r.id, srs)
        if eid == "Morphine": medx_template = (r.id, srs)

    custom_chems = [
        # 1. Clarity — AP + Perception boost (Gunslinger/Shadow synergy)
        ("MnChemClarity", "Clarity", "Archivist stimulant. Sharpens perception and reflexes. Side effects include existential dread.",
         jet_template, [
            (25, 180),    # AP +25 for 180s
            (40, 108000), # Addiction 40%
         ]),

        # 2. Overdrive — Damage + Crit (Rifleman/Scientist synergy)
        ("MnChemOverdrive", "Overdrive", "Archivist combat enhancer. Amplifies neural targeting pathways. Warning: may cause overconfidence.",
         psycho_template, [
            (0, 300),     # PsychoMagicEffect for 300s
            (40, 108000), # Addiction 40%
         ]),

        # 3. Fortify — STR + END + DT (Brawler/Survivor synergy)
        ("MnChemFortify", "Fortify", "Archivist endurance compound. Reinforces skeletal-muscular system. Withdrawal is unpleasant.",
         buffout_template, [
            (5, 180),     # STR +5
            (5, 180),     # END +5
            (120, 180),   # HP +120
            (45, 108000), # Addiction 45%
         ]),

        # 4. Reflex — Turbo but longer (Shadow/Gunslinger synergy)
        ("MnChemReflex", "Reflex", "Archivist temporal inhibitor. Slows perceived time. The universe disagrees with this.",
         turbo_template, [
            (1, 8),       # TurboEffect 8s
            (1, 10),      # TurboEffect 10s
         ]),

        # 5. Aegis — DR + rad resist (Demolisher/Survivor synergy)
        ("MnChemAegis", "Aegis", "Archivist protective compound. Hardens skin against damage and radiation. Tastes terrible.",
         medx_template, [
            (50, 180),    # DR +50
            (45, 108000), # Addiction 45%
         ]),
    ]

    for new_eid, new_name, desc, (tmpl_id, tmpl_srs), efit_changes in custom_chems:
        fid = builder.allocate_form_id()
        rec = RecordBuilder("ALCH", fid)

        efit_idx = 0
        for sr in tmpl_srs:
            if sr.type == "EDID":
                rec.add_string("EDID", new_eid)
            elif sr.type == "FULL":
                rec.add_string("FULL", new_name)
            elif sr.type == "DESC":
                rec.add_string("DESC", desc)
            elif sr.type == "EFIT" and len(sr.data) >= 12:
                if efit_idx < len(efit_changes) and efit_changes[efit_idx] is not None:
                    new_mag, new_dur = efit_changes[efit_idx]
                    area = struct.unpack("<I", sr.data[4:8])[0]
                    rec.add_bytes("EFIT", struct.pack("<III", new_mag, area, new_dur))
                else:
                    rec.add(SR.from_bytes(sr.type, sr.data))
                efit_idx += 1
            elif sr.type == "DATA" and len(sr.data) >= 4:
                # Set value (caps)
                old_data = bytearray(sr.data)
                struct.pack_into("<i", old_data, 0, 75)  # 75 caps each
                rec.add_bytes("DATA", bytes(old_data))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_record("ALCH", rec)
        print("  + " + new_name.ljust(16) + " (" + new_eid + ")")

    # ══════════════════════════════════════════
    # SAVE
    # ══════════════════════════════════════════
    builder.save(str(FNV_DATA / "HardcoreTuning.esp"))
    import os
    sz = os.path.getsize(str(FNV_DATA / "HardcoreTuning.esp"))
    print("\nSaved HardcoreTuning.esp (" + str(sz) + " bytes)")


if __name__ == "__main__":
    main()
