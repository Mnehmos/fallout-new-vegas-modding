# Fallout New Vegas Script Bytecode Format — Compiler Reference

Research compiled 2026-03-22 from xNVSE source, UESP docs, fopdoc, GECK wiki.

---

## 1. SCPT Record Structure (ESP/ESM)

A compiled script in a plugin consists of these subrecords in order:

| Subrecord | Type       | Description                        |
|-----------|------------|------------------------------------|
| EDID      | cstring    | Editor ID                          |
| SCHR      | struct[20] | Script header (see below)          |
| SCDA      | uint8[]    | Compiled bytecode                  |
| SCTX      | char[]     | Script source text (optional)      |
| SLSD+SCVR | pairs      | Local variable definitions (repeated) |
| SCRO      | formid[4]  | Reference FormIDs (repeated)       |

### 1.1 SCHR — Script Header (20 bytes)

```
Offset  Size  Type    Field
0x00    4     uint32  unused (always 0)
0x04    4     uint32  refCount       — number of SCRO subrecords
0x08    4     uint32  compiledSize   — byte length of SCDA
0x0C    4     uint32  variableCount  — highest local variable index + 1
0x10    2     uint16  type           — 0x0000=Object, 0x0001=Quest, 0x0100=Effect
0x12    2     uint16  flags          — 0x0001=Enabled/Compiled
```

Source: `Script::ScriptInfo` in xNVSE GameScript.h:
```cpp
struct ScriptInfo {
    UInt32 unusedVariableCount;  // 0x00
    UInt32 numRefs;              // 0x04
    UInt32 dataLength;           // 0x08
    UInt32 varCount;             // 0x0C
    UInt16 type;                 // 0x10
    bool   compiled;             // 0x12
    UInt8  unk13;                // 0x13
};
```

### 1.2 SLSD — Local Variable Data (24 bytes each)

```
Offset  Size  Type    Field
0x00    4     uint32  index          — variable index (referenced in bytecode)
0x04    12    byte[]  unused
0x10    1     uint8   flags          — 0x01 = IsLongOrShort (integer)
0x11    7     byte[]  unused
```

If flags == 0x00: float or ref variable.
If flags == 0x01: short or long (integer) variable.

Each SLSD is followed by a SCVR (cstring) containing the variable name.

### 1.3 SCRO — Reference FormIDs

Each SCRO is a 4-byte FormID. Referenced in bytecode by 1-based index.
Special FormID `0x00000014` = PlayerRef.

---

## 2. Bytecode Format (SCDA)

All multi-byte values are **little-endian**.

### 2.1 General Instruction Format

```
[uint16 opcode] [uint16 argLength] [arguments...]
```

- `opcode`: 2 bytes LE — identifies the statement or command
- `argLength`: 2 bytes LE — total byte count of arguments following
- Arguments vary by opcode

### 2.2 Statement Opcodes (0x10 — 0x1F)

These are the core control-flow opcodes. Source: `ScriptStatementCode` enum in xNVSE ScriptAnalyzer.h:

| Opcode | Name              | Format                                                    |
|--------|-------------------|-----------------------------------------------------------|
| 0x10   | Begin             | `10 00` `[argLen:2]` `[paramCount:2]` `[eventOpcode:2]` `[blockLen:4]` `[params...]` |
| 0x11   | End               | `11 00` `00 00`                                           |
| 0x12   | short             | `12 00` `[argLen:2]` (variable declaration)               |
| 0x13   | long              | `13 00` `[argLen:2]` (variable declaration)               |
| 0x14   | float             | `14 00` `[argLen:2]` (variable declaration)               |
| 0x15   | Set (SetTo)       | `15 00` `[argLen:2]` `[varData...]` `[exprLen:2]` `[expression...]` |
| 0x16   | If                | `16 00` `[argLen:2]` `[jumpOps:2]` `[exprLen:2]` `[expression...]` |
| 0x17   | Else              | `17 00` `02 00` `[jumpOps:2]`                             |
| 0x18   | ElseIf            | `18 00` `[argLen:2]` `[jumpOps:2]` `[exprLen:2]` `[expression...]` |
| 0x19   | EndIf             | (implicit — jumpOps points past it)                       |
| 0x1C   | SetCurrentRef     | `1C 00` `[refIdx:2]` (then next opcode applies to that ref) |
| 0x1D   | ScriptName        | `1D 00` `04 00` `00 00 00 00`                             |
| 0x1E   | Return            | `1E 00` `00 00`                                           |
| 0x1F   | ref               | `1F 00` `[argLen:2]` (ref variable declaration)           |

