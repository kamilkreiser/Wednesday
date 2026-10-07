#!/usr/bin/env python3
# Seat B 58th (round 53) -- merge53. A NEW COPY of Seat B 57th's merge52, never an edit of it.
# AUTHORSHIP HEADER WRITTEN BY HAND, Seat B 58th. The lines below are the predecessor's
# own record and survive byte-identical: a re-key would make them claim my round.
# Seat B 57th (round 52) -- merge52.py. A NEW COPY of Seat B 56th's merge51.py, never an edit of it.
# AUTHORSHIP HEADER WRITTEN BY HAND, Seat B 57th. The lines below are the predecessor's
# own record and survive byte-identical: a re-key would make them claim my round.
# Seat B 56th (round 51) -- merge51.py.
# AUTHORSHIP HEADER WRITTEN BY HAND. The lineage lines below survive byte-identical: they
# RECORD other seats' rounds, and a re-key would make them claim mine.
"""Seat B 44th — merge40.py. A NEW COPY of Seat B 43rd's merge39.py, never an edit of it.
Seat B 42nd — merge38.py. A NEW COPY of Seat B 41st's merge37.py, never an edit of it.
Seat B 41st — merge37.py. A NEW COPY of Seat B 40th's merge36.py, never an edit of it.
  Seat B 33rd — merge29.py. A NEW COPY of Seat B 32nd's merge28.py, never an edit of it.
Re-keyed in the LIVE REGION only, every count MEASURED and asserted by the generator.
⚠ The counts here are NON-OVERLAPPING and applied longest-token-first: `s-b32-` CONTAINS
`-b32-` which CONTAINS `b32`, so a census that counts all three separately triple-counts one
string. My first attempt asserted the census numbers and REFUSED — correctly. Each count below
is what remains after the longer tokens have already been replaced.
The predecessor header chain below is preserved byte-identical, because re-keying prose means
updating what a file claims about ITSELF, never what it RECORDS about others.

ENV VAR, STATED HERE BECAUSE THE CHAIN BELOW DOCUMENTS THE WRONG ONE: this tool reads
`MERGE29_SCRATCH`. B 32nd's docstring below says `MERGE27_SCRATCH` in its usage line while its code
read `MERGE28_SCRATCH` — its docstring was two generations stale and its own arms suite set
`MERGE27_SCRATCH` (three call sites), so the per-arm scratch isolation those calls were written to
provide NEVER TOOK EFFECT for B 32nd: merge28.py silently used its default SCRATCH. The refusal arms
do not depend on scratch, so its 17/17 is not thereby wrong — but the per-arm isolation it implies
was not in force. Found by rekey_check29.py, whose token list covers N-2. Reported to Wednesday.
I am NOT editing the chain below to fix it: it records what B 32nd wrote.

Seat B 32nd's header follows, unchanged in substance:
Seat B 32nd — merge28.py. A NEW COPY of Seat B 31st's merge27.py, never an edit of it, and never
RUN from B 31st's folder.

RE-KEYED THIS ROUND, in the LIVE region only: MERGE27_SCRATCH -> MERGE28_SCRATCH, merge27-*.log ->
merge28-*.log, idx_merge27_ -> idx_merge28_, the scratch default (B 31st's session path would write
into a DEAD session's directory), the --seat help example, and the log banner. The fetch window is
`.push-lock-28`.

--seat stays REQUIRED with NO default, and that is load-bearing, not ceremony: the seat name lands
in the squash body's provenance note, which is permanent on develop. B 31st's trap 1 is the one to
remember here — its arms suite hard-coded the PREDECESSOR's name in a FIXTURE while passing --seat
from argv, so merge27.py's merger-identity gate fired first and 5 of 17 arms, including the only
positive control, never reached their own assertion. Re-keying code is not re-keying data.

NOTHING IS MERGED BY THIS SEAT WITHOUT Wednesday's signed GO naming the head SHA, and the whole
batch is rehearsed with chained --dry runs that derive the END_TREE before anything irreversible.

Seat B 31st's header follows, unchanged in substance:
Seat B 31st — merge27.py. A NEW COPY of Seat M1's merge25.py, never an edit of it, and never RUN
from M1's folder: `R` is the script's own directory, so theirs would write MY logs into THEIR records.

🔴 THE ONE SEMANTIC DIFFERENCE FROM M1's COPY, and it is not a rename. M1 MERGED ONLY and authored
nothing, so `merge_note` / `wrap_artefact` existed to force a MEASURED claim that some OTHER seat had
wrapped. THIS SEAT IS THE AUTHOR of the PRs it merges (items 1 and 2 of round 27). So the note is a
claim about MY OWN work and its authority, not about a predecessor's wrap: Wednesday's signed GO
naming the head, under Kam's open-ended TESTED grant of 2026-09-11 ("we approve our own work ... fix
and merge all tickets after they are tested"). Both fields stay REQUIRED with NO default — a default
that makes a factual claim is a hardcoded claim with extra steps, and this one lands on develop
permanently. For an author-merge, `wrap_artefact` names the AUTHORITY (the GO mail's id and date),
and the assertion that it must appear INSIDE the note is unchanged, so the authority is written into
the text that lands on develop. ⚠ The exact note wording is put to Wednesday in Q-MERGE before any
merge; it is not chosen by this tool.

RE-KEYED: MERGE25_SCRATCH -> MERGE27_SCRATCH, merge25-*.log -> merge27-*.log, idx_merge25_ ->
idx_merge27_, the scratch default (M1's session path would have written into a dead session's dir),
the usage example's seat, and the fetch window `.push-lock-25` -> `.push-lock-27`.

Seat M1's header follows, unchanged in substance — it records what THAT round changed:
Seat M1 — merge25.py. A NEW COPY of the round-24 merge tool, never an edit of it.

M1 MERGED ONLY. It authored nothing, so every squash body it wrote was a statement about
work SOMEONE ELSE did. That is the whole reason the provenance lines below are parameters and
not defaults.

WHAT THIS COPY CHANGES, and each because of something measured in round 24:
  A. `merge_note` IS REQUIRED. The inherited default asserted "the author had already wrapped,
     so this is not the author merging their own PR". That is a CLAIM ABOUT A FACT OF THE WORLD
     sitting in a parameter's default, and it lands on develop permanently. A default that makes
     a factual claim is a hardcoded claim with extra steps. Both round-25 build seats found the
     same thing independently. Here it has no default at all.
  B. `wrap_artefact` IS REQUIRED and must appear INSIDE the note. The note may only say the
     author wrapped if the addendum names the artefact that MEASURES it — a handover file, a
     vault wrap section, a wrap mail id. Unmeasured => the addendum says so in its own words and
     the assertion below still forces the artefact string to be present and quoted.
  C. THE MERGER-IDENTITY GATE. The body must contain exactly ONE "Merged by " and it must name
     this seat. A predecessor's name surviving a copy-and-re-key is the failure this catches, and
     it is caught by reading the body the tool WOULD write, not by reading the tool.
  D. OBJECT-STORE CONTAINMENT IS BAKED IN, covering the WRITES of the prediction and every later
     READ of it. Containment is proved on BOTH sides or not at all: the shared store's loose-object
     delta is 0 AND the contained store is non-empty. A delta of 0 on its own is also exactly what
     a merge-tree that never ran would print.
  E. Namespace re-keyed for this seat: MERGE27_SCRATCH, merge27-*.log, and the fetch window is
     `.push-lock-27`.

WHAT IS UNCHANGED, and why it is kept: one PR per invocation; the head SHA pinned from the GO and
checked against BOTH instruments by the caller; the base read FRESH at every invocation and never a
literal; the merged tree PREDICTED before the merge and asserted after; the THREE-DOT patch, never
two-dot; a per-file blob-and-mode gate; the addendum's equality targets asserted at the squash;
MG-3 on the body's key set; MG-11 on the subject; `--dry`; STOP (exit 3) on any mismatch; no fetch
of its own; no force; no --admin.

Usage: merge27.py <PR> --addendum <json> --go-ts <ts> --gate <id> --seat 'Seat B 31st'
                  [--prev-tree <sha>] [--expect-develop <sha>] [--dry]
Env: GH_TOKEN. REQUIRED ARGUMENT: --scratch (Seat R 5th; see the SCRATCH block below).
Seat R 5th: the docstring said MERGE27_SCRATCH while the code read MERGE56_SCRATCH -- two
generations stale, the same drift this file records at :24-:26 about B 32nd. --scratch is now a
required argument with NO default and no env fallback, so neither can go stale again."""
import argparse, json, os, re, subprocess, sys, time, urllib.request, urllib.error

