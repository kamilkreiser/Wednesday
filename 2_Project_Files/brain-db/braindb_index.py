#!/usr/bin/env python3
"""braindb_index.py - the indexer behind braindb.sh (rebuild / check / search / at / info).

A LOCAL, REBUILDABLE full-text index over one seat's markdown brain. The files stay the master:
this tool only ever reads them, and writes only into the Postgres cluster named by the caller.

Called by braindb.sh, which sets the environment:
  BRAINDB_ROOT_EFF   tree root to index (the seat's tree, or a fixture tree in tests)
  BRAINDB_SCOPE_EFF  scope file (the allow-list) for the seat
  BRAINDB_SEAT       wednesday | tuesday | friday
  BRAINDB_SOCKDIR_EFF, BRAINDB_PORT_EFF, BRAINDB_PGBIN_EFF   how to reach psql and the server

Standard library only. Database access is through psql only. No network, no model call.
stderr of every child process is inherited, never discarded.
"""
import os, sys, re, json, hashlib, fnmatch, subprocess, time, datetime, argparse

DB = "braindb"
KINDS = ("rules", "lesson", "rules_index", "ledger", "daily", "skill", "identity", "people", "architecture")
SEARCH_KINDS = ("rules", "lesson", "ledger", "daily", "skill", "identity", "people", "architecture")
# A seat's own RECORDS: for these kinds a deny_seat_word is tested on the file name too. For every kind it is
# tested on the directory names. Lessons, skills and the rest are decided by content rules, never by a name.
RECORD_KINDS = ("ledger", "daily")
# Search shows knowledge (rules files, lessons, skills, ...) ahead of records (incident rows) by default.
RECORD_GROUP = ("ledger", "daily")
MAX_ROW_CHARS = 80000        # a search row's text is cut here (Postgres refuses a tsvector over 1 MB)
MAX_HEAD_CHARS = 20000       # titles, headings and rule lines
# Where a kind's files live. Only THERE may a lesson, skill, identity, people, architecture or rules file
# carry another seat's word in its NAME (ANSWER-1 ruling 2); anywhere else the name is tested (ANSWER-3 F11).
HOME = {"lesson": ("0_brain/learnings",), "skill": ("0_brain/skills",), "identity": ("0_brain/identity",),
        "people": ("0_brain/people",), "architecture": ("1_project_definition/architecture",),
        "rules": ("", "0_brain")}
LESSON_NAME = re.compile(r"\d{4}-\d{2}-\d{2}[_-].+\.md", re.S)   # used with fullmatch: a name may hold any character
DAILY_NAME = re.compile(r"\d{4}-\d{2}-\d{2}\.md")
TIERISH = re.compile(r'(?i)^\W*"?tier"?\s*:')                       # a line that looks like a tier line
MARKER = re.compile(r"(?i)^\s*<!--\s*tier\s*:\s*(.*?)\s*-->\s*$")   # a section's tier marker, any case or indent
FM_FENCE = re.compile(r"^---\s*$")
CLIENT_SEG = re.compile(r"^p\s*(?:-|\()\s*([^/()]*?)\s*(?:/|\)|$)")  # the CLIENT of 'P-Client/Project' or 'P (Client/Project)'
STRIP_BYTES = {0x00: None, 0x1e: None, 0x1f: None}                 # NUL, and the two bytes psql output is split on
ITEM_RE = re.compile(r"^(\d+[a-z]?(?:-[ivx]+)?)\.\s+(.*)$")
# Refused in code even when a scope file names them (matched on whole path segments, lower case).
HARD_DENY_PREFIX = ("4_credentials", "3_access_keys", "0_brain/dashboard", "0_brain/reference")
HARD_DENY_SEGMENT = ("4_credentials", "3_access_keys")
SEATS = ("wednesday", "tuesday", "friday")

HEAD_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
P_MARK = re.compile(r"^<!--\s*tier:\s*(P-.*?)\s*-->\s*$")          # same marker boot_digest.py reads
LEDGER_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s?(.*)$")
BOLD = re.compile(r"\*\*(.+?)\*\*")
BULLET = re.compile(r"^\s*[-*]\s+(.*)$")
STAMP = re.compile(r"^(\d{1,2}:\d{2})(?::\d{2})?\b")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ABBR_RE = re.compile(r"(\d{4}-\d{2}-\d{2})_([^\s\[\]()`,|\u2026]*)\u2026")   # as rules_card.py
MIN_ABBR = 20
US, RS = "\x1f", "\x1e"


def die(msg, rc=2):
    print("braindb: " + msg, file=sys.stderr)
    sys.exit(rc)


def env(name):
    v = os.environ.get(name, "")
    if not v:
        die("%s is not set (run this through braindb.sh)" % name)
    return v


# ---------------------------------------------------------------- scope (the allow-list)

def load_scope(path, seat):
    if not os.path.isfile(path):
        die("no scope file for seat '%s' at %s. A seat is indexed only through its own reviewed "
            "allow-list; see proposed/INSTRUCTIONS-for-other-seats.md" % (seat, path))
    sc = dict(seat=None, own=[], deny_clients=[], allow=[], deny_path=[], deny_seat_word=[], path=path)
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            key, _, rest = s.partition(" ")
            rest = rest.strip()
            where = "%s line %d" % (path, n)
            if key == "seat":
                sc["seat"] = rest
            elif key == "own_clients":
                sc["own"] = rest.lower().split()
            elif key == "deny_clients":
                sc["deny_clients"] = rest.lower().split()
            elif key == "deny_path":
                if not rest:
                    die("%s: deny_path needs a value" % where)
                sc["deny_path"].append(rest.lower())
            elif key == "deny_seat_word":
                if not re.match(r"^[A-Za-z0-9_]+$", rest):
                    die("%s: deny_seat_word needs one plain word" % where)
                sc["deny_seat_word"].append(rest.lower())
            elif key == "allow":
                kind, _, glob_ = rest.partition(" ")
                glob_ = glob_.strip()
                if kind not in KINDS:
                    die("%s: unknown kind %r (kinds: %s)" % (where, kind, " ".join(KINDS)))
                check_allow(glob_, kind, where)
                sc["allow"].append((kind, glob_))
            else:
                die("%s: unknown directive %r" % (where, key))
    if sc["seat"] != seat:
        die("scope file %s is for seat %r but this tree resolves to seat %r" % (path, sc["seat"], seat))
    if not sc["allow"]:
        die("scope file %s has no allow lines" % path)
    return sc


def check_allow(glob_, kind, where):
    """An allow line is one plain directory plus one file-name pattern. Refuses anything wider."""
    if not glob_ or glob_.startswith("/") or "\\" in glob_:
        die("%s: allow path must be relative to the tree root: %r" % (where, glob_))
    d, pat = os.path.split(glob_)
    segs = d.split("/")
    if not d:
        # a file at the tree root: one exact name, no pattern (the seat's own rules file)
        if kind != "rules" or any(c in pat for c in "*?[") or not pat.endswith(".md"):
            die("%s: only an exactly named .md file of kind 'rules' may sit at the tree root: %r" % (where, glob_))
        return
    if any(s in ("", ".", "..") for s in segs):
        die("%s: allow path needs a plain directory (no '..', no empty segment): %r" % (where, glob_))
    if any(c in d for c in "*?["):
        die("%s: no wildcard is allowed in the directory part (no recursion): %r" % (where, glob_))
    low = d.lower()
    for p in HARD_DENY_PREFIX:
        if low == p or low.startswith(p + "/"):
            die("%s: REFUSED, %s is never indexed (hard exclusion in braindb_index.py): %r" % (where, p, glob_))
    if any(s in HARD_DENY_SEGMENT for s in low.split("/")):
        die("%s: REFUSED, a credentials or keys directory is never indexed: %r" % (where, glob_))
    want = ".tsv" if kind == "rules_index" else ".md"
    if not pat.endswith(want):
        die("%s: a %s pattern must end in %s: %r" % (where, kind, want, glob_))
    if pat.lower().startswith("chat_"):
        die("%s: REFUSED, chat stores are never indexed: %r" % (where, glob_))


