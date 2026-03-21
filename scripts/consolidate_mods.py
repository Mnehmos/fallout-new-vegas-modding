"""Consolidate ArchivistsCache into MnehmosMojave.esp"""
import sys, struct
sys.path.insert(0, 'F:/Github/mnehmos.fnvedit.mcp/src')
from core.esp_binary_writer import ESPBuilder, SR, RecordBuilder
from core.binary_parser import PluginFile

print("Loading MnehmosMojave.esp...")
esp = ESPBuilder.load_existing('H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data/MnehmosMojave.esp')
print(f"  Loaded: {esp._record_count} records, {len(esp.masters)} masters")
print(f"  Next FormID: {esp._next_form_id:#06x}")

base = PluginFile('H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data/FalloutNV.esm')

# Helper: find weapon by EditorID
def find_weap(edid):
    for r in base.get_records('WEAP'):
        for sr in r.parse_subrecords():
            if sr.type == 'EDID' and sr.data.rstrip(b'\x00').decode() == edid:
                return r
    return None

def clone_weapon_manual(source, new_edid, new_name, data_changes, dnam_changes, crdt_changes, proj_count=None):
    fid = esp.allocate_form_id()
    rec = RecordBuilder('WEAP', fid)
    for sr in source.parse_subrecords():
        if sr.type == 'EDID':
            rec.add_string('EDID', new_edid)
        elif sr.type == 'FULL':
            rec.add_string('FULL', new_name)
        elif sr.type == 'DATA' and len(sr.data) >= 14:
            d = bytearray(sr.data)
            if 'Value' in data_changes: struct.pack_into('<I', d, 0, data_changes['Value'])
            if 'Health' in data_changes: struct.pack_into('<I', d, 4, data_changes['Health'])
            if 'Weight' in data_changes: struct.pack_into('<f', d, 8, data_changes['Weight'])
            if 'Base Damage' in data_changes: struct.pack_into('<H', d, 12, data_changes['Base Damage'])
            if 'Clip Size' in data_changes and len(d) > 14: d[14] = data_changes['Clip Size']
            rec.add_bytes('DATA', bytes(d))
        elif sr.type == 'DNAM' and len(sr.data) >= 72:
            d = bytearray(sr.data)
            if 'Min Spread' in dnam_changes: struct.pack_into('<f', d, 16, dnam_changes['Min Spread'])
            if 'Fire Rate' in dnam_changes: struct.pack_into('<f', d, 64, dnam_changes['Fire Rate'])
            if 'AP' in dnam_changes: struct.pack_into('<f', d, 68, dnam_changes['AP'])
            if proj_count and len(d) > 42: d[42] = proj_count
            if 'Skill Req' in dnam_changes and len(d) >= 4:
                struct.pack_into('<I', d, len(d)-4, dnam_changes['Skill Req'])
            rec.add_bytes('DNAM', bytes(d))
        elif sr.type == 'CRDT' and len(sr.data) >= 8:
            d = bytearray(sr.data)
            if 'Damage' in crdt_changes: struct.pack_into('<H', d, 0, crdt_changes['Damage'])
            if 'Mult' in crdt_changes: struct.pack_into('<f', d, 4, crdt_changes['Mult'])
            rec.add_bytes('CRDT', bytes(d))
        else:
            rec.add_bytes(sr.type, sr.data)
    esp.add_record('WEAP', rec)
    return fid

print("\nAdding Archivist Cache content...")

# QUEST
qrec = RecordBuilder('QUST', esp.allocate_form_id())
qrec.add_string('EDID', 'MnehmosQArchivistsCache')
qrec.add_string('FULL', 'The Archivists Cache')
qrec.add_bytes('DATA', struct.pack('<BBxx', 0x01, 50) + struct.pack('<f', 0.0))
esp.add_record('QUST', qrec)
print("  + Quest")

# NOTE
ns = None
for r in base.get_records('NOTE'):
    for sr in r.parse_subrecords():
        if sr.type == 'EDID' and b'GSSunnyNote' in sr.data:
            ns = r; break
    if ns: break
note_fid = esp.clone_record(ns, 'MnehmosArchivistNote', {
    'FULL': 'The Archivists Final Entry',
    'TNAM': 'Day 1. The sirens stopped. I made it to the cellar.\nDay 14. Water tests clean.\nDay 47. Found footprints. They never came back.\nDay 89. I am the last one. Everything is in the trunk.\nMnemosyne remembers. -- The Archivist'
})
print(f"  + Note: {note_fid:#010x}")

# EUREKA — Quad laser
eureka_fid = clone_weapon_manual(
    find_weap('WeapNVTriBeamLaserRifle'), 'WeapEureka', 'Eureka',
    {'Base Damage': 22, 'Clip Size': 32, 'Value': 8000, 'Health': 250, 'Weight': 7.0},
    {'Min Spread': 0.33, 'Fire Rate': 2.5, 'AP': 22.0, 'Skill Req': 75},
    {'Damage': 42, 'Mult': 2.0},
    proj_count=4
)
print(f"  + Eureka (quad laser): {eureka_fid:#010x}")