R = os.path.dirname(os.path.abspath(__file__))
REPO = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
KEY = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw"
ENV = dict(os.environ, GIT_SSH_COMMAND=f'ssh -i "{KEY}" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new')
# 🔴 A REQUIRED ARGUMENT, Seat R 5th (Q-TOOLS5). It arrived as os.environ.get("MERGE56_SCRATCH",
# <Seat B 65th's SESSION scratchpad, UUID 4f1e7e2b-...>) -- a DEAD DEFAULT naming another
# session. merge-tree/write-tree write their contained objects into this directory, so a stale
# value writes them into a wrapped seat's tree (or fails outright when that session is gone).
# The file already records exactly this: B 64th re-pointed the leaf and reseat62.py was BLIND
# to the UUID, "which is the worse half: the path LOOKED re-keyed". A required argument cannot
# be inherited silently. Resolved AFTER argparse, below.
SCRATCH = None
# OBJDIR / REALOBJ are resolved after argparse, because OBJDIR depends on --scratch.
REALOBJ = os.path.join(REPO, ".git", "objects")       # readable as an ALTERNATE so prediction still resolves

ap = argparse.ArgumentParser()
ap.add_argument("pr"); ap.add_argument("--addendum", required=True); ap.add_argument("--go-ts", required=True)
ap.add_argument("--gate", required=True); ap.add_argument("--prev-tree"); ap.add_argument("--expect-develop")
ap.add_argument("--repo", default=REPO); ap.add_argument("--api", default="https://api.github.com/repos/Secuura/Distributed_Secuura")
ap.add_argument("--dry", action="store_true")
ap.add_argument("--scratch", required=True, help="THIS session's scratch directory. REQUIRED, no "
                "default: merge-tree writes contained objects here and a predecessor's path writes "
                "them into a dead session's tree.")
ap.add_argument("--seat", required=True, help="this seat's name, e.g. 'Seat B 49th'. REQUIRED: it is "
                "written into the squash body, which lands on develop permanently.")
A = ap.parse_args()
REPO = A.repo
# WRONG-VALUE ARMS for --scratch: it must exist, be a directory, be writable, and must not be
# inside the shared checkout (writing contained objects there is the thing it exists to prevent).
SCRATCH = os.path.abspath(A.scratch)
if not os.path.isdir(SCRATCH):
    raise SystemExit(f"REFUSED: --scratch {SCRATCH!r} is not an existing directory")
if not os.access(SCRATCH, os.W_OK):
    raise SystemExit(f"REFUSED: --scratch {SCRATCH!r} is not writable")
if os.path.commonpath([SCRATCH, os.path.abspath(REPO)]) == os.path.abspath(REPO):
    raise SystemExit(f"REFUSED: --scratch {SCRATCH!r} is inside the shared checkout {REPO!r}; "
                     "contained objects must never be written there")
