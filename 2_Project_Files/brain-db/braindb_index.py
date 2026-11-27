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
import os, sys, re, json, hashlib, fnmatch, subprocess, time, datetime, argparse, stat, unicodedata, threading

DB = "braindb"
KINDS = ("rules", "lesson", "rules_index", "ledger", "daily", "pickup", "skill", "identity", "people", "architecture")
SEARCH_KINDS = ("rules", "lesson", "ledger", "daily", "pickup", "skill", "identity", "people", "architecture")
MAX_ROW_CHARS = 80000        # a search row's text is cut here (Postgres refuses a tsvector over 1 MB)
MAX_HEAD_CHARS = 20000       # titles, headings and rule lines
SEATS = ("wednesday", "tuesday", "friday")
ALL_SEATS = "all"            # the rules index's all-seats word (spec: "`all`, or a comma list of `wednesday`, `tuesday`, `friday`")
ROW_STATUS = ("live", "dead", "superseded")

# ---- ROUND 4: what an allow line may ask for is a CLOSED TABLE IN THIS FILE, per seat. A scope file can
# narrow it and can never widen it: a line that asks for anything else is REFUSED when the scope is loaded,
# before any cluster is created or started. (dir, exact file names or None = any name the pattern gives)
LEARN = "0_Brain/learnings"
SEAT_DAILY = {"wednesday": "0_Brain/daily", "tuesday": "0_Brain/daily_tuesday", "friday": "0_Brain/daily_friday"}   # as tools/seat_note.sh
SEAT_LEDGERS = {"wednesday": ("_ledger.md", "_ledger_archive.md"),
                "tuesday": ("_ledger_laptop_datasec.md", "_ledger_laptop_datasec_archive.md"),
                "friday": ("_ledger_friday.md", "_ledger_friday_archive.md")}
SEAT_PICKUP = {"wednesday": ("NEXT-PICKUP.md", "WEEK-INSTRUCTION.md"),
               "tuesday": ("NEXT-PICKUP-TUESDAY.md", "WEEK-INSTRUCTION-TUESDAY.md"),
               "friday": ("NEXT-PICKUP-FRIDAY.md", "WEEK-INSTRUCTION-FRIDAY.md")}
ROOT_RULES = ("CLAUDE.md", "0_Brain/CLAUDE.md")
SHARED_DIRS = {"lesson": LEARN, "skill": "0_Brain/skills", "identity": "0_Brain/identity", "people": "0_Brain/people",
               "architecture": "1_Project_Definition/Architecture"}
BUILTIN_DENY_PATH = ("(conflict_on_", ".pre-")     # sync leftovers and backups, whatever a scope file says


def allowed_place(seat, kind, daily_rel):
    """-> (directory, tuple of exact names or None). The one place a kind may be indexed from, for this seat."""
    if kind == "ledger":
        return LEARN, SEAT_LEDGERS[seat]
    if kind == "daily":
        return daily_rel, None
    if kind == "pickup":
        return "0_Brain/tasks", SEAT_PICKUP[seat]
    if kind == "rules_index":
        return LEARN, ("_rules_index.tsv",)
    return SHARED_DIRS[kind], None


LESSON_NAME = re.compile(r"\d{4}-\d{2}-\d{2}[_-].+\.md", re.S)   # used with fullmatch: a name may hold any character
DAILY_NAME = re.compile(r"\d{4}-\d{2}-\d{2}\.md")
STRIP_BYTES = {0x00: None, 0x1e: None, 0x1f: None}                 # NUL, and the two bytes psql output is split on
ITEM_RE = re.compile(r"^(\d+[a-z]?(?:-[ivx]+)?)\.\s+(.*)$")
# Refused in code even when a scope file names them (matched on whole path segments, lower case).
HARD_DENY_PREFIX = ("4_credentials", "3_access_keys", "0_brain/dashboard", "0_brain/reference")
HARD_DENY_SEGMENT = ("4_credentials", "3_access_keys")

HEAD_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
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

def load_scope(path, seat, daily_rel=None):
    """Read and VALIDATE the scope file. Everything here runs before a cluster is created or started
    (braindb.sh calls `validate` first), and every refusal is rc 2."""
    daily_rel = daily_rel or SEAT_DAILY[seat]
    if daily_rel != SEAT_DAILY[seat]:
        die("REFUSED: tools/seat_note.sh says seat %r keeps its daily notes in %r, this tool's table says %r; "
            "the two must agree before any daily note is indexed" % (seat, daily_rel, SEAT_DAILY[seat]))
    if not os.path.isfile(path):
        die("no scope file for seat '%s' at %s. A seat is indexed only through its own reviewed "
            "allow-list; see proposed/INSTRUCTIONS-for-other-seats.md" % (seat, path))
    sc = dict(seat=None, own=[], allow=[], deny_path=[], deny_seat_word=[], path=path, daily_rel=daily_rel)
    pending = []
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
                die("%s: REFUSED, 'deny_clients' is no longer a directive (round 4b): no lesson is left out for naming "
                    "a client, so the line would promise a protection that does not exist. Remove the line." % where)
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
                pending.append((kind, glob_, where))
            else:
                die("%s: unknown directive %r" % (where, key))
    if sc["seat"] != seat:
        die("REFUSED: scope file %s is for seat %r but this tree resolves to seat %r" % (path, sc["seat"], seat))
    for kind, glob_, where in pending:              # judged only once the seat line is known to be this seat's
        check_allow(glob_, kind, where, seat, daily_rel)
        sc["allow"].append((kind, glob_))
    for w_ in sc["own"]:
        if not re.fullmatch(r"[a-z][a-z0-9]{2,}", w_):
            die("%s: a client name is one plain lower-case word of 3 or more letters and digits: %r" % (path, w_))
    if not sc["allow"]:
        die("scope file %s has no allow lines" % path)
    return sc


