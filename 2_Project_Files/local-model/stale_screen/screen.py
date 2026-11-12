#!/usr/bin/env python3
"""screen.py - the nightly STALE-TICKET SCREEN (Kam 2026-11-12 11:36, routine (b); commission in
0_Brain/reference/2026-11-12_spark-stale-ticket-screen/commission.md).

For each open Secuura (KS) ticket (Backlog / Todo / In Progress) it:
  1. extracts every code citation DETERMINISTICALLY (paths, file:line, symbols in backticks),
  2. resolves each at LIVE develop (ls-remote for the sha; git show/grep in a --shared clone in this job's own scratch;
     NEVER a fetch or write into the shared checkout) -> FACTS (F1, F2 ... each with a status),
  3. asks the local Spark ONE question per ticket: STILL-VALID | LIKELY-FIXED | CITATION-MOVED |
     POSSIBLE-DUPLICATE-OF <key> | CANNOT-TELL, with a one-line reason citing a fact id,
  4. a CHECKER refuses any proposal whose reason cites a path/symbol/key/number that is not in FACTS, that cites a fact
     id that does not exist or whose status cannot support the class, or whose duplicate key is not an open ticket
     (and a candidate this ticket actually shares a citation/title with).
Output per run: proposals.tsv (key, proposal, reason, facts-hash, ...) + report.md (BLUF + class counts) + facts/ + spark/.
PROPOSALS ONLY. This script performs NO Linear write (the only HTTP verbs it sends to Linear are GraphQL *queries*), no
comment, no state change; a Claude board seat confirms before any board change.

usage: screen.py --limit N --out DIR [--wait SEC] [--update-state] [--keys KS-1,KS-2] [--facts-only]
       [--fixture tickets.json] [--repo CHECKOUT] [--no-remote] [--deadline HH:MM] [--env /path/.env]
Exit codes: 0 = ran, or refused cleanly (tunnel down / round live / outside the box's availability: said on stdout+log);
            2 = usage / harness fault (cannot read the board, cannot resolve develop).
Seams (tests): SCREEN_SPARK_STUB=<json file {key|"*": reply object|string}> bypasses the box; SPARK_URL; SPARK_STATE_DIR.
Python 3 stdlib only. One request at a time: takes spark/state/round.lock around EACH request (the same protocol round.sh
uses: mkdir + pid + what), refuses/ waits while another holder, a live queue.lock, or vLLM's own num_requests_running/waiting > 0.
"""
import argparse, collections, hashlib, json, os, re, signal, subprocess, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
LM = os.path.normpath(os.path.join(HERE, ".."))
SPARK_STATE = os.environ.get("SPARK_STATE_DIR") or os.path.join(LM, "spark", "state")
URL = os.environ.get("SPARK_URL", "http://127.0.0.1:47788").rstrip("/")
MODEL = os.environ.get("SPARK_MODEL", "deepseek-v4-flash-0731")
SECUURA = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain"
DEFAULT_REPO = SECUURA + "/2_Project_Files"
DEFAULT_ENV = SECUURA + "/4_Credentials/.env"
HIST = SECUURA + "/5_Project_History"
STATES = ["Backlog", "Todo", "In Progress"]
HUMANS = {"peter@obeden.com", "stuart.jamieson@secuura.ai"}
HUMAN_NAMES = ("peter", "stuart")
CLASSES = ["STILL-VALID", "LIKELY-FIXED", "CITATION-MOVED", "POSSIBLE-DUPLICATE", "CANNOT-TELL"]
OKS = {"OK", "UNCHANGED", "PRESENT", "SYMBOL_PARTIAL"}            # a cited thing is there
BADS = {"MISSING", "SYMBOL_ABSENT", "BEYOND_EOF"}  # a cited thing is gone
VALID_CITE = OKS | {"CHANGED", "UNMENTIONED", "REFERENCED", "NOT_IN_REPO"}
FIXED_CITE = BADS | {"MENTIONED"}   # a file merely being edited (CHANGED) is not evidence a problem was fixed
MOVED_CITE = {"MOVED", "AMBIGUOUS", "BEYOND_EOF", "SYMBOL_MOVED"}


def log(*a):
    print("screen:", *a, flush=True)


# ------------------------------------------------------------------------------------------ Spark box gate + client
def _live_pid(lock_dir):
    try:
        pid = int(open(os.path.join(lock_dir, "pid")).read().strip())
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError):
        return None


def tunnel_up():
    try:
        with urllib.request.urlopen(URL + "/v1/models", timeout=4) as r:
            return r.status == 200, "HTTP %s" % r.status
    except Exception as e:  # noqa: BLE001 - any failure is DOWN, with its reason
        return False, type(e).__name__


def vllm_busy():
    """vLLM's own gauges: the one signal that sees a client that holds no lock (the digest pilot waits on the lock but does
    not take it). None when /metrics is unreadable (then only the locks gate)."""
    try:
        with urllib.request.urlopen(URL + "/metrics", timeout=4) as r:
            t = r.read().decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return None
    n = 0.0
    for m in re.finditer(r"^vllm:num_requests_(?:running|waiting)\{[^}]*\}\s+([0-9.]+)", t, re.M):
        n += float(m.group(1))
    return n


def box_state():
    """('ok'|'busy'|'down', why). Lock first (so a live round is named as such even with a dead tunnel), then the tunnel."""
    lock = os.path.join(SPARK_STATE, "round.lock")
    if os.path.exists(lock):
        pid = _live_pid(lock)
        if pid:
            what = ""
            try: what = open(os.path.join(lock, "what")).read().strip()[:80]
            except OSError: pass
            return "busy", "a Spark round is live (round.lock pid %s: %s)" % (pid, what)
        # stale lock (holder dead): reclaim exactly as round.sh does (move aside, never delete)
        stale = os.path.join(SPARK_STATE, "stale_locks", time.strftime("%Y%m%d-%H%M%S"))
        try:
            os.makedirs(stale, exist_ok=True); os.rename(lock, os.path.join(stale, "round.lock"))
            log("reclaimed a stale round.lock (holder not alive) ->", stale)
        except OSError as e:
            return "busy", "round.lock present, holder dead, could not reclaim it (%s)" % type(e).__name__
    q = os.path.join(SPARK_STATE, "queue.lock")
    if os.path.exists(q) and _live_pid(q):
        return "busy", "a live queue.lock holder (pid %s) is draining the Spark queue" % _live_pid(q)
    up, why = tunnel_up()
    if not up:
        return "down", "Spark tunnel/endpoint is DOWN (%s at %s)" % (why, URL)
    b = vllm_busy()
    if b is not None and b > 0:
        return "busy", "vLLM reports %d request(s) running/waiting (someone is using the box without a lock)" % int(b)
    return "ok", "free"