OBJDIR = os.path.join(SCRATCH, "contained-objects")   # merge-tree/write-tree write HERE, never the shared store
ADD = json.load(open(A.addendum))
BASE_GO = ADD["base_go"]
if not re.fullmatch(r"[0-9a-f]{40}", BASE_GO): sys.exit("STOP: addendum base_go must be 40 hex")
if A.pr not in ADD["prs"]: sys.exit(f"STOP: addendum has no PR {A.pr}")
P = ADD["prs"][A.pr]
T = os.environ["GH_TOKEN"]

log = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); log.append(s)
def dump(): open(f"{R}/mergera1-{A.pr}{'.DRY' if A.dry else ''}.log", "a").write("\n".join(log) + "\n")
def stop(m): say("STOP:", m); dump(); sys.exit(3)
# Set once the prediction exists: later reads of it need the same object view. AND set UP FRONT when
# chaining, because --prev-tree IS a previous prediction and therefore lives in the CONTAINED store,
# never in the shared one. Measured, not reasoned about: with this False at the start, the chained
# leg STOPped at "--prev-tree ... is not a local tree" on a tree the tool had written itself minutes
# earlier. That would have refused merges 2..N of EVERY batch. The contained view keeps the real
# store as an alternate, so nothing else stops resolving.
CONTAIN_ALL = False


def git(*a, check=True, idx=None, inp=None, contain=False):
    e = dict(ENV)
    if idx: e["GIT_INDEX_FILE"] = idx
    if contain or CONTAIN_ALL:
        # Redirect object WRITES into this seat's own scratch dir, keeping the real store readable
        # as an alternate so the prediction still resolves every blob it needs. Baked in, not
        # exported: an export is a habit and the next caller does not inherit it.
        os.makedirs(OBJDIR, exist_ok=True)
        e["GIT_OBJECT_DIRECTORY"] = OBJDIR
        e["GIT_ALTERNATE_OBJECT_DIRECTORIES"] = REALOBJ
    p = subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True, env=e, input=inp)
    if check and p.returncode != 0: stop(f"git {' '.join(a)} rc {p.returncode} {p.stderr[-300:]}")
    return p.stdout.strip()
def api(path, method="GET", body=None):
    r = urllib.request.Request(A.api + path, method=method,
        headers={"Authorization": "token " + T, "Accept": "application/vnd.github+json", "Content-Type": "application/json"},
        data=json.dumps(body).encode() if body else None)
    try: return json.load(urllib.request.urlopen(r, timeout=120))
    except urllib.error.HTTPError as e: return {"_http": e.code, "_body": e.read().decode()[:500]}

say(f"{time.strftime('%H:%M:%SZ', time.gmtime())} mergera1 #{A.pr}{' (DRY)' if A.dry else ''} gate {A.gate} seat {A.seat!r}")

# ---- 1. the PR, and the head == the GO's pin -------------------------------------------------
d = api(f"/pulls/{A.pr}")
if "_http" in d: stop(f"GET /pulls/{A.pr} -> {d['_http']} {d['_body']}")
if d["state"] != "open": stop(f"PR #{A.pr} is {d['state']}, not open")
if d["merged"]: stop(f"PR #{A.pr} is already merged")
if d["head"]["sha"] != P["head"]: stop(f"PR head {d['head']['sha']} != the GO's pin {P['head']}")
if d["base"]["ref"] != "develop": stop(f"base is {d['base']['ref']}, not develop")
say(f"  head {P['head'][:12]} == the GO's pin; open; base develop")

# ---- 2. develop read FRESH (ls-remote writes no ref) ------------------------------------------
dev = git("ls-remote", "origin", "refs/heads/develop").split("\t")[0].strip()
if not re.fullmatch(r"[0-9a-f]{40}", dev): stop(f"ls-remote gave {dev!r}")
if A.expect_develop and dev != A.expect_develop: stop(f"develop {dev} != the expected {A.expect_develop} (it moved under me)")
moved = dev != BASE_GO
say(f"  develop at origin {dev[:12]}{' (== BASE_GO)' if not moved else ' (MOVED from BASE_GO ' + BASE_GO[:12] + ')'}")

# ---- 3. objects must be local; this script never fetches --------------------------------------
for sha, what in ((BASE_GO, "BASE_GO"), (P["head"], "the head")):
    if subprocess.run(["git", "-C", REPO, "cat-file", "-e", sha + "^{commit}"], env=ENV,
                      capture_output=True).returncode != 0:
        stop(f"{what} {sha[:12]} is not in this checkout. mergera1.py never fetches — take "
             f".push-lock-d8, run the fetch window, release, and re-run.")
if A.prev_tree:
    globals()["CONTAIN_ALL"] = True      # before the first read of it, not after
    os.makedirs(OBJDIR, exist_ok=True)
    _contained = dict(ENV, GIT_OBJECT_DIRECTORY=OBJDIR, GIT_ALTERNATE_OBJECT_DIRECTORIES=REALOBJ)
    if subprocess.run(["git", "-C", REPO, "cat-file", "-e", A.prev_tree + "^{tree}"],
                      env=_contained, capture_output=True).returncode != 0:
        stop(f"--prev-tree {A.prev_tree[:12]} is not in the contained object store {OBJDIR} nor in the "
             f"shared store. A chained prediction must come from THIS seat's own earlier --dry/merge run.")
    say(f"  --prev-tree {A.prev_tree[:12]} resolved in the CONTAINED store; every read from here uses that view")

