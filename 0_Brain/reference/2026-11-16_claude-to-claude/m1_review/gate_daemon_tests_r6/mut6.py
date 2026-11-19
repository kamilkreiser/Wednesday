#!/usr/bin/env python3
"""Gate r6 mutation driver: plant ONE mutant at a time in recovery.rs of the given clone, run the
named tests, restore the file byte for byte. Usage: mut6.py <clone> <mutant id> -- <cargo test args...>
Prints MUTANT <id> APPLIED / RESTORED and the test exit code."""
import pathlib
import subprocess
import sys

MUTANTS = {
    # Row 54's clock at twice T-RTO's value (deadline and tick alike).
    "M1": [
        ("            d.push(t + self.cfg.rto);\n", "            d.push(t + self.cfg.rto * 2);\n"),
        (".map(|t| now.duration_since(t) > self.cfg.rto)", ".map(|t| now.duration_since(t) > self.cfg.rto * 2)"),
    ],
    # The deadline is armed but the tick never fires the RESYNC.
    "M2": [
        ("if attached && self.skips_stuck(now) {", "if attached && self.skips_stuck(now) && cfg!(any()) {"),
    ],
    # R5-2's clear removed (desync stays after a missing tail).
    "M3": [
        ("        // step again (addendum 12, R5-2).\n        if self.next_out >= self.ob.send_next {",
         "        // step again (addendum 12, R5-2).\n        if self.next_out >= self.ob.send_next && cfg!(any()) {"),
    ],
    # A forward acknowledgement refills the budget but leaves the clock running.
    "M4": [
        ("            self.skips_left = self.cfg.max_skips;\n            self.skips_spent_at = None;\n        }\n        if m.seq == 0",
         "            self.skips_left = self.cfg.max_skips;\n        }\n        if m.seq == 0"),
    ],
}


def main():
    clone = pathlib.Path(sys.argv[1])
    mid = sys.argv[2]
    args = sys.argv[sys.argv.index("--") + 1:]
    f = clone / "crates/coagent-daemon/src/recovery.rs"
    orig = f.read_bytes()
    src = orig.decode()
    for old, new in MUTANTS[mid]:
        n = src.count(old)
        if n != 1:
            print(f"MUTANT {mid}: text occurs {n} times, not applied")
            sys.exit(2)
        src = src.replace(old, new)
    f.write_text(src)
    print(f"MUTANT {mid} APPLIED", flush=True)
    try:
        rc = subprocess.call(args, cwd=clone)
    finally:
        f.write_bytes(orig)
        print(f"MUTANT {mid} RESTORED", flush=True)
    print(f"MUTANT {mid} test exit {rc}")


if __name__ == "__main__":
    main()
