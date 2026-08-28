"""mnehmos.debug.mcp — x32dbg debugger control MCP server.

Wraps x32dbg's named pipe protocol as LLM-friendly tools. Spawns x32dbg
attached to a target and exposes breakpoint/register/memory/run control.

Protocol reference: x64dbg named pipe uses JSON commands:
  {"command":"<cmd>","arg":"<arg>"}
  Response: {"data":"<result>","result":<int>}
"""
from __future__ import annotations

import ctypes
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.fastmcp import FastMCP

X32DBG = Path(
    r"C:\Users\mnehm\AppData\Local\Microsoft\WinGet\Packages"
    r"\x64dbg.x64dbg_Microsoft.Winget.Source_8wekyb3d8bbwe\release\x32\x32dbg.exe"
)
FNV_EXE = Path(r"E:\GOG Galaxy\Games\Fallout New Vegas\FalloutNV.exe")
PIPE = r"\\.\pipe\x32dbg"
GEN_READ = 0x80000000
GEN_WRITE = 0x40000000
OPEN_EXISTING = 3

GAME_DIRS = [
    Path(r"H:\01_Games\Steam\steamapps\common\Fallout New Vegas"),
    Path(r"E:\GOG Galaxy\Games\Fallout New Vegas"),
]

mcp = FastMCP("mnehmos.debug.mcp")


def _pipe_send(cmd: str, timeout: float = 3.0) -> dict:
    k32 = ctypes.windll.kernel32
    h = k32.CreateFileW(PIPE, GEN_READ | GEN_WRITE, 0, None, OPEN_EXISTING, 0, None)
    if h == -1 or h == 0:
        return {"error": f"pipe connect failed 0x{ctypes.GetLastError():08X}"}
    data = (cmd + "\r\n").encode("utf-8")
    written = ctypes.c_ulong(0)
    k32.WriteFile(h, data, len(data), ctypes.byref(written), None)
    time.sleep(0.15)
    buf = ctypes.create_string_buffer(65536)
    read = ctypes.c_ulong(0)
    ok = k32.ReadFile(h, buf, 65536, ctypes.byref(read), None)
    k32.CloseHandle(h)
    if not ok:
        return {"error": f"pipe read failed 0x{ctypes.GetLastError():08X}"}
    raw = buf.value[:read.value].decode("utf-8", errors="replace").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"data": raw, "result": 1}


def _spawn_x32dbg(target: str | Path | None = None) -> bool:
    """Launch x32dbg with the target binary. Returns True if already running."""
    import psutil
    for p in psutil.process_iter(["name"]):
        if p.info["name"] and "x32dbg" in p.info["name"].lower():
            return True
    cmd = [str(X32DBG)]
    if target:
        cmd.append(str(target))
    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    time.sleep(2)
    return False


# ---------------------------------------------------------------- tools


@mcp.tool()
def dbg_attach(target: str = "") -> str:
    """Launch x32dbg attached to a target executable. Default = FalloutNV.exe (GOG)."""
    exe = Path(target) if target else FNV_EXE
    if not exe.exists():
        for d in GAME_DIRS:
            c = d / exe.name
            if c.exists():
                exe = c
                break
        else:
            return json.dumps({"error": f"not found: {exe}"})
    already = _spawn_x32dbg(exe)
    return json.dumps({"ok": True, "already_running": already, "command": str(exe), "note": "Press F9 in x32dbg to run the target"})


@mcp.tool()
def dbg_version() -> str:
    """Query x32dbg version via the named pipe."""
    return json.dumps(_pipe_send('{"command":"version"}'), indent=1)


@mcp.tool()
def dbg_set_bp(address: str, hw: bool = False) -> str:
    """Set a breakpoint at a VA (e.g. '0x00646F50'). hw=true for hardware write (watchpoint)."""
    if hw:
        r = _pipe_send(f'{{"command":"SetBPX","arg":"bp={address},type=hw-w"}}')
    else:
        r = _pipe_send(f'{{"command":"SetBPX","arg":"bp={address},type=ss"}}')
    return json.dumps(r, indent=1)