# ---- 4. predict the merged tree over the CURRENT develop --------------------------------------
if A.prev_tree:
    idx = f"{SCRATCH}/idx_merge56_{A.pr}"
    os.makedirs(SCRATCH, exist_ok=True)
    if os.path.exists(idx): os.remove(idx)
    git("read-tree", A.prev_tree, idx=idx)
    # RAW stdout, NOT git(): git() .strip()s, and stripping the diff's trailing newline makes
    # `git apply` report "corrupt patch at line N".
    # THREE-DOT, and this is not a style point. `git diff BASE_GO head` is TWO-DOT: it reports
    # everything develop gained since the PR forked as though the PR were undoing it. Measured in
    # round 24 on a one-file PR: the two-dot patch touched 25 files and would have REVERTED them
    # onto develop inside a squash whose stated scope is one file. The file-set assertion below is
    # what caught it. The patch this PR actually carries is diff(merge-base, head).
    mb = git("merge-base", BASE_GO, P["head"])
    if not re.fullmatch(r"[0-9a-f]{40}", mb): stop(f"merge-base(BASE_GO, head) gave {mb!r}")
    if mb != BASE_GO: say(f"  the head forked at {mb[:12]}, which is BEHIND BASE_GO {BASE_GO[:12]} -- "
                          f"using the THREE-DOT patch diff({mb[:12]}, head), never diff(BASE_GO, head)")
    dp = subprocess.run(["git", "-C", REPO, "diff", mb, P["head"]], capture_output=True, text=True, env=ENV)
    if dp.returncode: stop(f"git diff {mb[:9]}..{P['head'][:9]} rc {dp.returncode} {dp.stderr[-200:]}")
    diff = dp.stdout
    if diff and not diff.endswith("\n"): stop("the diff does not end in a newline; git apply would call it corrupt")
    r = subprocess.run(["git", "-C", REPO, "apply", "--cached", "-"], env=dict(ENV, GIT_INDEX_FILE=idx),
                       capture_output=True, text=True, input=diff)
    if r.returncode: stop(f"chained predict: apply failed {r.stderr[:250]}")
    pred = git("write-tree", idx=idx, contain=True); os.remove(idx)
    globals()["CONTAIN_ALL"] = True   # the prediction lives in OBJDIR; reads of it need that view
    say(f"  predicted tree {pred[:12]} (CHAINED from --prev-tree {A.prev_tree[:12]} + three-dot diff({mb[:12]}, head))")
else:
    pred = git("merge-tree", "--write-tree", dev, P["head"], contain=True).split("\n")[0]
    globals()["CONTAIN_ALL"] = True   # the prediction lives in OBJDIR; reads of it need that view
    if not re.fullmatch(r"[0-9a-f]{40}", pred): stop(f"merge-tree did not produce a clean tree: {pred!r}")
    say(f"  predicted tree {pred[:12]} (merge-tree over develop {dev[:12]} read this run)")

# ---- 5. THREE-DOT file set: what THIS PR changes, from GitHub's own /files ---------------------
files = sorted(f["filename"] for f in api(f"/pulls/{A.pr}/files?per_page=100"))
declared_paths = sorted(P["targets"].keys())
if files != declared_paths: stop(f"the PR's own files {files} != the addendum's equality-target paths {declared_paths}")
# Compare the prediction against a LOCAL base. When chaining, develop's new commit was never fetched
# (that is why we chain at all), so the base for this diff is the previous merged TREE, which is
# local and is exactly "what this PR adds on top of the batch so far".
diff_base = A.prev_tree if A.prev_tree else dev
changed = sorted(x for x in git("diff", "--name-only", diff_base, pred).split("\n") if x)
# 🔴 FIXED BY HAND, Seat B 48th — A SQUASH-STACK NO-OP MADE THIS ASSERTION UNSATISFIABLE.
# It compared the predicted tree's changed set against the PR's own /files list. In a STACK, an
# earlier squash in the same batch can already have landed the IDENTICAL blob for one of the later
# PR's paths; the later merge then changes FEWER paths than the PR lists, and this refused a correct
# merge. Measured on gate48b: #1354 landed systemTest/performance/package-lock.json at
# 80c6752aab86, and #1355 carries the same blob, so merging #1355 changed 4 paths while its /files
# lists 5. The gate's own MERGE ADDENDUM predicted it: "performance lock NO-OP at #1355".
# The subtraction is ONLY of paths the addendum DECLARES as no-ops, and the declaration is not taken
# on trust: the per-path gate below asserts head == merged == develop for each declared no-op and
# STOPs if they are not all equal, so a FALSE declaration cannot buy an exemption here. An
# UNDECLARED path that goes missing from the prediction still trips this line, which is the whole
# point of it.
noop_declared = set(P.get("noop_paths", []))
_unknown_noop = sorted(noop_declared - set(files))
if _unknown_noop: stop(f"noop_paths names path(s) the PR does not touch: {_unknown_noop}")
expect_changed = sorted(set(files) - noop_declared)
if changed != expect_changed:
    stop(f"predicted tree changes {changed} but the PR lists {files} "
         f"minus declared no-ops {sorted(noop_declared)} = {expect_changed}")
if noop_declared:
    say(f"  file set: {len(changed)} changed == the PR's {len(files)} path(s) minus "
        f"{len(noop_declared)} DECLARED no-op(s) {sorted(noop_declared)}; each is asserted "
        f"head == merged == develop below, so the declaration is proved, not trusted")
say(f"  three-dot file set {len(files)} path(s), == the addendum's targets, == diff("
    f"{'prev merged tree ' + diff_base[:12] if A.prev_tree else 'develop ' + dev[:12]}, predicted)")

# ---- 6. blob gate: every path at the predicted tree carries the head's blob AND the gate's target
# DECLARED OVERLAP (the gate's term): where an earlier merge of this round already moved a path this
# PR also touches, the addendum's equality target is the MERGED blob and is NOT the head blob.
# Asserting the head blob there would refuse a merge the gate measured clean. So for exactly the
# paths the addendum DECLARES, the head-blob equality is dropped and the merged target is asserted
# instead -- and the head blob is printed, so the substitution is on the record rather than silent.
overlap = set(P.get("merged_blob_paths", []))
# A NO-OP IS NOT AN OVERLAP (STANDING_LINES, 2026-09-27). `merged_blob_paths` declares a genuine
# overlap: the merge resolves a file to a blob DIFFERENT from the PR head's. A squash-stack no-op is
# head == merged == develop, and declaring it under the overlap key trips the overlap check
# CORRECTLY, because there is no substitution to make. It gets its own key.
noop = set(P.get("noop_paths", []))
_both = overlap & noop
if _both:
    stop(f"a path is declared BOTH as an overlap and as a no-op, which cannot both be true: {sorted(_both)}")
