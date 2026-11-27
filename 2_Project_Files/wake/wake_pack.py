#!/usr/bin/env python3
"""wake_pack.py — build (or check) ONE fixed-budget wake pack for a coordinator seat (WED-170 step 1).

WHY: the boot prompt mandated ~917 KB of whole-file reads for the Wednesday seat (census 2026-11-27).
Most of it was handover history. The pack is one generated file with a hard token budget; over budget
it writes nothing and says which part grew.

Usage:
  wake_pack.py --seat <wednesday|tuesday|friday> [--budget-tokens 60000] [--out <path>]
      write the pack (default <root>/0_Brain/wake/WAKE-<seat>.md), print one summary line
  wake_pack.py --seat <seat> --check [--out <path>]
      exit 1 with one line per fault when the pack is missing, older than a source, built on an
      earlier date, or different from what would be built now; 0 with an OK line
  --root <dir>              tree root (default: derived from this file's location)   [tests]
  --today YYYY-MM-DD        the date stamped into the pack (default: today)   [tests]

Parts, in order (each section has a row in the manifest table at the top of the pack):
  a. identity   persona, voice protocol, Kam: verbatim
  b. rules      the rules card's "Most reinforced" section verbatim, then family headings with counts
  c. state      the seat's STATE block (handover.sh); if none yet, the legacy pickup's first block
  d. grants     EXPIRING-GRANTS.md WHOLE: the file's own bytes, every row verbatim, in file order
  e. ledger     each row of the seat's own ledger as date, headline, Rule sentence
  f. pointers   paths only

THE GRANTS REGISTER IS CARRIED WHOLE (round 4; Kam's ruling on card wed-wake-pack-second-nogo-whole-register-1127:
"One more round: whole grants list, lock fixed"). Rounds 1 to 3 dropped rows the tool judged dead, another
seat's or past their date. Two independent checks showed that a recogniser of wording cannot be finished:
each one dropped live rows it had not been taught. So this tool no longer judges any row. No row is dropped
for any reason, there is no dropped-rows sidecar, and no flag switches a filter on. Tidying dead rows out
of the register is a deliberate housekeeping act by a seat, on the register itself; the pack never guesses
it. If the register makes the pack exceed its budget the build REFUSES; the register is never trimmed to fit.

A PART NEVER SHRINKS TO A PLACEHOLDER (round 3, M2): a missing, empty or unreadable source, a rules card
without its "Most reinforced" section, a grants file or ledger whose table header is not found, a grants
file that is not valid UTF-8 (it could not be carried verbatim), or a state source with no block, is a
FAILED BUILD: exit 2, nothing written, the part named, and a last line that starts "wake_pack: FAILED"
for the launcher to show the seat. THE STATE PART REFUSES WHAT `handover.sh check` REFUSES (round 4, N6):
a state file with no tool header, a block that does not match its header's sha256 or size, a header
naming another seat, a missing part or a stack is a FAILED BUILD too (the same function decides both).

Exit codes: 0 ok; 1 --check found a fault; 2 usage or a failed build (a source missing, empty, unreadable
or without its expected structure); 3 over budget.
Standard library only. Globs skip '(conflict_on_' and '.pre-' names. Never discards stderr.
"""
import argparse
import datetime
import glob
import hashlib
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True   # the handover engine is loaded from this directory; leave no cache beside it

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

GRANTS_HEADER = re.compile(r"^\|\s*grant\s*\|\s*given\s*\|\s*EXPIRES\s*\|", re.I)
LEDGER_HEADER = re.compile(r"^\|\s*Date\s*\|\s*What happened", re.I)
LEDGER_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)$")
BOLD = re.compile(r"\*\*(.+?)\*\*")
RULE = re.compile(r"\b(Rule|RULE)(\s*\([^)|]{1,60}\))?:\s*")
SENT_END = re.compile(r"[.!?](?=\s+[A-Z\[(*\U0001F511]|\s*$)")
RULE_MAX = 700
# The 'generated:' stamp this tool writes (N5): --check refuses any other text on that line.
STAMP = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?: [A-Za-z0-9+:-]{1,12})?")


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
    def __init__(self, root, seat, today):
        self.root, self.seat, self.today = root, seat, today
        self.sources = []  # absolute paths actually read
        self.parts = []    # (title, [section dict])
        self.stats = {}
        self.raw = {}      # rel -> the bytes read

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
        self.raw[rel] = data
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
def state_cap(part):
    """The same cap handover.sh uses (HANDOVER_CAP_BYTES, default 10000)."""
    v = os.environ.get("HANDOVER_CAP_BYTES", "10000")
    if not re.fullmatch(r"[0-9]+", v):
        raise BuildFail(part, "HANDOVER_CAP_BYTES must be a whole number, got %r" % v)
    return int(v)


