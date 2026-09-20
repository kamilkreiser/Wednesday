#!/usr/bin/env python3
"""check_undefined_names.py — flag module-level names that are USED but never BOUND.

WHY THIS EXISTS (2026-09-20, Tuesday): patching `reconcile_rulings.py` I added
`os.environ.get(...)` to a module whose imports read `import json, re, subprocess, sys`.
I "verified" it with `ast.parse`, which printed **syntax OK on a module that could not
load**. `python3 -m py_compile` does the same — measured on the same file. A syntax
check cannot fail on a missing name, so it is a check that could not have caught the
defect it was run against. Running the tool caught it one command later; this file is
that catch turned into something that does not depend on me remembering.

It uses Python's own `symtable`, not a hand-rolled scope walker: the interpreter's
symbol table already knows what a module binds, and re-implementing scoping rules is
how a second implementation disagrees with the first.

LIMIT, stated rather than discovered: this checks the MODULE's top-level scope only.
A name used inside a function and bound nowhere is a runtime error this will not see.
That is the narrower claim, and it is the claim that matches the defect it was built
from.

Usage: check_undefined_names.py <file.py> [more.py ...]
Exit:  0 all clean · 1 at least one undefined name · 2 usage / unreadable / unparsable
"""
import builtins
import io
import symtable
import sys

BUILTINS = set(dir(builtins)) | {"__file__", "__name__", "__doc__", "__spec__",
                                 "__package__", "__loader__", "__builtins__"}


def undefined_in(path):
    """Return a sorted list of module-scope names referenced but never assigned."""
    src = io.open(path, encoding="utf-8").read()
    table = symtable.symtable(src, path, "exec")
    out = []
    for sym in table.get_symbols():
        name = sym.get_name()
        if name in BUILTINS:
            continue
        # Referenced at module scope and bound nowhere in it (not imported, not
        # assigned, not a def/class). symtable already folds in `global` decls.
        if sym.is_referenced() and not sym.is_assigned() and not sym.is_imported():
            # A name only ever *declared* global in a nested scope shows here too;
            # requiring is_referenced() keeps it to names actually read.
            out.append(name)
    return sorted(set(out))


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(__doc__.strip().splitlines()[-2] + "\n")
        return 2
    bad = 0
    for path in argv[1:]:
        try:
            names = undefined_in(path)
        except SyntaxError as e:
            sys.stderr.write(f"UNPARSABLE {path}: {e}\n")
            return 2
        except OSError as e:
            sys.stderr.write(f"UNREADABLE {path}: {e}\n")
            return 2
        if names:
            bad += 1
            print(f"UNDEFINED {path}: {', '.join(names)}")
    if bad:
        print(f"-- {bad} file(s) reference a module-scope name they never bind")
        return 1
    print(f"ok: {len(argv) - 1} file(s), no undefined module-scope names")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