def check_allow(glob_, kind, where, seat, daily_rel):
    """An allow line is honoured only when it asks for something in the closed table above: the kind's one
    directory for THIS seat and, for ledgers, pickup files, the rules index and the rules files, one of the
    exact names listed there. Anything else is REFUSED here (N5, N7): a refusal, never a silent skip."""
    if not glob_ or glob_.startswith("/") or "\\" in glob_:
        die("%s: REFUSED, an allow path must be relative to the tree root: %r" % (where, glob_))
    d, pat = os.path.split(glob_)
    low = d.lower()
    for p in HARD_DENY_PREFIX:
        if low == p or low.startswith(p + "/"):
            die("%s: REFUSED, %s is never indexed (hard exclusion in braindb_index.py): %r" % (where, p, glob_))
    if any(s in HARD_DENY_SEGMENT for s in low.split("/")):
        die("%s: REFUSED, a credentials or keys directory is never indexed: %r" % (where, glob_))
    if pat.lower().startswith("chat_"):
        die("%s: REFUSED, chat stores are never indexed: %r" % (where, glob_))
    if kind == "rules":
        if glob_ not in ROOT_RULES:
            die("%s: REFUSED, kind 'rules' is only the seat's two rules files, named exactly (%s): %r"
                % (where, ", ".join(ROOT_RULES), glob_))
        return
    want_dir, names = allowed_place(seat, kind, daily_rel)
    if d != want_dir:
        die("%s: REFUSED, for seat '%s' kind '%s' is indexed only from %s/ (table in braindb_index.py); this line "
            "asks for %r. Another seat's records, and any folder not in the table, cannot be allowed by a scope line."
            % (where, seat, kind, want_dir, glob_))
    if names is not None:
        if pat not in names:
            die("%s: REFUSED, for seat '%s' kind '%s' is only the file(s) %s in %s/, named exactly (no pattern); "
                "this line asks for %r" % (where, seat, kind, ", ".join(names), want_dir, glob_))
        return
    if not pat.endswith(".md") or "/" in pat:
        die("%s: REFUSED, a %s pattern must be a file-name pattern ending in .md: %r" % (where, kind, glob_))


class Unsafe(Exception):
    """A file that may not be read: not a regular file, a link of either kind, or it changed under us."""


def open_checked(dirfd, name):
    """Open `name` inside the already-open directory WITHOUT following a symlink, then judge the file by
    fstat on the descriptor the bytes will be read from (N6): the thing judged is the thing read, so a file
    swapped for a symlink between a test and an open cannot get through. -> raw bytes, or raises Unsafe/OSError."""
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | getattr(os, "O_CLOEXEC", 0), dir_fd=dirfd)
    except OSError as e:
        import errno
        if e.errno in (errno.ELOOP, errno.EMLINK):
            raise Unsafe("symlink")
        raise
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise Unsafe("not a regular file")
        if st.st_nlink != 1:
            raise Unsafe("hard link (link count %d): the same file exists under another name" % st.st_nlink)
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
        return b"".join(chunks)
    finally:
        os.close(fd)


