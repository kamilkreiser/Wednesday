#!/usr/bin/env python3
"""Seat R 44th -- ORD / SEAT_DATE / suffix arms for the ra43 -> ra44 port (RULING f).
AUTHORED, not ported (port_ra44.py SKIP_FILES names ord_arms_ra43.py so the port cannot regenerate it).
usage: REC=<your record folder> BOOT=<YOUR REAL BOOT DATE> python3 -B ord_arms_ra44.py [path/to/port.py]
exit 0 only if every behaviour, absence and control line holds."""
import importlib.util, os, re, sys
REC, BOOT = os.environ["REC"], os.environ["BOOT"]
PORT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REC, "_item0_proofs", "port_ra44.py")
spec = importlib.util.spec_from_file_location("p44", PORT)
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
OWN = 43                                   # the SOURCE generation make_shift is called with
def safe(f, *a):
    try: return f(*a)
    except Exception as e: return ("EXC", repr(e))
shift, mp = p.make_shift(OWN, 1)
print("shift map:", mp)
B = []                                     # behaviour arms: (label, input, must, mustnot)
B += [("own      R 43rd -> R 44th",  "Seat R 43rd",            ["R 44th"], ["R 43rd", "R 44rd"]),
      ("succ     R 44th -> R 45th",  "Seat R 44th",            ["R 45th"], ["R 44th"]),
      ("pred     R 42nd -> R 43rd",  "Seat R 42nd",            ["R 43rd"], ["R 42nd", "R 43nd"]),
      ("token    ra43 -> ra44",      "tools/watch_ra43.py",    ["watch_ra44.py"], ["ra43"]),
      ("archive  copy_rec40 stays",  "copy_rec40/x",           ["copy_rec40"], ["copy_rec41"]),
      ("REC      REC43 -> REC44",    "REC43 is read-only",     ["REC44"], ["REC43"]),
      ("REC      REC42 -> REC43",    "REC42/tools",            ["REC43"], ["REC42"]),
      ("folder   seatR-43rd + date", "2026-10-12_seatR-43rd",  ["%s_seatR-44th" % BOOT], ["seatR-43rd", "seatR-44rd"]),
      ("folder   forward seatR-44th","2026-10-12_seatR-44th",  ["seatR-45th"], ["seatR-44th"]),
      ("ns       seatra43",          "--my-ref-ns seatra43",   ["seatra44"], ["seatra43"]),
      ("worktree s-ra43-m1455",      "worktrees/s-ra43-m1455", ["s-ra44-m1455"], ["s-ra43-"]),
      ("GO clause",                  "GO (Seat R 43rd): merge 1455 on gate86", ["GO (Seat R 44th): merge 1455 on gate86"], ["R 43rd"]),
      ("merge_note",                 "Merged by Seat R 43rd on the authority of", ["Merged by Seat R 44th on the authority of"], ["R 43rd"]),
      ("watcher  MINE_ORD",          'MINE_ORD="(Seat R 43rd)"', ['MINE_ORD="(Seat R 44th)"'], ["R 43rd"]),
      ("out-of-window copy_rec37",   "copy_rec37/tools",       ["copy_rec37"], ["copy_rec38"]),
      ("out-of-window R 33rd",       "R 33rd's literals",      ["R 33rd"], ["R 34th"])]
bad = 0
for lab, src, must, mustnot in B:
    got, n = shift(src)
    ok = all(m in got for m in must) and all(x not in got for x in mustnot)
    bad += (not ok)
    print("  %s  %-30s %r -> %r" % ("PASS" if ok else "FAIL", lab, src, got))
print("BEHAVIOUR ARMS: %d/%d passed" % (len(B) - bad, len(B)))
# ABSENCE arms: each broken form of the digit-only-shift bug class must be ABSENT from the output
ABS = [("Seat R 43rd", "R 44rd"), ("Seat R 42nd", "R 43nd"), ("Seat R 44th", "R 45rd"),
       ("seatR-43rd", "seatR-44rd"), ("ra43", "ra44th"), ("Seat R 41st", "R 42st")]
abad = 0
for src, broken in ABS:
    got, _ = shift(src); ok = broken not in got; abad += (not ok)
    print("  %s  %-12s -> %-12s %r ABSENT=%s" % ("PASS" if ok else "FAIL", src, got, broken, ok))
print("ABSENCE ARMS: %d/%d passed" % (len(ABS) - abad, len(ABS)))
# CONTROLS: each of these MUST read True on a correct port; a False is a REAL fault (or a dead arm)
src_txt = open(PORT, encoding="utf-8").read()
ghost, _ = shift("Seat R 43rd")
C = [("C1 inverted-want: the OLD ordinal must be GONE (reads True only if 'R 43rd' is absent)", "R 43rd" not in ghost),
     ("C2 ORD has every key make_shift(43,1) demands (43,44,45)", all(k in p.ORD for k in ("43", "44", "45"))),
     ("C3 SEAT_DATE['44'] == YOUR real boot date", p.SEAT_DATE.get("44") == BOOT),
     ("C4 the :55 date class reaches 44 (a wrong source date is CORRECTED)", shift("2026-10-11_seatR-43rd")[0] == "%s_seatR-44th" % BOOT),
     ("C5 the :55 class is 4[0-4] and the stale 4[0-3] is GONE", "4[0-4])(th|st|nd|rd)" in src_txt and "4[0-3])(th|st|nd|rd)" not in src_txt),
     ("C6 make_shift(44,1) (your successor's) does not KeyError", safe(lambda: p.make_shift(44, 1)[0]("Seat R 45th"))[0] != "EXC"),
     ("C7 SKIP_FILES names the two authored files", "ord_arms_ra43.py" in src_txt and "fix_sweep_ra43.py" in src_txt)]
cbad = 0
for lab, v in C:
    cbad += (v is not True); print("  %s  %s -> %s" % ("PASS" if v is True else "FAIL", lab, v))
print("CONTROLS: %d/%d passed" % (len(C) - cbad, len(C)))
tot = len(B) + len(ABS) + len(C); fails = bad + abad + cbad
print("VERDICT: %s  (%d behaviour + %d absence + %d controls = %d lines, %d failed)" %
      ("ALL PASS" if not fails else "FAILED", len(B), len(ABS), len(C), tot, fails))
sys.exit(1 if fails else 0)
