// FNVBug001Fix v2 — NVSE plugin fixing FNV-BUG-001:
// VATS-targetable thrown projectiles compute exactly 0.0 chance, which the
// VATS menu treats as unqueueable (0% shown, attack blocked).
//
// RUNTIME-PROVEN FIX (docs/data/bugs.json FNV-BUG-001):
//   writing a nonzero chance into the selected VATS target's chance field
//   (targetStruct + 0x28) makes the target clickable, displays the chance,
//   and allows the attack to queue and execute.
//
// v2 design: background poller thread. Every 250ms while VATS is open:
//   menu = *(0x011DB0D4);  if menu: target = *(menu+0x100);
//   if target && *(float*)(target+0x28) == 0.0f: write 0.5f
// One-shot writes stick (the engine writes the chance once per target at
// scan time and never revisits it), so polling is sufficient.

#include <windows.h>
#include <cstdint>

struct PluginInfo {
    unsigned int infoVersion;
    const char* name;
    unsigned int version;
};

struct NVSEInterface {
    unsigned int nvseVersion;
    unsigned int runtimeVersion;
    unsigned int editorVersion;
};

static const char* kName = "FNVBug001Fix";
static const unsigned int kVersion = 2;
static const unsigned int kInfoVersion = 1;

static volatile bool g_stop = false;
static HANDLE g_thread = nullptr;

// image-base-relative offsets (FNV.exe: no ASLR, base 0x00400000)
static const uintptr_t MENU_GLOBAL_RVA = 0x00DDB0D4;   // -> 0x011DB0D4
static const DWORD MENU_SEL_OFF = 0x100;               // menu+0x100 -> target ptr
static const DWORD TARGET_CHANCE_OFF = 0x28;           // target+0x28 -> float chance
static const float CHANCE_FLOOR = 0.5f;

struct MemWriter {
    HANDLE h;
    MemWriter() : h(nullptr) {}
    bool open(unsigned long pid) {
        h = OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION, FALSE, pid);
        return h != nullptr;
    }
    bool read(uintptr_t addr, void* out, size_t size) {
        SIZE_T got = 0;
        return ReadProcessMemory(h, reinterpret_cast<LPCVOID>(addr), out, size, &got) && got == size;
    }
    bool write(uintptr_t addr, const void* data, size_t size) {
        SIZE_T wrote = 0;
        return WriteProcessMemory(h, reinterpret_cast<LPVOID>(addr), data, size, &wrote) && wrote == size;
    }
    ~MemWriter() { if (h) CloseHandle(h); }
};

static uint32_t selfPid() { return GetCurrentProcessId(); }

static DWORD WINAPI PollThread(LPVOID)
{
    while (!g_stop) {
        Sleep(250);
        MemWriter mw;
        if (!mw.open(selfPid())) continue;

        uint32_t menu = 0;
        if (!mw.read(0x00400000 + MENU_GLOBAL_RVA, &menu, 4) || menu == 0) continue;  // VATS closed

        uint32_t target = 0;
        if (!mw.read(menu + MENU_SEL_OFF, &target, 4) || target == 0) continue;      // no selection

        float chance = 0;
        if (!mw.read(target + TARGET_CHANCE_OFF, &chance, 4)) continue;
        if (chance == 0.0f) {
            float fix = CHANCE_FLOOR;
            mw.write(target + TARGET_CHANCE_OFF, &fix, 4);
        }
    }
    return 0;
}

static bool ApplyPatches()
{
    // Fix 1: neutralize the zero-chance queue block (belt) —
    //   0x007EEA44: test ah,0x44 -> test ah,0x00
    BYTE* gate = reinterpret_cast<BYTE*>(0x00400000 + 0x003EEA46);  // 0x007EEA46
    if (*gate != 0x44) return false;
    DWORD old = 0;
    if (!VirtualProtect(gate, 1, PAGE_EXECUTE_READWRITE, &old)) return false;
    *gate = 0x00;
    VirtualProtect(gate, 1, old, &old);

    // Fix 2 (suspenders): the poller thread
    g_thread = CreateThread(nullptr, 0, PollThread, nullptr, 0, nullptr);
    return g_thread != nullptr;
}

extern "C" {

__declspec(dllexport) bool NVSEPlugin_Query(const NVSEInterface* nvse, PluginInfo* info)
{
    info->infoVersion = kInfoVersion;
    info->name = kName;
    info->version = kVersion;
    if ((nvse->nvseVersion >> 16) < 6) return false;
    return true;
}

__declspec(dllexport) bool NVSEPlugin_Load(const NVSEInterface* nvse)
{
    return ApplyPatches();
}

} // extern "C"

BOOL WINAPI DllMain(HINSTANCE, DWORD, LPVOID) { return TRUE; }
