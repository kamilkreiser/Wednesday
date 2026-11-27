#!/usr/bin/env python3
# A5_inject.py — FAULT INJECTION driver (checker's instrument, not the tool): imports the scratch copy's nb_core and
# delivers a signal to the run at a chosen point AFTER the accounting.  usage: A5_inject.py <lane> <point> <sig> -- <nb_core args>
import os, signal, sys
lane, point, sig = sys.argv[1], sys.argv[2], getattr(signal, sys.argv[3])
sys.path.insert(0, lane); import nb_core
fired = {"n": 0}
if point == "manifest":            # while the local manifest is being written (good already computed, nothing recorded yet)
    real = nb_core.json.dump
    def dump(obj, fh, **kw):
        if isinstance(obj, dict) and "good" in obj and not fired["n"]:
            fired["n"] = 1; os.kill(os.getpid(), sig)
        return real(obj, fh, **kw)
    nb_core.json.dump = dump
elif point == "after_complete":    # after the COMPLETE marker is on the NAS, before the state says good
    real = nb_core.Ctx.note_attempt
    def note(self, status, reason, extra=None):
        if status == "good" and not fired["n"]:
            fired["n"] = 1; os.kill(os.getpid(), sig)
        return real(self, status, reason, extra)
    nb_core.Ctx.note_attempt = note
sys.exit(nb_core.main(sys.argv[sys.argv.index("--") + 1:]))