### 2.3 Begin Block Detail

```
10 00                   — Begin opcode
[argLen:uint16]         — total bytes of arguments
[paramCount:uint16]     — number of parameters to the event
[eventOpcode:uint16]    — which event (see Event Block Types)
[blockLen:uint32]       — byte count of compiled code in this block
[params...]             — event-specific parameters
```

The `blockLen` counts from after the Begin header to the matching End (exclusive of the End opcode itself).

### 2.4 Event Block Types (Begin parameters)

| Opcode | Event                      |
|--------|----------------------------|
| 0x0000 | GameMode                   |
| 0x0001 | MenuMode                   |
| 0x0002 | OnActivate                 |
| 0x0003 | OnAdd                      |
| 0x0004 | OnEquip                    |
| 0x0005 | OnUnequip                  |
| 0x0006 | OnDrop                     |
| 0x0007 | SayToDone                  |
| 0x0008 | OnHit                      |
| 0x0009 | OnHitWith                  |
| 0x000A | OnDeath                    |
| 0x000B | OnMurder                   |
| 0x000C | OnCombatEnd                |
| 0x000F | OnPackageStart             |
| 0x0010 | OnPackageDone              |
| 0x0011 | ScriptEffectStart          |
| 0x0012 | ScriptEffectFinish         |
| 0x0013 | ScriptEffectUpdate         |
| 0x0014 | OnPackageChange            |
| 0x0015 | OnLoad                     |
| 0x0016 | OnMagicEffectHit           |
| 0x0017 | OnSell                     |
| 0x0018 | OnTrigger                  |
| 0x0019 | OnStartCombat              |
| 0x001A | OnTriggerEnter             |
| 0x001B | OnTriggerLeave             |
| 0x001C | OnActorEquip               |
| 0x001D | OnActorUnequip             |
| 0x001E | OnReset                    |
| 0x001F | OnOpen                     |
| 0x0020 | OnClose                    |
| 0x0021 | OnGrab                     |
| 0x0022 | OnRelease                  |
| 0x0023 | OnDestructionStageChange   |
| 0x0024 | OnFire                     |

### 2.5 If/ElseIf/Else/EndIf Encoding

**If statement:**
```
16 00                   — If opcode
[argLen:uint16]         — bytes of comparison data following
[jumpOps:uint16]        — number of operations to skip if condition false
                          (jumps to matching Else/ElseIf/EndIf)
[exprLen:uint16]        — byte length of expression data
[expression bytes...]   — RPN-encoded condition expression
```

**Else:**
```
17 00                   — Else opcode
02 00                   — argLen = 2
[jumpOps:uint16]        — operations to skip to reach EndIf
```

**ElseIf:**
```
18 00                   — ElseIf opcode
[argLen:uint16]         — same format as If
[jumpOps:uint16]
[exprLen:uint16]
[expression bytes...]
```

**EndIf:** Not an explicit opcode. The jump targets land at the next statement after the if/else chain.

### 2.6 Set Statement Encoding

```
15 00                   — Set opcode
[argLen:uint16]         — total argument bytes
[varRef]                — target variable (see Variable References below)
[exprLen:uint16]        — byte length of expression
[expression bytes...]   — RPN-encoded value expression
```