class Box:
    """Holds spark/state/round.lock for exactly one request at a time."""
    def __init__(self):
        self.lock = os.path.join(SPARK_STATE, "round.lock")
        self.held = False

    def acquire(self, what):
        os.makedirs(SPARK_STATE, exist_ok=True)
        try:
            os.mkdir(self.lock)
        except OSError:
            return False
        open(os.path.join(self.lock, "pid"), "w").write(str(os.getpid()))
        open(os.path.join(self.lock, "what"), "w").write("stale-screen %s since %s" % (what, time.strftime("%F %T")))
        self.held = True
        return True

    def release(self):
        if not self.held:
            return
        for f in ("pid", "what"):
            try: os.remove(os.path.join(self.lock, f))   # our own lock files only: the protocol's release, not a project file
            except OSError: pass
        try: os.rmdir(self.lock)
        except OSError: pass
        self.held = False


BOX = Box()


def _on_term(signum, frame):
    BOX.release()
    sys.exit(143)


signal.signal(signal.SIGTERM, _on_term)
signal.signal(signal.SIGINT, _on_term)


def wait_box(wait_s, what):
    """Block until the box is free AND we hold the lock (<= wait_s). Returns (True,'') or (False, reason)."""
    t0 = time.time(); last = ""
    while True:
        st, why = box_state()
        if st == "ok" and BOX.acquire(what):
            return True, ""
        if st == "ok":
            st, why = "busy", "lost the race for round.lock"
        if st == "down" or time.time() - t0 >= wait_s:
            return False, why
        if why != last:
            log("waiting:", why); last = why
        time.sleep(15)


SYSTEM = """You screen ONE open engineering ticket for staleness. You get the ticket text and a FACTS list that a script measured from the code at the live develop branch. Propose exactly ONE class:
- STILL-VALID: the code the ticket cites is present at develop and nothing in FACTS suggests the described problem was addressed.
- LIKELY-FIXED: a cited file or symbol is gone (MISSING / SYMBOL_ABSENT / BEYOND_EOF), or a MENTIONED fact shows commits that are this ticket's own work. A REFERENCED fact (a mere Refs/prose mention) is NOT evidence of a fix. A file merely being edited (CHANGED) is NOT enough. A NOT_IN_REPO symbol is NOT evidence of removal.
- CITATION-MOVED: the problem may still exist but the cited path, symbol or line now lives elsewhere (the fact says where).
- POSSIBLE-DUPLICATE: a CANDIDATE fact looks like the same problem; set duplicate_of to that candidate's key.
- CANNOT-TELL: FACTS do not support a call. When unsure, choose this. A ticket with no citations is CANNOT-TELL unless a CANDIDATE fact is a clear duplicate.
You never close or change a ticket: a human reviews your proposal. Use ONLY paths, symbols, KS keys and numbers that appear in FACTS.
Reply with ONE JSON object and nothing else:
{"proposal":"STILL-VALID|LIKELY-FIXED|CITATION-MOVED|POSSIBLE-DUPLICATE|CANNOT-TELL","duplicate_of":null,"fact_ids":["F1"],"reason":"ONE line, at most 220 characters, citing at least one fact id like [F2] and repeating the path or symbol exactly as the fact writes it"}"""


def build_prompt(t, facts):
    c = t.get("comments") or []
    cm = "\n".join("- [%s] %s" % ((x.get("createdAt") or "")[:10], " ".join((x.get("body") or "").split())[:500]) for x in c) or "(none)"
    d = t.get("description") or ""
    if len(d) > 5000:
        d = d[:4000] + "\n[... %d chars omitted ...]\n" % (len(d) - 5000) + d[-1000:]
    fl = "\n".join("[%s] %s %s: %s" % (f["id"], f["kind"], f["status"], f["text"]) for f in facts) or "(no citations were found in the ticket)"
    return ("TICKET %s [%s] created %s\nTITLE: %s\n\nDESCRIPTION:\n%s\n\nNEWEST COMMENTS:\n%s\n\nFACTS (measured at develop %s):\n%s\n\nReply with the JSON object."
            % (t["identifier"], t["state"]["name"], (t.get("createdAt") or "")[:10], t.get("title") or "", d, cm, t.get("_tip", "")[:12], fl))


def spark_call(key, prompt, max_tokens=500):
    """ONE non-streamed request. Returns (text, seconds). Raises on transport failure. The stub bypasses the box."""
    stub = os.environ.get("SCREEN_SPARK_STUB")
    if stub:
        m = json.load(open(stub))
        r = m.get(key, m.get("*"))
        if r is None:
            raise RuntimeError("stub has no reply for %s" % key)
        return (r if isinstance(r, str) else json.dumps(r)), 0.0
    body = {"model": MODEL, "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
            "max_tokens": max_tokens, "temperature": 0, "chat_template_kwargs": {"thinking": False}}
    req = urllib.request.Request(URL + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        j = json.load(r)
    return (j["choices"][0]["message"].get("content") or "").strip(), time.time() - t0


def extract_json(s):
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s.strip())
    a, b = s.find("{"), s.rfind("}")
    if a < 0 or b < a:
        raise ValueError("no JSON object in the reply")
    return json.loads(s[a:b + 1])


