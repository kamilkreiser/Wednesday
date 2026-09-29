#!/bin/bash
# launch_qa_nexusai_gate_batch10.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 10"), TWO members (+ two OPTIONAL),
# one verdict per ticket, ONE report (2026-09-29).
#   A — RD-733 (TIER 2, through-code, PLUS A REAL-BROWSER LEG — Tuesday's ruling): rd-733-user-access-stale-entra-check-s86m @ ed4c1bf, ONE commit on
#       faea66b (NOT forward-merged onto main f9cb440). The first-run User Access tab's dead auto-check (checkEntraStatus -> #check-entra-btn, an element no
#       page has) is REMOVED (-118/+5 in the page script), plus 4 jsdom cells, an rd465 comment, and 3 LOWERED counts in the rd200 brand-debt fixture.
#       Built by NexusAI-M. 4199/254.
#   B — RD-703 (TIER 2, through-code, test helper only): rd-703-wide-run-boundary-s86o @ bd8e8cd, ONE commit on dd15ce1. image-manifest.js reads an
#       ambiguous wide run by a boundary-character rule (Tuesday's ruling (a)); the parked rd699 BE cell is RE-ARMED (C-130); 10 new cells. Built by NexusAI-O. 4202/252.
#   Cross partner (C-68): RD-466 3f7e263 (queued; its image-content-exposure/rd418 consume B's helper) on MT2.
#   OPTIONAL — RD-707 (NexusAI-O, TIER 1) and RD-732 (NexusAI-M, TIER 2): NOT READY at drafting (no origin branch). Stamp P7_* / P32_* ONLY when a READY is on disk.
#   A and B share NO path but the counts file (guard 23). Predicted merged counts at M0 = f9cb440: MT1 (M0 + A + B) 4225/255; MT2 (+ 3f7e263) 4225/255.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch10' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch10.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's batch 10 commission (2026-09-29 ~19:0x AEST); READY mails copied in briefs/.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves a PR (C-190 is the merge
# authors' route); no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker. ONE browser leg (RD-733) against 127.0.0.1 only.
#
# PATTERN: launch_qa_nexusai_gate_batch9.sh (guard families 9 6 7 8 18 18b 22 93 94 95 96 97 92 23 35 70 80 31 39 10 17 60 11 12-15 20 19 24 53 71 76 77
# 78 79 81 38 32 40), prompt EMBEDDED, --check mode. CHANGES, each deliberate:
#   - 7/8: A's merge-base with main is faea66b; B's (and A x B's) is dd15ce1. Each chain is ONE commit on its base.
#   - 18b: main must be f9cb440 or a descendant; main's movement since f9cb440 touching a member path REFUSES; touching dom.js, the first-run page HTML
#     or any image-manifest requirer is a NOTE (C-68). NOTEs when main carries RD-466 or a queued merge, or when RD-707/RD-732 branches appear unstamped.
#   - 93: RD-733's premises (the removed timer + functions, the kept Analytics timer, the page ids, the fixture's three lowered counts and nothing else,
#     rd465 comment-only by a comment-stripped compare whose control fires, the four cells). 94: RD-703's premises (unwidenRuns, WIDE_RUN/unwiden kept,
#     the re-armed cell byte-identical to the parked one, the parked file inert at base, the 10 new cells, case 6's pin). 95: the census — the removed
#     functions have no caller in static/ or backend/ at the head (positive control at the parent). 96: C-187 does NOT apply (ICE 9ede5fd everywhere).
#     97: the browser leg's premises (Playwright in NexusAI node_modules; a Chromium-family binary on disk; the page's tab/list ids).
#   - 92: image-manifest's REQUIRE population (13 at dd15ce1 and f9cb440, 12 at bd8e8cd — the parked requirer removed).
#   - 80: a REAL merge-tree in a SCRATCH object dir under $TMPDIR (NexusAI's objects a read-only alternate). Pairs: main x A, main x B, A x B, A x 3f7e263,
#     B x 3f7e263. Each must merge clean or conflict on the counts file only.
#   - 60: the OPTIONAL members RD-707 / RD-732 — validated only when stamped; the prompt says "not a member" otherwise.
#   - 38: negative-control seats are a stamp placeholder until Tuesday stamps them (refuses via 32). 40: the routing line QA/NexusAI-batch10 must exist
#     (checked AFTER the stamp; Tuesday adds it to fleet/inbox_routing.conf). 32: SELF-CHECK stamp, LAST refusal before --check exits.
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §9); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, hash-object WITHOUT -w) plus
# merge-tree with a scratch GIT_OBJECT_DIRECTORY outside NexusAI; node/python over `git show` output; grep, ps, tmux, test -e.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch10.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..97 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

PH_STAMP='@STA''MP@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
BRIEF="$BRIEFS/2026-09-29_nexusai-gate-batch10-rd733-rd703.md"
READY_A="$BRIEFS/2026-09-29_nexusai-rd733-READY-mail.txt"
READY_B="$BRIEFS/2026-09-29_nexusai-rd703-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_M="$NX/session-tools/s86m"
EV_O="$NX/session-tools/s86o"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
RPTS="$QA_DIR/projects/nexusai/reports"
PREV_B9="$RPTS/2026-09-29-gate-batch9/report.md"
PREV_B9_BRIEF="$BRIEFS/2026-09-29_nexusai-gate-batch9-rd618r2-rd723.md"
B9_EV="$RPTS/2026-09-29-gate-batch9/evidence"
B7_EV="$RPTS/2026-09-29-gate-batch7/evidence"
PREV_FLOORLIB="$B9_EV/qa-floorlib.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-09-29-gate-batch10/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch10'

MAIN_SHA='f9cb44059401f560a9e72532b95705103354a7aa'      # origin main at drafting (19:08:17 and 19:16:19 AEST; = refs/pull/33/head, RD-204)
A_BASE='faea66b1bce5c17a2fef282c808821b3bf0825c6'        # RD-733's parent = merge-base(A, main)
B_BASE='dd15ce1ae8277cc9450e62b11b584a40d2226bf3'        # RD-703's parent = merge-base(B, main) = merge-base(A, B)
A_BRANCH='rd-733-user-access-stale-entra-check-s86m'
A_HEAD="${QA_A_HEAD_OVERRIDE:-ed4c1bfd5a195f163b8f76e84b467157f8b97813}"
B_BRANCH='rd-703-wide-run-boundary-s86o'
B_HEAD="${QA_B_HEAD_OVERRIDE:-bd8e8cdb4c7cd29706467a1e3dfa51591ecead69}"
X_BRANCH='rd-466-image-case-names-s86o'
X_SHA='3f7e263bf69f571d79aeae6ecc7b48ce6730d4c2'          # the cross partner (C-68) — pinned; a moved branch is a NOTE
# queued merges ahead of this batch — context only (NOTE if main carries one): RD-723, RD-618, 608a1cd, RD-685, RD-314, RD-700, RD-609, RD-648, RD-197
QUEUED='19fc17ca5aa41e3be3a6b9d174a5d627f4a33145 874c4f503d0f37a032014e562972b17e903e1072 608a1cd99adcc69f6d2cdc552f170e89710adb02 9d7076b0368f02ca030a904a2ce45de93739238e ce148d5d8332606654c189cd14f3aadee227a407 006b05609708bddeeea572ab5a1c7d404cbbe1dc 8f9d92197e0acf642b4fe2938673861e2a12c5aa b12a475fa73b439eea49cc9f692ef915af478253 43e729cbf056cd7ff064535372e7b2b2f23fcc5f'

# OPTIONAL members — Tuesday stamps these ONLY when a READY is on disk (full 40-hex head, branch, READY path). Empty = not a member.
P7_BRANCH=''    # RD-707 (NexusAI-O, TIER 1), expected rd-707-key-backup-copies-s86o, stacked on 3f7e263
P7_HEAD=''
P7_READY=''
P32_BRANCH=''   # RD-732 (NexusAI-M, TIER 2), expected rd-732-ip-address-10-7-2-s86m
P32_HEAD=''
P32_READY=''
P7_EXPECT_BRANCH='rd-707-key-backup-copies-s86o'
P32_EXPECT_BRANCH='rd-732-ip-address-10-7-2-s86m'

