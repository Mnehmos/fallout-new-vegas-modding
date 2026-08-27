# Ghidra postScript: decompile specific target functions to .c files.
# Args: <out_dir> <addr1> [addr2 ...]  (addresses via import_ghidra.py, read
# from decompile_targets.txt). Jython 2.7 compatible.
import os

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

args = getScriptArgs()
out_dir = os.path.join(args[0], "decompiled")
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)
targets = args[1:]

if not targets:
    print("decompile_targets: no target addresses supplied")
else:
    di = DecompInterface()
    monitor = ConsoleTaskMonitor()
    di.openProgram(currentProgram)

    af = currentProgram.getAddressFactory().getDefaultAddressSpace()
    fm = currentProgram.getFunctionManager()
    done = 0
    for a in targets:
        try:
            addr = af.getAddress(a)
        except Exception:
            print("bad address: %s" % a)
            continue
        fn = fm.getFunctionContaining(addr)
        if fn is None:
            fn = fm.getFunctionAt(addr)
        if fn is None:
            print("no function containing %s" % a)
            continue
        res = di.decompileFunction(fn, 180, monitor)
        if res.decompileCompleted():
            entry = fn.getEntryPoint()
            fname = "%s_%s.c" % (fn.getName().replace("`", "").replace("@", "_").replace(":", "_"),
                                 ("%08x" % entry.getOffset()))
            path = os.path.join(out_dir, fname)
            fh = open(path, "w")
            fh.write(res.getDecompiledFunction().getC())
            fh.close()
            print("decompiled %s (fn %s @ 0x%08x) -> %s" % (a, fn.getName(), entry.getOffset(), path))
            done += 1
        else:
            print("FAILED %s: %s" % (a, res.getErrorMessage()))
    print("decompile_targets: %d/%d completed" % (done, len(targets)))