# CATHARSIS — Quad multiplas
catharsis_fid = clone_weapon_manual(
    find_weap('WeapNVMultiPlasRifle'), 'WeapCatharsis', 'Catharsis',
    {'Base Damage': 42, 'Clip Size': 40, 'Value': 12000, 'Health': 300, 'Weight': 6.0},
    {'Min Spread': 0.80, 'Fire Rate': 2.0, 'AP': 28.0, 'Skill Req': 75},
    {'Damage': 56, 'Mult': 2.0},
    proj_count=4
)
print(f"  + Catharsis (quad plasma): {catharsis_fid:#010x}")

# DEJA VU BEAM — Crit recharger pistol
dvb_fid = esp.clone_record(find_weap('WeapNVRechargerPistol'), 'WeapDejaVuBeam', {
    'FULL': 'Deja Vu Beam',
    'DATA': {'Base Damage': 28, 'Clip Size': 30, 'Value': 8000, 'Health': 500, 'Weight': 2.5},
    'DNAM': {'Min Spread': 0.05, 'Fire Rate': 8.0, 'Override - Action Points': 8.0},
    'CRDT': {'Critical Damage': 42, 'Crit % Mult': 5.0}
})
print(f"  + Deja Vu Beam (crit pistol): {dvb_fid:#010x}")

# TOTAL RECALL — Crit recharger rifle
tr_fid = esp.clone_record(find_weap('WeapNVRechargerRifle'), 'WeapTotalRecall', {
    'FULL': 'Total Recall',
    'DATA': {'Base Damage': 32, 'Clip Size': 20, 'Value': 10000, 'Health': 500, 'Weight': 6.0},
    'DNAM': {'Min Spread': 0.01, 'Fire Rate': 6.0, 'Override - Action Points': 12.0},
    'CRDT': {'Critical Damage': 48, 'Crit % Mult': 5.0}
})
print(f"  + Total Recall (crit rifle): {tr_fid:#010x}")

# CONTAINER — The Archivist's Cache with FULL inventory
cs = None
for r in base.get_records('CONT'):
    for sr in r.parse_subrecords():
        if sr.type == 'EDID' and b'VLootWeapTrunkGen01' in sr.data:
            cs = r; break
    if cs: break

cont_fid = esp.allocate_form_id()
cont_rec = RecordBuilder('CONT', cont_fid)
for sr in cs.parse_subrecords():
    if sr.type == 'EDID': cont_rec.add_string('EDID', 'MnehmosArchivistTrunk')
    elif sr.type == 'FULL': cont_rec.add_string('FULL', 'The Archivists Cache')
    else: cont_rec.add_bytes(sr.type, sr.data)

# FormIDs use 00 prefix for FalloutNV.esm master (index 0 in MnehmosMojave)
# Self-references use the plugin's own index which will be resolved at load
items = [
    (note_fid, 1),
    (eureka_fid, 1),
    (catharsis_fid, 1),
    (dvb_fid, 1),
    (tr_fid, 1),
    # Original Mnehmos Collection items (already in this ESP)
    # These use local FormIDs that we need to reference correctly
    # The existing weapons start at 0x01000800 in the loaded ESP
    # But when writing, they need the plugin's own index
    (0x0100080b, 1),   # Bad Memories
    (0x0100080c, 1),   # First Impression
    (0x01000819, 1),   # Deja Vu knife
    (0x0100081c, 1),   # Archivist Duster
    (0x0100081b, 1),   # Mnehmos Hat
    (0x0100081d, 1),   # Recollection Lenses
    (0x00015169, 500),  # Caps (FalloutNV.esm)
    (0x0008ED78, 60),   # 20ga (FalloutNV.esm)
    (0x00121158, 60),   # .357 (FalloutNV.esm)
    (0x00078CC2, 200),  # Microfusion cells (FalloutNV.esm)
    (0x00078740, 200),  # Energy cells (FalloutNV.esm)
    (0x00078744, 15),   # Stimpaks (FalloutNV.esm)
    (0x00015197, 10),   # Purified Water (FalloutNV.esm)
]
for fid, cnt in items:
    cont_rec.add_bytes('CNTO', struct.pack('<Ii', fid, cnt))
esp.add_record('CONT', cont_rec)
print(f"  + Trunk ({len(items)} items): {cont_fid:#010x}")

# SAVE
out = esp.save('H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data/MnehmosMojave.esp')
print(f"\n=== CONSOLIDATED MnehmosMojave.esp ===")
print(f"Saved: {out}")
print(f"Total records: {esp._record_count}")

# Verify
from core.binary_parser import PluginFile as PF
v = PF(str(out))
for label in sorted(v.group_labels):
    count = v.count_records(label)
    print(f"  {label}: {count}")
