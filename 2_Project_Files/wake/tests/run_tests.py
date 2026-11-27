#!/usr/bin/env python3
"""run_tests.py — tests for the wake lane (handover.sh, wake_pack.py, wake_census.sh, the launcher proposal).

Everything is written under a scratch directory; fixtures are generated there. The real state,
grants, ledger and pickup files are never write targets; the real launcher is READ (never written)
by the P group, and the P group patches a scratch COPY.

Usage: run_tests.py [--groups H,W,C,P,D,S,R] [--mutants]
  env WAKE_UNDER_TEST   directory holding the tools (default: this file's parent's parent)
  env WAKE_TEST_SCRATCH scratch root (default: a fresh mkdtemp)
  --mutants             break each tool in a scratch copy and require the named test to go red
Output: one line per check, "PASS <id> <what>" or "FAIL <id> <what> :: <detail>", then a count line.
Exit 0 only when every check passed (or, with --mutants, every mutant was caught).
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
from hostile_rows import ROWS as HOSTILE  # noqa: E402  (the second checker's 41 rows)
LANE = os.path.abspath(os.path.join(HERE, ".."))
REAL_ROOT = os.path.abspath(os.path.join(LANE, "..", ".."))
TOOLS = os.path.abspath(os.environ.get("WAKE_UNDER_TEST", LANE))
LAUNCHER = os.path.join(REAL_ROOT, "Launch_Wednesday.command")
TODAY = "2026-11-27"
STAMP = "2026-11-27 12:00:00 TEST"
RESULTS = []


def check(tid, what, cond, detail=""):
    RESULTS.append((tid, bool(cond)))
    if cond:
        print("PASS %s %s" % (tid, what))
    else:
        print("FAIL %s %s :: %s" % (tid, what, str(detail)[:400].replace("\n", " / ")))


def run(cmd, data=None, env=None):
    e = dict(os.environ)
    for k in ("WED_AGENT", "HANDOVER_TREE", "HANDOVER_CAP_BYTES", "HANDOVER_TEST_BREAK", "HANDOVER_TEST_STAMP", "WED_SEAT",
              "HANDOVER_ALLOW_XCLOCK", "HANDOVER_LOCK_WAIT"):
        e.pop(k, None)
    e["PYTHONDONTWRITEBYTECODE"] = "1"   # the tools under test are imported by nobody; keep the lane free of caches
    e["HANDOVER_LOCK_WAIT"] = "5"
    e.update(env or {})
    p = subprocess.run(cmd, input=data if data is not None else b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=e)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text if isinstance(text, bytes) else text.encode("utf-8"))


def rb(path):
    with open(path, "rb") as f:
        return f.read()


def sha(path):
    return hashlib.sha256(rb(path)).hexdigest()


# ── fixtures ───────────────────────────────────────────────────────────────────────────────────
GRANTS = """# Expiring grants (fixture)

| grant | given | EXPIRES | scope, exactly |
|---|---|---|---|
| **WEDNESDAY: G01-MINE-LIVE** | Kam | **No end stated.** | scope |
| **DEAD since 2026-11-26: G02-DEAD-MARKED** | Kam | **EVENT: ends when done** | scope |
| **WEDNESDAY: G03-MINE-SAYS-DEAD-INSIDE the old row is DEAD, this replaces it** | Kam | **No end stated.** | DEAD is a word here too |
| **TUESDAY: G04-OTHER-SEAT** | Kam | **No end stated.** | scope |
| **TUESDAY, WEDNESDAY: G05-BOTH-SEATS** | Kam | **No end stated.** | scope |
| **WEDNESDAY: G06-MINE-MENTIONS a Tuesday meeting and a Friday review** | Kam | **No end stated.** | scope |
| **WEDNESDAY: G07-PAST-DATE** | Kam | **END OF SUNDAY 2026-11-22** (`date -j`: Sunday). | scope |
| **WEDNESDAY: G08-FUTURE-DATE** | Kam | **END OF SUNDAY 2026-11-29** | scope |
| **WEDNESDAY: G09-ENDS-TODAY** | Kam | **END OF FRIDAY 2026-11-27** | scope |
| **WEDNESDAY: G10-DATE-NOT-LEADING** | Kam | **EVENT: ends when he signs in (asked 2026-11-01)** | scope |
| **WEDNESDAY: G11-PAST-WITH-A-SECOND-DATE** | Kam | **END OF SUNDAY 2026-11-08**; the board grant runs to 2026-12-05 | scope |
| **\u26a0 EXTENDED 2026-11-20 by Kam: G12-EXTENDED-HINT** | Kam | **END OF SATURDAY 2026-10-31** | scope |
| **G13-UNLABELLED standing rule** | Kam | **OPEN-ENDED** | scope |
| **EXPIRED 2026-11-02: G14-EXPIRED-MARKED** | Kam | **EVENT** | scope |
| **WEDNESDAY: G15-PAST-DATE-FIVE-CELLS** | Kam | **END OF SUNDAY 2026-11-01** | scope with a | stray pipe |
| **FRIDAY: G16-OTHER-SEAT-FRIDAY** | Kam | **No end stated.** | scope |
| ~~**FRIDAY: G17-STRUCK-OTHER-SEAT**~~ SUPERSEDED | Kam | **No end stated.** | scope |
| **Friday 2026-11-20 review: G18-WEEKDAY-NOT-A-SEAT** | Kam | **No end stated.** | scope |
| **CLOSED 2026-11-21: G21-CLOSED-MARKED and made permanent by Kam, with a first cell that runs well past eighty characters** | Kam | **EVENT** | scope |
| **WEDNESDAY: G22-KEPT-SAYS-CLOSED the board is CLOSED for the day** | Kam | **No end stated.** | scope |
| **RETIRED 2026-11-05: G23-RETIRED-MARKED** | Kam | **EVENT** | scope |
| **\u2705 BOTH HALVES RETIRED: G24-RETIRED-NOT-LEADING** | Kam | **No end stated.** | scope |
| **PREMISE ENDED 2026-10-07: G25-PREMISE-ENDED-MARKED** | Kam | **EVENT** | scope |
| **WEDNESDAY: G26-KEPT-PREMISE the words PREMISE ENDED sit inside** | Kam | **No end stated.** | scope |
| \u26a0 **END EVENT REACHED 2026-09-25: G27-END-EVENT-MARKED** | Kam | **EVENT, not date** | scope |
| **G28-KEPT-END-EVENT not yet: END EVENT REACHED when the zip is mailed** | Kam | **EVENT** | scope |
| **CLOSED PRs may be reopened by the seat without a card G30-MARKER-AS-SUBJECT** | Kam | **No end stated.** | scope |
| **DEAD LETTER queue may be purged weekly G31-DEAD-LETTER** | Kam | **No end stated.** | scope |
| **EXPIRED certificates may be replaced without asking G32-EXPIRED-SUBJECT** | Kam | **No end stated.** | scope |
| **RETIRED laptops may be wiped G33-RETIRED-SUBJECT** | Kam | **No end stated.** | scope |
| ~~**EXPIRED 2026-11-20**~~ **REVIVED by Kam 2026-11-26: G34-STRUCK-THEN-REVIVED keep going** | Kam | **No end stated.** | scope |
| **CLOSED 2026-11-20, then REOPENED by Kam 2026-11-26: G35-CLOSED-THEN-REOPENED** | Kam | until he says stop | scope |
| **CLOSED-LOOP deploys allowed G36-HYPHENATED** | Kam | **No end stated.** | scope |
| **DEADLINE for the audit is in December G37-DEADLINE-WORD** | Kam | **No end stated.** | scope |
| **DEAD: do not rely on it G38-MARKER-WITHOUT-A-DATE** | Kam | **No end stated.** | scope |
| **TUESDAY (and ALL SEATS): no pushes to main until Kam says G39-ALL-SEATS** | Kam | **No end stated.** | all |
| **FRIDAY: hold all deploys G40-SCOPE-BINDS-THIS-SEAT** | Kam | **No end stated.** | binds WEDNESDAY too: nothing ships while it holds |
| **TUESDAY: OXPd agents may deploy G41-OTHER-NAMES-CLIENT** | Kam | **No end stated.** | includes the shared Secuura staging box |
| **TUESDAY 2026-12-01 kick-off prep may start G42-WEEKDAY-NO-SEPARATOR** | Kam | **No end stated.** | scope |
| **TUESDAY: G43-OTHER-WITH-WEEKDAY-STAMPS** | Kam, live board (`date -j`: Wednesday) | **END OF WEDNESDAY 2026-12-02** | scope |
| **TUESDAY: G44-OTHER-NAMES-SEAT-IN-GIVEN** | Kam, said while reviewing Wednesday's board | **No end stated.** | scope |
| **WEDNESDAY: G45-GIVEN-DATE-LEADS** | Kam | 2026-11-20 given; in force until withdrawn | scope |
| **WEDNESDAY: G46-START-DATE** | Kam | 2026-11-20 onwards, until further notice | scope |
| **WEDNESDAY: G47-KEPT-ALIVE** | Kam | END OF SUNDAY 2026-11-22, then kept alive until further notice (Kam 23 Nov) | scope |
| **WEDNESDAY: G48-WHICHEVER-LATER** | Kam | END OF SUNDAY 2026-11-22 or the EVENT (board clear), whichever is LATER | scope |
| **WEDNESDAY: G49-MOVED-IN-WORDS** | Kam | Sunday 2026-11-22 at first; Kam moved it to Mon 30 Nov | scope |
| **WEDNESDAY: G50-CONTINUED** | Kam | END OF SUNDAY 2026-11-22. CONTINUED by Kam on the 23rd | scope |
| **WEDNESDAY: G51-BARE-PAST-DATE** | Kam | 2026-11-20 | scope |
| **WEDNESDAY: G52-ENDED-YESTERDAY** | Kam | END OF THURSDAY 2026-11-26 | scope |
| **WEDNESDAY: G53-STOCK-PHRASE-AFTER-THE-DATE** | Kam | **END OF SUNDAY 2026-11-15**. Not renewed by inference. | scope |
| **TUESDAY — A HOLD, NOT A GRANT: NO HPSM WORK for three weeks G54-OTHER-SEATS-HOLD** | Kam | **END OF THURSDAY 2026-12-10** | the HPSM project |
| **TUESDAY + WED: share the box tonight G55-SHORT-NAME** | Kam | **No end stated.** | scope |
| **FLEET: nothing spoken before 06:00 G56-FLEET** | Kam | **No end stated.** | scope |
| **WEDNESDAY: G57-SECOND-DATE-IN-WORDS** | Kam | END OF SUNDAY 2026-11-22; then to Mon 30 Nov | scope |
| **WEDNESDAY: G58-DATE-OR-EVENT** | Kam | END OF SUNDAY 2026-11-22 or the EVENT (board clear) | scope |
| **TUESDAY: G59-STAMP-THEN-THE-SEAT** | Kam (`date -j`: Wednesday) and WEDNESDAY too | **No end stated.** | scope |
| **TUESDAY: G60-SHORT-NAME-IN-SCOPE** | Kam | **No end stated.** | binds WED as well |
| **TUESDAY: G61-TICKET-ID-IS-NOT-THE-SEAT** | Kam, note on WED-170 | **No end stated.** | scope |
| **TUESDAY: G62-BOTH-COORDINATORS** | Kam | **No end stated.** | both coordinators hold until he says |
| **DEAD since 2026-11-20? NOT DEAD: G63-MARKED-THEN-DENIED Kam says it is live** | Kam | **No end stated.** | scope |
| **WEDNESDAY: G64-PROVISIONAL-END** | Kam | END OF SUNDAY 2026-11-22 (provisional) | scope |
| **WEDNESDAY: G65-AT-LEAST** | Kam | until 2026-11-22 at least | scope |
| ~~**EXPIRED 2026-11-20**~~ back in force on his word: G66-STRUCK-MARKER-ONLY | Kam | **No end stated.** | scope |

## When a grant expires

1. Stop.

## Expired

### Lapsed 2026-09-20

| grant | given | EXPIRES | scope, exactly |
|---|---|---|---|
| **G19-UNDER-EXPIRED-HEADING unlabelled** | Kam | **EVENT: ends when done** | scope |
| **G20-UNDER-EXPIRED-PAST-DATE** | Kam | **END OF SUNDAY 2026-09-13 AEST** | scope |
"""
# Round 4: the register is carried WHOLE. Every fixture row above (dead-marked, another seat's, past-dated,
# struck through, under the Expired heading) must be in every seat's pack, verbatim, in file order.
GRANT_ROWS = [l for l in GRANTS.split("\n") if l.startswith("|") and any(("G%02d-" % i) in l for i in range(1, 70))]
BEGIN_G = "<<< BEGIN 0_Brain/tasks/EXPIRING-GRANTS.md (verbatim) >>>\n"
END_G = "<<< END 0_Brain/tasks/EXPIRING-GRANTS.md (verbatim) >>>\n"


def part_d(pack_text):
    """The register as the pack carries it: the text between the BEGIN and END lines ('' when either is missing)."""
    if pack_text.count(BEGIN_G) != 1 or pack_text.count(END_G) != 1:
        return ""
    return pack_text.split(BEGIN_G, 1)[1].split(END_G, 1)[0]


def rows_whole(pack_text, rows):
    """Every row verbatim, exactly once, in the order given. -> '' when so, else what is wrong."""
    pos = [pack_text.find(r) for r in rows]
    missing = [r[:60] for r, p in zip(rows, pos) if p < 0]
    if missing:
        return "%d row(s) missing, first: %s" % (len(missing), missing[0])
    twice = [r[:60] for r in rows if pack_text.count(r) != 1]
    if twice:
        return "%d row(s) not exactly once, first: %s" % (len(twice), twice[0])
    return "" if pos == sorted(pos) else "rows out of file order"

CARD = """---
type: rules-card
---

# Rules card: %(seat)s seat

## Most reinforced (read these first)
- [x5] %(tag)sTOP-RULE-ONE: check before claiming. `a.md`
- [x3] %(tag)sTOP-RULE-TWO: sources, not representations. `b.md`

## checks-that-can-fail
- [x5] FAMILY-ONLY-RULE-A. `a.md`
- [x2] second line. `c.md`
- [x1] third line. `d.md`

## kam-communication
- [x1] FAMILY-ONLY-RULE-B. `e.md`

## Enforced by a tool (the tool remembers; one line each)
- ENFORCED-ONLY-LINE. `f.md`

## Not on this card
- dead: z.md
"""

LEDGER = """# Correction ledger (fixture)

| w | Meaning | Required response |
|---|---|---|
| 1 | **Isolated** | Log it. |

## Ledger (newest at top)

| 2026-11-27 | \U0001F7E1 **%(tag)sLEDGER-HEADLINE-ONE.** [W] LEDGER-PROSE-ONLY-ONE the long cause text. Rule: do the LEDGER-RULE-ONE thing (e.g. three reads) before telling anyone. Then NOT-PART-OF-THE-RULE follows. | correction | 1 | [[x]] | done |

| 2026-11-26 | \U0001F7E1 **%(tag)sLEDGER-HEADLINE-TWO.** more prose. Rule (re-applied): LEDGER-RULE-TWO always. | correction | 2 | x | y |

| 2026-11-25 | \U0001F7E2 **%(tag)sLEDGER-HEADLINE-THREE** LEDGER-PROSE-ONLY-THREE and no rule sentence | praise | 1 | - | - |

| Date | What happened (root cause) | Type | w | Lesson | Status |
|---|---|---|---|---|---|
"""

PICKUP = """---
type: pickup
---

# NEXT PICKUP (fixture)

## BLOCK ONE newest
- %(tag)sPICKUP-FIRST-BLOCK-MARKER

## BLOCK TWO older
- %(tag)sPICKUP-SECOND-BLOCK-MARKER

