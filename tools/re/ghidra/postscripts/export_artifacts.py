# Ghidra headless postScript: export analysis artifacts for the RE knowledge base.
# Runs inside Ghidra's Jython after auto-analysis. Receives one arg: the output
# directory (research/re/). Emits:
#   functions.json - entry, name, namespace, size, signature text
#   calls.json     - caller -> callee edges (direct + thunked imports)
#   strings.json   - defined strings with VAs
# Jython 2.7: keep syntax compatible (no f-strings).
import json
import os

from ghidra.program.model.symbol import RefType

out_dir = getScriptArgs()[0]
prog = currentProgram
fm = prog.getFunctionManager()
af = prog.getAddressFactory().getDefaultAddressSpace()

functions = []
for f in fm.getFunctions(True):
    body = f.getBody()
    try:
        sig_text = f.getSignature(False)
        sig_text = sig_text.getFullSignature() if hasattr(sig_text, "getFullSignature") else str(sig_text)
    except Exception:
        sig_text = ""
    functions.append({
        "entry": "0x%08X" % f.getEntryPoint().getOffset(),
        "name": f.getName(),
        "namespace": f.getParentNamespace().getName(),
        "size": body.getNumAddresses(),
        "signature": sig_text,
        "thunk": f.isThunk(),
    })

calls = []
for f in fm.getFunctions(True):
    caller = f.getEntryPoint()
    try:
        called_set = f.getCalledFunctions(None)
    except Exception:
        called_set = []
    for called in called_set:
        calls.append({
            "caller": "0x%08X" % caller.getOffset(),
            "callee": "0x%08X" % called.getEntryPoint().getOffset(),
            "callee_name": called.getName(),
        })

strings = []
it = prog.getListing().getDefinedData(True)
for d in it:
    dt = d.getDataType().getName().lower()
    if "string" in dt or "char" in dt and d.getLength() > 3:
        try:
            val = d.getValue()
        except Exception:
            continue
        if isinstance(val, basestring) and len(val) >= 4:
            strings.append({
                "va": "0x%08X" % d.getAddress().getOffset(),
                "value": val,
                "type": dt,
            })

with open(os.path.join(out_dir, "functions.json"), "w") as fh:
    json.dump({"program": prog.getName(), "functions": functions}, fh, indent=1)
with open(os.path.join(out_dir, "calls.json"), "w") as fh:
    json.dump({"program": prog.getName(), "calls": calls}, fh, indent=1)
with open(os.path.join(out_dir, "strings.json"), "w") as fh:
    json.dump({"program": prog.getName(), "strings": strings}, fh, indent=1)

print("exported %d functions, %d call edges, %d strings to %s" % (len(functions), len(calls), len(strings), out_dir))
