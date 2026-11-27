#!/usr/bin/env python3
"""wake_pack.py — build (or check) ONE fixed-budget wake pack for a coordinator seat (WED-170 step 1).

WHY: the boot prompt mandated ~917 KB of whole-file reads for the Wednesday seat (census 2026-11-27).
Most of it was handover history and dead grant rows. The pack is one generated file with a hard
token budget; over budget it writes nothing and says which part grew.

Usage:
  wake_pack.py --seat <wednesday|tuesday|friday> [--budget-tokens 60000] [--out <path>]
      write the pack (default <root>/0_Brain/wake/WAKE-<seat>.md), print one summary line
  wake_pack.py --seat <seat> --check [--out <path>]
      exit 1 with one line per fault when the pack is missing, older than a source, built on an
      earlier date, or different from what would be built now; 0 with an OK line
  --trust-expired-heading   also drop grant rows that sit under the grants file's '## Expired' heading
  --root <dir>              tree root (default: derived from this file's location)   [tests]
  --today YYYY-MM-DD        the date the grant filter compares against (default: today)   [tests]

Parts, in order (each section has a row in the manifest table at the top of the pack):
  a. identity   persona, voice protocol, Kam: verbatim
  b. rules      the rules card's "Most reinforced" section verbatim, then family headings with counts
  c. state      the seat's STATE block (handover.sh); if none yet, the legacy pickup's first block
  d. grants     rows of EXPIRING-GRANTS.md that are not PROVABLY dead or another seat's
  e. ledger     each row of the seat's own ledger as date, headline, Rule sentence
  f. pointers   paths only

The grant filter fails toward inclusion (rules tightened in round 3 after the checker's 15 hostile rows).
A row is dropped only when ONE of these is proven from its own text; everything else is kept:
  1. DEAD MARKER  the first cell, after emphasis marks, starts with DEAD, EXPIRED, ENDED, LAPSED, CLOSED,
     RETIRED or END EVENT REACHED, the marker is followed by a DATE (optionally "since", "end of", a
     weekday), it is not struck through, and the cell carries no REOPENED / REVIVED / RENEWED /
     RE-AFFIRMED / REINSTATED / RESTORED / EXTENDED / RESUMED. A marker word used as the row's subject
     ("CLOSED PRs may be reopened") has no date after it and is kept.
  2. OTHER SEAT   the first cell leads with one or more OTHER seats' names and a separator, this seat is not
     among them, and NO cell of the row names this seat, all seats / every seat / both seats / the fleet,
     or this seat's client. A seat that serves every client (friday) never drops a row by this class.
     The seat's short name in capitals (WED) counts as naming it, except as a ticket id (WED-170).
     Two idioms are not "naming the seat" because they are a weekday by construction: the name directly
     followed by a date, and the register's clock stamp (`date`: Wednesday).
  3. PAST END     the row has exactly four cells; the EXPIRES cell STARTS with an explicit end form (END OF,
     until / through / ends / expires, or a weekday with the date), holds exactly one date, that date is
     before today, and the row carries none of: EVENT, until further notice, extended, renewed, no end
     stated, later, continued, kept alive, moved, stands, onwards, at first, whichever. A bare date at
     the start of the cell is a given or start date, not an end.
A kept row that leads with this seat's name is "this seat's"; any other kept row is "unclassified".
Every dropped row is listed in a sidecar beside the pack, <pack name>.dropped.txt: one line with its
class, its line in the grants file, the proof, and the first 80 characters of its first cell. The
sidecar is not part of the pack and is not counted in the budget; the pack names it.

A PART NEVER SHRINKS TO A PLACEHOLDER (round 3, M2): a missing, empty or unreadable source, a rules card
without its "Most reinforced" section, a grants file or ledger whose table header is not found, or a
state source with no block, is a FAILED BUILD: exit 2, nothing written, the part named, and a last
line that starts "wake_pack: FAILED" for the launcher to show the seat.

Exit codes: 0 ok; 1 --check found a fault; 2 usage or a failed build (a source missing, empty, unreadable
or without its expected structure); 3 over budget.
Standard library only. Globs skip '(conflict_on_' and '.pre-' names. Never discards stderr.
"""
import argparse
import datetime
import glob
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SELF_REL = "2_Project_Files/wake/wake_pack.py"

SEATS = ["wednesday", "tuesday", "friday"]
# The same seat -> file mapping the launcher holds (Launch_Wednesday.command, PICKUP_FILE / SEAT_LEDGER).
SEAT_FILES = {
    "wednesday": {"ledger": "_ledger.md", "pickup": "NEXT-PICKUP.md"},
    "tuesday": {"ledger": "_ledger_laptop_datasec.md", "pickup": "NEXT-PICKUP-TUESDAY.md"},
    "friday": {"ledger": "_ledger_friday.md", "pickup": "NEXT-PICKUP-FRIDAY.md"},
}
IDENTITY = ["0_Brain/identity/persona.md", "0_Brain/identity/voice-protocol.md", "0_Brain/people/kam.md"]
SKIP = ("(conflict_on_", ".pre-")

