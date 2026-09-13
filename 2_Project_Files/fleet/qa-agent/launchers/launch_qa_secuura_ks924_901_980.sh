#!/bin/bash
# launch_qa_secuura_ks924_901_980.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on
# Secuura PR #980 (KS-924 / KS-901) @ 9c620f890: packages/shared `entrypoint-corpus.test.ts` — the corpus checker.
# KS-924: K1 pins the 27 contributing `root/name` packages as a SORTED LITERAL (a whole package vanishing reds by
# name; the floor `> 350` has a 29-file blind band at 380 walked and 23 of the 27 packages fit inside it); K2
# compares SKIP as a set (`[...SKIP].sort()` vs a sorted literal — a reorder no longer reds, `+'routes'` still
# does); K3 is the floor retitled to what it does. KS-901: three more express-binding shapes (`require('express')()`
# direct · assign-after-declare · `import('express').then(`) pinned FALSE (H-a6..H-a8, the reader NOT widened),
# three regexes in BLIND_SPOT_SHAPES, three plant cells P1..P3, the census title says "the EIGHT pinned shapes".
# Test-file only, +130 -14 (327 -> 443 lines, 22 -> 29 cells); `entrypoint-corpus.ts` UNCHANGED (blob a7abd31ef
# at base AND head). Round 1 on this PR. Plain PR -> v1: cut from M9 50b729d69 (#971's squash), its parent.
#
# #980's parent is 50b729d69 (= the GitHub compare merge-base, exit 10). origin develop MOVED ONCE after the PR was
# cut — 50b729d69 -> e91eb5bda at 17:37:11 AEST 2026-09-13 (#972's squash, KS-1052 r2: 9 files ALL under
# services/auth/src/, 5 of them walked-and-modified, the 2 added .ts under src/__tests__/ which the corpus SKIPs) — so
# the walked set stays 380 files / 27 packages and the eight-shape census stays [] on the merged tree (Wednesday
# re-derived all three at e91eb5bda from blobs, 18:00 AEST). A squash lands every ~12 minutes, so the develop pin
# below is DISJOINTNESS-CHECKED rather than bare: DEVELOP_SHA is the develop the brief's census and ratio were
# written against; if origin develop has moved past it, the GitHub compare of that delta is read and the launcher
# REFUSES (exit 18) only when the delta touches packages/shared/ (that changes the brief's expectations — #975, the
# sibling ks781 test, would: the ratio becomes 794/794), or adds a walked .ts in a package OUTSIDE K1's 27-name
# literal (K1 would red on the merged tree — a different brief), or empties a K1 package of every walked file it
# had at the pin, or takes the walked count to K3's floor (<= 350), or adds a line in a walked file matching one
# of the EIGHT pinned express shapes (the census would red), or cannot be judged (unreadable, not `ahead`, >250
# files); otherwise it proceeds and prints the move, its file count and the walked-set delta, which the gate
# re-states itself (brief items 2 and 7). A refusal means: confirm the new delta, re-state the census, re-pin
# DEVELOP_SHA here AND in the brief's TARGET section and the prompt — a different brief, a deliberate edit.
#
# Adapted from launch_qa_secuura_ks885_886_978.sh by gen_launcher_980.py (asserted substitutions, ONE asserted
# insertion — this PR's disjointness judge — residual guard): same guards and exit codes, re-pointed at #980.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks924_901_980.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA980_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-980-ks924-901-tier2.md}"
PROMPT_FILE="${QA980_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-980-ks924-901-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-924-ks-901-entrypoint-corpus-presence-set-and-three-shapes'
HEAD_SHA="${QA980_HEAD:-9c620f890fe844b48252b72d935257bfa8b151ba}"
MERGE_BASE='50b729d69c58474624508ed79d05c520dab22cc6'
DEVELOP_SHA='e91eb5bdaf68461e43a6055ed39137bd60a36749'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-980-ks924-901-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}))
print(json.load(r)["merge_base_commit"]["sha"])
PY
)"
[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read the merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }

# The develop pin, disjointness-checked (see the header). GUARDED = the files whose movement changes this brief.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (the develop the brief's census and ratio were written against; git ls-remote)"
else
  # The judge's Python is read OUTSIDE the command substitution (bash 3.2 cannot parse a quote-bearing
  # heredoc inside $( ... ); the regexes below carry ['"]). `read -d ''` returns 1 at EOF by design.
  read -r -d '' JUDGE_PY <<'PYJ' || true