@mcp.tool()
def dbg_delete_bp(address: str) -> str:
    """Delete a breakpoint at a VA."""
    return json.dumps(_pipe_send(f'{{"command":"DelBPX","arg":"bp={address}"}}'), indent=1)


@mcp.tool()
def dbg_read_regs() -> str:
    """Read all CPU registers."""
    r = _pipe_send('{"command":"GetRegisters","arg":""}')
    return json.dumps(r, indent=1)


@mcp.tool()
def dbg_read_reg(register: str = "ecx") -> str:
    """Read a single register value (eax, ecx, edx, ebx, esp, ebp, esi, edi, eip, eflags)."""
    r = _pipe_send(f'{{"command":"GetRegisters","arg":"{register}"}}')
    return json.dumps(r, indent=1)


@mcp.tool()
def dbg_read_mem(address: str, size: int = 16) -> str:
    """Read hex bytes from memory at a VA (e.g. '0x00647A50')."""
    r = _pipe_send(f'{{"command":"ReadMem","arg":"addr={address},size={size}"}}')
    return json.dumps(r, indent=1)


@mcp.tool()
def dbg_write_mem(address: str, hex_data: str) -> str:
    """Write hex bytes to memory at a VA. hex_data = space-separated hex bytes."""
    data_clean = "".join(hex_data.split()).lower()
    r = _pipe_send(f'{{"command":"WriteMem","arg":"addr={address},data={data_clean}"}}')
    return json.dumps(r, indent=1)


@mcp.tool()
def dbg_write_float(address: str, value: float) -> str:
    """Write a 32-bit float to memory at a VA (for patching projectile+0x124 etc.)."""
    import struct
    data_clean = struct.pack("<f", value).hex()
    r = _pipe_send(f'{{"command":"WriteMem","arg":"addr={address},data={data_clean}"}}')
    return json.dumps({"value": value, "address": address, "written_hex": data_clean, **r}, indent=1)


@mcp.tool()
def dbg_run() -> str:
    """Continue execution (F9)."""
    return json.dumps(_pipe_send('{"command":"run"}'), indent=1)


@mcp.tool()
def dbg_pause() -> str:
    """Pause execution."""
    return json.dumps(_pipe_send('{"command":"pause"}'), indent=1)


@mcp.tool()
def dbg_step_into() -> str:
    """Step into instruction (F7)."""
    return json.dumps(_pipe_send('{"command":"stepinto"}'), indent=1)


@mcp.tool()
def dbg_step_over() -> str:
    """Step over instruction (F8)."""
    return json.dumps(_pipe_send('{"command":"stepover"}'), indent=1)


@mcp.tool()
def dbg_eval(expression: str) -> str:
    """Evaluate an x32dbg expression (e.g. 'ecx', '[ecx+0x124]', '[ecx+0x124]:4') and return value."""
    r = _pipe_send(f'{{"command":"Eval","arg":"{expression}"}}')
    return json.dumps(r, indent=1)


@mcp.tool()
def dbg_read_as_float(address: str) -> str:
    """Read a 32-bit float value from memory at VA (e.g., read projectile+0x124)."""
    mem = _pipe_send(f'{{"command":"ReadMem","arg":"addr={address},size=4"}}')
    try:
        data = mem.get("data", "")
        bytes_ = bytes.fromhex(data.replace(" ", ""))
        if len(bytes_) == 4:
            import struct
            val = struct.unpack("<f", bytes_)[0]
            return json.dumps({"address": address, "float_value": val, "hex": data}, indent=1)
    except Exception as e:
        pass
    return json.dumps({"error": "failed to parse float", "raw": mem}, indent=1)


if __name__ == "__main__":
    mcp.run()