# Leading words of a row's FIRST cell that mark the grant dead, when followed by a date (see DEAD_FORM).
# PREMISE ENDED was removed in round 3 (Wednesday's ANSWER-3): a premise ending is not the row ending.
DEAD_WORDS = ("DEAD", "EXPIRED", "ENDED", "LAPSED", "CLOSED", "RETIRED", "END EVENT REACHED")
DROP_CLASS = {"dead": "dead marker", "other": "other seat", "past": "past date", "expired_heading": "expired heading"}
EMPH = " \t*_`\u26a0\u2705\U0001F534\U0001F7E1\U0001F7E2\ufe0f"      # emphasis and signs; NOT the strike-through
MARKUP = EMPH + "~"
ISO = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
WEEKDAY = r"(?:mon|tues?|wed(?:nes)?|thu(?:rs)?|fri|sat(?:ur)?|sun)(?:day)?"
DEAD_FORM = re.compile(
    r"(%s)(?i:\s+(?:since\s+)?(?:(?:the\s+)?end\s+of\s+)?(?:%s,?\s+)?)(\d{4}-\d{2}-\d{2})\b"
    % ("|".join(re.escape(w) for w in sorted(DEAD_WORDS, key=len, reverse=True)), WEEKDAY))
REVIVED = re.compile(r"\b(?:REOPENED|RE-OPENED|REVIVED|RENEWED|RE-AFFIRMED|REAFFIRMED|REINSTATED|RESTORED|EXTENDED|RESUMED|"
                     r"REACTIVATED|RE-GRANTED|REGRANTED|REISSUED|RE-ISSUED|CONTINUED|STILL LIVE|LIVE AGAIN|NOT DEAD|BACK ON)\b")
SEAT_ALT = "|".join(x.upper() for x in ("wednesday", "tuesday", "friday"))
OWNERS = re.compile(r"((?:%s)(?:\s*(?:,|\+|/|&|(?i:and))\s*(?:%s))*)\b\s*(?::|\(|\u2014|\u2013|-(?![\w])|,)" % (SEAT_ALT, SEAT_ALT))
# Words that make another seat's row bind this seat too.
ALL_SEATS = re.compile(r"\b(?:all|every|each|both|any|other|the\s+other|sister)\s+(?:the\s+|three\s+|two\s+)?(?:seats?|coordinators?|agents?)\b|"
                       r"\bfleet\b|\ball\s+three\b|\beveryone\b|\beverybody\b", re.I)
# A seat's short name in capitals (TUESDAY + WED), but not a ticket id (WED-170) and not a day (WED 2026-11-25).
SEAT_SHORT = {"wednesday": "WED", "tuesday": "TUES?", "friday": "FRI"}
# A seat's client(s): another seat's row that names it is kept. None = the seat serves every client, so the
# other-seat class never drops a row for it (friday; the checker's N3, the register's line 26).
SEAT_CLIENTS = {"wednesday": ("secuura",), "tuesday": ("datasec",), "friday": None}
END_FORM = re.compile(
    r"(?:(until|through|thru|ends?(?:\s+(?:on|at))?|expires?(?:\s+on)?)\s+)?(?:the\s+)?(?:(end\s+of)\s+)?(?:(%s),?\s+)?(\d{4}-\d{2}-\d{2})\b" % WEEKDAY, re.I)
WORD_DATE = re.compile(r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b|"
                       r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2}\b|\bthe\s+\d{1,2}(?:st|nd|rd|th)\b", re.I)
NEGATED = re.compile(r"\b(?:not|never|nor)\s+(?:renewed|extended)\b|\bnot\s+renewed\s+and\s+not\s+extended\b", re.I)
ROW_KEEPS = re.compile(r"until\s+further\s+notice|extend|renew|no\s+end\b|no\s+expiry|no\s+date|open-ended|\blater\b|continu|"
                       r"kept\s+alive|\bmoved\b|\bstands\b|onwards?\b|\bat\s+first\b|whichever|re-?affirm|re-?read|\bchang|"
                       r"reopen|re-open|reviv|reinstat|restor|resum|\bunless\b|\bat\s+least\b|\bat\s+the\s+earliest\b|provisional|"
                       r"\bpending\b|\bongoing\b|indefinite|permanent|\brolling\b|\bor\s+until\b|\bor\s+when\b|\btbc\b|"
                       r"to\s+be\s+confirmed|still\s+(?:live|in\s+force)", re.I)
