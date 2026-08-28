// FNVBug001Fix v3 — NVSE plugin fixing FNV-BUG-001 with the RECOVERED FORMULA.
//
// Root cause (docs/data/bugs.json FNV-BUG-001): the engine's grenade-target
// chance implementation (FUN_00646F70 thrown branch) is dead code on PC —
// never called. The live VATS target scan writes 0.0 into the target data's
// chance field (+0x28) and nothing ever computes it.
//
// v3 fix: per-frame poller recomputes the chance for the selected target
// using the recovered falloff shape with the engine's own live settings:
//
//   rangeGap   = falloffScale                       (documented tunable)
//   distDelta  = |throwDist - fVATSGrenadeRangeMin| (128 = ideal arc sweet spot)
//   rangeOdds  = 1 - distDelta/rangeGap
//   chance     = clamp(rangeOdds, floor, 1.0) * fVATSGrenadeChanceMult * 100
//
// throwDist = |posA - posB| read live from the target struct (+0x08 vs +0x14),
// exactly the quantity the engine's own scan produces.
// Gate fix (DoIdle zero-chance block) remains applied.

#include <windows.h>
#include <cstdint>
#include <cmath>

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
static const unsigned int kVersion = 3;
static const unsigned int kInfoVersion = 1;

static volatile bool g_stop = false;
static HANDLE g_thread = nullptr;

// image-base-relative (FNV.exe: no ASLR, base 0x00400000)
static const uintptr_t MENU_GLOBAL = 0x011DB0D4;
static const DWORD MENU_SEL_OFF = 0x100;
static const float CHANCE_MULT_DEFAULT = 100.0f;

// falloff scale: max VATS engagement distance for thrown projectiles.
// Derived from observed scan envelope (targets tracked at 11k-47k units).
static float g_falloffScale = 50000.0f;
// floor: minimum displayed chance so far throws stay targetable (Stewie-style floor)
static float g_floor = 0.05f;

struct Mem {
    HANDLE h;
    Mem() : h(nullptr) {}
    bool open(unsigned long pid) {
        h = OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION, FALSE, pid);
        return h != nullptr;
    }
    bool read(uintptr_t a, void* out, size_t n) {
        SIZE_T g = 0;
        return ReadProcessMemory(h, (LPCVOID)a, out, n, &g) && g == n;
    }
    bool write(uintptr_t a, const void* d, size_t n) {
        SIZE_T w = 0;
        return WriteProcessMemory(h, (LPVOID)a, d, n, &w) && w == n;
    }
    ~Mem() { if (h) CloseHandle(h); }
};

struct MemWriter_ {};

static DWORD WINAPI PollThread(LPVOID)
{
    while (!g_stop) {
        Sleep(200);

        Mem mw;
        if (!mw.open(GetCurrentProcessId())) continue;

        uint32_t menu = 0;
        if (!mw.read(MENU_GLOBAL, &menu, 4) || !menu) continue;       // VATS closed

        uint32_t target = 0;
        if (!mw.read(menu + MENU_SEL_OFF, &target, 4) || !target) continue;

        unsigned char raw[0x2C];
        if (!mw.read(target, raw, 0x2C)) continue;

        float posA[3], posB[3];
        memcpy(posA, raw + 0x08, 12);
        memcpy(posB, raw + 0x14, 12);
        float dx = posA[0] - posB[0], dy = posA[1] - posB[1], dz = posA[2] - posB[2];
        float dist = sqrtf(dx*dx + dy*dy + dz*dz);

        // live settings (in-process: read Setting value floats directly at obj+4)
        float rangeMin = 128.0f, chanceMult = 1.0f;
        uint32_t v = 0;
        if (mw.read(0x011CFBA8 + 4, &v, 4)) rangeMin = *(float*)&v;   // fVATSGrenadeRangeMin
        if (mw.read(0x011CF8BC + 4, &v, 4)) chanceMult = *(float*)&v; // fVATSGrenadeChanceMult

        float distDelta = fabsf(dist - rangeMin);
        float rangeOdds = 1.0f - distDelta / g_falloffScale;
        if (rangeOdds < g_floor) rangeOdds = g_floor;
        if (rangeOdds > 1.0f) rangeOdds = 1.0f;

        float chance = rangeOdds * chanceMult * 100.0f;

        float current = 0.0f;
        memcpy(&current, raw + 0x28, 4);
        if (current <= 0.0f) {
            mw.write(target + 0x28, &chance, 4);   // only when zero: don't fight the UI
        }
    }
    return 0;
}

static bool ApplyGateFix()
{
    BYTE* gate = reinterpret_cast<BYTE*>(0x00400000 + 0x003EEA46);  // 0x007EEA46
    if (*gate != 0x44) return false;
    DWORD old = 0;
    if (!VirtualProtect(gate, 1, PAGE_EXECUTE_READWRITE, &old)) return false;
    *gate = 0x00;
    VirtualProtect(gate, 1, old, &old);
    return true;
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
    if (!ApplyGateFix()) return false;
    g_thread = CreateThread(nullptr, 0, PollThread, nullptr, 0, nullptr);
    return g_thread != nullptr;
}

} // extern "C"

BOOL WINAPI DllMain(HINSTANCE, DWORD, LPVOID) { return TRUE; }
