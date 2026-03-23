# MnemoScript Language Specification v0.1

A minimal DSL that compiles to Fallout New Vegas SCPT bytecode.
Designed for LLM authoring — clean syntax, no ambiguity, maximum signal.

---

## Design Principles

1. **LLM-native**: Claude/GPT can write valid MnemoScript without examples
2. **Minimal surface**: Only features that compile to vanilla+NVSE bytecode
3. **Explicit references**: FormIDs and EditorIDs resolve at compile time
4. **No implicit state**: Every variable declared, every ref registered

---

## Script Structure

```
script MyScriptName           ; required — becomes EDID
type quest                    ; object | quest | effect

; variable declarations (order matters — defines SLSD indices)
int iCounter
float fDamage
ref rTarget

; reference declarations (external FormIDs — becomes SCRO entries)
use player    0x00000014
use SunnyREF  0x0010A44C
use Luck      actorvalue 11

; event blocks
on GameMode
  ; statements here
end

on OnActivate
  ; statements here
end
```

---

## Types

| Type | SLSD Flag | Bytecode Marker | Notes |
|------|-----------|-----------------|-------|
| `int` | 0x01 | `s` (0x73) | Short/long integer |
| `float` | 0x00 | `f` (0x66) | Floating point |
| `ref` | 0x00 | `f` (0x66) | Object reference (same encoding as float) |

---

## Event Blocks

```
on <EventType> [params]
  ; body
end
```

| Event | Opcode | Params |
|-------|--------|--------|
| `GameMode` | 0x0000 | none |
| `MenuMode` | 0x0001 | none |
| `OnActivate` | 0x0002 | none |
| `OnAdd` | 0x0003 | none |
| `OnEquip` | 0x0004 | none |
| `OnUnequip` | 0x0005 | none |
| `OnDrop` | 0x0006 | none |
| `OnHit` | 0x0008 | none |
| `OnDeath` | 0x000A | none |
| `OnCombatEnd` | 0x000C | none |
| `ScriptEffectStart` | 0x0011 | none |
| `ScriptEffectFinish` | 0x0012 | none |
| `ScriptEffectUpdate` | 0x0013 | none |
| `OnStartCombat` | 0x0019 | none |
| `OnFire` | 0x0024 | none |

---

## Statements

### Assignment
```
set iCounter to 5
set fDamage to 3.14
set fDamage to player.GetAV Luck
set iCounter to iCounter + 1
```

### Function Calls (standalone)
```
player.ModAV Health 50.0
player.AddItem AmmoRef 100
player.EquipItem WeaponRef
Enable
Disable
```

### Conditionals
```
if iCounter > 5
  player.ModAV Health 10.0
elseif iCounter > 2
  player.ModAV Health 5.0
else
  player.ModAV Health 1.0
endif
```

### Return
```
return
```

---

## Expressions

Expressions appear in `set ... to <expr>` and `if <expr>` contexts.

### Literals
- Integer: `42`, `-5`, `0`
- Float: `3.14`, `-0.5`, `1.0`

### Variables
- Local: `iCounter`, `fDamage`, `rTarget`
- Prefix convention: `i` = int, `f` = float, `r` = ref (not enforced, just convention)

### Operators (precedence high → low)
| Op | Meaning |
|----|---------|
| `*`, `/`, `%` | Multiply, divide, modulo |
| `+`, `-` | Add, subtract |
| `<`, `<=`, `>`, `>=` | Comparison |
| `==`, `!=` | Equality |
| `&&` | Logical AND |
| `\|\|` | Logical OR |
| `-` (unary) | Negation |

### Function Calls in Expressions
```
set fDamage to player.GetAV Strength * 2.0
if player.GetAV Health < 50.0
```

---

## Reference Calls

Functions called on a reference use dot notation:
```
player.GetAV Health         ; 0x1C [playerIdx] 0x100E [params]
SunnyREF.GetDead            ; 0x1C [sunnyIdx] 0x102E
rTarget.Enable              ; 0x1C [rTargetIdx] 0x1021
```

Bare function calls (no ref prefix) execute on `self`:
```
Enable                      ; called on the scripted object itself
Disable
GetPos X
```

---

## Function Registry

Functions are resolved by name to opcode. The compiler ships with:

### Built-in (vanilla) — 533+ functions
All functions from 0x1000-0x1214 registered by canonical name and short alias.

### NVSE — registered by name
Key NVSE functions registered manually (Let, GetEquippedObject, etc.)
NVSE functions use the `0xFFFF` inline expression marker.

### JIP LN — registered by name
Key JIP functions registered manually (GetWeaponAmmoCount, etc.)

### Custom registration
```
; at top of script, register unknown opcodes
opcode GetWeaponAmmoCount 0x2547
```

---

## Comments

```
; single-line comment (semicolons, matching GECK convention)
```

---

## Complete Example

```
; Perk script: bonus damage when firing last round in magazine
script MnGunLastRound
type effect

float fAmmo
ref rWeap

use player 0x00000014

on ScriptEffectUpdate
  set rWeap to player.GetEquippedObject 5
  set fAmmo to player.GetWeaponAmmoCount rWeap
  if fAmmo <= 1.0
    player.ModAV DamageMultiplier 0.50
  endif
end
```

---

## Compilation Output

For the above script, the compiler produces:

1. **EDID**: `MnGunLastRound\0`
2. **SCHR**: `{unused:0, refCount:1, compiledSize:N, varCount:2, type:0x0100, flags:0x0001}`
3. **SCDA**: Compiled bytecode (ScriptName + var decls + Begin block + instructions + End)
4. **SCTX**: Original source text
5. **SLSD[0]**: `{index:0, flags:0x00}` + SCVR `fAmmo\0`
6. **SLSD[1]**: `{index:1, flags:0x00}` + SCVR `rWeap\0`
7. **SCRO[0]**: `0x00000014` (player)

These subrecords form a complete SCPT record ready for ESP injection.