COUNTS_FILE='scripts/verify-expected-counts.json'
FRJS='static/js/first-run-setup.js'
FRHTML='static/first-run-setup.html'
DEBT='__tests__/fixtures/rd200-js-brand-debt.json'
R465='__tests__/rd465-first-run-open-window.test.js'
A_TEST='__tests__/rd733-user-access-no-stale-check.test.js'
RD200='__tests__/rd200-js-colour-corpus.test.js'
HELPER='__tests__/helpers/image-manifest.js'
R699='__tests__/rd699-decode-branches-behaviour.test.js'
PARKED='__tests__/helpers/rd703-parked-NOT-RUN/rd699-be-run-glue.test.js'
DOMJS='__tests__/helpers/dom.js'
ICE='__tests__/image-content-exposure.test.js'
FRJS_BASE_BLOB='bec7ae8350705f3b4a101eb490c2970321494ccf'      # faea66b, dd15ce1, f9cb440
FRJS_HEAD_BLOB='9d62976628daf6d26ae443564f01621083677e2b'      # ed4c1bf
FRHTML_BLOB='50be50910bf1a35212442ab4654b814694069a7d'
DEBT_BASE_BLOB='48965a5f6da1349fef74441be4bd52729d964cdc'
DEBT_HEAD_BLOB='18afe439dd930143e11f3574de2eae934c9981c7'
R465_BASE_BLOB='720e6b1a056945df139e9194ae3cc49f823e4f65'
R465_HEAD_BLOB='f16b811756f70ddcd37ec43197383c5434cff6e4'
A_TEST_BLOB='ce8963aabac1cbb4b98951248ae661d43141869a'
RD200_BLOB='5219fd5147e7357a9fe365829eb0b45b88cd57ae'
HELPER_BASE_BLOB='ceacc7f87b2289fca5be4141d33d5cf4c68f426a'    # dd15ce1, f9cb440, ed4c1bf, 3f7e263
HELPER_HEAD_BLOB='23bfa4fcf4976b139e101162fa4699497c4dc146'
R699_BASE_BLOB='df3ae5a92592b2fed71a5e1c6262790fae19fea8'
R699_HEAD_BLOB='2047c79564f9f484553853e8f7a3b1d89ac9e8d0'
PARKED_BLOB='cd66df567199e707c90a115f53d75b7c19e40946'
DOM_OLD_BLOB='04f182f51f5114844558dba73a9c674e056ed16a'        # faea66b, dd15ce1 (both members carry it)
DOM_MAIN_BLOB='3f913ff542d504c6f642f582c86d6d8711f1689f'       # f9cb440 (RD-204)
ICE_MAIN_BLOB='9ede5fd94a1bcf6e9ba18749418e23b7106e98da'
ICE_X_BLOB='7e3262b001088991f7b3660c0a2949139f80510a'
LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
A_EXPECTED_FILES="$FRJS
$A_TEST
$R465
$DEBT
$COUNTS_FILE"
B_EXPECTED_FILES="$HELPER
$R699
$PARKED
$COUNTS_FILE"
HELPER_POP_BASE='13'   # dd15ce1 and f9cb440 (incl. the parked file)
HELPER_POP_B='12'      # bd8e8cd
NEG_SEATS='62649 9959 38362 20317 64933'  # Tuesday stamps: NexusAI-M, -N, -O, -P and her own claude pid, space-separated, each named in the brief's §10 in backticks

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 10: RD-733 · RD-703'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch10] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, CodeQL at any head without a PR, any browser other than the one local Chromium-family run against a 127.0.0.1 server, the page as styled by its CDN stylesheets (blocked), a real Entra tenant, the npm registry, any deploy, docker, real Azure, Partner Center, the demo, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
helper_pop() { g grep -l -E "require\([^)]*image-manifest" "$1" -- __tests__ 2>/dev/null | wc -l | tr -d ' '; }
# rd465 "comment text only": strip // and /* */ comments, collapse whitespace, compare base vs head. Prints "equal ctl" (want "true false").
# Control: the head with one literal changed ('x'.repeat(64) -> 'x'.repeat(65)) must NOT compare equal.
comments_only() { node -e '
const cp=require("child_process");const [R,a,b,p]=process.argv.slice(1);
const rd=(s)=>cp.execFileSync("git",["-C",R,"show",s+":"+p]).toString();
const strip=(s)=>s.replace(/\/\*[\s\S]*?\*\//g,"").replace(/^\s*\/\/.*$/gm,"").replace(/\s+/g," ").trim();
const A=rd(a),B=rd(b);const M=B.replace("\x27x\x27.repeat(64)","\x27x\x27.repeat(65)");
const ctl=(M===B)||(strip(M)===strip(A));
console.log(String(strip(A)===strip(B))+" "+String(ctl));' "$REPO" "$1" "$2" "$3" 2>/dev/null; }
# the rd200 fixture: only three counts differ, as briefed. Prints "ok" or a reason.
debt_check() { python3 - "$REPO" "$A_BASE" "$A_HEAD" "$DEBT" <<'PY' 2>&1
import json,subprocess,sys
R,a,b,p=sys.argv[1:]
rd=lambda s: json.loads(subprocess.check_output(["git","-C",R,"show",f"{s}:{p}"]))
A,B=rd(a),rd(b)
ea,eb=A["entries"],B["entries"]
if len(ea)!=66 or len(eb)!=66: print(f"entries {len(ea)}/{len(eb)}, not 66/66"); sys.exit()
want={("first-run-setup.js","#28a745"):(16,15),("first-run-setup.js","#dc3545"):(2,1),("first-run-setup.js","#ffc107"):(5,4)}
diff={}
for x,y in zip(ea,eb):
    if {k:v for k,v in x.items() if k!="count"}!={k:v for k,v in y.items() if k!="count"}: print("an entry changed beyond its count:",x.get("file"),x.get("value")); sys.exit()
    if x["count"]!=y["count"]: diff[(x["file"],x["value"].lower())]=(x["count"],y["count"])
if diff!=want: print("count changes are",diff); sys.exit()
if {k:v for k,v in A.items() if k!="entries"}!={k:v for k,v in B.items() if k!="entries"}: print("a top-level key changed"); sys.exit()
ta,tb=sum(e["count"] for e in ea),sum(e["count"] for e in eb)
if (ta,tb)!=(147,144): print(f"totals {ta}/{tb}, not 147/144"); sys.exit()
print("ok")
PY
}
# the re-armed cell: its test block at the head's rd699 is byte-identical to the parked file's at dd15ce1 (4 lines).
rearm_block() { g show "$1" 2>/dev/null | awk '/test\(.and a run starting right after a word does not glue onto it either/{f=1} f{print} f&&/^    \}\);/{exit}'; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 10", with TWO members, one verdict per ticket and ONE report: RD-733 (TIER 2, through-code, PLUS A REAL-BROWSER LEG: the first-run setup page's User Access tab threw an uncaught TypeError from a dead auto-check that drives an element no page has, and the builder REMOVED the check, lowered three counts in the rd200 brand-debt fixture and added four jsdom cells) and RD-703 (TIER 2, through-code, test helper only: the wide-run reader every image-content gate uses now splits an ambiguous run at its non-alphanumeric boundary — Tuesday's ruling (a) — and a parked cell is re-armed). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve or merge a pull request; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker. Your ONE browser leg talks only to a server you boot on 127.0.0.1.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-29_nexusai-gate-batch10-rd733-rd703.md
It opens with TUESDAY'S RULINGS (a) to (g): apply them, do not re-rule them. Then the charter it names, then the two READY mails it names, then the batch 9 report it names (the most recent gate: a member joined by ADDENDUM mid-gate, main moved during the gate, S-2 a driver that called a function an older tree lacked, S-4 a wrong merge prediction, S-5 a census control that could not fire for its parent set, E-1 npm-audit red on every ref until RD-732). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE TARGETS. RD-733: branch rd-733-user-access-stale-entra-check-s86m at ed4c1bfd5a195f163b8f76e84b467157f8b97813, one commit on faea66b1bce5c17a2fef282c808821b3bf0825c6 (NOT forward-merged onto main). RD-703: rd-703-wide-run-boundary-s86o at bd8e8cdb4c7cd29706467a1e3dfa51591ecead69, one commit on dd15ce1ae8277cc9450e62b11b584a40d2226bf3. Main at drafting was f9cb44059401f560a9e72532b95705103354a7aa (RD-204 via PR #33). The two deltas share NO path but the counts file. RD-703's semantic cross is with RD-466 3f7e263bf69f571d79aeae6ecc7b48ce6730d4c2 (queued), whose changed cell files read text through RD-703's helper (C-68): keep that cross cell on a merged tree. OPTIONAL: RD-707 and RD-732 are members ONLY if the launcher's closing lines say so; otherwise report "RD-707: not a member" / "RD-732: not a member" and do not measure their OPTIONAL TARGET sections. A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines (batch 9's lesson).

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b): RD-723, RD-618, RD-466, batch 3 (RD-685, RD-314), batch 8 (RD-700, RD-609, RD-648) and P's RD-197 are queued. Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (MT1 = M0 + RD-733 + RD-703 predicted 4225/255 at M0 = f9cb440; MT2 = MT1 + 3f7e263 predicted 4225/255), the tests census (298 / 298), the helper's consumer set, which partners are already in. Main since RD-733's parent changed the jsdom dom helper that rd733 and rd465 load: re-run them on the merged tree (C-68). Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree and name any combined blob.

C-190: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code. You READ ONLY whether each branch has a PR and its CodeQL result; with no PR, CodeQL is NOT RUN at that head — say so. C-185 with its ADDENDUM: main's CI known-failing set is {rd638-export-always-ends E2, rd465 O-1 only with the checkEntraStatus TypeError}; O-1 leaves the set when RD-733 merges.

RD-733 (TIER 2 + browser). POSITIVE CONTROL FIRST: u1 RED-AT-PARENT (the four cells against the parent's page script: U1 red with the TypeError, the three controls green), then 4/4, the builder's M1 re-derived (u3) and your own mutants (u4: M-other, M-guard, M-val, M-rec). THE BROWSER LEG (w0-w7, Tuesday's ruling): a server booted from YOUR OWN K1 tree on 127.0.0.1 (open mode, a fresh data dir, under the network belt, killed in a finally by pid), a real Chromium-family browser driven by Playwright or your browser tool — Playwright's bundled Chromium is NOT installed on this machine; /Applications/Google Chrome.app is (channel: 'chrome'); NEVER download a browser. A route handler ABORTS and counts every request not to 127.0.0.1:<port> (the CDN stylesheets will be aborted). w0 LANDING CONTROLS first (version string, an aborted TEST-NET fetch, a same-origin 200, a thrown error caught by your pageerror listener). w1 RED AT MAIN: one pageerror "TypeError: Cannot set properties of null (setting 'disabled')" naming checkEntraStatus about 500 ms after clicking #tab-users; w2 the head: 0 pageerrors and 0 same-origin console errors; w3 classify console errors (same-origin vs the aborted CDN URLs); w4 the tab renders fully by DOM measurement; w5 the kept Re-validate path in the browser; w6 viewport pixels main vs head; w7 blob identity of every page file between the head and MT1. Screenshots of the User Access tab at main and head go in your evidence. PRIOR WORK p1-p4 (C-49): which commits removed or moved the button and why (the id pickaxe scoped to static/ is empty, unscoped it returns ed4c1bf itself), what the removed code wrote and who writes it now, whether any fetch or write past its first line ever ran (L-A4), and the READY's stated reasons — name anything user-facing lost, or say nothing was. THE FIXTURE f1-f6: each lowered count equals the guard's own measured count at the head; a plant adding one #28a745 back reddens RESOLVES; removing one more reddens NO ROT; the head's code with the parent's fixture reddens exactly the three; only three counts changed (C-40). rd465 O-1 k1-k4: green at head, and a DETERMINISTIC race (a 600 ms wait inserted at O-1's start in a copy) is RED at the parent with the TypeError and GREEN at the head; the users timer is gone; rd465's diff is comment text only. THE CENSUS c1-c3: the removed functions have no other caller in static/ or backend/, directly or by a data-csp-fn name, beside a positive control at the parent.

RD-703 (TIER 2). POSITIVE CONTROL FIRST, RED-AT-BASE (r1): the head's rd699 against the base helper — exactly {re-armed, case 1, case 2, case 3} red, quoting each received value. r2 21/21; r3 the builder's three mutants re-derived (M1 {re-armed, 1, 2}; M2 {3}; M3 {re-armed, 1, 2, case 4}); r4 your own mutants — M-both must redden "both ends letters or digits" (the both-ends-alphanumeric branch), and every survivor is a branch no cell sees; r5 THE DIFFERENTIAL: the base and head helper over every tracked text file the gates scan and a seeded generated corpus of at least 10,000 strings (LE, BE and UTF-32-in-a-string runs, Latin, Cyrillic, CJK, digit and punctuation boundaries) — every differing input must be the ambiguous shape or the BE trailing-space rule, anything else is a Major, and case 1 must appear in the diff as the positive control; r6 case 6 and case 4 pin today's output (C-98 — name it, do not re-rule); r7 C-130: the re-armed test is byte-identical to the parked one and the parked file was inert at the base; r8 C-68: every consumer of the helper by name at the head and on the merged trees, naming the difference from the READY's "15 suites, 388/388"; x1-x2 the cross cell with RD-466 on MT2.

THE MERGED TREE — part of every verdict (brief section 8). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff ed4c1bf, bd8e8cd (MT1); in a separate clone from MT1, merge --no-ff 3f7e263 (MT2) unless M0 already holds it. Re-measure every pair by merge-tree in a SCRATCH object dir first — the drafter's merge-trees: every member pair conflicted on the counts file only, and each member with RD-466 merged clean. Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MT1: predicted 4225/255, re-based on YOUR M0; the measurement decides. A second clone in reverse order, root trees identical apart from the counts file, the side control run inside the clone that owns the objects. The id-superset control LIKE WITH LIKE, all K1, a copy of batch 9's script proven first to STOP on a planted missing id: predicted missing 0 (C-187 does NOT apply to either member), new 15. On MT1, one hold: every C-68 set by name, rows u2, f1, f3, k1, k2, r2, r8, the full verify, one mutant per ticket; on MT2 x1-x2. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

THE NEGATIVE-ASSERTION SWEEP (brief section 3b, C-102). RD-733 removes a scheduled throw and RD-703 adds an early branch to how a wide run is read: for every negative cell among their callers, show it still reaches the check it is NAMED for, by coverage. Self-test first (a positive control, a negative control, a non-empty population) or ABORT. Report population, negative cells, still reaching, disarmed.

FULL VERIFY of each head and of MT1 through the lock, SESSION_SECRET UNSET, npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only. Predicted ed4c1bf 4199/254, bd8e8cd 4202/252, M0 = f9cb440 4210/254, MT1 4225/255. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-21 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-2: seed before, read raw. H-3: a LANDING CONTROL for every hook, route handler, listener, plant or mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-5: restore your own perturbations before any hash. H-6: every extractor and census gets a positive control; quote every path (the QA path has spaces and a bang); every server under the network belt with its landing control; the browser's belt is your route handler, proven by w0. H-7: mutants only through a quoted tool with a negative control. H-8: the exact new text present and the old absent once it is removed. H-9: byte-level plants via Buffer and xxd. H-10: prove the phenomenon reachable before measuring its absence. H-11: /bin/bash explicitly; every sha:path braced; never set -- or declare -A in the default shell. H-12: list every modified or deleted test file before the C-57 control, and every stale-parent file each member carries at an old blob. H-13: NUL-safe tree censuses. H-14: every driver ends with an END record or the run is VOID. H-15: preloads with -r in argv, never NODE_OPTIONS — no exception in this batch. H-16: a plant is what the product will treat it as. H-17: absolute tool paths, and prove the thing STARTED before reading its rc. H-18: zsh eats :s and a leading =; reject the empty-input hash as a VOID read. H-19: gitleaks canaries as real keys. H-20 (standing): EVERY jest invocation inside a hold carries --forceExit AND runs under a per-step hard deadline (qa-to.sh; targeted 600 s, the C-68 union 2400 s, a full verify 2700 s, each browser run 180 s); a fired deadline aborts that step, is reported by name, and the lock releases through your wrapper's own exit. H-21: every file you mutate is restored in a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, and its hash compared to the pinned blob after every hold; a tree left mutated is quarantined, never reused.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch10.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive, count-objects); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean, or merge-tree --write-tree without your own scratch object directory there, and never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold or serve scripts. Symlinks, chmod, sockets, held ports, browser profiles, env files and scratch git repos ONLY under your own mktemp dirs. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI, never merge anything anywhere the fleet can see. No Azure (no az at all), no demo, no docker, no npm registry, no CDN, no Entra tenant, no Partner Center. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 10 of the brief exactly. QUEUE, NEVER TAKE OVER: the NexusAI seats share session-tools/nexusai-lock.sh with you. Every jest run and every server boot goes through it with a tag starting qa-b10- (C-141 gate-class, ADDENDUM 2 and 3: each new qa ticket earns a fresh, self-applied yield). When a merge ticket is already queued, file yours with --after that merge ticket's tag (C-141 ADDENDUM 4's tool), never ahead of it; expect a busy queue. Hold the lock once per multi-run measurement as a tracked child of your seat. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying foreign in the same run (correct the stale ROOT and NEG defaults of batch 9's copied instrument first); record the foreign count beside every result; count the browser processes you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe, boot, browser run, request and jest run has a per-step DEADLINE and a client timeout, every server and browser is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

CI: whether either branch has a PR, its CodeQL result, and M0's CI Build and its failing set against C-185's known set, are UNVERIFIED by the drafter — read them with gh READ ONLY or say you could not. CI NOT RUN at a head with no PR. The npm-audit workflow's red on every ref (batch 9's E-1) is not a member's finding.

RE-PIN at start, mid and end: both branches, RD-466's branch, the queued merges, main, and whether RD-707/RD-732 branches exist — three timestamped readings with the branch name beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main MAY move: call main at your start M0 and say so; it must be f9cb440 or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch10. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch10] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch10/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 10: RD-733 · RD-703
Lead the body with one line per ticket (RD-733: <GO|GO WITH FINDINGS|NO GO> @ ed4c1bf (browser leg: main TypeError <n>, head errors <n>) · RD-703: … @ bd8e8cd · RD-707: … or not a member · RD-732: … or not a member), then one line naming M0, your recommended merge order, the merged counts you measured, rd465 O-1 (k2 red at the parent, green at the head?), the r5 differential's result, and the C-57 result. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's NOT TESTED list as the brief quotes it, every declared limit L-A1 to L-A5 and L-B1 to L-B4 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. C-18 (dead UI is removed, not hidden), C-40, C-98 and C-130 are the clarifications this batch leans on; C-102, C-112 and C-125 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, CodeQL at any head without a PR, any browser other than the one local Chromium-family run against a 127.0.0.1 server, the page as styled by its CDN stylesheets (blocked), a real Entra tenant, the npm registry, any deploy, docker, real Azure, Partner Center, the demo, and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
for S in "$A_HEAD" "$B_HEAD"; do
  [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$S' is not a full 40-hex sha" >&2; exit 9; }
done

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$MAIN_SHA" "$A_BASE" "$A_HEAD" "$B_BASE" "$B_HEAD" "$X_SHA" $QUEUED; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases: A's with main is faea66b; B's with main, and A x B, is dd15ce1; both bases are on main.
g merge-base --is-ancestor "$A_BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: faea66b is not an ancestor of f9cb440 — re-brief" >&2; exit 7; }
g merge-base --is-ancestor "$B_BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: dd15ce1 is not an ancestor of f9cb440 — re-brief" >&2; exit 7; }
[ "$(g merge-base "$A_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$A_BASE" ] || { echo "REFUSING: merge-base(ed4c1bf, f9cb440) is not faea66b — re-brief" >&2; exit 7; }
[ "$(g merge-base "$B_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$B_BASE" ] || { echo "REFUSING: merge-base(bd8e8cd, f9cb440) is not dd15ce1 — re-brief" >&2; exit 7; }
[ "$(g merge-base "$A_HEAD" "$B_HEAD" 2>/dev/null)" = "$B_BASE" ] || { echo "REFUSING: merge-base(ed4c1bf, bd8e8cd) is not dd15ce1 — re-brief" >&2; exit 7; }

# 8 — chains exact: each member is ONE commit on its base.
chainset() { g log --format='%H %P' "${1}..${2}" 2>&1 | sort | tr '\n' '|'; }
[ "$(chainset "$A_BASE" "$A_HEAD")" = "$A_HEAD $A_BASE|" ] || { echo "REFUSING: faea66b..RD-733 is not exactly one commit ed4c1bf on faea66b" >&2; exit 8; }
[ "$(chainset "$B_BASE" "$B_HEAD")" = "$B_HEAD $B_BASE|" ] || { echo "REFUSING: dd15ce1..RD-703 is not exactly one commit bd8e8cd on dd15ce1" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote: the two ticket branches exactly the pinned heads (REFUSE on mismatch); RD-466's branch a NOTE.
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
X_NOW="$(g ls-remote origin "refs/heads/$X_BRANCH" 2>/dev/null | awk '{print $1}')"
[ "$X_NOW" = "$X_SHA" ] || echo "NOTE: origin $X_BRANCH is '${X_NOW:-absent}', not 3f7e263 — the cross cell stays pinned on 3f7e263; the gate names the move (C-68)" >&2
for PAIR in "$P7_EXPECT_BRANCH RD-707 P7" "$P32_EXPECT_BRANCH RD-732 P32"; do
  read -r OBR ONAME OTAG <<<"$PAIR"
  NOWO="$(g ls-remote origin "refs/heads/$OBR" 2>/dev/null | awk '{print $1}')"
  if [ -n "$NOWO" ]; then
    case "$OTAG" in P7) ST="$P7_HEAD" ;; *) ST="$P32_HEAD" ;; esac
    [ -n "$ST" ] || echo "NOTE: origin now has refs/heads/$OBR = ${NOWO:0:7} ($ONAME) but ${OTAG}_HEAD is not stamped — $ONAME is NOT a member unless Tuesday stamps it" >&2
  fi
done
# 18b — main MAY move (ruling b). It must be f9cb440 or a descendant IN THE OBJECT STORE; its movement since f9cb440 must not touch a member path.
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}')" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from f9cb440 — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — a member merged before its gate; re-brief" >&2; exit 18; fi
done
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$FRJS" "$A_TEST" "$R465" "$DEBT" "$HELPER" "$R699" "$PARKED" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved f9cb440..${M_ORIGIN:0:7} and touched a member path: $HIT — re-brief" >&2; exit 18; }
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from f9cb440) — the gate re-pins M0 itself and re-bases every prediction" >&2
printf '%s\n' "$MOVED" | grep -qxF "$DOMJS" && echo "NOTE: main's movement changes the jsdom dom helper again — rd733/rd465 run under it on M0 (C-68)" >&2
printf '%s\n' "$MOVED" | grep -qxF "$FRHTML" && echo "NOTE: main's movement changes the first-run page HTML — the browser leg's main arm and the jsdom cells read a page neither head carried (C-68)" >&2
HREQ="$(g grep -l -E "require\([^)]*image-manifest" "$M_ORIGIN" -- __tests__ 2>/dev/null | sed "s/^${M_ORIGIN}://" | sort -u)"
HM="$(comm -12 <(printf '%s\n' "$HREQ" | sed '/^$/d') <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HM" ] || echo "NOTE: main's movement changes image-manifest consumer(s): $HM— RD-703's C-68 set runs on them (C-68)" >&2
Q_IN=''
for H in $QUEUED "$X_SHA"; do g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null && Q_IN="$Q_IN ${H:0:7}"; done
[ -z "$Q_IN" ] || echo "NOTE: origin main carries queued/partner commit(s):$Q_IN — the gate re-bases counts, census and C-68 populations on M0" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed; the only product path is A's page script; B touches no product path.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$A_BASE" "$A_HEAD" "$A_EXPECTED_FILES" "RD-733 (faea66b..ed4c1bf)"
chk_delta "$B_BASE" "$B_HEAD" "$B_EXPECTED_FILES" "RD-703 (dd15ce1..bd8e8cd)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$A_BASE" "$A_HEAD" "$FRJS")" = "5 118" ] && [ "$(ns "$A_BASE" "$A_HEAD" "$A_TEST")" = "97 0" ] && [ "$(ns "$A_BASE" "$A_HEAD" "$R465")" = "4 3" ] && [ "$(ns "$A_BASE" "$A_HEAD" "$DEBT")" = "3 3" ] || { echo "REFUSING: RD-733's numstats are not page script +5/-118, cells +97, rd465 +4/-3, fixture +3/-3" >&2; exit 22; }
[ "$(ns "$B_BASE" "$B_HEAD" "$HELPER")" = "38 1" ] && [ "$(ns "$B_BASE" "$B_HEAD" "$R699")" = "59 4" ] && [ "$(ns "$B_BASE" "$B_HEAD" "$PARKED")" = "0 28" ] || { echo "REFUSING: RD-703's numstats are not helper +38/-1, rd699 +59/-4, parked -28" >&2; exit 22; }
[ -z "$(g diff --name-only "$B_BASE" "$B_HEAD" -- backend static docs Dockerfile .dockerignore package.json package-lock.json 2>/dev/null)" ] || { echo "REFUSING: RD-703 touches a product, docs, image or package path — commissioned as test-helper only" >&2; exit 22; }
[ -z "$(g diff --name-only "$A_BASE" "$A_HEAD" -- backend docs Dockerfile .dockerignore package.json package-lock.json 2>/dev/null)" ] && [ "$(g diff --name-only "$A_BASE" "$A_HEAD" -- static 2>/dev/null)" = "$FRJS" ] || { echo "REFUSING: RD-733's product change is not exactly the first-run page script" >&2; exit 22; }

