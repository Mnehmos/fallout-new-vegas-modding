"""
Endgame Unique Weapons — One per archetype

Each unique is based on a mid-tier weapon, scaled to endgame (75-100 skill).
Damage ~1.5-2x the base, better spread, higher crit, more durable.
Named with Mnehmos lore flavor.
"""

import sys
import struct
from pathlib import Path

sys.path.insert(0, "F:/Github/mnehmos.fnvedit.mcp/src")

from core.binary_parser import PluginFile
from core.esp_binary_writer import ESPBuilder, RecordBuilder, SubrecordBuilder as SR

FNV_DATA = Path("H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data")


# (template_edid, new_edid, new_name, description, dmg, clip, health, value, spread_mult, firerate_mult, critdmg, critmult)
UNIQUES = [
    # ── PISTOLS ──
    ("WeapNV9mmPistol", "WeapMnMemento", "Memento",
     "A well-worn 9mm with notches on the grip. Each one is a memory you can't forget.",
     32, 16, 800, 3500, 0.7, 1.0, 32, 2.0),

    ("Weap10mmPistol", "WeapMnReprieve", "Reprieve",
     "A 10mm that whispers mercy. The safety's been filed off.",
     42, 16, 900, 4200, 0.7, 1.0, 42, 2.0),

    ("WeapNV357Revolver", "WeapMnVerdict", "The Verdict",
     "A .357 with a courthouse engraving. Justice comes in six rounds.",
     50, 6, 1000, 5000, 0.6, 1.0, 50, 2.5),

    ("WeapNV44Revolver", "WeapMnRedaction", "Redaction",
     "A .44 Magnum with blacked-out serial numbers. Some things are better left unsaid.",
     65, 6, 1200, 6500, 0.6, 1.0, 65, 2.0),

    ("WeapNVHuntingRevolver", "WeapMnFinalAppeal", "Final Appeal",
     "A hunting revolver engraved with legal citations. The last argument anyone hears.",
     90, 5, 1500, 9000, 0.5, 1.0, 90, 2.5),

    ("WeapNV127mmPistol", "WeapMnRedacted", "Redacted",
     "A 12.7mm pistol with classified markings. Whatever it was built for, it works.",
     70, 9, 1100, 7000, 0.6, 1.0, 70, 2.0),

    ("WeapLaserPistol", "WeapMnEpilogue", "Epilogue",
     "A laser pistol tuned to a frequency that ends stories.",
     28, 36, 800, 4000, 0.6, 1.0, 28, 3.0),

    ("WeapPlasmaPistol", "WeapMnPostscript", "Postscript",
     "A plasma pistol. P.S. — You should have run.",
     60, 40, 900, 5500, 0.7, 1.0, 60, 2.0),

    ("WeapNVPlasmaDefender", "WeapMnAmendment", "The Amendment",
     "A plasma defender with constitutional engravings. The right to bear plasma.",
     65, 36, 1000, 6000, 0.6, 1.0, 65, 2.0),

    # ── RIFLES ──
    ("WeapNVVarmintRifle", "WeapMnPrologue", "Prologue",
     "A varmint rifle that started it all. Upgraded beyond recognition.",
     38, 8, 800, 3000, 0.5, 1.0, 38, 2.0),

    ("WeapNVCowboyRepeater", "WeapMnChronicle", "Chronicle",
     "A cowboy repeater that's seen every chapter of the Mojave's story.",
     55, 10, 900, 4500, 0.5, 1.0, 55, 2.5),

    ("WeapNVServiceRifle", "WeapMnStandingOrder", "Standing Order",
     "A service rifle that never got the order to stand down.",
     36, 24, 1000, 4000, 0.6, 1.0, 36, 2.0),

    ("WeapHuntingRifle", "WeapMnDeepRead", "Deep Read",
     "A hunting rifle with a scope that reads between the lines.",
     80, 6, 1200, 7000, 0.4, 1.0, 80, 2.5),

    ("WeapNVBrushGun", "WeapMnLastChapter", "Last Chapter",
     "A brush gun with 'THE END' carved into the stock.",
     110, 8, 1500, 10000, 0.4, 1.0, 110, 2.5),

    ("WeapNVMarksmanCarbine", "WeapMnAnnotation", "Annotation",
     "A marksman carbine with margin notes on the receiver. Precise commentary.",
     42, 24, 1000, 5500, 0.5, 1.0, 42, 2.0),

    ("WeapSniperRifle", "WeapMnOmniscient", "Omniscient",
     "A sniper rifle. It knows where you are before you do.",
     72, 6, 1300, 8500, 0.3, 1.0, 72, 3.0),

    ("WeapNVAssaultCarbine", "WeapMnRunOnSentence", "Run-On Sentence",
     "An assault carbine that doesn't know when to stop.",
     24, 30, 1100, 5000, 0.6, 1.15, 24, 2.0),

    # ── SHOTGUNS ──
    ("WeapNVCaravanShotgun", "WeapMnShortStory", "Short Story",
     "A caravan shotgun. Brief, brutal, to the point.",
     80, 2, 800, 3500, 0.8, 1.0, 12, 2.0),

    ("WeapNVHuntingShotgun", "WeapMnExcerpt", "Excerpt",
     "A hunting shotgun. This is just a sample of what's coming.",
     100, 6, 1200, 6000, 0.7, 1.0, 15, 2.0),

    ("WeapNVRiotShotgun", "WeapMnManifesto", "Manifesto",
     "A riot shotgun with pamphlets taped to the stock. Spread the word.",
     90, 12, 1400, 8000, 0.8, 1.0, 14, 2.0),

    # ── ENERGY RIFLES ──
    ("WeapLaserRifle", "WeapMnBibliography", "Bibliography",
     "A laser rifle. Every shot is a citation.",
     35, 28, 900, 5000, 0.5, 1.0, 35, 2.5),

    ("WeapPlasmaRifle", "WeapMnDissertation", "Dissertation",
     "A plasma rifle. A thorough examination of your opponents.",
     72, 28, 1100, 7000, 0.6, 1.0, 72, 2.0),

    ("WeapNVGaussRifle", "WeapMnAxiom", "Axiom",
     "A gauss rifle. Self-evident truth at 2km.",
     175, 6, 1800, 12000, 0.2, 1.0, 120, 3.0),

    # ── AUTOMATICS ──
    ("WeapNV9mmSubmachineGun", "WeapMnFreewriting", "Freewriting",
     "A 9mm SMG. Stream of consciousness in lead.",
     24, 36, 800, 3500, 0.7, 1.0, 24, 2.0),

    ("Weap10mmSubmachineGun", "WeapMnEditorial", "Editorial",
     "A 10mm SMG. Opinions delivered at 600 RPM.",
     32, 36, 900, 4500, 0.6, 1.0, 32, 2.0),

    ("WeapNV127mmSubmachineGun", "WeapMnRedline", "Redline",
     "A 12.7mm SMG. Aggressive editing.",
     55, 27, 1200, 7000, 0.6, 1.0, 55, 2.0),

    ("WeapNVLightMachineGun", "WeapMnVerbatim", "Verbatim",
     "A light machine gun. Quoting you word for word for word for word.",
     36, 120, 1400, 6500, 0.7, 1.0, 36, 2.0),

    # ── BIG GUNS ──
    ("WeapMinigun", "WeapMnErrata", "Errata",
     "A minigun. Corrections issued at 6000 RPM.",
     20, 240, 1800, 9000, 0.8, 1.0, 20, 1.5),

    ("WeapGatlingLaser", "WeapMnAbstract", "Abstract",
     "A gatling laser. A brief summary of total destruction.",
     18, 240, 1800, 10000, 0.7, 1.0, 18, 2.0),

    ("WeapFlamer", "WeapMnCensorship", "Censorship",
     "A flamer. Some ideas need to burn.",
     28, 80, 1000, 5500, 0.8, 1.0, 5, 2.0),

    ("WeapNVPlasmaCaster", "WeapMnThesis", "Thesis",
     "A plasma caster. Defend this.",
     95, 12, 1500, 11000, 0.5, 1.0, 95, 2.5),

    # ── MELEE ──
    ("WeapNVMachete", "WeapMnRedPen", "Red Pen",
     "A machete painted red. Marks up everything it touches.",
     28, 0, 800, 2000, 1.0, 1.0, 28, 2.0),

    ("WeapNVFireaxe", "WeapMnStrikethrough", "Strikethrough",
     "A fire axe. Crosses things out permanently.",
     80, 0, 1200, 5000, 1.0, 1.0, 40, 2.5),

    ("WeapSuperSledge", "WeapMnRevision", "Revision",
     "A super sledge. Rewrites history on impact.",
     110, 0, 1500, 8000, 1.0, 1.0, 55, 2.5),

    ("WeapRipper", "WeapMnShredder", "Shredder",
     "A ripper. For documents and people.",
     75, 0, 1000, 5500, 1.0, 1.0, 15, 3.0),

    ("WeapNVChainsaw", "WeapMnDeclassified", "Declassified",
     "A chainsaw. Everything it touches becomes public record.",
     120, 0, 1400, 7000, 1.0, 1.0, 15, 2.0),

    # ── UNARMED ──
    ("WeapPowerFist", "WeapMnFootnote2", "Footnote",
     "A power fist. Small text, big impact.",
     65, 0, 1000, 5000, 1.0, 1.0, 65, 2.0),

    ("WeapNVBallisticFist", "WeapMnExclamation", "Exclamation Point",
     "A ballistic fist. Adds emphasis.",
     120, 0, 1500, 9000, 1.0, 1.0, 120, 2.0),

    # ── EXPLOSIVES ──
    ("WeapNVGrenadeLauncher", "WeapMnParenthetical", "Parenthetical",
     "A grenade launcher. An aside that derails the conversation.",
     4, 6, 900, 5000, 0.7, 1.0, 2, 2.0),

    ("WeapMissileLauncher", "WeapMnAddendum", "Addendum",
     "A missile launcher. A late addition to the discussion.",
     175, 1, 1500, 10000, 0.5, 1.0, 0, 1.0),
]