EVENT = re.compile(r"\bEVENT\b")
GRANTS_HEADER = re.compile(r"^\|\s*grant\s*\|\s*given\s*\|\s*EXPIRES\s*\|", re.I)
LEDGER_HEADER = re.compile(r"^\|\s*Date\s*\|\s*What happened", re.I)
LEDGER_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)$")
BOLD = re.compile(r"\*\*(.+?)\*\*")
RULE = re.compile(r"\b(Rule|RULE)(\s*\([^)|]{1,60}\))?:\s*")
SENT_END = re.compile(r"[.!?](?=\s+[A-Z\[(*\U0001F511]|\s*$)")
RULE_MAX = 700


def eprint(*a):
    print(*a, file=sys.stderr)


def tok(n):
    return (n + 3) // 4


def safe_glob(pattern):
    """Sorted glob that never returns a sync-conflict copy or a .pre- backup."""
    return [p for p in sorted(glob.glob(pattern)) if not any(s in os.path.basename(p) for s in SKIP)]


class BuildFail(Exception):
    """A part cannot be built from its source. The build fails whole; a part never shrinks to a placeholder."""
    def __init__(self, part, reason):
        Exception.__init__(self, "part %s: %s" % (part, reason))
        self.part, self.reason = part, reason


class Build:
    def __init__(self, root, seat, today, trust_expired):
        self.root, self.seat, self.today, self.trust_expired = root, seat, today, trust_expired
        self.sources = []  # absolute paths actually read
        self.parts = []    # (title, [section dict])
        self.stats = {}
        self.dropped = []  # (class key, grants-file line number, proof, first 80 chars of the first cell)

    def p(self, rel):
        return os.path.join(self.root, rel)

    def read(self, rel, part, must_exist=True, allow_empty=False):
        """-> text. A missing, unreadable or (unless allowed) empty file is a BuildFail naming the part and path.
        must_exist=False returns None for an absent file (used where the caller chooses between two sources)."""
        path = self.p(rel)
        if any(s in os.path.basename(path) for s in SKIP):
            raise BuildFail(part, "refusing to read a conflict copy or backup: " + rel)
        if not os.path.lexists(path):
            if must_exist:
                raise BuildFail(part, "source missing: %s" % rel)
            return None
        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError as e:
            raise BuildFail(part, "source unreadable: %s (%s)" % (rel, e.strerror or e))
        if not data.strip() and not allow_empty:
            raise BuildFail(part, "source is empty: %s" % rel)
        if path not in self.sources:
            self.sources.append(path)
        return data.decode("utf-8", "replace")

    def size(self, rel):
        path = self.p(rel)
        return os.path.getsize(path) if os.path.isfile(path) else None

    def add(self, title, sections):
        self.parts.append((title, sections))


def sec(source, src_bytes, text, label=None):
    if not text.endswith("\n"):
        text += "\n"
    return {"source": source, "src_bytes": src_bytes, "text": text, "label": label or source}


# ── a. identity ────────────────────────────────────────────────────────────────────────────────
def part_identity(b):
    out = []
    for rel in IDENTITY:
        text = b.read(rel, "a (identity)")
        out.append(sec(rel, b.size(rel), "### %s (verbatim)\n\n%s" % (rel, text)))
    b.add("a. Identity (verbatim)", out)


# ── b. rules ───────────────────────────────────────────────────────────────────────────────────
def part_rules(b):
    part = "b (rules)"
    rel = "0_Brain/learnings/_rules_card_%s.md" % b.seat
    tool_rel = "2_Project_Files/tools/rules_card.py"
    card = b.read(rel, part)
    tool = b.read(tool_rel, part)
    if '"--at"' not in tool:
        raise BuildFail(part, "%s has no --at flag: the pack's fetch line would name a command that does not exist" % tool_rel)
    vocab = ""
    m = re.search(r"VOCAB\s*=\s*\[(.*?)\]", tool, re.S)
    if m:
        vocab = " ".join(re.findall(r'"([^"]+)"', m.group(1)))
    fam_dir = "0_Brain/learnings/families"
    fam_files = dict((os.path.basename(p)[:-3], p) for p in safe_glob(os.path.join(b.p(fam_dir), "*.md")))
    b.stats["family_files"] = len(fam_files)
    lines = card.split("\n")
    heads = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
    top_text, fams, others = None, [], []
    for n, (i, name) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        body = lines[i:end]
        count = sum(1 for l in body[1:] if l.startswith("- "))
        if top_text is None and name.lower().startswith("most reinforced"):
            if count == 0:
                raise BuildFail(part, "the 'Most reinforced' section of %s holds no rule line" % rel)
            top_text = "\n".join(body).rstrip("\n") + "\n"
        elif name.lower().startswith(("enforced by a tool", "not on this card")):
            others.append((name, count))
        else:
            fams.append((name, count))
    if top_text is None:
        raise BuildFail(part, "%s has no '## Most reinforced' section (regenerate it: python3 %s --seat %s)" % (rel, tool_rel, b.seat))
    out = [sec(rel, b.size(rel), "From `%s` (verbatim section; the rest of the card is NOT in this pack):\n\n%s" % (rel, top_text),
               label=rel + " (Most reinforced)")]
    fl = ["### Rule families on the card (headings and line counts only)", ""]
    for name, count in fams:
        ff = fam_files.get(name)
        where = "`%s/%s.md`" % (fam_dir, name) if ff else "the card's `## %s` section" % name
        fl.append("- %s: %d lines. Cases: %s" % (name, count, where))
    for name, count in others:
        fl.append("- (%s: %d lines, on the card)" % (name, count))
    fl.append("")
    fl.append("Family files in `%s/`: %d." % (fam_dir, len(fam_files)))
    fl.append("")
    fl.append("### Fetch at the moment of action")
    fl.append("")
    fl.append("- The rules for a moment: `python3 %s --at <trigger> --seat %s` (add `--top 8` for the heaviest). It prints, writes nothing."
              % (tool_rel, b.seat))
    if vocab:
        fl.append("- Triggers: %s" % vocab)
    fl.append("- A whole family: its file above, or its `## <family>` section in `%s`." % rel)
    fl.append("- A rule's cases: the lesson file named at the end of its line, in `0_Brain/learnings/`.")
    out.append(sec("-", None, "\n".join(fl) + "\n", label="family headings + fetch lines (generated)"))
    b.add("b. Rules (most reinforced verbatim; families by heading)", out)


