#!/bin/bash
# build_comment_input.sh <KS-id> <out input.json> <brief.md> product=<repo path> [ctx=<n>]
#
# Builds ONE comment_patch input (tasks/comment_patch/): a comment/docblock-only edit to ONE .ts/.tsx/.js/.mjs/.cjs file,
# graded by token equivalence instead of a red cell (HARNESS_WIDEN_PROPOSAL_2026-09-17b §3; built 2026-09-17 19:4x).
# The KS id may carry a suffix (`KS-1118-F3a`); the Linear number is its first digits.
#
# THE BRIEF (Wednesday writes; night/briefs/<id>.md):
#   ## Premises (measured)   — bullets; EVERY bullet names its instrument (`instrument:`)
#   ## Lines                 — one bullet per range: `- <repo path>:171-174` (or `- :171-174` when the fence names one file)
#   ## The exact change      — ONE ```diff fence, git-apply shaped: `--- a/<path>` / `+++ b/<path>` / `@@ -N,n +M,m @@`.
#                              The hunk header KEYS every '-' line to its tip line number. This fence is the golden.
# REFUSES (rc 2, each naming why), before anything is written:
#   R0  no `## Premises (measured)`, or a premise bullet with no `instrument:`
#   R1  product= is not .ts/.tsx/.js/.mjs/.cjs under services/*/src, packages/shared/src or scripts/ (Blockchain/Dev/…)
#   R2  the tip object is not local and there is no verified override (G6, the sibling builders' block)
#   R3  no `## Lines` range for the product, a range outside the file, or no fence section for the product
#   R4  a tip line inside a named range carries a code token (part code, part comment is refused: a brief cannot hide
#       a code edit) — measured by tasks/comment_patch/token_equiv.cjs, never a regex
#   R5  a '-' or context line is not the tip's line at its hunk-keyed number; a '-' line not BYTE-UNIQUE at the tip;
#       a '-' line outside the named ranges
#   R6  a '+' line carries non-ASCII (rule of 2026-09-17 11:00)
#   R7  a '+' line byte-identical to a '-' line in its hunk (context-as-addition), or already present at the tip (C7
#       could not prove it), or not a COMMENT line in the golden result (a code token touches it)
#   R8  golden self-check: the brief's own diff applied to the tip must PASS C4, C4b, C5, C6, C7
#   R9  a READY diff (night/READY_*) hunks the product file within 10 lines of a named range
#   R10 the Linear ticket is archived, not Backlog/Todo, assigned to Peter/Stuart, or attached to an OPEN PR (the
#       build_input.sh gates, mirrored; the key by NAME from the Secuura .env, no Bearer prefix; fail closed)
#   R11 an OPEN GitHub PR changes the product file (REST GET pulls?state=open + pulls/<n>/files, GH_TOKEN by NAME;
#       fail closed)
# Seams (tests only): NIGHT_LINEAR_API, NIGHT_GITHUB_API (http/https only), NIGHT_READY_DIR, NIGHT_SOURCE_CHECKOUT,
# NIGHT_SECUURA_ENV. Never writes anywhere but <out>; git READ verbs only on the source checkout. rc 0 ok · 2 refused · 1 error.
set -uo pipefail
ID="${1:-}"; OUT="${2:-}"; BRIEF="${3:-}"; shift 3 2>/dev/null
[ -n "$ID" ] && [ -n "$OUT" ] && [ -f "$BRIEF" ] || { echo "usage: build_comment_input.sh <KS-id> <out> <brief.md> product=<path> [ctx=N]" >&2; exit 1; }
case "$ID" in KS-[0-9]*) ;; *) echo "build_comment_input: not a KS id: $ID" >&2; exit 1 ;; esac
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM_DIR="$(cd -P "$SELF_DIR/.." && pwd)"
SRC="${NIGHT_SOURCE_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
ENV_FILE="${NIGHT_SECUURA_ENV:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env}"
[ -d "$SRC/.git" ] || { echo "build_comment_input: source checkout missing at $SRC" >&2; exit 1; }
TIP="$(git -C "$SRC" ls-remote origin refs/heads/develop 2>/dev/null | awk '{print $1}')"
[ -n "$TIP" ] || { echo "build_comment_input: ls-remote returned nothing" >&2; exit 1; }
if [ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" != "commit" ]; then
  OV="$SELF_DIR/tip_override.txt"; OV_SHA=""; OV_AGAINST=""
  [ -f "$OV" ] && read -r OV_SHA OV_AGAINST OV_REST < "$OV"
  if [ -n "$OV_SHA" ] && [ "$OV_AGAINST" = "$TIP" ] && [ "$(git -C "$SRC" cat-file -t "$OV_SHA" 2>/dev/null)" = "commit" ]; then
    echo "build_comment_input: G6 — origin develop $TIP is not local; using VERIFIED OVERRIDE $OV_SHA ($OV_REST)" >&2; TIP="$OV_SHA"
  else
    echo "build_comment_input: REFUSED R2 — tip $TIP not local and no valid override (no fetch from here)" >&2; exit 2
  fi
fi
NIGHT_READY_DIR="${NIGHT_READY_DIR:-$SELF_DIR}" CP_DIR="$LM_DIR/tasks/comment_patch" ENV_FILE="$ENV_FILE" \
python3 - "$ID" "$OUT" "$BRIEF" "$SRC" "$TIP" "$@" <<'PY'
import glob, json, os, re, subprocess, sys, tempfile, urllib.request
ident, out, brief_path, src, tip = sys.argv[1:6]
pins = dict(a.split("=", 1) for a in sys.argv[6:] if "=" in a)
CP_DIR = os.environ["CP_DIR"]; sys.path.insert(0, CP_DIR)
import cp_gates as G

def refuse(code, msg):
    sys.stderr.write(f"build_comment_input: REFUSED {code} {ident} — {msg}\n"); sys.exit(2)

prod = pins.get("product") or refuse("R1", "product= is required")
# ---- R1 the class of file
if not re.match(r"^Blockchain/Dev/(services/[A-Za-z0-9_\-]+/src|packages/shared/src|scripts)/[A-Za-z0-9_\-./]+\.(ts|tsx|js|mjs|cjs)$", prod) or prod.endswith(".d.ts"):
    refuse("R1", f"{prod} is not a .ts/.tsx/.js/.mjs/.cjs under Blockchain/Dev/services/*/src, packages/shared/src or scripts/ (markdown -> doc_patch, shell -> bash_patch)")
r = subprocess.run(["git", "-C", src, "show", f"{tip}:{prod}"], capture_output=True, text=True)
if r.returncode:
    refuse("R3", f"{prod} is not at the tip {tip[:9]}")
tip_text = r.stdout
tip_lines = G.split_lines(tip_text)
text = open(brief_path, encoding="utf-8").read()

# ---- R0 premises
prem = G.section(text, r"Premises \(measured\)")
if prem is None:
    refuse("R0", "the brief has no `## Premises (measured)` section — a comment edit asserts facts; each needs its measure")
bullets = [l.strip() for l in prem.split("\n") if re.match(r"^\s*[-*]\s+\S", l)]
if not bullets:
    refuse("R0", "`## Premises (measured)` has no bullet")
noinst = [b for b in bullets if not re.search(r"instrument:", b, re.I)]
if noinst:
    refuse("R0", f"{len(noinst)} premise bullet(s) name no `instrument:` — first: {noinst[0][:100]!r}")

# ---- R3 lines + fence section
lines_sec = G.section(text, r"Lines\b")
if lines_sec is None:
    refuse("R3", "the brief has no `## Lines` section")
ch = G.section(text, r"The exact change\b")
fences = re.findall(r"^```diff[^\n]*\n(.*?)^```", ch or "", re.M | re.S)
if len(fences) != 1:
    refuse("R3", f"`## The exact change` must carry exactly ONE ```diff fence (found {len(fences)})")
secs = G.parse_diff_sections(fences[0])
files_in_fence = sorted({s["plus_path"] for s in secs})
mine = [s for s in secs if s["plus_path"] == prod]
if len(mine) != 1 or mine[0]["minus_path"] != prod:
    refuse("R3", f"the fence has {len(mine)} section(s) for {prod} with matching ---/+++ headers (fence files: {files_in_fence})")
hunks = mine[0]["hunks"]
if not hunks:
    refuse("R3", f"the fence section for {prod} has no @@ hunk")
ranges = []
for l in lines_sec.split("\n"):
    m = re.match(r"^\s*[-*]\s+`?([^`\s:]*)`?:(\d+)(?:-(\d+))?\b", l)
    if not m:
        continue
    p, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
    if p == "" and len(files_in_fence) != 1:
        refuse("R3", f"`## Lines` bullet {l.strip()!r} names no file, and the fence carries {len(files_in_fence)} files")
    if p in ("", prod):
        if a < 1 or b < a or b > len(tip_lines):
            refuse("R3", f"range :{a}-{b} falls outside {prod} ({len(tip_lines)} lines at the tip)")
        ranges.append((a, b))
if not ranges:
    refuse("R3", f"`## Lines` names no range for {prod}")

# ---- R4 the class predicate: every tip line in a range is comment/blank only
ts_dir = os.path.join(src, "Blockchain/Dev/node_modules/typescript")
tmp = tempfile.mkdtemp(prefix="cp_build_")
before_p = os.path.join(tmp, "before" + os.path.splitext(prod)[1]); open(before_p, "w", encoding="utf-8").write(tip_text)
jl, err = G.node_json(["lines", ts_dir, before_p, os.path.basename(prod)])
if jl is None:
    sys.stderr.write(f"build_comment_input: token instrument error on the tip file: {err}\n"); sys.exit(1)
code_lines = set(jl["code_lines"])
hot = [n for a, b in ranges for n in range(a, b + 1) if n in code_lines]
if hot:
    refuse("R4", f"tip line(s) {hot[:5]} inside the named ranges carry a CODE token (e.g. :{hot[0]} {tip_lines[hot[0]-1].strip()[:70]!r}) — a comment_patch range holds comment/blank lines only")

# ---- R5 / R6 / R7 on the fence
after, minus, plus, err = G.strict_apply(tip_lines, hunks)
if err:
    refuse("R5", f"the brief's own diff does not apply to the tip strictly: {err}")
for m_ in minus:
    if not any(a <= m_["line"] <= b for a, b in ranges):
        refuse("R5", f"'-' line :{m_['line']} ({m_['text'][:60]!r}) is outside the named ranges")
    cnt = tip_lines.count(m_["text"])
    if cnt != 1:
        refuse("R5", f"'-' line :{m_['line']} ({m_['text'][:60]!r}) is not byte-unique at the tip ({cnt} copies) — C6 could not prove its removal")
nonascii = [p["text"] for p in plus if any(ord(c) > 127 for c in p["text"])]
if nonascii:
    refuse("R6", f"{len(nonascii)} '+' line(s) carry non-ASCII (write -- for an em dash, -> for an arrow): {nonascii[0][:70]!r}")
for p in plus:
    if any(m_["hunk"] == p["hunk"] and m_["text"] == p["text"] for m_ in minus):
        refuse("R7", f"'+' line {p['text'][:60]!r} is byte-identical to a '-' line in its hunk (context written as an edit)")
    if p["text"] in tip_lines:
        refuse("R7", f"'+' line {p['text'][:60]!r} already exists at the tip — C7 could not prove it was added; keep that line as context")
after_p = os.path.join(tmp, "after" + os.path.splitext(prod)[1]); open(after_p, "w", encoding="utf-8").write("\n".join(after) + "\n")
ja, err = G.node_json(["lines", ts_dir, after_p, os.path.basename(prod)])
if ja is None:
    refuse("R8", f"the brief's own result cannot be measured: {err}")
codey = [p for p in plus if p["after_line"] in set(ja["code_lines"])]
if codey:
    refuse("R7", f"'+' line {codey[0]['text'][:70]!r} is not a comment line in the result (a code token touches result line {codey[0]['after_line']})")

# ---- R8 golden self-check through the checker's own gates
must_remove = [{"line": m_["line"], "text": m_["text"]} for m_ in minus if m_["text"] not in {p["text"] for p in plus}]
expected_plus = [p["text"] for p in plus]
res = G.run_gates(before_p, after_p, ts_dir, os.path.basename(prod), ranges, must_remove, expected_plus)
bad = [f"{g} {msg}" for st, g, msg in res if st == "FAIL"]
if bad:
    refuse("R8", f"the brief's own diff fails its gates: {bad[0][:300]}")

# ---- R9 READY hunks near a range
ready_dir = os.environ["NIGHT_READY_DIR"]
near, touching = [], []
for rf in sorted(glob.glob(os.path.join(ready_dir, "READY_*"))):
    cur = None
    for ln in open(rf, encoding="utf-8", errors="replace").read().split("\n"):
        mh = re.match(r"^\+\+\+ (?:b/)?(\S+)", ln)
        if mh:
            cur = mh.group(1); continue
        mm = re.match(r"^@@ -(\d+)(?:,(\d+))?", ln)
        if mm and cur and (cur == prod or prod.endswith("/" + cur) or cur.endswith("/" + prod.split("Blockchain/Dev/", 1)[-1])):
            s0 = int(mm.group(1)); e0 = s0 + max(int(mm.group(2) or 1), 1) - 1
            touching.append(os.path.basename(rf))
            if any(s0 <= b + 10 and e0 >= a - 10 for a, b in ranges):
                near.append(f"{os.path.basename(rf)} @@ -{s0},{e0 - s0 + 1}")
if near:
    refuse("R9", f"READY diff(s) hunk {prod} within 10 lines of a named range: {near[:3]}")
print(f"R9 READY scan: {len(glob.glob(os.path.join(ready_dir, 'READY_*')))} READY files; hunks in this file: {sorted(set(touching)) or 'none'} (none within 10 lines of a range)")

# ---- R10 / R11 network gates (fail closed)
env = {}
for l in open(os.environ["ENV_FILE"], encoding="utf-8"):
    mm = re.match(r"^\s*(?:export\s+)?([A-Z_][A-Z0-9_]*)=(.*)$", l.rstrip("\n"))
    if mm:
        env[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
lin_api = os.environ.get("NIGHT_LINEAR_API", "https://api.linear.app/graphql")
gh_api = os.environ.get("NIGHT_GITHUB_API", "https://api.github.com").rstrip("/")
for nm, u in (("NIGHT_LINEAR_API", lin_api), ("NIGHT_GITHUB_API", gh_api)):
    if not re.match(r"^https?://", u):
        refuse("R10", f"{nm} is not an http(s) URL — the state cannot be read (fail closed)")
lkey = env.get("LINEAR_API_KEY") or refuse("R10", "LINEAR_API_KEY unset in the Secuura .env — the ticket state cannot be read (fail closed)")
gtok = env.get("GH_TOKEN") or refuse("R11", "GH_TOKEN unset in the Secuura .env — open PRs cannot be read (fail closed)")
number = int(re.match(r"^KS-(\d+)", ident).group(1))
Q = '''query($n:Float){ issues(first:2, includeArchived:true, filter:{ team:{key:{eq:"KS"}}, number:{eq:$n} }){
  nodes{ identifier title archivedAt state{name type} assignee{email} attachments{nodes{url}} } } }'''
try:
    rq = urllib.request.Request(lin_api, data=json.dumps({"query": Q, "variables": {"n": number}}).encode(),
                                headers={"Content-Type": "application/json", "Authorization": lkey, "User-Agent": "wednesday-build-comment-input"})
    with urllib.request.urlopen(rq, timeout=60) as f:
        lj = json.loads(f.read())
    nodes = lj["data"]["issues"]["nodes"]
except Exception as e:
    refuse("R10", f"Linear could not be read ({type(e).__name__}: {str(e)[:160]}) — fail closed")
if len(nodes) != 1:
    refuse("R10", f"Linear returned {len(nodes)} issues for KS-{number}")
n = nodes[0]
state, stype = n["state"]["name"], n["state"]["type"]
assignee = (n.get("assignee") or {}).get("email") or ""
print(f"ticket {n['identifier']} · {state} ({stype}) · assignee={assignee or '-'} · {n['title'][:90]!r}")
if n.get("archivedAt"):
    refuse("R10", f"archived at {n['archivedAt']}")
if stype not in ("backlog", "unstarted"):
    refuse("R10", f"state is {state} ({stype}) — not Backlog/Todo; a seat has it")
if any(x in assignee for x in ("peter", "stuart")):
    refuse("R10", f"assigned to {assignee} (Peter/Stuart tickets are off-limits)")
def gh(path):
    rq = urllib.request.Request(gh_api + path, headers={"Authorization": "Bearer " + gtok, "Accept": "application/vnd.github+json",
                                "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "wednesday-build-comment-input"})
    with urllib.request.urlopen(rq, timeout=30) as f:
        return json.loads(f.read())
murl = subprocess.run(["git", "-C", src, "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
mo = re.search(r"github\.com[:/]([A-Za-z0-9_.\-]+)/([A-Za-z0-9_.\-]+?)(?:\.git)?$", murl)
if not mo:
    refuse("R11", "the source checkout's origin is not a github.com URL — open PRs cannot be read (fail closed)")
owner, repo = mo.groups()
for u in [a["url"] for a in n["attachments"]["nodes"] if "/pull/" in (a.get("url") or "")]:
    mp = re.match(r"^https?://github\.com/([A-Za-z0-9_.\-]+)/([A-Za-z0-9_.\-]+)/pull/(\d+)", u)
    if not mp:
        refuse("R10", f"attached PR URL {u!r} is not a github.com pull URL (fail closed)")
    try:
        pj = gh(f"/repos/{mp.group(1)}/{mp.group(2)}/pulls/{mp.group(3)}"); st = pj["state"]
    except Exception as e:
        refuse("R10", f"attached PR #{mp.group(3)}: state unreadable ({type(e).__name__}) — fail closed")
    print(f"attached PR #{mp.group(3)}: {st}{' (merged)' if pj.get('merged') else ''}")
    if st == "open":
        refuse("R10", f"attached to OPEN pull request #{mp.group(3)} — a lane has it")
try:
    open_prs, page = [], 1
    while True:
        batch = gh(f"/repos/{owner}/{repo}/pulls?state=open&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError(f"pulls list is not a list: {str(batch)[:100]}")
        open_prs += batch
        if len(batch) < 100:
            break
        page += 1
    hits = []
    for pr in open_prs:
        fpage = 1
        while True:
            fl = gh(f"/repos/{owner}/{repo}/pulls/{pr['number']}/files?per_page=100&page={fpage}")
            if not isinstance(fl, list):
                raise ValueError(f"files of #{pr['number']} is not a list")
            if any(f.get("filename") == prod or f.get("previous_filename") == prod for f in fl):
                hits.append(f"#{pr['number']}")
            if len(fl) < 100:
                break
            fpage += 1
except Exception as e:
    refuse("R11", f"open PRs could not be read ({type(e).__name__}: {str(e)[:160]}) — fail closed")
if hits:
    refuse("R11", f"OPEN pull request(s) {hits} change {prod} — a lane holds the file")
print(f"R11 open PRs: {len(open_prs)} open on {owner}/{repo}; none changes {prod}")

inp = {"ticket": {"identifier": ident, "title": text.splitlines()[0].lstrip("# ").strip()[:200], "description": text},
       "repo": {"source_checkout": src, "tip": tip, "branch": "develop"},
       "task_type": "comment_patch", "product_file": prod, "repo_subdir": "Blockchain/Dev",
       "comment": {"ranges": ranges, "must_remove": must_remove, "expected_plus": expected_plus,
                   "brief_diff": "--- a/%s\n+++ b/%s\n" % (prod, prod) + "\n".join(
                       "@@ -%d,%d +%d,%d @@\n" % (h["old_start"], h["old_len"], h["new_start"], h["new_len"]) + "\n".join(h["body"]) for h in hunks) + "\n"},
       "files": {prod: tip_text},
       "tip": tip}
if "ctx" in pins:
    inp["_night_num_ctx"] = int(pins["ctx"])
json.dump(inp, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"R8 golden self-check: " + " · ".join(f"{st} {g}" for st, g, _ in res))
print(f"wrote {out}: {prod} ({len(tip_text)} B at {tip[:9]}), ranges {ranges}, '-' {len(must_remove)}, '+' {len(expected_plus)}")
PY
