"""BUG-001 runtime patch: force projectile+0x124 to a test value.
No debugger needed — uses WriteProcessMemory on the live FNV process.
Run AFTER launching FNV normally and reaching the main menu.
This patches the code at 0x00646F50 to return a controlled float,
then restores the original bytes when you press Enter.
"""
import ctypes
import struct
import sys
import time

FNV_EXE = "FalloutNV.exe"
PATCH_VA = 0x00646F50

# Original bytes: fld dword [ecx+0x124]; ret
# Patch:          mov eax, <float_val>; ret (7 bytes)
#   B8 xx xx xx xx C3  — mov eax, imm32; ret

k32 = ctypes.windll.kernel32

PROCESS_ALL_ACCESS = 0x1F0FFF
PAGE_EXECUTE_READWRITE = 0x40
PAGE_EXECUTE_READ = 0x20


def find_process(name):
    import psutil
    for p in psutil.process_iter(["name"]):
        if p.info["name"] == name:
            return p.pid
    return None


def patch_float(float_val: float):
    pid = find_process(FNV_EXE)
    if not pid:
        print(f"error: {FNV_EXE} not running. Launch it first.")
        return

    h = k32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h:
        print(f"error: OpenProcess failed (err={ctypes.GetLastError()})")
        return

    # Save original bytes
    orig = ctypes.create_string_buffer(7)
    read = ctypes.c_ulong(0)
    k32.ReadProcessMemory(h, PATCH_VA, orig, 7, ctypes.byref(read))
    orig_bytes = bytes(orig)

    # Make code page writable
    old = ctypes.c_ulong(0)
    k32.VirtualProtectEx(h, PATCH_VA, 7, PAGE_EXECUTE_READWRITE, ctypes.byref(old))

    # Build patch: mov eax, float_val; ret
    patch = bytes([0xB8]) + struct.pack("<f", float_val) + bytes([0xC3])

    written = ctypes.c_ulong(0)
    ok = k32.WriteProcessMemory(h, PATCH_VA, patch, 7, ctypes.byref(written))

    if not ok:
        print(f"error: WriteProcessMemory failed (err={ctypes.GetLastError()})")
        k32.CloseHandle(h)
        return

    print(f"patched 0x{PATCH_VA:08X} -> return {float_val} (orig: {orig_bytes.hex()})")
    print(f"Enter VATS with a thrown grenade and observe hit chance.")
    input("Press Enter to restore original bytes...")

    # Restore original
    k32.WriteProcessMemory(h, PATCH_VA, orig_bytes, 7, ctypes.byref(written))
    k32.VirtualProtectEx(h, PATCH_VA, 7, old, ctypes.byref(old))
    k32.CloseHandle(h)
    print("restored. done.")


if __name__ == "__main__":
    val = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0
    patch_float(val)