# ------------------------------------------------------------------------------------------ citation extraction
EXT = r"(?:tsx?|jsx?|mjs|cjs|py|sh|ya?ml|json|md|sql|toml|go|rs|css|html|conf|tf|bash|lock|txt|prisma|cfg|ini)"
PATH_RE = re.compile(r"(?<![\w/@.:\-])((?:\.{0,2}/)?(?:[\w@.\-]+/)*[\w@\-][\w@.\-]*\.%s)(?:(?::|#L)(\d+)(?:[-–](?:L)?(\d+))?)?(?![\w/])" % EXT)
IDENT_RE = re.compile(r"^[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*(?:\(\))?$")
NOT_FILES = {"node.js", "next.js", "vue.js", "express.js", "react.js", "d3.js", "three.js", "chart.js", "nest.js", "nuxt.js", "ember.js", "e.g", "i.e"}
STOP_SYM = {"true", "false", "null", "undefined", "string", "number", "boolean", "object", "array", "void", "async", "await", "const", "return",
            "function", "class", "import", "export", "default", "type", "interface", "promise", "error", "json", "http", "https", "get", "post",
            "put", "patch", "delete", "npm", "git", "docker", "node", "main", "develop", "master", "test", "todo", "none", "nan", "env"}
MAX_PATHS, MAX_SYMS = 10, 8


def extract_citations(text):
    """-> (paths [(path, line_a, line_b, quoted)], symbols [str], dropped count). Deterministic; order of first appearance."""
    t = re.sub(r"https?://\S+", " ", text or "")
    quoted = set(re.findall(r"`([^`\n]+)`", t))
    paths, seen = [], set()
    for m in PATH_RE.finditer(t):
        p = m.group(1)
        if p.startswith("./"):
            p = p[2:]
        if p.lower() in NOT_FILES or p.lower().endswith(("e.g", "i.e")):
            continue
        a = int(m.group(2)) if m.group(2) else None
        b = int(m.group(3)) if m.group(3) else a
        k = (p, a, b)
        if k in seen:
            continue
        seen.add(k)
        paths.append((p, a, b, any(p in q for q in quoted)))
    syms, sseen = [], set()
    for q in re.findall(r"`([^`\n]{3,80})`", t):
        q = q.strip()
        if PATH_RE.fullmatch(q) or not IDENT_RE.match(q):
            continue
        s = q[:-2] if q.endswith("()") else q
        if len(s) < 4 or s.lower() in STOP_SYM:
            continue
        if not (re.search(r"[A-Z_]", s) or "." in s or q.endswith("()")):
            continue
        if s not in sseen:
            sseen.add(s); syms.append(s)
    dropped = max(0, len({p[0] for p in paths}) - MAX_PATHS) + max(0, len(syms) - MAX_SYMS)
    return paths, syms[:MAX_SYMS], dropped


# ------------------------------------------------------------------------------------------ git facts (read-only)
def git(clone, *a, timeout=90):
    try:
        r = subprocess.run(["git", "-C", clone, *a], capture_output=True, text=True, timeout=timeout, errors="replace")
        return r.stdout
    except subprocess.TimeoutExpired:
        return ""


class Tree:
    def __init__(self, clone, sha):
        self.clone, self.sha = clone, sha
        self.files = [l for l in git(clone, "ls-tree", "-r", "--name-only", sha, timeout=300).splitlines() if l]
        self.set = set(self.files)
        self.by_base = collections.defaultdict(list)
        for f in self.files:
            self.by_base[f.rsplit("/", 1)[-1]].append(f)
        self._blob = {}

    def lines(self, path):
        if path not in self._blob:
            self._blob[path] = git(self.clone, "show", "%s:%s" % (self.sha, path)).splitlines()
        return self._blob[path]


def resolve_path(tree, p):
    """-> (status, [resolved paths], moved-candidates). OK exact or unique suffix; AMBIGUOUS several suffix; MOVED same basename elsewhere; MISSING."""
    if p in tree.set:
        return "OK", [p], []
    base = p.rsplit("/", 1)[-1]
    same = tree.by_base.get(base, [])
    suf = [f for f in same if f.endswith("/" + p)] if "/" in p else list(same)
    if len(suf) == 1:
        return "OK", suf, []
    if len(suf) > 1:
        return "AMBIGUOUS", suf[:3], []
    if same:
        return "MOVED", [], same[:3]
    return "MISSING", [], []


def trunc(s, n):
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n - 3] + "..."