def main():
    print("=== Endgame Unique Weapons ===\n")

    esm = PluginFile(str(FNV_DATA / "FalloutNV.esm"))

    # Build template lookup
    templates = {}
    for r in esm.get_records("WEAP"):
        srs = r.parse_subrecords()
        for sr in srs:
            if sr.type == "EDID":
                eid = sr.data.rstrip(b"\x00").decode()
                templates[eid] = srs
                break

    builder = ESPBuilder.load_existing(str(FNV_DATA / "MnehmosMojave.esp"))

    created = 0
    for (tmpl_eid, new_eid, new_name, desc, dmg, clip, health, value,
         spread_mult, firerate_mult, critdmg, critmult) in UNIQUES:

        if tmpl_eid not in templates:
            print("  SKIP: " + tmpl_eid + " not found")
            continue

        template = templates[tmpl_eid]
        fid = builder.allocate_form_id()
        rec = RecordBuilder("WEAP", fid)

        for sr in template:
            if sr.type == "EDID":
                rec.add_string("EDID", new_eid)
            elif sr.type == "FULL":
                rec.add_string("FULL", new_name)
            elif sr.type == "DESC":
                rec.add_string("DESC", desc)
            elif sr.type == "DATA" and len(sr.data) == 15:
                new_data = struct.pack("<iif", value, health, struct.unpack("<f", sr.data[8:12])[0])
                new_data += struct.pack("<hB", dmg, clip)
                rec.add_bytes("DATA", new_data)
            elif sr.type == "DNAM" and len(sr.data) >= 48:
                dnam = bytearray(sr.data)
                # Spread
                old_spread = struct.unpack("<f", dnam[4:8])[0]
                struct.pack_into("<f", dnam, 4, old_spread * spread_mult)
                # Fire rate
                old_rate = struct.unpack("<f", dnam[44:48])[0]
                struct.pack_into("<f", dnam, 44, old_rate * firerate_mult)
                rec.add_bytes("DNAM", bytes(dnam))
            elif sr.type == "CRDT" and len(sr.data) >= 12:
                crdt = bytearray(sr.data)
                struct.pack_into("<H", crdt, 0, critdmg)
                struct.pack_into("<f", crdt, 4, critmult)
                rec.add_bytes("CRDT", bytes(crdt))
            else:
                rec.add(SR.from_bytes(sr.type, sr.data))

        builder.add_record("WEAP", rec)
        print("  + " + new_name.ljust(24) + " (" + new_eid + ") dmg=" + str(dmg) + " clip=" + str(clip))
        created += 1

    builder.save(str(FNV_DATA / "MnehmosMojave.esp"))

    import os
    sz = os.path.getsize(str(FNV_DATA / "MnehmosMojave.esp"))
    print("\nCreated: " + str(created) + " endgame uniques")
    print("Saved MnehmosMojave.esp (" + str(sz) + " bytes)")


if __name__ == "__main__":
    main()
