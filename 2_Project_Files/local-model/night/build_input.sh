#!/bin/bash
# build_input.sh <KS-id> <out input.json> [product=<repo path>] [ref=<repo path>] [line=<n>] [ctx=<n>]
#
# Builds ONE `code_patch` input.json for a Secuura KS ticket, the way the KS-871
# input was built by hand on 2026-09-14 (runs/2026-09-14_ks871-gptoss120b/BUILD_REPORT.md
# §HOW step 2), as a script so the night runner can do it unattended:
#
#   1. read the ticket from Linear (READ-ONLY GraphQL; the key is sourced from the
#      Secuura project's 4_Credentials/.env and never printed),
#   2. pin `tip` = origin/develop from `git ls-remote` (no fetch — a fetch is a write
#      verb on the source checkout; if the object is not local, refuse),
#   3. `git show <tip>:<path>` for the ONE product file and ONE reference test,
#   4. emit the contract-shaped JSON (same key set as the KS-806/KS-871 inputs).
#
# REFUSES (rc 2, reason printed) when the ticket does not fit the contract:
#   - archived, not Backlog/Todo (a lane took it), assigned to Peter/Stuart, or
#     attached to a GitHub pull request;
#   - names MORE than one product file (unless `product=` pins one) or NONE;
#   - has no fix shape (no "Fix shape" / "Recommendation" / "Fix:" / "Acceptance"
#     section) — a ticket that asks a question is a ruling, not a task;
#   - the service is not on vitest (the checker runs `npx vitest run`; originate and
#     governance are jest) — or is not a services/* | packages/shared path;
#   - no in-process test under the service's src/__tests__ imports the product
#     module (nothing to copy the mock shape from) — unless `ref=` pins one;
#   - no defect line can be found (`<file>:NNN` in the ticket, or `line=`).
#
# Never writes anywhere but <out>. Never touches the source checkout (git READ
# verbs only: ls-remote, cat-file, show, ls-tree). rc 0 ok · 2 refused · 1 error.
# stderr never discarded. bash 3.2 + python3.
set -uo pipefail

TICKET="${1:-}"; OUT="${2:-}"; shift 2 2>/dev/null
if [ -z "$TICKET" ] || [ -z "$OUT" ]; then
  echo "usage: build_input.sh <KS-id> <out input.json> [product=..] [ref=..] [line=N] [ctx=N]" >&2
  exit 1
fi
case "$TICKET" in KS-[0-9]*) ;; *) echo "build_input: not a KS id: $TICKET" >&2; exit 1 ;; esac

SRC="${NIGHT_SOURCE_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
ENV_FILE="${NIGHT_SECUURA_ENV:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env}"
REPO_SUBDIR="Blockchain/Dev"

if [ ! -f "$ENV_FILE" ]; then echo "build_input: Secuura .env missing at $ENV_FILE" >&2; exit 1; fi
set -a; source "$ENV_FILE"; set +a
if [ -z "${LINEAR_API_KEY:-}" ]; then echo "build_input: LINEAR_API_KEY unset in $ENV_FILE" >&2; exit 1; fi
if [ ! -d "$SRC/.git" ]; then echo "build_input: source checkout missing at $SRC" >&2; exit 1; fi