def build_facts(t, tree, paths, syms, dropped):
    """The deterministic FACTS for one ticket. Each fact: id, kind, status, text (the exact text the checker's corpus is built from)."""
    facts = []

    def add(kind, status, text):
        facts.append({"id": "F%d" % (len(facts) + 1), "kind": kind, "status": status, "text": text})
    created = (t.get("createdAt") or "")[:10]
    cited_files, seen_p = [], set()
    uniq = []
    for p, a, b, q in paths:
        if p not in seen_p:
            seen_p.add(p); uniq.append(p)
    kept = set(uniq[:MAX_PATHS])
    # bare, unquoted names that are not in the tree are prose ("Node.js"), not citations
    resolved = {}
    for p in uniq:
        if p not in kept:
            continue
        st, res, mv = resolve_path(tree, p)
        if "/" not in p and st in ("MISSING", "MOVED") and not any(pp == p and q for pp, _, _, q in paths):
            kept.discard(p)
            continue
        resolved[p] = (st, res, mv)
    for p in uniq:
        if p not in resolved:
            continue
        st, res, mv = resolved[p]
        if st == "OK":
            full = res[0]
            add("PATH", "OK", "cited `%s` exists at develop%s" % (p, "" if full == p else " as `%s` (the ticket omitted a directory prefix)" % full))
            if full in cited_files:
                continue          # same file already cited another way: one CHANGES fact per file
            cited_files.append(full)
            n = len([x for x in git(tree.clone, "log", "--since=%s" % created, "--format=%h", tree.sha, "--", full).split() if x]) if created else 0
            last = git(tree.clone, "log", "-1", "--format=%h %cs %s", tree.sha, "--", full).strip()
            add("CHANGES", "CHANGED" if n else "UNCHANGED",
                "%d commit(s) touched `%s` since the ticket was created (%s); latest: %s" % (n, full, created or "?", trunc(last, 110)))
        elif st == "AMBIGUOUS":
            add("PATH", "AMBIGUOUS", "cited `%s` matches %d files at develop (e.g. %s)" % (p, len(res), ", ".join("`%s`" % r for r in res)))
            cited_files.extend(res)
        elif st == "MOVED":
            add("PATH", "MOVED", "cited `%s` does NOT exist at develop, but a file with the same name does: %s" % (p, ", ".join("`%s`" % r for r in mv)))
            cited_files.extend(mv[:1])
        else:
            dele = git(tree.clone, "log", "-1", "--diff-filter=D", "--format=%h %cs %s", tree.sha, "--", p, timeout=45).strip()
            add("PATH", "MISSING", "cited `%s` does NOT exist at develop and no file with that name exists%s"
                % (p, "; last deleted by commit %s" % trunc(dele, 110) if dele else "; no deleting commit found in history"))
    # file:line citations (at most 8 facts; the rest are counted, never silently dropped)
    nline = 0
    for p, a, b, q in paths:
        if a is None or p not in resolved or resolved[p][0] != "OK":
            continue
        nline += 1
        if nline > 8:
            continue
        full = resolved[p][1][0]
        ls = tree.lines(full)
        if a > len(ls):
            add("LINE", "BEYOND_EOF", "cited `%s:%d` is beyond the end of the file: `%s` has %d lines at develop" % (p, a, full, len(ls)))
        else:
            seg = " | ".join(trunc(ls[i - 1], 90) for i in range(a, min(b or a, a + 2, len(ls)) + 1))
            add("LINE", "PRESENT", "cited `%s:%d` now reads: %s (file has %d lines)" % (p, a, seg, len(ls)))
    # symbols
    for s in syms:
        term = s
        w = ["-w"] if re.match(r"^[\w$]+$", s) else []
        excl = [":(exclude)*.md", ":(exclude)*package-lock.json", ":(exclude)*.lock", ":(exclude)node_modules"]
        hit_in_cited = []
        for cf in dict.fromkeys(cited_files):
            if git(tree.clone, "grep", "-c", "-F", *w, "-e", term, tree.sha, "--", cf).strip():
                hit_in_cited.append(cf)
        if hit_in_cited:
            add("SYMBOL", "OK", "symbol `%s` is present in cited file(s): %s" % (s, ", ".join("`%s`" % h for h in hit_in_cited[:3])))
            continue
        out = [l.split(":", 1)[1] for l in git(tree.clone, "grep", "-l", "-F", *w, "-e", term, tree.sha, "--", ".", *excl, timeout=120).splitlines() if ":" in l]
        if not out and "." in s:   # a dotted table.column / obj.member: try its last part before calling it absent
            last = s.rsplit(".", 1)[1]
            part = [l.split(":", 1)[1] for l in git(tree.clone, "grep", "-l", "-F", "-w", "-e", last, tree.sha, "--", ".", *excl, timeout=120).splitlines() if ":" in l]
            if part:
                add("SYMBOL", "SYMBOL_PARTIAL", "symbol `%s` is not written literally anywhere, but its last part `%s` appears in %d file(s), e.g. %s" % (s, last, len(part), ", ".join("`%s`" % o for o in part[:3])))
                continue
        if out:
            if cited_files:
                add("SYMBOL", "SYMBOL_MOVED", "symbol `%s` is NOT in the cited file(s) but appears in %d other file(s), e.g. %s" % (s, len(out), ", ".join("`%s`" % o for o in out[:3])))
            else:
                add("SYMBOL", "OK", "symbol `%s` appears at develop in %d file(s), e.g. %s" % (s, len(out), ", ".join("`%s`" % o for o in out[:3])))
        elif cited_files:
            add("SYMBOL", "SYMBOL_ABSENT", "symbol `%s` appears in NO code file at develop, not even the cited file(s) (markdown and lockfiles excluded)" % s)
        else:
            add("SYMBOL", "NOT_IN_REPO", "symbol `%s` appears in NO code file at develop, but the ticket cites no file for it, so it may live outside this repository (an external API, another repo): this is NOT evidence it was removed" % s)
    dropped += max(0, nline - 8)
    num = (t.get("identifier") or "").split("-")[-1]
    if num.isdigit():
        raw = git(tree.clone, "log", "-E", "--since=%s" % created, "--grep=KS-%s([^0-9]|$)" % num, "--format=%h%x1f%cs%x1f%B%x1e", tree.sha, timeout=120) if created else ""
        own, ref = [], []
        for rec in [r for r in raw.split("\x1e") if r.strip()]:
            h, d, body = (rec.strip("\n").split("\x1f", 2) + ["", ""])[:3]
            subj = body.strip().splitlines()[0] if body.strip() else ""
            line = "%s %s %s" % (h.strip(), d, trunc(subj, 110))
            # STRONG = the commit is this ticket's own work (subject opens with the key) or says fixes/closes/resolves KS-n.
            # WEAK = a "Refs KS-n" / prose mention: a commit that merely points at the ticket is NOT evidence it was fixed.
            if re.match(r"^\s*(?:(?:KS-\d+)\s*(?:\+|,|&)\s*)*KS-%s\b" % num, subj) or re.search(r"(?i)\b(?:fix(?:es|ed)?|clos(?:e|es|ed)|resolv(?:e|es|ed))\s+KS-%s\b" % num, body):
                own.append(line)
            else:
                ref.append(line)
        if own:
            add("COMMITS", "MENTIONED", "%d commit(s) at develop since the ticket was created are this ticket's own work (subject opens with KS-%s, or says fixes/closes KS-%s), newest: %s" % (len(own), num, num, " || ".join(own[:3])))
        elif ref:
            add("COMMITS", "REFERENCED", "%d commit(s) at develop since the ticket was created only REFER to KS-%s (a Refs/prose mention, not its own work; not evidence it was fixed), newest: %s" % (len(ref), num, " || ".join(ref[:3])))
        else:
            add("COMMITS", "UNMENTIONED", "no commit at develop since the ticket was created mentions KS-%s" % num)
    if dropped:
        add("NOTE", "INFO", "%d more cited path(s)/line(s)/symbol(s) were not checked (per-ticket cap)" % dropped)
    return facts