## OWED
- PICKUP-OWED-MARKER
"""

RULES_CARD_STUB = '''VOCAB = ["boot", "brief", "launch"]
ap.add_argument("--at")
'''


def make_tree(root, big_ledger=False):
    b = os.path.join(root, "0_Brain")
    w(os.path.join(root, "CLAUDE.md"), "root rules fixture\n" * 20)
    w(os.path.join(b, "CLAUDE.md"), "brain routing fixture\n" * 10)
    w(os.path.join(b, "identity", "persona.md"), "# Persona\nPERSONA-MARKER line one.\n\n## A heading inside\nmore persona.\n")
    w(os.path.join(b, "identity", "voice-protocol.md"), "# Voice\nVOICE-MARKER speak briefly.\n")
    w(os.path.join(b, "people", "kam.md"), "# Kam\nKAM-MARKER who he is.\nNo trailing newline here")
    w(os.path.join(b, "identity", "persona.md.pre-1127"), "POISON-BACKUP\n")
    w(os.path.join(b, "identity", "persona (conflict_on_2026-11-01).md"), "POISON-CONFLICT\n")
    lg = os.path.join(b, "learnings")
    w(os.path.join(lg, "_rules_card_wednesday.md"), CARD % {"seat": "wednesday", "tag": ""})
    w(os.path.join(lg, "_rules_card_tuesday.md"), CARD % {"seat": "tuesday", "tag": "TUE-"})
    w(os.path.join(lg, "_rules_card_friday.md"), CARD % {"seat": "friday", "tag": "FRI-"})
    w(os.path.join(lg, "_ledger_friday.md"), LEDGER % {"tag": "FRI-"})
    w(os.path.join(lg, "_rules_card_wednesday (conflict_on_2026-11-03).md"), "POISON-CONFLICT\n")
    w(os.path.join(lg, "families", "checks-that-can-fail.md"), "family file\n")
    w(os.path.join(lg, "families", "kam-communication.md"), "family file\n")
    w(os.path.join(lg, "families", "checks-that-can-fail (conflict_on_2026-11-20).md"), "POISON-CONFLICT\n")
    w(os.path.join(lg, "families", "old-family.md.pre-1101"), "POISON-BACKUP\n")
    led = LEDGER % {"tag": ""}
    if big_ledger:
        led += "".join("| 2026-11-24 | **BIG-ROW-%d** %s Rule: %s. | c | 1 | - | - |\n\n" % (i, "x" * 200, "y " * 300) for i in range(600))
    w(os.path.join(lg, "_ledger.md"), led)
    w(os.path.join(lg, "_ledger (conflict_on_2026-11-02).md"), "| 2026-11-27 | **POISON-CONFLICT** |\n")
    w(os.path.join(lg, "_ledger.md.pre-1126"), "| 2026-11-27 | **POISON-BACKUP** |\n")
    w(os.path.join(lg, "_ledger_laptop_datasec.md"), LEDGER % {"tag": "TUE-"})
    t = os.path.join(b, "tasks")
    w(os.path.join(t, "NEXT-PICKUP.md"), PICKUP % {"tag": ""})
    w(os.path.join(t, "NEXT-PICKUP-TUESDAY.md"), PICKUP % {"tag": "TUE-"})
    w(os.path.join(t, "NEXT-PICKUP-FRIDAY.md"), PICKUP % {"tag": "FRI-"})
    w(os.path.join(t, "EXPIRING-GRANTS.md"), GRANTS)
    w(os.path.join(t, "TASKS.md"), "TASKS-CONTENT-MARKER\n")
    w(os.path.join(t, "WEEK-INSTRUCTION.md"), "week instruction fixture\n")
    w(os.path.join(b, "projects_index", "INDEX.md"), "INDEX-CONTENT-MARKER\n" * 3000)
    w(os.path.join(b, "projects_index", "entries", "Secuura__X.md"), "entry\n" * 30)
    w(os.path.join(b, "projects_index", "entries", "Secuura__X (conflict_on_2026-09-04).md"), "entry copy\n" * 10)
    w(os.path.join(b, "daily", "2026-11-26.md"), "yesterday note\n" * 40)
    w(os.path.join(b, "daily", "2026-11-27.md"), "today note\n" * 5)
    w(os.path.join(root, "2_Project_Files", "tools", "rules_card.py"), RULES_CARD_STUB)
    w(os.path.join(root, "2_Project_Files", "wake", "handover.sh"), "# stub so the pointer resolves\n")
    w(os.path.join(root, "2_Project_Files", "tools", "kam_msgs.sh"), "#\n")
    w(os.path.join(root, "2_Project_Files", "tools", "kam_rulings_today.sh"), "#\n")
    w(os.path.join(root, "1_Project_Definition", "Architecture", "2026-11-27_fleet-structure-v2-design.md"), "design\n")
    return root


def block(tag, extra=""):
    return ("## FLOOR\n- %s floor: no seat running\n\n## FIRST WORK\n- %s first work\n\n## OWED\n- none\n\n"
            "## OPEN CARDS\n- none\n\n## GRANTS IN PLAY\n- none\n%s" % (tag, tag, extra)).encode("utf-8")


# ── H: handover ────────────────────────────────────────────────────────────────────────────────
def group_h(scratch):
    ho = os.path.join(TOOLS, "handover.sh")
    base = os.path.join(scratch, "h")
    wed = os.path.join(base, "WEDNESDAY")
    tasks = os.path.join(wed, "0_Brain", "tasks")
    w(os.path.join(tasks, "NEXT-PICKUP.md"), "legacy pickup, never touched\n")
    pick_sha = sha(os.path.join(tasks, "NEXT-PICKUP.md"))
    state = os.path.join(tasks, "STATE-wednesday.md")
    arch = os.path.join(tasks, "STATE-wednesday-archive.md")
    env = {"HANDOVER_TREE": wed, "HANDOVER_TEST_STAMP": STAMP}

    def h(args, data=None, extra=None):
        e = dict(env)
        e.update(extra or {})
        return run(["bash", ho] + args, data, e)

    rc, out, err = h(["--where"])
    check("H01", "--where prints the seat's paths and writes nothing",
          rc == 0 and "STATE-wednesday.md" in out and "STATE-wednesday-archive.md" in out and os.listdir(tasks) == ["NEXT-PICKUP.md"], out + err)
    rc, out, err = h(["check"])
    check("H20", "check on a tree with no state file says ABSENT, rc 0", rc == 0 and "ABSENT" in out, out + err)
    rc, out, err = h(["show"])
    check("H20b", "show with no state file is rc 1", rc == 1, out + err)
    b1 = block("B1")
    rc, out, err = h(["write", "--stdin", "--dry"], b1)
    check("H12", "--dry prints the plan and writes nothing", rc == 0 and "DRY" in out and not os.path.exists(state), out + err)

    rc, out, err = h(["write", "--stdin"], b"")
    check("H06", "REFUSES an empty block (rc 3, says empty)", rc == 3 and "empty" in err and not os.path.exists(state), err)
    rc, out, err = h(["write", "--stdin"], b"\n  \n\t\n")
    check("H06b", "REFUSES a whitespace-only block", rc == 3 and "empty" in err, err)
    rc, out, err = h(["write"], b1)
    check("H13", "REFUSES write without --stdin (rc 2)", rc == 2 and "stdin" in err and not os.path.exists(state), err)
    rc, out, err = h(["write", "some text as an argument"], b1)
    check("H13b", "REFUSES the block as an argument (rc 2)", rc == 2 and not os.path.exists(state), err)
    rc, out, err = h(["write", "--stdin"], b1.replace(b"## OWED\n- none\n\n", b""))
    check("H08", "REFUSES a block with a part missing, names it", rc == 3 and "part missing: '## OWED'" in err, err)
    rc, out, err = h(["write", "--stdin"], b1 + b"\n" + block("B1b"))
    check("H09", "REFUSES two blocks in one write (each part twice)", rc == 3 and "appears 2 times" in err, err)
    rc, out, err = h(["write", "--stdin"], b1 + b"\n## CHECKPOINT 70% an extra dated block\n- text\n")
    check("H10", "REFUSES a '##' heading that is not one of the five", rc == 3 and "not exactly one of the five" in err, err)
    hostile = [("b", "a '###' heading", "\n### a sub-heading under the last part\n- detail\n"),
               ("c", "an INDENTED '## ' heading", "\n  ## SECOND BLOCK\n- detail\n"),
               ("d", "a second dated block under a '# ' heading", "\n# CHECKPOINT 70% a second block\n- detail\n"),
               ("e", "a heading after a zero-width space", "\n\u200b## HIDDEN\n- detail\n"),
               ("f", "a deeper heading (######)", "\n###### deep\n- detail\n")]
    for hid, what, extra in hostile:
        rc, out, err = h(["write", "--stdin", "--dry"], block("B1", extra))
        check("H10" + hid, "REFUSES %s inside a block (any level, indented or not)" % what, rc == 3 and "not exactly one of the five" in err, err)
    rc, out, err = h(["write", "--stdin", "--dry"], block("B1").replace(b"## FLOOR\n", "## FLOOR\u200b\n".encode("utf-8")))
    check("H10g", "REFUSES a part name followed by a zero-width space (a look-alike part)", rc == 3 and "part missing: '## FLOOR'" in err, err)
    rc, out, err = h(["write", "--stdin", "--dry"], block("B1", "\n**a bold line as a sub-title**\n- ticket #123 and item #4\n#123 at the start of a line is not a heading\n"))
    check("H10h", "accepts a bold line and a '#' that is not a heading (must succeed beside H10 to H10g)", rc == 0, err)
    rc, out, err = h(["write", "--stdin"], b1.replace(b"## OWED\n- none\n", b"## OWED\n"))
    check("H11", "REFUSES a part with no text under it", rc == 3 and "'## OWED' has no text" in err, err)
    rc, out, err = h(["write", "--stdin"], block("B1", "- landed at 11:4x this morning\n"))
    check("H07", "REFUSES a clock with an x digit, names it", rc == 3 and "x digit" in err and "11:4x" in err, err)
    rc, out, err = h(["write", "--stdin", "--dry"], block("B1", "- landed at 11:42, re-read 9:05; an x86 box; 12:50 next\n"))
    check("H07b", "accepts real clocks 11:42 and 9:05 (must succeed beside H07)", rc == 0, err)
    xc = os.path.join(base, "xc", "WEDNESDAY")
    xt = os.path.join(xc, "0_Brain", "tasks")
    os.makedirs(xt)
    xenv = {"HANDOVER_TREE": xc, "HANDOVER_TEST_STAMP": STAMP}
    quoted = block("XC", "- the grant named '(new account, ~10:1x AEDT)' is in play\n")
    why = "quoting the grant row's own name"
    rc, out, err = run(["bash", ho, "write", "--stdin"], quoted, dict(xenv, HANDOVER_ALLOW_XCLOCK="too short"))
    check("H07d", "x-clock override with a reason under 15 characters is still REFUSED", rc == 3 and "at least 15" in err and os.listdir(xt) == [], err)
    rc, out, err = run(["bash", ho, "write", "--stdin"], quoted, xenv)
    check("H07g", "without the variable the x-clock refusal stands (same block)", rc == 3 and "x digit" in err and os.listdir(xt) == [], err)
    rc, out, err = run(["bash", ho, "write", "--stdin"], quoted, dict(xenv, HANDOVER_ALLOW_XCLOCK=why))
    xs = rb(os.path.join(xt, "STATE-wednesday.md")) if rc == 0 else b""
    rc2, out2, err2 = run(["bash", ho, "check"], None, xenv)
    check("H07c", "x-clock override with an owned reason is accepted; the reason is in the block's header; check stays OK",
          rc == 0 and ("xclock_override: " + why).encode() in xs.split(b"\n---\n")[0] and b"~10:1x" in xs and rc2 == 0, out + err + out2 + err2)
    rc, out, err = run(["bash", ho, "write", "--stdin"], block("XC2"), dict(xenv, HANDOVER_ALLOW_XCLOCK=why))
    xap = os.path.join(xt, "STATE-wednesday-archive.md")
    xa = rb(xap).decode("utf-8") if os.path.exists(xap) else ""
    heads = [l for l in xa.split("\n") if l.startswith("# ARCHIVED ")]
    xs2 = rb(os.path.join(xt, "STATE-wednesday.md"))
    check("H07e", "the override's reason is written into that block's archive heading", rc == 0 and len(heads) == 1 and ("| x-clock override: " + why) in heads[0], heads)
    check("H07f", "a block with no x-clock records no override even when the variable is set", b"xclock_override" not in xs2)
    filler = block("BIG")
    big = filler + b"- " + b"z" * (11000 - len(filler) - 3) + b"\n"
    rc, out, err = h(["write", "--stdin"], big)
    check("H05", "REFUSES a block over the cap with size, cap and what to cut",
          rc == 3 and "11000 bytes" in err and "10000" in err and "largest first" in err and "GRANTS IN PLAY" in err, err)
    exact = filler + b"- " + b"z" * (10000 - len(filler) - 3) + b"\n"
    rc, out, err = h(["write", "--stdin", "--dry"], exact)
    check("H05b", "accepts a block of exactly the cap (must succeed beside H05)", rc == 0 and len(exact) == 10000, err)
    rc, out, err = h(["write", "--stdin", "--dry"], big, {"HANDOVER_CAP_BYTES": "20000"})
    check("H05c", "the cap is a variable: HANDOVER_CAP_BYTES=20000 accepts the 11000-byte block", rc == 0, err)
    check("H05d", "after every refusal above nothing was written", os.listdir(tasks) == ["NEXT-PICKUP.md"], os.listdir(tasks))

    rc, out, err = h(["write", "--stdin"], b1)
    ok = rc == 0 and os.path.exists(state) and not os.path.exists(arch)
    rc2, shown, _ = h(["show"])
    check("H02", "first write succeeds; show returns the block byte for byte; no archive yet",
          ok and rc2 == 0 and shown.encode("utf-8") == b1, out + err)
    rc, out, err = h(["check"])
    check("H17a", "check says OK after a tool write", rc == 0 and "OK" in out, out + err)

    b2 = block("B2")
    rc, out, err = h(["write", "--stdin"], b2)
    st = rb(state) if os.path.exists(state) else b""
    ar = rb(arch) if os.path.exists(arch) else b""
    one = all(st.count(("## %s\n" % p).encode()) == 1 for p in ["FLOOR", "FIRST WORK", "OWED", "OPEN CARDS", "GRANTS IN PLAY"])
    check("H03", "second write leaves exactly ONE block in the state file", rc == 0 and one and b"B2 floor" in st and b"B1 floor" not in st, out + err)
    check("H03b", "second write put the previous block verbatim in the archive, one entry",
          b1 in ar and ar.count(b"\n# ARCHIVED ") + (1 if ar.startswith(b"# ARCHIVED ") else 0) == 1, ar[:300])
    len_before = len(ar)
    b3 = block("B3")
    rc, out, err = h(["write", "--stdin"], b3)
    ar2 = rb(arch)
    st = rb(state)
    one = all(st.count(("## %s\n" % p).encode()) == 1 for p in ["FLOOR", "FIRST WORK", "OWED", "OPEN CARDS", "GRANTS IN PLAY"])
    check("H04", "stacked third write: still one block, archive longer, newest entry first, earlier bytes kept",
          rc == 0 and one and b"B3 floor" in st and len(ar2) > len_before and b1 in ar2 and b2 in ar2
          and ar2.find(b2) < ar2.find(b1) and ar2.endswith(ar[ar.find(b"# ARCHIVED "):]), out + err)

    s_before, a_before = rb(state), rb(arch)
    rc, out, err = h(["write", "--stdin"], block("B4"), {"HANDOVER_TEST_BREAK": "archive-truncate"})
    check("H15", "a conservation mismatch refuses (rc 4) and writes nothing",
          rc == 4 and "conservation" in err and rb(state) == s_before and rb(arch) == a_before, out + err)

    with open(state, "ab") as f:
        f.write(b"\nHAND-APPENDED-LINE outside the tool\n")
    hand_body = rb(state).split(b"\n---\n", 1)[1]
    rc, out, err = h(["check"])
    check("H17", "check goes red (rc 1) when the state file was appended to by hand", rc == 1 and "sha256" in out, out + err)
    rc, out, err = h(["write", "--stdin"], block("B5"))
    ar3 = rb(arch)
    check("H18", "a hand-edited state is archived verbatim by the next write, never lost",
          rc == 0 and hand_body in ar3 and b"HAND-APPENDED-LINE" in ar3 and "NOTE" in out, out + err)
    rc, out, err = h(["check"])
    check("H17b", "check is OK again after the tool rewrote the block", rc == 0, out + err)
    check("H16", "NEXT-PICKUP.md is byte-identical after every write", sha(os.path.join(tasks, "NEXT-PICKUP.md")) == pick_sha)
    check("H19", "no temp file left in the tasks directory",
          sorted(os.listdir(tasks)) == ["NEXT-PICKUP.md", "STATE-wednesday-archive.md", "STATE-wednesday.md"], os.listdir(tasks))

    tue = os.path.join(base, "TUESDAY")
    os.makedirs(os.path.join(tue, "0_Brain", "tasks"))
    rc, out, err = run(["bash", ho, "write", "--stdin"], block("T1"), {"HANDOVER_TREE": tue, "HANDOVER_TEST_STAMP": STAMP})
    check("H14", "the seat comes from the tree: a TUESDAY tree writes STATE-tuesday.md",
          rc == 0 and os.listdir(os.path.join(tue, "0_Brain", "tasks")) == ["STATE-tuesday.md"], out + err)
    other = os.path.join(base, "elsewhere")
    os.makedirs(os.path.join(other, "0_Brain", "tasks"))
    rc, out, err = run(["bash", ho, "write", "--stdin"], block("X1"), {"HANDOVER_TREE": other, "HANDOVER_TEST_STAMP": STAMP})
    check("H14b", "an unrecognised tree REFUSES (rc 2) and writes nothing",
          rc == 2 and "REFUSED" in err and os.listdir(os.path.join(other, "0_Brain", "tasks")) == [], out + err)
    rc, out, err = h(["--where"], None, {"WED_AGENT": "tuesday"})
    check("H14c", "WED_AGENT disagreeing with the tree REFUSES (rc 2)", rc == 2 and "REFUSED" in err, out + err)
    rc, out, err = h(["--where"], None, {"WED_AGENT": "wednesday"})
    check("H14d", "WED_AGENT agreeing with the tree is accepted (must succeed beside H14c)", rc == 0, out + err)

    nn = os.path.join(base, "nonl", "WEDNESDAY")
    os.makedirs(os.path.join(nn, "0_Brain", "tasks"))
    nenv = {"HANDOVER_TREE": nn, "HANDOVER_TEST_STAMP": STAMP}
    bare = block("NONL").rstrip(b"\n")
    rc, out, err = run(["bash", ho, "write", "--stdin"], bare, nenv)
    nst = rb(os.path.join(nn, "0_Brain", "tasks", "STATE-wednesday.md")) if rc == 0 else b""
    check("H22", "a block given without a final newline is stored with exactly one (the state file always ends in a newline)",
          rc == 0 and nst.endswith(bare + b"\n") and ("block_bytes: %d" % (len(bare) + 1)).encode() in nst, out + err)

    seatx = os.path.join(base, "seatx", "WEDNESDAY")
    os.makedirs(os.path.join(seatx, "0_Brain", "tasks"))
    tsrc = os.path.join(tue, "0_Brain", "tasks", "STATE-tuesday.md")
    if os.path.exists(tsrc):
        shutil.copy(tsrc, os.path.join(seatx, "0_Brain", "tasks", "STATE-wednesday.md"))
    rc, out, err = run(["bash", ho, "check"], None, {"HANDOVER_TREE": seatx})
    check("H23", "check goes red on a state file whose header names another seat", rc == 1 and "names seat 'tuesday'" in out, out + err)

    ur = os.path.join(base, "unread", "WEDNESDAY")
    urt = os.path.join(ur, "0_Brain", "tasks")
    os.makedirs(urt)
    uenv = {"HANDOVER_TREE": ur, "HANDOVER_TEST_STAMP": STAMP}
    run(["bash", ho, "write", "--stdin"], block("U1"), uenv)
    run(["bash", ho, "write", "--stdin"], block("U2"), uenv)
    ua = rb(os.path.join(urt, "STATE-wednesday-archive.md"))
    os.chmod(os.path.join(urt, "STATE-wednesday.md"), 0)
    rc, out, err = run(["bash", ho, "write", "--stdin"], block("U3"), uenv)
    os.chmod(os.path.join(urt, "STATE-wednesday.md"), 0o644)
    check("H24", "an UNREADABLE state file is a refusal naming the path (rc 4, no traceback); it is never treated as absent",
          rc == 4 and "cannot read" in err and "STATE-wednesday.md" in err and "Traceback" not in err
          and rb(os.path.join(urt, "STATE-wednesday-archive.md")) == ua and b"U2 floor" in rb(os.path.join(urt, "STATE-wednesday.md"))
          and sorted(os.listdir(urt)) == ["STATE-wednesday-archive.md", "STATE-wednesday.md"], out + err)

    seamtree = os.path.join(HERE, "seam_fixture", "WEDNESDAY")
    before_seam = sorted(os.listdir(os.path.join(seamtree, "0_Brain", "tasks")))
    rc, out, err = run(["bash", ho, "--where"], None, {"HANDOVER_TREE": seamtree})
    check("H25", "the test seam HANDOVER_TREE is REFUSED for a tree that is not under a temp or scratch directory, and says so",
          rc == 2 and "test seams" in err and sorted(os.listdir(os.path.join(seamtree, "0_Brain", "tasks"))) == before_seam, out + err)
    rc, out, err = h(["--where"])
    check("H25b", "the same seam is honoured for a tree under the scratch directory (must succeed beside H25)", rc == 0, out + err)
    rc, out, err = run([sys.executable, os.path.join(TOOLS, "handover_core.py"), "write", "--seat", "tuesday", "--tasks-dir", tasks, "--stamp", "X", "--cap", "10000"], block("ENGINE"))
    check("H25c", "the engine called directly with another seat's name for this tree is refused (rc 2), nothing written",
          rc == 2 and "the seat is the tree's own" in err and "STATE-tuesday.md" not in os.listdir(tasks), out + err)
    rc, out, err = run([sys.executable, os.path.join(TOOLS, "handover_core.py"), "where", "--seat", "wednesday",
                        "--tasks-dir", os.path.join(seamtree, "0_Brain", "tasks")], None, {"HANDOVER_TEST_BREAK": "archive-truncate"})
    check("H25d", "HANDOVER_TEST_BREAK is refused by the engine for a tree that is not under a temp directory", rc == 2 and "test seam" in err, out + err)

    raw = os.path.join(base, "raw", "WEDNESDAY")
    w(os.path.join(raw, "0_Brain", "tasks", "STATE-wednesday.md"), "a state file somebody typed, no header\nRAW-LINE\n")
    rc, out, err = run(["bash", ho, "write", "--stdin"], block("R1"), {"HANDOVER_TREE": raw, "HANDOVER_TEST_STAMP": STAMP})
    ra = os.path.join(raw, "0_Brain", "tasks", "STATE-wednesday-archive.md")
    check("H21", "a headerless state file is archived whole",
          rc == 0 and os.path.exists(ra) and b"a state file somebody typed, no header\nRAW-LINE\n" in rb(ra), out + err)


# ── W: wake pack ───────────────────────────────────────────────────────────────────────────────
def group_w(scratch):
    wp = os.path.join(TOOLS, "wake_pack.py")
    root = make_tree(os.path.join(scratch, "w", "WEDNESDAY"))
    out_default = os.path.join(root, "0_Brain", "wake", "WAKE-wednesday.md")

    def p(args, today=TODAY, r=root):
        return run([sys.executable, wp, "--root", r, "--today", today] + args)

    rc, out, err = p(["--seat", "nobody"])
    check("W14", "an unknown seat is refused (rc 2)", rc == 2, out + err)
    rc, out, err = p(["--seat", "wednesday", "--budget-tokens", "200"])
    lines = [l for l in err.split("\n") if " B  ~" in l]
    sizes = [int(l.split()[0]) for l in lines]
    check("W09", "over budget: non-zero, nothing written (no pack, no sidecar), parts listed largest first",
          rc == 3 and not os.path.exists(out_default) and not os.path.exists(os.path.join(root, "0_Brain", "wake"))
          and err.strip().split("\n")[-1].startswith("wake_pack: FAILED — over budget") and "OVER BUDGET" in err and len(sizes) >= 5 and sizes == sorted(sizes, reverse=True), err)
    bigroot = make_tree(os.path.join(scratch, "wbig", "WEDNESDAY"), big_ledger=True)
    rc, out, err = p(["--seat", "wednesday"], r=bigroot)
    lines = [l for l in err.split("\n") if " B  ~" in l]
    check("W09b", "a planted over-budget part (a huge ledger) refuses at the default budget and is named first",
          rc == 3 and not os.path.exists(os.path.join(bigroot, "0_Brain", "wake")) and lines and "ledger" in lines[0].lower(), err)

    rc, out, err = p(["--seat", "wednesday"])
    ok = rc == 0 and os.path.isfile(out_default)
    pack = rb(out_default).decode("utf-8") if ok else ""
    check("W01", "builds (rc 0) to the default path under the given root", ok, out + err)
    check("W12", "the manifest table lists every part with its source, bytes and tokens",
          all(s in pack for s in ["## Manifest", "| a | `0_Brain/identity/persona.md` |", "| b | `0_Brain/learnings/_rules_card_wednesday.md (Most reinforced)` |",
                                  "| c | `0_Brain/tasks/NEXT-PICKUP.md (first block)` |", "| d | `0_Brain/tasks/EXPIRING-GRANTS.md (whole, verbatim)` |",
                                  "| e | `0_Brain/learnings/_ledger.md (reduced rows)` |", "| f | `pointers (generated)` |", "| **total** |"]), pack[:900])
    total_line = [l for l in pack.split("\n") if l.startswith("| **total** |")]
    check("W12b", "the manifest total equals the file's real size",
          total_line and ("**%d**" % len(pack.encode("utf-8"))) in total_line[0], total_line)
    ident = True
    for rel in ("identity/persona.md", "identity/voice-protocol.md", "people/kam.md"):
        ident = ident and rb(os.path.join(root, "0_Brain", rel)).decode("utf-8") in pack
    check("W02", "identity files are in the pack verbatim, whole", ident)
    check("W03", "rules: 'Most reinforced' lines are in, a family's own lines are not",
          "TOP-RULE-ONE" in pack and "TOP-RULE-TWO" in pack and "FAMILY-ONLY-RULE-A" not in pack and "FAMILY-ONLY-RULE-B" not in pack
          and "ENFORCED-ONLY-LINE" not in pack)
    check("W03b", "rules: family headings carry their line counts, and the fetch command is named",
          "- checks-that-can-fail: 3 lines." in pack and "- kam-communication: 1 lines." in pack
          and "2_Project_Files/tools/rules_card.py --at <trigger> --seat wednesday" in pack and "Triggers: boot brief launch" in pack)
    check("W04", "state: with no STATE file the pack says so and carries ONLY the legacy pickup's first block",
          "NO STATE FILE YET" in pack and "PICKUP-FIRST-BLOCK-MARKER" in pack and "PICKUP-SECOND-BLOCK-MARKER" not in pack
          and "PICKUP-OWED-MARKER" not in pack)
    why = rows_whole(pack, GRANT_ROWS)
    check("W05", "grants: EVERY row of the register is in the pack verbatim, exactly once, in file order (%d rows: dead-marked, "
                 "another seat's, past-dated, struck through and under the Expired heading included)" % len(GRANT_ROWS),
          len(GRANT_ROWS) == 65 and not why, "%d rows; %s" % (len(GRANT_ROWS), why))
    check("W05b", "grants: the file's own text is in the pack as ONE unbroken run between the BEGIN and END lines (headings and prose too)",
          part_d(pack) == GRANTS and GRANTS.endswith("\n"), "part d is %d bytes, the file %d" % (len(part_d(pack)), len(GRANTS)))
    gsha = hashlib.sha256(GRANTS.encode("utf-8")).hexdigest()[:16]
    check("W05c", "grants: the part's first line gives the file's bytes, its row count and its sha256, and says nothing is judged",
          ("(%d bytes, %d table rows, sha256 %s)" % (len(GRANTS.encode("utf-8")), len(GRANT_ROWS), gsha)) in pack
          and "does NOT judge which grants are live" in pack, [l[:200] for l in pack.split("\n") if "table rows" in l])
    check("W05d", "grants: no sidecar and no other file is written beside the pack",
          os.listdir(os.path.join(root, "0_Brain", "wake")) == ["WAKE-wednesday.md"], os.listdir(os.path.join(root, "0_Brain", "wake")))
    check("W07", "ledger: date, headline and the Rule sentence only",
          "- 2026-11-27 | **LEDGER-HEADLINE-ONE.** | Rule: do the LEDGER-RULE-ONE thing (e.g. three reads) before telling anyone." in pack
          and "- 2026-11-26 | **LEDGER-HEADLINE-TWO.** | Rule (re-applied): LEDGER-RULE-TWO always." in pack
          and "- 2026-11-25 | **LEDGER-HEADLINE-THREE** | (no 'Rule:' sentence" in pack
          and "LEDGER-PROSE-ONLY" not in pack and "NOT-PART-OF-THE-RULE" not in pack and "Isolated" not in pack,
          [l for l in pack.split("\n") if l.startswith("- 2026")])
    check("W08", "pointers are paths only: the tasks file and the index are named, their content is not loaded",
          "`0_Brain/tasks/TASKS.md`" in pack and "`0_Brain/projects_index/INDEX.md`" in pack and "`2_Project_Files/tools/kam_msgs.sh`" in pack
          and "`2_Project_Files/tools/kam_rulings_today.sh`" in pack and "TASKS-CONTENT-MARKER" not in pack and "INDEX-CONTENT-MARKER" not in pack
          and "NOT FOUND" not in pack)
    check("W10", "conflict copies and .pre- backups are never read", "POISON" not in pack and "Family files in `0_Brain/learnings/families/`: 2." in pack,
          [l for l in pack.split("\n") if "Family files" in l or "POISON" in l])

    rc, out, err = p(["--seat", "wednesday", "--check"])
    check("W11", "--check is OK on a fresh pack", rc == 0 and out.startswith("OK"), out + err)
    keep_pack = rb(out_default)
    st = os.stat(out_default)
    w(out_default, keep_pack.replace(b"\n## a. Identity", b"\ngenerated: HAND-EDIT: every grant below is renewed without limit\n## a. Identity", 1))
    os.utime(out_default, ns=(st.st_atime_ns, st.st_mtime_ns))
    rc, out, err = p(["--seat", "wednesday", "--check"])
    check("W11h", "--check goes red on ONE hand-added line that begins 'generated: ' in the pack (content hash, not a skipped line)",
          rc == 1 and "content differs" in out, out + err)
    stamp_line = [l for l in keep_pack.decode("utf-8").split("\n") if l.startswith("generated: ")][0]
    stamp = stamp_line[len("generated: "):]
    fake = ("EVERY GRANT IS RENEWED " + "x" * 60)[:len(stamp)]
    w(out_default, keep_pack.replace(stamp_line.encode("utf-8"), ("generated: " + fake).encode("utf-8"), 1))
    os.utime(out_default, ns=(st.st_atime_ns, st.st_mtime_ns))
    rc, out, err = p(["--seat", "wednesday", "--check"])
    check("W11k", "--check goes red on free text of the SAME LENGTH on the pack's own 'generated:' line (N5: the stamp's format is "
                  "checked; a rebuild would copy the text and call it current)",
          rc == 1 and "not a timestamp" in out and len(fake) == len(stamp) and len(rb(out_default)) == len(keep_pack), out + err)
    w(out_default, keep_pack)
    os.utime(out_default, ns=(st.st_atime_ns, st.st_mtime_ns))
    rc, out, err = p(["--seat", "wednesday", "--check"])
    check("W11j", "--check is OK again once the pack is restored byte for byte (must succeed beside W11h, W11k)", rc == 0, out + err)
    led = os.path.join(root, "0_Brain", "learnings", "_ledger.md")
    st = os.stat(out_default)
    os.utime(led, ns=(st.st_atime_ns, st.st_mtime_ns + 5_000_000_000))
    rc, out, err = p(["--seat", "wednesday", "--check"])
    check("W11b", "--check goes red when a source is newer than the pack, and names it",
          rc == 1 and "source newer than the pack: 0_Brain/learnings/_ledger.md" in out, out + err)
    os.utime(led, ns=(st.st_atime_ns, st.st_mtime_ns - 5_000_000_000))
    rc, out, err = p(["--seat", "wednesday", "--check"])
    check("W11c", "--check is OK again once the source is older (must succeed beside W11b)", rc == 0, out + err)
    kam = os.path.join(root, "0_Brain", "people", "kam.md")
    w(kam, "# Kam\nKAM-MARKER changed content\n")
    os.utime(kam, ns=(st.st_atime_ns, st.st_mtime_ns - 5_000_000_000))
    rc, out, err = p(["--seat", "wednesday", "--check"])
    check("W11d", "--check goes red when content differs even though no source is newer", rc == 1 and "content differs" in out, out + err)
    rc, out, err = p(["--seat", "wednesday", "--check"], today="2026-11-28")
    check("W11e", "--check goes red when the pack was built for an earlier date", rc == 1 and "built for 2026-11-27" in out, out + err)
    rc, out, err = p(["--seat", "wednesday", "--check", "--out", os.path.join(scratch, "w", "nowhere", "WAKE.md")])
    check("W11f", "--check goes red when the pack is missing", rc == 1 and "pack missing" in out, out + err)

    alt = os.path.join(scratch, "w", "out", "alt.md")
    rc, out, err = p(["--seat", "wednesday", "--out", alt], today="2026-11-28")
    a = rb(alt).decode("utf-8") if rc == 0 else ""
    check("W15", "the date changes NO row: a build for tomorrow carries the same register, byte for byte (G07 past-dated, G09 ends today)",
          rc == 0 and part_d(a) == GRANTS and "G07-" in a and "G09-" in a and "built_for_date: 2026-11-28" in a, out + err)
    rc, out, err = p(["--seat", "wednesday", "--out", alt, "--trust-expired-heading"])
    check("W06", "--trust-expired-heading is GONE: the flag is refused as unknown (rc 2); no option switches a filter on",
          rc == 2 and "unrecognized arguments" in err, out + err)
    for tid, seat, mark in (("W13", "tuesday", "TUE-"), ("W19", "friday", "FRI-")):
        rc, out, err = p(["--seat", seat, "--out", alt])
        a = rb(alt).decode("utf-8") if rc == 0 else ""
        check(tid, "%s gets ITS OWN card, ledger and pickup, and the SAME whole register as every seat (no row is another seat's to drop)" % seat,
              rc == 0 and (mark + "TOP-RULE-ONE") in a and (mark + "LEDGER-HEADLINE-ONE") in a and (mark + "PICKUP-FIRST-BLOCK-MARKER") in a
              and "| **LEDGER-HEADLINE-ONE" not in a and part_d(a) == GRANTS and not rows_whole(a, GRANT_ROWS), out + err)

    # The second checker's 38 hostile LIVE rows and its 3 controls (round 3 dropped 30 of the 38). Nothing is judged now,
    # so all 41 are carried, for every seat.
    hroot = make_tree(os.path.join(scratch, "whost", "WEDNESDAY"))
    hrows = [r[3] for r in HOSTILE]
    glines = GRANTS.split("\n")
    at = glines.index("|---|---|---|---|") + 1
    planted = "\n".join(glines[:at] + hrows + glines[at:])
    w(os.path.join(hroot, "0_Brain", "tasks", "EXPIRING-GRANTS.md"), planted)
    bad = []
    for seat in ("wednesday", "tuesday", "friday"):
        ho_ = os.path.join(scratch, "whost", "pack-%s.md" % seat)
        rc, out, err = p(["--seat", seat, "--out", ho_], r=hroot)
        a = rb(ho_).decode("utf-8") if rc == 0 else ""
        why = rows_whole(a, hrows + GRANT_ROWS) if rc == 0 else "rc %d %s" % (rc, err[-200:])
        if why or part_d(a) != planted:
            bad.append("%s: %s" % (seat, why or "part d is not the file"))
    check("W05h", "the second checker's %d hostile rows (38 LIVE, 3 controls), planted in the register, are ALL in the pack verbatim "
                  "and in order, for all three seats" % len(hrows),
          len(hrows) == 41 and sum(1 for r in HOSTILE if r[1] == "LIVE") == 38 and not bad, bad)

    # M2: a part never shrinks to a placeholder while the build exits 0
    def faulty(name, mutate):
        r = make_tree(os.path.join(scratch, "wfail", name, "WEDNESDAY"))
        mutate(r)
        rc_, out_, err_ = p(["--seat", "wednesday"], r=r)
        last = err_.strip().split("\n")[-1] if err_.strip() else ""
        return rc_, last, os.path.exists(os.path.join(r, "0_Brain", "wake")), err_, r

    def gone(rel):
        return lambda r: shutil.move(os.path.join(r, rel), os.path.join(r, "moved_away"))

    def setto(rel, text):
        return lambda r: w(os.path.join(r, rel), text)

    card = "0_Brain/learnings/_rules_card_wednesday.md"
    gr = "0_Brain/tasks/EXPIRING-GRANTS.md"
    led = "0_Brain/learnings/_ledger.md"
    cases = [
        ("a", "the rules card is missing", gone(card), "part b (rules)"),
        ("b", "the rules card is empty", setto(card, ""), "part b (rules)"),
        ("c", "the rules card has no 'Most reinforced' section", setto(card, (CARD % {"seat": "wednesday", "tag": ""}).replace("## Most reinforced", "## Top rules")), "part b (rules)"),
        ("d", "rules_card.py is missing", gone("2_Project_Files/tools/rules_card.py"), "part b (rules)"),
        ("e", "the grants file is missing", gone(gr), "part d (grants)"),
        ("f", "the grants file is empty", setto(gr, ""), "part d (grants)"),
        ("g", "the grants table is indented by one space (rows are there, none readable)", setto(gr, "\n".join((" " + l) if l.startswith("|") else l for l in GRANTS.split("\n"))), "part d (grants)"),
        ("h", "the grants file has rows but no table header", setto(gr, "\n".join(l for l in GRANTS.split("\n") if not l.startswith(("| grant", "|---")))), "part d (grants)"),
        ("p", "the grants file is not valid UTF-8 (it could not be carried verbatim)", setto(gr, GRANTS.encode("utf-8") + b"| \xff\xfe a row | Kam | x | y |\n"), "part d (grants)"),
        ("j", "the ledger is missing", gone(led), "part e (ledger)"),
        ("k", "the ledger has no table header", setto(led, "# Ledger\n\nprose only\n"), "part e (ledger)"),
        ("l", "persona.md is empty", setto("0_Brain/identity/persona.md", ""), "part a (identity)"),
        ("m", "there is no state file and no legacy pickup", gone("0_Brain/tasks/NEXT-PICKUP.md"), "part c (state)"),
        ("n", "the legacy pickup holds no block", setto("0_Brain/tasks/NEXT-PICKUP.md", "# NEXT PICKUP\n\nno block here\n"), "part c (state)"),
    ]
    for cid, what, mutate, part in cases:
        rc_, last, wrote, err_, _ = faulty(cid, mutate)
        check("W18" + cid, "FAILED BUILD, nothing written, the part named, when " + what,
              rc_ == 2 and not wrote and last.startswith("wake_pack: FAILED — " + part) and "Traceback" not in err_, err_)

    def unreadable(r):
        os.chmod(os.path.join(r, card), 0)
    rc_, last, wrote, err_, r_ = faulty("o", unreadable)
    os.chmod(os.path.join(r_, card), 0o644)
    check("W18o", "FAILED BUILD with the path (a refusal, not a traceback) when a source is unreadable",
          rc_ == 2 and not wrote and "source unreadable: " + card in last and "Traceback" not in err_, err_)
    r_ok = make_tree(os.path.join(scratch, "wfail", "ok0", "WEDNESDAY"))
    w(os.path.join(r_ok, gr), "# Expiring grants\n\n| grant | given | EXPIRES | scope, exactly |\n|---|---|---|---|\n")
    w(os.path.join(r_ok, led), "# Ledger\n\n| Date | What happened (root cause) | Type | w | Lesson | Status |\n|---|---|---|---|---|---|\n")
    rc_, out_, err_ = p(["--seat", "wednesday"], r=r_ok)
    pk_ = os.path.join(r_ok, "0_Brain", "wake", "WAKE-wednesday.md")
    check("W18z", "an EMPTY table is believed when its header IS found: 0 grant rows and 0 ledger rows build (must succeed beside W18e to W18k)",
          rc_ == 0 and os.path.exists(pk_) and "0 table rows" in rb(pk_).decode("utf-8") and "0 rows, each reduced" in rb(pk_).decode("utf-8"), out_ + err_)
    r_ind = make_tree(os.path.join(scratch, "wfail", "indented", "WEDNESDAY"))
    ind = GRANTS.replace("| **WEDNESDAY: G08", " | **WEDNESDAY: G08")
    w(os.path.join(r_ind, gr), ind)
    rc_, out_, err_ = p(["--seat", "wednesday"], r=r_ind)
    pk_ = os.path.join(r_ind, "0_Brain", "wake", "WAKE-wednesday.md")
    pt_ = rb(pk_).decode("utf-8") if os.path.exists(pk_) else ""
    check("W18i", "an INDENTED grant row is carried like every other line (the file goes in whole, so no row can be missed by a parser)",
          rc_ == 0 and part_d(pt_) == ind and "\n | **WEDNESDAY: G08-FUTURE-DATE**" in pt_ and ("%d table rows" % len(GRANT_ROWS)) in pt_, out_ + err_)

    ho = os.path.join(TOOLS, "handover.sh")
    rc, out, err = run(["bash", ho, "write", "--stdin"], block("STATE-IN-PACK"), {"HANDOVER_TREE": root, "HANDOVER_TEST_STAMP": STAMP})
    rc2, out2, err2 = p(["--seat", "wednesday", "--out", alt])
    a = rb(alt).decode("utf-8") if rc2 == 0 else ""
    check("W04b", "state: once handover.sh has written a STATE block the pack carries it and drops the legacy pickup",
          rc == 0 and rc2 == 0 and "STATE-IN-PACK floor" in a and "PICKUP-FIRST-BLOCK-MARKER" not in a and "NO STATE FILE YET" not in a
          and "| c | `0_Brain/tasks/STATE-wednesday.md` |" in a, out + err + out2 + err2)
    nok = make_tree(os.path.join(scratch, "wnoid", "WEDNESDAY"))
    shutil.move(os.path.join(nok, "0_Brain", "identity", "persona.md"), os.path.join(nok, "persona.moved"))
    rc, out, err = p(["--seat", "wednesday"], r=nok)
    check("W16", "a missing identity file refuses (rc 2) and writes nothing",
          rc == 2 and not os.path.exists(os.path.join(nok, "0_Brain", "wake")) and "wake_pack: FAILED — part a (identity): source missing" in err, out + err)

    # N6 (and the checker's mutant Y09): the pack's state part refuses what `handover.sh check` refuses
    good = rb(os.path.join(root, "0_Brain", "tasks", "STATE-wednesday.md"))

    def crafted(body_):
        return ("---\ntype: seat-state\nseat: wednesday\nwritten: %s\nblock_bytes: %d\nblock_sha256: %s\nsource: crafted by the test\n---\n"
                % (STAMP, len(body_), hashlib.sha256(body_).hexdigest())).encode("utf-8") + body_
    nofloor = block("NOFLOOR").replace(b"## FLOOR\n- NOFLOOR floor: no seat running\n\n", b"")
    scases = [("a", "appended to by hand", good + b"\nHAND-APPENDED-LINE\n", "sha256"),
              ("b", "whose header names another seat", good.replace(b"\nseat: wednesday\n", b"\nseat: tuesday\n", 1), "names seat 'tuesday'"),
              ("c", "with NO '## FLOOR' part under a header that matches it (the checker's Y09)", crafted(nofloor), "part missing: '## FLOOR'"),
              ("d", "typed by hand, no tool header", b"## FLOOR\n- typed\n", "no tool header"),
              ("e", "holding a STACK of two blocks under a header that matches it", crafted(block("ONE") + b"\n" + block("TWO")), "appears 2 times")]
    for cid, what, data, needle in scases:
        r_ = make_tree(os.path.join(scratch, "wstate", cid, "WEDNESDAY"))
        w(os.path.join(r_, "0_Brain", "tasks", "STATE-wednesday.md"), data)
        rc_, out_, err_ = p(["--seat", "wednesday"], r=r_)
        last = err_.strip().split("\n")[-1] if err_.strip() else ""
        rcc, outc, errc = run(["bash", ho, "check"], None, {"HANDOVER_TREE": r_})
        check("W20" + cid, "FAILED BUILD, nothing written, when the STATE file is one " + what + "; `handover.sh check` refuses the same file",
              rc_ == 2 and last.startswith("wake_pack: FAILED — part c (state)") and needle in last and "Traceback" not in err_
              and not os.path.exists(os.path.join(r_, "0_Brain", "wake")) and rcc == 1 and needle in outc, err_ + outc + errc)
    rc_, out_, err_ = p(["--seat", "wednesday", "--out", alt])
    check("W20z", "the state file handover.sh itself wrote is accepted by the same build (must succeed beside W20a to W20e)",
          rc_ == 0 and b"block_sha256: " in good and "STATE-IN-PACK floor" in rb(alt).decode("utf-8"), out_ + err_)
    lone = os.path.join(scratch, "wstate", "lone_tool")
    os.makedirs(lone)
    shutil.copy(wp, os.path.join(lone, "wake_pack.py"))
    rc_, out_, err_ = run([sys.executable, os.path.join(lone, "wake_pack.py"), "--root", root, "--today", TODAY, "--seat", "wednesday", "--out", alt])
    check("W20f", "a state file that cannot be checked (no handover engine beside wake_pack.py) is a FAILED BUILD, never carried unchecked",
          rc_ == 2 and "wake_pack: FAILED — part c (state)" in err_ and "cannot be loaded" in err_, out_ + err_)
    asdir = os.path.join(scratch, "w", "out", "a_directory.md")
    os.makedirs(asdir)
    rc_, out_, err_ = p(["--seat", "wednesday", "--out", asdir])
    check("W21", "the pack path is a directory: rc 2, and nothing at all is left behind (N13)",
          rc_ == 2 and "is a directory" in err_ and os.listdir(asdir) == [] and not [f for f in os.listdir(os.path.dirname(asdir)) if ".tmp." in f],
          err_ + repr(os.listdir(os.path.dirname(asdir))))



# ── C: census ──────────────────────────────────────────────────────────────────────────────────
def group_c(scratch):
    cs = os.path.join(TOOLS, "wake_census.sh")
    wp = os.path.join(TOOLS, "wake_pack.py")
    root = make_tree(os.path.join(scratch, "c", "WEDNESDAY"))
    b = os.path.join(root, "0_Brain")
    files = ["CLAUDE.md", "0_Brain/CLAUDE.md", "0_Brain/identity/persona.md", "0_Brain/identity/voice-protocol.md", "0_Brain/people/kam.md",
             "0_Brain/learnings/_rules_card_wednesday.md", "0_Brain/learnings/_ledger.md", "0_Brain/tasks/NEXT-PICKUP.md",
             "0_Brain/tasks/EXPIRING-GRANTS.md", "0_Brain/tasks/TASKS.md", "0_Brain/projects_index/INDEX.md", "0_Brain/tasks/WEEK-INSTRUCTION.md",
             "0_Brain/daily/2026-11-26.md", "0_Brain/daily/2026-11-27.md"]
    want = sum(os.path.getsize(os.path.join(root, f)) for f in files)
    ent = sum(os.path.getsize(os.path.join(b, "projects_index", "entries", f)) for f in os.listdir(os.path.join(b, "projects_index", "entries")))
    want += ent
    noidx = want - ent - os.path.getsize(os.path.join(b, "projects_index", "INDEX.md"))
    rc, out, err = run(["bash", cs, "--seat", "wednesday", "--root", root, "--today", TODAY])
    tl = [l for l in out.split("\n") if "TOTAL, with INDEX.md and entries whole" in l]
    nl = [l for l in out.split("\n") if "TOTAL, without INDEX.md and entries" in l]
    check("C01", "census BEFORE total equals the sum of the mandated files' sizes",
          rc == 0 and tl and int(tl[0].split()[-2]) == want and int(tl[0].split()[-1]) == (want + 3) // 4, out + err)
    check("C01b", "census total without INDEX.md and entries is right", nl and int(nl[0].split()[-2]) == noidx, out + err)
    check("C02", "census says the pack is MISSING when there is none (rc 0)", rc == 0 and "pack: MISSING" in out, out)
    before = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(root) for f in fs)
    run([sys.executable, wp, "--root", root, "--today", TODAY, "--seat", "wednesday"])
    pack = os.path.join(b, "wake", "WAKE-wednesday.md")
    rc, out, err = run(["bash", cs, "--seat", "wednesday", "--root", root, "--today", TODAY])
    pb = os.path.getsize(pack) if os.path.exists(pack) else -1
    kept = sum(os.path.getsize(os.path.join(root, f)) for f in ["CLAUDE.md", "0_Brain/CLAUDE.md", "0_Brain/tasks/WEEK-INSTRUCTION.md",
                                                                 "0_Brain/daily/2026-11-26.md", "0_Brain/daily/2026-11-27.md"])
    al = [l for l in out.split("\n") if "pack + rules files" in l]
    check("C03", "census AFTER shows the pack's bytes and pack + kept reads", rc == 0 and ("%d" % pb) in out and al and int(al[0].split()[-2]) == pb + kept
          and "REDUCTION (headline, the lower figure)" in out and "| **total** |" in out, out + err)
    conf = os.path.getsize(os.path.join(b, "projects_index", "entries", "Secuura__X (conflict_on_2026-09-04).md"))
    cl = [l for l in out.split("\n") if "TOTAL, without the 1 sync-conflict / backup copies" in l]
    hl = [l for l in out.split("\n") if l.startswith("REDUCTION (headline")]
    after_b = pb + kept
    want_pct = "%d.%d%%" % ((want - conf - after_b) * 1000 // (want - conf) // 10, (want - conf - after_b) * 1000 // (want - conf) % 10)
    check("C07", "census reports BEFORE both ways (with and without sync-conflict copies) and the headline reduction is against the LOWER one",
          cl and int(cl[0].split()[-2]) == want - conf and hl and ("%d -> %d bytes" % (want - conf, after_b)) in hl[0] and want_pct in hl[0]
          and ("with the conflict copies counted (%d bytes)" % want) in out, out)
    notes = sum(os.path.getsize(os.path.join(root, f)) for f in ["0_Brain/daily/2026-11-26.md", "0_Brain/daily/2026-11-27.md"])
    ol = [l for l in out.split("\n") if "earlier notes on demand" in l]
    check("C06", "census also prints the figure with earlier notes on demand (pack + kept reads - the two notes)",
          ol and int(ol[0].split()[-2]) == pb + kept - notes, ol)
    after = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(root) for f in fs)
    check("C04", "census writes nothing (only the pack build added a file: the pack, and no sidecar)",
          [f for f in after if f not in before] == [pack], [f for f in after if f not in before])
    rc, out, err = run(["bash", cs, "--seat", "nobody", "--root", root])
    check("C05", "census refuses an unknown seat (rc 2)", rc == 2, out + err)


# ── P: the launcher proposal ───────────────────────────────────────────────────────────────────
HARNESS = r'''set -u
bash() { echo "/STUB/note/where"; }   # the prompt holds ONE backtick pair that runs note_entry.sh --where at launch: stubbed
AGENT="$1"; PROJECT_DIR="$2"; MODE="$3"; OUT="$4"
BRAIN_DIR="$PROJECT_DIR/0_Brain"; DEVMASTER="/Volumes/DevMASTER"; DEVMASTER_STATE="mounted"; DEVMASTER_VAULT="/Volumes/DevMASTER/Notes (MASTER)"
DASH_URL="http://127.0.0.1:47780"; DASH_STATE="live"; RULES_CARD_NOTE="CARD NOTE: "
case "$AGENT" in wednesday) AGENT_UPPER=WEDNESDAY ;; tuesday) AGENT_UPPER=TUESDAY ;; friday) AGENT_UPPER=FRIDAY ;; esac
@SEATFILES@
if [ "$MODE" = "with" ]; then
@HUNK_A@
fi
@REGION@
printf '%s' "$INITIAL_PROMPT" > "$OUT.legacy"
if [ "$MODE" = "with" ]; then
@HUNK_B@
fi
printf '%s' "$INITIAL_PROMPT" > "$OUT.final"
'''


def launcher_parts(path=None):
    src = open(path or LAUNCHER, encoding="utf-8").read().split("\n")
    s = [i for i, l in enumerate(src) if l == 'if [ "$AGENT" = "tuesday" ]; then' and "PICKUP_FILE=" in src[i + 1]]
    r0 = [i for i, l in enumerate(src) if l.startswith('SEAT_HOST="$(hostname')]
    r1 = [i for i, l in enumerate(src) if l == '  session-end ritual in ./CLAUDE.md."']
    if len(s) != 1 or len(r0) != 1 or len(r1) != 1:
        return None, None
    e = next(i for i in range(s[0], len(src)) if src[i] == "fi")
    return "\n".join(src[s[0]:e + 1]), "\n".join(src[r0[0]:r1[0] + 1])


def group_p(scratch):
    prop = os.path.join(TOOLS, "proposed")
    seatfiles, region = launcher_parts()
    check("P00", "the launcher's seat-files block and prompt region are found by their anchors", bool(seatfiles and region),
          "anchors moved in %s" % LAUNCHER)
    if not (seatfiles and region):
        return
    ha = open(os.path.join(prop, "launcher_hunk_A.sh"), encoding="utf-8").read()
    hb = open(os.path.join(prop, "launcher_hunk_B.sh"), encoding="utf-8").read()
    hs = os.path.join(scratch, "p", "harness.sh")
    w(hs, HARNESS.replace("@SEATFILES@", seatfiles).replace("@HUNK_A@", ha).replace("@REGION@", region).replace("@HUNK_B@", hb))

    def tree(name, **kw):
        r = make_tree(os.path.join(scratch, "p", name, "WEDNESDAY"), **kw)
        shutil.copy(os.path.join(TOOLS, "wake_pack.py"), os.path.join(r, "2_Project_Files", "wake", "wake_pack.py"))
        return r

    def go(agent, root, mode, tag):
        out = os.path.join(scratch, "p", tag)
        rc, so, se = run(["/bin/bash", hs, agent, root, mode, out])
        leg = rb(out + ".legacy") if os.path.exists(out + ".legacy") else None
        fin = rb(out + ".final") if os.path.exists(out + ".final") else None
        return rc, so, se, leg, fin

    for n, seat in (("P01", "tuesday"), ("P02", "friday")):
        root = tree("t_" + seat)
        rc0, so0, se0, leg0, fin0 = go(seat, root, "without", seat + "_without")
        rc, so, se, leg, fin = go(seat, root, "with", seat + "_with")
        check(n, "%s: the prompt with the change is byte-identical to the prompt without it" % seat,
              rc0 == 0 and rc == 0 and fin0 is not None and fin == fin0 and leg == fin0 and len(fin0) > 10000, se0 + se)
        check(n + "b", "%s: the added code prints nothing and builds no pack" % seat,
              so == "" and se == "" and not os.path.exists(os.path.join(root, "0_Brain", "wake")), so + se)
    root = tree("t_wed")
    rc, so, se, leg, fin = go("wednesday", root, "with", "wed_with")
    lt = leg.decode("utf-8") if leg else ""
    ft = fin.decode("utf-8") if fin else ""
    pack = os.path.join(root, "0_Brain", "wake", "WAKE-wednesday.md")
    check("P03", "wednesday: the pack is built and the prompt's read list becomes the pack",
          rc == 0 and os.path.isfile(pack) and fin != leg and ("read %s WHOLE" % pack) in ft and "handover.sh write --stdin" in ft
          and "EXPIRING-GRANTS.md whole" not in ft and "WHOLE, and" not in ft and "_boot_digest_by_tier.md WHOLE" not in ft, se + so)
    m1, m2 = "FIRST ACTIONS (token cost is accepted", "\n5. Read yesterday's and today's notes"
    check("P03b", "wednesday: everything before FIRST ACTIONS and from step 5 on is the legacy text, byte for byte",
          lt and ft.split("FIRST ACTIONS (WAKE PACK boot")[0] == lt.split(m1)[0] and ft.split(m2, 1)[-1] == lt.split(m2, 1)[-1]
          and "STANDING BEHAVIOUR:" in ft.split(m2, 1)[-1] and ft.count("\n5. Read yesterday's") == 1, "")
    check("P03c", "wednesday: no unexpanded variable is left in the new steps", "${" not in ft.split(m2)[0].split("FIRST ACTIONS (WAKE PACK boot")[-1]
          and "$WAKE" not in ft, [l for l in ft.split("\n") if "${" in l][:3])
    rc, so, se, leg, fin = go("wednesday", root, "without", "wed_without")
    check("P03d", "wednesday without the change: the legacy prompt (the comparison base)", rc == 0 and fin == leg and "EXPIRING-GRANTS.md whole" in fin.decode("utf-8"), se)
    big = tree("t_big", big_ledger=True)
    rc, so, se, leg, fin = go("wednesday", big, "with", "wed_big")
    U = b"ultrathink\n\n"

    def loud(leg_, fin_, why):
        """The legacy prompt whole, with the failure notice as the first lines after 'ultrathink'."""
        if not leg_ or not fin_ or not leg_.startswith(U) or not fin_.startswith(U):
            return False
        rest = leg_[len(U):]
        if not fin_.endswith(b"\n" + rest):
            return False
        notice = fin_[len(U):len(fin_) - len(rest)].decode("utf-8")
        nl = notice.split("\n")
        return (nl[0].startswith("\U0001F534\U0001F534 THE WAKE PACK FAILED AT THIS LAUNCH") and why in nl[1] and "NOT built" in nl[1]
                and "LEGACY READ LIST" in nl[2] and "YOUR FIRST ACT" in nl[3] and "tell Kam on the panel" in nl[3]
                and "fix it or raise a ticket" in nl[3] and len(nl) <= 7)
    check("P04", "wednesday, pack over budget: the legacy prompt whole, and its FIRST lines say the pack failed, why, and what to do first",
          rc == 0 and loud(leg, fin, "wake_pack: FAILED — over budget") and "WAKE PACK NOT BUILT" in so
          and not os.path.exists(os.path.join(big, "0_Brain", "wake")), so + se)
    nop = make_tree(os.path.join(scratch, "p", "t_notool", "WEDNESDAY"))
    shutil.move(os.path.join(nop, "2_Project_Files", "wake"), os.path.join(nop, "2_Project_Files", "wake_moved"))
    rc, so, se, leg, fin = go("wednesday", nop, "with", "wed_notool")
    check("P04b", "wednesday, wake_pack.py absent: loud in the prompt's first lines; legacy reads", rc == 0 and loud(leg, fin, "wake_pack.py is missing"), so + se)
    bad = tree("t_badsrc")
    shutil.move(os.path.join(bad, "0_Brain", "tasks", "EXPIRING-GRANTS.md"), os.path.join(bad, "grants_moved"))
    rc, so, se, leg, fin = go("wednesday", bad, "with", "wed_badsrc")
    check("P04c", "wednesday, a source missing (the grants file): the build fails and the prompt's first lines name the part",
          rc == 0 and loud(leg, fin, "wake_pack: FAILED — part d (grants): source missing") and not os.path.exists(os.path.join(bad, "0_Brain", "wake")), so + se)
    liar = tree("t_liar")
    w(os.path.join(liar, "2_Project_Files", "wake", "wake_pack.py"), "print('pretend/path  bytes: 1  ~tokens: 1 of 60000')\n")
    rc, so, se, leg, fin = go("wednesday", liar, "with", "wed_liar")
    check("P16", "wednesday, the build exits 0 but there is NO pack file: not trusted; loud fallback (m2)",
          rc == 0 and loud(leg, fin, "exited 0 but there is no pack"), so + se)
    hs3 = os.path.join(scratch, "p", "harness_reworded.sh")
    w(hs3, HARNESS.replace("@SEATFILES@", seatfiles).replace("@HUNK_A@", ha)
      .replace("@REGION@", region.replace("FIRST ACTIONS (token cost is accepted", "FIRST THINGS (token cost is accepted")).replace("@HUNK_B@", hb))
    rw = tree("t_reworded")
    o3 = os.path.join(scratch, "p", "wed_reworded")
    rc, so, se = run(["/bin/bash", hs3, "wednesday", rw, "with", o3])
    check("P17", "wednesday, the launcher's prompt reworded so a slice marker is gone: loud fallback naming the markers, never a broken prompt",
          rc == 0 and loud(rb(o3 + ".legacy"), rb(o3 + ".final"), "slice markers were not found"), so + se)
    for n_, seat_ in (("P15", "tuesday"), ("P15b", "friday")):
        r_ = make_tree(os.path.join(scratch, "p", "t_fail_" + seat_, "WEDNESDAY"))
        rc, so, se, leg, fin = go(seat_, r_, "with", seat_ + "_nopack")
        check(n_, "%s with no wake_pack.py at all: no notice, no output, the prompt untouched (the loud fallback is the Wednesday seat's only)" % seat_,
              rc == 0 and fin == leg and so == "" and se == "" and b"WAKE PACK" not in fin, so + se)

    # the checker's Q14 and Y11: "never boots on a stale or an empty pack" had no test
    old = tree("t_oldpack")
    rc, so, se, leg, fin = go("wednesday", old, "with", "wed_oldpack_1")
    oldpack = os.path.join(old, "0_Brain", "wake", "WAKE-wednesday.md")
    built = rc == 0 and os.path.isfile(oldpack) and fin != leg
    shutil.move(os.path.join(old, "0_Brain", "tasks", "EXPIRING-GRANTS.md"), os.path.join(old, "grants_moved"))
    rc, so, se, leg, fin = go("wednesday", old, "with", "wed_oldpack_2")
    check("P21", "wednesday, the build FAILS while an OLDER pack is still on disk: the exit code decides; loud fallback, never a boot on the stale pack (Q14)",
          built and rc == 0 and os.path.getsize(oldpack) > 1000 and loud(leg, fin, "wake_pack: FAILED — part d (grants): source missing")
          and "WAKE PACK boot" not in (fin or b"").decode("utf-8"), so + se)
    emp = tree("t_emptypack")
    w(os.path.join(emp, "2_Project_Files", "wake", "wake_pack.py"),
      "import os\nr = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n"
      "p = os.path.join(r, '0_Brain', 'wake', 'WAKE-wednesday.md')\nos.makedirs(os.path.dirname(p), exist_ok=True)\n"
      "open(p, 'w').close()\nprint(p + '  bytes: 0  ~tokens: 0 of 60000')\n")
    rc, so, se, leg, fin = go("wednesday", emp, "with", "wed_emptypack")
    check("P22", "wednesday, the build exits 0 and leaves an EMPTY pack file: not trusted; loud fallback, never a boot on an empty pack (Y11)",
          rc == 0 and os.path.isfile(os.path.join(emp, "0_Brain", "wake", "WAKE-wednesday.md"))
          and loud(leg, fin, "exited 0 but there is no pack (or an empty one)"), so + se)


    diff_path = os.path.join(prop, "01_launcher_boot_prompt.diff")
    rc, so, se = run([sys.executable, os.path.join(prop, "build_launcher_diff.py"), "--launcher", LAUNCHER])
    stored = open(diff_path, encoding="utf-8").read() if os.path.exists(diff_path) else ""
    check("P05", "the stored diff is what the two hunk files give against today's launcher", rc == 0 and so == stored and stored, se)
    body = [l for l in stored.split("\n") if not l.startswith(("---", "+++"))]
    check("P06", "the diff is additive only: zero removed lines", stored and not [l for l in body if l.startswith("-")])
    copy = os.path.join(scratch, "p", "Launch_copy.command")
    shutil.copy(LAUNCHER, copy)
    before = sha(LAUNCHER)
    rc, so, se = run(["patch", "-s", copy, diff_path])
    rc2, so2, se2 = run(["/bin/bash", "-n", copy])
    pt = open(copy, encoding="utf-8").read()
    check("P07", "the diff applies cleanly to a scratch COPY of the launcher, which then passes bash -n and holds both hunks",
          rc == 0 and rc2 == 0 and ha in pt and hb in pt and sha(LAUNCHER) == before, so + se + se2)
    shape = True
    for name, text, first in (("A", ha, 'WAKE_PACK_OK=0; WAKE_PACK=""; WAKE_SUMMARY=""; WAKE_FAIL=""'), ("B", hb, 'if [ "$AGENT" = "wednesday" ]; then')):
        code = [l for l in text.split("\n") if l.strip() and not l.startswith("#")]
        guards = [l for l in code if l.startswith('if [ "$AGENT" = "wednesday" ]')]
        shape = shape and code[0].startswith(first) and code[-1] == "fi" and len(guards) == 1 and code.count("fi") == 1
        if name == "A":
            shape = shape and code[1] == 'if [ "$AGENT" = "wednesday" ]; then'
    check("P08", "each hunk is one 'if AGENT = wednesday' block (hunk A preceded only by four default assignments)", shape)
    group_p_texts(prop)
    # P12: the daily-notes switch is ONE line of hunk B
    one = '\n  WAKE_NOTES="whole"\n'   # the assignment line (the comment above it also quotes the setting)
    hb2 = hb.replace(one, '\n  WAKE_NOTES="ondemand"\n')
    hs2 = os.path.join(scratch, "p", "harness_ondemand.sh")
    w(hs2, HARNESS.replace("@SEATFILES@", seatfiles).replace("@HUNK_A@", ha).replace("@REGION@", region).replace("@HUNK_B@", hb2))
    r12 = tree("t_notes")
    o12 = os.path.join(scratch, "p", "wed_ondemand")
    rc, so, se = run(["/bin/bash", hs2, "wednesday", r12, "with", o12])
    f12 = rb(o12 + ".final").decode("utf-8") if os.path.exists(o12 + ".final") else ""
    l12 = rb(o12 + ".legacy").decode("utf-8") if os.path.exists(o12 + ".legacy") else ""
    m6 = "\n6. If DevMASTER is mounted: "
    check("P12", "daily notes on demand is a ONE-line change (WAKE_NOTES): step 5 is replaced, the legacy text from step 6 is reused byte for byte",
          hb.count(one) == 1 and rc == 0 and "5. Read yesterday's and today's notes" not in f12 and "\n5. Today's note: create it" in f12
          and "Earlier notes are read ON DEMAND" in f12 and f12.count(m6) == 1 and l12 and f12.split(m6, 1)[-1] == l12.split(m6, 1)[-1]
          and "STANDING BEHAVIOUR:" in f12 and "${" not in f12.split(m6)[0].split("FIRST ACTIONS (WAKE PACK boot")[-1], se + so)
    check("P12b", "the default (WAKE_NOTES=whole) keeps Kam's rule: the legacy step 5 is in the Wednesday prompt",
          "\n5. Read yesterday's and today's notes in THIS SEAT'S OWN note directory" in ft and "Earlier notes are read ON DEMAND" not in ft)
    # P13: proposal 7's replacement leaves doctor.sh syntactically valid (scratch copy)
    import re as _re
    t7 = open(os.path.join(prop, "07_doctor_pickup_warning.md"), encoding="utf-8").read()
    old7 = _re.search(r"```old\n(.*?)\n```", t7, _re.S).group(1)
    new7 = _re.search(r"```new\n(.*?)\n```", t7, _re.S).group(1)
    doc = open(os.path.join(REAL_ROOT, "2_Project_Files", "doctor.sh"), encoding="utf-8").read()
    d7 = os.path.join(scratch, "p", "doctor_copy.sh")
    w(d7, doc.replace(old7, new7))
    rc, so, se = run(["/bin/bash", "-n", d7])
    check("P13", "proposal 7 applied to a scratch copy of doctor.sh passes bash -n", doc.count(old7) == 1 and rc == 0, se)
    # P14: proposal 9 (the backtick fix) and proposal 1 together, on a scratch copy
    t9 = open(os.path.join(prop, "09_prompt_backtick.md"), encoding="utf-8").read()
    old9 = _re.search(r"```old\n(.*?)\n```", t9, _re.S).group(1)
    new9 = _re.search(r"```new\n(.*?)\n```", t9, _re.S).group(1)
    lt9 = open(LAUNCHER, encoding="utf-8").read()
    l9 = os.path.join(scratch, "p", "Launch_backtick_fixed.command")
    w(l9, lt9.replace(old9, new9))
    l9p = os.path.join(scratch, "p", "Launch_backtick_fixed_patched.command")
    rc, so, se = run([sys.executable, os.path.join(prop, "build_launcher_diff.py"), "--launcher", l9, "--patched-out", l9p])
    rc2, so2, se2 = run(["/bin/bash", "-n", l9p])
    sf9, rg9 = launcher_parts(l9)
    hs9 = os.path.join(scratch, "p", "harness_backtick.sh")
    w(hs9, HARNESS.replace("@SEATFILES@", sf9 or "").replace("@HUNK_A@", ha).replace("@REGION@", rg9 or "exit 9").replace("@HUNK_B@", hb)
      .replace('bash() { echo "/STUB/note/where"; }', 'bash() { echo "THE-LAUNCHER-RAN-IT"; }'))
    r9 = tree("t_backtick")
    o9 = os.path.join(scratch, "p", "wed_backtick")
    rc3, so3, se3 = run(["/bin/bash", hs9, "wednesday", r9, "with", o9])
    f9 = rb(o9 + ".final").decode("utf-8") if os.path.exists(o9 + ".final") else ""
    check("P14", "proposal 9: with the two backticks escaped the prompt carries the command as text, nothing is run at launch, and proposal 1 still applies",
          lt9.count(old9) == 1 and rc == 0 and rc2 == 0 and rc3 == 0 and "`bash 2_Project_Files/tools/note_entry.sh --where` prints today's" in f9
          and "THE-LAUNCHER-RAN-IT" not in f9 and "FIRST ACTIONS (WAKE PACK boot" in f9, se + se2 + se3)
    check("P14b", "today, without proposal 9, the launcher runs that command and pastes its output into the prompt (what the proposal describes)",
          "/STUB/note/where prints today's" in lt and "`bash 2_Project_Files" not in lt)
    nf = make_tree(os.path.join(scratch, "p", "t_ptr", "WEDNESDAY"))
    shutil.move(os.path.join(nf, "2_Project_Files", "tools", "kam_msgs.sh"), os.path.join(nf, "kam_msgs.moved"))
    rc, so, se = run([sys.executable, os.path.join(TOOLS, "wake_pack.py"), "--root", nf, "--today", TODAY, "--seat", "wednesday"])
    pk = os.path.join(nf, "0_Brain", "wake", "WAKE-wednesday.md")
    check("P09", "a pointer whose file is gone is marked NOT FOUND in the pack (not silently listed)",
          rc == 0 and "`2_Project_Files/tools/kam_msgs.sh`  (NOT FOUND in this tree)" in rb(pk).decode("utf-8"), so + se)


def group_p_texts(prop):
    """P10/P11: every 'old' block in a text proposal is in its target exactly once; no 'new' block is applied yet."""
    import re
    bad, n_old = [], 0
    olds = {}
    news = {}
    for name in ("02_root_CLAUDE_md.md", "03_brain_CLAUDE_md.md", "06_wrap_step.md", "05_gitignore.md",
                 "07_doctor_pickup_warning.md", "08_nas_staleness.md", "09_prompt_backtick.md", "10_stuart_weekly.md",
                 "FOR-KAM_lesson-load-ruling.md"):
        text = open(os.path.join(prop, name), encoding="utf-8").read()
        m = re.search(r"^TARGET: `([^`]+)`", text, re.M)
        if not m:
            bad.append("%s: no TARGET line" % name)
            continue
        target = open(os.path.join(REAL_ROOT, m.group(1)), encoding="utf-8").read()
        olds[name] = re.findall(r"```old\n(.*?)\n```", text, re.S)
        news[name] = re.findall(r"```new\n(.*?)\n```", text, re.S)
        for old in re.findall(r"```old\n(.*?)\n```", text, re.S):
            n_old += 1
            if target.count(old) != 1:
                bad.append("%s: an old block is in %s %d times" % (name, m.group(1), target.count(old)))
        for new in re.findall(r"```new\n(.*?)\n```", text, re.S):
            if new in target:
                bad.append("%s: a new block is ALREADY in %s" % (name, m.group(1)))
    check("P10", "every 'old' block of the text proposals is in its target file exactly once (%d blocks); none is applied" % n_old,
          not bad and n_old == 10, bad)
    kam1, kam2 = "the full lesson load STAYS", "**All** of `learnings/`"
    scoped = "**On a seat that boots on a wake pack**"
    check("P18", "proposals 2 and 3 are scoped in words to a seat on a pack, add text only, and leave Kam's lesson-load sentence in place (it goes to FOR-KAM)",
          not any(kam1 in o or "Read ALL of" in o for o in olds["02_root_CLAUDE_md.md"]) and not any(kam2 in o for o in olds["03_brain_CLAUDE_md.md"])
          and scoped in news["02_root_CLAUDE_md.md"][0] and scoped in news["03_brain_CLAUDE_md.md"][0]
          and all(l in news["02_root_CLAUDE_md.md"][0].split("\n") for l in olds["02_root_CLAUDE_md.md"][0].split("\n"))
          and all(l in news["03_brain_CLAUDE_md.md"][0].split("\n") for l in olds["03_brain_CLAUDE_md.md"][0].split("\n"))
          and "follow" in news["02_root_CLAUDE_md.md"][0] and "exactly as written" in news["03_brain_CLAUDE_md.md"][0]
          and any(kam1 in o for o in olds["FOR-KAM_lesson-load-ruling.md"]),
          [o[:60] for o in olds["02_root_CLAUDE_md.md"]])
    gi = news["05_gitignore.md"][0].split("\n")
    check("P19", "the gitignore proposal ignores only generated packs, temp files and lock directories (a set-aside '.stale-' one too, N3); "
                 "never the lane's whole out/ directory",
          "2_Project_Files/wake/out/WAKE-*" in gi and "2_Project_Files/wake/out/" not in gi and "0_Brain/tasks/STATE-*.lock.d*" in gi
          and "0_Brain/tasks/STATE-*.lock.d/" not in gi and not any(l.strip() in ("0_Brain/tasks/", "0_Brain/tasks/STATE-*") for l in gi), gi)
    n2, n3, n6 = news["02_root_CLAUDE_md.md"][0], news["03_brain_CLAUDE_md.md"][0], " ".join(news["06_wrap_step.md"][0].split())
    check("P23", "proposals 2 and 3 no longer tell the pack seat to skip Kam's lesson-load step before he has ruled (N9)",
          "in place of steps 1 and 3 below" in " ".join(n2.split()) and "for step 2 see the question put to Kam" in " ".join(n2.split())
          and "steps 1 to 3" not in n2 and "items 1, 2, 4 and 5 below" in " ".join(n3.split())
          and "for item 3 see the question put to Kam" in " ".join(n3.split()) and "items 1 to 5" not in n3, [n2[:300], n3[:300]])
    check("P24", "proposal 6 tells LOCK BUSY (run it again) from STALE LOCK (run the recovery line first), and names rc 6 (N3)",
          "LOCK BUSY" in n6 and "STALE LOCK" in n6 and "recovery line" in n6 and "rc 6" in n6 and "simply run again" not in n6, n6[-700:])
    t9 = open(os.path.join(prop, "09_prompt_backtick.md"), encoding="utf-8").read()
    dtext = open(os.path.join(prop, "01_launcher_boot_prompt.diff"), encoding="utf-8").read()
    check("P20", "proposal 9 is marked all-seats and is not in this round's launcher diff",
          "ALL SEATS: needs Tuesday's and Friday's agreement" in t9 and "`" not in "\n".join(l[1:] for l in dtext.split("\n") if l.startswith("+") and not l.startswith("+#"))
          and "never hardcode it" not in dtext)
    doc = open(os.path.join(REAL_ROOT, "2_Project_Files", "doctor.sh"), encoding="utf-8").read()
    check("P11", "the doctor proposal's insertion anchor and the helpers it uses exist in doctor.sh; the snippet is not applied",
          doc.count('RC="$PROJECT_DIR/2_Project_Files/tools/rules_card.py"') == 1 and "_DOC_AGENT=" in doc and "\nok()" in doc and "\nwarn()" in doc
          and "wake_pack.py" not in doc)


# ── S: handover.sh seed --from-legacy (the cut-over helper) ─────────────────────────────────────
SEED_LEGACY = """---
type: pickup
---