for path in files:
    want_head = git("rev-parse", f"{P['head']}:{path}", check=False)
    got = git("rev-parse", f"{pred}:{path}", check=False)
    tb, tm = P["targets"][path]
    if path in noop:
        # head == merged == develop. All three asserted; anything else is a STOP, so a wrong
        # declaration cannot pass as a no-op.
        # 🔴 RENAMED BY HAND, Seat B 48th. This assigned the per-path BLOB to a variable called
        # `dev`, which is the name the develop COMMIT sha is held in from section 4 onwards. It only
        # executes when a no-op is DECLARED — which no previous round did — so the shadowing sat here
        # latent until gate48b's squash stack hit it: section 7's `dev[:12]` then raised
        # TypeError: 'NoneType' object is not subscriptable, because this PR's addendum entry carries
        # no `expect_develop` key and the expression evaluated to None. Adding that key would have
        # silenced the crash and made section 7 print a BLOB sha labelled as develop's commit, which
        # is worse than the crash. The variable is renamed instead; `dev` is left alone.
        dev_blob = git("rev-parse", f"{P['expect_develop']}:{path}", check=False) if P.get("expect_develop") else None
        if not (want_head == got == (dev_blob if dev_blob else want_head)):
            stop(f"DECLARED NO-OP {path}: head {want_head[:12]}, merged {got[:12]}"
                 + (f", develop {dev_blob[:12]}" if dev_blob else "") + " — they are not all equal")
        say(f"  NO-OP {path}: head == merged{' == develop' if dev else ''} ({want_head[:12]})")
        continue
    if path in overlap:
        if got != tb:
            stop(f"DECLARED OVERLAP {path}: predicted blob {got[:12]} != the addendum's MERGED target {tb[:12]}")
        if want_head == tb:
            stop(f"DECLARED OVERLAP {path}: the head blob EQUALS the merged target {tb[:12]}, so there is no "
                 f"overlap here and the addendum's declaration is wrong -- STOP rather than accept it")
        say(f"  DECLARED OVERLAP {path.split('/')[-1]}: predicted {got[:12]} == the addendum's MERGED target; "
            f"the head's own blob is {want_head[:12]} and is deliberately NOT asserted")
    else:
        if got != want_head: stop(f"blob of {path} at the predicted tree {got[:12]} != the head's {want_head[:12]}")
        if got != tb: stop(f"blob of {path} {got[:12]} != the gate addendum's equality target {tb[:12]}")
    o = git("ls-tree", pred, "--", path).split()
    if len(o) < 3 or o[0] != tm: stop(f"mode of {path} {o[:1]} != the addendum's {tm}")
for ov_path in overlap:
    if ov_path not in files:
        stop(f"the addendum declares an overlap on {ov_path}, which is not among this PR's files {files}")
say(f"  blob gate: {len(files)}/{len(files)} path(s) == the addendum's target, modes equal"
    + (f"; {len(overlap)} DECLARED OVERLAP path(s) asserted against the MERGED blob" if overlap else
       "; every path also == the head's blob"))

# ---- 7. the addendum's merged tree reproduces ONLY while develop is still BASE_GO --------------
# The addendum's merged_tree is the PR-ALONE tree over BASE_GO. It is expected to reproduce ONLY when
# the prediction is BOTH over an unmoved develop AND unchained. A CHAINED prediction is by construction
# "the batch so far plus this PR", so it differs from the PR-alone tree even while develop has not moved
# — which is exactly the state of a whole-batch DRY rehearsal run before the first merge. The original
# condition tested only `not moved`, so it refused the rehearsal; and the rehearsal is the only chance
# to check the GO's END_TREE BEFORE the first irreversible merge rather than after the last one.
if P.get("merged_tree"):
    alone = (not moved) and (not A.prev_tree)
    if alone and pred != P["merged_tree"]:
        stop(f"predicted {pred} != the addendum's merged tree {P['merged_tree']} while develop is still "
             f"BASE_GO and this prediction is unchained")
    if alone: say(f"  predicted tree == the addendum's merged tree {P['merged_tree'][:12]}")
    elif not moved: say(f"  addendum tree {P['merged_tree'][:12]} is the PR-ALONE tree over BASE_GO; this "
                        f"prediction is CHAINED from {A.prev_tree[:12]}, so it is the batch-so-far tree and "
                        f"is NOT expected to equal it — the chained file-set and blob gates are the assertion")
    else: say(f"  addendum tree {P['merged_tree'][:12]} is the PR-ALONE tree over BASE_GO; develop has moved to "
              f"{dev[:12]}, so it is NOT expected to reproduce (base-invariant) — the chained prediction is the assertion")

# ---- 8. subject (MG-11), provenance, and body (MG-3) -------------------------------------------
# The gate may supply its own <=92-char subject; PR titles have run to 95/132/182 chars, so the PR
# title is a fallback, not the rule. When the addendum gives one, the addendum wins.
# 🔴 HAND-FIX, Seat D 6th, carried by Seat B 59th: THE ADDENDUM SUBJECT IS REQUIRED.
# It used to read `P.get("subject") or d["title"]`, so an OMITTED subject silently fell back to
# the PR TITLE -- and PR titles have run to 95, 132 and 182 chars here. D 6th's clean dry run was
# green BECAUSE of that fallback, and it was found only by diffing a planted addendum against a
# REAL one. A green dry run can be green because a default filled a field you never declared.
if not P.get("subject"):
    stop("MG-11: the gate addendum declares no `subject`. There is NO fallback to the PR title: "
         "the squash subject is irreversible and must be declared explicitly by the addendum "
         "that the GO names.")