# ── c. state ───────────────────────────────────────────────────────────────────────────────────
def part_state(b):
    part = "c (state)"
    rel = "0_Brain/tasks/STATE-%s.md" % b.seat
    state = b.read(rel, part, must_exist=False)
    if state is not None:
        if not re.search(r"^## FLOOR\s*$", state, re.M):
            raise BuildFail(part, "%s holds no '## FLOOR' part: it is not a block written by handover.sh" % rel)
        b.stats["state"] = "STATE file"
        b.add("c. State (the one-block handover)",
              [sec(rel, b.size(rel),
                   "From `%s`, whole. FIRST WORK and OWED are the first work of this session. "
                   "Written only through `2_Project_Files/wake/handover.sh write --stdin`; earlier blocks: `0_Brain/tasks/STATE-%s-archive.md`.\n\n%s"
                   % (rel, b.seat, state))])
        return
    prel = "0_Brain/tasks/" + SEAT_FILES[b.seat]["pickup"]
    pick = b.read(prel, part, must_exist=False)
    if pick is None:
        raise BuildFail(part, "no state file at %s and no legacy pickup at %s: the seat has no handover to boot on" % (rel, prel))
    head = ("NO STATE FILE YET at `%s`: the one-block handover has not been cut over for this seat. "
            "Write one with `2_Project_Files/wake/handover.sh write --stdin`.\n\n" % rel)
    lines = pick.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("## ")]
    if not idx:
        raise BuildFail(part, "the legacy pickup %s holds no '## ' block" % prel)
    end = idx[1] if len(idx) > 1 else len(lines)
    block = "\n".join(lines[idx[0]:end]).rstrip("\n") + "\n"
    span, more = "lines %d to %d of %d" % (idx[0] + 1, end, len(lines)), len(idx) - 1
    b.stats["state"] = "legacy pickup, first block only"
    text = (head + "Until then the handover is the legacy pickup `%s` (%d bytes). ONLY ITS FIRST BLOCK follows (%s). "
            "%d further '## ' blocks, including any STANDING and OWED sections, are NOT in this pack: read them in the file.\n\n%s"
            % (prel, b.size(prel), span, more, block))
    b.add("c. State (legacy pickup, first block only)", [sec(prel, b.size(prel), text, label=prel + " (first block)")])


# ── d. grants ──────────────────────────────────────────────────────────────────────────────────
def lead(cell):
    return cell.strip().lstrip(MARKUP)


WEEKDAY_IDIOM = r"(?:`date[^`]*`:\s*(?:%s)\b)|(?:\b(?:%s)\b,?\s+\d{4}-\d{2}-\d{2})"


def names_seat(row, seat):
    """Does the row name this seat as a seat? The seats are named after weekdays, so two forms that are a weekday
    by construction are removed first: the register's clock stamp (`date -j`: Wednesday) and the name directly
    followed by a date. Any other occurrence, in any case, counts: fail toward inclusion."""
    text = re.sub(WEEKDAY_IDIOM % (seat, seat), " ", row, flags=re.I)
    if re.search(r"\b%s\b" % re.escape(seat), text, re.I):
        return True
    short = SEAT_SHORT.get(seat)
    return bool(short) and re.search(r"\b(?:%s)\b(?!-\d)(?!,?\s+\d)" % short, text) is not None


