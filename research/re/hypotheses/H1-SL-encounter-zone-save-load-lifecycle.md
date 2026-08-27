# H1-SL: Encounter-zone save/load lifecycle

**Status:** static reconstruction complete, runtime verification pending
**Parent:** H1 split from `H1-encounter-spawn-resolution.md`
**Scope:** persistence, form rebinding, and missing-zone cleanup for the
`ExtraEncounterZone` save/load object.
**Explicit boundary:** this slice does not validate encounter selection,
leveled-list evaluation, actor level selection, or spawning.

## Recovered chain

```text
serialized zone identifier
  -> 0x00428150 ExtraDataList::LoadGame (void)
     -> extra-data type 0x74
     -> 0x00432E60 construct/reuse ExtraEncounterZone
        (0x74 bytes, vtable 0x01015C54)
     -> 0x0040FF60 BaseExtraList::AddExtra candidate
     -> 0x008648A0 load-buffer/form-ID path candidate
     -> 0x004839C0 opaque form/handle lookup helper
     -> RTDynamicCast, TESForm descriptor 0x01183028
        -> BGSEncounterZone descriptor 0x011840DC
     -> store result at ExtraEncounterZone +0x0C
     -> 0x00416BE0 rebinds the saved identifier
        -> missing zone: log and remove the extra-data object
```

The two direct parents of `0x00428150` are:

- `0x005623D0` (`TESObjectREFR::LoadGame` candidate), called at `0x005624AB`;
- `0x004BEE00`, an unresolved bound-object/nested extra-data load context,
  called at `0x004BEF31`.

The exported GOG call graph records those edges. It omits some helper calls
visible in the decompiler's `case 0x74` body, so that export/decompiler
contradiction is retained rather than silently normalized.

## Evidence

- [`0x00428150` decompilation](../decompiled/FUN_00428150_00428150.c): the
  self-identifying `ExtraDataList::LoadGame` error string, the type-code loop,
  and the `0x74` branch.
- [`0x00432E60` constructor](../decompiled/FUN_00432E60_00432E60.c) and
  [`0x00432E90` comparator candidate](../decompiled/FUN_00432E90_00432E90.c):
  the `ExtraEncounterZone` object surface and its `+0x0C` comparison slot.
- [`0x00416BE0` rebind path](../decompiled/FUN_00416BE0_00416BE0.c): the
  successful cast/write and the existing missing-zone removal message.
- [`calls.json`](../calls.json): direct caller/callee evidence.
- [`symbols.json`](../symbols.json): policy-capped symbol entries. Atlas names
  remain candidate mappings, and `0x004839C0` remains intentionally unnamed.
- `fnvedit`: form-type ordinal 98 is `ECZN`; the current configured master
  reports 17 ECZN records, but its editor IDs mix FNV-looking and Fallout
  3-like names and expose no DATA bytes. That record-source contradiction is
  not treated as runtime proof.

## Runtime verification

Use the Steam executable only after confirming GOG-to-Steam function matching;
the Steam image is CEG-wrapped. Use module RVAs rather than assuming the
plaintext GOG virtual addresses are directly valid:

| Static VA | RVA | Observation |
|---|---:|---|
| `0x00428150` | `0x00028150` | extra-data load and type `0x74` branch |
| `0x00416BE0` | `0x00016BE0` | rebind and remove-on-failure path |
| `0x008648A0` | `0x004648A0` | serialized form-ID/load-buffer path candidate |

1. Load a save that naturally contains an `ExtraEncounterZone` entry. Log the
   buffer argument, serialized identifier, lookup result, cast result, and
   `ExtraEncounterZone +0x0C` after the write.
2. Repeat with the referenced ECZN unavailable, or apply a debugger-only
   conditional manipulation that makes this lookup/cast null. Do not modify
   the installed master for the baseline.
3. Predicted results: an available ECZN leaves a non-null zone pointer in
   `+0x0C`; an unavailable ECZN reaches the existing `0x00416BE0` cleanup
   message and removes the extra-data object.

A passing pair promotes only the H1-SL persistence/rebinding claims. It does
not promote any spawning claim. If no natural save reaches type `0x74`, stop
and record that coverage gap.

## Close condition

Close H1-SL only after the available/missing pair is observed at runtime. The
historical, detailed investigation ledger is retained in
[`H1-encounter-spawn-resolution.md`](H1-encounter-spawn-resolution.md).