### 2.7 Function Call (Command) Encoding

For a standalone function call (not in an expression):
```
[refIdx?]               — if called on a reference: 1C 00 [refIdx:2] precedes
[opcode:uint16]         — function opcode (e.g., 0x100E for GetActorValue)
[argLen:uint16]         — total byte count of parameters
[paramCount:uint16]     — number of parameters (omitted if argLen=0)
[parameters...]         — parameter data
```

When reading bytecode, the iterator detects `0x1C` (SetCurrentRef) and reads:
```cpp
opcode = Read16();
if (opcode == 0x1C) {          // ReferenceFunction
    refIdx = Read16();          // 1-based SCRO index
    opcode = Read16();          // actual command opcode
    length = Read16();          // argument length
} else {
    refIdx = 0;
    length = Read16();
}
```

---

## 3. Expression Bytecode (RPN / Postfix)

Expressions in Set and If statements use **Reverse Polish Notation** encoding. The expression data is a byte stream parsed left-to-right with a stack evaluator.

### 3.1 Expression Token Types

| Byte    | Code | Meaning                                      |
|---------|------|----------------------------------------------|
| 0x20    | ' '  | Push separator / operand delimiter            |
| 0x47    | 'G'  | Global variable: followed by uint16 index     |
| 0x58    | 'X'  | Function call in expression                   |
| 0x5A    | 'Z'  | Standalone reference (SCRO index)             |
| 0x66    | 'f'  | Float/Ref local variable: followed by uint16 index |
| 0x6E    | 'n'  | Numeric constant (int32)                      |
| 0x72    | 'r'  | Reference for function call: uint16 SCRO index |
| 0x73    | 's'  | Short/Long local variable: uint16 index       |
| 0x7A    | 'z'  | Double-precision float constant               |
| 0x7E    | '~'  | Unary negation                                |

### 3.2 Expression ExpressionCode (from xNVSE ScriptAnalyzer.h)

```cpp
enum class ExpressionCode : UInt8 {
    None     = '\0',  // 0x00
    Int      = 's',   // 0x73 — short/long variable
    FloatRef = 'f',   // 0x66 — float or ref variable
    Global   = 'G',   // 0x47 — global variable
    Command  = 'X',   // 0x58 — function call
};
```

### 3.3 Numeric Constants in Expressions

**Integer constant:** `6E [int32 LE]` — 'n' followed by 4-byte signed integer
**Float constant:** `7A [double LE]` — 'z' followed by 8-byte IEEE 754 double

### 3.4 Variable References in Expressions

**Local integer (short/long):** `73 [uint16 varIndex]`
**Local float/ref:** `66 [uint16 varIndex]`
**Global variable:** `47 [uint16 SCRO-index]` (1-based index into SCRO list)
**Reference:** `72 [uint16 SCRO-index]` (for ref.Function or ref.variable access)
**Standalone ref:** `5A [uint16 SCRO-index]`

### 3.5 Function Calls Within Expressions

```
58                      — 'X' token
[funcOpcode:uint16]     — function opcode (e.g., 0x100E)
[paramBytes:uint16]     — byte count of params (includes paramCount)
[paramCount:uint16]     — number of parameters (omitted if paramBytes=0)
[parameters...]         — encoded parameter data
```

### 3.6 Operators in Expressions

Arithmetic and comparison operators are encoded as **literal ASCII character(s)**:

| Operator | Bytes      | Meaning          |
|----------|------------|------------------|
| `+`      | 0x2B       | Addition         |
| `-`      | 0x2D       | Subtraction      |
| `*`      | 0x2A       | Multiplication   |
| `/`      | 0x2F       | Division         |
| `%`      | 0x25       | Modulo           |
| `==`     | 0x3D 0x3D  | Equals           |
| `!=`     | 0x21 0x3D  | Not equals       |
| `<`      | 0x3C       | Less than        |
| `<=`     | 0x3C 0x3D  | Less or equal    |
| `>`      | 0x3E       | Greater than     |
| `>=`     | 0x3E 0x3D  | Greater or equal |
| `&&`     | 0x26 0x26  | Logical AND      |
| `\|\|`   | 0x7C 0x7C  | Logical OR       |
| `~`      | 0x7E       | Unary negation   |