def classify_grant(line, seat, today):
    """-> (verdict, why). verdict: 'mine' | 'unclassified' | 'dead' | 'other' | 'past'. Drops need proof."""
    cells = line.split("|")[1:-1]
    first = cells[0] if cells else ""
    # 1. dead marker: the row's status, followed by a date, not struck through, not revived
    struck = first.strip().lstrip(EMPH).startswith("~~")
    dm = DEAD_FORM.match(lead(first))
    if dm and not struck and not REVIVED.search(first):
        return "dead", "first cell starts with %s %s" % (dm.group(1), dm.group(2))
    # 2. another seat's: leading owner list without this seat, and no cell that binds this seat
    om = OWNERS.match(lead(first))
    owners = [o.lower() for o in re.findall(SEAT_ALT, om.group(1))] if om else []
    if owners and seat not in owners:
        clients = SEAT_CLIENTS.get(seat)
        if (clients is not None and not names_seat(line, seat) and not ALL_SEATS.search(line)
                and not any(re.search(r"\b%s\b" % re.escape(c), line, re.I) for c in clients)):
            return "other", "first cell starts with " + " + ".join(o.upper() for o in owners)
    # 3. past end date: an explicit end form, exactly one date, nothing in the row that keeps it alive
    if len(cells) == 4:
        exp = cells[2]
        em = END_FORM.match(lead(exp))
        if em and (em.group(1) or em.group(2) or em.group(3)):
            try:
                end = datetime.date.fromisoformat(em.group(4))
            except ValueError:
                end = None
            isos = set(ISO.findall(exp))
            plain = NEGATED.sub(" ", line)
            if (end is not None and end < today and isos == set([em.group(4)]) and not WORD_DATE.search(exp)
                    and not EVENT.search(line) and not ROW_KEEPS.search(plain)):
                return "past", "EXPIRES cell starts with end date %s" % end.isoformat()
    return ("mine" if seat in owners else "unclassified"), ""


def part_grants(b):
    part = "d (grants)"
    rel = "0_Brain/tasks/EXPIRING-GRANTS.md"
    text = b.read(rel, part)
    all_lines = text.split("\n")
    if not any(GRANTS_HEADER.match(l) for l in all_lines):
        piped = sum(1 for l in all_lines if l.lstrip().startswith("|"))
        raise BuildFail(part, "no grants table header ('| grant | given | EXPIRES | ...' at the left margin) found in %s, "
                              "although %d line(s) there start with a pipe: the table cannot be read, so no row can be proven dead or kept"
                        % (rel, piped))
    counts = {"rows": 0, "mine": 0, "unclassified": 0, "dead": 0, "other": 0, "past": 0,
              "expired_heading_kept": 0, "expired_heading_dropped": 0}
    mine, uncl, under = [], [], []
    header = "| grant | given | EXPIRES | scope, exactly |\n|---|---|---|---|"
    in_expired = False
    for lineno, line in enumerate(text.split("\n"), 1):
        if line.startswith("## "):
            in_expired = line[3:].strip().lower().startswith("expired")
            continue
        if not line.startswith("|"):
            continue
        cells = line.split("|")[1:-1]
        c0 = cells[0].strip() if cells else ""
        if c0.lower() == "grant" or (c0 and set(c0) <= set("-: ")):
            continue  # table header or separator
        counts["rows"] += 1
        verdict, why = classify_grant(line, b.seat, b.today)
        if verdict in ("dead", "other", "past"):
            counts[verdict] += 1
            b.dropped.append((verdict, lineno, why, c0[:80]))
            continue
        if in_expired:
            if b.trust_expired:
                counts["expired_heading_dropped"] += 1
                b.dropped.append(("expired_heading", lineno, "under the file's '## Expired' heading (--trust-expired-heading)", c0[:80]))
                continue
            counts["expired_heading_kept"] += 1
            under.append(line)
            continue
        counts[verdict] += 1
        (mine if verdict == "mine" else uncl).append(line)
    indented = sum(1 for l in all_lines if l.startswith((" |", "\t|")))
    if indented:
        raise BuildFail(part, "%d table line(s) in %s are indented, so they were not read as rows; fix the file's table" % (indented, rel))
    b.stats["grants"] = counts
    kept = len(mine) + len(uncl) + len(under)
    out = ["From `%s` as of %s: %d rows in the file, %d kept here." % (rel, b.today.isoformat(), counts["rows"], kept),
           "Kept: %d this seat's, %d unclassified, %d unclassified under the file's Expired heading. "
           "Dropped on proof: %d marked dead, %d another seat's, %d past their end date%s."
           % (len(mine), len(uncl), len(under), counts["dead"], counts["other"], counts["past"],
              (", %d under the Expired heading" % counts["expired_heading_dropped"]) if b.trust_expired else ""),
           "A row is dropped only on proof, so some rows kept here are dead in fact: read the EXPIRES cell before relying on one. "
           "A grant past its date is DEAD and is re-asked, never assumed. A grant NOT shown here is not thereby dead: read the file.",
           ""]
    for title, rows in (("### This seat's (%d)" % len(mine), mine),
                        ("### Unclassified: kept because nothing proves them dead or another seat's (%d)" % len(uncl), uncl),
                        ("### Unclassified, under the file's '## Expired' heading (%d)" % len(under), under)):
        if rows:
            out += [title, "", header] + rows + [""]
    if not kept:
        out.append("(no row kept)")
    b.add("d. Live grants (not provably dead, not provably another seat's)",
          [sec(rel, b.size(rel), "\n".join(out) + "\n", label=rel + " (filtered rows)")])


