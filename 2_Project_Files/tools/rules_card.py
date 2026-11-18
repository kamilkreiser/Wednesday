#!/usr/bin/env python3
"""rules_card.py — generate (and check) the short per-seat RULES CARD from the rules index.

The lesson files in 0_Brain/learnings/ stay the source of truth. `_rules_index.tsv` is a sidecar with
one row per lesson (spec: 0_Brain/learnings/_rules_index/README.md). From it this tool writes a short
card read whole at boot, and answers "which rules apply at this moment" (--at).

Usage:
  rules_card.py --seat <wednesday|tuesday|friday>    write _rules_card_<seat>.md, print one summary line
  rules_card.py --at <trigger> [--seat <seat>]       print the live rules for that moment (nothing written)
  rules_card.py --check [--seat <seat>]              exit 1 with one line per fault, 0 with an OK line
  rules_card.py --stats                              counts by status / seat scope / family / trigger
  rules_card.py --weights                            TSV file/weight/own_rows/last (stdout), summary (stderr)
  rules_card.py --at <trigger> --top <n>             only the n highest-weight lines, then a '(+k more...)' line
                                                     (plus, never cut: this seat's own regressions of the last 30 days)
Multi-rule lessons: the `file` field may be `<lesson>.md#<n>` (n >= 2) for a lesson's 2nd, 3rd ... rule; the plain
`<lesson>.md` row is its first rule and must exist. A '#n' row shows its base lesson's weight.
Weights (reinforcement) = ledger table rows citing a lesson, recomputed every run from the _ledger*.md files;
never stored. A superseded row `-> <file>:` passes its weight to <file>.
Seat weights (P4): a seat with its own ledger files (SEAT_LEDGERS below; named by the files' own headers) also gets a
weight counted from those files only. The line shows it beside the fleet weight when the two differ: `[x5, seat x1]` (x = the multiply sign).
A seat REGRESSION = seat weight >= 3 and last seat citation within 30 days; `--top n` never cuts one (printed in addition,
marked). A seat with no ledger file of its own (wednesday: its rows share _ledger.md) sees no change at all.
Options: --learnings-dir <dir> (tests), --root <dir> (tree root for enforced_by paths; default = parent
of 2_Project_Files, derived from this file's location). Standard library only. Never discards stderr.
"""
import os, sys, glob, datetime, argparse, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LEARN = os.path.join(ROOT, "0_Brain", "learnings")

SEATS = ["wednesday", "tuesday", "friday"]
STATUSES = ["live", "dead", "superseded"]
VOCAB = ["boot", "brief", "launch", "pane", "review", "merge", "deploy", "card", "kam-message", "mail",
         "report", "verify", "tooling", "git", "rotate", "wrap", "lesson", "identity", "drive", "usage",
         "wait", "always"]
MAX_RULE = 260
ENF_TRUNC = 120


def read_index(path):
    """-> list of (lineno, fields). Skips blank lines and lines starting with #."""
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip("\r\n")
            if not line.strip() or line.startswith("#"):
                continue
            rows.append((n, line.split("\t")))
    return rows


def split_key(file_):
    """'x.md' -> ('x.md', 1, True); 'x.md#3' -> ('x.md', 3, True); 'x.md#1' / 'x.md#abc' / 'x.md#' -> (base, 0, False).
    A '#n' row is the n-th rule of lesson x.md (n >= 2); the plain row is its first rule."""
    if "#" not in file_:
        return file_, 1, True
    base, _, num = file_.partition("#")
    if num.isdigit() and int(num) >= 2:
        return base, int(num), True
    return base, 0, False


def label(r):
    """Display form of a row's lesson file: `file`, or `file` (rule n) for a '#n' row."""
    if r["n"] > 1:
        return "`%s` (rule %d)" % (r["base"], r["n"])
    return "`%s`" % r["base"]


def plain_label(r):
    return r["base"] if r["n"] <= 1 else "%s (rule %d)" % (r["base"], r["n"])


def good_rows(rows):
    out = []
    for n, f in rows:
        if len(f) == 7:
            base, num, ok = split_key(f[0])
            if not ok:
                continue  # bad '#n' suffix: reported as a fault by check(), never indexed
            out.append(dict(file=f[0], base=base, n=num, status=f[1], seats=f[2], family=f[3],
                            triggers=[t.strip() for t in f[4].split(",") if t.strip()],
                            enforced_by=f[5], rule=f[6]))
    return out