def enumerate_files(root, sc):
    """-> ({rel: (kind, raw bytes)}, [(rel, reason)]) for every allow-list match; the second list is what
    was skipped. Each file is read here, once, through open_checked(): nothing is opened by name later."""
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
            dirfd = os.open(absd, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | (os.O_NOFOLLOW if d else 0))
        except OSError as e:
            skipped.append((d + "/", "unreadable: %s" % type(e).__name__))
            continue
        try:
            try:
                names = sorted(os.listdir(dirfd))
            except OSError as e:
                skipped.append((d + "/", "unreadable: %s" % type(e).__name__))
                continue
            for name in names:
                if not fnmatch.fnmatchcase(name, pat):
                    continue
                rel = (d + "/" + name) if d else name
                if rel in out:
                    continue
                low = rel.lower()
                hit = next((x for x in tuple(sc["deny_path"]) + BUILTIN_DENY_PATH if x in low), None)
                if hit:
                    skipped.append((rel, "path contains '%s'" % hit))
                    continue
                # a file is taken only under the kind its name says it is
                if kind == "lesson" and not LESSON_NAME.fullmatch(name):
                    skipped.append((rel, "not a lesson file name (a lesson's name starts with its date)"))
                    continue
                if kind == "daily" and not DAILY_NAME.fullmatch(name):
                    skipped.append((rel, "not a daily-note file name (a plain date, nothing more)"))
                    continue
                if kind not in ("ledger", "rules_index") and name.lower().startswith("_"):
                    skipped.append((rel, "a file whose name starts with '_' is a ledger, digest or index, never a %s" % kind))
                    continue
                hit = next((x for x in sc["deny_seat_word"] if x in d.lower()), None)
                if hit:
                    skipped.append((rel, "another seat's records ('%s' in the folder name)" % hit))
                    continue
                try:
                    out[rel] = (kind, open_checked(dirfd, name))
                except Unsafe as e:
                    skipped.append((rel, str(e)))
                except OSError as e:
                    skipped.append((rel, "unreadable: %s" % type(e).__name__))
        finally:
            os.close(dirfd)
    return out, skipped


# ---------------------------------------------------------------- ROUND 4: QUALIFY OR STAY OUT
# A lesson is indexed only when it positively qualifies on EVERY clause below, each read strictly.
# Nothing here recognises a bad shape: each clause states the one good shape, and whatever is not that
# shape is left out and named with the clause it failed. There is no "untagged", no "unknown, so W",
# no section dropping and no fence or span parsing.

def fold(s):
    """Text reduced for a WORD test: compatibility forms unfolded, accents and format characters dropped,
    case folded. (Clause t guarantees every letter of a qualifying lesson is an ASCII letter under this.)"""
    return "".join(c for c in unicodedata.normalize("NFKD", s) if unicodedata.category(c) not in ("Mn", "Cf")).casefold()


def fold_key(s):
    """A frontmatter key folded HARD: NFKC, format characters and non-alphanumerics dropped, case folded."""
    return "".join(c for c in unicodedata.normalize("NFKC", s) if c.isalnum() and unicodedata.category(c) != "Cf").casefold()


def norm_name(s):
    """A file name or a rules-index key for comparison: NFC, format characters removed. Nothing else: no
    case folding, no stripping, no path removal. A key that is not EXACTLY the name is not this file's row."""
    return "".join(c for c in unicodedata.normalize("NFC", s) if unicodedata.category(c) != "Cf")


FM_KEY_LINE = re.compile(r"([a-z][a-z0-9_-]*):(?: (\S.*))?")
P_TIER = re.compile(r"P-([A-Za-z][A-Za-z0-9]*)/[A-Za-z0-9][A-Za-z0-9 ._-]*")
TIER_LINE_START = re.compile(r"^[^a-z0-9]*tier(?![a-z0-9])")                      # on a folded line
TIER_ASSIGN = re.compile(r"(?<![a-z0-9])tier[^a-z0-9\n]{0,3}(?:\([^)\n]{0,40}\)[^a-z0-9\n]{0,3})?[:=]")   # on a folded line


def allowed_tier(value, sc):
    """The CLOSED list of tier values, written exactly as the lessons write them: `W`, `M`, or
    `P-<Client>/<Project>` whose client is one of this seat's own. Nothing else is a tier."""
    if value in ("W", "M"):
        return True
    m = P_TIER.fullmatch(value or "")
    return bool(m) and m.group(1).casefold() in sc["own"]