# ── e. ledger ──────────────────────────────────────────────────────────────────────────────────
def reduce_ledger_row(line):
    m = LEDGER_ROW.match(line)
    if not m:
        return None
    date, rest = m.group(1), m.group(2)
    hm = BOLD.search(rest)
    headline = hm.group(1).strip() if hm else rest.split("|")[0].strip()[:200]
    rm = RULE.search(rest)
    if rm:
        tail = rest[rm.end():].split(" | ")[0]
        se = SENT_END.search(tail)
        rule = tail[:se.end()] if se else tail.rstrip(" |")
        if len(rule) > RULE_MAX:
            rule = rule[:RULE_MAX].rstrip() + " [cut: see the row]"
        rule = "Rule%s: %s" % (rm.group(2) or "", rule.strip())
    else:
        rule = "(no 'Rule:' sentence in this row; read the row)"
    return "- %s | **%s** | %s" % (date, headline, rule)


def part_ledger(b):
    part = "e (ledger)"
    rel = "0_Brain/learnings/" + SEAT_FILES[b.seat]["ledger"]
    text = b.read(rel, part)
    if not any(LEDGER_HEADER.match(l) for l in text.split("\n")):
        raise BuildFail(part, "no ledger table header ('| Date | What happened ...') found in %s: its rows cannot be told from prose" % rel)
    rows = [r for r in (reduce_ledger_row(l) for l in text.split("\n")) if r]
    b.stats["ledger_rows"] = len(rows)
    arch = rel[:-3] + "_archive.md"
    out = ["From `%s`: %d rows, each reduced to date | headline | Rule sentence. The whole row (cause, cost, lesson link, weight) "
           "is in that file; rows moved out by the archive rule are in `%s` (read on demand)." % (rel, len(rows), arch), ""]
    out += rows or ["(no dated row)"]
    b.add("e. Own ledger (date, headline, rule)", [sec(rel, b.size(rel), "\n".join(out) + "\n", label=rel + " (reduced rows)")])


# ── f. pointers ────────────────────────────────────────────────────────────────────────────────
def part_pointers(b):
    ptrs = [
        ("Tasks", "0_Brain/tasks/TASKS.md"),
        ("The design this pack implements", "1_Project_Definition/Architecture/2026-11-27_fleet-structure-v2-design.md"),
        ("Project index", "0_Brain/projects_index/INDEX.md"),
        ("Kam's messages (verbatim, by view)", "2_Project_Files/tools/kam_msgs.sh"),
        ("Kam's rulings today (read every line before any card, brief or ruling)", "2_Project_Files/tools/kam_rulings_today.sh"),
        ("The whole grants file", "0_Brain/tasks/EXPIRING-GRANTS.md"),
        ("The whole rules card", "0_Brain/learnings/_rules_card_%s.md" % b.seat),
        ("The handover tool", "2_Project_Files/wake/handover.sh"),
    ]
    out = ["Paths only; nothing below is loaded. Open one when the work needs it.", ""]
    for name, rel in ptrs:
        out.append("- %s: `%s`%s" % (name, rel, "" if os.path.exists(b.p(rel)) else "  (NOT FOUND in this tree)"))
    b.add("f. Pointers (paths only)", [sec("-", None, "\n".join(out) + "\n", label="pointers (generated)")])


# ── render ─────────────────────────────────────────────────────────────────────────────────────
def sidecar_path(out):
    return (out[:-3] if out.endswith(".md") else out) + ".dropped.txt"


def sidecar_text(b, generated, pack_label):
    L = ["# Grant rows DROPPED from the wake pack %s (%s seat). Not part of the pack; not counted in its budget." % (pack_label, b.seat),
         "generated: " + generated,
         "# built for %s from 0_Brain/tasks/EXPIRING-GRANTS.md by %s. %d rows dropped." % (b.today.isoformat(), SELF_REL, len(b.dropped)),
         "# A live grant listed here was dropped by mistake: say so, and read it in the grants file at the line given.",
         "# class | line in the grants file | proof | first 80 characters of the row's first cell"]
    for key, lineno, why, cell in b.dropped:
        L.append("%s | line %d | %s | %s" % (DROP_CLASS[key], lineno, why, cell))
    return "\n".join(L) + "\n"