subject = P["subject"]
say(f"  subject from the gate addendum ({len(subject)} chars), REQUIRED; "
    f"the PR title is {len(d['title'])} chars and is NOT used")
# ---- MG-11 MEASURED AS IT WILL LAND (STANDING_LINES, 2026-09-27) -------------------------------
# [SUPERSEDED RECORD, marked by Seat B 59th -- the paragraph below described the behaviour this
#  file had BEFORE Seat D 6th's hand-fix 3, and read as a live claim about code that no longer
#  does it. Kept because it is WHY these guards exist, not deleted; but a comment asserting
#  something false about its own live code is a defect, not history:]
#    "GitHub's squash merge APPENDS \" (#n)\" to whatever subject it is given, and this tool does
#     so explicitly when it builds commit_title. So a declared subject of exactly 92 chars LANDS
#     at 92 + len(\" (#n)\"). gate31 declared subjects that ALREADY ended in \"(#n)\", and three
#     doubled subjects landed on develop permanently, one of them at 95 chars over a 92-char
#     rule. Two guards, and the length one measures the LANDED string, never the declared one."
# WHAT IS TRUE NOW: this tool appends NOTHING (hand-fix 3), so the declared subject is the landed
# subject byte for byte, and the length guard measures it directly. Measured live by Seat D 6th
# on #1376: declared 67, landed 67, `contains '(#'` False.
# 🔴 HAND-FIX, Seat D 6th, carried by Seat B 59th. THE SUFFIX ARITHMETIC IS GONE because the
# append is gone (hand-fix 3). The declared subject is what LANDS, byte for byte. Seat D 6th's
# near-miss is why this matters: its gate addendum and Wednesday's GO both annotated the subject
# "(67, lands 75)" -- 67 + len(" (#1376)") -- the OLD arithmetic, while hand-fix 3 had already
# removed the append. Had the suffix still appeared, D 6th's post-merge guard would have refused
# AFTER a correct irreversible merge: the worst shape a post-merge assertion can have. It held
# the merge and asked; Wednesday ruled 67, no suffix, and superseded her own GO's wording.
_suffix = ""
if re.search(r'\(#\d+\)$', subject):
    stop(f"MG-11: the declared subject ALREADY ends in a (#n) suffix: {subject!r}. This tool "
         f"appends nothing, so such a subject would land WITH the suffix and name the wrong PR.")
if "(#" in subject:
    stop(f"MG-11: the declared subject contains '(#': {subject!r}. Nothing appends it now, so a "
         f"'(#' in the subject is text someone typed, not a suffix to tolerate.")
_landed = len(subject)
if _landed > 92:
    stop(f"MG-11: the subject is {_landed} chars > 92: {subject!r}. "
         f"Shorten it by at least {_landed - 92} char(s).")
say(f"  MG-11: the subject LANDS at exactly {_landed} chars <= 92, no suffix appended by this tool")
if any(ord(c) > 127 for c in subject): stop(f"MG-11: squash subject is not ASCII: {subject!r}")
own = P["own_keys"]
# --- MG-3 needs an INDEPENDENT source for "this PR's own keys" ----------------------------------
# Measured here before this was written: with a COMPOSED body, the Refs line is GENERATED from
# own_keys, so `found == own` is very nearly a tautology and an own_keys of ["KS-9999"] passed the
# MG-3 check cleanly. It caught a foreign key planted in the PROSE and nothing else. The addendum
# is the gate's word about the key set; the PR body's own `Refs KS-####` lines are the AUTHOR's
# word, written before any GO existed. Requiring the two to agree is what makes the key set
# falsifiable. Measured agreement 10/10 across every PR in this seat's scope, 2026-09-25 18:4xZ.
d["body"] = open('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-08_gate74/merge_inputs/1422.pr_body_with_refs.DRAFT.txt', encoding="utf-8").read()  # DRAFTER SIMULATION: the PR body AS IF edited per Q-1422-REFS (a)
pr_refs = sorted(set(re.findall(r"Refs\s+(KS-\d+)", d.get("body") or "")))
if not pr_refs:
    stop("the PR body carries no `Refs KS-####` line, so the independent key-set instrument cannot "
         "run. A check that cannot run is not a pass: confirm the key set with Wednesday before merging.")
if pr_refs != sorted(set(own)):
    stop(f"the addendum's own_keys {sorted(set(own))} != the PR body's own Refs lines {pr_refs}. "
         f"The gate and the author disagree about what this PR is keyed to — STOP and mail.")
say(f"  own_keys {sorted(set(own))} == the PR body's independent Refs lines {pr_refs}")

# --- the provenance sentence. REQUIRED, and measured. -------------------------------------------
# This seat did not write any of these heads, so the note is a statement about another seat's work.
# There is no default: a default here would be a factual claim nobody measured.
note = P.get("merge_note")
if not note: stop("merge_note is REQUIRED in the addendum for this PR. This seat IS the author of the PRs "
                  "it merges, so the provenance sentence is a claim about my own work and its AUTHORITY "
                  "(Wednesday's signed GO under Kam's TESTED grant) and must be filled from the GO, never "
                  "defaulted.")
art = P.get("wrap_artefact")
if not art: stop("wrap_artefact is REQUIRED in the addendum for this PR: for an AUTHOR-MERGE name the "
                 "artefact carrying the AUTHORITY (the signed GO mail's id and date); for a merge of "
                 "another seat's work name the artefact that MEASURES that the author wrapped, or the word "
                 "UNMEASURED and what is being relied on instead.")
