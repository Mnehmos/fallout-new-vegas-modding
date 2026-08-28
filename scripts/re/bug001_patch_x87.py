"""BUG-001 patch v2: push float -> fld [esp] -> adjust stack -> ret."""
import ctypes, struct, psutil, sys

PATCH_VA = 0x00646F50
k32 = ctypes.windll.kernel32
PAGE_EXECUTE_READWRITE = 0x40

val = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0
float_bytes = struct.pack("<f", val)

patch = bytes([0x68]) + float_bytes + bytes([0xD9, 0x04, 0x24, 0x83, 0xC4, 0x04, 0xC3])
# push imm32; fld [esp]; add esp,4; ret  (12 bytes)

for p in psutil.process_iter(["name"]):
    if p.info["name"] == "FalloutNV.exe":
        h = k32.OpenProcess(0x1F0FFF, False, p.pid)
        old = ctypes.c_ulong(0)
        k32.VirtualProtectEx(h, PATCH_VA, 12, PAGE_EXECUTE_READWRITE, ctypes.byref(old))
        written = ctypes.c_ulong(0)
        k32.WriteProcessMemory(h, PATCH_VA, patch, 12, ctypes.byref(written))
        print(f"patched 0x{PATCH_VA:08X} -> return {val}f (pid {p.pid})")
        print("Now enter VATS with a grenade. 0% should disappear.")
        k32.CloseHandle(h)
        break