def render(b, budget, generated, side_label):
    body_parts = []
    rows = []
    for title, sections in b.parts:
        text = "## %s\n\n" % title + "\n".join(s["text"] for s in sections)
        body_parts.append(text)
        for s in sections:
            rows.append((title.split(".")[0], s["label"], s["src_bytes"], len(s["text"].encode("utf-8"))))
    body = "\n".join(body_parts)
    body_b = len(body.encode("utf-8"))
    sect_b = sum(r[3] for r in rows)
    total = body_b
    for _ in range(8):  # the manifest prints its own size: settle the fixed point
        man = ["---", "type: wake-pack", "seat: " + b.seat, "generated: " + generated, "built_for_date: " + b.today.isoformat(),
               "budget_tokens: %d" % budget,
               "source: GENERATED by %s --seat %s. Never hand-edit: a fix written here lasts until the next build." % (SELF_REL, b.seat),
               "---", "",
               "# Wake pack: %s seat" % b.seat, "",
               "Read this whole at boot. It replaces the whole reads of the rules card, the ledger, the pickup file, the grants file, "
               "the project index and its entries. It is a working model: the source named beside each part is the truth, and a "
               "fact from here is checked at its source before it is acted on.", "",
               "## Manifest", "",
               "| part | source | source bytes | bytes in pack | est. tokens (bytes/4) |", "|---|---|---|---|---|"]
        for part, label, sb, pb in rows:
            man.append("| %s | `%s` | %s | %d | %d |" % (part, label, "-" if sb is None else str(sb), pb, tok(pb)))
        man.append("| - | headings, manifest, this header | - | %d | %d |" % (total - sect_b, tok(total - sect_b)))
        man.append("| **total** | | | **%d** | **%d** of %d |" % (total, tok(total), budget))
        man.append("")
        man.append("Grant rows dropped from part d (%d): listed one per line, with class and proof, in `%s`. That file is not part of this "
                   "pack and not in its budget; look there before concluding a grant is gone." % (len(b.dropped), side_label))
        man.append("")
        head = "\n".join(man) + "\n"
        new_total = len(head.encode("utf-8")) + body_b
        if new_total == total:
            break
        total = new_total
    return head + body, rows, total


def build(root, seat, today, trust_expired):
    b = Build(root, seat, today, trust_expired)
    part_identity(b)
    part_rules(b)
    part_state(b)
    part_grants(b)
    part_ledger(b)
    part_pointers(b)
    return b


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def header_stamp(text):
    """The pack's own 'generated:' value, read ONLY from its front matter (the lines between the first two '---')."""
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        return None
    for l in lines[1:12]:
        if l == "---":
            return None
        if l.startswith("generated: "):
            return l[len("generated: "):]
    return None


def sidecar_stamp(text):
    """The sidecar's own 'generated:' value: its SECOND line and no other."""
    lines = text.split("\n")
    if len(lines) > 1 and lines[1].startswith("generated: "):
        return lines[1][len("generated: "):]
    return None