TOK = re.compile(r"[a-z][a-z0-9]{3,}")
TSTOP = {"that", "this", "with", "from", "when", "should", "have", "does", "into", "ticket", "add", "fix", "make", "will", "your", "only", "also"}


def title_set(t):
    return {w for w in TOK.findall((t or "").lower()) if w not in TSTOP}


def candidates(t, cite_idx, tickets_by_key, mine_paths, mine_syms):
    """Open tickets that share a cited path or symbol, or a close title, with this one. -> [(key, shared_paths, shared_syms, jaccard)]"""
    scores = collections.Counter(); sp = collections.defaultdict(set); ss = collections.defaultdict(set)
    for p in mine_paths:
        for k in cite_idx["path"].get(p, ()):
            if k != t["identifier"]:
                sp[k].add(p); scores[k] += 2
    for s in mine_syms:
        for k in cite_idx["sym"].get(s, ()):
            if k != t["identifier"]:
                ss[k].add(s); scores[k] += 1
    mt = title_set(t.get("title"))
    jac = {}
    for k, o in tickets_by_key.items():
        if k == t["identifier"]:
            continue
        ot = title_set(o.get("title"))
        j = len(mt & ot) / len(mt | ot) if mt and ot else 0.0
        jac[k] = j
        if j >= 0.5:
            scores[k] += 3
    out = []
    for k, sc in scores.most_common():
        j = jac.get(k, 0.0)
        if (len(sp[k]) >= 1 and (len(ss[k]) >= 1 or len(sp[k]) >= 2 or j >= 0.3)) or j >= 0.5:
            out.append((k, sorted(sp[k]), sorted(ss[k]), j))
    return out[:5]


# ------------------------------------------------------------------------------------------ the CHECKER
def reason_tokens(r):
    r2 = re.sub(r"\[?\bF\d+\b\]?", " ", r)
    toks = set(x.strip().rstrip("()") for x in re.findall(r"`([^`]+)`", r2))
    toks |= set(re.findall(r"\bKS-\d+\b", r2))
    toks |= set(m.group(0) for m in re.finditer(r"[\w@.\-]+(?:/[\w@.\-]+)+|[\w\-]+\.%s\b" % EXT, r2))
    toks |= set(re.findall(r"\b\d{2,}\b", r2))
    toks |= set(re.findall(r"\b[0-9a-f]{7,40}\b", r2))
    return {x for x in toks if x}


def check_proposal(raw, facts, key, open_keys, cand_keys, n_citations):
    """-> (ok, normalized dict or None, [refusal reasons]). Pure; no I/O. Every refusal names what failed."""
    errs = []
    if not isinstance(raw, dict):
        return False, None, ["reply is not a JSON object"]
    prop = str(raw.get("proposal") or "").strip().upper()
    dup = raw.get("duplicate_of")
    m = re.match(r"^POSSIBLE-DUPLICATE(?:-OF)?\s*(KS-\d+)?$", prop)
    if m:
        prop = "POSSIBLE-DUPLICATE"
        dup = dup or m.group(1)
    if prop not in CLASSES:
        return False, None, ["proposal %r is not one of %s" % (prop, CLASSES)]
    reason = " ".join(str(raw.get("reason") or "").split())
    if not reason:
        errs.append("empty reason")
    if len(reason) > 400:
        errs.append("reason longer than 400 chars")
    fids = raw.get("fact_ids")
    fids = [str(x) for x in fids] if isinstance(fids, list) else []
    fids = list(dict.fromkeys(fids + re.findall(r"\bF\d+\b", reason)))
    byid = {f["id"]: f for f in facts}
    bad = [x for x in fids if x not in byid]
    if bad:
        errs.append("cites fact id(s) %s that are not in FACTS" % bad)
    cited = [byid[x] for x in fids if x in byid]
    if prop != "CANNOT-TELL" and not cited:
        errs.append("%s must cite at least one fact id" % prop)
    corpus = "\n".join("%s %s %s" % (f["id"], f["status"], f["text"]) for f in facts)
    for tok in sorted(reason_tokens(reason)):
        if tok in corpus:
            continue
        # a slash-joined LIST of symbols (`a/b/c`, no file extension) passes when every part is in FACTS; a path with an extension never gets this
        if "/" in tok and not re.search(r"\.%s$" % EXT, tok) and all(part in corpus for part in tok.split("/") if part):
            continue
        errs.append("reason cites %r which is not in FACTS" % tok)
    sts = {f["status"] for f in cited}
    allst = {f["status"] for f in facts}
    if prop == "STILL-VALID":
        if n_citations == 0:
            errs.append("STILL-VALID with no citations")
        if allst & BADS:
            errs.append("STILL-VALID but FACTS contain %s" % sorted(allst & BADS))
        if cited and not (sts & OKS):
            errs.append("STILL-VALID cites no fact showing a cited thing is present")
        if sts - VALID_CITE - {"INFO"}:
            errs.append("STILL-VALID cites facts with status %s" % sorted(sts - VALID_CITE))
    elif prop == "LIKELY-FIXED":
        if cited and not (sts & FIXED_CITE):
            errs.append("LIKELY-FIXED cites no fact that is missing/absent/changed")
    elif prop == "CITATION-MOVED":
        if cited and not (sts & MOVED_CITE):
            errs.append("CITATION-MOVED cites no fact with a moved/ambiguous/beyond-EOF status")
    elif prop == "POSSIBLE-DUPLICATE":
        d = str(dup or "").strip().upper()
        if not re.match(r"^KS-\d+$", d):
            errs.append("POSSIBLE-DUPLICATE without a KS key")
        elif d == key:
            errs.append("duplicate of itself")
        elif d not in open_keys:
            errs.append("duplicate key %s is not an open ticket" % d)
        elif d not in cand_keys:
            errs.append("duplicate key %s is not a CANDIDATE in FACTS for this ticket" % d)
        elif not any(f["kind"] == "CAND" and d in f["text"] for f in cited):
            errs.append("POSSIBLE-DUPLICATE does not cite the CANDIDATE fact for %s" % d)
        dup = d
    if prop == "CANNOT-TELL":
        dup = None
    return (not errs), {"proposal": prop, "duplicate_of": dup if prop == "POSSIBLE-DUPLICATE" else None, "reason": reason, "fact_ids": fids}, errs