**IMPORTANT**: The vanilla GECK engine also has a **numeric** operator encoding used by the internal evaluator (distinct from expression bytecode):

```cpp
enum ScriptOperatorCode {
    kOp_LeftBracket      = 0x0,
    kOp_RightBracket     = 0x1,
    kOp_LogicalAnd       = 0x2,
    kOp_LogicalOr        = 0x3,
    kOp_LessOrEqual      = 0x4,
    kOp_LessThan         = 0x5,
    kOp_GreaterOrEqual   = 0x6,
    kOp_GreaterThan      = 0x7,
    kOp_Equals           = 0x8,
    kOp_NotEquals        = 0x9,
    kOp_Minus            = 0xA,
    kOp_Plus             = 0xB,
    kOp_Multiply         = 0xC,
    kOp_Divide           = 0xD,
    kOp_Modulo           = 0xE,
    kOp_Tilde            = 0xF,  // negation / bitwise NOT
};
```

### 3.7 Expression Evaluation Example

Script: `set myFloat to player.GetAV Luck + 5`

Bytecode (conceptual):
```
15 00                   — Set opcode
[argLen:2]              — total arg bytes
66 [myFloat_idx:2]      — target: float variable
[exprLen:2]             — expression byte count
  72 [player_idx:2]     — push ref: player (SCRO index)
  58 0E 10 02 00 01 00  — call GetAV(Luck) on ref
    [Luck param]
  20                    — push separator
  6E 05 00 00 00        — push int constant 5
  20                    — push separator
  2B                    — operator: +
```

---

## 4. Base Game Function Opcodes (0x1000 — 0x13FF)

All Fallout NV base game functions live in the range 0x1000-0x13FF. Key functions:

### 4.1 Essential Functions