def read_text(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser(description="fixed-budget wake pack builder / checker")
    ap.add_argument("--seat", required=True)
    ap.add_argument("--budget-tokens", type=int, default=60000)
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--trust-expired-heading", action="store_true")
    ap.add_argument("--root")
    ap.add_argument("--today")
    a = ap.parse_args()
    if a.seat not in SEATS:
        eprint("wake_pack: unknown seat %r; use one of: %s" % (a.seat, ", ".join(SEATS)))
        return 2
    root = os.path.abspath(a.root) if a.root else ROOT
    try:
        today = datetime.date.fromisoformat(a.today) if a.today else datetime.date.today()
    except ValueError:
        eprint("wake_pack: --today must be YYYY-MM-DD, got %r" % a.today)
        return 2
    out = os.path.abspath(a.out) if a.out else os.path.join(root, "0_Brain", "wake", "WAKE-%s.md" % a.seat)
    try:
        b = build(root, a.seat, today, a.trust_expired_heading)
    except BuildFail as e:
        if a.check:
            print("FAULT: a build now would FAIL: %s" % e)
            print("wake_pack: STALE — the pack cannot be rebuilt until that source is fixed (root %s)" % root)
            return 1
        eprint("wake_pack: BUILD FAILED — nothing written (root %s). A part is never replaced by a placeholder." % root)
        eprint("wake_pack: FAILED — %s" % e)
        return 2
    side = sidecar_path(out)
    inside = os.path.commonpath([root, side]) == root
    side_label = os.path.relpath(side, root) if inside else os.path.basename(side)

    def make(stamp):
        text, rows, total = render(b, a.budget_tokens, stamp, side_label)
        return text, rows, total, sidecar_text(b, stamp, os.path.basename(out))

    generated = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    text, rows, total, side_text = make(generated)
    over = tok(total) > a.budget_tokens

    def by_part():
        agg = {}
        for part, label, sb, pb in rows:
            agg[part] = agg.get(part, 0) + pb
        names = dict((t.split(".")[0], t) for t, _ in b.parts)
        return [(names.get(part, part), part, pb) for part, pb in sorted(agg.items(), key=lambda kv: -kv[1])]

    if a.check:
        faults = []
        if not os.path.isfile(out):
            faults.append("pack missing: %s (run --seat %s)" % (out, a.seat))
        else:
            pm = os.stat(out).st_mtime_ns
            for src in b.sources + [os.path.abspath(__file__)]:
                if os.stat(src).st_mtime_ns > pm:
                    faults.append("source newer than the pack: %s" % os.path.relpath(src, root))
            have = read_text(out)
            m = re.search(r"^built_for_date: (\S+)$", have, re.M)
            if not m or m.group(1) != today.isoformat():
                faults.append("pack was built for %s, today is %s (the grant filter depends on the date)"
                              % (m.group(1) if m else "an unknown date", today.isoformat()))
            # CONTENT HASH (m1): rebuild with the pack's OWN header stamp and compare sha256 of the whole file.
            # No line is skipped, so a line added by hand cannot hide behind a 'generated:' prefix.
            stamp = header_stamp(have)
            if stamp is None:
                faults.append("the pack's front matter has no 'generated:' line: it was not written by this tool, or was edited")
            else:
                want = make(stamp)[0]
                if sha(have) != sha(want):
                    faults.append("pack content differs from what would be built now (sha256 %s on disk, %s expected)"
                                  % (sha(have)[:12], sha(want)[:12]))
            if not os.path.isfile(side):
                faults.append("dropped-rows sidecar missing: %s" % side)
            else:
                shave = read_text(side)
                sstamp = sidecar_stamp(shave)
                if sstamp is None:
                    faults.append("the sidecar's second line is not its 'generated:' line: edited or not this tool's (%s)" % side)
                else:
                    swant = make(sstamp)[3]
                    if sha(shave) != sha(swant):
                        faults.append("dropped-rows sidecar differs from what would be built now (sha256 %s on disk, %s expected): %s"
                                      % (sha(shave)[:12], sha(swant)[:12], side))
        if over:
            faults.append("a build now would be over budget: ~%d tokens of %d" % (tok(total), a.budget_tokens))
        if faults:
            for f in faults:
                print("FAULT: " + f)
            print("wake_pack: STALE — rebuild: python3 %s --seat %s" % (SELF_REL, a.seat))
            return 1
        print("OK: wake pack current (%s, %d bytes, ~%d tokens of %d, sha256 %s)"
              % (os.path.relpath(out, root), total, tok(total), a.budget_tokens, sha(read_text(out))[:12]))
        return 0

    if over:
        eprint("wake_pack: OVER BUDGET — nothing written. The pack would be %d bytes, ~%d tokens; the budget is %d tokens (over by ~%d)."
               % (total, tok(total), a.budget_tokens, tok(total) - a.budget_tokens))
        eprint("Parts, largest first:")
        parts = by_part()
        for name, part, pb in parts:
            eprint("  %8d B  ~%6d tokens  %s" % (pb, tok(pb), name))
            for p2, label, sb, pb2 in sorted((r for r in rows if r[0] == part), key=lambda r: -r[3]):
                eprint("            %8d B  %s" % (pb2, label))
        eprint("Shrink the largest SOURCE (its own rule: one handover block, dead grants marked DEAD, ledger rows archived), "
               "not the pack; or raise --budget-tokens on Kam's word.")
        eprint("wake_pack: FAILED — over budget: ~%d tokens of %d; the largest part is '%s' (%d bytes)"
               % (tok(total), a.budget_tokens, parts[0][0], parts[0][2]))
        return 3
    try:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        for path, body in ((side, side_text), (out, text)):  # the sidecar first, so the pack is never the older of the two
            tmp = "%s.tmp.%d" % (path, os.getpid())
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(body)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
    except OSError as e:
        eprint("wake_pack: FAILED — cannot write the pack at %s: %s" % (out, e))
        return 2
    g = b.stats["grants"]
    gs = "grants kept %d of %d (%d unclassified)" % (g["mine"] + g["unclassified"] + g["expired_heading_kept"], g["rows"],
                                                     g["unclassified"] + g["expired_heading_kept"])
    print("%s  bytes: %d  ~tokens: %d of %d  state: %s  %s  dropped rows listed in %s  ledger rows: %d"
          % (out, total, tok(total), a.budget_tokens, b.stats.get("state"), gs, os.path.basename(side), b.stats.get("ledger_rows", 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