def enumerate_files(root, sc):
    """-> ({rel: kind}, [(rel, reason)]) for every allow-list match; the second list is what was skipped."""
    out, skipped = {}, []
    rroot = os.path.realpath(root)
    for kind, glob_ in sc["allow"]:
        d, pat = os.path.split(glob_)
        absd = os.path.join(root, d) if d else root
        if not os.path.isdir(absd):
            continue
        if d and os.path.realpath(absd) != os.path.join(rroot, d):
            skipped.append((d + "/", "directory is or sits under a symlink"))
            continue
        try:
            names = sorted(os.listdir(absd))
        except OSError as e:
            skipped.append((d + "/", "unreadable: %s" % type(e).__name__))
            continue
        for name in names:
            if not fnmatch.fnmatchcase(name, pat):
                continue
            rel = (d + "/" + name) if d else name
            low = rel.lower()
            hit = next((x for x in sc["deny_path"] if x in low), None)
            if hit:
                skipped.append((rel, "path contains '%s'" % hit))
                continue
            dlow, nlow = d.lower(), name.lower()
            # a file is taken only under the kind its name and folder say it is
            if kind == "lesson" and not LESSON_NAME.fullmatch(name):
                skipped.append((rel, "not a lesson file name (a lesson's name starts with its date)"))
                continue
            if kind == "daily" and not DAILY_NAME.fullmatch(name):
                skipped.append((rel, "not a daily-note file name (a plain date, nothing more)"))
                continue
            if kind == "ledger" and not nlow.startswith("_ledger"):
                skipped.append((rel, "not a ledger file name"))
                continue
            if kind != "ledger" and nlow.startswith("_ledger"):
                skipped.append((rel, "a ledger file is indexed only by an 'allow ledger' line"))
                continue
            if kind != "daily" and os.path.basename(dlow).startswith("daily"):
                skipped.append((rel, "a daily-note folder is indexed only by an 'allow daily' line"))
                continue
            # another seat's own records: its word in a folder name (any kind), or in the file name, unless the
            # file sits in its kind's home folder (a lesson, skill or architecture file may be NAMED for a seat)
            name_exempt = kind in HOME and dlow in HOME[kind]
            hit = next((x for x in sc["deny_seat_word"] if x in dlow or (not name_exempt and x in nlow)), None)
            if hit:
                skipped.append((rel, "another seat's records ('%s' in the %s)" % (hit, "folder name" if hit in dlow else "file name")))
                continue
            p = os.path.join(absd, name)
            try:
                st = os.lstat(p)
            except OSError as e:
                skipped.append((rel, "unreadable: %s" % type(e).__name__))
                continue
            if os.path.islink(p):
                skipped.append((rel, "symlink"))
                continue
            if not os.path.isfile(p):
                skipped.append((rel, "not a regular file"))
                continue
            if st.st_nlink > 1:
                skipped.append((rel, "hard link (link count %d): the same file exists under another name" % st.st_nlink))
                continue
            out.setdefault(rel, kind)
    return out, skipped


def tier_verdict(tier, sc):
    """-> (indexed?, reason). W / M / MIXED / untagged are indexed. A project tier is indexed only when its
    CLIENT segment is exactly one of the seat's own clients (never a substring of the project name).
    A denied client's name anywhere in the value excludes. Anything else is unknown, and excluded."""
    t = (tier or "").strip().strip("\"'").strip()
    if not t:
        return True, "untagged"
    low = t.lower()
    for c in sc["deny_clients"]:
        if c in low:
            return False, "tier '%s' names %s" % (t, c)
    if low in ("w", "m", "mixed"):
        return True, t
    m = CLIENT_SEG.match(low)
    if m:
        client = m.group(1).strip()
        if client in sc["own"]:
            return True, t
        return False, "project tier '%s': its client is not one of this seat's" % t
    return False, "unknown tier value '%s'" % t


# ---------------------------------------------------------------- parsing

def read_file(p):
    """-> (raw bytes, text). The text has no BOM, no NUL and neither of the two separator bytes."""
    with open(p, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="replace")
    if text.startswith("\ufeff"):
        text = text[1:]
    return raw, text.replace("\r\n", "\n").translate(STRIP_BYTES)


def parse_frontmatter(text):
    """-> (fm dict, body, body_first_line, faults). Keys are folded (stripped, unquoted, lower case).
    `faults` lists every way the head is ambiguous about the lesson's tier; the caller EXCLUDES a lesson
    with any fault (fail closed): unclosed frontmatter, tier given more than once (in the block, in a second
    block, or as a stray line before the first heading), or a tier line whose value could not be read."""
    lines = text.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    fm, faults, tier_lines, start = {}, [], 0, 0
    if i < len(lines) and FM_FENCE.match(lines[i]):
        j = i + 1
        while j < len(lines) and not FM_FENCE.match(lines[j]):
            j += 1
        if j >= len(lines):
            faults.append("the frontmatter is not closed")
        block, start = lines[i + 1:j], min(j + 1, len(lines))
        for line in block:
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip().strip("\"'").strip().lower()
                if k == "tier":
                    tier_lines += 1
                if k:
                    fm[k] = v.strip().strip("\"'").strip()
            elif TIERISH.match(line):
                tier_lines += 1
        k = start
        while k < len(lines) and not lines[k].strip():
            k += 1
        if k < len(lines) and FM_FENCE.match(lines[k]) and any(FM_FENCE.match(l) for l in lines[k + 1:k + 40]):
            faults.append("a second frontmatter block follows the first")
    # stray tier lines between the frontmatter and the first heading (section markers are not tier lines)
    for line in lines[start:start + 60]:
        if HEAD_RE.match(line):
            break
        if TIERISH.match(line) and not MARKER.match(line):
            tier_lines += 1
    if tier_lines > 1:
        faults.append("tier is given more than once")
    if tier_lines >= 1 and not fm.get("tier"):
        faults.append("a tier line is present but no tier value could be read from the frontmatter")
    return fm, "\n".join(lines[start:]), start + 1, faults


def heading_lines(lines):
    """Indices of real headings (not inside a code fence)."""
    out, fenced = [], False
    for i, l in enumerate(lines):
        if FENCE_RE.match(l):
            fenced = not fenced
            continue
        if not fenced and HEAD_RE.match(l):
            out.append(i)
    return out