| Opcode | Function           | Short Name    | Params                           |
|--------|--------------------|---------------|----------------------------------|
| 0x100E | GetActorValue      | GetAV         | (ActorValue)                     |
| 0x100F | SetActorValue      | SetAV         | (ActorValue, Amount)             |
| 0x1010 | ModActorValue      | ModAV         | (ActorValue, Amount)             |
| 0x1115 | GetBaseActorValue  | GetBaseAV     | (ActorValue)                     |
| 0x110E | ForceActorValue    | ForceAV       | (ActorValue, Amount)             |
| 0x1181 | DamageActorValue   | DamageAV      | (ActorValue, Amount)             |
| 0x1182 | RestoreActorValue  | RestoreAV     | (ActorValue, Amount)             |
| 0x11EF | GetPermanentAV     | GetPermAV     | (ActorValue)                     |
| 0x10B6 | GetEquipped        |               | (ObjectID)                       |
| 0x10EE | EquipItem          | EquipObject   | (ObjectID, [Flag], [MsgFlag])    |
| 0x10EF | UnequipItem        | UnEquipObject | (ObjectID, [Flag], [MsgFlag])    |
| 0x1001 | GetDistance         |               | (ObjectRefID)                    |
| 0x1002 | AddItem            |               | (ObjectID, Count, [Flag])        |
| 0x1052 | RemoveItem         |               | (ObjectID, Count, [Flag])        |
| 0x102F | GetItemCount       |               | (ObjectID)                       |
| 0x100D | Activate           |               | ([ObjectRefID], [Int])           |
| 0x1021 | Enable             |               | ([Int])                          |
| 0x1022 | Disable            |               | ([Int])                          |
| 0x1025 | PlaceAtMe          |               | (ObjectID, [Count], [Dist], [Dir]) |
| 0x102E | GetDead            |               | —                                |
| 0x1039 | SetStage           |               | (Quest, Stage)                   |
| 0x103A | GetStage           |               | (Quest)                          |
| 0x1036 | StartQuest         |               | (Quest)                          |
| 0x1037 | StopQuest          |               | (Quest)                          |
| 0x1038 | GetQuestRunning    |               | (Quest)                          |
| 0x1176 | AddPerk            |               | (Perk, [Alt])                    |
| 0x11A8 | RemovePerk         |               | (Perk, [Alt])                    |
| 0x11C1 | HasPerk            |               | (Perk, [Alt])                    |
| 0x1174 | IsInList           |               | (FormList)                       |
| 0x100C | GetSecondsPassed   |               | —                                |
| 0x1050 | GetLevel           |               | —                                |
| 0x1006 | GetPos             |               | (Axis)                           |
| 0x1007 | SetPos             |               | (Axis, Float)                    |
| 0x1008 | GetAngle           |               | (Axis)                           |
| 0x1009 | SetAngle           |               | (Axis, Float)                    |
| 0x116B | GetLinkedRef       |               | —                                |
| 0x1088 | GetIsReference     |               | (ObjectRefID)                    |
| 0x1048 | GetIsID            |               | (ObjectID)                       |
| 0x109E | MoveToMarker       |               | (ObjectRefID, [X], [Y], [Z])    |
| 0x108B | KillActor          |               | ([Actor], [Int], [Int])          |
| 0x1033 | Say                |               | (Topic, [Int], [ActorBase], ...) |
| 0x1034 | SayTo              |               | (Actor, Topic, [Int], [Int])     |
| 0x11BB | MarkForDelete      |               | —                                |
| 0x1059 | ShowMessage        |               | (Message)                        |
| 0x11AF | GetHealthPercentage|               | —                                |
| 0x1121 | IsInCombat         |               | —                                |
| 0x112C | IsInInterior       |               | —                                |
| 0x1136 | GetInWorldspace    |               | (WorldSpace)                     |

### 4.2 Full Opcode Range Reference

The complete base game opcode range (0x1000-0x1214, ~533 functions) is documented at:
https://mod.gib.me/fonv/functions.html

Notable ranges:
- 0x1000-0x10FF: Core functions (movement, combat, items, AI, factions)
- 0x1100-0x11FF: Extended functions (AV manipulation, cells, quests, VATS)
- 0x1200-0x1214: New Vegas additions (karma, radio, destruction, alignment)

---

## 5. NVSE Opcode Ranges

NVSE functions start at opcode 0x1400. Commands are registered sequentially.

| Range           | Owner                    | Count |
|-----------------|--------------------------|-------|
| 0x0000 - 0x13FF | Base Game (Fallout NV)  | 5120  |
| 0x1400 - 0x1FFF | NVSE Core              | 3072  |
| 0x2200 - 0x2FFF | JIP LN NVSE            | 4096  |
| 0x3100 - 0x35FF | JohnnyGuitar NVSE      | 1280  |
| 0x2125 - 0x212D | Project Nevada         | 9     |
| 0x2132 - 0x213F | lStewieAl              | 14    |
| 0x21C0 - 0x21C8 | MCM                    | 9     |
| 0x3800 - 0x38FF | TTW                    | 256   |
| 0x3961 - 0x3A66 | SUP NVSE               | 261   |
| 0x3C93 - 0x3D74 | ShowOff NVSE           | 226   |
| 0x3DFF - 0x3EFF | ppNVSE                 | 256   |

### 5.1 Key NVSE Functions

NVSE commands are assigned sequentially from 0x1400 via `CommandTable::Add()`. The exact opcode for a specific function depends on registration order. Key NVSE functions include:

- **Let** — NVSE expression-aware assignment (replaces Set for NVSE expressions)
- **Eval** — Evaluate an NVSE expression
- **TestExpr** — Test an expression (for conditions)
- **GetEquippedObject** (GetEqObj) — Returns base form of item in equipment slot
- **ar_List, ar_Map, ar_Construct** — Array creation
- **ToString, TypeOf** — Type introspection
- **While, Loop, Break, Continue** — Loop control
- **Call, SetFunctionValue** — User-defined functions

### 5.2 NVSE Expression Compilation

When NVSE encounters `Let`, `Eval`, `TestExpr`, or NVSE-aware commands, it uses its **own compiler** (not the GECK's). NVSE expressions compile to a different token format:

The NVSE expression evaluator uses `0xFFFF` as a marker indicating inline NVSE expression tokens follow. The token stream uses the `Token_Type` enum:

```cpp
enum Token_Type {
    kTokenType_Number      = 0,
    kTokenType_Boolean     = 1,
    kTokenType_String      = 2,
    kTokenType_Form        = 3,
    kTokenType_Ref         = 4,
    kTokenType_Global      = 5,
    kTokenType_Array       = 6,
    kTokenType_ArrayElement= 7,
    kTokenType_Slice       = 8,
    kTokenType_Command     = 9,
    kTokenType_Variable    = 10,
    kTokenType_NumericVar  = 11,
    kTokenType_RefVar      = 12,
    kTokenType_StringVar   = 13,
    kTokenType_ArrayVar    = 14,
    kTokenType_Ambiguous   = 15,
    kTokenType_Operator    = 16,
    kTokenType_ForEachContext = 17,
    kTokenType_Byte        = 18,
    kTokenType_Short       = 19,
    kTokenType_Int         = 20,
    kTokenType_Pair        = 21,
    kTokenType_Lambda      = 22,
    kTokenType_Invalid     = 28,
};
```

NVSE operator types:
```cpp
enum OperatorType {
    kOpType_Assignment     = 0,   // :=
    kOpType_LogicalOr      = 1,   // ||
    kOpType_LogicalAnd     = 2,   // &&
    kOpType_Slice          = 3,   // [x:y]
    kOpType_Equals         = 4,   // ==
    kOpType_NotEqual       = 5,   // !=
    kOpType_GreaterThan    = 6,   // >
    kOpType_LessThan       = 7,   // <
    kOpType_GreaterOrEqual = 8,   // >=
    kOpType_LessOrEqual    = 9,   // <=
    kOpType_BitwiseOr      = 10,  // |
    kOpType_BitwiseAnd     = 11,  // &
    kOpType_LeftShift      = 12,  // <<
    kOpType_RightShift     = 13,  // >>
    kOpType_Add            = 14,  // +
    kOpType_Subtract       = 15,  // -
    kOpType_Multiply       = 16,  // *
    kOpType_Divide         = 17,  // /
    kOpType_Modulo         = 18,  // %
    kOpType_Exponent       = 19,  // ^
    kOpType_Negation       = 20,  // - (unary)
    kOpType_LogicalNot     = 21,  // !
    kOpType_LeftParen      = 22,
    kOpType_RightParen     = 23,
    kOpType_LeftBracket    = 24,
    kOpType_RightBracket   = 25,
    kOpType_In             = 26,  // <-
    kOpType_ToString       = 27,  // $
    kOpType_ToNumber       = 28,  // #
    kOpType_PlusEquals     = 29,  // +=
    kOpType_MinusEquals    = 30,  // -=
    kOpType_Dereference    = 31,  // *
    kOpType_MemberAccess   = 32,  // ->
    kOpType_MakePair       = 33,  // ::
    kOpType_Box            = 34,  // &
};
```

---

## 6. Actor Value Indices

Used as parameters for GetAV/SetAV/ModAV etc.

| Index | Actor Value        |
|-------|--------------------|
| 0     | Aggression         |
| 1     | Confidence         |
| 2     | Energy             |
| 3     | Responsibility     |
| 4     | Mood               |
| 5     | Strength (ST)      |
| 6     | Perception (PE)    |
| 7     | Endurance (EN)     |
| 8     | Charisma (CH)      |
| 9     | Intelligence (IN)  |
| 10    | Agility (AG)       |
| 11    | Luck (LK)          |
| 12    | ActionPoints       |
| 13    | CarryWeight        |
| 14    | CritChance         |
| 15    | HealRate           |
| 16    | Health             |
| 17    | MeleeDamage        |
| 18    | DamageResist       |
| 19    | PoisonResist       |
| 20    | RadResist          |
| 21    | SpeedMult          |
| 22    | Fatigue            |
| 23    | Karma              |
| 24    | XP                 |
| 25    | PerceptionCondition (Head) |
| 26    | EnduranceCondition (Torso) |
| 27    | LeftAttackCondition (LArm) |
| 28    | RightAttackCondition (RArm) |
| 29    | LeftMobilityCondition (LLeg) |
| 30    | RightMobilityCondition (RLeg) |
| 31    | BrainCondition     |
| 32    | Barter             |
| 33    | BigGuns            |
| 34    | EnergyWeapons      |
| 35    | Explosives         |
| 36    | Lockpick           |
| 37    | Medicine           |
| 38    | MeleeWeapons       |
| 39    | Repair             |
| 40    | Science            |
| 41    | Guns (SmallGuns)   |
| 42    | Sneak              |
| 43    | Speech             |
| 44    | Survival           |
| 45    | Unarmed            |

---

## 7. Parameter Type IDs

From `ParamType` enum in CommandTable.h. Used in `ParamInfo` to describe expected argument types:

| ID   | Type              |
|------|-------------------|
| 0x00 | String            |
| 0x01 | Integer           |
| 0x02 | Float             |
| 0x03 | ObjectID          |
| 0x04 | ObjectRef         |
| 0x05 | ActorValue        |
| 0x06 | Actor             |
| 0x07 | SpellItem         |
| 0x08 | Axis              |
| 0x09 | Cell              |
| 0x0A | AnimGroup         |
| 0x0B | MagicItem         |
| 0x0C | Sound             |
| 0x0D | Topic             |
| 0x0E | Quest             |
| 0x0F | Race              |
| 0x10 | Class             |
| 0x11 | Faction           |
| 0x12 | Sex               |
| 0x13 | Global            |
| 0x14 | Furniture         |
| 0x15 | TESObject         |
| 0x18 | MapMarker         |
| 0x19 | ActorBase         |
| 0x1A | Container         |
| 0x1B | WorldSpace        |
| 0x1C | CrimeType         |
| 0x1D | Package           |
| 0x1E | CombatStyle       |
| 0x1F | MagicEffect       |
| 0x20 | FormType          |
| 0x21 | WeatherID         |
| 0x23 | Owner             |
| 0x24 | EffectShader       |
| 0x25 | FormList          |
| 0x27 | Perk              |
| 0x28 | Note              |
| 0x29 | MiscellaneousStat |
| 0x2A | ImageSpaceMod     |
| 0x2B | ImageSpace        |
| 0x2E | EncounterZone     |
| 0x30 | Message           |
| 0x31 | InvObjectOrFormList |
| 0x32 | Alignment         |
| 0x33 | EquipType         |
| 0x34 | ObjectOrFormList  |
| 0x35 | Music             |
| 0x36 | CriticalStage     |

---

## 8. Compilation Pipeline Summary

### 8.1 ScriptBuffer (xNVSE)

The compilation accumulates into a `ScriptBuffer` (0x58 bytes):
```cpp
struct ScriptBuffer {
    char*   scriptText;      // 0x00 — source text pointer
    UInt32  textOffset;      // 0x04 — current parse position
    UInt8   runtimeMode;     // 0x08
    String  scriptName;      // 0x0C
    UInt8*  scriptData;      // 0x20 — output buffer (0x4000 bytes)
    UInt32  dataOffset;      // 0x24 — current write position
    ScriptInfo info;         // 0x28 — accumulating header
    VarInfoList vars;        // 0x3C — variable definitions
    RefList refVars;         // 0x44 — reference list (becomes SCRO)
    tList<ScriptLineBuffer> lines; // 0x50
};
```

### 8.2 ScriptLineBuffer

Each line compiles via low-level write methods:
- `Write16(uint16)` — write 2-byte LE value
- `Write32(uint32)` — write 4-byte LE value
- `WriteByte(uint8)` — write single byte
- `WriteFloat(double)` — write 8-byte double
- `WriteString(len, chars)` — write uint16 length prefix + chars

### 8.3 Steps to Compile

1. Parse `ScriptName` line -> emit `1D 00 04 00 00 00 00 00`
2. Parse variable declarations -> emit `12/13/14/1F 00` + name data, populate varList
3. For each `Begin` block:
   a. Emit `10 00 [argLen] [paramCount] [eventOpcode] [placeholder blockLen]`
   b. Compile all statements inside the block
   c. Patch `blockLen` with actual byte count
   d. Emit `11 00 00 00` (End)
4. For each statement inside a block:
   - Function calls: resolve opcode from CommandTable, emit `[opcode:2] [argLen:2] [params...]`
   - Set statements: emit `15 00`, encode target variable, compile expression to RPN
   - If/ElseIf: emit `16 00`/`18 00`, compile expression, store jump placeholder, patch later
   - Else: emit `17 00 02 00 [jumpOps]`
   - Return: emit `1E 00 00 00`
5. Build SCHR from accumulated info
6. Collect SCRO from refList, SLSD+SCVR from varList

### 8.4 Reference Resolution

When a script references `player`, a quest, a form, etc:
1. Add the FormID to the script's refList (if not already present)
2. Record its 1-based index
3. In bytecode, use `72 [index:2]` or `1C 00 [index:2]` to reference it

Player is always FormID `0x00000014`.

---

## 9. Sources

- [fopdoc: FalloutNV Script Subrecord](https://github.com/TES5Edit/fopdoc/blob/master/FalloutNV/Records/Subrecords/Script.md)
- [fopdoc: SCHR Subrecord](https://github.com/TES5Edit/fopdoc/blob/master/FalloutNV/Records/Subrecords/SCHR.md)
- [UESP: Oblivion SCPT Format](https://en.uesp.net/wiki/Oblivion_Mod:Mod_File_Format/SCPT) — same bytecode engine as FNV
- [UESP: Oblivion Function Indices](https://en.uesp.net/wiki/Oblivion_Mod:Function_Indices)
- [xNVSE Source: GameScript.h](https://github.com/xNVSE/NVSE/blob/master/nvse/nvse/GameScript.h)
- [xNVSE Source: ScriptAnalyzer.h](https://github.com/xNVSE/NVSE/blob/master/nvse/nvse/ScriptAnalyzer.h)
- [xNVSE Source: ScriptTokens.h](https://github.com/xNVSE/NVSE/blob/master/nvse/nvse/ScriptTokens.h)
- [xNVSE Source: CommandTable.h](https://github.com/xNVSE/NVSE/blob/master/nvse/nvse/CommandTable.h)
- [GECK Wiki: NVSE Opcode Base](https://geckwiki.com/index.php/NVSE_Opcode_Base)
- [GECK Wiki: NVSE Expressions](https://geckwiki.com/index.php/NVSE_Expressions)
- [FNV Functions: mod.gib.me](https://mod.gib.me/fonv/functions.html)
- [GECK Wiki: NVSE Functions Category](https://geckwiki.com/index.php/Category:Functions_(NVSE))
- [JIP LN NVSE: GitHub](https://github.com/jazzisparis/JIP-LN-NVSE)
- [GECK Wiki: JIP Functions Category](https://geckwiki.com/index.php/Category:Functions_(JIP))