def for_seat(r, seat):
    s = [x.strip() for x in r["seats"].split(",")]
    return "all" in s or seat in s


def enforced(r):
    return r["enforced_by"].strip() not in ("-", "")


LEDGER_SKIP = ("(conflict_on_", ".pre-", "_fleet_insights")
# Which ledger files are one seat's OWN (file stems; stem.md and stem_archive.md). Taken from the files' headers:
# _ledger_friday.md "Friday's OWN corrections"; _ledger_laptop_datasec.md "LAPTOP (Datasec) seat" = Tuesday.
# Wednesday has none of its own: _ledger.md / _ledger_archive.md are the SHARED files (they also hold other seats' rows).
SEAT_LEDGERS = {"friday": "_ledger_friday", "tuesday": "_ledger_laptop_datasec"}
REGRESSION_W = 3
REGRESSION_DAYS = 30
ROW_RE = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})")
ABBR_RE = re.compile(r"(\d{4}-\d{2}-\d{2})_([^\s\[\]()`,|\u2026]*)\u2026")
MIN_ABBR = 20


def ledger_files(learn):
    out = []
    for p in sorted(glob.glob(os.path.join(learn, "_ledger*.md"))):
        name = os.path.basename(p)
        if any(x in name for x in LEDGER_SKIP):
            continue
        out.append(p)
    return out


def seat_ledger_files(learn, seat):
    stem = SEAT_LEDGERS.get(seat)
    if not stem:
        return []
    want = (stem + ".md", stem + "_archive.md")
    return [p for p in ledger_files(learn) if os.path.basename(p) in want]


def compute_weights(learn, rows, ledgers=None):
    """-> (weights, scanned). weights: file -> dict(w, own, last) after merging superseded rows into their
    target; scanned: ledger file name -> table rows scanned. Matching is a regex over the WHOLE line
    (row prose contains '|', so never by column)."""
    files = []
    for r in rows:
        if r["base"] not in files:
            files.append(r["base"])
    stems = {f: (f[:-3] if f.endswith(".md") else f) for f in files}
    pats = {f: re.compile(r"(?<![\w-])" + re.escape(stems[f]) + r"(?![\w-])") for f in files}
    own = dict((f, 0) for f in files)
    last = dict((f, "") for f in files)
    scanned = {}
    for p in (ledger_files(learn) if ledgers is None else ledgers):
        n = 0
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = ROW_RE.match(line)
                if not m:
                    continue
                n += 1
                date = m.group(1)
                cited = set(f for f in files if stems[f] in line and pats[f].search(line))
                for am in ABBR_RE.finditer(line):
                    d, rest = am.group(1), am.group(2)
                    if len(rest) < MIN_ABBR:
                        continue
                    pref = d + "_" + rest
                    hit = [f for f in files if stems[f].startswith(pref)]
                    if len(hit) == 1:
                        cited.add(hit[0])
                for f in cited:
                    own[f] += 1
                    if date > last[f]:
                        last[f] = date
        scanned[os.path.basename(p)] = n
    target = {}
    for r in rows:
        # only a lesson's plain (first-rule) row passes weight on; targets are always base file names
        if r["n"] == 1 and r["status"] == "superseded" and r["rule"].startswith("-> "):
            t = r["rule"][3:].split(":", 1)[0].strip()
            if t in own and t != r["base"]:
                target[r["base"]] = t
    def final(f):
        seen = set([f])
        while f in target:
            nxt = target[f]
            if nxt in seen:
                return None  # cycle: keep the weight where it is
            seen.add(nxt)
            f = nxt
        return f
    w = dict((f, own[f]) for f in files)
    lastm = dict(last)
    gave = set()
    for f in files:
        if f in target:
            t = final(f)
            if t is not None and t != f:
                w[t] += own[f]
                w[f] -= own[f]
                gave.add(f)
                if last[f] > lastm[t]:
                    lastm[t] = last[f]
    weights = dict((f, dict(w=w[f], own=own[f], last=lastm[f], passed=(f in gave))) for f in files)
    return weights, scanned


def seat_weights(learn, rows, seat):
    """-> weights computed from the seat's own ledger files only, or None when the seat has none (no change then)."""
    if not seat:
        return None
    files = seat_ledger_files(learn, seat)
    if not files:
        return None
    return compute_weights(learn, rows, files)[0]


