"""Full 10-sweep audit of MnehmosMojave.esp"""
import sys, struct
sys.path.insert(0, 'F:/Github/mnehmos.fnvedit.mcp/src')
from core.binary_parser import PluginFile

mm = PluginFile('H:/01_Games/Steam/steamapps/common/Fallout New Vegas/Data/MnehmosMojave.esp')
errors = []
warnings = []

print('=== MNEHMOS MOJAVE ESP - FULL AUDIT ===\n')

# SWEEP 1: Weapon damage
print('SWEEP 1: Weapon damage')
for r in mm.get_records('WEAP'):
    srs = r.parse_subrecords()
    edid = ''; name = ''; dmg = 0; proj = 1; clip = 0; rate = 0; cd = 0; cm = 0
    for sr in srs:
        if sr.type == 'EDID': edid = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'FULL': name = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'DATA' and len(sr.data) >= 14:
            dmg = struct.unpack_from('<H', sr.data, 12)[0]
            clip = sr.data[14] if len(sr.data) > 14 else 0
        if sr.type == 'DNAM' and len(sr.data) >= 72:
            rate = struct.unpack_from('<f', sr.data, 64)[0]
            proj = sr.data[42] if len(sr.data) > 42 else 1
        if sr.type == 'CRDT' and len(sr.data) >= 8:
            cd = struct.unpack_from('<H', sr.data, 0)[0]
            cm = struct.unpack_from('<f', sr.data, 4)[0]
    total = dmg * proj if proj > 1 else dmg
    s = 'OK'
    if dmg == 0: s = 'ERR'; errors.append(f'{edid}: 0 damage')
    print(f'  [{s:3s}] {name:35s} DMG={dmg:4d} x{proj}={total:5d} Clip={clip:3d} Rate={rate:5.1f} Crit={cd}/{cm:.1f}')

# SWEEP 2: Armor DT
print('\nSWEEP 2: Armor DT')
for r in mm.get_records('ARMO'):
    srs = r.parse_subrecords()
    edid = ''; name = ''; dt = 0; val = 0; hp = 0
    for sr in srs:
        if sr.type == 'EDID': edid = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'FULL': name = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'DATA' and len(sr.data) >= 12:
            val = struct.unpack_from('<I', sr.data, 0)[0]
            hp = struct.unpack_from('<I', sr.data, 4)[0]
        if sr.type == 'DNAM' and len(sr.data) >= 8:
            dt = struct.unpack_from('<f', sr.data, 4)[0]
    s = 'OK'
    if dt == 0 and 'Glasses' not in edid and 'Hat' not in edid and 'Lenses' not in edid and val > 1000:
        s = 'WARN'; warnings.append(f'{edid}: 0 DT')
    print(f'  [{s:4s}] {name:35s} DT={dt:5.1f} HP={hp:5d} Val={val:6d}')

# SWEEP 3: Enchantments
print('\nSWEEP 3: Enchantments')
for r in mm.get_records('ENCH'):
    srs = r.parse_subrecords()
    edid = ''; name = ''; effects = 0
    for sr in srs:
        if sr.type == 'EDID': edid = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'FULL': name = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'EFID': effects += 1
    print(f'  [OK ] {name:35s} {effects} effect(s)')

# SWEEP 4: NPCs
print('\nSWEEP 4: NPCs')
for r in mm.get_records('NPC_'):
    srs = r.parse_subrecords()
    edid = ''; name = ''
    for sr in srs:
        if sr.type == 'EDID': edid = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'FULL': name = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
    local = r.id & 0xFFFFFF
    print(f'  [OK ] {name:35s} local:{local:#08x}')

# SWEEP 5: Leveled lists
print('\nSWEEP 5: Leveled lists')
for rtype in ['LVLN', 'LVLI']:
    for r in mm.get_records(rtype):
        srs = r.parse_subrecords()
        edid = ''; entries = 0
        for sr in srs:
            if sr.type == 'EDID': edid = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
            if sr.type == 'LVLO': entries += 1
        print(f'  [{rtype}] {edid:40s} {entries} entries')

# SWEEP 6: Casinos
print('\nSWEEP 6: Casinos')
for r in mm.get_records('CSNO'):
    srs = r.parse_subrecords()
    name = ''; max_win = 0; payout = 0
    for sr in srs:
        if sr.type == 'FULL': name = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'DATA' and len(sr.data) >= 44:
            payout = struct.unpack_from('<f', sr.data, 4)[0]
            max_win = struct.unpack_from('<I', sr.data, 40)[0]
    print(f'  [OK ] {name:20s} MaxWin={max_win:>7d} Payout={payout:.1f}x')

# SWEEP 7: Duplicate EditorIDs
print('\nSWEEP 7: Duplicate check')
all_edids = {}
for label in mm.group_labels:
    for r in mm.get_records(label):
        for sr in r.parse_subrecords():
            if sr.type == 'EDID':
                edid = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
                if edid in all_edids:
                    errors.append(f'DUPLICATE: {edid} in {label} and {all_edids[edid]}')
                    print(f'  [ERR] DUPLICATE: {edid}')
                else:
                    all_edids[edid] = label
print(f'  {len(all_edids)} unique, {len([e for e in errors if "DUPLICATE" in e])} duplicates')

# SWEEP 8: Note text
print('\nSWEEP 8: Notes')
for r in mm.get_records('NOTE'):
    srs = r.parse_subrecords()
    name = ''; has_tnam = False
    for sr in srs:
        if sr.type == 'FULL': name = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'TNAM': has_tnam = True
    s = 'OK' if has_tnam else 'WARN'
    print(f'  [{s:4s}] {name}')

# SWEEP 9: Container inventory
print('\nSWEEP 9: Containers')
for r in mm.get_records('CONT'):
    srs = r.parse_subrecords()
    name = ''; cnto = 0
    for sr in srs:
        if sr.type == 'FULL': name = sr.data.rstrip(b'\x00').decode('utf-8', errors='replace')
        if sr.type == 'CNTO': cnto += 1
    print(f'  [{"OK" if cnto > 0 else "WARN":4s}] {name:35s} {cnto} items')

# SWEEP 10: Record totals
print('\nSWEEP 10: Totals')
total = 0
for label in sorted(mm.group_labels):
    count = mm.count_records(label)
    total += count
    print(f'  {label:6s}: {count:4d}')
print(f'  TOTAL: {total:4d}')

# FINAL
print(f'\n{"="*60}')
print(f'ERRORS:   {len(errors)}')
for e in errors: print(f'  ! {e}')
print(f'WARNINGS: {len(warnings)}')
for w in warnings: print(f'  ~ {w}')
print(f'\n{"ESP CLEAN" if len(errors) == 0 else f"{len(errors)} ISSUES"}')