def handover_engine(part):
    """The handover engine that sits beside this file: its check_faults() is what `handover.sh check` runs."""
    path = os.path.join(HERE, "handover_core.py")
    try:
        spec = importlib.util.spec_from_file_location("wake_handover_core", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.check_faults
        return mod
    except Exception as e:  # missing, unreadable, or an older engine without check_faults
        raise BuildFail(part, "a state file exists but the handover engine at %s cannot be loaded to check it (%s: %s)"
                        % (path, type(e).__name__, e))


def part_state(b):
    part = "c (state)"
    rel = "0_Brain/tasks/STATE-%s.md" % b.seat
    state = b.read(rel, part, must_exist=False)
    if state is not None:
        # N6: the pack refuses what `handover.sh check` refuses, by calling the same function.
        faults, _, _ = handover_engine(part).check_faults(b.raw[rel], b.seat, state_cap(part))
        if faults:
            raise BuildFail(part, "%s is not one clean tool-written block (`handover.sh check` refuses it too): %s%s. "
                                  "Rewrite it through 2_Project_Files/wake/handover.sh write --stdin"
                            % (rel, faults[0], ("; and %d more fault(s)" % (len(faults) - 1)) if len(faults) > 1 else ""))
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


# ── d. grants: the register, WHOLE ─────────────────────────────────────────────────────────────
def part_grants(b):
    """The file's own text, start to end. No row is judged, dropped, moved or reworded (see the module text)."""
    part = "d (grants)"
    rel = "0_Brain/tasks/EXPIRING-GRANTS.md"
    text = b.read(rel, part)
    raw = b.raw[rel]
    if text.encode("utf-8") != raw:
        raise BuildFail(part, "%s is not valid UTF-8, so it cannot be carried verbatim; fix the file's encoding" % rel)
    lines = text.split("\n")
    if not any(GRANTS_HEADER.match(l) for l in lines):
        piped = sum(1 for l in lines if l.lstrip().startswith("|"))
        raise BuildFail(part, "no grants table header ('| grant | given | EXPIRES | ...' at the left margin) found in %s, "
                              "although %d line(s) there start with a pipe: this is not the register this part expects"
                        % (rel, piped))
    rows = 0
    for l in lines:  # counted for the reader only; nothing is selected by this loop
        if not l.lstrip().startswith("|"):
            continue
        cells = l.strip().split("|")[1:-1]
        c0 = cells[0].strip() if cells else ""
        if c0.lower() == "grant" or (c0 and set(c0) <= set("-: ")):
            continue
        rows += 1
    b.stats["grants_rows"] = rows
    head = ("From `%s`: the WHOLE register, verbatim and in file order (%d bytes, %d table rows, sha256 %s). "
            "Nothing is left out, moved or reworded, and this pack does NOT judge which grants are live. "
            "Some rows are dead, spent or another seat's: each row's own first cell and EXPIRES cell say so, and the "
            "file's own headings (an Expired section among them) are carried as they stand. Read a row's EXPIRES cell "
            "before relying on it. A grant past its date is DEAD and is re-asked, never assumed.\n\n"
            "<<< BEGIN %s (verbatim) >>>\n" % (rel, len(raw), rows, hashlib.sha256(raw).hexdigest()[:16], rel))
    tail = "%s<<< END %s (verbatim) >>>\n" % ("" if text.endswith("\n") else "\n", rel)
    b.add("d. Grants register (WHOLE, verbatim: every row, in file order)",
          [sec(rel, b.size(rel), head + text + tail, label=rel + " (whole, verbatim)")])


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
def render(b, budget, generated):
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
               "Read this whole at boot. It replaces the whole reads of the rules card, the ledger, the pickup file, the grants file "
               "(carried here whole, part d), the project index and its entries. It is a working model: the source named beside each part is the truth, and a "
               "fact from here is checked at its source before it is acted on.", "",
               "## Manifest", "",
               "| part | source | source bytes | bytes in pack | est. tokens (bytes/4) |", "|---|---|---|---|---|"]
        for part, label, sb, pb in rows:
            man.append("| %s | `%s` | %s | %d | %d |" % (part, label, "-" if sb is None else str(sb), pb, tok(pb)))
        man.append("| - | headings, manifest, this header | - | %d | %d |" % (total - sect_b, tok(total - sect_b)))
        man.append("| **total** | | | **%d** | **%d** of %d |" % (total, tok(total), budget))
        man.append("")
        head = "\n".join(man) + "\n"
        new_total = len(head.encode("utf-8")) + body_b
        if new_total == total:
            break
        total = new_total
    return head + body, rows, total


