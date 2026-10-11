#!/usr/bin/env python3
"""Seat R 44th -- derive port_ra44.py from port_ra43.py by COUNT-ASSERTED substitutions.
Model: R 43rd's _item0_proofs/mk_port_ra43.py (26 substitutions); this one has 24 (the two
'past rows' and 'past tickets' LIT edits are NOT made: 1455 / KS-1417 are THIS seat's own row, and
adding them would flag the row's own tokens as stale; R 45th adds them once 1455 has landed).
Every pattern is a RAW string. A wrong count refuses the WHOLE write; the output is ast.parse'd.
usage: mk_port_ra44.py <src port_ra43.py> <dst port_ra44.py> <YOUR REAL BOOT DATE, YYYY-MM-DD>"""
import sys, ast, re
src_p, dst_p, BOOT = sys.argv[1], sys.argv[2], sys.argv[3]
assert re.fullmatch(r"2026-10-\d\d", BOOT), "boot date must look like 2026-10-DD: %r" % BOOT
t = open(src_p, encoding="utf-8").read()
B = "@@BOOT@@"
EDITS = [
 # (label, old, new, expected count)
 ("docstring seat+gen",
  r"""Seat R 43rd -- port the tool set to generation 43""",
  r"""Seat R 44th -- port the tool set to generation 44""", 1),
 ("docstring source",
  r"""Sources are Seat R 42nd's OWN outputs (my copy_rec42/), shifted +1: own 42 -> 43; predecessor 41 -> 42;""",
  r"""Sources are Seat R 43rd's OWN outputs (my copy_rec43/), shifted +1: own 43 -> 44; predecessor 42 -> 43;""", 1),
 ("docstring forward-add",
  r"""forward-added 43 -> 44.""", r"""forward-added 44 -> 45.""", 1),
 ("docstring usage",
  r"""usage: port_ra43.py survey|write""", r"""usage: port_ra44.py survey|write""", 1),
 ("SEAT_DATE comment absent-key",
  r"""# my boot date is 2026-10-12 (AEDT; launched 2026-10-11T15:47:02Z = 02:47 AEDT). 44 is deliberately ABSENT so a""",
  r"""# my boot date is @@BOOT@@ (AEDT). 45 is deliberately ABSENT so a""", 1),
 ("SEAT_DATE comment mine",
  r"""# forward-added path keeps its source date. Key "43" is MINE and must exist (RULING f).""",
  r"""# forward-added path keeps its source date. Key "44" is MINE and must exist (RULING f).""", 1),
 ("SEAT_DATE add key 44 (your REAL boot date)",
  r""""42":"2026-10-12","43":"2026-10-12"}""",
  r""""42":"2026-10-12","43":"2026-10-12","44":"@@BOOT@@"}""", 1),
 ("ORD comment example",
  r"""# so "R 42nd" would become "R 43nd" -- the same class of bug R 41st measured at 88 sites""",
  r"""# so "R 43rd" would become "R 44rd" -- the same class of bug R 41st measured at 88 sites""", 1),
 ("ORD comment GO clause",
  r"""# M7_GO_CLAUSE (it must equal Wednesday's literal "GO (Seat R 43rd): ..."), the merge_note""",
  r"""# M7_GO_CLAUSE (it must equal Wednesday's literal "GO (Seat R 44th): ..."), the merge_note""", 1),
 ("ORD comment merge_note",
  r"""# regex "Merged by Seat R 43rd on the authority of ...", and M7_SEAT, which is written into""",
  r"""# regex "Merged by Seat R 44th on the authority of ...", and M7_SEAT, which is written into""", 1),
 ("ORD add 46 (44 and 45 are ALREADY there; 46 is your successor's make_shift(44,1))",
  r""""43":"rd","44":"th","45":"th"}""",
  r""""43":"rd","44":"th","45":"th","46":"th"}""", 1),
 ("date-fix class :55 (a digit shift cannot see it): 4[0-3] -> 4[0-4]",
  r"""s2 = re.sub(r"(2026-10-\d\d)_seatR-(3[5-9]|4[0-3])(th|st|nd|rd)",""",
  r"""s2 = re.sub(r"(2026-10-\d\d)_seatR-(3[5-9]|4[0-4])(th|st|nd|rd)",""", 1),
 ("SRC copy_rec43",
  r"""SRC = os.path.join(R, "copy_rec42")""",
  r"""SRC = os.path.join(R, "copy_rec43")""", 1),
 ("SKIP_FILES (adds the two AUTHORED arms files: the port must never regenerate them)",
  r"""SKIP_FILES = ("port_ra42.py", "mk_port_ra42.py")""",
  r"""SKIP_FILES = ("port_ra43.py", "mk_port_ra43.py", "ord_arms_ra43.py", "fix_sweep_ra43.py")""", 1),
 ("SKIP_FILES comment",
  r"""if fn in SKIP_FILES: continue   # I authored my own ra43 versions of these""",
  r"""if fn in SKIP_FILES: continue   # I authored my own ra44 versions of these""", 1),
 ("stage comment paths",
  r"""# DEST MIRRORS THE SOURCE LAYOUT: copy_rec42/ported/X -> stage/ported/X ; copy_rec42/tools/X -> stage/tools/X""",
  r"""# DEST MIRRORS THE SOURCE LAYOUT: copy_rec43/ported/X -> stage/ported/X ; copy_rec43/tools/X -> stage/tools/X""", 1),
 ("stage dir",
  r"""stage = os.path.join(R, "_stage_ra43")""",
  r"""stage = os.path.join(R, "_stage_ra44")""", 1),
 ("make_shift own",
  r"""shift, mp = make_shift(42, 1)""", r"""shift, mp = make_shift(43, 1)""", 1),
 ("shift map print",
  r"""print("shift map (own 42, k=+1): %s" % mp)""",
  r"""print("shift map (own 43, k=+1): %s" % mp)""", 1),
 ("LIT class comment bounds",
  r"""# NOTE the previous-generation classes must now cover ra42 as well (A41-plan:1):
# `3[0-9]` stops at 39, and `[34][0-9]` would ALSO match 43/44 (my own and my successor's)
# -- so the class is (?:3[0-9]|40|41|42), appended as the EXACT alternative. It fires on
# ra30..ra42 and NOT on ra43/ra44. The suffix of 42 is "nd", of 41 "st": all forms listed.""",
  r"""# NOTE the previous-generation classes must now cover ra43 as well (A41-plan:1):
# `3[0-9]` stops at 39, and `[34][0-9]` would ALSO match 44/45 (my own and my successor's)
# -- so the class is (?:3[0-9]|40|41|42|43), appended as the EXACT alternative. It fires on
# ra30..ra43 and NOT on ra44/ra45. The suffix of 43 is "rd", of 42 "nd", of 41 "st": all forms listed.""", 1),
 ("LIT ordinal<=N key+regex",
  r""" "ordinal<=42 (stale in code)": r"(?i)ra(?:3[0-9]|40|41|42)(?!\d)|[Rr] (?:3[0-9]|40)th|[Rr] 41st|[Rr] 42nd|seatR-(?:3[0-9]|40)th|seatR-41st|seatR-42nd",""",
  r""" "ordinal<=43 (stale in code)": r"(?i)ra(?:3[0-9]|40|41|42|43)(?!\d)|[Rr] (?:3[0-9]|40)th|[Rr] 41st|[Rr] 42nd|[Rr] 43rd|seatR-(?:3[0-9]|40)th|seatR-41st|seatR-42nd|seatR-43rd",""", 1),
 ("LIT previous seat",
  r""" "PREVIOUS SEAT ra42/R 42nd (the gate)": r"(?i)\bra42\b|[Rr] 42nd|seatra42|s-ra42-",""",
  r""" "PREVIOUS SEAT ra43/R 43rd (the gate)": r"(?i)\bra43\b|[Rr] 43rd|seatra43|s-ra43-",""", 1),
 ("LIT scratch UUIDs + R43 153c9bb9",
  r""" "scratch UUID R36..R42": r"5b7b88c2|8e7842da|bbcf227c|38deced2|7ef22b0d|aed7a0e9|0bc59869|5a4cb565|ab170fd5",""",
  r""" "scratch UUID R36..R43": r"5b7b88c2|8e7842da|bbcf227c|38deced2|7ef22b0d|aed7a0e9|0bc59869|5a4cb565|ab170fd5|153c9bb9",""", 1),
 ("LIT range bound",
  r""" "bare range bound range(1, N<=42)": r"range\(1,\s*(?:3[0-9]|40|41|42)\)",""",
  r""" "bare range bound range(1, N<=43)": r"range\(1,\s*(?:3[0-9]|40|41|42|43)\)",""", 1),
]
fail = []
for label, old, new, want in EDITS:
    got = t.count(old)
    if got != want:
        fail.append("%-60s want %d got %d" % (label, want, got))
if fail:
    print("REFUSED -- %d count assert(s) failed:" % len(fail))
    for f in fail: print("   " + f)
    sys.exit(2)
for label, old, new, want in EDITS:
    t = t.replace(old, new.replace(B, BOOT), want)
assert B not in t, "placeholder left behind"
assert t.count('"44":"%s"}' % BOOT) == 1, "SEAT_DATE key 44 not written exactly once"
ast.parse(t)
open(dst_p, "w", encoding="utf-8").write(t)
print("WROTE %s  (%d substitutions, all count-asserted, ast.parse OK; boot date %s)" % (dst_p, len(EDITS), BOOT))