# 93 — RD-733's premises at source.
[ "$(cnt "$A_BASE" "$FRJS" 'async function checkEntraStatus()')" = "1" ] && [ "$(cnt "$A_HEAD" "$FRJS" 'async function checkEntraStatus()')" = "0" ] || { echo "REFUSING: checkEntraStatus is not defined once at faea66b and absent at ed4c1bf" >&2; exit 93; }
[ "$(cnt "$A_BASE" "$FRJS" 'function updateEntraComponent(')" = "1" ] && [ "$(cnt "$A_HEAD" "$FRJS" 'function updateEntraComponent(')" = "0" ] || { echo "REFUSING: updateEntraComponent is not defined once at faea66b and absent at ed4c1bf" >&2; exit 93; }
[ "$(cnt "$A_BASE" "$FRJS" 'setTimeout(() => checkEntraStatus(), 500);')" = "1" ] && [ "$(cnt "$A_HEAD" "$FRJS" 'setTimeout(() => checkEntraStatus(), 500);')" = "0" ] || { echo "REFUSING: the users-branch 500 ms timer is not present at faea66b and gone at ed4c1bf" >&2; exit 93; }
[ "$(cnt "$A_BASE" "$FRJS" 'setTimeout(() => loadDataSources(), 300);')" = "1" ] && [ "$(cnt "$A_HEAD" "$FRJS" 'setTimeout(() => loadDataSources(), 300);')" = "1" ] || { echo "REFUSING: the Analytics 300 ms timer (CTRL-REC's premise) is not present once at both" >&2; exit 93; }
[ "$(cnt "$A_BASE" "$FRJS" "const btn = document.getElementById('check-entra-btn');")" = "1" ] || { echo "REFUSING: faea66b's checkEntraStatus does not read #check-entra-btn as briefed" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$FRJS" 'revalidateEntraConfig')" -ge 1 ] || { echo "REFUSING: revalidateEntraConfig (KEPT) is absent at ed4c1bf" >&2; exit 93; }
for S in "$A_BASE" "$A_HEAD"; do
  [ "$(cnt "$S" "$FRHTML" 'id="check-entra-btn"')" = "0" ] && [ "$(cnt "$S" "$FRHTML" 'id="entra-status-list"')" = "1" ] && [ "$(cnt "$S" "$FRHTML" 'id="tab-users"')" = "1" ] && [ "$(cnt "$S" "$FRHTML" 'id="section-users"')" = "1" ] || { echo "REFUSING: the first-run page HTML at ${S:0:7} is not as briefed (no #check-entra-btn; one #entra-status-list, #tab-users, #section-users)" >&2; exit 93; }