if art not in note: stop(f"wrap_artefact {art!r} does not appear in merge_note — the note must NAME the "
                         f"artefact it rests on, in the text that lands on develop")
SIGN = "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>\n"
# 🔴 HOISTED BY HAND, Seat B 54th — B 53rd's suppression governed ONLY the body_verbatim branch.
# The composed branch below still appended SIGN UNCONDITIONALLY, so a GO whose addendum takes the
# composed path would have landed the trailer the GO forbids. Read once, here, for both branches.
no_trailer = bool(P.get("no_trailer"))
if P.get("body_verbatim"):
    # The addendum prescribes the body text. It already carries its own Refs line(s), so none is
    # appended — a second Refs for the same key would be a duplicate MG-3 cannot distinguish from
    # a mistake.
    vb = P["body_verbatim"].strip()
    # A head commit message used as body_verbatim usually ALREADY ends with the Co-Authored-By
    # trailer, so appending SIGN unconditionally writes it twice. Measured: 3 of 3 verbatim squashes
    # carried it twice, while all 6 composed ones carried it once. Cosmetic, but it lands on develop
    # permanently, so the trailer is appended only when the body does not already carry one.
    has_sign = any(l.startswith("Co-Authored-By:") for l in vb.splitlines())
    # 🔴 ADDED BY HAND, Seat B 53rd — THE TOOL WAS ABOUT TO VIOLATE MY GO'S "NO TRAILER" CLAUSE,
    # AND THIS CORRECTS THE FLEET'S RECORD OF WHY B 52nd's TRAILER LANDED.
    # B 52nd reported that GitHub's squash merge HARVESTS Co-Authored-By from the squashed commits
    # "whatever body the API is given", and concluded a seat told NO TRAILER at GO time "can no
    # longer comply". Measured on their OWN artefacts: squash-body-1365.txt carries 0 trailers, but
    # merge47-1365-body.DRY.txt — the body the tool actually COMPOSED AND SENT — carries 1. The
    # append on the else branch below is where it came from. So the mechanism was at least partly
    # the TOOL, not necessarily GitHub, and a seat CAN comply: suppress the append.
    # Driven off the GO, never off preference: the addendum carries no_trailer only when the GO's
    # own line says NO TRAILER. When it does, the composed body is ASSERTED trailer-free, and the
    # un-suppressed path is proved still able to add one so the suppression is not vacuous.
    # no_trailer is read once above, so the composed branch sees it too.
    if no_trailer:
        body = vb + "\n\n" + note + "\n"
        _bad = [l for l in body.splitlines() if l.startswith("Co-Authored-By:")]
        assert not _bad, f"no_trailer was set but the composed body still carries {_bad}"
        _ctl = vb + "\n\n" + note + "\n\n" + SIGN
        assert any(l.startswith("Co-Authored-By:") for l in _ctl.splitlines()), \
            "CONTROL: the un-suppressed path no longer adds a trailer — suppression proves nothing"
        say("  squash body: VERBATIM from the gate addendum (its own Refs kept; none appended)"
            "; NO TRAILER per the GO — append SUPPRESSED, composed body asserted trailer-free, and"
            " the un-suppressed path proved still able to add one")
    else:
        body = vb + "\n\n" + note + ("\n" if has_sign else "\n\n" + SIGN)
        say("  squash body: VERBATIM from the gate addendum (its own Refs kept; none appended)"
            + ("; it already carries a Co-Authored-By trailer, so none is appended" if has_sign
               else "; trailer appended"))
else:
    parts = [P["ships_with"].strip()]
    if P.get("body_extra"): parts.append(P["body_extra"].strip())
    parts += [P["legs"].strip(), note,
              "\n".join(dict.fromkeys(f"Refs {k}" for k in own))]
    _base = "\n\n".join(parts)
    if no_trailer:
        body = _base + "\n"
        _bad = [l for l in body.splitlines() if l.startswith("Co-Authored-By:")]
        assert not _bad, f"no_trailer was set but the COMPOSED body still carries {_bad}"
        _ctl = _base + "\n\n" + SIGN
        assert any(l.startswith("Co-Authored-By:") for l in _ctl.splitlines()), \
            "CONTROL: the un-suppressed COMPOSED path no longer adds a trailer — suppression proves nothing"
        say("  squash body: COMPOSED from the gate addendum; NO TRAILER per the GO — append"
            " SUPPRESSED, composed body asserted trailer-free, and the un-suppressed path proved"
            " still able to add one")
    else:
        body = _base + "\n\n" + SIGN
        say("  squash body: COMPOSED from the gate addendum; trailer appended")

# --- MERGER-IDENTITY GATE ------------------------------------------------------------------------
# Two separate assertions, because they catch different things and a single regex catches neither
# cleanly (an earlier form here captured the whole clause after "Merged by" and refused its own
# correct text — a gate that cannot pass is as useless as one that cannot fail):
#   (i)  exactly ONE merger claim in the body, and the seat it names is THIS seat;
#   (ii) the ONLY seat names in the provenance note are this seat and whatever the REQUIRED,
#        quoted wrap_artefact itself contains. The artefact legitimately names the AUTHOR's seat
#        (a handover filename, a vault section title) and that is the point of quoting it; any
#        OTHER seat name in the note is a predecessor's name surviving a copy.
SEAT_TOKEN = re.compile(r"\bSeat\s+[A-Z]\w*(?:\s+\d+(?:st|nd|rd|th))?")
n_claims = body.count("Merged by ")
if n_claims != 1:
    stop(f"the body contains {n_claims} 'Merged by ' phrase(s), expected exactly 1")
after = body.split("Merged by ", 1)[1]
if not re.match(re.escape(A.seat) + r"\b", after):
    stop(f"the body says 'Merged by {after[:40]!r}...' but this seat is {A.seat!r} — a predecessor's "
         f"name surviving a copy would write a FALSE merger onto develop, permanently")
