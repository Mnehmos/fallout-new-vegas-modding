"""BUG-001 engine fix: neutralize the VATS zero-chance queue block.

0x007EEA44: test ah, 0x44   ->   test ah, 0x00
(one byte: the equality/unordered mask becomes always-zero, so the
zero-chance block never triggers and grenade entries become queueable
at their computed chance, matching console behavior.)
"""
import ctypes
import struct
import psutil

GATE_ADDR = 0x007EEA44
ORIG = bytes([0x44])
FIXED = bytes([0x00])

k32 = ctypes.windll.kernel32
pid = next((p.pid for p in psutil.process_iter(["name"]) if p.info["name"] == "FalloutNV.exe"), None)
if not pid:
    raise SystemExit("FalloutNV.exe not running")

h = k32.OpenProcess(0x1F0FFF, False, pid)

def read(addr, size):
    buf = ctypes.create_string_buffer(size)
    got = ctypes.c_ulong(0)
    k32.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, size, ctypes.byref(got))
    return buf.raw[:got.value]

cur = read(GATE_ADDR, 1)
if cur == FIXED:
    print("already patched (test ah,0x00) — restoring original instead")
    patch, label = ORIG, "original"
else:
    if cur != ORIG:
        raise SystemExit(f"unexpected byte at gate: {cur.hex()} (expected 0x44)")
    patch, label = FIXED, "fix"

old = ctypes.c_ulong(0)
k32.VirtualProtectEx(h, GATE_ADDR, 1, 0x40, ctypes.byref(old))
wrote = ctypes.c_ulong(0)
k32.WriteProcessMemory(h, GATE_ADDR, patch, 1, ctypes.byref(wrote))
k32.CloseHandle(h)
print(f"applied {label}: test ah,{patch.hex()} at 0x{GATE_ADDR:08X}")