def plain_text(raw):
    """Clause (t). -> (text, None) or (None, why). The bytes must be UTF-8 (an optional BOM first), hold no
    control, format or line-separator character other than LF and TAB, and every letter must be an ASCII
    letter once accents are removed. Without this the word tests of clauses (c) and (d) could be walked
    round with a look-alike letter, a zero-width character or a line break only some readers see."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "the file is not valid UTF-8"
    if text.startswith("﻿"):
        text = text[1:]
    for c in set(text):
        cat = unicodedata.category(c)
        if c in "\n\t":
            continue
        if cat in ("Cc", "Cf", "Zl", "Zp", "Cs", "Co", "Cn"):
            return None, "it holds a control, format or line-separator character (U+%04X)" % ord(c)
        if cat.startswith("L") and ord(c) > 127:
            base = "".join(x for x in unicodedata.normalize("NFKD", c) if not unicodedata.category(x).startswith("M"))
            if not base or any(ord(x) > 127 or not x.isalpha() for x in base):
                return None, "it holds a letter that is not a Latin letter (U+%04X)" % ord(c)
    return text, None


def qualify_lesson(name, raw, idx, sc):
    """-> (None, None) when the lesson qualifies, else (clause, why). Clauses: 'a' its rules-index row,
    'b' that row's seat, 'c' its frontmatter and tier, 'd' no tier marker or tier-like line, 't' plain text.
    `idx` is the parsed rules index (parse_rules_index)."""
    # ---- (t) plain text
    text, why = plain_text(raw)
    if text is None:
        return "t", why
    # ---- (a) exactly one row whose key EQUALS the file's name, in an index whose other rows do not name it
    key = norm_name(name)
    stem = key[:-3] if key.endswith(".md") else key
    for ln, bad in idx["rejected"]:
        if stem in bad:
            return "a", "a rules-index line that could not be read names it (line %d)" % ln
    mine = [r for r in idx["rows"] if r["base"] == key]
    plain = [r for r in mine if r["n"] == 1]
    if len(plain) != 1:
        return "a", ("it has no rules-index row whose key is exactly its file name" if not plain
                     else "it has %d rules-index rows with the same key" % len(plain))
    ns = [r["n"] for r in mine if r["n"] > 1]
    if len(ns) != len(set(ns)):
        return "a", "two of its rules-index rows have the same '#n' key"
    # ---- (b) that row names this seat
    seats = plain[0]["seats"]
    if not (ALL_SEATS in seats or sc["seat"] in seats):
        return "b", "its rules-index row is scoped to %s" % ",".join(seats)
    # ---- (c) one frontmatter block opened on line 1 and closed; one clean tier line; a tier from the closed list
    lines = text.split("\n")
    if lines[0] != "---":
        return "c", "line 1 is not exactly '---' (the frontmatter must open on line 1)"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return "c", "the frontmatter is not closed by a line that is exactly '---'"
    tier, seen = None, set()
    for i in range(1, end):
        m = FM_KEY_LINE.fullmatch(lines[i])
        if not m:
            return "c", "frontmatter line %d is not a plain 'key: value' line" % (i + 1)
        k, v = m.group(1), m.group(2) or ""
        if k in seen:
            return "c", "frontmatter key '%s' is given twice" % k
        seen.add(k)
        if k == "tier":
            tier = v
        elif "tier" in fold_key(k):
            return "c", "frontmatter key '%s' looks like a tier key and is not exactly 'tier'" % k
        elif TIER_ASSIGN.search(fold(v)) or TIER_LINE_START.search(fold(v)):
            return "c", "frontmatter line %d carries something tier-like inside the value of '%s'" % (i + 1, k)
    if tier is None:
        return "c", "no tier line in the frontmatter"
    nxt = next((l for l in lines[end + 1:] if l.strip()), "")
    if nxt.lstrip().startswith("---") or nxt.lstrip().startswith("+++"):
        return "c", "a second frontmatter block follows the first (exactly one is allowed)"
    if not allowed_tier(tier, sc):
        return "c", "tier '%s' is not one of this seat's tiers (W, M, P-<own client>/<project>)" % tier[:60]
    # ---- (d) no tier marker in any spelling ANYWHERE in the text, and nothing tier-like outside that one line
    if "<!--" in text or "-->" in text:
        return "d", "it holds an HTML comment (a section marker in any spelling is one)"
    for i, line in enumerate(lines):
        if i < end and i != 0 and line.startswith("tier:"):
            continue                                    # the one clean tier line, judged above
        f = fold(line)
        if TIER_LINE_START.search(f) or TIER_ASSIGN.search(f):
            return "d", "line %d is tier-like outside the frontmatter's one tier line" % (i + 1)
    # ROUND 4b (ANSWER-7, ruled): there is NO client-name test. A lesson is not left out for naming another
    # client; a word list is a recogniser, it took 55 of this seat's own lessons and still missed a project
    # named without its client. What keeps another client's material out is declared by a person: the row (b),
    # the tier (c) and the marker (d). Do not put a name test back.
    if "&#" in text:
        return "d", "it holds a numeric character reference (&#...;), which can spell the word tier where the line test cannot see it"
    return None, None


CLAUSES = (("a", "no single well-read rules-index row for it"),
           ("b", "its rules-index row is scoped to other seats"),
           ("c", "frontmatter or tier does not qualify"),
           ("d", "tier marker or tier-like line in its text"),
           ("t", "not plain text"),
           ("f", "not a plain regular file (link, hard link, unreadable)"))


# ---------------------------------------------------------------- parsing

def to_text(raw):
    """Bytes -> text for indexing: no BOM, LF line ends, no NUL and neither of the two separator bytes."""
    text = raw.decode("utf-8", errors="replace")
    if text.startswith("﻿"):
        text = text[1:]
    return text.replace("\r\n", "\n").translate(STRIP_BYTES)


def split_frontmatter(text):
    """-> (fm dict, body, body_first_line). For DISPLAY only (date, type, status of a file that is already
    in): it decides nothing. A lesson reaches here only after qualify_lesson() accepted its head."""
    lines = text.split("\n")
    fm, start = {}, 0
    if lines and lines[0] == "---" and "---" in lines[1:]:
        end = lines.index("---", 1)
        for line in lines[1:end]:
            m = FM_KEY_LINE.fullmatch(line)
            if m:
                fm[m.group(1)] = m.group(2) or ""
        start = end + 1
    return fm, "\n".join(lines[start:]), start + 1


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


ROW_KEY = re.compile(r"([^#/\\\t]+\.md)(?:#([2-9]|[1-9][0-9]+))?")


def parse_rules_index(raw):
    """-> dict(rows=[...], rejected=[(line_no, normalised line)], fatal=None or why).
    A ROW is read only when it is exactly the shape the spec gives (0_Brain/learnings/_rules_index/README.md):
    seven TAB-separated fields, none empty, none with outer white space, no control character; a key that is
    `<file>.md` or `<file>.md#n` (n >= 2); a status of live, dead or superseded; a seats cell that is `all`
    or a comma list of distinct seat words. Any other non-blank line, a comment line below line 1 included,
    is REJECTED and kept: qualify_lesson() leaves out every lesson whose name such a line so much as holds."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return dict(rows=[], rejected=[], fatal="it is not valid UTF-8")
    if text.startswith("﻿"):
        text = text[1:]
    rows, rejected = [], []
    for ln, line in enumerate(text.split("\n"), 1):
        if not line.strip():
            continue
        if ln == 1 and line.startswith("#"):
            continue                                 # the header comment
        nline = norm_name(line)
        f = nline.split("\t")
        ok = (len(f) == 7 and not line.startswith("#")
              and all(x and x == x.strip() for x in f)
              and not any(unicodedata.category(c) in ("Cc", "Zl", "Zp") and c != "\t" for c in nline))
        m = ROW_KEY.fullmatch(f[0]) if ok else None
        seats = f[2].split(",") if ok else []
        if not (m and f[1] in ROW_STATUS and len(seats) == len(set(seats))
                and (seats == [ALL_SEATS] or all(x in SEATS for x in seats))):
            rejected.append((ln, nline))
            continue
        rows.append(dict(key=f[0], base=m.group(1), n=int(m.group(2) or 1), status=f[1], seats=seats, family=f[3],
                         triggers=[t.strip() for t in f[4].split(",") if t.strip()], enforced_by=f[5], rule=f[6],
                         raw=nline, line=ln))
    return dict(rows=rows, rejected=rejected, fatal=None)


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
    """Walk the allow-list. -> dict(files={rel: dict(kind, sha, bytes, text)}, skipped=[(rel, reason)] for
    non-lesson files and folders, left_out=[(rel, clause, why)] for LESSON files, idx=the parsed rules index,
    rules={lesson file name: [its rows that name this seat]}, orphan_rows, other_seat_rows).
    rebuild and check both go through here, so they agree."""
    listed, skipped0 = enumerate_files(root, sc)
    lesson_dir = SHARED_DIRS["lesson"] + "/"
    skipped, left_out = [], []
    for rel, why in skipped0:
        is_lesson = rel.startswith(lesson_dir) and LESSON_NAME.fullmatch(rel[len(lesson_dir):] or "") \
            and not any(x in rel.lower() for x in tuple(sc["deny_path"]) + BUILTIN_DENY_PATH)
        if is_lesson:
            left_out.append((rel, "f", why))
        else:
            skipped.append((rel, why))
    wants_lessons = any(k == "lesson" for k, _ in sc["allow"])
    idx = dict(rows=[], rejected=[], fatal="no rules index is on the allow-list")
    idx_rels = [rel for rel in listed if listed[rel][0] == "rules_index"]
    if idx_rels:
        idx = parse_rules_index(listed[idx_rels[0]][1])
    elif any(k == "rules_index" for k, _ in sc["allow"]):
        idx["fatal"] = "it is missing, or is not a plain regular file (%s)" % (
            "; ".join(w for r, w in skipped if r.endswith("_rules_index.tsv")) or "not found")
    if wants_lessons and (idx["fatal"] or not idx["rows"]):
        die("REFUSED: lessons are on the allow-list but the rules index under %s cannot be used: %s. The rules "
            "index decides which lessons belong to this seat; without it no lesson qualifies. Nothing was read "
            "into or changed in the index." % (root, idx["fatal"] or "it has no row that could be read"), 2)
    files, rules = {}, {}
    names_on_disk = set()
    for rel in sorted(listed):
        kind, raw = listed[rel]
        name = os.path.basename(rel)
        if kind == "lesson":
            names_on_disk.add(norm_name(name))
            clause, why = qualify_lesson(name, raw, idx, sc)
            if clause:
                left_out.append((rel, clause, why))
                continue
            rules[name] = [r for r in idx["rows"] if r["base"] == norm_name(name)
                           and (ALL_SEATS in r["seats"] or sc["seat"] in r["seats"])]
        files[rel] = dict(kind=kind, sha=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                          text=to_text(raw) if want_text else None)
    for rel, clause, why in left_out:
        names_on_disk.add(norm_name(os.path.basename(rel)))
    orphan = sorted(set(r["key"] for r in idx["rows"] if r["base"] not in names_on_disk))
    kept = sum(len(v) for v in rules.values())
    return dict(files=files, skipped=skipped, left_out=sorted(left_out), idx=idx, rules=rules, orphan_rows=orphan,
                unreadable=[rel for rel, why in skipped0 if why.startswith("unreadable")],
                rows_not_joined=len(idx["rows"]) - kept)