residual = [t for t in SEAT_TOKEN.findall(note.replace(art, "")) if t != A.seat]
if residual:
    stop(f"the provenance note names other seat(s) {sorted(set(residual))} outside the quoted wrap "
         f"artefact {art!r}. Only {A.seat!r} and the artefact's own text may name a seat here.")
say(f"  merger identity: exactly 1 'Merged by ' claim and it names {A.seat!r}; 0 other seat names in the "
    f"note outside the quoted artefact; wrap artefact {art!r} present in the note")

found = sorted(set(re.findall(r"KS-\d+", body)))
if found != sorted(set(own)):
    stop(f"MG-3: the body's hyphenated key set {found} != this PR's own keys {sorted(set(own))} "
         f"(a foreign key must be written un-hyphenated)")
# The GO's "write KS-932 as ks932" binds only IF the key is mentioned. A PRESENCE check would STOP
# on a body that simply never names it, which is the common case and not a defect. The real rule is
# that the HYPHENATED form must never appear, because that is what attaches a foreign ticket.
# Asserted as an absence, which fires.
for fk in P.get("foreign_keys_never_hyphenated", []):
    if re.search(re.escape(fk) + r"\b", body):
        stop(f"foreign key {fk} appears HYPHENATED in the body — it would attach that ticket; write it as "
             f"{fk.replace('-', '').lower()}")
say(f"  MG-11 subject {len(subject)} chars ASCII; MG-3 body key set {found} == own {sorted(set(own))}"
    + (f"; foreign keys asserted ABSENT in hyphenated form: {P.get('foreign_keys_never_hyphenated')}" if P.get("foreign_keys_never_hyphenated") else ""))

if A.dry:
    open(f"{R}/mergera1-{A.pr}-body.DRY.txt", "w").write(subject + "\n\n" + body)
    say(f"DRY #{A.pr}: every pre-merge assertion passed; predicted tree {pred}; body written to "
        f"mergera1-{A.pr}-body.DRY.txt ({len(body)} chars). NOTHING MERGED.")
    dump(); print(f"PREDICTED_TREE={pred}"); sys.exit(0)

# ---- 9. the merge, head PINNED ------------------------------------------------------------------
m = api(f"/pulls/{A.pr}/merge", "PUT", {"merge_method": "squash", "sha": P["head"],
                                        # 🔴 HAND-FIX, Seat D 6th, carried by Seat B 59th: the
                                        # subject EXACTLY. This tool appended " (#n)" itself --
                                        # the TOOL, not GitHub -- which is how "(#1375)" reached
                                        # develop permanently. A squash subject cannot be taken
                                        # back.
                                        "commit_title": subject, "commit_message": body})
if "_http" in m: stop(f"merge -> HTTP {m['_http']} {m['_body']}")
if not m.get("merged"): stop(f"not merged: {m}")
sq = m["sha"]
say(f"  MERGED #{A.pr} -> squash {sq}")

# ---- 10. verify at origin, by API only (no fetch, so no lock) -----------------------------------
new = git("ls-remote", "origin", "refs/heads/develop").split("\t")[0].strip()
if new != sq: stop(f"origin develop {new} != the squash {sq}")
c = api(f"/commits/{sq}")
if "_http" in c: stop(f"GET /commits/{sq} -> {c['_http']}")
if c["commit"]["tree"]["sha"] != pred: stop(f"the squash's tree {c['commit']['tree']['sha']} != predicted {pred}")
parents = [p["sha"] for p in c["parents"]]
if parents != [dev]: stop(f"the squash's parents {parents} != [the develop I predicted over {dev}]")
touched = sorted(f["filename"] for f in c.get("files", []))
# 🔴 FIXED BY HAND, Seat B 48th — THE SAME NO-OP GAP AS THE PRE-MERGE FILE-SET CHECK, one section on.
# I patched the prediction-side assertion and this one still refused, AFTER the merge had already
# happened and been verified correct: on gate48b the squash of #1355 touched 4 paths while its /files
# lists 5, because the preceding squash of #1354 had already landed the identical blob for
# systemTest/performance/package-lock.json. The merge was right and the check was wrong — which is
# the worst shape a post-merge assertion can have, because it reports a correct irreversible action
# as a failure. Subtract ONLY declared no-ops, exactly as the pre-merge check now does; an
# UNDECLARED missing path still trips this line.
expect_touched = sorted(set(files) - set(P.get("noop_paths", [])))
if touched != expect_touched:
    stop(f"the squash touched {touched}, not exactly the PR's paths minus declared no-ops "
         f"{expect_touched} (PR lists {files})")
if set(files) - set(expect_touched):
    say(f"  the squash touched {len(touched)} path(s); the {len(set(files) - set(expect_touched))} "
        f"declared no-op(s) are absent from it BY CONSTRUCTION, having landed identically earlier "
        f"in this batch")
blobs = {}
tr = api(f"/git/trees/{pred}?recursive=1")
if "_http" in tr: stop(f"GET /git/trees/{pred} -> {tr['_http']}")
for e in tr.get("tree", []):
    if e["type"] == "blob": blobs[e["path"]] = (e["sha"], e["mode"])
for path, (tb, tm) in P["targets"].items():
    got = blobs.get(path)
    if not got: stop(f"equality target {path} absent from the merged tree")
    if got[0] != tb or got[1] != tm: stop(f"equality target {path}: {got} != ({tb}, {tm})")
say(f"  VERIFIED at origin: develop == squash {sq[:12]}; tree == predicted {pred[:12]}; parent == {dev[:12]}; "
    f"{len(files)} path(s) touched, {len(P['targets'])} equality target(s) equal")
dump(); print(f"SQUASH={sq}"); print(f"PREDICTED_TREE={pred}")