done
[ "$(blob "$A_BASE" "$FRJS")" = "$FRJS_BASE_BLOB" ] && [ "$(blob "$MAIN_SHA" "$FRJS")" = "$FRJS_BASE_BLOB" ] && [ "$(blob "$A_HEAD" "$FRJS")" = "$FRJS_HEAD_BLOB" ] || { echo "REFUSING: page-script blobs are not bec7ae8 (faea66b, f9cb440) -> 9d62976 (ed4c1bf)" >&2; exit 93; }
[ "$(blob "$A_BASE" "$FRHTML")" = "$FRHTML_BLOB" ] && [ "$(blob "$A_HEAD" "$FRHTML")" = "$FRHTML_BLOB" ] && [ "$(blob "$MAIN_SHA" "$FRHTML")" = "$FRHTML_BLOB" ] || { echo "REFUSING: first-run page HTML is not 50be509 at faea66b, ed4c1bf and f9cb440" >&2; exit 93; }
[ "$(blob "$A_BASE" "$DEBT")" = "$DEBT_BASE_BLOB" ] && [ "$(blob "$A_HEAD" "$DEBT")" = "$DEBT_HEAD_BLOB" ] && [ "$(blob "$A_HEAD" "$RD200")" = "$RD200_BLOB" ] && [ "$(blob "$MAIN_SHA" "$RD200")" = "$RD200_BLOB" ] || { echo "REFUSING: fixture/rd200 blobs are not 48965a5 -> 18afe43 with rd200's cell 5219fd5 unchanged" >&2; exit 93; }
DC="$(debt_check)"; [ "$DC" = "ok" ] || { echo "REFUSING: the rd200 debt fixture change is not exactly #28a745 16->15, #dc3545 2->1, #ffc107 5->4 (totals 147->144, 66 entries): $DC" >&2; exit 93; }
[ "$(comments_only "$A_BASE" "$A_HEAD" "$R465")" = "true false" ] || { echo "REFUSING: rd465's change is not comment text only (or the compare's control did not fire)" >&2; exit 93; }
[ "$(blob "$A_BASE" "$R465")" = "$R465_BASE_BLOB" ] && [ "$(blob "$A_HEAD" "$R465")" = "$R465_HEAD_BLOB" ] && [ "$(blob "$A_HEAD" "$A_TEST")" = "$A_TEST_BLOB" ] || { echo "REFUSING: rd465 / rd733 blobs are not 720e6b1 -> f16b811 / ce8963a" >&2; exit 93; }
for T in "test('U1 — " "test('CTRL-REC — " "test('CTRL-TAB — " "test('CTRL-VAL — "; do
  [ "$(cnt "$A_HEAD" "$A_TEST" "$T")" = "1" ] || { echo "REFUSING: rd733 cell '$T' is not present once at ed4c1bf" >&2; exit 93; }