def drop_foreign_sections(lines, sc):
    """Blank out every section marked <!-- tier: ... --> for a client this seat may not index (marker in any
    case, with any indent, in either spelling, blank lines allowed before its heading). The dropped span runs
    from the marker to the next heading of the SAME OR A HIGHER level, so sub-sections go with it. A marker
    with no heading directly under it drops everything to the next heading. Line numbers are kept."""
    heads = heading_lines(lines)
    level = dict((i, len(HEAD_RE.match(lines[i]).group(1))) for i in heads)
    drop, dropped = set(), []
    for k, l in enumerate(lines):
        m = MARKER.match(l)
        if not m:
            continue
        ok, why = tier_verdict(m.group(1), sc)
        if ok:
            continue
        j = k + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j in level:
            end = next((h for h in heads if h > j and level[h] <= level[j]), len(lines))
            name = HEAD_RE.match(lines[j]).group(2)
        else:
            end = next((h for h in heads if h > k), len(lines))
            name = "(no heading directly under the marker)"
        drop.update(range(k, end))
        dropped.append((m.group(1), name))
    kept = ["" if (i in drop or MARKER.match(l)) else l for i, l in enumerate(lines)]
    return kept, dropped


def chunk(lines, first_line, fallback_title):
    """-> (title, [(line_no, heading, text)]) split at headings; a section with no text is skipped."""
    heads = heading_lines(lines)
    title = fallback_title
    for i in heads:
        m = HEAD_RE.match(lines[i])
        if len(m.group(1)) == 1:
            title = m.group(2)
            break
    out = []
    bounds = [(-1, title)] + [(i, HEAD_RE.match(lines[i]).group(2)) for i in heads]
    for n, (i, head) in enumerate(bounds):
        end = bounds[n + 1][0] if n + 1 < len(bounds) else len(lines)
        text = "\n".join(lines[i + 1:end]).strip()
        if text:
            out.append((first_line + max(i, 0), head, text))
    return title, out


def chunk_rules(lines, first_line, fallback_title):
    """A rules file (CLAUDE.md): one row per numbered rule, and one row for each heading section's other text.
    -> (title, [(line_no, heading, lead, text)]); lead is the rule's bold opening words, if any."""
    heads = heading_lines(lines)
    title = fallback_title
    for i in heads:
        m = HEAD_RE.match(lines[i])
        if len(m.group(1)) == 1:
            title = m.group(2)
            break
    out = []
    bounds = [(-1, title)] + [(i, HEAD_RE.match(lines[i]).group(2)) for i in heads]
    for n, (i, head) in enumerate(bounds):
        end = bounds[n + 1][0] if n + 1 < len(bounds) else len(lines)
        cur = [first_line + max(i, 0), head, None, []]       # the section's own text, before any numbered rule
        items = [cur]
        fenced = False
        for k in range(i + 1, end):
            l = lines[k]
            if FENCE_RE.match(l):
                fenced = not fenced
            m = None if fenced else ITEM_RE.match(l)
            if m:
                b = BOLD.match(m.group(2))
                cur = [first_line + k, "%s > rule %s" % (head, m.group(1)), b.group(1) if b else None, [l]]
                items.append(cur)
            else:
                cur[3].append(l)
        for ln, h, lead, body in items:
            text = "\n".join(body).strip()
            if text:
                out.append((ln, h, lead, text))
    return title, out


def iso_date(s):
    s = (s or "").strip()[:10]
    if not DATE_RE.match(s):
        return None
    try:
        datetime.date.fromisoformat(s)
    except ValueError:
        return None
    return s


def slug_words(name):
    stem = name[:-3] if name.endswith(".md") else name
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}[_-]?", "", stem)
    return re.sub(r"[-_.]+", " ", stem).strip()


def parse_ledger(text):
    """-> [(line_no, date, headline, rule_sentence, body)] one per table row whose first cell is a date."""
    rows = []
    for n, line in enumerate(text.split("\n"), 1):
        m = LEDGER_ROW.match(line)
        if not m:
            continue
        date = iso_date(m.group(1))
        body = m.group(2).rstrip()
        if body.endswith("|"):
            body = body[:-1].rstrip()
        b = BOLD.search(body)
        headline = b.group(1).strip() if b else body[:200]
        rule = ""
        k = body.find("Rule:")
        if k == -1:
            k = body.find("\U0001F511")           # the key marker that introduces the lesson link
        if k != -1:
            rule = body[k:].split(" | ", 1)[0].strip()
        rows.append((n, date, headline, rule, body))
    return rows


def parse_daily(text):
    """-> [(line_no, stamp, section, is_bullet, body)]. One row per bullet line; a non-bullet, non-heading
    line is folded into the bullet above it, or kept as its own row when there is none in the section."""
    rows, section, fenced = [], "", False
    for n, line in enumerate(text.split("\n"), 1):
        if FENCE_RE.match(line):
            fenced = not fenced
        h = None if fenced else HEAD_RE.match(line)
        if h:
            section = h.group(2)
            rows.append(None)                     # a heading ends the run a continuation line may join
            continue
        if not line.strip():
            continue
        b = None if fenced else BULLET.match(line)
        if b:
            body = b.group(1).strip()
            st = STAMP.match(body)
            rows.append([n, st.group(1) if st else None, section, True, body])
        elif rows and rows[-1] is not None:
            rows[-1][4] += "\n" + line.rstrip()
        else:
            rows.append([n, None, section, False, line.strip()])
    return [tuple(r) for r in rows if r is not None]


def norm_name(s):
    """A rules-index key or a file name, reduced to what identifies the lesson: stripped, '#n' and any
    path removed, case folded."""
    s = s.strip().split("#", 1)[0].strip()
    return s.replace("\\", "/").rsplit("/", 1)[-1].casefold()


def read_rules(text):
    """-> (rows, rejected). rows: the well-formed lines (7 tab-separated fields, '#' lines skipped), as
    rules_card.py reads them. rejected: [(line_no, first field)] for every other non-blank line; a lesson
    named by a rejected line is EXCLUDED by scan() (fail closed), never treated as having no row."""
    out, rejected = [], []
    for ln, line in enumerate(text.split("\n"), 1):
        line = line.rstrip("\r")
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        if len(f) != 7:
            rejected.append((ln, f[0]))
            continue
        key = f[0]
        if "#" in key:
            base, _, num = key.partition("#")
            if not (num.isdigit() and int(num) >= 2):
                rejected.append((ln, f[0]))
                continue
            n = int(num)
        else:
            base, n = key, 1
        out.append(dict(key=key, base=base, n=n, status=f[1].strip(),
                        seats=[x.strip() for x in f[2].split(",") if x.strip()],
                        family=f[3].strip(), triggers=[t.strip() for t in f[4].split(",") if t.strip()],
                        enforced_by=f[5].strip(), rule=f[6].strip()))
    return out, rejected


def compute_weights(rules, ledger_lines):
    """Mirror of rules_card.compute_weights, over THIS seat's indexed ledger rows only.
    ledger_lines: [(date, whole row line)]. -> {base: (weight, last_cited)}"""
    files = []
    for r in rules:
        if r["base"] not in files:
            files.append(r["base"])
    stems = {f: (f[:-3] if f.endswith(".md") else f) for f in files}
    pats = {f: re.compile(r"(?<![\w-])" + re.escape(stems[f]) + r"(?![\w-])") for f in files}
    own = dict((f, 0) for f in files)
    last = dict((f, "") for f in files)
    for date, line in ledger_lines:
        cited = set(f for f in files if stems[f] in line and pats[f].search(line))
        for am in ABBR_RE.finditer(line):
            d, rest = am.group(1), am.group(2)
            if len(rest) < MIN_ABBR:
                continue
            hit = [f for f in files if stems[f].startswith(d + "_" + rest)]
            if len(hit) == 1:
                cited.add(hit[0])
        for f in cited:
            own[f] += 1
            if date and date > last[f]:
                last[f] = date
    target = {}
    for r in rules:
        if r["n"] == 1 and r["status"] == "superseded" and r["rule"].startswith("-> "):
            t = r["rule"][3:].split(":", 1)[0].strip()
            if t in own and t != r["base"]:
                target[r["base"]] = t

    def final(f):
        seen = set([f])
        while f in target:
            nxt = target[f]
            if nxt in seen:
                return None
            seen.add(nxt)
            f = nxt
        return f
    w = dict(own)
    lastm = dict(last)
    for f in files:
        if f in target:
            t = final(f)
            if t is not None and t != f:
                w[t] += own[f]
                w[f] -= own[f]
                if last[f] > lastm[t]:
                    lastm[t] = last[f]
    return dict((f, (w[f], lastm[f] or None)) for f in files)


