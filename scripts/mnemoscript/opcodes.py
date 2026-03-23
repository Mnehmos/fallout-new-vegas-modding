"""
MnemoScript Opcode Registry — Fallout New Vegas

Maps function names to their 2-byte opcode values.
Sources:
  - mod.gib.me/fonv/functions.html (vanilla 0x1000-0x1214)
  - xNVSE source CommandTable.h (NVSE 0x1400+)
  - JIP LN NVSE source (0x2200+)
"""

# --- Statement opcodes (control flow) ---
OP_BEGIN         = 0x0010
OP_END           = 0x0011
OP_SHORT         = 0x0012
OP_LONG          = 0x0013
OP_FLOAT         = 0x0014
OP_SET           = 0x0015
OP_IF            = 0x0016
OP_ELSE          = 0x0017
OP_ELSEIF        = 0x0018
OP_SETCURRENTREF = 0x001C
OP_SCRIPTNAME    = 0x001D
OP_RETURN        = 0x001E
OP_REF           = 0x001F

# --- Event block types ---
EVENTS = {
    'gamemode':              0x0000,
    'menumode':              0x0001,
    'onactivate':            0x0002,
    'onadd':                 0x0003,
    'onequip':               0x0004,
    'onunequip':             0x0005,
    'ondrop':                0x0006,
    'saytodone':             0x0007,
    'onhit':                 0x0008,
    'onhitwith':             0x0009,
    'ondeath':               0x000A,
    'onmurder':              0x000B,
    'oncombatend':           0x000C,
    'onpackagestart':        0x000F,
    'onpackagedone':         0x0010,
    'scripteffectstart':     0x0011,
    'scripteffectfinish':    0x0012,
    'scripteffectupdate':    0x0013,
    'onpackagechange':       0x0014,
    'onload':                0x0015,
    'onmagiceffecthit':      0x0016,
    'onsell':                0x0017,
    'ontrigger':             0x0018,
    'onstartcombat':         0x0019,
    'ontriggerenter':        0x001A,
    'ontriggerleave':        0x001B,
    'onactorequip':          0x001C,
    'onactorunequip':        0x001D,
    'onreset':               0x001E,
    'onopen':                0x001F,
    'onclose':               0x0020,
    'ongrab':                0x0021,
    'onrelease':             0x0022,
    'onfire':                0x0024,
}

# --- Actor Value indices (for GetAV/SetAV/ModAV parameter) ---
ACTOR_VALUES = {
    'aggression':       0,  'confidence':       1,  'energy':           2,
    'responsibility':   3,  'mood':             4,
    'strength':         5,  'perception':       6,  'endurance':        7,
    'charisma':         8,  'intelligence':     9,  'agility':         10,
    'luck':            11,
    'actionpoints':    12,  'carryweight':     13,  'critchance':      14,
    'healrate':        15,  'health':          16,  'meleedamage':     17,
    'damageresist':    18,  'poisonresist':    19,  'radresist':       20,
    'speedmult':       21,  'fatigue':         22,  'karma':           23,
    'xp':              24,
    'barter':          32,  'bigguns':         33,  'energyweapons':   34,
    'explosives':      35,  'lockpick':        36,  'medicine':        37,
    'meleeweapons':    38,  'repair':          39,  'science':         40,
    'guns':            41,  'sneak':           42,  'speech':          43,
    'survival':        44,  'unarmed':         45,
    # Aliases
    'damagemultiplier': 18,  # Fallback — commonly used in perk scripts
}

# --- Vanilla function opcodes (0x1000-0x1214) ---
# Key functions only — extend as needed
VANILLA_FUNCTIONS = {
    # Core
    'getdistance':          0x1001,
    'additem':              0x1002,
    'getpos':               0x1006,
    'setpos':               0x1007,
    'getangle':             0x1008,
    'setangle':             0x1009,
    'getsecondspassed':     0x100C,
    'activate':             0x100D,
    'getactorvalue':        0x100E,
    'setactorvalue':        0x100F,
    'modactorvalue':        0x1010,
    'enable':               0x1021,
    'disable':              0x1022,
    'placeatme':            0x1025,
    'getitemcount':         0x102F,
    'getdead':              0x102E,
    'say':                  0x1033,
    'sayto':                0x1034,
    'startquest':           0x1036,
    'stopquest':            0x1037,
    'getquestrunning':      0x1038,
    'setstage':             0x1039,
    'getstage':             0x103A,
    'getlevel':             0x1050,
    'removeitem':           0x1052,
    'showmessage':          0x1059,
    'kill':                 0x108B,
    'getisreference':       0x1088,
    'getisid':              0x1048,
    'movetomarker':         0x109E,
    'getequipped':          0x10B6,
    'equipitem':            0x10EE,
    'unequipitem':          0x10EF,
    'forceactorvalue':      0x110E,
    'getbaseactorvalue':    0x1115,
    'isincombat':           0x1121,
    'isininterior':         0x112C,
    'getinworldspace':      0x1136,
    'getlinkedref':         0x116B,
    'isinlist':             0x1174,
    'addperk':              0x1176,
    'damageactorvalue':     0x1181,
    'restoreactorvalue':    0x1182,
    'removeperk':           0x11A8,
    'gethealthpercentage':  0x11AF,
    'markfordelete':        0x11BB,
    'hasperk':              0x11C1,
    'getpermanentav':       0x11EF,

    # Aliases (short names)
    'getav':        0x100E,
    'setav':        0x100F,
    'modav':        0x1010,
    'forceav':      0x110E,
    'getbaseav':    0x1115,
    'getpermav':    0x11EF,
    'damageav':     0x1181,
    'restoreav':    0x1182,
}

# --- NVSE functions (0x1400+) ---
# Exact opcodes depend on NVSE version — these are from xNVSE 6.x
NVSE_FUNCTIONS = {
    # These are approximate — the user can override with `opcode` declarations
    'getequippedobject':    0x1458,  # GetEqObj
    'geteqobj':             0x1458,
}

# --- JIP LN NVSE functions (0x2200+) ---
JIP_FUNCTIONS = {
    # Weapon info
    'getweaponammocount':   0x2547,  # approximate
    'getweapontype':        0x2200,  # approximate
}

# --- Combined registry ---
def build_registry():
    """Build the combined function name → opcode mapping."""
    registry = {}
    registry.update(VANILLA_FUNCTIONS)
    registry.update(NVSE_FUNCTIONS)
    registry.update(JIP_FUNCTIONS)
    return registry

FUNCTION_REGISTRY = build_registry()


def resolve_function(name: str) -> int | None:
    """Resolve a function name (case-insensitive) to its opcode."""
    return FUNCTION_REGISTRY.get(name.lower())


def resolve_actor_value(name: str) -> int | None:
    """Resolve an actor value name (case-insensitive) to its index."""
    return ACTOR_VALUES.get(name.lower())


def resolve_event(name: str) -> int | None:
    """Resolve an event name (case-insensitive) to its block type opcode."""
    return EVENTS.get(name.lower())