def build(root, seat, today):
    b = Build(root, seat, today)
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



def read_text(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", "replace")



def main():
    ap = argparse.ArgumentParser(description="fixed-budget wake pack builder / checker")
    ap.add_argument("--seat", required=True)
    ap.add_argument("--budget-tokens", type=int, default=60000)
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
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
        b = build(root, a.seat, today)
    except BuildFail as e:
        if a.check:
            print("FAULT: a build now would FAIL: %s" % e)
            print("wake_pack: STALE — the pack cannot be rebuilt until that source is fixed (root %s)" % root)
            return 1
        eprint("wake_pack: BUILD FAILED — nothing written (root %s). A part is never replaced by a placeholder." % root)
        eprint("wake_pack: FAILED — %s" % e)
        return 2

    def make(stamp):
        return render(b, a.budget_tokens, stamp)

    generated = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z").strip()
    text, rows, total = make(generated)
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
                faults.append("pack was built for %s, today is %s (a pack is built at each launch; yesterday's is stale)"
                              % (m.group(1) if m else "an unknown date", today.isoformat()))
            # CONTENT HASH (m1): rebuild with the pack's OWN header stamp and compare sha256 of the whole file.
            # No line is skipped, so a line added by hand cannot hide behind a 'generated:' prefix.
            # THE STAMP'S FORMAT IS CHECKED FIRST (N5): the rebuild copies the stamp from the pack, so any text
            # written on that line would otherwise be rebuilt as it stands and read as current.
            stamp = header_stamp(have)
            if stamp is None:
                faults.append("the pack's front matter has no 'generated:' line: it was not written by this tool, or was edited")
            elif not STAMP.fullmatch(stamp):
                faults.append("the pack's 'generated:' line is not a timestamp this tool writes (%r): edited by hand" % stamp[:80])
            else:
                want = make(stamp)[0]
                if sha(have) != sha(want):
                    faults.append("pack content differs from what would be built now (sha256 %s on disk, %s expected)"
                                  % (sha(have)[:12], sha(want)[:12]))
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
        eprint("Shrink the largest SOURCE (its own rule: one handover block, ledger rows archived, the grants register "
               "tidied by a deliberate housekeeping step on the register itself), not the pack; or raise --budget-tokens "
               "on Kam's word. The pack never trims a source to fit.")
        eprint("wake_pack: FAILED — over budget: ~%d tokens of %d; the largest part is '%s' (%d bytes)"
               % (tok(total), a.budget_tokens, parts[0][0], parts[0][2]))
        return 3
    if os.path.isdir(out):
        eprint("wake_pack: FAILED — the pack path %s is a directory; nothing written" % out)
        return 2
    tmp = "%s.tmp.%d" % (out, os.getpid())
    try:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, out)
    except OSError as e:
        eprint("wake_pack: FAILED — cannot write the pack at %s: %s" % (out, e))
        return 2
    print("%s  bytes: %d  ~tokens: %d of %d  state: %s  grants: the whole register, %d rows  ledger rows: %d"
          % (out, total, tok(total), a.budget_tokens, b.stats.get("state"), b.stats.get("grants_rows", 0), b.stats.get("ledger_rows", 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
