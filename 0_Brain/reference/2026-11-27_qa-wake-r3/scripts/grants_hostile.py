# grants_hostile.py — NEW hostile rows against round 3's filter. Every row labelled LIVE must be KEPT (seat wednesday, today 2026-11-27).
# The rows are run two ways: classify_grant() directly, and through a real build on a scratch tree (pack must hold the row verbatim).
# P = how plausible the shape is in THIS register (H: the register already holds rows worded this way; M: its idiom, not yet seen; L: contrived).
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
root = mk_real("grants_hostile")
sys.path.insert(0, os.path.join(root, "2_Project_Files/wake"))
import wake_pack as w
T0 = datetime.date(2026, 11, 27)
ROWS = [
 # --- past end date, kept alive in words the keep list lacks (the register's own idiom: status prefixed to the first cell)
 ("H", "LIVE", "past: end LIFTED, 'now ends on his word' (the wording of the register's line 34 without the word CHANGED)",
  "| **⚠ Kam 2026-11-22 21:05 (live board): the END-OF-SUNDAY end of this grant is LIFTED; it now ends on his word.** **WEDNESDAY: deploy everything that is ready (Secuura)** | Kam, live board | **END OF SUNDAY 2026-11-22** (`date -j`: Sunday). | Kintsugi and demo |"),
 ("H", "LIVE", "past: 'until I say stop' (option c of the register's line 34) in the first cell",
  "| **⚠ Kam 2026-11-22: *\"keep it going until I say stop\"*: the Sunday end no longer applies.** **WEDNESDAY: keep going over the weekend (Secuura)** | Kam | **END OF SUNDAY 2026-11-22** (`date -j`: Sunday). | seats, gates, merges |"),
 ("H", "LIVE", "past: a RESTRICTION (the register's line 134 shape) kept in place in the scope cell, no listed word",
  "| **RESTRICTION (not a grant): NO Claude agents on the demo box** | Kam, panel | **END OF SUNDAY 2026-11-22** (`date -j`: Sunday). | Kam 2026-11-23 09:02, verbatim: *\"leave that in place till I am back\"*. It holds. |"),
 ("M", "LIVE", "past: new end date written in the SCOPE cell (only the EXPIRES cell is searched for a second date)",
  "| **WEDNESDAY: close, merge and archive (Secuura board)** | Kam | **END OF SUNDAY 2026-11-22** (`date -j`: Sunday). | Kam 2026-11-23: now runs to Sun 2026-12-06. |"),
 ("M", "LIVE", "past: new end date written in the FIRST cell",
  "| **⚠ NOW ENDS SUNDAY 2026-12-06 (Kam, live board 2026-11-23 08:10).** **WEDNESDAY: close, merge and archive** | Kam | **END OF SUNDAY 2026-11-22** (`date -j`: Sunday). | scope |"),
 ("M", "LIVE", "past: weekday + date at the start of the cell is a START, followed by a duration",
  "| **WEDNESDAY: deploy everything ready (Secuura)** | Kam | **MONDAY 2026-11-23, for 14 days** (`date -j`: Monday). | scope |"),
 ("M", "LIVE", "past: 'until <date>' then 'and for as long as the board is not clear'",
  "| **WEDNESDAY: clear the board** | Kam | until 2026-11-20 and for as long as the board is not clear | scope |"),
 ("M", "LIVE", "past: 'rolled over' by Kam",
  "| **WEDNESDAY: weekend run (Secuura)** | Kam | **END OF SUNDAY 2026-11-22**. Rolled over by Kam on Monday morning for another week. | scope |"),
 ("M", "LIVE", "past: 'still applies' note in the first cell",
  "| **⚠ 2026-11-24 Kam: this still applies.** **WEDNESDAY: Spark off; Sonnet tilt** | Kam | **END OF SUNDAY 2026-11-22** | scope |"),
 ("M", "LIVE", "past: REINSTATED / RE-GRANTED word only in the GIVEN cell is caught? (control for the keep list: 'reinstat' is listed)",
  "| **WEDNESDAY: weekend run** | Kam; REINSTATED by him 2026-11-23 | **END OF SUNDAY 2026-11-22** | scope |"),
 ("M", "LIVE", "past: 're-granted' (not in the row keep list; REVIVED holds RE-GRANTED only for the dead class)",
  "| **WEDNESDAY: weekend run** | Kam; re-granted by him on the board Monday | **END OF SUNDAY 2026-11-22** | scope |"),
 ("L", "LIVE", "past: end date in UTC still running in AEDT's morning (dropped a few hours early)",
  "| **WEDNESDAY: use the vendor sandbox** | Kam | until 2026-11-26 23:59 UTC-10 (Honolulu, the vendor's clock) | scope |"),
 ("M", "LIVE", "past: 'through 2026-11-26' with 'incl. Friday' (a second day in words the WORD_DATE pattern lacks)",
  "| **WEDNESDAY: deploy window** | Kam | through 2026-11-26 and Friday too | scope |"),
 # --- dead marker with a date, but the row (or half of it) is live
 ("H", "LIVE", "dead: one HALF ended, the other half stands (the register's lines 49 and 126 record halves)",
  "| **ENDED 2026-11-25 for the DEMO half only (Peter's freeze); the Kintsugi half is unchanged.** **WEDNESDAY: DEPLOY EVERYTHING as soon as it is tested and ready (Secuura)** | Kam | **END OF SUNDAY 2026-11-29** (`date -j`: Sunday) | Kintsugi and demo |"),
 ("M", "LIVE", "dead: RETIRED <date> for one advisory, the other still baselined",
  "| **RETIRED 2026-11-03 (zod half): PR 1953 merged. The msal half is still baselined to MONDAY 2026-11-30.** **SECUURA: two HIGH advisories BASELINED** | Kam | **MONDAY 2026-11-30** | rows by Seat R |"),
 ("M", "LIVE", "dead: CLOSED <date> made PERMANENT, for THIS seat (the register's line 24 shape, Wednesday's own)",
  "| **CLOSED 2026-11-26 — made PERMANENT by Kam: \"never deploy to demo without Peter's nod\" (a HOLD that now always binds).** ~~WEDNESDAY: demo frozen this week~~ | Kam | **No end: permanent.** | Secuura demo |"),
 ("M", "LIVE", "dead: CLOSED used for a HOLD that is still binding ('closed to deploys')",
  "| **CLOSED since 2026-11-25: the Secuura demo box is closed to deploys until Peter's nod (A HOLD, NOT A GRANT)** | Kam, live board | **EVENT: Peter's nod.** | demo only; Kintsugi carries on |"),
 ("M", "LIVE", "dead: EXPIRED <date>, then 'reopened' in lower case / other words (REVIVED is case-sensitive, exact words)",
  "| **EXPIRED 2026-11-20; Kam reopened it 2026-11-24 (\"carry on with that\").** **WEDNESDAY: clear the Secuura board** | Kam | **EVENT: the board is clear.** | scope |"),
 ("M", "LIVE", "dead: EXPIRED <date> 'but REPLACED IN PLACE by' a new live grant written in the same row",
  "| **EXPIRED 2026-11-20. REPLACED IN PLACE 2026-11-24 by Kam's new word: WEDNESDAY may deploy to Kintsugi without a card this week.** | Kam | **END OF SUNDAY 2026-11-29** | Kintsugi |"),
 ("L", "LIVE", "dead: marker word is the row's subject and a date follows",
  "| **EXPIRED 2026-11-26 certificates on Kintsugi may be rotated by WEDNESDAY without a card** | Kam | **No end stated.** | scope |"),
 ("L", "LIVE", "dead: 'DEAD 2026-11-26 letter queue' subject",
  "| **DEAD since 2026-11-20 seats may be respawned by the watcher without asking** | Kam | **No end stated.** | scope |"),
 ("M", "LIVE", "dead: only PART of the first cell is struck (the marker is not struck; the struck part is the OLD end)",
  "| **ENDED 2026-11-22 ~~at midnight~~ — no: Kam 2026-11-23 \"keep at it\".** **WEDNESDAY: weekend run (Secuura)** | Kam | **No end stated now.** | scope |"),
 # --- another seat leads, but the row binds this seat in words the lists lack
 ("H", "LIVE", "other: 'the Studio seat' (the launcher's own name for Wednesday's seat)",
  "| **TUESDAY: owns the heavy lock tonight; the Studio seat holds its local-model runs until she releases it** | Kam | **EVENT: her release.** | heavy runs |"),
 ("H", "LIVE", "other: 'no seat' (every coordinator bound, words the ALL_SEATS list lacks)",
  "| **TUESDAY — A HOLD, NOT A GRANT: no seat pushes to the shared launcher while her rotation fix is in flight** | Kam | **EVENT: her fix lands.** | Launch_Wednesday.command |"),
 ("M", "LIVE", "other: 'nobody else' / 'the others'",
  "| **FRIDAY: sole user of Kam's PC helper this week; nobody else sends it work, the others queue through her** | Kam | **END OF SUNDAY 2026-11-29** | the PC |"),
 ("M", "LIVE", "other: 'ALL-SEATS' hyphenated, 'all 3 seats'",
  "| **TUESDAY (ALL-SEATS rule, all 3 seats): nothing spoken aloud before 06:00** | Kam | **No end stated.** | voice |"),
 ("M", "LIVE", "other: 'the coordinators' / 'each of the three'",
  "| **TUESDAY, FRIDAY: and the third coordinator too: cards to Kam pause while he is at the HP event** | Kam | **EVENT: he is back.** | cards |"),
 ("M", "LIVE", "other: 'W + T' initials and 'her sister' singular",
  "| **TUESDAY: may borrow one of her sister's Secuura-free seats on the Studio; W yields a pane when asked** | Kam | **No end stated.** | panes |"),
 ("M", "LIVE", "other: binds this seat by its machine and its project name (Blockchain / Platform K / Kintsugi), not the word Secuura",
  "| **FRIDAY: holds the Kintsugi deploy slot tonight; no Platform K deploy from any other pane** | Kam | **EVENT: her deploy is verified.** | Kintsugi |"),
 ("M", "LIVE", "other: this seat named only inside a path (Launch_Wednesday.command: no word boundary before W)",
  "| **TUESDAY: only she edits Launch_Wednesday.command this week; every other edit to it waits** | Kam | **END OF SUNDAY 2026-11-29** | the launcher |"),
 ("M", "LIVE", "other: 'general' work (Wednesday's own scope word, deliberately not a client word: STATUS deviation 8)",
  "| **FRIDAY: takes ALL general work this week, Secuura excepted; hand general tickets to her** | Kam | **END OF SUNDAY 2026-11-29** | general |"),
 ("M", "LIVE", "other: 'Wed.' / 'Weds' short forms in mixed case",
  "| **TUESDAY: shares the Mac mini's GPU with Weds tonight; first come, first served** | Kam | **No end stated.** | GPU |"),
 ("L", "LIVE", "other: the stamp idiom followed directly by the seat's name in the same cell (the exclusion must not swallow it)",
  "| **TUESDAY: hold all deploys** | Kam, live board (`date -j`: Wednesday); Wednesday is bound as well | **No end stated.** | all |"),
 ("L", "LIVE", "other: the name followed by a date is treated as a weekday: 'WEDNESDAY 2026-11-27 seat' is the SEAT here",
  "| **TUESDAY: hands HPSM triage to WEDNESDAY 2026-11-27 onward** | Kam | **No end stated.** | triage |"),
 # --- structure
 ("M", "LIVE", "five cells (a pipe in Kam's words) AND another seat's name leads a quoted first cell",
  "| **WEDNESDAY: run `a | b` nightly** | Kam | **END OF SUNDAY 2026-11-22** then until he says stop | scope |"),
 ("M", "LIVE", "merged cells: three cells only, end date in the last",
  "| **WEDNESDAY: deploy window; given by Kam on the board** | **END OF SUNDAY 2026-11-22**, then week by week | scope |"),
 ("M", "LIVE", "date in another format in EXPIRES (22/11/2026) with a live extension",
  "| **WEDNESDAY: weekend run** | Kam | END OF SUNDAY 22/11/2026, then to 06/12/2026 | scope |"),
 ("M", "LIVE", "end date glued to a time (2026-11-26T23:59) and later prolonged in words",
  "| **WEDNESDAY: sandbox use** | Kam | until 2026-11-26T23:59, prolonged by a week | scope |"),
 # --- controls: these MUST drop (the instrument can see a drop)
 ("-", "DEAD", "control: plain past end date", "| **WEDNESDAY: weekend run** | Kam | **END OF SUNDAY 2026-11-22** (`date -j`: Sunday). | scope |"),
 ("-", "DEAD", "control: dead marker with date", "| **EXPIRED 2026-11-20 — its EVENT happened. DEAD.** **WEDNESDAY: x** | Kam | **EVENT** | scope |"),
 ("-", "DEAD", "control: plain other seat", "| **TUESDAY: OXPd agents may deploy** | Kam | **No end stated.** | OXPd only |"),
]
bad = {"H": 0, "M": 0, "L": 0}
live = {"H": 0, "M": 0, "L": 0}
out = []
for p, kind, label, row in ROWS:
    v, why = w.classify_grant(row, "wednesday", T0)
    dropped = v in ("dead", "other", "past")
    if kind == "LIVE":
        live[p] += 1
        if dropped:
            bad[p] += 1
    flag = ("WRONGLY DROPPED" if dropped else "kept") if kind == "LIVE" else ("dropped (control ok)" if dropped else "CONTROL NOT DROPPED")
    out.append("%-20s P=%s %-12s %s  [%s]" % (flag, p, v, label, why))