# ---------------------------------------------------------------- scan (shared by rebuild and check)

def scan(root, sc, want_text):
    """Walk the allow-list. -> dict(files={rel: dict(kind, sha, bytes, text)}, skipped=[(rel, reason)],
    unreadable=[rel], untagged=[rel], rejected_rows=n). Every decision about a LESSON fails closed: a head
    that is ambiguous about its tier, a damaged rules-index row naming it, or no usable rules index at all
    keeps it OUT. rebuild and check both go through here, so they agree."""
    listed, skipped = enumerate_files(root, sc)
    files, unreadable, untagged = {}, [], []
    loaded = {}

    def load(rel):
        if rel not in loaded:
            try:
                loaded[rel] = read_file(os.path.join(root, rel))
            except OSError as e:
                loaded[rel] = None
                unreadable.append(rel)
                skipped.append((rel, "unreadable: %s" % type(e).__name__))
        return loaded[rel]

    # the rules index decides lessons: normalised lesson name -> True when a row is scoped 'all' or this seat
    seat_rows, bad_names, good, rejected = {}, {}, 0, 0
    for rel in sorted(listed):
        if listed[rel] != "rules_index":
            continue
        got = load(rel)
        if got is None:
            continue
        rows, rej = read_rules(got[1])
        good += len(rows)
        rejected += len(rej)
        for r in rows:
            mine = "all" in r["seats"] or sc["seat"] in r["seats"]
            k = norm_name(r["key"])
            seat_rows[k] = seat_rows.get(k, False) or mine
        for ln, first in rej:
            bad_names.setdefault(norm_name(first), ln)
    if any(k == "lesson" for k, _ in sc["allow"]) and good == 0:
        die("REFUSED: lessons are on the allow-list but no readable rules index with at least one well-formed "
            "row was found under %s. The rules index decides which lessons belong to this seat; without it every "
            "other seat's lesson would be indexed. Nothing was read into or changed in the index." % root, 2)
    for rel in sorted(listed):
        kind = listed[rel]
        got = load(rel)
        if got is None:
            continue
        raw, text = got
        if kind == "lesson":
            fm, _, _, faults = parse_frontmatter(text)
            if faults:
                skipped.append((rel, "tier cannot be read safely: " + "; ".join(faults)))
                continue
            ok, why = tier_verdict(fm.get("tier"), sc)
            if not ok:
                skipped.append((rel, why))
                continue
            k = norm_name(os.path.basename(rel))
            if k in bad_names:
                skipped.append((rel, "a damaged rules-index row names it (rules index line %d)" % bad_names[k]))
                continue
            if seat_rows.get(k) is False:
                skipped.append((rel, "every rules-index row for it names only other seats"))
                continue
            if not (fm.get("tier") or "").strip():
                untagged.append(rel)
        files[rel] = dict(kind=kind, sha=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                          text=text if want_text else None)
    return dict(files=files, skipped=skipped, unreadable=unreadable, untagged=untagged, rejected_rows=rejected)