def wlabel(weights, f, sw=None):
    n = weights.get(f, {}).get("w", 0)
    if n <= 0:
        return "[new]"
    if sw is not None:
        m = sw.get(f, {}).get("w", 0)
        if m > 0 and m != n:  # a seat weight of 0 is not printed: it was noise on most lines (Friday, 2026-11-18)
            return "[\u00d7%d, seat \u00d7%d]" % (n, m)
    return "[\u00d7%d]" % n


def is_regression(sw, f, today=None):
    """Seat weight >= REGRESSION_W and its last seat citation within REGRESSION_DAYS of today."""
    if sw is None:
        return False
    x = sw.get(f)
    if not x or x["w"] < REGRESSION_W or not x["last"]:
        return False
    today = today or datetime.date.today()
    try:
        last = datetime.date.fromisoformat(x["last"])
    except ValueError:
        return False
    return (today - last).days <= REGRESSION_DAYS


def wkey(weights):
    return lambda r: (-weights.get(r["base"], {}).get("w", 0), r["base"], r["n"])


def build_card(rows, seat, date, weights=None, sw=None):
    weights = weights or {}
    live = [r for r in rows if r["status"] == "live"]
    mine = [r for r in live if for_seat(r, seat)]
    on_card = [r for r in mine if not enforced(r)]
    enf = [r for r in mine if enforced(r)]
    dead = sorted(plain_label(r) for r in rows if r["status"] == "dead")
    sup = sorted(plain_label(r) for r in rows if r["status"] == "superseded")
    other = sorted(plain_label(r) for r in live if not for_seat(r, seat))
    lessons = len(set(r["base"] for r in rows))
    fams = {}
    for r in on_card:
        fams.setdefault(r["family"], []).append(r)
    L = ["---", "date: " + date, "type: rules-card",
         "source: GENERATED by 2_Project_Files/tools/rules_card.py --seat %s from _rules_index.tsv — never hand-edit" % seat,
         "status: live", "---", "",
         "# Rules card — %s seat" % seat, "",
         "- Each line is one lesson's working rule with its reinforcement count: [\u00d71] happened once and is worth noting, [\u00d72] is the start of a pattern, higher counts have been reinforced and deserve the most attention.",
         "- These are weighted guidance, not absolute laws. The hard rules live in the project rules file (client separation, secrets, production, money, external messages, irreversible actions) and stay hard.",
         "- Open the family file in families/ or the lesson itself the moment a rule fires or a diagnosis needs its cases.",
         "- Lessons that say the same thing are merged into one line; the count carries their combined reinforcement.", "",
         "Counts: %d lessons, %d rule lines, %d on this card, %d enforced, %d dead, %d superseded, %d other-seat-only"
         % (lessons, len(rows), len(on_card), len(enf), len(dead), len(sup), len(other)), ""]
    # one line per lesson: only the plain (first-rule) row, so one heavily cited lesson cannot fill the section
    top = [r for r in sorted(on_card, key=wkey(weights)) if r["n"] == 1 and weights.get(r["base"], {}).get("w", 0) > 0][:20]
    L.append("## Most reinforced (read these first)")
    for r in top:
        L.append("- %s %s \u2014 %s" % (wlabel(weights, r["base"], sw), r["rule"], label(r)))
    if not top:
        L.append("- (nothing reinforced yet)")
    L.append("")
    for fam in sorted(fams, key=lambda k: (-len(fams[k]), k)):
        L.append("## " + fam)
        for r in sorted(fams[fam], key=wkey(weights)):
            L.append("- %s %s \u2014 %s" % (wlabel(weights, r["base"], sw), r["rule"], label(r)))
        L.append("")
    L.append("## Enforced by a tool (the tool remembers; one line each)")
    for r in sorted(enf, key=lambda x: (x["base"], x["n"])):
        rule = r["rule"]
        if len(rule) > ENF_TRUNC:
            rule = rule[:ENF_TRUNC] + "…"
        L.append("- %s — enforced by `%s` — %s" % (rule, r["enforced_by"], label(r)))
    L.append("")
    L.append("## Not on this card")
    L.append("- dead: " + ", ".join(dead))
    L.append("- superseded: " + ", ".join(sup))
    L.append("- other seats only: " + ", ".join(other))
    L.append("")
    return "\n".join(L), len(on_card)


def strip_date(text):
    return "\n".join(l for l in text.split("\n") if not l.startswith("date: "))


def derive_seat():
    s = os.environ.get("WED_SEAT")
    if s:
        return s.strip().lower()
    for key, seat in (("/FRIDAY", "friday"), ("/TUESDAY", "tuesday"), ("/WEDNESDAY", "wednesday")):
        if key in ROOT:
            return seat
    return None