print("\n".join(out))
print("LIVE rows: %d; wrongly dropped: %d (plausibility H %d of %d, M %d of %d, L %d of %d)"
      % (sum(live.values()), sum(bad.values()), bad["H"], live["H"], bad["M"], live["M"], bad["L"], live["L"]))
# through a real build: append the rows to a scratch copy of the real register's first table and build
gp = os.path.join(root, "0_Brain/tasks/EXPIRING-GRANTS.md")
g = open(gp, encoding="utf-8").read().split("\n")
hdr = [i for i, l in enumerate(g) if l.startswith("|---")][0]
tagged = [r.replace("| scope |", "| scope QAROW%02d |" % i).replace(" |", " QAROW%02d |" % i, 1) if "QAROW" not in r else r for i, (_, _, _, r) in enumerate(ROWS)]
tagged = []
for i, (_, _, _, r) in enumerate(ROWS):
    cells = r.split("|")
    cells[-2] = cells[-2].rstrip() + " QAROW%02d " % i
    tagged.append("|".join(cells))
g[hdr + 1:hdr + 1] = tagged
open(gp, "w", encoding="utf-8").write("\n".join(g))
rc, o, e = wp(root, "--today", "2026-11-27")
pack = open(os.path.join(root, "0_Brain/wake/WAKE-wednesday.md"), encoding="utf-8").read() if rc == 0 else ""
side = open(os.path.join(root, "0_Brain/wake/WAKE-wednesday.dropped.txt"), encoding="utf-8").read() if rc == 0 else ""
miss = [i for i, (p, kind, _, _) in enumerate(ROWS) if kind == "LIVE" and ("QAROW%02d" % i) not in pack]
print("real build with the %d rows planted: rc %d; LIVE rows absent from the pack: %d %s; sidecar rows %d" % (len(ROWS), rc, len(miss), miss, sum(1 for l in side.split("\n") if " | line " in l)))
agree = all((("QAROW%02d" % i) in pack) == (w.classify_grant(tagged[i], "wednesday", T0)[0] in ("mine", "unclassified")) for i in range(len(ROWS)))
print("build and direct classification agree on every row: %s" % agree)