# --- tip: origin/develop by ls-remote, object must already be local (no fetch) ---
TIP="$(git -C "$SRC" ls-remote origin refs/heads/develop 2>/dev/null | awk '{print $1}')"
if [ -z "$TIP" ]; then echo "build_input: ls-remote origin develop returned nothing (offline?)" >&2; exit 1; fi
if [ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" != "commit" ]; then
  echo "build_input: REFUSED — develop tip $TIP is not in the local object store; a fetch is a write verb on the source checkout, so a Secuura seat must fetch first" >&2
  exit 2
fi

# Everything else is Python: the Linear read, the parse, the JSON emit.
python3 - "$TICKET" "$OUT" "$SRC" "$TIP" "$REPO_SUBDIR" "$@" <<'PYEOF'
import json, os, re, subprocess, sys, urllib.request

ticket, out, src, tip, subdir = sys.argv[1:6]
pins = {}
for a in sys.argv[6:]:
    if "=" in a:
        k, v = a.split("=", 1); pins[k] = v
number = int(ticket.split("-")[1])
key = os.environ["LINEAR_API_KEY"]

def refuse(msg):
    sys.stderr.write(f"build_input: REFUSED {ticket} — {msg}\n"); sys.exit(2)
def git(*args):
    return subprocess.run(["git", "-C", src, *args], capture_output=True, text=True)

# ---------------------------------------------------------------- 1. Linear read
Q = '''query($n:Float){ issues(first:2, includeArchived:true,
  filter:{ team:{key:{eq:"KS"}}, number:{eq:$n} }){
  nodes{ id identifier title description priorityLabel archivedAt updatedAt
    state{name type} assignee{name email} attachments{nodes{url title}} } } }'''
req = urllib.request.Request("https://api.linear.app/graphql",
    data=json.dumps({"query": Q, "variables": {"n": number}}).encode(),
    headers={"Content-Type": "application/json", "Authorization": key})
with urllib.request.urlopen(req, timeout=60) as r:
    j = json.loads(r.read())
if "errors" in j:
    sys.stderr.write(f"build_input: Linear error: {j['errors']}\n"); sys.exit(1)
nodes = j["data"]["issues"]["nodes"]
if len(nodes) != 1:
    refuse(f"Linear returned {len(nodes)} issues for number {number}")
n = nodes[0]
desc = n["description"] or ""
state, stype = n["state"]["name"], n["state"]["type"]
assignee = (n["assignee"] or {}).get("email") or ""
print(f"ticket {n['identifier']} · {state} ({stype}) · {n['priorityLabel']} · assignee={assignee or '-'} · updated {n['updatedAt']}")
if n["archivedAt"]:
    refuse(f"archived at {n['archivedAt']}")
if stype not in ("backlog", "unstarted"):
    refuse(f"state is {state} ({stype}) — not Backlog/Todo; a seat has it")
if any(x in assignee for x in ("peter", "stuart")):
    refuse(f"assigned to {assignee} (Peter/Stuart tickets are off-limits)")
prs = [a["url"] for a in n["attachments"]["nodes"] if "/pull/" in (a["url"] or "")]
if prs:
    refuse(f"attached to pull request(s): {prs}")

# ---------------------------------------------------------------- 2. product file
PATH_RE = re.compile(r"(?:Blockchain/Dev/)?((?:services/[a-z0-9\-]+|packages/shared)/src/[A-Za-z0-9_\-./]+\.ts)(?::(\d+))?")
cands = []
for m in PATH_RE.finditer(desc):
    p = m.group(1)
    if "__tests__" in p or p.endswith(".test.ts"): continue
    if p not in cands: cands.append(p)
if "product" in pins:
    product_rel = pins["product"].replace(subdir + "/", "", 1)
    print(f"product file PINNED: {product_rel} (ticket names {len(cands)}: {cands})")
elif len(cands) == 1:
    product_rel = cands[0]
elif len(cands) == 0:
    refuse("names no product file under services/*/src or packages/shared/src (a bare filename is not a path); pin one with product=")
else:
    refuse(f"names {len(cands)} product files — not ONE: {cands}; pin one with product= if the fix site is unambiguous")
# a second .ts basename cited without a services/ prefix (`src/routes/foo.ts:12`, `bar.ts:9`)
# is a second site the regex above cannot see — refuse unless the product file is pinned
bases = set(b for b in re.findall(r"\b([A-Za-z0-9_\-]+\.ts)\b(?!\.)", desc) if not b.endswith(".test.ts"))
bases.discard(os.path.basename(product_rel))
if bases and "product" not in pins:
    refuse(f"besides {os.path.basename(product_rel)} the ticket also cites {sorted(bases)} — more than one site; pin product= if the fix is unambiguous")
product = f"{subdir}/{product_rel}"
if product_rel.startswith("services/"):
    service_dir = "services/" + product_rel.split("/")[1]
elif product_rel.startswith("packages/shared/"):
    service_dir = "packages/shared"
else:
    refuse(f"product path is neither services/* nor packages/shared: {product_rel}")

# ---------------------------------------------------------------- 3. fix shape
FIX_RE = re.compile(r"(?im)^\s*(?:#+\s*|\*\*)?(fix shape[^\n]*|recommendation[^\n]*|fix:[^\n]*|the fix[^\n]*|acceptance[^\n]*)")
fm = FIX_RE.search(desc)
if not fm:
    refuse("no fix shape in the description (no 'Fix shape' / 'Recommendation' / 'Fix:' / 'Acceptance' section) — a ruling, not a task")
# the quotable sentence: the inline text after the heading's colon (`**Fix shape:** do X`),
# else the first non-empty line after the heading
head = fm.group(1).strip()
inline = ""
if re.search(r"^(fix shape|recommendation|fix|the fix|acceptance)[^:\n]{0,80}:\**\s*\S", head, flags=re.I):
    inline = re.sub(r"^(fix shape|recommendation|fix|the fix|acceptance)[^:\n]{0,80}:\**\s*", "", head, flags=re.I).strip("* ").strip()
if len(inline) >= 25:
    fix_sentence = inline
else:
    after = desc[fm.end():].lstrip("\n")
    fix_sentence = next((ln.strip() for ln in after.split("\n") if ln.strip()), head)
print(f"fix shape: {fm.group(1).strip()[:60]!r} → {fix_sentence[:160]!r}")
# a fix shape that is explicitly a question/decision is refused
if re.search(r"(?i)\b(decision needed|needs a (call|ruling)|do not reconcile|fix shape deliberately blank|not chosen)\b", desc[fm.start():fm.start()+600]):
    refuse("the fix-shape section itself says a decision/ruling is needed first")

# ---------------------------------------------------------------- 4. test runner at the tip
def show(path):
    r = git("show", f"{tip}:{subdir}/{path}")
    return r.stdout if r.returncode == 0 else None
pkg = show(f"{service_dir}/package.json")
if pkg is None:
    refuse(f"{service_dir}/package.json is not at the tip")
test_script = json.loads(pkg).get("scripts", {}).get("test", "")
if "vitest" not in test_script:
    refuse(f"{service_dir} test script is {test_script!r} — the checker runs vitest only (jest services are out of the contract)")
has_setup = show(f"{service_dir}/vitest.setup.ts") is not None
has_cfg = show(f"{service_dir}/vitest.config.ts") is not None
tsconfig_txt = show(f"{service_dir}/tsconfig.json") or "{}"
try:
    co = json.loads(re.sub(r"//[^\n]*", "", tsconfig_txt)).get("compilerOptions", {})
except Exception:
    co = {}
ts_flags = ", ".join(k for k in ("strict", "noUnusedLocals", "noUnusedParameters", "esModuleInterop") if co.get(k))
ts_desc = f"{ts_flags}, module {co.get('module','?')}, target {co.get('target','?')}"

# ---------------------------------------------------------------- 5. product file content + defect line
content = show(product_rel)
if content is None:
    refuse(f"product file {product_rel} is not at the tip {tip[:9]} (renamed or deleted since the ticket was filed)")
lines = content.split("\n")
# Line numbers in a ticket are pinned to the SHA the ticket was read at and DRIFT by the
# time the night runs (KS-1072's `:240` was a comment line at the 09-14 tip). So the
# defect line is anchored on CODE the ticket quotes in backticks whenever possible: a
# snippet (>= 12 chars, not a path, not a bare `:NNN`) that occurs on exactly ONE line of
# the file at the tip. A cited `:NNN` is used only when that line contains such a snippet
# or when the ticket quotes nothing anchorable. `line=` pins override both.
snippets = [t.strip() for t in re.findall(r"`([^`\n]{12,160})`", desc)]
snippets = [t for t in snippets if not re.match(r"^[:\d\-, ]+$", t) and "/" not in t and not t.endswith(".ts")]
def unique_line_for(snippet):
    hits = [i + 1 for i, ln in enumerate(lines) if snippet in ln]
    return hits[0] if len(hits) == 1 else None
anchored = []
for sn in snippets:
    ln = unique_line_for(sn)
    if ln and ln not in [a[0] for a in anchored]:
        anchored.append((ln, sn))
cited = None
base = os.path.basename(product_rel)
idx = desc.find(base)
tail = desc[idx:] if idx >= 0 else desc
lm = re.search(r"(?<![\d.])[:`]\s*:?(\d{1,5})(?![\d])", tail) or re.search(r"`:(\d{1,5})`", desc)
if lm:
    cited = int(lm.group(1))
method = ""
if "line" in pins:
    defect_no = int(pins["line"]); method = "pinned (line=)"
elif cited and 1 <= cited <= len(lines) and any(sn in lines[cited - 1] for _, sn in anchored):
    defect_no = cited; method = f"cited :{cited}, confirmed by a quoted snippet"
elif anchored:
    defect_no, sn = anchored[0]; method = f"anchored on quoted snippet {sn[:50]!r} (cited :{cited} not confirmed — line numbers drift)"
elif cited:
    defect_no = cited; method = f"cited :{cited} (UNCONFIRMED — the ticket quotes no code that occurs on one line of the file)"
else:
    refuse("no defect line: the ticket cites no `<file>:NNN` line and quotes no code that occurs on one line of the file; pin one with line=")
if not (1 <= defect_no <= len(lines)):
    refuse(f"defect line {defect_no} is outside the file ({len(lines)} lines at the tip)")
defect_text = lines[defect_no - 1]
print(f"product {product_rel} ({len(content)} B, {len(lines)} lines) defect line {defect_no} [{method}]: {defect_text.strip()[:100]!r}")
if len(anchored) > 1:
    print(f"  other quoted-code anchors at the tip: {[a[0] for a in anchored[1:8]]}")
imports = [ln for ln in lines if ln.startswith("import ")][:12]

# ---------------------------------------------------------------- 6. reference test (imports the product module)
test_dir_rel = f"{service_dir}/src/__tests__"
r = git("ls-tree", "-r", "--name-only", tip, "--", f"{subdir}/{test_dir_rel}")
tests = [p for p in r.stdout.split("\n") if p.endswith(".test.ts")]
if not tests:
    refuse(f"no test files under {test_dir_rel} at the tip")
mod_rel = product_rel[len(service_dir) + len("/src/"):]          # e.g. middleware/audit.ts
mod_noext = re.sub(r"\.ts$", "", mod_rel)                          # middleware/audit
mod_base = os.path.basename(mod_noext)                             # audit
scored = []
for t in tests:
    body = git("show", f"{tip}:{t}").stdout
    imp = re.findall(r"from\s+['\"](\.{1,2}/[^'\"]+)['\"]", body) + re.findall(r"import\(\s*['\"](\.{1,2}/[^'\"]+)['\"]\s*\)", body)
    hits = [i for i in imp if i.rstrip("/").endswith("/" + mod_noext) or i.rstrip("/").endswith("/" + mod_base) or i.endswith(mod_noext)]
    if not hits: continue
    mocks = re.findall(r"vi\.mock\(\s*['\"]([^'\"]+)['\"]", body)
    ksn = re.search(r"ks(\d+)", os.path.basename(t))
    scored.append((len(mocks) > 0, int(ksn.group(1)) if ksn else 0, t, body, mocks, hits))
if "ref" in pins:
    ref_path = pins["ref"] if pins["ref"].startswith(subdir) else f"{subdir}/{pins['ref']}"
    ref_body = show(ref_path[len(subdir) + 1:])
    if ref_body is None: refuse(f"pinned ref test {ref_path} is not at the tip")
    ref_mocks = re.findall(r"vi\.mock\(\s*['\"]([^'\"]+)['\"]", ref_body)
    print(f"reference test PINNED: {ref_path}")
elif scored:
    scored.sort(key=lambda s: (s[0], s[1]), reverse=True)
    _, _, ref_path, ref_body, ref_mocks, hits = scored[0]
    print(f"reference test: {ref_path} (imports {hits[0]!r}; {len(ref_mocks)} vi.mock stubs; {len(scored)} candidate(s))")
else:
    refuse(f"no in-process test under {test_dir_rel} imports {mod_noext!r} — nothing to copy the mock shape from; pin one with ref=")
if ref_path.replace(subdir + "/", "") == product_rel:
    refuse("reference test equals the product file")

# ---------------------------------------------------------------- 7. emit
slug = re.sub(r"[^a-z0-9]+", "-", n["title"].lower()).strip("-")
slug = "-".join(slug.split("-")[:6])[:60].rstrip("-")
suggested = f"{subdir}/{test_dir_rel}/ks{number}-{slug}.test.ts"
runner = f"vitest (run one file with `npx vitest run <file>` from {subdir}/{service_dir}" + \
         ("; setupFiles ./vitest.setup.ts" if has_setup else "") + (")" if has_cfg else "; no vitest.config.ts at the tip)")
note = (
    f"READ-ONLY template: `{ref_path}` is an EXISTING test in the same __tests__ directory that imports the "
    f"product module (`{mod_noext}`) and drives it in-process" +
    (f" with vi.mock stubs for: {', '.join(ref_mocks[:12])}" if ref_mocks else " (no vi.mock — it calls the module directly)") +
    ". Copy its app-building / import / mock shape; do NOT modify it. "
    f"The ticket's fix shape, quoted: \"{fix_sentence[:400]}\". "
    f"The ticket-named cell must reach the defective code at line {defect_no} of `{product_rel}` "
    f"({defect_text.strip()[:120]!r}) and assert the BEHAVIOUR the ticket describes — fix every site the ticket names inside the product file, "
    "not only the first. The CONTROL cell passes before and after the fix and proves the harness reaches the code "
    "(an early return, a 4xx on a mismatch, or a found-row branch means the code under test was never reached). "
    "Where the reference test's mocks do not cover a dependency your cell needs, add a vi.mock for it in YOUR test file "
    "following the same factory shape; write UNKNOWN in a comment rather than inventing an API."
)
repo = {
    "source_checkout": src, "tip": tip, "branch": "develop", "repo_subdir": subdir,
    "service_dir": service_dir, "shared_pkg_dir": "packages/shared", "shared_pkg_name": "@secuura/shared",
    "test_runner": runner,
    "typescript": f"{ts_desc}; the product file's imports at the tip are: " + (" | ".join(i.strip() for i in imports) if imports else "(none)"),
}
inp = {
    "ticket": {"identifier": n["identifier"], "title": n["title"], "state": state,
               "priority": n["priorityLabel"], "description": desc},
    "repo": repo,
    "product_file": product,
    "defect_line": {"line": defect_no, "text": defect_text},
    "test_dir": f"{subdir}/{test_dir_rel}",
    "suggested_test_file": suggested,
    "reference_test_file": ref_path,
    "reference_test_note": note,
    "files": {product: content, ref_path: ref_body},
    "source_checkout": src, "tip": tip, "repo_subdir": subdir, "service_dir": service_dir,
    "shared_pkg_dir": "packages/shared", "shared_pkg_name": "@secuura/shared",
}
# contract self-check against the KS-871 input's key set, when that evidence is present
kt = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-14_ks871-gptoss120b/input.json"
if os.path.exists(kt):
    k871 = json.load(open(kt))
    if set(k871) != set(inp) or set(k871["ticket"]) != set(inp["ticket"]) or set(k871["repo"]) != set(inp["repo"]):
        sys.stderr.write("build_input: key set differs from the KS-871 input — contract drift\n"); sys.exit(1)
    print("contract: key set == KS-871 input (top-level, ticket, repo)")
if "ctx" in pins:
    inp["_night_num_ctx"] = int(pins["ctx"])
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(inp, f, indent=1, ensure_ascii=False); f.write("\n")
sz = os.path.getsize(out)
est = (len(json.dumps(inp)) ) // 4
ctx = int(pins.get("ctx", 32768))
print(f"wrote {out} ({sz} B; ~{est} prompt tokens at 4 B/token — num_ctx {ctx} leaves ~{ctx - est} for the answer)")
if ctx - est < 12000:
    print(f"WARNING: prompt estimate {est} tokens leaves under 12K for the answer at num_ctx {ctx} — pin a larger ctx= on the queue line")
sys.exit(0)
PYEOF