def check(learn, root, seat, rows):
    faults = []
    idx = os.path.join(learn, "_rules_index.tsv")
    seen = {}
    bases = set()
    plain = set()
    extra = []  # (line, base, key) for valid '#n' rows
    for n, f in rows:
        if len(f) != 7:
            faults.append("line %d: wrong field count (%d fields, need 7): %s" % (n, len(f), f[0]))
            continue
        file_, status, seats, fam, trig, enf, rule = f
        base, num, ok = split_key(file_)
        bases.add(base)
        if not ok:
            faults.append("line %d: bad rule number in %s (a '#n' suffix needs an integer n >= 2)" % (n, file_))
        else:
            key = base if num == 1 else "%s#%d" % (base, num)
            if key in seen:
                faults.append("line %d: duplicate row for %s (first at line %d)" % (n, key, seen[key]))
            else:
                seen[key] = n
            if num == 1:
                plain.add(base)
            else:
                extra.append((n, base, key))
        if not os.path.isfile(os.path.join(learn, base)):
            faults.append("line %d: index row names missing file %s%s" % (n, base, "" if base == file_ else " (row %s)" % file_))
        if status not in STATUSES:
            faults.append("line %d: bad status %r in %s" % (n, status, file_))
        for s in [x.strip() for x in seats.split(",")]:
            if s != "all" and s not in SEATS:
                faults.append("line %d: bad seats value %r in %s" % (n, s, file_))
        ts = [t.strip() for t in trig.split(",")]
        if not any(ts):
            faults.append("line %d: bad trigger (empty) in %s" % (n, file_))
        for t in ts:
            if t and t not in VOCAB:
                faults.append("line %d: bad trigger %r in %s" % (n, t, file_))
        if enf.strip() not in ("-", "") and not os.path.exists(os.path.join(root, enf.strip())):
            faults.append("line %d: enforced_by path does not exist: %s (%s)" % (n, enf, file_))
        if not rule.strip():
            faults.append("line %d: rule empty in %s" % (n, file_))
        elif len(rule) > MAX_RULE:
            faults.append("line %d: rule too long (%d > %d chars) in %s" % (n, len(rule), MAX_RULE, file_))
    for n, base, key in extra:
        if base not in plain:
            faults.append("line %d: %s has no plain row for %s (the plain row is the lesson's first rule and must exist)" % (n, key, base))
    for p in sorted(glob.glob(os.path.join(learn, "20*.md"))):
        name = os.path.basename(p)
        if "(conflict_on_" in name:
            continue  # Unison conflict copies are not lessons (same exclusion as boot_digest.py)
        if name not in bases:
            faults.append("lesson file has no index row: " + name)
    if seat:
        card = os.path.join(learn, "_rules_card_%s.md" % seat)
        if not os.path.isfile(card):
            faults.append("card missing: %s (run --seat %s)" % (card, seat))
        else:
            g = good_rows(rows)
            want, _ = build_card(g, seat, "", compute_weights(learn, g)[0], seat_weights(learn, g, seat))
            have = open(card, encoding="utf-8").read()
            if strip_date(want) != strip_date(have):
                faults.append("card stale: %s differs from what would be generated now (run --seat %s)" % (card, seat))
    return faults


def stats(rows):
    g = good_rows(rows)
    def count(vals):
        d = {}
        for v in vals:
            d[v] = d.get(v, 0) + 1
        return d
    def show(title, d):
        print(title)
        for k in sorted(d, key=lambda k: (-d[k], k)):
            print("  %-45s %d" % (k, d[k]))
    print("rows: %d (well-formed %d)" % (len(rows), len(g)))
    print("lessons: %d, rule lines: %d" % (len(set(r["base"] for r in g)), len(g)))
    show("by status:", count(r["status"] for r in g))
    show("by seat scope:", count(r["seats"] for r in g))
    show("by family:", count(r["family"] for r in g))
    show("by trigger:", count(t for r in g for t in r["triggers"]))
    print("enforced: %d" % sum(1 for r in g if enforced(r)))