# ------------------------------------------------------------------------------------------ Linear (QUERIES only)
def read_key(envfile):
    try:
        for l in open(envfile):
            if l.startswith("LINEAR_API_KEY="):
                return l.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return None


def gql(key, query, variables=None):
    assert query.lstrip().startswith(("query", "{")), "screen.py sends GraphQL queries only"
    req = urllib.request.Request("https://api.linear.app/graphql", data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": key})
    d = json.load(urllib.request.urlopen(req, timeout=90))
    if d.get("errors"):
        raise RuntimeError("GraphQL errors: " + json.dumps(d["errors"])[:300])
    return d["data"]


def fetch_open(key):
    out, after = [], None
    q = ("query($after:String){issues(first:100, after:$after, filter:{team:{key:{eq:\"KS\"}}, state:{name:{in:%s}}}){"
         "nodes{identifier number title description priority createdAt updatedAt state{name} assignee{name email}} pageInfo{hasNextPage endCursor}}}" % json.dumps(STATES))
    while True:
        d = gql(key, q, {"after": after})["issues"]
        out += d["nodes"]
        if not d["pageInfo"]["hasNextPage"]:
            return out
        after = d["pageInfo"]["endCursor"]


def fetch_comments(key, tickets):
    nums = [t["number"] for t in tickets]
    for i in range(0, len(nums), 25):
        chunk = nums[i:i + 25]
        q = ("query{issues(first:50, filter:{team:{key:{eq:\"KS\"}}, number:{in:%s}}){nodes{identifier comments(first:50){nodes{body createdAt}}}}}" % json.dumps(chunk))
        by = {n["identifier"]: n["comments"]["nodes"] for n in gql(key, q)["issues"]["nodes"]}
        for t in tickets:
            if t["identifier"] in by:
                t["comments"] = sorted(by[t["identifier"]], key=lambda x: x.get("createdAt") or "")[-3:]


def latest_partition():
    """The no-write partition named in the LATEST S-seat record (highest seat number): -> (set of keys, file path)."""
    best = (-1, None)
    try:
        for d in os.listdir(HIST):
            m = re.match(r"^\d{4}-\d{2}-\d{2}_seatS-(\d+)(?:st|nd|rd|th)$", d)
            if m:
                ev = os.path.join(HIST, d, "evidence")
                for f in (os.listdir(ev) if os.path.isdir(ev) else []):
                    if re.match(r"^partition_s\d+\.txt$", f):
                        k = (int(m.group(1)), os.path.join(ev, f))
                        if k > best:
                            best = k
    except OSError:
        pass
    if not best[1]:
        return set(), None
    return {l.strip() for l in open(best[1], encoding="utf-8") if re.match(r"^KS-\d+$", l.strip())}, best[1]


def is_human(t):
    a = t.get("assignee") or {}
    return (a.get("email") or "").lower() in HUMANS or any(h in (a.get("name") or "").lower() for h in HUMAN_NAMES)


# ------------------------------------------------------------------------------------------ repo / develop
def prepare_clone(repo, scratch, no_remote, tip_pin):
    """A --shared, --no-checkout clone of the shared checkout in OUR scratch; develop's sha by ls-remote; fetched INTO THE CLONE only."""
    clone = os.path.join(scratch, "clone")
    if not os.path.isdir(os.path.join(clone, ".git")):
        os.makedirs(scratch, exist_ok=True)
        r = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", repo, clone], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError("clone failed: " + r.stderr.strip()[:200])
        subprocess.run(["git", "-C", clone, "config", "gc.auto", "0"])
    if no_remote:
        sha = git(clone, "rev-parse", "--verify", "-q", "origin/develop").strip() or git(clone, "rev-parse", "--verify", "-q", "develop").strip()
        if not re.match(r"^[0-9a-f]{40}$", sha):
            raise RuntimeError("--no-remote: no develop in the clone")
        return clone, sha, "local develop (no-remote)"
    url = git(repo, "remote", "get-url", "origin").strip()
    if not re.match(r"^(git@|ssh://|https://)", url):
        raise RuntimeError("the shared checkout's origin is not a remote URL (%r): ls-remote would answer from a local path" % url)
    ssh = git(repo, "config", "--get", "core.sshCommand").strip()
    subprocess.run(["git", "-C", clone, "remote", "set-url", "origin", url])
    if ssh:
        subprocess.run(["git", "-C", clone, "config", "core.sshCommand", ssh])
    if tip_pin:
        tip, how = tip_pin, "pinned by the caller"
    else:
        lr = git(repo, "ls-remote", "origin", "refs/heads/develop", timeout=60)
        m = re.search(r"^([0-9a-f]{40})\s+refs/heads/develop$", lr, re.M)
        if not m:
            raise RuntimeError("could not read develop's tip by ls-remote (offline?)")
        tip, how = m.group(1), "git -C <shared checkout> ls-remote origin refs/heads/develop at " + time.strftime("%F %T")
    if subprocess.run(["git", "-C", clone, "cat-file", "-e", tip + "^{commit}"], capture_output=True).returncode:
        r = subprocess.run(["git", "-C", clone, "fetch", "-q", "origin", "develop"], capture_output=True, text=True, timeout=900)
        if r.returncode or subprocess.run(["git", "-C", clone, "cat-file", "-e", tip + "^{commit}"], capture_output=True).returncode:
            raise RuntimeError("develop %s not fetchable into the clone: %s" % (tip[:12], r.stderr.strip()[:200]))
    return clone, tip, how


# ------------------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--out", required=True)
    ap.add_argument("--wait", type=int, default=0, help="seconds to wait for a busy box (nightly: 0 = refuse)")
    ap.add_argument("--update-state", action="store_true")
    ap.add_argument("--keys", default="")
    ap.add_argument("--facts-only", action="store_true")
    ap.add_argument("--fixture")
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("--no-remote", action="store_true")
    ap.add_argument("--tip", default="")
    ap.add_argument("--deadline", default="", help="HH:MM local: stop starting new tickets after this time")
    ap.add_argument("--env", default=DEFAULT_ENV)
    ap.add_argument("--partition-file", default="")
    ap.add_argument("--scratch", default=os.path.join(HERE, "scratch"))
    ap.add_argument("--state-file", default=os.path.join(HERE, "state", "screened.tsv"))
    a = ap.parse_args()
    t_start = time.time()

    # 0. box gate FIRST (cheap): refuse cleanly before any work when the Spark is not usable
    if not a.facts_only and not os.environ.get("SCREEN_SPARK_STUB"):
        st, why = box_state()
        if st != "ok" and a.wait == 0:
            log("REFUSED (%s): %s - no tickets screened, nothing written, exit 0" % (st, why))
            return 0
        if st == "down":
            log("REFUSED (down): %s - no tickets screened, nothing written, exit 0" % why)
            return 0

    os.makedirs(a.out, exist_ok=True)
    # 1. board (read-only queries) or fixture
    try:
        if a.fixture:
            tickets = json.load(open(a.fixture))
            key = None
        else:
            key = read_key(a.env)
            if not key:
                log("HARNESS: no LINEAR_API_KEY readable from the env file; cannot read the board"); return 2
            tickets = fetch_open(key)
    except Exception as e:  # never echo the key
        log("HARNESS: cannot read the board: %s" % type(e).__name__, str(e)[:200]); return 2
    open_all = {t["identifier"]: t for t in tickets}
    part, part_file = (set(), None)
    if a.partition_file:
        part, part_file = {l.strip() for l in open(a.partition_file) if re.match(r"^KS-\d+$", l.strip())}, a.partition_file
    elif not a.fixture:
        part, part_file = latest_partition()
    skipped = collections.Counter()
    elig = []
    for t in tickets:
        k = t["identifier"]
        if is_human(t):
            skipped["assigned to Peter/Stuart"] += 1
        elif k in part:
            skipped["no-write partition"] += 1
        else:
            elig.append(t)
    # 2. selection: explicit keys, else never-screened first then least-recently-screened, stalest updatedAt first
    scr = {}
    if os.path.isfile(a.state_file):
        for l in open(a.state_file):
            p = l.rstrip("\n").split("\t")
            if len(p) >= 2:
                scr[p[0]] = float(p[1])
    if a.keys:
        want = [k.strip() for k in a.keys.split(",") if k.strip()]
        sel = [open_all[k] for k in want if k in open_all and k in {e["identifier"] for e in elig}]
        for k in want:
            if k not in open_all:
                log("note: %s is not an open ticket; skipped" % k)
    else:
        sel = sorted(elig, key=lambda t: (scr.get(t["identifier"], 0.0), t.get("updatedAt") or ""))[:a.limit]
    if key and sel:
        try:
            fetch_comments(key, sel)
        except Exception as e:
            log("note: comments not fetched (%s); screening on title+description" % type(e).__name__)
    # 3. develop
    try:
        clone, tip, how = prepare_clone(a.repo, a.scratch, a.no_remote, a.tip)
        tree = Tree(clone, tip)
    except Exception as e:
        log("HARNESS: cannot resolve develop:", str(e)[:300]); return 2
    log("develop %s (%s); %d tree files; %d open KS tickets read, %d eligible, %d selected" % (tip[:12], how, len(tree.files), len(tickets), len(elig), len(sel)))

    # citation index over ALL open tickets (for duplicate candidates)
    cite_idx = {"path": collections.defaultdict(set), "sym": collections.defaultdict(set)}
    cites = {}
    for t in tickets:
        txt = "%s\n%s" % (t.get("title") or "", t.get("description") or "")
        ps, ss, dr = extract_citations(txt)
        cites[t["identifier"]] = (ps, ss, dr)
        for p in {x[0] for x in ps}:
            cite_idx["path"][p].add(t["identifier"])
        for s in ss:
            cite_idx["sym"][s].add(t["identifier"])

    # 4. per ticket
    tsv = os.path.join(a.out, "proposals.tsv")
    os.makedirs(os.path.join(a.out, "facts"), exist_ok=True); os.makedirs(os.path.join(a.out, "spark"), exist_ok=True)
    fh = open(tsv, "w", encoding="utf-8")
    fh.write("key\tproposal\treason\tfacts_hash\tchecker\tsource\tspark_s\n")
    counts = collections.Counter(); rows = []; consecutive_fail = 0; spark_s = 0.0; aborted = ""
    for t in sel:
        k = t["identifier"]
        if a.deadline:
            hh, mm = map(int, a.deadline.split(":"))
            n = datetime.now()
            if (n.hour, n.minute) >= (hh, mm) and (n.hour, n.minute) < (12, 0):
                aborted = "deadline %s reached after %d tickets" % (a.deadline, len(rows)); break
        t["_tip"] = tip
        # the citations used for FACTS come from title + description + the newest comments the Spark is shown
        txt = "%s\n%s\n%s" % (t.get("title") or "", t.get("description") or "", "\n".join(c.get("body") or "" for c in (t.get("comments") or [])))
        ps, ss, dr = extract_citations(txt)
        facts = build_facts(t, tree, ps, ss, dr)
        cl = candidates(t, cite_idx, open_all, {x[0] for x in ps}, set(ss))
        for ck, sp_, ss_, j in cl:
            o = open_all[ck]
            facts.append({"id": "F%d" % (len(facts) + 1), "kind": "CAND", "status": "CANDIDATE",
                          "text": "open ticket %s [%s] \"%s\" shares paths %s symbols %s title-similarity %.2f"
                                  % (ck, o["state"]["name"], trunc(o.get("title") or "", 90), sp_ or "none", ss_ or "none", j)})
        fhash = hashlib.sha256(json.dumps([[f["kind"], f["status"], f["text"]] for f in facts], sort_keys=True).encode()).hexdigest()[:12]
        json.dump({"key": k, "tip": tip, "facts": facts, "facts_hash": fhash}, open(os.path.join(a.out, "facts", k + ".json"), "w"), indent=1)
        ncite = len(ps) + len(ss)
        cand_keys = {c[0] for c in cl}
        prop, reason, checker, source, secs = "NOT-RUN", "", "", "", 0.0
        if a.facts_only:
            prop, source, reason = "NOT-RUN", "facts-only", "facts extracted; Spark not asked"
        elif ncite == 0 and not cand_keys and not any(f["status"] == "MENTIONED" for f in facts):
            prop, source, checker, reason = "CANNOT-TELL", "rule", "n/a", "no code citations, no candidate duplicate and no commit mentioning the key were found (decided by the extractor, Spark not asked)"
        else:
            ok, why = (True, "") if os.environ.get("SCREEN_SPARK_STUB") else wait_box(a.wait, k)
            if not ok:
                aborted = "box not available mid-run: %s" % why; break
            try:
                try:
                    text, secs = spark_call(k, build_prompt(t, facts))
                finally:
                    BOX.release()
                spark_s += secs
                open(os.path.join(a.out, "spark", k + ".txt"), "w").write(text)
                consecutive_fail = 0
                try:
                    obj = extract_json(text)
                except Exception as e:
                    obj = None; errs = ["unparseable reply: %s" % type(e).__name__]
                    ok_c, norm = False, None
                else:
                    ok_c, norm, errs = check_proposal(obj, facts, k, set(open_all), cand_keys, ncite)
                if ok_c:
                    prop = norm["proposal"] + (" " + norm["duplicate_of"] if norm["duplicate_of"] else "")
                    bs = sorted({f["status"] for f in facts if f["id"] in norm["fact_ids"]})
                    reason, checker, source = norm["reason"], "PASS basis=" + ",".join(bs), "spark"
                else:
                    prop = "REFUSED"
                    first = (norm or {}).get("proposal") or (str((obj or {}).get("proposal")) if isinstance(obj, dict) else "?")
                    reason = "checker refused the Spark's %s: %s" % (first, "; ".join(errs))[:600]
                    checker, source = "REFUSED", "spark"
            except Exception as e:
                consecutive_fail += 1
                prop, reason, checker, source = "ERROR", "Spark request failed: %s" % type(e).__name__, "n/a", "spark"
                if consecutive_fail >= 3:
                    aborted = "Spark failed 3 requests in a row (%s); stopping, exit 0" % type(e).__name__
        counts[prop.split(" ")[0]] += 1
        rows.append((k, prop, reason, fhash, checker, source, secs))
        fh.write("%s\t%s\t%s\t%s\t%s\t%s\t%.1f\n" % (k, prop, reason.replace("\t", " ").replace("\n", " "), fhash, checker, source, secs)); fh.flush()
        log("%s -> %s (%s)" % (k, prop, trunc(reason, 100)))
        if a.update_state and prop not in ("ERROR", "NOT-RUN"):
            os.makedirs(os.path.dirname(a.state_file), exist_ok=True)
            open(a.state_file, "a").write("%s\t%d\t%s\n" % (k, time.time(), fhash))
        if aborted:
            break
    fh.close()
    # 5. report.md (BLUF first)
    total = len(rows)
    ordc = ["STILL-VALID", "LIKELY-FIXED", "CITATION-MOVED", "POSSIBLE-DUPLICATE-OF", "CANNOT-TELL", "REFUSED", "ERROR", "NOT-RUN"]
    cc = {c: counts.get(c if c != "POSSIBLE-DUPLICATE-OF" else "POSSIBLE-DUPLICATE", 0) for c in ordc}
    L = ["# Stale-ticket screen %s" % time.strftime("%Y-%m-%d %H:%M"), ""]
    L.append("**BLUF:** %d of %d selected open KS ticket(s) screened against develop `%s`: %s. PROPOSALS ONLY; nothing was written to Linear or any checkout. A Claude board seat confirms before any board change.%s"
             % (total, len(sel), tip[:12], ", ".join("%s %d" % (c, n) for c, n in cc.items() if n) or "none", ("\n\n**Stopped early:** " + aborted) if aborted else ""))
    L += ["", "## Counts per class", "", "| class | tickets |", "|---|---|"] + ["| %s | %d |" % (c, cc[c]) for c in ordc]
    L += ["", "## Scope", "", "- open KS tickets read from the board (Backlog/Todo/In Progress, paginated to the end): %d" % len(tickets),
          "- skipped: %s" % (", ".join("%s %d" % (k_, v) for k_, v in skipped.items()) or "none"),
          "- no-write partition used: `%s` (%d keys)" % (part_file or "none", len(part)),
          "- develop: `%s` (%s)" % (tip, how), "- Spark wall-clock total: %.0f s over %d request(s) made" % (spark_s, sum(1 for r in rows if r[5] == "spark" and r[1] != "ERROR")),
          "- run time: %.0f s" % (time.time() - t_start), "", "## Proposals", "", "| key | proposal | reason | facts-hash |", "|---|---|---|---|"]
    for r in rows:
        L.append("| %s | %s | %s | `%s` |" % (r[0], r[1], r[2].replace("|", "/")[:260], r[3]))
    open(os.path.join(a.out, "report.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    log("done: %d screened; %s%s" % (total, dict(counts), "; STOPPED: " + aborted if aborted else ""))
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    finally:
        BOX.release()
    sys.exit(rc)