import json, os, re, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["DEVELOP_SHA"] + "..." + os.environ["CUR_DEV"]
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = ["Blockchain/Dev/packages/shared/",
           "Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.ts"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
# entrypoint-corpus.ts's walk, re-implemented over paths: <root>/<pkg>/src/**/*.ts (not .d.ts), SKIP applied BELOW src.
ROOTS = ("services", "connectors"); SKIP = {"node_modules", "dist", "build", "coverage", ".git", "__tests__", "tests"}
# K1's 27 names with each package's walked-file count at the pinned develop (Wednesday's blob census); WALKED_AT_PIN = K3's input.
K1 = {"connectors/whatsapp-bot": 5, "services/analytics": 16, "services/anchoring": 19, "services/api-gateway": 33,
      "services/auth": 50, "services/billing": 10, "services/blockchain": 2, "services/demo-service": 31,
      "services/governance": 7, "services/guardian": 1, "services/kyc": 11, "services/m365-integration": 9,
      "services/mcp-server": 10, "services/nft-certificate": 20, "services/originate": 50, "services/prism": 6,
      "services/queue": 1, "services/referral": 16, "services/security": 10, "services/shared": 13,
      "services/staking": 10, "services/tenant-provisioning": 4, "services/timestamping": 7,
      "services/tokenisation": 6, "services/transfer": 10, "services/vc-issuer": 12, "services/wallet-connector": 11}
WALKED_AT_PIN = 380
def walked(p):
    q = p.split("/")
    return (len(q) >= 6 and q[0] == "Blockchain" and q[1] == "Dev" and q[2] in ROOTS and q[4] == "src"
            and not (set(q[5:-1]) & SKIP) and q[-1].endswith(".ts") and not q[-1].endswith(".d.ts"))
def pkg(p):
    q = p.split("/"); return q[2] + "/" + q[3]
added = [f["filename"] for f in files if f["status"] in ("added", "renamed", "copied") and walked(f["filename"])]
removed = [f.get("previous_filename") or f["filename"] for f in files
           if (f["status"] == "removed" and walked(f["filename"])) or (f["status"] == "renamed" and walked(f.get("previous_filename") or ""))]
modified = [f["filename"] for f in files if f["status"] in ("modified", "changed") and walked(f["filename"])]
newpkg = sorted({pkg(p) for p in added if pkg(p) not in K1})
gone = sorted(k for k in K1 if K1[k] > 0 and sum(1 for p in removed if pkg(p) == k) - sum(1 for p in added if pkg(p) == k) >= K1[k])
merged_count = WALKED_AT_PIN + len(added) - len(removed)
# the EIGHT pinned express shapes (BLIND_SPOT_SHAPES at head), scanned over the delta's ADDED lines in walked files
SHAPES = [("H-a1", re.compile(r"""import\s+[A-Za-z_$][\w$]*\s*=\s*require\(\s*['"]express['"]\s*\)""")),
          ("H-a2", re.compile(r"""require\(\s*['"]express['"]\s*\)\s*\.\s*default""")),
          ("H-a3", re.compile(r"""\{[^}]*\}\s*=\s*require\(\s*['"]express['"]\s*\)""")),
          ("H-a4", re.compile(r"""import\s*\{[^}]*\bdefault\s+as\b[^}]*\}\s*from\s*['"]express['"]""")),
          ("H-a5", re.compile(r"""await\s+import\(\s*['"]express['"]\s*\)""")),
          ("H-a6", re.compile(r"""require\(\s*['"]express['"]\s*\)\s*\(\s*\)""")),
          ("H-a7", re.compile(r"""^\s*[A-Za-z_$][\w$]*\s*=\s*require\(\s*['"]express['"]\s*\)""", re.M)),
          ("H-a8", re.compile(r"""import\(\s*['"]express['"]\s*\)\s*\.\s*then\s*\("""))]
shape_hits = []; nopatch = 0
for f in files:
    if f["filename"] not in added and f["filename"] not in modified: continue
    patch = f.get("patch") or ""
    if not patch: nopatch += 1; continue
    plus = "\n".join(l[1:] for l in patch.splitlines() if l.startswith("+") and not l.startswith("+++"))
    for label, rx in SHAPES:
        if rx.search(plus): shape_hits.append(f["filename"] + ":" + label)
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
if newpkg:
    print("NEWPKG " + " ".join(newpkg) + " (a package not in K1's 27-name literal contributes a walked file: K1 reds on the merged tree)"); sys.exit(0)
if gone:
    print("PKGGONE " + " ".join(gone) + " (a K1 package loses every walked file it had at the pin: K1 reds on the merged tree)"); sys.exit(0)
if merged_count <= 350:
    print("FLOOR walked=%d at the merged tree (K3's floor is > 350): K3 reds on the merged tree" % merged_count); sys.exit(0)
if shape_hits:
    print("SHAPE " + " ".join(sorted(shape_hits)) + " (an added line in a walked file matches a pinned express shape: the census reds on the merged tree)"); sys.exit(0)
print("DISJOINT commits=%d files=%d walked+%d/-%d modified=%d nopatch=%d merged-walked=%d" % (c["ahead_by"], len(files), len(added), len(removed), len(modified), nopatch, merged_count))
PYJ
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 -c "$JUDGE_PY"
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from packages/shared/ (both entrypoint-corpus files), adds no package outside K1's 27, empties none of them, keeps the walk above K3's floor and adds no pinned express shape in a walked file; the gate re-states the census on the merged tree (brief items 2 and 7)" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, re-state the census, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QA980_BRIEF:-}${QA980_PROMPT:-}${QA980_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