def main():
    ap = argparse.ArgumentParser(description="rules card generator / checker")
    ap.add_argument("--seat")
    ap.add_argument("--at")
    ap.add_argument("--if-card", action="store_true",
                    help="with --at: print nothing unless this seat already has a generated card (a seat that has not adopted the card sees no change)")
    ap.add_argument("--primary", action="store_true",
                    help="with --at: only rows whose FIRST trigger is the one asked for (the short list a tool prints at the moment of action)")
    ap.add_argument("--weights", action="store_true", help="TSV of file, weight, own_rows, last (stdout); summary on stderr")
    ap.add_argument("--top", type=int, help="with --at: only the n highest-weight lines")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--learnings-dir")
    ap.add_argument("--root")
    a = ap.parse_args()
    learn = os.path.abspath(a.learnings_dir) if a.learnings_dir else LEARN
    root = os.path.abspath(a.root) if a.root else ROOT
    idx = os.path.join(learn, "_rules_index.tsv")
    if a.seat and a.seat not in SEATS:
        print("unknown seat %r; use one of: %s" % (a.seat, ", ".join(SEATS)), file=sys.stderr)
        return 2

    if a.at is not None:
        if not os.path.isfile(idx):
            return 0
        if a.at not in VOCAB:
            print("unknown trigger %r; vocabulary: %s" % (a.at, " ".join(VOCAB)), file=sys.stderr)
            return 2
        seat = a.seat or derive_seat()
        if seat not in SEATS:
            print("cannot determine seat; pass --seat or set WED_SEAT", file=sys.stderr)
            return 2
        if a.if_card and not os.path.isfile(os.path.join(os.path.dirname(idx), "_rules_card_%s.md" % seat)):
            return 0
        hits = [r for r in good_rows(read_index(idx)) if r["status"] == "live"
                and for_seat(r, seat) and a.at in r["triggers"]
                and (not a.primary or r["triggers"][:1] == [a.at])]
        allrows = good_rows(read_index(idx))
        wts = compute_weights(learn, allrows)[0]
        sw = seat_weights(learn, allrows, seat)
        hits = sorted(hits, key=wkey(wts))
        shown = hits[:a.top] if a.top is not None and a.top >= 0 else hits
        # P4: --top never cuts this seat's own recent regression; those are printed in addition, marked
        kept = [r for r in hits[len(shown):] if is_regression(sw, r["base"])]
        print("Rules for: %s (%d)" % (a.at, len(hits)))
        for r in shown + kept:
            print("• %s %s%s%s  (%s)" % (wlabel(wts, r["base"], sw), "[seat regression] " if r in kept else "",
                                         "[enforced] " if enforced(r) else "", r["rule"],
                                         r["base"] if r["n"] <= 1 else "%s, rule %d" % (r["base"], r["n"])))
        if len(hits) > len(shown) + len(kept):
            print("(+%d more: rules_card.py --at %s)" % (len(hits) - len(shown) - len(kept), a.at))
        return 0

    if not os.path.isfile(idx):
        print("index not found: " + idx, file=sys.stderr)
        return 1 if a.check else 2

    rows = read_index(idx)
    if a.check:
        faults = check(learn, root, a.seat, rows)
        if faults:
            for f in faults:
                print("FAULT: " + f)
            return 1
        print("OK: rules index clean (%d rows%s)" % (len(rows), ", card %s current" % a.seat if a.seat else ""))
        return 0
    if a.stats:
        stats(rows)
        return 0
    if a.weights:
        g = good_rows(rows)
        wts, scanned = compute_weights(learn, g)
        for f in sorted(wts, key=lambda k: (-wts[k]["w"], k)):
            x = wts[f]
            print("%s\t%d\t%d\t%s" % (f, x["w"], x["own"], x["last"] or "-"))
        keep = [x["w"] for x in wts.values() if not x["passed"]]
        print("weights: 0=%d 1=%d 2=%d 3+=%d (lessons=%d, excluding %d merged into a target); ledger rows scanned: %s"
              % (sum(1 for v in keep if v == 0), sum(1 for v in keep if v == 1), sum(1 for v in keep if v == 2),
                 sum(1 for v in keep if v >= 3), len(keep), len(wts) - len(keep),
                 ", ".join("%s=%d" % (k, scanned[k]) for k in sorted(scanned)) or "none"), file=sys.stderr)
        return 0
    if a.seat:
        g = good_rows(rows)
        text, n = build_card(g, a.seat, datetime.date.today().isoformat(), compute_weights(learn, g)[0],
                             seat_weights(learn, g, a.seat))
        out = os.path.join(learn, "_rules_card_%s.md" % a.seat)
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print("%s  rows on card: %d  bytes: %d" % (out, n, len(text.encode("utf-8"))))
        return 0
    ap.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
