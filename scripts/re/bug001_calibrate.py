"""Calibrate VATSTargetData position triples: which combination = target distance?
Run while IN VATS targeting a thrown projectile. Samples both triples over time
and prints deltas so we can identify the player->target distance source."""
import ctypes, struct, psutil, time, math

pid = next((p.pid for p in psutil.process_iter(["name"]) if p.info["name"] == "FalloutNV.exe"), None)
h = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)

def read(addr, size):
    buf = ctypes.create_string_buffer(size); got = ctypes.c_ulong(0)
    k32 = ctypes.windll.kernel32
    k32.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, size, ctypes.byref(got))
    return buf.raw[:got.value]

def u32(a): return struct.unpack("<I", read(a, 4))[0]

def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

print("sampling 10s — stay in VATS, keep the grenade targeted, move the camera a little...")
for i in range(20):
    menu = u32(0x011DB0D4)
    if not menu:
        print("VATS closed"); break
    sel = u32(menu + 0x100)
    raw = read(sel, 0x2C)
    if not raw or len(raw) < 0x2C:
        time.sleep(0.5); continue
    pa = struct.unpack_from("<3f", raw, 0x08)   # triple 1 (+0x08)
    pb = struct.unpack_from("<3f", raw, 0x14)   # triple 2 (+0x14)
    chance = struct.unpack_from("<f", raw, 0x28)[0]
    d_ab = dist(pa, pb)
    print(f"t={i*0.5:4.1f}s  posA=({pa[0]:9.1f},{pa[1]:9.1f},{pa[2]:7.1f})  "
          f"posB=({pb[0]:9.1f},{pb[1]:9.1f},{pb[2]:7.1f})  |A-B|={d_ab:8.1f}  chance={chance}")
    time.sleep(0.5)
ctypes.windll.kernel32.CloseHandle(h)