def self_hashes(sc):
    def h(p):
        with open(p, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    return h(os.path.abspath(__file__)), h(sc["path"])


# ---------------------------------------------------------------- psql

def psql_cmd(db, variables=None, tuples=False):
    cmd = [os.path.join(env("BRAINDB_PGBIN_EFF"), "psql"), "-X", "-q", "-v", "ON_ERROR_STOP=1",
           "-h", env("BRAINDB_SOCKDIR_EFF"), "-p", env("BRAINDB_PORT_EFF"), "-d", db]
    for k, v in (variables or {}).items():
        cmd += ["-v", "%s=%s" % (k, v)]
    if tuples:
        cmd += ["-A", "-t", "-F", US, "-R", RS]
    return cmd


def query(sql, db=DB, variables=None):
    """Run SQL read from stdin (so :'var' is interpolated). -> (rc, [row fields])"""
    r = subprocess.run(psql_cmd(db, variables, tuples=True), input=sql.encode("utf-8"), stdout=subprocess.PIPE)
    out = r.stdout.decode("utf-8", errors="replace")
    if out.endswith("\n"):
        out = out[:-1]
    rows = [rec.split(US) for rec in out.split(RS)] if out else []
    return r.returncode, rows


def server_up():
    rc, rows = query("select 1", db="postgres")
    return rc == 0 and rows == [["1"]]


def need_server():
    """The server must answer AND must be the one this command is addressed to: a socket directory alone
    does not identify a cluster (ANSWER-3 F2). rc 3 = not answering, rc 4 = another cluster answers."""
    if not server_up():
        die("the index server is not answering on %s (run: braindb.sh start)" % env("BRAINDB_SOCKDIR_EFF"), 3)
    want = env("BRAINDB_PGDATA_EFF")
    rc, rows = query("show data_directory", db="postgres")
    got = rows[0][0] if rc == 0 and rows and rows[0] else ""
    if not got or os.path.realpath(got) != os.path.realpath(want):
        die("REFUSED: the server answering on socket directory %s serves data directory '%s', but this command "
            "is addressed to '%s'. Nothing was read or changed. Another cluster is using this socket directory: "
            "stop it with its own braindb.sh, or give this one its own BRAINDB_SOCKDIR."
            % (env("BRAINDB_SOCKDIR_EFF"), got or "(unknown)", want), 4)


def index_present():
    rc, rows = query("select 1 from pg_database where datname = 'braindb'", db="postgres")
    if rc != 0 or not rows:
        return False
    rc, rows = query("select to_regclass('brain.files') is not null")
    if rc != 0 or rows != [["t"]]:
        return False
    rc, rows = query("select count(*) from brain.files")
    return rc == 0 and bool(rows) and rows[0][0] != "0"


def ensure_index(root, sc, seat):
    """search and at build the index themselves when there is none (never when it is merely stale: that is check's job)."""
    if index_present():
        return
    fd = take_lock()                                 # another command may be building it right now: wait, then look again
    try:
        if index_present():
            return
        print("braindb: no index yet (never built, or emptied by an unclean stop): building it now", file=sys.stderr)
        import contextlib
        with contextlib.redirect_stdout(sys.stderr):
            rc = cmd_rebuild(None, root, sc, seat, lock_held=True)
        if rc != 0:
            die("could not build the index", 1)
    finally:
        os.close(fd)


def cp(v):
    """One COPY text-format field."""
    if v is None:
        return "\\N"
    if v is True:
        return "t"
    if v is False:
        return "f"
    return str(v).replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")


def pg_array(items):
    return "{" + ",".join('"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"' for x in items) + "}"


SCHEMA = r"""
BEGIN;
DROP SCHEMA IF EXISTS brain CASCADE;
CREATE SCHEMA brain;
CREATE UNLOGGED TABLE brain.meta (k text PRIMARY KEY, v text);
CREATE UNLOGGED TABLE brain.files (path text PRIMARY KEY, kind text NOT NULL, sha256 text NOT NULL, bytes bigint NOT NULL);
CREATE UNLOGGED TABLE brain.lessons (path text PRIMARY KEY, file text NOT NULL UNIQUE, date date, type text,
    status text, tier text, heading text, body text);
CREATE UNLOGGED TABLE brain.rules (key text PRIMARY KEY, file text NOT NULL, n int NOT NULL, status text,
    seats text[], family text, triggers text[], enforced_by text, rule text, weight int NOT NULL, last_cited date);
CREATE UNLOGGED TABLE brain.ledger_rows (path text NOT NULL, line int NOT NULL, date date, headline text,
    rule_sentence text, body text, PRIMARY KEY (path, line));
CREATE UNLOGGED TABLE brain.daily_rows (path text NOT NULL, line int NOT NULL, date date, stamp text,
    section text, is_bullet boolean, body text, PRIMARY KEY (path, line));
CREATE UNLOGGED TABLE brain.chunks (id bigint PRIMARY KEY, path text NOT NULL, kind text NOT NULL,
    unit text NOT NULL, line int, date date, stamp text, status text, title text, slug text, heading text, extra text, body text,
    tsv tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(title, '') || ' ' || coalesce(slug, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(heading, '') || ' ' || coalesce(extra, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(body, '')), 'D')) STORED);
CREATE VIEW brain.lesson_rules AS
    SELECT l.path, l.file, l.date, l.type, l.status, l.tier, l.heading, r.key, r.n, r.status AS rule_status,
           r.seats, r.family, r.triggers, r.enforced_by, r.rule, r.weight, r.last_cited
    FROM brain.lessons l LEFT JOIN brain.rules r ON r.file = l.file;
"""

FINISH = r"""
CREATE INDEX chunks_tsv ON brain.chunks USING gin (tsv);
CREATE INDEX chunks_kind ON brain.chunks (kind);
CREATE INDEX rules_triggers ON brain.rules USING gin (triggers);
CREATE UNLOGGED TABLE brain.lexeme_df AS SELECT word, ndoc FROM ts_stat('SELECT tsv FROM brain.chunks');
ALTER TABLE brain.lexeme_df ADD PRIMARY KEY (word);
COMMIT;
ANALYZE brain.chunks;
ANALYZE brain.lexeme_df;
"""


def copy_block(table, cols, rows):
    yield "COPY brain.%s (%s) FROM STDIN;\n" % (table, ", ".join(cols))
    for r in rows:
        yield "\t".join(cp(v) for v in r) + "\n"
    yield "\\.\n"


# ---------------------------------------------------------------- rebuild

def build_rows(root, sc, seat):
    sc_res = scan(root, sc, want_text=True)
    files = sc_res["files"]
    T = dict(files=[], lessons=[], rules=[], ledger=[], daily=[], chunks=[])
    notes = []                                     # human lines for the rebuild report
    truncated = []                                 # (path, line, what, original length)
    for rel, f in files.items():
        T["files"].append((rel, f["kind"], f["sha"], f["bytes"]))

    def cap(v, limit, rel, line, what):
        if v is None or len(v) <= limit:
            return v
        truncated.append((rel, line, what, len(v)))
        return v[:limit] + " [TRUNCATED by brain-db: this %s was %d characters]" % (what, len(v))

    def add(cid, rel, kind, unit, line, date, stamp, status, title, slug, heading, extra, body):
        T["chunks"].append((cid, rel, kind, unit, line, date, stamp, status,
                            cap(title, MAX_HEAD_CHARS, rel, line, "title"), slug,
                            cap(heading, MAX_HEAD_CHARS, rel, line, "heading"),
                            cap(extra, MAX_HEAD_CHARS, rel, line, "rule line"),
                            cap(body, MAX_ROW_CHARS, rel, line, "row")))

    # rules index first: lessons carry their rule lines into the search text
    rules = []
    for rel, f in files.items():
        if f["kind"] == "rules_index":
            rules += read_rules(f["text"])[0]
    lesson_names = dict((os.path.basename(rel), rel) for rel, f in files.items() if f["kind"] == "lesson")
    kept_rules = [r for r in rules if r["base"] in lesson_names]
    seen, uniq = set(), []
    for r in kept_rules:
        if r["key"] not in seen:
            seen.add(r["key"])
            uniq.append(r)
    kept_rules = uniq
    if rules:
        notes.append("rules index: %d well-formed rows, %d joined to an indexed lesson, %d dropped "
                     "(their lesson is excluded or missing)" % (len(rules), len(kept_rules), len(rules) - len(kept_rules)))
    if sc_res["rejected_rows"]:
        notes.append("rules index: %d DAMAGED row(s) ignored (wrong field count or a bad '#n'); a lesson named by "
                     "one is excluded and listed below" % sc_res["rejected_rows"])

    ledger_lines = []
    cid = 0
    dropped_sections = 0
    for rel in sorted(files):
        f = files[rel]
        kind, text, name = f["kind"], f["text"], os.path.basename(rel)
        if kind == "rules_index":
            continue
        if kind == "ledger":
            for (n, date, headline, rule, body) in parse_ledger(text):
                T["ledger"].append((rel, n, date, headline, rule, body))
                ledger_lines.append((date or "", body))
                cid += 1
                add(cid, rel, kind, "%s:%d" % (rel, n), n, date, None, None, headline, None, None, rule, body)
            continue
        if kind == "daily":
            date = iso_date(name)
            for (n, stamp, section, is_bullet, body) in parse_daily(text):
                T["daily"].append((rel, n, date, stamp, section, is_bullet, body))
                cid += 1
                add(cid, rel, kind, "%s:%d" % (rel, n), n, date, stamp, None, None, None, section, None, body)
            continue
        fm, body, first, _faults = parse_frontmatter(text)
        lines = body.split("\n")
        status = None
        extra = None
        if kind == "rules":
            title, rchunks = chunk_rules(lines, first, name)
            for (n, head, lead, ctext) in rchunks:
                cid += 1
                add(cid, rel, kind, "%s:%d" % (rel, n), n, None, None, None, lead, None,
                    "%s > %s" % (rel, head), None, ctext)
            continue
        if kind == "lesson":
            lines, dropped = drop_foreign_sections(lines, sc)
            dropped_sections += len(dropped)
            mine = [r for r in kept_rules if r["base"] == name]
            plain = next((r for r in mine if r["n"] == 1), None)
            status = plain["status"] if plain else ((fm.get("status") or "").split() or [None])[0]
            extra = " ".join(r["rule"] for r in mine) or None
        title, chunks = chunk(lines, first, name)
        date = iso_date(fm.get("date")) or iso_date(name)
        if kind == "lesson":
            T["lessons"].append((rel, name, date, fm.get("type"), fm.get("status"), fm.get("tier"),
                                 title[:MAX_HEAD_CHARS], "\n".join(lines).strip()))
        for (n, head, ctext) in chunks:
            cid += 1
            add(cid, rel, kind, rel, n, date, None, status, title, slug_words(name),
                None if head == title else head, extra, ctext)
    weights = compute_weights(kept_rules, ledger_lines)
    for r in kept_rules:
        w, last = weights.get(r["base"], (0, None))
        T["rules"].append((r["key"], r["base"], r["n"], r["status"], pg_array(r["seats"]), r["family"],
                           pg_array(r["triggers"]), r["enforced_by"], r["rule"], w, iso_date(last)))
    if dropped_sections:
        notes.append("lesson sections dropped by their project-tier marker: %d" % dropped_sections)
    return T, sc_res, notes, truncated


def reason_group(why):
    """One heading per kind of exclusion, for the rebuild report."""
    if why.startswith("tier '"):
        return "tier names a client this seat may not index"
    if why.startswith("project tier"):
        return "project tier whose client is not one of this seat's"
    if why.startswith("unknown tier"):
        return "unknown tier value"
    return re.sub(r"\s*\((rules index line|link count) \d+\)", "", why)


def take_lock():
    """One rebuild at a time per cluster (two first builds would both try to create the database). The lock
    is flock() on the cluster's lock file; the kernel drops it when this process ends."""
    import fcntl
    fd = os.open(env("BRAINDB_LOCK_EFF"), os.O_RDWR | os.O_CREAT, 0o600)
    fcntl.flock(fd, fcntl.LOCK_EX)
    return fd


def cmd_rebuild(a, root, sc, seat, lock_held=False):
    need_server()
    t0 = time.time()
    T, sc_res, notes, truncated = build_rows(root, sc, seat)
    t_parse = time.time() - t0
    lock_fd = None if lock_held else take_lock()
    rc, rows = query("select 1 from pg_database where datname = 'braindb'", db="postgres")
    if rc != 0:
        die("cannot query the server", 1)
    if not rows:
        rc, _ = query("CREATE DATABASE braindb ENCODING 'UTF8' TEMPLATE template0", db="postgres")
        if rc != 0:
            die("cannot create database braindb", 1)
    idx_sha, scope_sha = self_hashes(sc)
    kinds = {}
    for (_, _, kind, *_rest) in T["chunks"]:
        kinds[kind] = kinds.get(kind, 0) + 1
    fkinds = {}
    for (_, kind, _, _) in T["files"]:
        fkinds[kind] = fkinds.get(kind, 0) + 1
    meta = [("seat", seat), ("root", root), ("built_at", datetime.datetime.now().astimezone().isoformat(timespec="seconds")),
            ("indexer_sha256", idx_sha), ("scope_sha256", scope_sha),
            ("counts", json.dumps(dict(files=fkinds, search_rows=kinds, rules=len(T["rules"])))),
            ("faults", json.dumps(dict(unreadable=len(sc_res["unreadable"]), truncated=len(truncated))))]
    p = subprocess.Popen(psql_cmd(DB), stdin=subprocess.PIPE)
    try:
        w = lambda s: p.stdin.write(s.encode("utf-8"))
        w(SCHEMA)
        for blk in (
            copy_block("meta", ("k", "v"), meta),
            copy_block("files", ("path", "kind", "sha256", "bytes"), T["files"]),
            copy_block("lessons", ("path", "file", "date", "type", "status", "tier", "heading", "body"), T["lessons"]),
            copy_block("rules", ("key", "file", "n", "status", "seats", "family", "triggers", "enforced_by",
                                 "rule", "weight", "last_cited"), T["rules"]),
            copy_block("ledger_rows", ("path", "line", "date", "headline", "rule_sentence", "body"), T["ledger"]),
            copy_block("daily_rows", ("path", "line", "date", "stamp", "section", "is_bullet", "body"), T["daily"]),
            copy_block("chunks", ("id", "path", "kind", "unit", "line", "date", "stamp", "status", "title", "slug",
                                  "heading", "extra", "body"), T["chunks"]),
        ):
            for s in blk:
                w(s)
        w(FINISH)
        p.stdin.close()
    except (BrokenPipeError, OSError):
        try:
            p.stdin.close()
        except OSError:
            pass
    rc = p.wait()
    if rc != 0:
        die("REBUILD FAILED (psql rc %d). The transaction was rolled back; the previous index, if any, is unchanged." % rc, 1)
    dt = time.time() - t0
    print("rebuild: seat %s, tree %s" % (seat, root))
    print("  data directory: %s" % env("BRAINDB_PGDATA_EFF"))
    print("  %-14s %6s %8s" % ("kind", "files", "rows"))
    for k in KINDS:
        if k == "rules_index":
            print("  %-14s %6d %8d   (rule lines)" % (k, fkinds.get(k, 0), len(T["rules"])))
        elif fkinds.get(k, 0) or kinds.get(k, 0):
            print("  %-14s %6d %8d" % (k, fkinds.get(k, 0), kinds.get(k, 0)))
    print("  %-14s %6d %8d   (search rows)" % ("total", len(T["files"]), len(T["chunks"])))
    for n in notes:
        print("  " + n)
    reasons = {}
    for rel, why in sc_res["skipped"]:
        reasons.setdefault(reason_group(why), []).append((rel, why))
    if reasons:
        print("  matched an allow line but NOT indexed: %d" % len(sc_res["skipped"]))
        for key in sorted(reasons):
            items = reasons[key]
            # anything that fails closed, or is a fault, is listed in full by name; routine exclusions are sampled
            full = key.startswith(("tier cannot", "a damaged", "unreadable", "hard link", "unknown tier", "project tier", "tier names"))
            show = items if full else items[:4]
            print("    %3d  %s%s" % (len(items), key.strip(), "" if full else "  (%s%s)" % (
                ", ".join(os.path.basename(x.rstrip("/")) or x for x, _ in show), ", ..." if len(items) > 4 else "")))
            if full:
                for rel, why in show:
                    print("           %s  [%s]" % (rel, why))
    if sc_res["untagged"]:
        print("  UNTAGGED lessons indexed (no tier in the frontmatter; treated as W, as boot_digest.py does): %d" % len(sc_res["untagged"]))
        for rel in sc_res["untagged"]:
            print("           %s" % rel)
    if truncated:
        print("  rows TRUNCATED at their size limit: %d" % len(truncated))
        for rel, line, what, n in truncated[:20]:
            print("           %s:%s  %s of %d characters" % (rel, line, what, n))
        if len(truncated) > 20:
            print("           (+%d more)" % (len(truncated) - 20))
    print("  time: %.2f s (read and parse %.2f s, load and index %.2f s)" % (dt, t_parse, dt - t_parse))
    nu, nt = len(sc_res["unreadable"]), len(truncated)
    if nu or nt:
        print("rebuild: DONE WITH FAULTS: %d unreadable file(s) skipped, %d row(s) truncated; they are listed above" % (nu, nt))
    else:
        print("rebuild: done; no file was unreadable and no row was truncated")
    if lock_fd is not None:
        os.close(lock_fd)
    return 0


# ---------------------------------------------------------------- check

def cmd_check(a, root, sc, seat):
    need_server()
    where = "  data directory: %s" % env("BRAINDB_PGDATA_EFF")
    rc, rows = query("select 1 from pg_database where datname = 'braindb'", db="postgres")
    if rc != 0 or not rows:
        print("check: RED, no index database yet (run: braindb.sh rebuild)")
        print(where)
        return 1
    rc, rows = query("select to_regclass('brain.files') is not null and to_regclass('brain.meta') is not null")
    if rc != 0 or rows != [["t"]]:
        print("check: RED, the index schema is missing (run: braindb.sh rebuild)")
        print(where)
        return 1
    rc, rows = query("select path, sha256 from brain.files")
    if rc != 0:
        die("cannot read the index", 1)
    have = dict((r[0], r[1]) for r in rows)
    rc, mrows = query("select k, v from brain.meta")
    meta = dict((r[0], r[1]) for r in mrows) if rc == 0 else {}
    res = scan(root, sc, want_text=False)
    disk = dict((rel, f["sha"]) for rel, f in res["files"].items())
    diffs = []
    for rel in sorted(set(disk) | set(have)):
        if rel not in have:
            diffs.append("on disk, not in the index: " + rel)
        elif rel not in disk:
            diffs.append("in the index, gone from disk or now out of scope: " + rel)
        elif disk[rel] != have[rel]:
            diffs.append("changed since the last rebuild: " + rel)
    idx_sha, scope_sha = self_hashes(sc)
    stale = []
    if not have:
        stale.append("the index is empty (never built, or emptied by an unclean stop)")
    if meta.get("indexer_sha256") != idx_sha:
        stale.append("braindb_index.py has changed since the last rebuild")
    if meta.get("scope_sha256") != scope_sha:
        stale.append("the scope file has changed since the last rebuild")
    if meta.get("seat") not in (None, seat):
        stale.append("the index was built for seat %s, this is seat %s" % (meta.get("seat"), seat))
    try:
        last = json.loads(meta.get("faults") or "{}")
    except ValueError:
        last = {}
    faults = "  skipped for a fault: %d file(s) unreadable on disk now; at the last rebuild %s unreadable, %s row(s) truncated" % (
        len(res["unreadable"]), last.get("unreadable", "?"), last.get("truncated", "?"))
    if not diffs and not stale:
        print("check: GREEN, %d files on disk match the index (built %s)" % (len(disk), meta.get("built_at", "?")))
        print(where)
        print(faults)
        for rel in res["unreadable"][:20]:
            print("    unreadable: " + rel)
        return 0
    print("check: RED, %d path(s) differ%s (run: braindb.sh rebuild)"
          % (len(diffs), "; " + "; ".join(stale) if stale else ""))
    for d in diffs[:20]:
        print("  " + d)
    if len(diffs) > 20:
        print("  (+%d more)" % (len(diffs) - 20))
    print(where)
    print(faults)
    for rel in res["unreadable"][:20]:
        print("    unreadable: " + rel)
    return 1


# ---------------------------------------------------------------- search

SEARCH_SQL = r"""
WITH terms AS (
    SELECT lexeme FROM unnest(tsvector_to_array(to_tsvector('english', :'q'))) AS lexeme
), n AS (
    SELECT count(*)::float8 AS n FROM brain.chunks
), tw AS (
    SELECT t.lexeme, quote_literal(t.lexeme)::tsquery AS tq,
           ln(1 + (n.n - coalesce(d.ndoc, 0) + 0.5) / (coalesce(d.ndoc, 0) + 0.5)) AS idf
    FROM terms t CROSS JOIN n LEFT JOIN brain.lexeme_df d ON d.word = t.lexeme
), allq AS (
    SELECT string_agg(quote_literal(lexeme), ' | ')::tsquery AS oq, sum(idf) AS idfsum FROM tw
), keyw AS (
    -- the query's KEY WORDS: its rarest few terms. search reports which of them the first result holds and
    -- which it lacks. No score threshold is applied: on 34 judged questions none separated right from wrong
    -- (evidence/threshold_study_round3.txt), so the tool states the fact and leaves the judgement to the reader.
    SELECT lexeme, tq, idf FROM tw ORDER BY idf DESC, lexeme LIMIT :topk
), cand AS (
    SELECT c.id, c.unit, c.tsv, c.status, c.kind FROM brain.chunks c, allq
    WHERE c.tsv @@ allq.oq AND (:'kind' = '' OR c.kind = :'kind')
), scored AS (
    SELECT c.id, c.unit, c.status, c.kind,
           sum(tw.idf * ts_rank('{0.1, 0.2, 0.4, 1.0}', c.tsv, tw.tq, 1)) AS s,
           sum(CASE WHEN c.tsv @@ tw.tq THEN tw.idf ELSE 0 END) AS matched
    FROM cand c CROSS JOIN tw GROUP BY c.id, c.unit, c.status, c.kind
), ranked AS (
    -- ORDER: rarity-weighted mean rank over ALL the query's terms, times the square of the share matched
    SELECT s.id, s.unit, s.kind,
           (s.s / nullif(a.idfsum, 0)) * power(s.matched / nullif(a.idfsum, 0), 2)
               * (CASE WHEN s.status IN ('dead', 'superseded') THEN 0.5 ELSE 1 END) AS score
    FROM scored s CROSS JOIN allq a
), best AS (
    SELECT DISTINCT ON (unit) id, unit, kind, score FROM ranked ORDER BY unit, score DESC, id
), grouped AS (
    SELECT id, score, CASE WHEN kind IN ('ledger', 'daily') THEN 1 ELSE 0 END AS grp,
           row_number() OVER (PARTITION BY (CASE WHEN kind IN ('ledger', 'daily') THEN 1 ELSE 0 END)
                              ORDER BY score DESC, id) AS rn
    FROM best
), top AS (
    SELECT id, score, grp FROM grouped WHERE rn <= :lim
)
SELECT round(t.score::numeric, 4), c.kind, c.path, coalesce(c.line::text, ''), coalesce(c.date::text, ''),
       coalesce(c.stamp, ''), coalesce(c.status, ''), coalesce(c.title, ''), coalesce(c.heading, ''),
       coalesce((SELECT string_agg(r.rule, ' / ' ORDER BY r.n) FROM brain.rules r
                 WHERE c.kind = 'lesson' AND r.file = regexp_replace(c.path, '^.*/', '')), ''),
       coalesce((SELECT max(r.weight)::text FROM brain.rules r
                 WHERE c.kind = 'lesson' AND r.file = regexp_replace(c.path, '^.*/', '')), ''),
       ts_headline('english', c.body, a.oq, 'MaxWords=34, MinWords=14, MaxFragments=2, StartSel=[[, StopSel=]], FragmentDelimiter=" ... "'),
       t.grp, t.id,
       coalesce((SELECT string_agg(k.lexeme, ' ' ORDER BY k.idf DESC, k.lexeme) FILTER (WHERE c.tsv @@ k.tq) FROM keyw k), ''),
       coalesce((SELECT string_agg(k.lexeme, ' ' ORDER BY k.idf DESC, k.lexeme) FILTER (WHERE NOT c.tsv @@ k.tq) FROM keyw k), '')
FROM top t JOIN brain.chunks c ON c.id = t.id CROSS JOIN allq a
ORDER BY t.score DESC, c.id;
"""

RECORDS_SHOWN = 2      # in the default order: how many incident rows follow the knowledge results
TOPK_DEFAULT = "4"     # how many of the question's rarest words count as its key words


def one_line(s, width):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= width else s[:width - 1] + "\u2026"


def holds_all(r):
    """True when the row holds every key word of the question (r[14] = held, r[15] = lacking)."""
    return bool(r[14]) and not r[15]


def arrange(rows, limit, mode):
    """rows: best first; kind r[1], group r[12]. -> (main list, records tail)
    mode 'all' or 'kind': one list by score. mode 'default': knowledge first, then a short tail of incident
    rows. A rules-file row goes ahead of the lessons only when it holds EVERY key word of the question;
    otherwise it competes on score like any other row (so the rules file cannot become a confident wrong
    neighbour on the strength of one shared word)."""
    if mode != "default":
        return rows[:limit], []
    know = [r for r in rows if r[12] == "0"]
    first = [r for r in know if r[1] == "rules" and holds_all(r)]
    rest = [r for r in know if not (r[1] == "rules" and holds_all(r))]
    return (first + rest)[:limit], [r for r in rows if r[12] == "1"][:RECORDS_SHOWN]


def print_result(i, r):
    score, k, path, line, date, stamp, status, title, heading, rule, weight, snip = r[:12]
    tags = [k]
    if status:
        tags.append(status)
    if weight and weight != "0":
        tags.append("×" + weight)
    if k in ("ledger", "daily"):
        tags.append((date + " " + stamp).strip())
    print("%2d. %s  [%s]  %s%s" % (i, score, ", ".join(t for t in tags if t), path, ":" + line if line else ""))
    head = title if not heading else ("%s > %s" % (title, heading) if title else heading)
    if head:
        print("    heading: " + one_line(head, 200))
    if rule:
        print("    rule:    " + one_line(rule, 300))
    print("    snippet: " + one_line(snip, 320))


def cmd_search(a, root, sc, seat):
    topk = os.environ.get("BRAINDB_TOPK", TOPK_DEFAULT)
    if topk not in ("1", "2", "3", "4", "5", "6"):
        die("BRAINDB_TOPK must be 1 to 6")
    need_server()
    ensure_index(root, sc, seat)
    words = " ".join(a.words).strip()
    if not words:
        die("search needs words")
    kind = a.kind or ""
    if kind and kind not in SEARCH_KINDS:
        die("unknown --kind %r (kinds: %s)" % (kind, " ".join(SEARCH_KINDS)))
    if kind and a.all:
        die("--kind and --all do not go together")
    if a.limit < 1 or a.limit > 200:
        die("--limit must be 1 to 200")
    mode = "kind" if kind else ("all" if a.all else "default")
    t0 = time.time()
    rc, rows = query(SEARCH_SQL, variables=dict(q=words, kind=kind, lim=str(a.limit), topk=topk))
    ms = (time.time() - t0) * 1000
    if rc != 0:
        die("search failed (is the index built? run: braindb.sh check)", 1)
    rows = [r for r in rows if len(r) == 16]
    main, tail = arrange(rows, a.limit, mode)
    print('search: "%s"  %s' % (words, {"kind": "kind=" + kind, "all": "all kinds, one order",
                                         "default": "rules and lessons first"}[mode]))
    for i, r in enumerate(main, 1):
        print_result(i, r)
    if tail:
        print("  also, incident rows from the ledger and daily notes (what happened, not the rule):")
        for i, r in enumerate(tail, len(main) + 1):
            print_result(i, r)
    n = len(main) + len(tail)
    if not main and not tail:
        print("NO MATCH: none of these words is in the index. If you know the moment, try: braindb.sh at <trigger>")
        print("(0 results, %.0f ms)" % ms)
        return 0
    if not main:
        print("NOTE: only incident rows matched; no rule or lesson did. If you know the moment, try: braindb.sh at <trigger>")
    # a neutral statement of fact about the first result; no threshold, no verdict
    f = main[0] if main else tail[0]
    held, lack = f[14].split(), f[15].split()
    if not lack:
        fact = "it holds all %d of the question's rarest words [%s]" % (len(held), " ".join(held))
    else:
        fact = "of the question's %d rarest words it holds %d [%s] and lacks %d [%s]" % (
            len(held) + len(lack), len(held), " ".join(held), len(lack), " ".join(lack))
    print("(%d result%s, %.0f ms; first result: score %s; %s)" % (n, "" if n == 1 else "s", ms, f[0], fact))
    return 0


# ---------------------------------------------------------------- at <trigger>

AT_SQL = r"""
SELECT weight, coalesce(enforced_by, '-'), rule, file, n FROM brain.rules
WHERE status = 'live' AND :'t' = ANY (triggers) AND ('all' = ANY (seats) OR :'seat' = ANY (seats))
ORDER BY weight DESC, file, n;
"""


def cmd_at(a, root, sc, seat):
    need_server()
    ensure_index(root, sc, seat)
    if not re.fullmatch(r"[a-z][a-z-]*", a.trigger):
        die("a trigger is one lower-case word from the rules-index vocabulary")
    rc, rows = query(AT_SQL, variables=dict(t=a.trigger, seat=seat))
    if rc != 0:
        die("lookup failed (is the index built? run: braindb.sh check)", 1)
    rows = [r for r in rows if len(r) == 5]
    print("Rules for: %s (%d)  [weights counted from this seat's indexed ledgers only]" % (a.trigger, len(rows)))
    shown = rows[:a.top] if a.top else rows
    for w, enf, rule, file_, n in shown:
        label = "[\u00d7%s]" % w if w != "0" else "[new]"
        print("\u2022 %s %s%s  (%s)" % (label, "[enforced] " if enf not in ("-", "") else "", rule,
                                         file_ if n == "1" else "%s, rule %s" % (file_, n)))
    if len(rows) > len(shown):
        print("(+%d more: braindb.sh at %s)" % (len(rows) - len(shown), a.trigger))
    return 0


# ---------------------------------------------------------------- info (used by `braindb.sh status`)

def cmd_info(a, root, sc, seat):
    if not server_up():
        return 3
    need_server()                                   # refuses (rc 4) when another cluster answers on this socket
    print("  the server answering is this data directory's: %s" % env("BRAINDB_PGDATA_EFF"))
    rc, rows = query("select 1 from pg_database where datname = 'braindb'", db="postgres")
    if rc != 0 or not rows:
        print("  index: no database yet (run: braindb.sh rebuild)")
        return 0
    rc, rows = query("select pg_database_size('braindb'), pg_size_pretty(pg_database_size('braindb'))")
    if rc == 0 and rows:
        print("  database size: %s (%s bytes)" % (rows[0][1], rows[0][0]))
    rc, rows = query("select to_regclass('brain.meta') is not null")
    if rc != 0 or rows != [["t"]]:
        print("  index: schema missing (run: braindb.sh rebuild)")
        return 0
    rc, rows = query("select k, v from brain.meta where k in ('built_at', 'seat', 'counts', 'faults') order by k")
    for r in rows:
        if len(r) == 2:
            print("  %s: %s" % (r[0], r[1]))
    return 0


def main():
    ap = argparse.ArgumentParser(prog="braindb_index.py", description="indexer behind braindb.sh")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("rebuild")
    sub.add_parser("check")
    sub.add_parser("info")
    s = sub.add_parser("search")
    s.add_argument("words", nargs="+")
    s.add_argument("--kind")
    s.add_argument("--limit", type=int, default=5)
    s.add_argument("--all", action="store_true", help="all kinds in one order by score (the pre-round-2 behaviour)")
    t = sub.add_parser("at")
    t.add_argument("trigger")
    t.add_argument("--top", type=int, default=0)
    a = ap.parse_args()
    if not a.cmd:
        ap.print_usage(sys.stderr)
        return 2
    seat = env("BRAINDB_SEAT")
    if seat not in SEATS:
        die("unknown seat %r" % seat)
    root = env("BRAINDB_ROOT_EFF")
    if not os.path.isdir(root):
        die("tree root does not exist: " + root)
    sc = load_scope(env("BRAINDB_SCOPE_EFF"), seat)
    return dict(rebuild=cmd_rebuild, check=cmd_check, search=cmd_search, at=cmd_at, info=cmd_info)[a.cmd](a, root, sc, seat)


if __name__ == "__main__":
    sys.exit(main())