def left_out_counts(res):
    c = dict((k, 0) for k, _ in CLAUSES)
    for _, clause, _ in res["left_out"]:
        c[clause] += 1
    return c


def left_out_line(res):
    """One line: how many lesson files are left out, by clause. Printed by rebuild (last line), check and doctor."""
    c = left_out_counts(res)
    n = len(res["left_out"])
    if not n:
        return "0 lesson files left out"
    return "%d lesson file(s) LEFT OUT by the qualify rule: %s" % (
        n, ", ".join("%s=%d" % (k, c[k]) for k, _ in CLAUSES if c[k]))


def print_left_out(res, limit):
    """The names, grouped by clause, up to `limit` per clause (0 = all)."""
    by = {}
    for rel, clause, why in res["left_out"]:
        by.setdefault(clause, []).append((rel, why))
    for k, title in CLAUSES:
        items = by.get(k, [])
        if not items:
            continue
        print("    clause (%s) %s: %d" % (k, title, len(items)))
        for rel, why in (items if not limit else items[:limit]):
            print("           %s  [%s]" % (os.path.basename(rel), why))
        if limit and len(items) > limit:
            print("           (+%d more: braindb.sh rebuild lists every name)" % (len(items) - limit))


def self_hashes(sc):
    def h(p):
        with open(p, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    return h(os.path.abspath(__file__)), h(sc["path"])


# ---------------------------------------------------------------- psql

def want_dd():
    """The data directory this command is addressed to, as the server itself spells it: braindb.sh resolves
    the path (realpath) once and both starts the server with it and passes it here."""
    return os.path.realpath(env("BRAINDB_PGDATA_EFF"))


def psql_cmd(db, variables=None, tuples=False):
    cmd = [os.path.join(env("BRAINDB_PGBIN_EFF"), "psql"), "-X", "-q", "-v", "ON_ERROR_STOP=1",
           "-h", env("BRAINDB_SOCKDIR_EFF"), "-p", env("BRAINDB_PORT_EFF"), "-d", db, "-v", "want_dd=" + want_dd()]
    for k, v in (variables or {}).items():
        cmd += ["-v", "%s=%s" % (k, v)]
    if tuples:
        cmd += ["-A", "-t", "-F", US, "-R", RS]
    return cmd


# ROUND 4 (N3): the FIRST statements of EVERY psql session this tool opens. They run in the same session, and
# for a rebuild or a read in the same transaction, as the work itself: the server that answers these is the
# server that does the work, so there is no moment between "which cluster is this" and the write.
ASSERT_SQL = r"""SELECT set_config('braindb.want_dd', :'want_dd', false) AS v \gset bdb_
DO $bdb$ BEGIN
  IF current_setting('data_directory') IS DISTINCT FROM current_setting('braindb.want_dd') THEN
    RAISE EXCEPTION 'BRAINDB_WRONG_CLUSTER got=[%] want=[%]', current_setting('data_directory'), current_setting('braindb.want_dd');
  END IF;
END $bdb$;
"""
WRONG = re.compile(r"BRAINDB_WRONG_CLUSTER got=\[(.*?)\] want=\[")


def judge_psql(rc, err, on_down="die"):
    """Exit the tool when the session was refused or never happened. rc 4: another cluster answered (nothing
    was read or changed). rc 3: nothing answered (N11: an empty answer is 'not answering', never 'another')."""
    m = WRONG.search(err)
    if m:
        die("REFUSED: the server answering on socket directory %s serves data directory '%s', but this command "
            "is addressed to '%s'. Nothing was read or changed. Another cluster is using this socket directory: "
            "stop it with its own braindb.sh, or give this one its own BRAINDB_SOCKDIR."
            % (env("BRAINDB_SOCKDIR_EFF"), m.group(1), want_dd()), 4)
    if rc == 2 and not re.search(r'database "[^"]*" does not exist', err):
        if on_down == "die":
            die("the index server is not answering on %s (run: braindb.sh start)" % env("BRAINDB_SOCKDIR_EFF"), 3)
        return "down"
    return "ok"


def query(sql, db=DB, variables=None, txn=True, on_down="die"):
    """Run SQL read from stdin (so :'var' is interpolated) in ONE psql session that first asserts the server's
    data directory. -> (rc, [row fields]); with on_down='return', rc is 'down' when nothing answers."""
    full = ("BEGIN;\n" if txn else "") + ASSERT_SQL + sql + ("\n;COMMIT;\n" if txn else "\n")
    r = subprocess.run(psql_cmd(db, variables, tuples=True), input=full.encode("utf-8"),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = r.stderr.decode("utf-8", errors="replace")
    if judge_psql(r.returncode, err, on_down) == "down":
        return "down", []
    if err:
        sys.stderr.write(err)                         # psql's own words are never discarded
    out = r.stdout.decode("utf-8", errors="replace")
    if out.endswith("\n"):
        out = out[:-1]
    rows = [rec.split(US) for rec in out.split(RS)] if out else []
    return r.returncode, rows


def need_server():
    """An early, friendly form of the same test: rc 3 when nothing answers, rc 4 when another cluster does.
    It is NOT what protects the work: every later session carries the assertion itself."""
    rc, rows = query("select 1", db="postgres")
    if rc != 0 or rows != [["1"]]:
        die("the index server is not answering on %s (run: braindb.sh start)" % env("BRAINDB_SOCKDIR_EFF"), 3)


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
    idx = sc_res["idx"]
    kept_rules = []
    for name in sorted(sc_res["rules"]):
        for r in sc_res["rules"][name]:
            kept_rules.append(dict(r, file=name))
    notes.append("rules index: %d row(s) read, %d joined to an indexed lesson for this seat, %d not joined "
                 "(the lesson is left out or missing, or the row is scoped to other seats)"
                 % (len(idx["rows"]), len(kept_rules), sc_res["rows_not_joined"]))
    if idx["rejected"]:
        notes.append("rules index: %d line(s) could NOT be read as a row (line %s); every lesson such a line "
                     "names is left out under clause (a)"
                     % (len(idx["rejected"]), ", ".join(str(ln) for ln, _ in idx["rejected"][:20])))
    if sc_res["orphan_rows"]:
        notes.append("rules index: %d row(s) name no lesson file on disk: %s"
                     % (len(sc_res["orphan_rows"]), ", ".join(sc_res["orphan_rows"][:10])))

    ledger_lines = []
    cid = 0
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
        fm, body, first = split_frontmatter(text)
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
            mine = sc_res["rules"].get(name, [])
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
        T["rules"].append((r["key"], r["file"], r["n"], r["status"], pg_array(r["seats"]), r["family"],
                           pg_array(r["triggers"]), r["enforced_by"], r["rule"], w, iso_date(last)))
    return T, sc_res, notes, truncated


def reason_group(why):
    """One heading per kind of skip, for the rebuild report (non-lesson files)."""
    return re.sub(r"\s*\(link count \d+\).*$", "", why)


def take_lock():
    """One rebuild at a time per cluster (two first builds would both try to create the database). The lock
    is flock() on the cluster's lock file; the kernel drops it when this process ends. The wait has the same
    limit and the same words as braindb_lock.py (N13)."""
    import fcntl
    path = env("BRAINDB_LOCK_EFF")
    try:
        wait_s = float(os.environ.get("BRAINDB_LOCK_WAIT", "150"))
    except ValueError:
        die("BRAINDB_LOCK_WAIT must be a number of seconds")
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    deadline = time.time() + wait_s
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd
        except OSError:
            if time.time() > deadline:
                print("braindb: another braindb command has held %s for more than %.0f s; nothing was done" % (path, wait_s),
                      file=sys.stderr)
                sys.exit(75)
            time.sleep(0.1)


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
        # same session: the assertion, then the CREATE (which cannot run inside a transaction block)
        rc, _ = query("CREATE DATABASE braindb ENCODING 'UTF8' TEMPLATE template0", db="postgres", txn=False)
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
            ("faults", json.dumps(dict(unreadable=len(sc_res["unreadable"]), truncated=len(truncated)))),
            ("left_out", json.dumps(dict(total=len(sc_res["left_out"]), by_clause=left_out_counts(sc_res))))]
    hold = os.environ.get("BRAINDB_TEST_HOLD")       # tests only: pause here, after every separate session and
    if hold:                                         # before the load session opens, until the named file exists
        open(hold + ".waiting", "w").close()
        t_hold = time.time()
        while not os.path.exists(hold) and time.time() - t_hold < 60:
            time.sleep(0.1)
    p = subprocess.Popen(psql_cmd(DB), stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    errbuf = []
    drain = threading.Thread(target=lambda: errbuf.append(p.stderr.read()))
    drain.start()
    try:
        w = lambda s: p.stdin.write(s.encode("utf-8"))
        # ONE session, ONE transaction: BEGIN, the data-directory assertion, then the whole reload.
        w("BEGIN;\n" + ASSERT_SQL)
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
    drain.join()
    err = b"".join(errbuf).decode("utf-8", errors="replace")
    judge_psql(rc, err)
    if err:
        sys.stderr.write(err)
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
        print("  matched an allow line but NOT indexed (files that are not lessons): %d" % len(sc_res["skipped"]))
        for key in sorted(reasons):
            items = reasons[key]
            full = key.startswith(("unreadable", "hard link", "symlink", "not a regular", "directory is"))
            show = items if full else items[:4]
            print("    %3d  %s%s" % (len(items), key.strip(), "" if full else "  (%s%s)" % (
                ", ".join(os.path.basename(x.rstrip("/")) or x for x, _ in show), ", ..." if len(items) > 4 else "")))
            if full:
                for rel, why in show:
                    print("           %s  [%s]" % (rel, why))
    n_lessons = fkinds.get("lesson", 0)
    print("  LESSONS: %d file(s) matched the allow line; %d qualified and are indexed; %d LEFT OUT, each named with the clause it failed:"
          % (n_lessons + len(sc_res["left_out"]), n_lessons, len(sc_res["left_out"])))
    print_left_out(sc_res, 0)
    if truncated:
        print("  rows TRUNCATED at their size limit: %d" % len(truncated))
        for rel, line, what, n in truncated[:20]:
            print("           %s:%s  %s of %d characters" % (rel, line, what, n))
        if len(truncated) > 20:
            print("           (+%d more)" % (len(truncated) - 20))
    print("  time: %.2f s (read and parse %.2f s, load and index %.2f s)" % (dt, t_parse, dt - t_parse))
    nu, nt = len(sc_res["unreadable"]), len(truncated)
    tail = left_out_line(sc_res)
    if nu or nt:
        print("rebuild: DONE WITH FAULTS: %d unreadable file(s) skipped, %d row(s) truncated; they are listed above; %s" % (nu, nt, tail))
    else:
        print("rebuild: done; no file was unreadable and no row was truncated; %s" % tail)
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
    def tail_lines():
        print(where)
        print(faults)
        for rel in res["unreadable"][:20]:
            print("    unreadable: " + rel)
        print("  left out: " + left_out_line(res))
        print_left_out(res, NAMES_SHOWN)
        if res["idx"]["rejected"]:
            print("  rules index: %d line(s) could not be read as a row (line %s)" % (
                len(res["idx"]["rejected"]), ", ".join(str(ln) for ln, _ in res["idx"]["rejected"][:20])))
    if not diffs and not stale:
        print("check: GREEN, %d files on disk match the index (built %s)" % (len(disk), meta.get("built_at", "?")))
        tail_lines()
        return 0
    print("check: RED, %d path(s) differ%s (run: braindb.sh rebuild)"
          % (len(diffs), "; " + "; ".join(stale) if stale else ""))
    for d in diffs[:20]:
        print("  " + d)
    if len(diffs) > 20:
        print("  (+%d more)" % (len(diffs) - 20))
    tail_lines()
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
), flagged AS (
    -- N9: a rules-file row that holds EVERY key word is selected here, before the top-N cut, so whether it is
    -- shown first can never depend on --limit
    SELECT b.id, b.score, b.kind,
           (b.kind = 'rules' AND :'mode' = 'default' AND EXISTS (SELECT 1 FROM keyw)
            AND NOT EXISTS (SELECT 1 FROM keyw k JOIN brain.chunks c ON c.id = b.id WHERE NOT c.tsv @@ k.tq)) AS lead
    FROM best b
), grouped AS (
    SELECT id, score, lead, CASE WHEN kind IN ('ledger', 'daily') THEN 1 ELSE 0 END AS grp,
           row_number() OVER (PARTITION BY (CASE WHEN kind IN ('ledger', 'daily') THEN 1 ELSE 0 END)
                              ORDER BY score DESC, id) AS rn,
           row_number() OVER (PARTITION BY lead ORDER BY score DESC, id) AS rn_lead
    FROM flagged
), top AS (
    SELECT id, score, grp FROM grouped WHERE rn <= :lim OR (lead AND rn_lead <= :lim)
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

NAMES_SHOWN = 5        # check: names printed per clause of the qualify rule (rebuild prints every name)
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
    rc, rows = query(SEARCH_SQL, variables=dict(q=words, kind=kind, lim=str(a.limit), topk=topk, mode=mode))
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
        rc, lo = query("select v from brain.meta where k = 'left_out'")
        try:
            n_out = json.loads(lo[0][0])["total"] if rc == 0 and lo else 0
        except (ValueError, KeyError, IndexError, TypeError):
            n_out = 0
        if n_out:
            print("NOTE: %d lesson file(s) are LEFT OUT of this index by the qualify rule and are not searched; "
                  "`braindb.sh check` names them. search does not look inside them." % n_out)
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
    if a.top < 0:
        die("--top must be 0 (all) or more")
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
    rc, rows = query("select 1", db="postgres", on_down="return")   # rc 4 (exit) when another cluster answers
    if rc == "down":
        print("  the server process exists but is not answering on %s" % env("BRAINDB_SOCKDIR_EFF"))
        return 3
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
    rc, rows = query("select k, v from brain.meta where k in ('built_at', 'seat', 'counts', 'faults', 'left_out') order by k")
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
    sub.add_parser("validate")
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
    sc = load_scope(env("BRAINDB_SCOPE_EFF"), seat, os.environ.get("BRAINDB_DAILY_REL") or None)
    if a.cmd == "validate":                          # the scope is sound; nothing was created, started or read
        return 0
    return dict(rebuild=cmd_rebuild, check=cmd_check, search=cmd_search, at=cmd_at, info=cmd_info)[a.cmd](a, root, sc, seat)


if __name__ == "__main__":
    sys.exit(main())
