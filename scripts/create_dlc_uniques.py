"""
DLC-Themed Endgame Uniques — 22 weapons inspired by all 4 DLCs + GRA
Uses base game weapon models to avoid DLC master dependencies.
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")

# (template_eid, new_eid, new_name, desc, dmg, clip, health, value, spread_mult, rate_mult, critdmg, critmult)
DLC_UNIQUES = [
    # DEAD MONEY
    ("WeapNVPoliceBaton", "WeapMnSierraMadre", "Sierra Madre Swagger Stick",
     "A police baton from the Sierra Madre. The ghost people could not break it.",
     35, 0, 800, 3500, 1.0, 1.0, 35, 2.5),
    ("WeapNVHuntingRevolver", "WeapMnDeansSecret", "Dean's Last Secret",
     "A hunting revolver with a monogrammed D.D. grip. Dean's insurance policy.",
     85, 5, 1400, 8000, 0.5, 1.0, 85, 2.5),
    ("WeapNVGaussRifle", "WeapMnElijahsLegacy", "Elijah's Legacy",
     "A gauss rifle rebuilt from Elijah's schematics. Insane engineering, flawless results.",
     165, 6, 2000, 14000, 0.2, 1.0, 110, 3.0),
    ("WeapShotgunSawedOff", "WeapMnChristinesKiss", "Christine's Kiss",
     "A sawed-off with a lipstick mark on the stock. For when they got close.",
     130, 2, 1000, 7000, 0.9, 1.0, 20, 2.0),

    # HONEST HEARTS
    ("WeapNV357Revolver", "WeapMnBurningBush", "Burning Bush",
     "A revolver blessed by the Burned Man. The fire that consumed Joshua forged this.",
     55, 6, 1200, 6000, 0.5, 1.0, 55, 3.0),
    ("WeapNVServiceRifle", "WeapMnSurvivalistOath", "Survivalist's Oath",
     "A service rifle from Zion. Randall Clark's last gift to the Sorrows.",
     60, 12, 1500, 7500, 0.4, 1.0, 60, 2.5),
    ("WeapNVFireaxe", "WeapMnWhiteLegs", "White Legs' Reckoning",
     "A tribal war axe from a White Legs chieftain. Stained with history.",
     85, 0, 1200, 5000, 1.0, 1.0, 42, 2.5),
    ("WeapPowerFist", "WeapMnZionsFist", "Zion's Fist",
     "A power fist carved with canyon petroglyphs. The strength of Zion.",
     72, 0, 1100, 6000, 1.0, 1.0, 72, 2.0),

    # OLD WORLD BLUES
    ("WeapLaserRifle", "WeapMnBigMTBeam", "Big MT Experimental Beam",
     "A laser rifle from Think Tank Lab 7. Dr. Klein insists it is perfectly safe.",
     45, 30, 1200, 8000, 0.4, 1.15, 45, 2.5),
    ("WeapNVPlasmaCaster", "WeapMnMobiusGambit", "Mobius' Gambit",
     "A plasma caster modified during one of Mobius' more lucid moments.",
     100, 14, 1600, 11000, 0.5, 1.0, 100, 2.5),
    ("WeapTeslaCannon", "WeapMnTeslaReborn", "Tesla Reborn",
     "A tesla cannon rebuilt with Big MT superconductors. The arc chains through everything.",
     110, 24, 1800, 13000, 0.6, 1.0, 60, 2.0),
    ("WeapNVZapGlove", "WeapMnDrKleinsHandshake", "Dr. Klein's Handshake",
     "A zap glove with Think Tank modifications. Klein's way of saying hello and goodbye.",
     55, 0, 900, 5500, 1.0, 1.0, 55, 3.0),
    ("WeapSniperRifle", "WeapMnChristinesSilence", "Christine's Silence",
     "A sniper rifle with OWB stealth dampeners. Christine adapted. She always does.",
     80, 6, 1400, 9000, 0.2, 1.0, 80, 3.0),

    # LONESOME ROAD
    ("WeapNVLightMachineGun", "WeapMnDivideStorm", "Divide Storm",
     "A light machine gun scarred by nuclear wind. The Divide tried to destroy it.",
     35, 120, 1600, 8000, 0.6, 1.0, 35, 2.0),
    ("WeapNVBrushGun", "WeapMnUlyssesWord", "Ulysses' Word",
     "A brush gun with Old World flags carved into the stock. The last message.",
     105, 8, 1600, 10000, 0.3, 1.0, 105, 2.5),
    ("WeapMissileLauncher", "WeapMnRedGlareMk2", "Red Glare Mk. II",
     "A missile launcher rebuilt from Divide salvage. Not a signal. A declaration.",
     200, 3, 2000, 12000, 0.5, 1.0, 0, 1.0),
    ("WeapNVMacheteGladius", "WeapMnBladeWestReforged", "Blade of the West (Reforged)",
     "Lanius' blade reforged with Divide metals. Heavier. Sharper. Hungrier.",
     75, 0, 1500, 8000, 1.0, 1.0, 75, 2.5),
    ("WeapDeathclawGauntlet", "WeapMnFistOfRawrMk2", "Fist of Rawr Mk. II",
     "A deathclaw gauntlet reinforced with Divide alloys. Rawr would be proud.",
     85, 0, 1200, 7000, 1.0, 1.0, 85, 2.0),

    # GRA SPECIAL
    ("WeapNVBallisticFist", "WeapMnTwoStepFinale", "Two-Step Finale",
     "A ballistic fist with GRA modifications. Step one: punch. No step two.",
     130, 0, 1600, 10000, 1.0, 1.0, 130, 2.0),
    ("WeapShishkebab", "WeapMnGehennaRelit", "Gehenna Relit",
     "A shishkebab with GRA fuel injectors. Burns hotter and longer than the original.",
     65, 0, 1200, 7000, 1.0, 1.0, 35, 3.0),
    ("WeapNVAntiMaterielRifle", "WeapMnPatienceRewarded", "Patience Rewarded",
     "An anti-materiel rifle with GRA barrel. Paciencia taught patience. This teaches finality.",
     145, 10, 2000, 14000, 0.2, 1.0, 120, 3.0),
    ("WeapNVTriBeamLaserRifle", "WeapMnSprtelMk2", "Sprtel-Wood Mk. II",
     "A tri-beam laser with GRA capacitors. Three beams, three times the problem.",
     88, 28, 1500, 10000, 0.5, 1.0, 30, 2.5),
]


def main():
    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))
    templates = {}
    for r in esm.get_records("WEAP"):
        srs = r.parse_subrecords()
        for sr in srs:
            if sr.type == "EDID":
                templates[sr.data.rstrip(b"\x00").decode()] = srs
                break

    builder = ESPBuilder.load_existing(str(FNV_DATA / "MnehmosMojave.esp"))

    created = 0
    for (tmpl, eid, name, desc, dmg, clip, hp, val,
         sp_mult, rate_mult, critdmg, critmult) in DLC_UNIQUES:
        if tmpl not in templates:
            print("SKIP: " + tmpl)
            continue
        template = templates[tmpl]
        fid = builder.allocate_form_id()
        rec = RecordBuilder("WEAP", fid)
        for sr in template:
            if sr.type == "EDID":
                rec.add_string("EDID", eid)
            elif sr.type == "FULL":
                rec.add_string("FULL", name)
            elif sr.type == "DESC":
                rec.add_string("DESC", desc)
            elif sr.type == "DATA" and len(sr.data) == 15:
                wt = struct.unpack("<f", sr.data[8:12])[0]
                rec.add_bytes("DATA", struct.pack("<iif", val, hp, wt) + struct.pack("<hB", dmg, clip))
            elif sr.type == "DNAM" and len(sr.data) >= 48:
                dnam = bytearray(sr.data)
                old_sp = struct.unpack("<f", dnam[4:8])[0]
                struct.pack_into("<f", dnam, 4, old_sp * sp_mult)
                old_rate = struct.unpack("<f", dnam[44:48])[0]
                struct.pack_into("<f", dnam, 44, old_rate * rate_mult)
                rec.add_bytes("DNAM", bytes(dnam))
            elif sr.type == "CRDT" and len(sr.data) >= 12:
                crdt = bytearray(sr.data)
                struct.pack_into("<H", crdt, 0, critdmg)
                struct.pack_into("<f", crdt, 4, critmult)
                rec.add_bytes("CRDT", bytes(crdt))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))
        builder.add_record("WEAP", rec)
        print("  + " + name.ljust(32) + " dmg=" + str(dmg).rjust(4) + " clip=" + str(clip).rjust(3))
        created += 1

    builder.save(str(FNV_DATA / "MnehmosMojave.esp"))
    import os
    print("\nCreated: " + str(created) + " DLC uniques")
    print("Saved: " + str(os.path.getsize(str(FNV_DATA / "MnehmosMojave.esp"))) + " bytes")


if __name__ == "__main__":
    main()