done
[ "$(cnt "$A_HEAD" "$R465" "test('Turn on Authentication Control: success removes the banner'")" = "1" ] || { echo "REFUSING: rd465 O-1's cell title is not as C-185's ADDENDUM names it" >&2; exit 93; }
[ "$(blob "$M_ORIGIN" "$FRJS")" = "$FRJS_BASE_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s page script is not bec7ae8 — the browser leg's main arm then differs from the parent's; run both (brief w1)" >&2

# 94 — RD-703's premises at source.
[ "$(cnt "$B_HEAD" "$HELPER" 'function unwidenRuns(text) {')" = "1" ] && [ "$(cnt "$B_BASE" "$HELPER" 'function unwidenRuns(text) {')" = "0" ] || { echo "REFUSING: unwidenRuns is not new at bd8e8cd" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$HELPER" "return unwidenRuns(text).split(NUL).join(' ');")" = "1" ] && [ "$(cnt "$B_BASE" "$HELPER" "return text.replace(WIDE_RUN, unwiden).split(NUL).join(' ');")" = "1" ] || { echo "REFUSING: scannableText's last line is not text.replace(WIDE_RUN, unwiden) -> unwidenRuns(text) as briefed" >&2; exit 94; }
DEL="$(g diff "$B_BASE" "$B_HEAD" -- "$HELPER" 2>/dev/null | grep '^-' | grep -v '^---')"
[ "$(printf '%s\n' "$DEL" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && printf '%s\n' "$DEL" | grep -qF 'text.replace(WIDE_RUN, unwiden)' || { echo "REFUSING: the helper's only removed line is not the old WIDE_RUN replace (WIDE_RUN/unwiden must be KEPT)" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$HELPER" 'const ALNUM = /[\p{L}\p{N}]/u;')" = "1" ] && [ "$(cnt "$B_HEAD" "$HELPER" 'WIDE_RUN.lastIndex = end;')" = "1" ] || { echo "REFUSING: ALNUM / the lastIndex advance are not as briefed" >&2; exit 94; }
RA="$(rearm_block "${B_BASE}:${PARKED}")"; RB="$(rearm_block "${B_HEAD}:${R699}")"
[ -n "$RA" ] && [ "$RA" = "$RB" ] && [ "$(printf '%s\n' "$RB" | wc -l | tr -d ' ')" = "4" ] || { echo "REFUSING: the re-armed cell at bd8e8cd is not byte-identical (4 lines) to the parked cell at dd15ce1 (C-130)" >&2; exit 94; }
[ "$(rearm_block "${B_BASE}:${R699}" | wc -c | tr -d ' ')" = "0" ] || { echo "REFUSING: the re-armed cell already exists in dd15ce1's rd699 — the extractor's premise fails" >&2; exit 94; }
[ "$(blob "$B_BASE" "$PARKED")" = "$PARKED_BLOB" ] && ! g cat-file -e "${B_HEAD}:${PARKED}" 2>/dev/null || { echo "REFUSING: the parked file is not cd66df5 at dd15ce1 and absent at bd8e8cd" >&2; exit 94; }
[ "$(g show "${B_BASE}:package.json" 2>/dev/null | grep -cF '"/__tests__/helpers/"')" -ge 1 ] || { echo "REFUSING: dd15ce1's jest config does not ignore /__tests__/helpers/ — the parked file's inertness premise fails" >&2; exit 94; }
for T in "test('case 1 — " "test('case 2 — " "test('case 3 — " "test('case 4 (control) — " "test('case 5 (control; both ends letters) — " "test('both ends letters or digits — " \
         "test('neither end a letter or digit — " "test('case 7 (control) — " "test('case 8 (control) — " "test('case 6 — STATED LIMIT"; do
  [ "$(cnt "$B_HEAD" "$R699" "$T")" = "1" ] && [ "$(cnt "$B_BASE" "$R699" "$T")" = "0" ] || { echo "REFUSING: rd699 cell '$T' is not new once at bd8e8cd" >&2; exit 94; }
done
[ "$(cnt "$B_HEAD" "$R699" "toBe('abcxy z')")" = "1" ] || { echo "REFUSING: case 6's stated-limit pin 'abcxy z' is not as briefed" >&2; exit 94; }
[ "$(blob "$B_BASE" "$HELPER")" = "$HELPER_BASE_BLOB" ] && [ "$(blob "$B_HEAD" "$HELPER")" = "$HELPER_HEAD_BLOB" ] && [ "$(blob "$MAIN_SHA" "$HELPER")" = "$HELPER_BASE_BLOB" ] && [ "$(blob "$A_HEAD" "$HELPER")" = "$HELPER_BASE_BLOB" ] && [ "$(blob "$X_SHA" "$HELPER")" = "$HELPER_BASE_BLOB" ] || { echo "REFUSING: helper blobs are not ceacc7f (dd15ce1, f9cb440, ed4c1bf, 3f7e263) -> 23bfa4f (bd8e8cd)" >&2; exit 94; }
[ "$(blob "$B_BASE" "$R699")" = "$R699_BASE_BLOB" ] && [ "$(blob "$B_HEAD" "$R699")" = "$R699_HEAD_BLOB" ] && [ "$(blob "$MAIN_SHA" "$R699")" = "$R699_BASE_BLOB" ] || { echo "REFUSING: rd699 blobs are not df3ae5a (dd15ce1, f9cb440) -> 2047c79 (bd8e8cd)" >&2; exit 94; }
[ "$(blob "$M_ORIGIN" "$HELPER")" = "$HELPER_BASE_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s image-manifest helper is not ceacc7f — RD-703 merges into a combined helper (C-68)" >&2

# 95 — CENSUS: the removed functions have no other caller in static/ or backend/ at the head (positive control at the parent).
CEN_H="$(g grep -n -E 'checkEntraStatus|updateEntraComponent' "$A_HEAD" -- static backend 2>/dev/null | sed "s/^${A_HEAD}://")"
CEN_P="$(g grep -n -E 'checkEntraStatus|updateEntraComponent' "$A_BASE" -- static backend 2>/dev/null | wc -l | tr -d ' ')"
[ "$CEN_P" -ge 5 ] || { echo "REFUSING: the census's positive control at faea66b found $CEN_P line(s), not >= 5 — the census cannot be trusted" >&2; exit 95; }
[ "$(printf '%s\n' "$CEN_H" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && printf '%s\n' "$CEN_H" | grep -qE "^${FRJS}:[0-9]+:[[:space:]]*//" || { echo "REFUSING: at ed4c1bf a removed function is still named outside one comment line in the page script:" >&2; printf '%s\n' "$CEN_H" >&2; exit 95; }
[ "$(g grep -c -E 'data-csp-fn="(checkEntraStatus|updateEntraComponent)"' "$A_HEAD" -- static 2>/dev/null | wc -l | tr -d ' ')" = "0" ] && [ "$(g grep -c -F 'data-csp-fn="switchSection"' "$A_HEAD" -- "$FRHTML" 2>/dev/null | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: a data-csp-fn names a removed function at ed4c1bf (or the switchSection control is absent)" >&2; exit 95; }

# 96 — C-187 does NOT apply: image-content-exposure is main's blob on both members; RD-466 carries its own.
[ "$(blob "$MAIN_SHA" "$ICE")" = "$ICE_MAIN_BLOB" ] && [ "$(blob "$A_HEAD" "$ICE")" = "$ICE_MAIN_BLOB" ] && [ "$(blob "$B_HEAD" "$ICE")" = "$ICE_MAIN_BLOB" ] && [ "$(blob "$X_SHA" "$ICE")" = "$ICE_X_BLOB" ] || { echo "REFUSING: image-content-exposure blobs are not 9ede5fd (f9cb440, ed4c1bf, bd8e8cd) / 7e3262b (3f7e263) — ruling (d)'s premise" >&2; exit 96; }
[ "$(blob "$M_ORIGIN" "$ICE")" = "$ICE_MAIN_BLOB" ] || echo "NOTE: image-content-exposure on origin main ${M_ORIGIN:0:7} is not 9ede5fd (RD-466 landed?) — C-187's ADDENDUM governs any 1904765-cut merge; neither member is one" >&2
[ "$(blob "$A_BASE" "$DOMJS")" = "$DOM_OLD_BLOB" ] && [ "$(blob "$A_HEAD" "$DOMJS")" = "$DOM_OLD_BLOB" ] && [ "$(blob "$B_HEAD" "$DOMJS")" = "$DOM_OLD_BLOB" ] && [ "$(blob "$MAIN_SHA" "$DOMJS")" = "$DOM_MAIN_BLOB" ] || { echo "REFUSING: dom.js blobs are not 04f182f (both members) / 3f913ff (f9cb440) — the C-68 premise of brief §1" >&2; exit 96; }

# 97 — the browser leg's premises: Playwright in NexusAI's node_modules and a Chromium-family binary on disk (NEVER a download).
PW_VER="$(node -e 'try{console.log(require(process.argv[1]+"/node_modules/@playwright/test/package.json").version)}catch(e){console.log("")}' "$REPO" 2>/dev/null)"
[ -n "$PW_VER" ] || { echo "REFUSING: @playwright/test is not in $REPO/node_modules — the browser leg (Tuesday's ruling) would need a download" >&2; exit 97; }
PW_EXE="$(node -e 'try{const e=require(process.argv[1]+"/node_modules/playwright").chromium.executablePath();console.log(require("fs").existsSync(e)?e:"")}catch(e){console.log("")}' "$REPO" 2>/dev/null)"
CHROME_APP='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
if [ -z "$PW_EXE" ] && [ ! -x "$CHROME_APP" ]; then echo "REFUSING: neither Playwright's bundled Chromium nor $CHROME_APP is on disk — the browser leg cannot run without a download" >&2; exit 97; fi
[ -n "$PW_EXE" ] || echo "NOTE: Playwright's bundled Chromium is absent; the gate uses channel 'chrome' ($CHROME_APP) — brief w-rows" >&2
[ "$(cnt "$A_HEAD" "$FRHTML" 'data-arg="users"')" -ge 1 ] || { echo "REFUSING: #tab-users does not switch to 'users' by data-arg at ed4c1bf" >&2; exit 97; }

# 92 — image-manifest's REQUIRE population (not a name grep): 13 at dd15ce1 and f9cb440, 12 at bd8e8cd; rd699 among them; main-now noted.
[ "$(helper_pop "$B_BASE")" = "$HELPER_POP_BASE" ] && [ "$(helper_pop "$MAIN_SHA")" = "$HELPER_POP_BASE" ] && [ "$(helper_pop "$B_HEAD")" = "$HELPER_POP_B" ] || { echo "REFUSING: image-manifest require-population is not 13 (dd15ce1, f9cb440) / 12 (bd8e8cd) — re-brief" >&2; exit 92; }
g grep -l -E "require\([^)]*image-manifest" "$B_HEAD" -- "$R699" >/dev/null 2>&1 || { echo "REFUSING: rd699 does not require image-manifest at bd8e8cd (the census's positive control)" >&2; exit 92; }
HP_NOW="$(helper_pop "$M_ORIGIN")"
[ "$HP_NOW" = "$HELPER_POP_BASE" ] || echo "NOTE: at origin main ${M_ORIGIN:0:7} the image-manifest require-population is ${HP_NOW:-?} (brief: 13 at f9cb440) — the gate re-derives it on M0" >&2

# 23 — EXPECTED OVERLAPS: A's and B's deltas share the counts file and nothing else.
COMMON="$(comm -12 <(g diff --name-only "$A_BASE" "$A_HEAD" 2>/dev/null | sort) <(g diff --name-only "$B_BASE" "$B_HEAD" 2>/dev/null | sort) | sed '/^$/d' | tr '\n' ' ' | sed 's/ $//')"
[ "$COMMON" = "$COUNTS_FILE" ] || { echo "REFUSING: RD-733 and RD-703 share '${COMMON:-<nothing>}', expected '$COUNTS_FILE' only" >&2; exit 23; }

# 35 — counts at every pinned sha.
for PAIR in "$A_BASE 4195 253" "$A_HEAD 4199 254" "$B_BASE 4191 252" "$B_HEAD 4202 252" "$MAIN_SHA 4210 254" "$X_SHA 4191 252"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree), main-now included.
for S in "$A_BASE" "$B_BASE" "$MAIN_SHA" "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$X_SHA"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 80 — the merge premise by a REAL merge-tree in a scratch object dir OUTSIDE NexusAI (NexusAI's objects are a read-only alternate).
MT_OBJ="$(mktemp -d "${TMPDIR:-/tmp}/qa-b10-mergetree.XXXXXX")" || { echo "REFUSING: cannot make a scratch object dir for guard 80" >&2; exit 80; }
mtree() { GIT_OBJECT_DIRECTORY="$MT_OBJ" GIT_ALTERNATE_OBJECT_DIRECTORIES="$REPO/.git/objects" git -C "$REPO" merge-tree --write-tree --name-only "$1" "$2" 2>&1; }
for PAIR in "$M_ORIGIN $A_HEAD" "$M_ORIGIN $B_HEAD" "$A_HEAD $B_HEAD" "$A_HEAD $X_SHA" "$B_HEAD $X_SHA"; do
  X="${PAIR%% *}"; Y="${PAIR#* }"
  OUT="$(mtree "$X" "$Y")"; RC=$?
  CONF="$(printf '%s\n' "$OUT" | sed -n '2,/^$/p' | sed '/^$/d' | tr '\n' ' ' | sed 's/ $//')"
  { [ "$RC" = "0" ] && [ -z "$CONF" ]; } || { [ "$RC" = "1" ] && [ "$CONF" = "$COUNTS_FILE" ]; } || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} rc=$RC conflicted '${CONF:-?}' — not counts-only (80); scratch objects in $MT_OBJ" >&2; exit 80; }
done
[ -d "$REPO/.git/objects" ] || { echo "REFUSING: $REPO/.git/objects is not a directory — the alternate would be wrong" >&2; exit 80; }

# 31 — builder evidence, prior reports, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$CLAR" "$PREV_B9" "$PREV_B9_BRIEF" \
         "$EV_M/rd733-hold.log" "$EV_M/rd733-hold.sh" "$EV_M/rd733-hold.run1.log" "$EV_M/rd733-verify.log" "$EV_M/rd733-verify.sh" "$EV_M/rd733-serve.sh" \
         "$EV_M/rd733-fixed-first-run-setup.js.keep" "$EV_M/rd733-evidence/browser-check.txt" "$EV_M/rd733-evidence/rd733-before-main-faea66b-user-access.png" \
         "$EV_M/rd733-evidence/rd733-after-fix-user-access.png" "$EV_M/rd733-evidence/rd733-after-fix-user-access-full.png" \
         "$EV_O/rd703-hold.log" "$EV_O/rd703-hold.sh" "$EV_O/rd703-measure.js" "$EV_O/rd703-measure-dd15ce1.txt" "$EV_O/rd703-measure-fixed.txt" \
         "$EV_O/rd703-red.json" "$EV_O/rd703-green.json" "$EV_O/rd703-M1-no-boundary-rule.json" "$EV_O/rd703-M2-no-BE-trailing-space.json" \
         "$EV_O/rd703-M3-boundary-rule-inverted.json" "$EV_O/rd703-c68.json" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$B9_EV/qa-floorlib.sh" "$B9_EV/qa-floorcount.py" "$B9_EV/qa-to.sh" "$B9_EV/qa-holdlib.sh" "$B9_EV/qa-jestwrap.sh" "$B9_EV/qa-runj9.sh" \
         "$B9_EV/qa-mut9.py" "$B9_EV/qa-mutlib9.sh" "$B9_EV/qa-merge9.sh" "$B9_EV/qa-c57-id-superset.sh" "$B9_EV/qa-c112-census.py" "$B9_EV/qa-h1-selftest.sh" \
         "$B9_EV/qa-h1-scan.py" "$B9_EV/qa-jsum.js" "$B9_EV/qa-mail.py" "$B9_EV/qa-ssprint.sh" "$B9_EV/qa-netbelt.sb" "$B9_EV/qa-netbelt-ctl.js" "$B9_EV/qa-cov9.js" \
         "$B7_EV/qa-srvlib.js" "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "$A_HEAD" "$READY_A" || { echo "REFUSING: the RD-733 READY does not name $A_HEAD" >&2; exit 31; }
grep -qF "$B_HEAD" "$READY_B" || { echo "REFUSING: the RD-703 READY does not name $B_HEAD" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4199/4199 tests passed across 254 suites' "$EV_M/rd733-verify.log" && grep -qF 'VERDICT: PASS — 4202/4202 tests passed across 252 suites' "$EV_O/rd703-hold.log" && grep -qF "TypeError: Cannot set properties of null (setting 'disabled')" "$EV_M/rd733-evidence/browser-check.txt" || { echo "REFUSING: a builder log no longer carries the READY's result line" >&2; exit 31; }
[ "$(git hash-object "$EV_M/rd733-fixed-first-run-setup.js.keep" 2>/dev/null)" = "$FRJS_HEAD_BLOB" ] || { echo "REFUSING: the builder's browser-checked page script (.keep) is not ed4c1bf's blob 9d62976" >&2; exit 31; }

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PREV_B9" "$READY_A" "$READY_B"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 60 — the OPTIONAL members RD-707 / RD-732: validated only when stamped.
P7_LINE="RD-707 (NexusAI-O) is NOT a member of this gate: report \"RD-707: not a member\" and do not measure the brief's OPTIONAL TARGET — RD-707 section."
P32_LINE="RD-732 (NexusAI-M) is NOT a member of this gate: report \"RD-732: not a member\" and do not measure the brief's OPTIONAL TARGET — RD-732 section."
opt_check() { local head="$1" br="$2" ready="$3" name="$4"
  [[ "$head" =~ ^[0-9a-f]{40}$ ]] && [ -n "$br" ] && [ -s "$ready" ] || { echo "REFUSING: $name is half-stamped (a 40-hex head, a branch and an on-disk READY are all required)" >&2; exit 60; }
  [ "$(g cat-file -t "$head" 2>&1)" = "commit" ] || { echo "REFUSING: $name head $head is not in the object store" >&2; exit 60; }
  g ls-remote origin "refs/heads/$br" 2>/dev/null | grep -q "^${head}[[:space:]]" || { echo "REFUSING: origin refs/heads/$br is not $head" >&2; exit 60; }
  if g merge-base --is-ancestor "$head" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: $name ${head:0:7} is already on main" >&2; exit 60; fi
  grep -qF "${head:0:7}" "$ready" || { echo "REFUSING: the $name READY does not name ${head:0:7}" >&2; exit 60; }
  grep -qF "$ready" "$BRIEF" || { echo "REFUSING: brief §OPT does not name the $name READY $ready" >&2; exit 60; }; }
if [ -n "$P7_HEAD$P7_BRANCH$P7_READY" ]; then
  opt_check "$P7_HEAD" "$P7_BRANCH" "$P7_READY" "RD-707"
  g merge-base --is-ancestor "$X_SHA" "$P7_HEAD" 2>/dev/null || g merge-base --is-ancestor "$X_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: RD-707 ${P7_HEAD:0:7} is not stacked on RD-466 3f7e263 and RD-466 is not on main" >&2; exit 60; }
  g diff --name-only "$X_SHA" "$P7_HEAD" 2>/dev/null | grep -qxF '.dockerignore' || { echo "REFUSING: RD-707's delta over 3f7e263 does not change .dockerignore" >&2; exit 60; }
  P7_LINE="RD-707 (NexusAI-O) IS A MEMBER (TIER 1): branch $P7_BRANCH at $P7_HEAD, READY $P7_READY — measure the brief's OPTIONAL TARGET — RD-707 section v1-v5 and give it its own verdict."
fi
if [ -n "$P32_HEAD$P32_BRANCH$P32_READY" ]; then
  opt_check "$P32_HEAD" "$P32_BRANCH" "$P32_READY" "RD-732"
  MB32="$(g merge-base "$P32_HEAD" "$M_ORIGIN" 2>/dev/null)"
  [ "$(g diff --name-only "$MB32" "$P32_HEAD" 2>/dev/null | grep -v -x -F "$COUNTS_FILE" | tr '\n' ' ')" = "package-lock.json " ] || { echo "REFUSING: RD-732's delta over its merge-base with main is not package-lock.json only" >&2; exit 60; }
  g show "${P32_HEAD}:package-lock.json" 2>/dev/null | python3 -c 'import json,sys; p=json.load(sys.stdin)["packages"]["node_modules/ip-address"]; sys.exit(0 if p["version"]=="10.7.2" and p["integrity"].startswith("sha512-7H/2gFSIitxc0hG3nOI1glS8QLo") else 1)' || { echo "REFUSING: RD-732's lock does not pin ip-address 10.7.2 with the briefed integrity" >&2; exit 60; }
  P32_LINE="RD-732 (NexusAI-M) IS A MEMBER (TIER 2): branch $P32_BRANCH at $P32_HEAD, READY $P32_READY — measure the brief's OPTIONAL TARGET — RD-732 section y1-y5 and give it its own verdict."
fi

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-733 is TIER 2 (through-code) PLUS A REAL-BROWSER LEG' 'RD-703 is TIER 2 (through-code)' 'One verdict PER ticket' 'TIER 2 AT THROUGH-CODE WEIGHT'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-733 (TIER 2, through-code, PLUS A REAL-BROWSER LEG' 'RD-703 (TIER 2, through-code' 'one verdict per ticket'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$A_BASE" "$B_BASE" "$MAIN_SHA" "$X_SHA"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in $QUEUED; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
done
for S in "$FRJS_BASE_BLOB" "$FRJS_HEAD_BLOB" "$FRHTML_BLOB" "$DEBT_BASE_BLOB" "$DEBT_HEAD_BLOB" "$R465_BASE_BLOB" "$R465_HEAD_BLOB" "$A_TEST_BLOB" "$RD200_BLOB" \
         "$HELPER_BASE_BLOB" "$HELPER_HEAD_BLOB" "$R699_BASE_BLOB" "$R699_HEAD_BLOB" "$PARKED_BLOB" "$DOM_OLD_BLOB" "$DOM_MAIN_BLOB" "$ICE_MAIN_BLOB" "$ICE_X_BLOB" "$LOCK_BLOB"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the verdict subject exactly" >&2; exit 15 ;; esac
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 19 — the words the prompt must carry (% is a space); and the brief's sections.
WORDS="RD-733 RD-703 RD-466 RD-707 RD-732 C-18 C-40 C-49 C-57 C-68 C-89 C-98 C-102 C-104 C-112 C-125 C-130 C-141 ADDENDUM C-174 C-185 C-187 C-190
RED-AT-PARENT RED-AT-BASE RED%AT%MAIN u1 u3 u4 w0 w1 w2 w3 w4 w5 w6 w7 p1 p4 f1 f3 f6 k1 k2 k4 c1 c3 r1 r2 r3 r4 r5 r6 r7 r8 x1 x2 MT1 MT2
L-A1 L-A4 L-A5 L-B1 L-B4 H-1 H-15 H-19 H-20 H-21 --forceExit trap%on%EXIT deadline LANDING%CONTROL 127.0.0.1 route%handler NEVER%download%a%browser
4225/255 4199/254 4202/252 4210/254 SCRATCH%object%dir reverse%order git%clone%--shared REGENERATION id-superset pull%request DIFFERENTIAL
POSITIVE%CONTROL%FIRST NEGATIVE-ASSERTION%SWEEP node%--check VOID EXCLUSIVE qa-b10- QUEUE,%NEVER%TAKE%OVER --after DEADLINE HEARTBEAT
2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CI%NOT%RUN CodeQL
Prior%work FOREGROUND never%push NEVER%merge Partner%Center batch%9 M0 Screenshots"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in "^## TUESDAY'S RULINGS" '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## OPTIONAL TARGET — RD-707' '^## OPTIONAL TARGET — RD-732' \
         '^## 8. THE MERGED TREE' '^## 10. Floor discipline' '^## WRONG OR UNVERIFIED' '^## PROVENANCE' '^### MERGE ORDER' '^### TARGET A' '^### TARGET B' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-B1 L-B2 L-B3 L-B4; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
# every builder's NOT TESTED list is carried verbatim (each line checked in the READY AND the brief)
for PAIR in "$READY_A|- The demo (RD-76)." \
            "$READY_A|- A real Entra round trip on the tab: open mode, no tenant configured. The saved-config path (revalidateEntraConfig on load) is driven only in jsdom, by CTRL-VAL." \
            "$READY_A|- Browsers other than Chromium." \
            "$READY_A|- Whether any operator relied on the tab marking steps complete by itself: it never did, because the function threw before reaching that code." \
            "$READY_B|- Case 6 (endianness switching inside one run with no separator) is a stated limit, pinned, not solved." \
            "$READY_B|- Non-Latin scripts at the boundary: ALNUM is \p{L}\p{N}, so a CJK or Cyrillic boundary char counts as a letter; only Latin and digit boundaries were driven." \
            "$READY_B|- UTF-32-in-a-string runs (up to three NULs per char) at an ambiguous boundary: not driven." \
            "$READY_B|- CI Build and CodeQL at this head: not run (no PR). The diff adds no fs calls; the new regex is a single-class \p test, and WIDE_RUN is unchanged."; do
  F="${PAIR%%|*}"; T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the NOT TESTED line '$T' verbatim" >&2; exit 19; }
done
# the rulings the brief rests on are quoted from source and still say so
for PAIR in "Dead UI is removed, not hidden." \
            "Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code" \
            "O-1 counts as known ONLY while its failure is" \
            "A cell asserts the PROPERTY THAT MUST HOLD AFTER THE FIX, never the defect" \
            "A cell that fails for a known, ticketed reason is PARKED outside the suite" \
            "a clean merge-tree and a changed measured surface are not in tension"; do
  grep -qF -- "$PAIR" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$PAIR' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$PAIR" "$BRIEF" || { echo "REFUSING: brief does not quote '$PAIR'" >&2; exit 19; }
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b10-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may move' '--after' 'never push' 'C-174' '--forceExit' 'trap … EXIT'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 76 — the brief carries the ONE safe SESSION_SECRET printer verbatim and names the forbidden idioms (H-1).
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done

# 77 — the heartbeat is a separate child, aborted if absent at 90 s, max gap reported (H-4).
for w in 'separate child' 'within 90 s' 'max gap'; do
  grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat rule fragment '$w' (H-4)" >&2; exit 77; }
done

# 78 — byte-level plants via Buffer, verified with xxd (H-9).
for w in 'H-9' 'Buffer' 'xxd -l 16' 'JSON.stringify'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant rule fragment '$w' (H-9)" >&2; exit 78; }
done

# 79 — quoted mutant tool with a negative control; insertion-aware landing rule (H-7, H-8).
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing rule fragment '$w' (H-7/H-8)" >&2; exit 79; }
done

# 81 — this batch's own premises are in the brief.
for w in 'RED-AT-PARENT' 'RED-AT-BASE' 'RED AT MAIN' 'C-187 does NOT apply' 'missing 0' 'C-190' 'NEVER opens, comments on, approves or merges a PR' \
         '4225/255' 'ADD ONLY IF Tuesday stamps it with a head sha' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'NEVER merges and never pushes' \
         'DIFFERENTIAL' 'byte-identical' 'C-98' 'route handler' "channel: 'chrome'" 'NEVER download a browser' 'DETERMINISTIC RED for the race' \
         'PLANT (debt added back)' 'no other caller' 'No exception is declared in this batch'; do
  grep -qF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 38 — negative-control seats: stamped by Tuesday (a placeholder here refuses via 32), named in the brief, live now.
UNSTAMPED_SEATS=0
case "$NEG_SEATS" in *"$PH_STAMP"*) UNSTAMPED_SEATS=1; echo "NOTE: NEG_SEATS in this launcher is still a stamp placeholder — Tuesday stamps the live seat pids" >&2 ;; esac
if [ "$UNSTAMPED_SEATS" = "0" ]; then
  for P in $NEG_SEATS; do
    grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
    [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 10 before launch" >&2
  done
fi
if command -v tmux >/dev/null 2>&1; then
  for N in M N P O; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check AND the seats. LAST refusal, so --check shows every other guard first.
if [ "$UNSTAMPED_SEATS" = "1" ] || grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 18b 22 93 94 95 96 97 92 23 35 70 80 31 39 10 17 60 11 12 13 14 15 20 19 24 53 71 76 77 78 79 81 38); stamp NOT complete." >&2
  echo "  merge-tree scratch objects (guard 80): $MT_OBJ" >&2
  echo "REFUSING: a stamp placeholder remains (the brief's SELF-CHECK line / Self-check note / §10 seats, or this launcher's NEG_SEATS) — the coordinator re-reads end-to-end and stamps them before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7} at $PIN_TS (18); $X_BRANCH ${X_NOW:0:7} (pinned 3f7e263)"
  echo "  main ${M_ORIGIN:0:7} (f9cb440 or a descendant; no member path moved) (18b); image-manifest population there ${HP_NOW:-?} (92); queued/partner on main:${Q_IN:- none}"
  echo "  merge-bases (7); chains (8); deltas (22); RD-733 premises (93); RD-703 premises (94); census (95); C-187 n/a + dom.js (96); browser ${PW_EXE:-channel chrome} (97)"
  echo "  overlaps (23); counts (35); package-lock ${LOCK_BLOB:0:7} (70); merge-tree counts-only (80, $MT_OBJ); evidence (31); RD-707 (60): ${P7_HEAD:-not a member}; RD-732 (60): ${P32_HEAD:-not a member}"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS (38)"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

$P7_LINE
$P32_LINE

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$X_BRANCH = ${X_NOW:-absent} (the cross cell stays on 3f7e263); refs/heads/main = $M_ORIGIN (f9cb440 or a descendant; no member path moved since f9cb440; image-manifest require-population there ${HP_NOW:-unread}; queued/partner commits on it:${Q_IN:- none}). Browser: ${PW_EXE:-the Playwright bundled Chromium is absent, use channel chrome at $CHROME_APP}. Merge-tree (scratch objects, clean or counts-only) held for main x each member, the member pair, and each member x 3f7e263. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