# NEXT PICKUP (fixture)

## NEWEST-BLOCK-HEADING checkpoint 11:57
- **FLOOR (2 seats):** SEED-FLOOR-LINE
- **WED-170 (priority):** SEED-UNMAPPED-LINE
  continuation SEED-CONT-LINE
- **CARDS:** SEED-CARDS-LINE
- **OPEN for Kam:** SEED-FORKAM-LINE
- **OWED (carried):** SEED-OWED-LINE
- **NEXT (first work):** SEED-NEXT-LINE
- plain bullet SEED-PLAIN-LINE%s

## OLDER block
- **FLOOR:** SEED-OLDER-MUST-NOT-APPEAR

## \U0001F534 STATE 10:00 an older dated block whose heading mentions OWED
- SEED-DATED-BLOCK-MENTIONING-OWED

## OWED (in order, after the floor)
- SEED-STANDING-OWED-LINE-1
- SEED-STANDING-OWED-LINE-2

## STANDING (unchanged; applies to every block)
- SEED-STANDING-LINE%s
"""


def split_parts(text):
    parts, cur = {}, None
    for l in text.split("\n"):
        if l.startswith("## "):
            cur = l[3:].strip()
            parts[cur] = []
        elif cur:
            parts[cur].append(l)
    return dict((k, "\n".join(v)) for k, v in parts.items())


def group_s(scratch):
    ho = os.path.join(TOOLS, "handover.sh")
    base = os.path.join(scratch, "s")

    def tree(name, legacy=None, folder="WEDNESDAY", fname="NEXT-PICKUP.md"):
        r = os.path.join(base, name, folder)
        os.makedirs(os.path.join(r, "0_Brain", "tasks"))
        if legacy is not None:
            w(os.path.join(r, "0_Brain", "tasks", fname), legacy)
        return r, os.path.join(r, "0_Brain", "tasks")

    def sd(r, args, extra=None):
        e = {"HANDOVER_TREE": r, "HANDOVER_TEST_STAMP": STAMP}
        e.update(extra or {})
        return run(["bash", ho] + args, None, e)

    r, t = tree("a", SEED_LEGACY % ("", ""))
    leg_sha = sha(os.path.join(t, "NEXT-PICKUP.md"))
    rc, out, err = sd(r, ["seed", "--from-legacy"])
    pp = split_parts(out)
    check("S01", "seed is DRY by default: prints the block, writes nothing", rc == 0 and "DRY" in err and os.listdir(t) == ["NEXT-PICKUP.md"], out + err)
    check("S01b", "seed maps the newest legacy block into the five parts by each bullet's label",
          list(pp.keys()) == ["FLOOR", "FIRST WORK", "OWED", "OPEN CARDS", "GRANTS IN PLAY"]
          and "SEED-FLOOR-LINE" in pp["FLOOR"] and "NEWEST-BLOCK-HEADING checkpoint 11:57" in pp["FLOOR"]
          and "SEED-NEXT-LINE" in pp["FIRST WORK"] and "SEED-OWED-LINE" in pp["OWED"]
          and "SEED-CARDS-LINE" in pp["OPEN CARDS"] and "SEED-FORKAM-LINE" in pp["OPEN CARDS"]
          and "none stated in the legacy block" in pp["GRANTS IN PLAY"], pp)
    check("S01c", "seed keeps what it cannot map (unknown label, its continuation line, a plain bullet) under FIRST WORK",
          "SEED-UNMAPPED-LINE" in pp.get("FIRST WORK", "") and "SEED-CONT-LINE" in pp.get("FIRST WORK", "") and "SEED-PLAIN-LINE" in pp.get("FIRST WORK", ""), pp)
    body = [l for l in (SEED_LEGACY % ("", "")).split("## NEWEST")[1].split("## OLDER")[0].split("\n")[1:] if l.strip()]
    check("S06", "seed loses no line of the newest block and takes nothing from an older block",
          all(l in out for l in body) and "SEED-OLDER-MUST-NOT-APPEAR" not in out and "OLDER block" not in out, [l for l in body if l not in out])
    legacy_lines = (SEED_LEGACY % ("", "")).split("\n")
    ln_owed = legacy_lines.index("## OWED (in order, after the floor)") + 1
    ln_stand = legacy_lines.index("## STANDING (unchanged; applies to every block)") + 1
    check("S09", "seed CARRIES the legacy file's standing sections: '## OWED' into OWED, '## STANDING' as a named line under FIRST WORK",
          "SEED-STANDING-OWED-LINE-1" in pp.get("OWED", "") and "SEED-STANDING-OWED-LINE-2" in pp.get("OWED", "")
          and ("OWED, carried from the legacy file's standing section (`NEXT-PICKUP.md` line %d" % ln_owed) in pp.get("OWED", "")
          and "SEED-STANDING-LINE" in pp.get("FIRST WORK", "")
          and ("STANDING, carried from the legacy file's standing section (`NEXT-PICKUP.md` line %d" % ln_stand) in pp.get("FIRST WORK", ""), pp)
    check("S09b", "the dry report says what it took from where, by line number, and what it did NOT carry",
          ("standing section at line %d" % ln_owed) in err and ("standing section at line %d" % ln_stand) in err
          and "newest block: heading line 7, body lines 8 to" in err and "-> FLOOR: lines 8" in err
          and "NOT carried: line" in err and "mentions OWED or STANDING but is a dated block" in err
          and "SEED-DATED-BLOCK-MENTIONING-OWED" not in out, err)
    rc, o2, e2 = sd(r, ["seed", "--from-legacy", "--run"])
    rc3, shown, _ = sd(r, ["show"])
    rc4, o4, e4 = sd(r, ["check"])
    check("S02", "seed --run writes that same block as the FIRST state block; check is OK; the legacy file is untouched",
          rc == 0 and rc3 == 0 and shown == out and rc4 == 0 and sha(os.path.join(t, "NEXT-PICKUP.md")) == leg_sha
          and sorted(os.listdir(t)) == ["NEXT-PICKUP.md", "STATE-wednesday.md"], o2 + e2 + o4 + e4)
    before = rb(os.path.join(t, "STATE-wednesday.md"))
    rc, o, e = sd(r, ["seed", "--from-legacy"])
    rc2, o2, e2 = sd(r, ["seed", "--from-legacy", "--run"])
    check("S03", "seed REFUSES when a state file already exists (dry and --run), and changes nothing",
          rc == 3 and rc2 == 3 and "already exists" in e and "already exists" in e2 and rb(os.path.join(t, "STATE-wednesday.md")) == before
          and sorted(os.listdir(t)) == ["NEXT-PICKUP.md", "STATE-wednesday.md"], e + e2)

    r, t = tree("b", SEED_LEGACY % ("\n- **OWED (older):** left at 12:1x by the earlier seat", ""))
    rc, o, e = sd(r, ["seed", "--from-legacy", "--run"])
    hdr = rb(os.path.join(t, "STATE-wednesday.md")).split(b"\n---\n")[0].decode("utf-8") if rc == 0 else ""
    rc2, o2, e2 = run(["bash", ho, "write", "--stdin"], block("AFTER-SEED"), {"HANDOVER_TREE": r, "HANDOVER_TEST_STAMP": STAMP})
    arp = os.path.join(t, "STATE-wednesday-archive.md")
    ar = rb(arp).decode("utf-8") if os.path.exists(arp) else ""
    check("S04", "a legacy block that carries an x-digit clock is seeded verbatim with the reason recorded, and the reason reaches the archive heading",
          rc == 0 and "xclock_override: seeded verbatim from the legacy pickup's newest block" in hdr and rc2 == 0
          and "| x-clock override: seeded verbatim from the legacy pickup's newest block" in ar and "12:1x" in ar, o + e + o2 + e2)

    r, t = tree("c")
    rc, o, e = sd(r, ["seed", "--from-legacy", "--run"])
    check("S05", "seed REFUSES when there is no legacy pickup (rc 3), nothing written", rc == 3 and "no legacy pickup" in e and os.listdir(t) == [], o + e)
    rc, o, e = sd(r, ["seed"])
    rc2, o2, e2 = run(["bash", ho, "write", "--stdin", "--run"], block("X"), {"HANDOVER_TREE": r, "HANDOVER_TEST_STAMP": STAMP})
    check("S05b", "seed without --from-legacy, and --run on write, are usage refusals (rc 2)", rc == 2 and rc2 == 2 and os.listdir(t) == [], e + e2)

    r, t = tree("d", SEED_LEGACY % ("", ""), folder="TUESDAY", fname="NEXT-PICKUP-TUESDAY.md")
    rc, o, e = sd(r, ["seed", "--from-legacy", "--run"])
    check("S07", "the seat's own legacy file is used: a TUESDAY tree seeds STATE-tuesday.md from NEXT-PICKUP-TUESDAY.md",
          rc == 0 and sorted(os.listdir(t)) == ["NEXT-PICKUP-TUESDAY.md", "STATE-tuesday.md"], o + e)

    r, t = tree("e", SEED_LEGACY % ("\n- **OWED (huge):** " + "z" * 11000, ""))
    rc, o, e = sd(r, ["seed", "--from-legacy"])
    rc2, o2, e2 = sd(r, ["seed", "--from-legacy", "--run"])
    check("S08", "a legacy block over the cap: the dry run says --run WOULD BE REFUSED, and --run is refused (rc 3), nothing written",
          rc == 0 and "WOULD BE REFUSED" in e and rc2 == 3 and os.listdir(t) == ["NEXT-PICKUP.md"], e + e2)

    r, t = tree("f", SEED_LEGACY % ("", "\n- " + "s" * 9500))
    rc, o, e = sd(r, ["seed", "--from-legacy"])
    rc2, o2, e2 = sd(r, ["seed", "--from-legacy", "--run"])
    check("S10", "standing sections that do not fit the cap: the seed REFUSES (rc 3) with the list to place by hand, nothing written",
          rc == 0 and "WOULD BE REFUSED" in e and rc2 == 3 and "place them by hand" in e2 and "`## STANDING (unchanged; applies to every block)`" in e2
          and "`## OWED (in order, after the floor)`" in e2 and os.listdir(t) == ["NEXT-PICKUP.md"], e + e2)
    r, t = tree("g", (SEED_LEGACY % ("", "")).split("## OWED (in order")[0].split("## \U0001F534 STATE")[0])
    rc, o, e = sd(r, ["seed", "--from-legacy"])
    check("S11", "a legacy file with no standing section seeds as before and says there is none (must succeed beside S09)",
          rc == 0 and "standing sections" in e and "none in the file" in e and "carried from the legacy" not in o, o + e)


# ── D: the doctor proposal ─────────────────────────────────────────────────────────────────────
DOCTOR_HARNESS = r"""set -uo pipefail
PROJECT_DIR="$1"; _DOC_AGENT="$2"
ok()   { printf 'OK: %s\n' "$1"; }
warn() { printf 'WARN: %s | %s\n' "$1" "${2:-}"; }
@SNIPPET@
"""


def install_tools(root):
    """Put the tools under test (and the two seat libraries they source) into a fixture tree."""
    pf = os.path.join(root, "2_Project_Files")
    for f in ("handover.sh", "handover_core.py", "wake_pack.py"):
        shutil.copy(os.path.join(TOOLS, f), os.path.join(pf, "wake", f))
    for rel in ("tools/seat_note.sh", "fleet/cockpit/seat_resolve.sh"):
        os.makedirs(os.path.dirname(os.path.join(pf, rel)), exist_ok=True)
        shutil.copy(os.path.join(REAL_ROOT, "2_Project_Files", rel), os.path.join(pf, rel))
    return os.path.join(pf, "wake")


def group_d(scratch):
    snip = open(os.path.join(TOOLS, "proposed", "doctor_check_snippet.sh"), encoding="utf-8").read()
    hs = os.path.join(scratch, "d", "doctor_harness.sh")
    w(hs, DOCTOR_HARNESS.replace("@SNIPPET@", snip))
    root = make_tree(os.path.join(scratch, "d", "WEDNESDAY"))
    lane = install_tools(root)

    def doc():
        return run(["/bin/bash", hs, root, "wednesday"])

    rc, out, err = doc()
    check("D01", "doctor snippet: a seat with no pack and no state file prints nothing", rc == 0 and out == "" and err == "", out + err)
    run([sys.executable, os.path.join(lane, "wake_pack.py"), "--seat", "wednesday"])
    rc0, o0, e0 = run(["bash", os.path.join(lane, "handover.sh"), "write", "--stdin"], block("D"))
    run([sys.executable, os.path.join(lane, "wake_pack.py"), "--seat", "wednesday"])
    rc, out, err = doc()
    check("D02", "doctor snippet: a fresh pack and a tool-written block give two OK lines and no warning",
          rc0 == 0 and rc == 0 and out.count("OK: ") == 2 and "WARN" not in out and "wake pack current" in out and "one block" in out, out + err + e0)
    led = os.path.join(root, "0_Brain", "learnings", "_ledger.md")
    st = os.stat(os.path.join(root, "0_Brain", "wake", "WAKE-wednesday.md"))
    os.utime(led, ns=(st.st_atime_ns, st.st_mtime_ns + 5_000_000_000))
    rc, out, err = doc()
    check("D03", "doctor snippet: a pack older than a source warns and names the rebuild command",
          "WARN: wake pack STALE" in out and "source newer than the pack" in out and "wake_pack.py --seat wednesday" in out, out + err)
    with open(os.path.join(root, "0_Brain", "tasks", "STATE-wednesday.md"), "ab") as f:
        f.write(b"\n## CHECKPOINT stacked by hand\n- text\n")
    rc, out, err = doc()
    check("D04", "doctor snippet: a block stacked onto the state file by hand warns", "WARN: handover is NOT one clean block" in out, out + err)
    tue = make_tree(os.path.join(scratch, "d", "tue", "TUESDAY"))
    install_tools(tue)
    w(os.path.join(tue, "0_Brain", "tasks", "STATE-wednesday.md"), "the Wednesday seat's state file, synced by git\n")
    os.makedirs(os.path.join(tue, "0_Brain", "wake"))
    w(os.path.join(tue, "0_Brain", "wake", "WAKE-wednesday.md"), "a stray pack of another seat\n")
    rc, out, err = run(["/bin/bash", hs, tue, "wednesday"])
    check("D05", "doctor snippet: a TUESDAY tree holding the Wednesday seat's files prints nothing (the seat comes from the tree)",
          rc == 0 and out == "" and err == "", out + err)
    cut = make_tree(os.path.join(scratch, "d", "cut", "WEDNESDAY"))
    cl_ = install_tools(cut)
    run(["bash", os.path.join(cl_, "handover.sh"), "write", "--stdin"], block("CUTOVER"))
    rc, out, err = run(["/bin/bash", hs, cut, "wednesday"])
    check("D06", "doctor snippet: a seat that is cut over (state file exists) with NO pack is warned, with the build command",
          "WARN: NO wake pack for the wednesday seat" in out and "wake_pack.py --seat wednesday" in out and "OK: " in out, out + err)
    els = make_tree(os.path.join(scratch, "d", "x", "elsewhere"))
    install_tools(els)
    rc, out, err = run(["/bin/bash", hs, els, "wednesday"])
    check("D07", "doctor snippet: when handover.sh cannot resolve the seat its refusal is SHOWN in a warning, never discarded",
          "WARN: handover.sh cannot tell which seat this tree is" in out and "REFUSED" in out and "were NOT run" in out, out + err)
    lk = make_tree(os.path.join(scratch, "d", "lock", "WEDNESDAY"))
    install_tools(lk)
    rc0, out0, err0 = run(["/bin/bash", hs, lk, "wednesday"])
    lockp = os.path.join(lk, "0_Brain", "tasks", "STATE-wednesday.lock.d")
    os.makedirs(lockp)
    w(os.path.join(lockp, "owner"), "pid: 1\nhost: somewhere\nstarted: earlier\n")
    rc, out, err = run(["/bin/bash", hs, lk, "wednesday"])
    rec = [x for x in out.replace(" mv -n '", "\nmv -n '").split("\n") if x.startswith("mv -n '")]
    check("D08", "doctor snippet: a standing handover lock directory is WARNED at boot with the exact recovery line, and the seat is told "
                 "it may run it itself (N3); with no lock directory the snippet says nothing about one",
          rc == 0 and "lock" not in out0 and "WARN: a handover write lock is standing" in out and "STATE-wednesday.lock.d" in out
          and len(rec) == 1 and rec[0].startswith("mv -n '%s' '%s.stale-" % (lockp, lockp)) and "the seat may run this itself" in out
          and "pid: 1" in out and os.path.isdir(lockp), out0 + out + err)
    os.rename(lockp, lockp + ".stale-20261127-000000")
    rc, out, err = run(["/bin/bash", hs, lk, "wednesday"])
    check("D08b", "doctor snippet: once the lock has been set aside by the recovery line the warning is gone (must succeed beside D08)",
          rc == 0 and "lock is standing" not in out, out + err)


# ── R: the write lock, races, and a death part-way (the checker's Blocker B1 and its missed mutants) ──
def group_r(scratch):
    import socket
    import time
    ho = os.path.join(TOOLS, "handover.sh")
    core = os.path.join(TOOLS, "handover_core.py")
    wrap = os.path.join(HERE, "wrap_replace.py")
    base = os.path.join(scratch, "r")

    def tree(name):
        r = os.path.join(base, name, "WEDNESDAY")
        os.makedirs(os.path.join(r, "0_Brain", "tasks"))
        return r, os.path.join(r, "0_Brain", "tasks")

    def envfor(r, wait="5"):
        e = dict(os.environ)
        for k in ("WED_AGENT", "HANDOVER_CAP_BYTES", "HANDOVER_TEST_BREAK", "HANDOVER_ALLOW_XCLOCK"):
            e.pop(k, None)
        e.update({"HANDOVER_TREE": r, "HANDOVER_TEST_STAMP": STAMP, "HANDOVER_LOCK_WAIT": wait, "PYTHONDONTWRITEBYTECODE": "1"})
        return e

    def write(r, data, wait="5"):
        return run(["bash", ho, "write", "--stdin"], data, {"HANDOVER_TREE": r, "HANDOVER_TEST_STAMP": STAMP, "HANDOVER_LOCK_WAIT": wait})

    def engine(mode, t, data, wait="5", r=None):
        pr = subprocess.Popen([sys.executable, wrap, mode, core, "write", "--seat", "wednesday", "--tasks-dir", t, "--stamp", "WRAPPED", "--cap", "10000"],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=envfor(r, wait))
        pr.stdin.write(data)
        pr.stdin.close()
        return pr

    def body(t):
        return rb(os.path.join(t, "STATE-wednesday.md")).split(b"\n---\n", 1)[1]

    def arch(t):
        pth = os.path.join(t, "STATE-wednesday-archive.md")
        return rb(pth) if os.path.exists(pth) else b""

    def held(a, t):
        return body(t) == a or a in arch(t)

    S0, A, B = block("S0"), block("WRITER-A"), block("WRITER-B")

    # R01: the checker's deterministic interleave. B pauses at its first rename (every check passed, lock held);
    # A is started; before the lock, A wrote whole and B then overwrote it. Now A must WAIT.
    r, t = tree("interleave")
    write(r, S0)
    gate = os.path.join(base, "interleave", "gate")
    pb = engine("barrier:" + gate, t, B, r=r)
    t0 = time.time()
    while not os.path.exists(gate + ".waiting") and time.time() - t0 < 20:
        time.sleep(0.01)
    pa = subprocess.Popen(["bash", ho, "write", "--stdin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=envfor(r, "30"))
    pa.stdin.write(A)
    pa.stdin.close()
    time.sleep(1.0)
    waiting = pa.poll() is None and body(t) == S0
    open(gate, "w").close()
    rcb = pb.wait()
    rca = pa.wait()
    ob = pb.stdout.read().decode() + pb.stderr.read().decode()
    oa = pa.stdout.read().decode() + pa.stderr.read().decode()
    ar = arch(t)
    check("R01", "the deterministic interleave: writer A WAITS while writer B holds the lock; both are acknowledged and BOTH blocks survive",
          waiting and rcb == 0 and rca == 0 and body(t) == A and ar.count(S0) == 1 and ar.count(B) == 1
          and not os.path.exists(os.path.join(t, "STATE-wednesday.lock.d")), "A waited=%s rcA=%s rcB=%s | %s | %s" % (waiting, rca, rcb, oa, ob))

    # R02: the wait is BOUNDED and the refusal is loud; the refused writer never proceeds unlocked
    r, t = tree("bounded")
    write(r, S0)
    gate = os.path.join(base, "bounded", "gate")
    pb = engine("barrier:" + gate, t, B, r=r)
    t0 = time.time()
    while not os.path.exists(gate + ".waiting") and time.time() - t0 < 20:
        time.sleep(0.01)
    t1 = time.time()
    rca, oa, ea = write(r, A, wait="1")
    took = time.time() - t1
    before_gate = body(t)
    open(gate, "w").close()
    rcb = pb.wait()
    check("R02", "a second writer waits a bounded time (HANDOVER_LOCK_WAIT=1), then REFUSES loudly with rc 5 and the recovery line; it never writes unlocked",
          rca == 5 and "LOCK BUSY" in ea and "mv -n '" in ea and "Nothing was written" in ea and 0.8 <= took < 5 and before_gate == S0
          and rcb == 0 and body(t) == B and arch(t).count(S0) == 1 and A not in arch(t), "%s took %.1fs" % (ea, took))

    # R03: a stale lock (its holder is not running) is reported at once with the exact recovery line, never removed
    r, t = tree("stale")
    write(r, S0)
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait()
    lock = os.path.join(t, "STATE-wednesday.lock.d")
    os.mkdir(lock)
    w(os.path.join(lock, "owner"), "pid: %d\nhost: %s\nstarted: earlier\nepoch: 1\n" % (dead.pid, socket.gethostname()))
    t1 = time.time()
    rc, o, e = write(r, A, wait="30")
    took = time.time() - t1
    rec = [l.strip() for l in e.split("\n") if l.strip().startswith("mv -n '")]
    check("R03", "a STALE lock is reported at once (no 30 s wait) with the exact recovery line, and is NOT removed; nothing is written",
          rc == 5 and "STALE LOCK" in e and took < 5 and len(rec) == 1 and rec[0].startswith("mv -n '%s' '%s.stale-" % (lock, lock))
          and os.path.isdir(lock) and rb(os.path.join(lock, "owner")).startswith(b"pid: %d\n" % dead.pid) and body(t) == S0, e)
    if os.path.isdir(lock):
        shutil.move(lock, lock + ".stale-test")   # the recovery line, done by the test
    rc, o, e = write(r, A)
    check("R03b", "after the recovery line is run by a person the write succeeds (must succeed beside R03)", rc == 0 and body(t) == A and S0 in arch(t), o + e)

    # R04: a FRESH lock directory with no owner file is never assumed stale: wait, then refuse
    r, t = tree("noowner")
    write(r, S0)
    lock = os.path.join(t, "STATE-wednesday.lock.d")
    os.mkdir(lock)
    rc, o, e = write(r, A, wait="1")
    check("R04", "a FRESH lock directory with no owner file: bounded wait, then rc 5 LOCK BUSY naming 'no usable owner file'; not called stale; left alone",
          rc == 5 and "LOCK BUSY" in e and "no usable owner file" in e and "STALE LOCK" not in e and os.path.isdir(lock) and body(t) == S0, e)

    # R15: an owner-less lock OLDER THAN A MINUTE is stale (the checker's 2 of 8 kill points: killed between mkdir and the
    # owner file, or between removing the owner file and rmdir). Reported at once with the recovery line; never removed.
    ok15, notes15 = True, []
    for name, owner in (("ownerless_old", None), ("ownerempty_old", "")):
        r, t = tree(name)
        write(r, S0)
        lock = os.path.join(t, "STATE-wednesday.lock.d")
        os.mkdir(lock)
        if owner is not None:
            w(os.path.join(lock, "owner"), owner)
        old_t = time.time() - 120
        os.utime(lock, (old_t, old_t))
        t1 = time.time()
        rc, o, e = write(r, A, wait="30")
        took = time.time() - t1
        rec = [x.strip() for x in e.split("\n") if x.strip().startswith("mv -n '")]
        good_ = (rc == 5 and "STALE LOCK" in e and "no usable owner file" in e and took < 5 and len(rec) == 1
                 and rec[0].startswith("mv -n '%s' '%s.stale-" % (lock, lock)) and os.path.isdir(lock) and body(t) == S0)
        ok15 = ok15 and good_
        notes15.append("%s rc %s took %.1fs %s" % (name, rc, took, e[:200]))
    check("R15", "an owner-less lock (no owner file, or an empty one) untouched for over a minute is reported as STALE at once, with the "
                 "recovery line; nothing is removed, nothing written", ok15, notes15)

    # R16 (N4): an owner pid that is not a pid is a plain refusal, never a traceback
    ok16, notes16 = True, []
    for name, pid_text in (("pid_huge", "99999999999999999999999"), ("pid_past_int", "4294967296"), ("pid_zero", "0")):
        r, t = tree(name)
        write(r, S0)
        lock = os.path.join(t, "STATE-wednesday.lock.d")
        os.mkdir(lock)
        w(os.path.join(lock, "owner"), "pid: %s\nhost: %s\n" % (pid_text, socket.gethostname()))
        rc, o, e = write(r, A, wait="1")
        good_ = rc == 5 and "Traceback" not in e and "LOCK BUSY" in e and "mv -n '" in e and os.path.isdir(lock) and body(t) == S0
        ok16 = ok16 and good_
        notes16.append("%s rc %s %s" % (name, rc, e[-300:]))
    check("R16", "an owner file whose pid is beyond a C int, or 0, is a plain refusal (rc 5, LOCK BUSY, the recovery line), no traceback (N4)",
          ok16, notes16)

    # R03c (the checker's mutant Y02): a dead pid recorded by ANOTHER host proves nothing here
    r, t = tree("otherhost")
    write(r, S0)
    lock = os.path.join(t, "STATE-wednesday.lock.d")
    os.mkdir(lock)
    w(os.path.join(lock, "owner"), "pid: %d\nhost: some-other-mac\nstarted: earlier\nepoch: 1\n" % dead.pid)
    rc, o, e = write(r, A, wait="1")
    check("R03c", "a lock whose owner is a dead pid on ANOTHER host is not called stale (that pid cannot be judged from here): LOCK BUSY",
          rc == 5 and "LOCK BUSY" in e and "STALE LOCK" not in e and os.path.isdir(lock) and body(t) == S0, e)

    # R05: the process dies BETWEEN the archive rename and the state rename (the checker's crash; its mutant Q01)
    r, t = tree("crash")
    S1, S2, S3 = block("S1"), block("S2"), block("S3")
    write(r, S0)
    write(r, S1)
    pc = engine("crash-before-2nd", t, S2, r=r)
    rcc = pc.wait()
    check("R05", "a death between the two renames leaves the old block in BOTH files (archive first, state second): nothing is lost",
          rcc == 137 and body(t) == S1 and arch(t).count(S1) == 1 and arch(t).count(S0) == 1 and S2 not in arch(t), "rc %s" % rcc)
    rc, o, e = write(r, S3)
    lock = os.path.join(t, "STATE-wednesday.lock.d")
    check("R05b", "the dead writer's lock is then reported as STALE with the recovery line (not removed, not waited on)",
          rc == 5 and "STALE LOCK" in e and os.path.isdir(lock) and body(t) == S1, e)
    if os.path.isdir(lock):
        shutil.move(lock, lock + ".stale-test")
    rc, o, e = write(r, S3)
    check("R05c", "after recovery the next write succeeds; the archive holds a duplicate of the old block, never a gap",
          rc == 0 and body(t) == S3 and arch(t).count(S1) == 2 and arch(t).count(S0) == 1, o + e)

    # R06: a hand edit lands on the state file while the write is being prepared (the checker's mutant Q02)
    r, t = tree("edited")
    write(r, S0)
    write(r, S1)
    a_before = arch(t)
    sp = os.path.join(t, "STATE-wednesday.md")
    pe = engine("edit-state-at-fsync2:" + sp, t, S2, r=r)
    rce = pe.wait()
    ee = pe.stderr.read().decode()
    check("R06", "an edit made outside the tool during the write is seen: rc 4, the edited file is left as it is, nothing renamed",
          rce == 4 and "changed on disk" in ee and rb(sp).endswith(b"\nHAND-EDIT-DURING-THE-WRITE\n") and arch(t) == a_before
          and not os.path.exists(os.path.join(t, "STATE-wednesday.lock.d")), ee)

    # R07: a temp file that does not read back as written (the checker's mutant Q03)
    r, t = tree("tmpbad")
    write(r, S0)
    write(r, S1)
    s_before, a_before = rb(os.path.join(t, "STATE-wednesday.md")), arch(t)
    pt = engine("truncate-tmp-at-fsync1", t, S2, r=r)
    rct = pt.wait()
    et = pt.stderr.read().decode()
    check("R07", "a temp file that does not read back as written stops the write: rc 4, state and archive unchanged, the temp file named",
          rct == 4 and "does not read back as written" in et and rb(os.path.join(t, "STATE-wednesday.md")) == s_before and arch(t) == a_before
          and "left for inspection" in et, et)

    def waitfor(path, secs=20):
        t0_ = time.time()
        while not os.path.exists(path) and time.time() - t0_ < secs:
            time.sleep(0.005)
        return os.path.exists(path)

    C, D, E = block("WRITER-C"), block("WRITER-D"), block("WRITER-E")

    # R09: the second checker's false_stale.py, lifted. Holder A finishes NORMALLY while waiter B sits between "read the
    # owner file" and "is that pid alive"; a third writer C then holds a live lock at the same path. Round 3 told B
    # "STALE LOCK, pid A is no longer running" and printed a recovery line that named C's live lock.
    r, t = tree("falsestale")
    write(r, S0)
    gA, gB, gC = (os.path.join(base, "falsestale", x) for x in ("gateA", "gateB", "gateC"))
    pa = engine("barrier:" + gA, t, A, r=r)
    okA = waitfor(gA + ".waiting")
    pb = engine("pause-at-kill:" + gB, t, B, wait="30", r=r)
    okB = waitfor(gB + ".atkill")
    open(gA, "w").close()
    rca = pa.wait()
    pc = engine("barrier:" + gC, t, C, r=r)
    okC = waitfor(gC + ".waiting")
    open(gB, "w").close()
    time.sleep(1.5)
    b_waits = pb.poll() is None
    open(gC, "w").close()
    rcc = pc.wait()
    rcb = pb.wait()
    eb = pb.stderr.read().decode()
    ar = arch(t)
    check("R09", "false STALE (the checker's reproduction): a holder that finished normally is NOT reported dead; the waiter looks twice, "
                 "keeps waiting for the live writer, and all three acknowledged blocks are on disk",
          okA and okB and okC and rca == 0 and b_waits and "STALE" not in eb and rcc == 0 and rcb == 0 and body(t) == B
          and ar.count(S0) == 1 and ar.count(A) == 1 and ar.count(C) == 1 and not os.path.exists(os.path.join(t, "STATE-wednesday.lock.d")),
          "paused A/B/C %s %s %s; rcA %s rcC %s rcB %s; B still waiting %s; B stderr: %s" % (okA, okB, okC, rca, rcc, rcb, b_waits, eb[:300]))

    # R10: the PRINTED recovery line is run while a writer is ALIVE (the LOCK BUSY message prints it too). The live writer C
    # is paused INSIDE its first rename, after every check it makes in Python. Two more writers then complete. C must not
    # rename anything: its temp files sat in the lock directory that was moved away.
    r, t = tree("recoveryalive")
    write(r, S0)
    g = os.path.join(base, "recoveryalive", "gate")
    pc = engine("barrier:" + g, t, C, r=r)
    okC = waitfor(g + ".waiting")
    WAITER = block("WAITER")
    rcw, ow, ew = write(r, WAITER, wait="1")
    rec = [x.strip() for x in ew.split("\n") if x.strip().startswith("mv -n '")]
    ran = -1
    if len(rec) == 1 and rec[0].count(base) == 2:     # the line names scratch paths only
        ran = subprocess.run(["/bin/sh", "-c", rec[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode
    rcd, od, ed = write(r, D)
    rce, oe, ee = write(r, E)
    open(g, "w").close()
    rcc = pc.wait()
    oc, ec = pc.stdout.read().decode(), pc.stderr.read().decode()
    ar = arch(t)
    check("R10", "the printed recovery line run while a writer is ALIVE, then two more writes: the displaced writer renames NOTHING "
                 "(rc 5, LOCK LOST, no 'written'), and no acknowledged block is lost",
          okC and rcw == 5 and "LOCK BUSY" in ew and ran == 0 and rcd == 0 and rce == 0 and rcc == 5 and "LOCK LOST" in ec
          and "NOTHING was renamed" in ec and "handover: written" not in oc and body(t) == E and ar.count(D) == 1 and ar.count(S0) == 1
          and C not in ar and WAITER not in ar,
          "waiter rc %s; recovery ran %s; D %s E %s; C rc %s: %s | archive D x%d S0 x%d" % (rcw, ran, rcd, rce, rcc, ec[:300], ar.count(D), ar.count(S0)))

    # R11: the lock directory is moved away in the instant before a rename (after the owner check). The rename itself must fail.
    r, t = tree("steal1")
    write(r, S0)
    write(r, S1)
    s_before, a_before = rb(os.path.join(t, "STATE-wednesday.md")), arch(t)
    lock = os.path.join(t, "STATE-wednesday.lock.d")
    px = engine("steal-lock-at:1:" + lock, t, S2, r=r)
    rcx = px.wait()
    ox, ex = px.stdout.read().decode(), px.stderr.read().decode()
    check("R11", "the lock moved away in the instant before the FIRST rename: rc 5, nothing renamed, state and archive byte-identical, no 'written'",
          rcx == 5 and "LOCK LOST" in ex and "NOTHING was renamed" in ex and "handover: written" not in ox
          and rb(os.path.join(t, "STATE-wednesday.md")) == s_before and arch(t) == a_before, "rc %s %s" % (rcx, ex[:300]))
    r, t = tree("steal2")
    write(r, S0)
    write(r, S1)
    lock = os.path.join(t, "STATE-wednesday.lock.d")
    px = engine("steal-lock-at:2:" + lock, t, S2, r=r)
    rcx = px.wait()
    ox, ex = px.stdout.read().decode(), px.stderr.read().decode()
    mid_ok = (rcx == 5 and "ARCHIVE had already been replaced" in ex and "STATE file was NOT replaced" in ex and "handover: written" not in ox
              and body(t) == S1 and arch(t).count(S1) == 1 and arch(t).count(S0) == 1 and S2 not in arch(t))
    rc, o, e = write(r, S3)
    check("R11b", "the lock moved away between the two renames: rc 5 saying exactly what was renamed; the old block is in BOTH files; "
                  "the next write succeeds with one duplicate archive entry, never a gap",
          mid_ok and rc == 0 and body(t) == S3 and arch(t).count(S1) == 2 and arch(t).count(S0) == 1, "rc %s %s | next rc %s %s" % (rcx, ex[:300], rc, e[:200]))

    # R12: the lock directory stays but its owner file becomes ANOTHER writer's during the write: the owner re-read stops it
    r, t = tree("foreignowner")
    write(r, S0)
    write(r, S1)
    s_before, a_before = rb(os.path.join(t, "STATE-wednesday.md")), arch(t)
    lock = os.path.join(t, "STATE-wednesday.lock.d")
    px = engine("foreign-owner-at-fsync2:" + lock, t, S2, r=r)
    rcx = px.wait()
    ox, ex = px.stdout.read().decode(), px.stderr.read().decode()
    own12 = rb(os.path.join(lock, "owner")) if os.path.isfile(os.path.join(lock, "owner")) else b"(the owner file is gone)"
    in12 = sorted(os.listdir(lock)) if os.path.isdir(lock) else ["(the lock directory is gone)"]
    aside12 = sorted(f for f in os.listdir(t) if ".md.tmp." in f)
    check("R12", "the owner file is re-read before each rename: when it is another writer's, rc 5 and nothing is renamed; the other "
                 "writer's lock is left with its owner file and with NOTHING of this writer's inside it (its temp files are moved out)",
          rcx == 5 and "before the archive rename the lock was no longer this process's" in ex and "NOTHING was renamed" in ex
          and rb(os.path.join(t, "STATE-wednesday.md")) == s_before and arch(t) == a_before
          and b"FOREIGN-TOKEN" in own12 and in12 == ["owner"] and len(aside12) == 2 and "moved out of the lock directory" in ex,
          "rc %s; in the lock: %s; set aside: %s; owner: %r; %s" % (rcx, in12, aside12, own12[:60], ex[:300]))

    # R13: the lock is gone at RELEASE (moved away after the second rename): the writer must not say 'written' and must exit non-zero
    r, t = tree("gone_at_release")
    write(r, S0)
    write(r, S1)
    lock = os.path.join(t, "STATE-wednesday.lock.d")
    px = engine("steal-lock-after:2:" + lock, t, S2, r=r)
    rcx = px.wait()
    ox, ex = px.stdout.read().decode(), px.stderr.read().decode()
    check("R13", "a writer that finds its lock gone at release exits NON-ZERO (rc 6), says NOT ACKNOWLEDGED, and never prints 'written'",
          rcx == 6 and "NOT ACKNOWLEDGED" in ex and "handover: written" not in ox and ox.strip() == "" and body(t) == S2, "rc %s out %r err %s" % (rcx, ox[:80], ex[:300]))

    # R14 (the checker's mutant Y01): release removes ONLY its own lock. Another owner's lock stands at the path at release.
    r, t = tree("foreign_at_release")
    write(r, S0)
    write(r, S1)
    lock = os.path.join(t, "STATE-wednesday.lock.d")
    px = engine("swap-lock-after:2:" + lock, t, S2, r=r)
    rcx = px.wait()
    ox, ex = px.stdout.read().decode(), px.stderr.read().decode()
    check("R14", "release removes ONLY its own lock: another owner's lock standing at the path is left with its owner file, and the "
                 "writer exits non-zero (Y01)",
          rcx == 6 and os.path.isdir(lock) and os.path.isfile(os.path.join(lock, "owner")) and b"FOREIGN-TOKEN" in rb(os.path.join(lock, "owner"))
          and "not this process's any more" in ex and "handover: written" not in ox, "rc %s %s" % (rcx, ex[:300]))


    # R08: N trials of two handover.sh writes started together (the checker's natural race: 23 of 150 lost before the lock)
    n = int(os.environ.get("WAKE_RACE_TRIALS", "200"))
    lost = both = refused = dup = 0
    pad = "- " + "p" * 8800 + "\n"
    for i in range(n):
        r, t = tree("race/%03d" % i)
        base_block = block("BASE%d" % i, pad)
        write(r, base_block)
        blocks = [block("RACE-A%d" % i, pad), block("RACE-B%d" % i, pad)]
        ps = [subprocess.Popen(["bash", ho, "write", "--stdin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=envfor(r, "30"))
              for _ in (0, 1)]
        for pr, d in zip(ps, blocks):
            pr.stdin.write(d)
            pr.stdin.close()
        rcs = [pr.wait() for pr in ps]
        for pr in ps:
            pr.stdout.close()
            pr.stderr.close()
        acked = [d for d, rc_ in zip(blocks, rcs) if rc_ == 0]
        both += len(acked) == 2
        refused += any(rc_ != 0 for rc_ in rcs)
        lost += sum(1 for d in acked if not held(d, t))
        dup += arch(t).count(base_block) != 1
    check("R08", "%d trials of two simultaneous writes: every acknowledged block is in the state file or the archive" % n,
          n >= 200 and lost == 0 and dup == 0 and both == n and refused == 0,
          "lost %d; both acknowledged %d of %d; refused %d; base block not exactly once in the archive %d" % (lost, both, n, refused, dup))
    print("     R08 counts: trials %d, both acknowledged %d, one refused %d, acknowledged block LOST %d, base block not once in archive %d"
          % (n, both, refused, lost, dup))


GROUPS = {"H": group_h, "W": group_w, "C": group_c, "P": group_p, "D": group_d, "S": group_s, "R": group_r}

# ── mutants: break the thing, see red ──────────────────────────────────────────────────────────
# The list lives in tests/mutants.py: (name, [(file relative to the lane, needle, replacement)], group, [check ids]).
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
from mutants import M as MUTANTS  # noqa: E402


def run_mutants(scratch):
    caught = 0
    # WAKE_MUTANT_RANGE=<first>-<last> runs only those mutants (1-based, inclusive), so a long run can be done in parts.
    lo, hi = 1, len(MUTANTS)
    if os.environ.get("WAKE_MUTANT_RANGE"):
        lo, hi = (int(x) for x in os.environ["WAKE_MUTANT_RANGE"].split("-"))
    ran = 0
    for n, (name, edits, group, must) in enumerate(MUTANTS, 1):
        if not lo <= n <= hi:
            continue
        ran += 1
        mroot = os.path.join(scratch, "mut", "m%02d" % n, "2_Project_Files")
        mlane = os.path.join(mroot, "wake")
        os.makedirs(mlane)
        shutil.copytree(os.path.join(LANE, "proposed"), os.path.join(mlane, "proposed"))
        for f in ("handover.sh", "handover_core.py", "wake_pack.py", "wake_census.sh"):
            shutil.copy(os.path.join(LANE, f), os.path.join(mlane, f))
        for rel in ("tools/seat_note.sh", "fleet/cockpit/seat_resolve.sh"):
            os.makedirs(os.path.dirname(os.path.join(mroot, rel)), exist_ok=True)
            shutil.copy(os.path.join(REAL_ROOT, "2_Project_Files", rel), os.path.join(mroot, rel))
        applied = True
        for rel, needle, repl in edits:
            p = os.path.join(mlane, rel)
            s = open(p, encoding="utf-8").read()
            if s.count(needle) != 1:
                applied = False
                print("MUTANT-ERROR m%02d %s :: needle found %d times in %s" % (n, name, s.count(needle), rel))
                break
            w(p, s.replace(needle, repl))
        if not applied:
            continue
        ms = os.path.join(scratch, "mut", "m%02d_scratch" % n)
        os.makedirs(ms)
        e = dict(os.environ)
        only = os.environ.get("WAKE_MUTANT_GROUPS", "")
        if only and group not in only:
            continue
        e.update({"WAKE_UNDER_TEST": mlane, "WAKE_TEST_SCRATCH": ms, "PYTHONDONTWRITEBYTECODE": "1",
                  "WAKE_RACE_TRIALS": os.environ.get("WAKE_MUTANT_RACE_TRIALS", "200")})
        if any(rel.startswith("proposed/launcher_hunk") for rel, _, _ in edits):   # the stored diff must follow its hunks
            subprocess.run([sys.executable, os.path.join(mlane, "proposed", "build_launcher_diff.py"), "--launcher", LAUNCHER, "--write"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e)
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--groups", group], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e)
        out = r.stdout.decode("utf-8", "replace")
        red = [l.split()[1] for l in out.split("\n") if l.startswith("FAIL ")]
        if all(m in red for m in must):
            caught += 1
            print("RED-AS-EXPECTED m%02d %s :: went red: %s" % (n, name, " ".join(red)))
        else:
            print("NOT-CAUGHT m%02d %s :: expected red %s, got red %s" % (n, name, must, red))
        sys.stdout.flush()
    print("mutants: %d of %d caught (each tool broken in a scratch copy; the lane's files are untouched)%s"
          % (caught, ran, "" if ran == len(MUTANTS) else "; this run covered mutants %d to %d of %d" % (lo, hi, len(MUTANTS))))
    sys.stdout.flush()
    return 0 if caught == ran and ran else 1


def main():
    args = sys.argv[1:]
    scratch = os.environ.get("WAKE_TEST_SCRATCH") or tempfile.mkdtemp(prefix="wake_tests.")
    os.makedirs(scratch, exist_ok=True)
    if os.listdir(scratch):
        scratch = tempfile.mkdtemp(prefix="run.", dir=scratch)
    real = os.path.realpath(scratch)
    if not any(real.startswith(os.path.realpath(r) + "/") for r in ("/tmp", "/private/tmp", "/var/folders", "/private/var/folders")):
        print("run_tests: the scratch directory %s is not under a system temp directory; handover.sh honours its test seams "
              "only there (round 3, m4). Set WAKE_TEST_SCRATCH to a directory under /tmp or leave it unset." % scratch)
        return 2
    if "--mutants" in args:
        return run_mutants(scratch)
    groups = "HWCPDSR"
    if "--groups" in args:
        groups = args[args.index("--groups") + 1].replace(",", "")
    print("tools under test: %s" % TOOLS)
    print("scratch: %s" % scratch)
    for g in groups:
        try:
            GROUPS[g](scratch)
        except Exception as ex:  # a crash in a group is a failure, never a silent skip
            check(g + "-CRASH", "group %s ran to the end" % g, False, repr(ex))
    passed = sum(1 for _, ok in RESULTS if ok)
    failed = len(RESULTS) - passed
    print("checks: %d passed, %d failed, %d total (groups %s)" % (passed, failed, len(RESULTS), groups))
    return 0 if failed == 0 and RESULTS else 1


if __name__ == "__main__":
    sys.exit(main())
