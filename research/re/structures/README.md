# Reconstructed structures (`research/re/structures/`)

C-ish layouts recovered from disassembly, cross-checked against known sources
(xEdit ` BethStructs`, NVSE plugin SDKs, GECK wiki). One file per structure:

```
structures/
    tesobjectrefr.h.md
    encounterzone.h.md
    tescell.h.md
    ...
```

Each file records: field offsets with the evidence (which instructions
accessed them), struct size, inheritance chain, and whether offsets were
verified at runtime. Offsets are per binary version — note the exact exe md5
(an `inspect_pe.py --json` run) at the top of each file.
