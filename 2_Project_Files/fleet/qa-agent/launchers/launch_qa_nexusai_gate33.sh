#!/bin/bash
# launch_qa_nexusai_gate33.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 33): a TIER-2 GATE THROUGH CODE, ROUND 1 (not a re-gate), B355 (SEAT-R11)
# RD-874 + RD-875, PR #101, branch rd-874-875-test-guards-uat-port-r11 @ 6e947f4 (TWO commits over main d463f88; 6 paths, +147/-15) — one gated head, one verdict,
# ONE report. RD-874 = three settings-plant guards (gate 32's G32-1); RD-875 = tests/uat-run.js has no default target and honours the port (N30-2 / N32).
# (derived 2026-10-21 by Tuesday's launcher-drafting sub-agent from launch_qa_nexusai_gate32.sh; the drafter ran ONLY `bash -n` and an unstamped `--check` — see
#  2026-10-21_gate33_LAUNCHER-REPORT.md beside this file. Tuesday stamps the kit, adds the routing line, re-runs `--check`, then chmod +x.)
# A FRESH gate on the Mac mini, /Volumes/Laptop-DEV; the T9 is UNMOUNTED, so the lock base is the Laptop-DEV locks-laptop-1017.
#   PR101 rd-874-875-test-guards-uat-port-r11 @ 6e947f4 (2 commits over d463f88: a7e8f4f RD-874, 6e947f4 RD-875)
#   M0 = the MAIN pin Tuesday STAMPS (d463f88 at drafting = mode '0': main = the PR's base, the gated tree IS the landing tree). If main has moved at the stamp the
#   launcher derives what landed and REFUSES when it touches any of the 6 PR paths (T0).
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-gate33' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate33.sh'"
#   (i.e. /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-33 commission (B359, 2026-10-21), the kit's TIER 2 argument (routing v1.0 row G2: tests-only / tooling follow-up whose mechanism a prior
# gate already measured) and its ESCALATION RULE (any weakened auth/SCIM test guarantee stops the grading and hands the PR to TIER 1 / Opus).
# THE MODEL RULE: Kam, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b), PER SESSION.
# The MODEL is the kit's MODEL line (tier 2, routing v1.0 row G2, Sonnet), which must equal models_latest.json levels.sonnet.model_id (the template ALSO ran on
# Sonnet: it already read levels.sonnet.model_id — no Opus-to-Sonnet re-point was needed).
# FINDINGS-ONLY: never merges (outside its own store), never pushes, never opens/comments/approves/un-drafts/updates a PR, never dismisses an alert, never swaps or
# edits the lock tool; no fix, no deploy, no az, no docker, no model call, no demo, no human; tests/uat-run.js is NEVER executed (T2).
#
# PATTERN: launch_qa_nexusai_gate32.sh (prompt EMBEDDED, --check mode, PIN-table parser, C-192 lsr retry, lock-tool pin 90, the LIVE negative-control seat
# derivation 38R, guard 86, stamp + route refusals LAST) over gate 33's content. CHANGES, each deliberate (full list in the LAUNCHER-REPORT):
#   - STAMP: the kit's slots are '@MAIN_SHA@' (x2: MAIN-STAMP line + PIN-HEADS MAIN row) and '@STAMP_TIME@' (x1), NOT gate 32's '@SLOT': the placeholder detector is
#     a generic '@[A-Z][A-Z_0-9]*@' (gate 32's literal-'@SLOT' counter would have counted ZERO slots here and let an unstamped kit launch).
#   - 40: PIN-HEADS has TWO rows, MAIN + PR101 (branch, head 6e947f4, base d463f88, 2 commits). (gate 32: MAIN + PR98 + GATED.)
#   - 18: refuses when the branch OR refs/pull/101/head is not 6e947f4.
#   - 7/8: the chain base d463f88 <- a7e8f4f <- 6e947f4 (2 rows), linear, merge-base = base, first-parent count 2. 22D (the gate-32 delta) is DROPPED.
#   - 22: the SIX paths (5 M + 1 A) pinned by sha256, numstat table, every blob pinned (head, and main for the 5 M); 5 of 6 are test code/tooling and the 6th is the
#     counts file; guarded set (backend/ static/ templates/ .github/ bicep/ Dockerfile package*.json HISTORY.md CLARIFICATIONS.md) = 0.
#   - 93: lockfile, package.json, deploy-demo.yml same blobs at M0 and head and equal their pins; the HEAD counts file is blob 9a723cd = 4941/304; BASE's is a28458a =
#     4934/303; M0's is READ (in mode 0 it must equal BASE's); deploy-demo gates BOTH jobs at M0; tests/uat-run.js source premises (see 93U).
#   - 31: the builder's B355 STATUS must end with the READY line for 6e947f4 (sha NOTEd, a CLAIM); the PR-TEXT sha NOTEd; gate 32's report must read COMPLETE and carry G32-1;
#     gate 32's instruments the kit copies BY NAME are PINNED by sha256 (gate 30's seven + mutant texts and gate 27's instruments are no longer required).
#   - 12/19/53/71: the kit-declaration lists are REWRITTEN for this kit's own words (rows r0-r8 + r1c, T0-T5, limits L-R1..L-R7 + L-Y1, tags qa-g33-, G33-<n>/N33-<n>,
#     verdict lines 'B359/PR101: …' and 'LANDING CHECKLIST: PR #101 …').
#   - DROPPED (gate-32-specific): 22D, the rd407 / html-dom / RD-786-open-site pins, the G30 report/instrument/mutant pins, the 'qa-g32' guards, gate 29/30 brief
#     requirements, section 3b / 7 / PRIOR ROUND headings (this kit has none), the kit's 'never --first-parent' phrase (the code itself never uses --first-parent for ancestry).
#   - The PROMPT is rewritten for gate 33 from the KIT (round 1, S8a red-proof, uat-run mutants + no-socket spy, counts, PR text, the TIER-1 escalation).
#
# Identity: exports NexusAI's OWN az/gh dirs (az is NOT used; gh READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs with --no-optional-locks (cat-file, log, merge-base, diff, diff-tree, rev-parse, ls-remote, rev-list, show) and
# the legacy stdout-only merge-tree (no object written, only when main moved); shasum / bash -n / grep over files; python over `git show` output; ls, ps,
# tmux list-panes, test -e. Writes nothing. It starts no claude (the exec is AFTER the --check exit).
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate33.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..99 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

# the kit's three at-sign placeholders are '@MAIN_SHA@' x2 and '@STAMP_TIME@' x1; this regex is generic on purpose (any '@NAME@' left = unstamped)
PH_RE='@[A-Z][A-Z_0-9]*@'

QA_DIR='/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN'
TUE='/Volumes/Laptop-DEV/TUESDAY'
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
STAGED="$TUE/2_Project_Files/fleet/briefs_staged"
TBRIEFS="$TUE/2_Project_Files/tuesday/briefs"
BRIEF="$TBRIEFS/2026-10-21_B359_SEAT-G24_nexusai-gate-pr101-tier2.md"
BRIEF32="$TBRIEFS/2026-10-20_B336_SEAT-G23_nexusai-gate32-pr98-round2.md"
BRIEF_B355="$TBRIEFS/2026-10-21_B355_SEAT-R11_nexusai-rd874-rd875.md"
TEMPLATE="$TUE/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md"
ADD25="$TBRIEFS/2026-10-18_gate25_ADDENDUM-1_ref-order.md"
ANS1="$TBRIEFS/2026-10-18_S101O_ANSWER-1_plan-confirmation.md"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
ST="$NX/session-tools"
BRIEFS_NX="$NX/1_Project_Definition/Briefs"
STATUS_B355="$BRIEFS_NX/2026-10-21_B355_STATUS.md"
PR101TEXT="$BRIEFS_NX/2026-10-21_B355_PR-TEXT.md"
B355_EVID="$BRIEFS_NX/2026-10-21_B355_evidence"      # a CLAIM: presence only, the launcher never opens it
LOCKTOOL="$ST/nexusai-lock.sh"
LOCK_SHA_INST='3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792'   # RD-821 round 3, INSTALLED — PINNED
T9_VOL='/Volumes/KK_T9_External_HDD'
LOCK_BASE_LAPTOP="$ST/locks-laptop-1017"
LOCKQ_J="$LOCK_BASE_LAPTOP/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
RPTS="$QA_DIR/projects/nexusai/reports"
B25_INST="$RPTS/2026-10-18-gate25-rd761-rd794-merged/evidence/inst"
G32_DIR="$RPTS/2026-10-20-gate32-b336-pr98-r2"
G32_REPORT="$G32_DIR/report.md"
G32_INST="$G32_DIR/evidence/inst"
# gate 32's instruments the kit's T4 copies BY NAME (gate 32 is COMPLETE: these files never move) — "<file> <sha256>"
G32_TOOLS='qa-applymut.py 491477a749953a21ce67ceabb8b3c4bcb663fcc3efb5b06624fdcedbc0acdfd8
qa-mutlib30.sh 2eb5420b7f6cc5772a382f146a5446dddfa0dd83afbd05ce4895bc3f78ba1bfd
qa-jestwrap.sh 2383e1bead32e06d566dcdc17c3fdbb0060bc4c14ddf8669d540af5a14fc7324
qa-assertcount-preload.js 6282f6737ec41aa0e815f33122ae7aba0a93236b039c1899b0da3a5983cf9ba4
qa-names23.py c552d4d401dc5a9e7a5201963758e56d8e2cbff513b8bafd38450e7d92d6d16f
qa-file32.sh abdd5adb30dde509aa395d6df7dc4f49ff59304f211ac0e8a7b1c610700fac21
qa-holdlib32.sh 27f2cdf2cbae4fd0ebee3ef246322c36584494f7dffafa28feb3e7ee0b0f4de6
qa-floorlib32.sh cb82c7b314ec6d1739e47c01144183c22027a7f85de4de4be0097628b0c8761d
qa-loadwait32.sh 76a19e6d600e68f04b285ccb030c880be3ec57adb61616d591c2b83a274a0976
qa-plantcells-32.js 9acb74d92167cc086c52d948b2fe44e5617686a235e005e8ed529b6154dba9fb'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-gate33'
EXPECT_REPORT="$RPTS/2026-10-21-gate33-b359-pr101/report.md"
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'

# ---- the pins (cross-checked against the kit's PIN-HEADS, guard 40; each MEASURED 2026-10-21 by read verbs)
BASE='d463f8817fba925dee7e78c5216df3d5ea8ad073'; BASE_TREE='53d51c59698401237b1b1573fa942bf9f650b51d'   # the PR's base (main when the PR was cut). NB: the KIT has the two tree ids SWAPPED (it calls 53d51c5 the head's); git says base 53d51c5, head eb5fc01 (MEASURED rev-parse)
BR='rd-874-875-test-guards-uat-port-r11'
HEAD_SHA='6e947f4d15411d6b0ac15547addb30799bda0782'; HEAD_TREE='eb5fc01a4ce22237f28f325db0c5292e4d376f1a'   # the head under gate 33 (RD-875 commit)
PR_REF='refs/pull/101/head'
P97_REF='refs/pull/97/head'; P97_NOTED='115a775b6d5808629f493ef7a3f602d8c5853a22'   # NOTEd only: another mover (S101O); its head is NOT this gate's pin
P67_REF='refs/pull/67/head'; P67_NOTED='94b288cc64d6348ebd75b502a8712a543358e51b'
# the chain, oldest first: <full sha> <tree> (each commit's parent is the previous row; row 1's parent is BASE)
CHAIN='a7e8f4f9e280e13f8de4a5c211ab39a6746461ac 3358d239b4edc08a810fc1a3d7160b677160dd98
6e947f4d15411d6b0ac15547addb30799bda0782 eb5fc01a4ce22237f28f325db0c5292e4d376f1a'
C1_SHA='a7e8f4f9e280e13f8de4a5c211ab39a6746461ac'
PATHS_SHA='f4db97c617800403ec8a35133455733c22aaadb7a63d76f1b5d8a2a05797795c'   # sha256 of the sorted, space-joined 6-path list (git diff --name-only BASE HEAD)
# the six paths: <path> <head blob> <main(base) blob, or - for the added file>
PATH_BLOBS='__tests__/auth-gate-fail-closed.test.js 5db407a55b6120dda592c7cf20ce1f52170332f4 d91f441a2cef59e66e9cb200764a57632845df6a
__tests__/rd395-ai-enabled-unreadable-store.test.js 0c92455e713d6c05cfee30b83fd95b85294d22c4 f02e477089ec93f277f6ff9505321ba88abd10b8
__tests__/rd875-uat-run-target-and-port.test.js ca3ca56138e889c52bc232f3effae51972288291 -
__tests__/scim-security-controls.test.js b9aeef8b97c08eb4b3d39e237715baaa41d3b060 23df594703e8c242d6bbee3ab3321f3c7e6ec1a9
scripts/verify-expected-counts.json 9a723cdc3bec7d2863b6501cc52928ec93760efc a28458adef1e24416865a425201dc4bc840f9f30
tests/uat-run.js e5370d2d5ad86fcc78a18f9d2bd117f064d1020c 3841b60ac30f5ec58d6ce3b1b18c0fb3c23b9916'
NUMSTAT='2 0 __tests__/auth-gate-fail-closed.test.js
2 0 __tests__/rd395-ai-enabled-unreadable-store.test.js
103 0 __tests__/rd875-uat-run-target-and-port.test.js
2 0 __tests__/scim-security-controls.test.js
3 3 scripts/verify-expected-counts.json
35 12 tests/uat-run.js'
NEW_TEST='__tests__/rd875-uat-run-target-and-port.test.js'
UAT='tests/uat-run.js'
COUNTS_FILE='scripts/verify-expected-counts.json'; COUNTS_BLOB_HEAD='9a723cdc3bec7d2863b6501cc52928ec93760efc'; COUNTS_BLOB_BASE='a28458adef1e24416865a425201dc4bc840f9f30'
PKG='package.json'; PKG_BLOB='384805d9e286718bb34ffd05be01c62c00806cf5'
LOCK='package-lock.json'; LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'
DEPLOY_WF='.github/workflows/deploy-demo.yml'; DEPLOY_BLOB='953b2a2f84e8710bea857ec87c6f00faa50fa56b'
# the guarded set of the kit's r0 (backend/ static/ templates/ .github/ bicep/ Dockerfile package*.json HISTORY.md CLARIFICATIONS.md). Gate 32's expression also listed the
# counts file; THIS PR legitimately edits it (it is one of the six), so it is excluded here and pinned by blob / numstat / counts instead.
GUARDED_RE='^(backend/|static/|templates/|package\.json$|package-lock\.json$|\.github/|bicep/|Dockerfile$|HISTORY\.md$|CLARIFICATIONS\.md$)'
TESTCODE_RE='^(__tests__/|tests/|scripts/test-[^/]*\.js$)'
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 33'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-gate33] ANSWER'
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
counts_blob() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
counts_at() { counts_blob "$(g rev-parse --verify -q "${1}:${COUNTS_FILE}" 2>/dev/null)"; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cntF() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
fsha() { shasum -a 256 "$1" 2>/dev/null | cut -d' ' -f1; }
tree_of() { g rev-parse --verify -q "${1}^{tree}" 2>/dev/null; }
parents_of() { g log -1 --format='%P' "$1" 2>/dev/null; }
paths_of() { g diff --name-only "$1" "$2" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//'; }
# the LEGACY stdout-only merge-tree (trivial-merge mode; writes NO object; never --write-tree in the NexusAI repo): prints the paths whose section
# carries conflict markers, space-separated.
mt_conflicts() { g merge-tree "$1" "$2" "$3" 2>/dev/null | python3 -c '
import sys,re
heads=("changed in both","added in remote","added in local","removed in remote","removed in local","merged","added in both","removed in both")
cur=None; out={}
for ln in sys.stdin.read().split("\n"):
    if ln.strip() in heads and not ln.startswith((" ","+","-","@")):
        cur={"p":set(),"c":False}; out[id(cur)]=cur; continue
    if cur is None: continue
    m=re.match(r"^  (base|our|their|result|both)\s+\d+\s+[0-9a-f]+\s+(.*)$",ln)
    if m: cur["p"].add(m.group(2))
    if ln.startswith(("+<<<<<<<","+>>>>>>>")): cur["c"]=True
print(" ".join(sorted(p for s in out.values() if s["c"] for p in s["p"])))' 2>/dev/null; }
# C-192: ls-remote retried up to 5 x ~10 s on a publickey denial; sets LSR_OUT on success (no subshell, so LSR_ATTEMPTS counts), returns 1 (UNKNOWN) otherwise.
LSR_ATTEMPTS=0
LSR_OUT=''
lsr() { local out rc i
  LSR_OUT=''
  for i in 1 2 3 4 5; do
    LSR_ATTEMPTS=$((LSR_ATTEMPTS + 1))
    out="$(g ls-remote origin "$@" 2>&1)"; rc=$?
    if [ "$rc" = "0" ]; then LSR_OUT="$out"; return 0; fi
    printf '%s\n' "$out" | grep -qi 'publickey' || { printf '%s\n' "$out" >&2; return 1; }
    [ "$i" = "5" ] || sleep 10
  done
  printf '%s\n' "$out" >&2; return 1; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, gate 33: a TIER-2 GATE THROUGH CODE, ROUND 1 (a first gate on this head, not a re-gate), ONE verdict, ONE report. A NO GO from you gets ONE fix round on the same seat model; a second NO GO on the class stops. It is a FRESH gate on Kam's Mac mini, working volume /Volumes/Laptop-DEV; the T9 drive is UNMOUNTED, so the project's jest lock lives on this drive's locks-laptop-1017 base. The item: B355 (builder SEAT-R11), RD-874 + RD-875, PR #101 (datasecau/Reporting_Dashboard_Au), branch rd-874-875-test-guards-uat-port-r11 at 6e947f4d15411d6b0ac15547addb30799bda0782 (tree eb5fc01a4ce22237f28f325db0c5292e4d376f1a): TWO commits (a7e8f4f9e280e13f8de4a5c211ab39a6746461ac RD-874, then 6e947f4d RD-875) over main d463f8817fba925dee7e78c5216df3d5ea8ad073 (tree 53d51c59698401237b1b1573fa942bf9f650b51d), SIX files, +147/-15, the PR NON-draft (Tuesday opened it so CodeQL runs). RD-874 (gate 32's finding G32-1): three settings.json plants in three tests (auth-gate-fail-closed, rd395-ai-enabled-unreadable-store, scim-security-controls) now assert they sit where the product reads; each guard is ONE expect plus ONE comment line, before its plant. RD-875 (gate 30's N30-2 / gate 32's N32): tests/uat-run.js has no default target and connects on the port UAT_BASE names, with a regression test file. M0 is the main Tuesday STAMPED (the launcher verified origin main equals it; sha, tree and the mode are at the end of this prompt): mode 0 means main equals the PR's base and the gated tree IS the landing tree. Tree ids: the launcher MEASURED the head's tree as eb5fc01a... and main's as 53d51c59... (git rev-parse); if the brief's text calls them the other way round, that is the drafter's slip: re-derive both yourself and report it as a note. Never trust the builder's logs, probes, scan or counts as the proof; every line of the builder's STATUS is a CLAIM, RELAYED, never evidence. FINDINGS-ONLY: you NEVER merge anything the fleet can see (a merge commit in YOUR OWN store is never pushed), NEVER push, NEVER open, comment on, approve, un-draft or merge a pull request, never comment on Jira, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool; no fixes, no deploys, no az, no docker, no model call of any kind, no production, no HTTP to any production or demo host, nothing to Partner Center, the demo or any human, no host npm registry. One client only: Datasec/NexusAI.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B359_SEAT-G24_nexusai-gate-pr101-tier2.md
It opens with the item, the six files, the builder's STATUS (read WHOLE; a CLAIM), the MODEL line and the stamp line, PIN-HEADS, the TIER 2 argument and its ESCALATION RULE, the LEGITIMATE SHAPES, the drafter's WRONG OR UNVERIFIED list (each item MEASURED, READ-ONLY-INFERRED or RELAYED), then TUESDAY'S RULINGS (T0 the re-pin mode, T1 the jest scope, T2 uat-run.js never executed, T3 the network, T4 where the gate lives, T5 the pane), the carried rulings and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, BRIEF_TEMPLATE section 2a, 5 and 6a, and gate 32's kit section 3a (the H-rules, carried by reference, except what is about docker, server boots of your own, browsers, SQL spies or the C-57 runner). The brief's section 2b rows (r0 to r8 and r1c), section 3 (the questions answered first) and section 9 (the floor) are required measurement. The verdict is PROVISIONAL if r1 (THE S8a RED-PROOF), r2 (the uat-run mutants and the no-socket spy) or r3 (the full verify) did not run.

THE ESCALATION RULE (binding, from the brief's TIER section): if the gate finds ANY change in this PR that weakens an auth or SCIM test's guarantee (an assertion removed, loosened, moved after its plant or made tautological, a cell the S8a mutant leaves GREEN at the head, or an assertion count in those files that fell), you STOP grading, record the finding, and hand the PR to TIER 1 / Opus: the verdict line then reads ESCALATED TO TIER 1, not GO or NO GO. That escalation hands the PR to a new tier-1 gate; it is not a model switch of this seat.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by the running model's safeguards, PER SESSION. You start on the model named at the end of this prompt (Sonnet 5.5). This is a Sonnet seat and none of the rows composes exploit payloads (the mutants are one-line renames, a port number, a boolean and a deleted guard). If one of your responses is stopped by the safeguards anyway: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt (the AEDT time, the row, what you were composing, the model, NOT RUN); let any running step finish and let the hold exit so you never sit holding a lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model to Opus 4.8 and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE PROPERTIES (brief section 2b and the commission). (1) DELTA AND SCOPE (r0): two commits, exactly the six paths (5 modified, 1 added), test code, tooling and the counts file only, with a planted-path control. (2) RD-874 GUARDS ARE REAL, BY THE S8a RED-PROOF (r1, in H2): in scratch clones at main and at the head, the rename mutant S8a (ONLY backend/jsonStorage.js line 1085, settings.json to settings_x.json) leaves the three named cells GREEN at main and turns exactly them RED at the head by the new expect (86/10 versus 83/13 of 96), a no-op mutant stays 96/96, and a copy of each test with the new expect deleted turns the cell GREEN again; each mutant LANDED and restored by a trap to the pinned blob; the sibling census of the plant cells in the three files (r1c). (3) RD-875 FIX HOLDS AND NO SOCKET OPENS (r2, in H4): M-port, M-default and M-cert each turn exactly their own cell RED in the new test, your own spy on the network and process primitives (positive control first, never forwarding) counts 0 calls, and tests/uat-run.js is NEVER executed, in any form (T2). (4) COUNTS AND NAMES (r3): the committed 4941/304, a regenerated count and ONE plain npm run verify at the head tree agree, the names multiset LOST 0 ADDED 0 over the three edited files, per-test assertion counts exactly three +1. (5) CODEQL (r4, gh READ): every analysis for 6e947f4d listed and COMPLETED, the open alerts on refs/pull/101/head BY NUMBER, alert 151 (RD-810, js/file-access-to-http) read BY NUMBER on main (at tests/uat-run.js line 30) and on the PR ref (line 43) and reported as a finding with its labels, never dismissed; PR #96's fixed list as the firing control; the check runs including build. (6) FORWARD-MERGE (r5): the overlap of the six paths with PR #97 and PR #67 (expected: the counts file only), the legacy merge-tree readings if their head objects are in your store, the TURN consequence stated as numbers; the merged-tree hold H3 only if main moved at the stamp. (7) THE PR TEXT (r6): every number and named item in Tuesday's title and body checked against the compare, the diff and your own measurements. (8) HYGIENE (r7): gitleaks over the range with a planted control, deploy-demo skipped, lockfile equal to M0's. (9) PRIOR WORK and the builder's STATUS claims VERIFIED, FALSE or UNVERIFIED (r8, C-49). The sibling sweep asks whether the guards closed the CLASS or only the three named cells. Findings only, never fixes.

MAIN MUST NOT MOVE: the launcher verified origin main equals the stamped MAIN pin exactly, that d463f881 is in its ancestry, that the head and its chain are not on it, and that what landed since d463f881 (nothing, in mode 0) touches none of the six PR paths; take M0 by git ls-remote at YOUR start and say so. If main moves mid-gate (PR #97 from S101O and PR #67 are the likeliest movers, and both also edit the counts file), name what landed (git log with explicit revs), finish nothing that would read as a verdict on the new main, and mail a QUESTION (C-68). GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the lock tool at start, mid and end.

C-190 + its ADDENDUM: BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. Alerts are fixed in code, never dismissed. The land is the SAME commit: never squash, never rebase. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed. C-68: a gate verdict is valid only at the head it ran on; after the forward merge that a land may require (if main moves, main goes FORWARD into the branch: a NEW head) the affected cells are re-run on the NEW head, each named individually: the three guarded cells and the seven rd875 cells. CodeQL is NOT RUN by this gate on any tree: say so.

THE LOCK (C-63). The installed tool is session-tools/nexusai-lock.sh in the NexusAI project on this drive, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792. While the T9 is unmounted the base is NEXUSAI_LOCK_BASE=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017, which the launcher has EXPORTED into your environment: keep it on every jest step and never touch this drive's stale session-tools/locks (a 2026-09-22 holder lives there). THE JEST LOCK IS NOT YOURS and it is SHARED with gate 29 (QA/NexusAI-gate29, LIVE on it when the kit was drafted), S101O, any landing hold and the builders: you QUEUE behind them FIFO through the INSTALLED tool (never copied, never edited), never touch a holder, its owner file, its process or its worktree, and never use --replace on a ticket that is not your own. If the T9 mounts mid-gate, finish the running hold, file nothing more, and mail a QUESTION. EVERY jest run goes in the jest lock, each hold tagged qa-g33- (no tag of yours contains the word "merge": C-141 ADDENDUM 7; name the merged-tree hold qa-g33-H3), ONE hold at a time. MERGES GO FIRST: if a ticket is queued ahead of you, wait behind it (FIFO). AT A WAIT DEADLINE: --replace on your own still-waiting ticket BEFORE its deadline fires (a SAME-PLACE handover), confirmed from the queue listing; a duplicate-tag refusal takes a -r<N> suffix. Read queue-jest at start, around every hold and at end; any qa-g33- entry that is not your current hold is a STOP. THE LOAD RULE: file a hold, start any jest run only below a 1-minute load of 8 (8 cores; Tuesday's ANSWER-1 to S101O); record uptime beside each; over 8, poll every 20 s and log each wait (the floor read 10 to 17 at drafting, so expect to wait).

NODE_MODULES WITHOUT THE HOST REGISTRY (ruling m, H-31): offline npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache on the same volume; the head and main share lock 19477a9 (the PR touches no package file), so ONE proven install is APFS-cloned into the other trees (never copy node_modules from any checkout or worktree); EVERY npm invocation carries npm_config_update_notifier=false; an ENOTCACHED is NOT RUN, named, with a QUESTION: never go online from the host, never npm install. sqlite3's binding from the cached prebuild (an APFS clone of ~/.npm/_prebuilds), with its conditions, is PART OF H-31.

FLOOR DISCIPLINE (brief section 9): do ALL lock-free work first (r0, r1c, r4, r5 a to c, r6, r7, r8, the offline npm ci and the self-tests); then file your holds one at a time through your COPY of gate 32's qa-file32.sh re-pointed to qa-g33 tags and the jest kind only (its diff against its source quoted): H2 (the S8a matrix, r1), H4 (the uat-run matrix and the spy, r2), H1b (ONE plain npm run verify with --maxWorkers=2 at the clean head tree, expect VERDICT: PASS — 4941/4941 tests passed across 304 suites) and H1a (npm run verify with --update-counts in a SEPARATE scratch clone of the head, expect 4941/304 and the counts file changed in its _updated line only), each at most about 40 minutes planned except the verifies, each part file bash -n checked first. H1b is the one that must run; H1a may be ruled NOT RUN by Tuesday if the lock is starved; lock-starved about 2 h after filing, a hold is NAMED NOT RUN under ruling (o) EXTENDED, never "skipped". QUEUE, NEVER TAKE OVER. DEADLINE AND HEARTBEAT: every step has a per-step DEADLINE (H-20), every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported. Count foreign processes the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window.

THE INSTRUMENT RULES H-1 TO H-36 (brief section 3a; gate 32's kit section 3a read WHOLE). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes (SESSION_SECRET UNSET on every host run), and UAT_BASE is printed UNSET the same way. H-3: a LANDING CONTROL for every plant, revert and mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper. H-6: every path with a space quoted; jest runs under your copy of the network belt. H-7/H-8/H-21: every mutant by a quoted tool with a negative control, an edit whose anchor is absent FAILS LOUDLY, every file you mutate restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation and hash-compared to its pin. H-11/H-18: /bin/bash explicitly, quote "${sha}:${path}" and never type cd. H-14: every driver ends END ok or END VOID with a reason. H-17: assert each arm STARTED (jest's first suite); censuses by pgrep. H-20: deadlines on every jest run (with --forceExit). H-24: jest array options after the paths. H-27: THE MODEL RULE. H-28: ONE focused hold at a time, you stay in the FOREGROUND, a hold that must outlive one tool call runs as a TRACKED child of your session (never nohup). H-29: other gates' and the builder's evidence is method only (gate 32's instruments are copied BY NAME and hashed, re-pointed, never written; the builder's session-tools files are hashed at start and end, never run in place). H-31: offline host node_modules. H-33: never rm, quarantine; every child reaped by pid. H-34: the Laptop-DEV lock base. H-35: NO docker object and NO az command, and NO call to any real model. A revert, plant or mutant counts only if it LANDED (the exact text present, the original absent) and parses; a planted control that does not fire makes its row VOID (never a pass).

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh dirs under projects/nexusai/qa-trees/gate33.* in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN): ONE --mirror clone of the NexusAI repo on THIS drive as your store with gc.auto 0, your refs g33/* in it made BEFORE origin is removed (gate 25 ADDENDUM-1: g33/m0, g33/head, g33/c1, and g33/p97 and g33/p67 if those head objects are present), every work tree a clone of that store, status-checked before use, EXCLUSIVE to one purpose (MAIN, HEAD (also the clean full-verify tree), MUT (plus a second MUT clone at main), CNT). NEVER work in the NexusAI root checkout or any worktrees folder (LIVE: the builders' and S101O's). In the NexusAI repo use ONLY read verbs (show, diff, log with an explicit rev, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list, count-objects, for-each-ref, and the legacy stdout merge-tree); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, merge-tree --write-tree or hash-object -w there. Copy instruments BY NAME from gate 32's COMPLETE evidence/inst (qa-applymut.py, qa-mutlib30.sh, qa-jestwrap.sh, qa-assertcount-preload.js, qa-names23.py, qa-file32.sh, the holdlib, floorlib and loadwait set, and qa-plantcells-32.js) and gate 25's qa-lockcheck.py; re-point every copy to gate 33 including the lock base line (quote each diff); never write into another gate's dirs. Count the NexusAI .git/objects files and their newest mtime at start and end and account for any delta (S101O may be live). No Microsoft, Log Analytics or login host, no mail host except api.agentmail.to, no demo, no Partner Center, no workflow dispatch, no repo variable written. tests/uat-run.js is NEVER executed (its default target used to be the demo; only a node --check parse is permitted outside jest) and the tests/e2e files are NEVER run. No mail to any human. Never rm: quarantine.

RE-PIN at start, mid and end: main, rd-874-875-test-guards-uat-port-r11 and refs/pull/101/head (and refs/pull/97/head and refs/pull/67/head, the other movers) by git ls-remote, plus the lock tool's sha256: three timestamped readings with the branch name and attempt count beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so.

QUESTIONS: your routing name is QA/NexusAI-gate33. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-gate33] ANSWER". Approval-class items (anything Azure, any real model call, the demo, Partner Center, money, a human, the live lock tool beyond queueing) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to the path the launcher names at the end of this prompt (the brief's section 11). Write its VERDICT and FINDINGS table early and keep it current; line 3 is STATUS: IN PROGRESS or COMPLETE with the date. Findings are G33-<n>, notes N33-<n>, each naming its instrument and evidence class.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 33
Lead the body with the TWO lines in the form the brief's section 11 gives — the B359/PR101 verdict line and the LANDING CHECKLIST line — then one line naming M0 and END main, the sibling sweep, which rows ran on which model, which holds ran and which are NAMED NOT RUN, and "CodeQL NOT RUN by this gate on any tree". The report's last two lines are those same two lines, verbatim as mailed. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.
The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice: the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output: a NOT TESTED section carrying the builder's stated limits, every declared limit L-R1 to L-R7 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-190 with its ADDENDUM, C-209, C-185, C-192, C-205, C-141 with ADDENDUM 7, C-63, C-40, C-68, C-76, C-102, C-112, C-174 and C-57 are the clarifications this gate leans on; C-49, C-89, C-115, C-125, C-130 and C-131 are carried. That section must carry, verbatim, the NOT TESTED line the launcher appends at the end of this prompt (it is the brief's section 11 line).
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

STAMP_OK=1          # cleared below by any unstamped slot or a PENDING read-whole line; the refusal itself is LAST (32S)
PROVISIONAL=''      # what --check ran against provisionally while a slot was unstamped

# 9 / MODEL — the kit's MODEL line must equal models_latest.json levels.sonnet.model_id (tier 2, Sonnet); never typed from memory.
MODEL_LINE="$(grep -E '^MODEL \(tier 2;' "$BRIEF" | head -1)"
[ -n "$MODEL_LINE" ] || { echo "REFUSING: the brief has no 'MODEL (tier 2; …' line" >&2; exit 9; }
SONNET_ID="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"]["sonnet"]["model_id"])' "$MODELS_JSON" 2>/dev/null)"
[ -n "$SONNET_ID" ] || { echo "REFUSING: $MODELS_JSON levels.sonnet.model_id is unreadable" >&2; exit 9; }
MODEL="$(printf '%s' "$MODEL_LINE" | sed -E 's/.*: *`?([a-z0-9.-]+)`? *$/\1/')"
[ "$MODEL" = "$SONNET_ID" ] || { echo "REFUSING: the kit's MODEL '$MODEL' is not models_latest.json levels.sonnet.model_id '$SONNET_ID' — re-stamp the MODEL line from the file" >&2; exit 9; }

# 40 — parse PIN-HEADS (the ONLY source of heads) and cross-check against this launcher's pins; the MAIN row and the MAIN-STAMP line agree.
parse_block() { python3 - "$BRIEF" "$1" <<'PY'
import sys, re
s = open(sys.argv[1], encoding='utf-8').read(); name = sys.argv[2]
m = re.search(r'<!-- %s:BEGIN -->(.*?)<!-- %s:END -->' % (name, name), s, re.S)
if not m:
    print('NO-BLOCK'); sys.exit(0)
for line in m.group(1).splitlines():
    line = line.strip()
    if not line.startswith('|') or line.startswith('| id ') or set(line) <= set('|-: '):
        continue
    print('\t'.join(c.strip().strip('`') for c in line.strip('|').split('|')))
PY
}
PIN="$(parse_block PIN-HEADS)"
[ "$PIN" != "NO-BLOCK" ] && [ -n "$PIN" ] || { echo "REFUSING: the brief has no PIN-HEADS block — the heads have nowhere to come from" >&2; exit 40; }
prow() { printf '%s\n' "$1" | awk -F'\t' -v id="$2" '$1==id'; }
pfld() { prow "$1" "$2" | awk -F'\t' -v n="$3" '{print $n}'; }
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "2" ] || { echo "REFUSING: PIN-HEADS must carry exactly two rows (MAIN PR101)" >&2; exit 40; }
for ID in MAIN PR101; do
  R="$(prow "$PIN" "$ID")"
  [ "$(printf '%s\n' "$R" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: PIN-HEADS must carry exactly one row '$ID'" >&2; exit 40; }
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN-HEADS row $ID does not have 7 cells: $R" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 7)" = "IN" ] || { echo "REFUSING: PIN-HEADS row $ID status is not IN" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 2)" = "nexusai" ] || { echo "REFUSING: PIN-HEADS row $ID repo must be nexusai" >&2; exit 40; }
done
printf '%s' "$(prow "$PIN" PR101)" | grep -q '@' && { echo "REFUSING: PIN-HEADS row PR101 carries a placeholder" >&2; exit 40; }
[ "$(pfld "$PIN" PR101 3)" = "$BR" ] && [ "$(pfld "$PIN" PR101 4)" = "$HEAD_SHA" ] && [ "$(pfld "$PIN" PR101 5)" = "$BASE" ] && [ "$(pfld "$PIN" PR101 6)" = "2" ] \
  || { echo "REFUSING: PIN-HEADS PR101 is not $BR @ 6e947f4, base d463f88, 2 commits — re-pin kit AND launcher" >&2; exit 40; }
[ "$(pfld "$PIN" MAIN 3)" = "main" ] || { echo "REFUSING: PIN-HEADS MAIN row is not branch main" >&2; exit 40; }
PIN_MAIN="$(pfld "$PIN" MAIN 4)"
STAMP_LINE="$(grep -E '^MAIN-STAMP: ' "$BRIEF")"
[ "$(printf '%s\n' "$STAMP_LINE" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: the brief must carry exactly one 'MAIN-STAMP: ' line" >&2; exit 40; }
MAIN_STAMPED=1; S_SHA=''; S_LAUNCH=''
if printf '%s' "$STAMP_LINE$PIN_MAIN" | grep -qE "$PH_RE"; then
  MAIN_STAMPED=0; STAMP_OK=0
else
  STAMP_RE='s/^MAIN-STAMP: sha `?([0-9a-f]{40})`? \| launched (20[0-9]{2}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2} AEDT)$/'
  S_SHA="$(printf '%s' "$STAMP_LINE" | sed -nE "${STAMP_RE}\\1/p")"
  S_LAUNCH="$(printf '%s' "$STAMP_LINE" | sed -nE "${STAMP_RE}\\2/p")"
  is40 "$S_SHA" && [ -n "$S_LAUNCH" ] || { echo "REFUSING: the MAIN-STAMP line is not 'MAIN-STAMP: sha <40-hex> | launched <YYYY-MM-DD HH:MM AEDT>'" >&2; exit 40; }
  [ "$PIN_MAIN" = "$S_SHA" ] || { echo "REFUSING: PIN-HEADS MAIN ($PIN_MAIN) and the MAIN-STAMP sha ($S_SHA) disagree — stamp the same sha in both" >&2; exit 40; }
fi

# 18T — the T9 MOUNTED refuses: two lock bases would split the FIFO (ruling q); Tuesday decides the base first.
[ ! -d "$T9_VOL" ] || { echo "REFUSING: $T9_VOL is MOUNTED — the brief's lock base (locks-laptop-1017) assumes it is not; Tuesday decides the base, then re-brief" >&2; exit 18; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): main = the stamped MAIN pin EXACTLY; the branch AND the PR ref = the head pin. #97/#67 are read for the NOTE only.
lsr refs/heads/main "refs/heads/$BR" "$PR_REF" "$P97_REF" "$P67_REF" \
  || { echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="$1" '$2==r{print $1}'; }
M_ORIGIN="$(ref_now refs/heads/main)"
is40 "$M_ORIGIN" || { echo "REFUSING: origin main is unreadable in the ls-remote output — UNKNOWN (C-192)" >&2; exit 18; }
if [ "$MAIN_STAMPED" = "1" ]; then
  [ "$M_ORIGIN" = "$S_SHA" ] || { echo "REFUSING: origin main is '${M_ORIGIN:0:12}', not the stamped MAIN pin '${S_SHA:0:12}' — main MOVED since stamp; re-stamp the MAIN pin (never sed a sha blindly)" >&2; exit 18; }
  MAIN_SHA="$S_SHA"
else
  MAIN_SHA="$M_ORIGIN"; PROVISIONAL="$PROVISIONAL MAIN(unstamped: guards ran against origin main ${M_ORIGIN:0:12})"
fi
[ "$(ref_now "refs/heads/$BR")" = "$HEAD_SHA" ] || { echo "REFUSING: origin $BR is '$(ref_now "refs/heads/$BR")', not 6e947f4 — the head MOVED; re-pin kit AND launcher (a new head is a new kit amendment and a new CodeQL run)" >&2; exit 18; }
[ "$(ref_now "$PR_REF")" = "$HEAD_SHA" ] || { echo "REFUSING: $PR_REF is '$(ref_now "$PR_REF")', not 6e947f4 — PR #101 moved (or the ref is unreadable); re-pin kit AND launcher" >&2; exit 18; }
[ "$(ref_now "$P97_REF")" = "$P97_NOTED" ] || echo "NOTE: $P97_REF is '$(ref_now "$P97_REF")', not the drafter's ${P97_NOTED:0:8} — PR #97 (another mover, also edits the counts file) moved; the gate re-reads it (r5)" >&2
[ "$(ref_now "$P67_REF")" = "$P67_NOTED" ] || echo "NOTE: $P67_REF is '$(ref_now "$P67_REF")', not the drafter's ${P67_NOTED:0:8} — PR #67 (another mover, also edits the counts file) moved; the gate re-reads it (r5)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
CHAIN_SHAS="$(printf '%s\n' "$CHAIN" | awk '{print $1}')"
for S in "$MAIN_SHA" "$BASE" $CHAIN_SHAS; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: ${S:0:12} is not a commit in $REPO (got '$T') — this launcher never fetches; the seat's next fetch brings it, then re-check" >&2; exit 6; }
done

# 18M — M0 by ANCESTRY (never --first-parent); M0's tree DERIVED; NONE of the PR commits on M0; the mode; a moved M0 touching a PR path REFUSES.
[ "$(tree_of "$BASE")" = "$BASE_TREE" ] || { echo "REFUSING: d463f88 is not tree 53d51c5 (the measured main)" >&2; exit 18; }
g merge-base --is-ancestor "$BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: d463f88 is not in M0 ${MAIN_SHA:0:7}'s ANCESTRY — M0 is not a descendant of the PR's base d463f88" >&2; exit 18; }
M0_TREE="$(tree_of "$MAIN_SHA")"
for S in $CHAIN_SHAS; do
  if g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: PR #101 commit ${S:0:7} is ALREADY on M0 ${MAIN_SHA:0:7} — it landed before its gate; re-brief" >&2; exit 18; fi
done
LANDED_N="$(g rev-list --count "${BASE}..${MAIN_SHA}" 2>/dev/null)"
LANDED='none'
FFABLE='yes'
if [ "$MAIN_SHA" = "$BASE" ]; then
  MODE='0'
else
  MODE='moved'
  FFABLE='NO (the head is not a descendant of M0: the land needs main merged forward, a NEW head)'
  LANDED="$(g log --format='%h %s' "${BASE}..${MAIN_SHA}" 2>/dev/null | head -5 | cut -c1-90 | tr '\n' ';')"
  echo "NOTE: M0 ${MAIN_SHA:0:7} is $LANDED_N commit(s) past d463f88 — what landed: $LANDED — T0 applies (mode moved: the gated tree is the head; the merged tree is r5(d), hold qa-g33-H3)" >&2
  OVERLAP="$(comm -12 <(g diff --name-only "$BASE" "$MAIN_SHA" 2>/dev/null | sort) <(g diff --name-only "$BASE" "$HEAD_SHA" 2>/dev/null | sort) | tr '\n' ' ' | sed 's/ $//')"
  [ -z "$OVERLAP" ] || { echo "REFUSING: what landed since d463f88 touches PR #101 path(s) '$OVERLAP' — T0: STOP and mail a QUESTION; re-brief (a landed PR #97 / #67 touches the counts file: expected, and a re-stamp)" >&2; exit 18; }
  MB_M0="$(g merge-base "$MAIN_SHA" "$HEAD_SHA" 2>/dev/null)"
  GD0="$(g rev-parse --absolute-git-dir 2>/dev/null)"; OB0="$(find "$GD0/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
  MC0="$(mt_conflicts "$MB_M0" "$MAIN_SHA" "$HEAD_SHA")"
  OA0="$(find "$GD0/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
  [ -z "$MC0" ] || { echo "REFUSING: the legacy merge-tree of 6e947f4 onto M0 shows conflict markers in '$MC0' — T0: STOP; re-brief" >&2; exit 18; }
  [ "$OB0" = "$OA0" ] || echo "NOTE: NexusAI .git/objects went $OB0 -> $OA0 around the legacy merge-tree read — the trivial-merge mode writes none; a live seat may have" >&2
fi
M0_COUNTS="$(counts_at "$MAIN_SHA")"
case "$M0_COUNTS" in [0-9]*" "[0-9]*) ;; *) echo "REFUSING: M0 ${MAIN_SHA:0:7}'s counts file is unreadable ('$M0_COUNTS')" >&2; exit 93 ;; esac

# 7 / 8 — the head's chain: d463f88 <- a7e8f4f <- 6e947f4, oldest first, each parent = the previous row, EVERY tree; linear; the gated head is row 2.
PREV="$BASE"
while read -r CSHA CTREE; do
  [ -n "$CSHA" ] || continue
  [ "$(parents_of "$CSHA")" = "$PREV" ] || { echo "REFUSING: the parent of ${CSHA:0:7} is '$(parents_of "$CSHA")', not ${PREV:0:7} — the chain is not the briefed 2 linear commits" >&2; exit 7; }
  [ "$(tree_of "$CSHA")" = "$CTREE" ] || { echo "REFUSING: ${CSHA:0:7}'s tree is not ${CTREE:0:7}" >&2; exit 8; }
  PREV="$CSHA"
done <<EOF_CHAIN
$CHAIN
EOF_CHAIN
[ "$PREV" = "$HEAD_SHA" ] && [ "$(tree_of "$HEAD_SHA")" = "$HEAD_TREE" ] \
  || { echo "REFUSING: the chain does not end at 6e947f4 tree eb5fc01" >&2; exit 8; }
[ "$(g merge-base "$HEAD_SHA" "$BASE" 2>/dev/null)" = "$BASE" ] && [ "$(g rev-list --count "${BASE}..${HEAD_SHA}" 2>/dev/null)" = "2" ] \
  && [ "$(g rev-list --count --first-parent "${BASE}..${HEAD_SHA}" 2>/dev/null)" = "2" ] \
  || { echo "REFUSING: 6e947f4 is not 2 linear commits over d463f88 (merge-base, count, first-parent count)" >&2; exit 8; }

# 90 — the INSTALLED lock tool PINNED; it honours NEXUSAI_LOCK_BASE; the Laptop-DEV base is present with queue-jest; no qa-g33 ticket or holder.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… — find out who changed it; re-brief" >&2; exit 90; }
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-' "$LOCKTOOL" || { echo "REFUSING: the installed tool no longer honours NEXUSAI_LOCK_BASE — ruling q's premise" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" && grep -qF 'jest|docker) ;;' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL lacks --replace or the jest kind" >&2; exit 90; }
[ -d "$LOCK_BASE_LAPTOP" ] && [ -d "$LOCKQ_J" ] || { echo "REFUSING: the Laptop-DEV lock base $LOCK_BASE_LAPTOP (queue-jest) is not present (ruling q)" >&2; exit 90; }
BQ="$(grep -l '^tag=qa-g33' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${BQ:-0}" = "0" ] || { echo "REFUSING: $BQ qa-g33* ticket(s) already in $LOCKQ_J — a live or stale gate-33 ticket; read before launch" >&2; exit 90; }
HOLDER="$(sed -n 's/^tag=//p' "$LOCK_BASE_LAPTOP/nexusai-jest.lock/owner" 2>/dev/null | head -1)"
case "$HOLDER" in
  qa-g33*) echo "REFUSING: the Laptop-DEV jest lock is HELD by '$HOLDER' — a gate-33 holder already exists" >&2; exit 90 ;;
  '') ;;
  *) echo "NOTE: the Laptop-DEV jest lock is held now by '$HOLDER' (FIFO; the gate queues behind it, never touches it)" >&2 ;;
esac
GQ="$(grep -lE '^tag=' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${GQ:-0}" = "0" ] || echo "NOTE: $GQ ticket(s) queued in $LOCKQ_J — FIFO; gate 33 waits behind them, never touches them" >&2
LB_WAS="${NEXUSAI_LOCK_BASE:-}"
[ -z "$LB_WAS" ] || [ "$LB_WAS" = "$LOCK_BASE_LAPTOP" ] || echo "NOTE: NEXUSAI_LOCK_BASE was '$LB_WAS' in the launcher's environment — REPLACED by the Laptop-DEV base before exec (ruling q)" >&2

# 22 — the SIX paths (5 M + 1 A): the list PINNED, numstat and every blob PINNED, five of six test code/tooling and the sixth the counts file, none in the guarded set.
NS="$(g diff --name-status "$BASE" "$HEAD_SHA" 2>/dev/null)"
[ "$(printf '%s\n' "$NS" | grep -c .)" = "6" ] && [ "$(printf '%s\n' "$NS" | grep -c '^M')" = "5" ] && [ "$(printf '%s\n' "$NS" | grep '^A' | cut -f2)" = "$NEW_TEST" ] \
  || { echo "REFUSING: base..head is not 6 paths = 5 M + 1 A ($NEW_TEST)" >&2; exit 22; }
PL="$(g diff --name-only "$BASE" "$HEAD_SHA" 2>/dev/null | sort)"
[ "$(printf '%s' "$(printf '%s\n' "$PL" | tr '\n' ' ' | sed 's/ $//')" | shasum -a 256 | cut -d' ' -f1)" = "$PATHS_SHA" ] || { echo "REFUSING: the sorted 6-path list's sha256 is not ${PATHS_SHA:0:12}… — the PR's file set moved" >&2; exit 22; }
[ "$(g diff-tree -r --name-only "$BASE" "$HEAD_SHA" 2>/dev/null | grep -c .)" = "6" ] || { echo "REFUSING: diff-tree base..head does not list 6 paths" >&2; exit 22; }
[ "$(printf '%s\n' "$PL" | grep -vE "$TESTCODE_RE")" = "$COUNTS_FILE" ] || { echo "REFUSING: the only non-test-code path in base..head must be $COUNTS_FILE; got: $(printf '%s\n' "$PL" | grep -vE "$TESTCODE_RE" | head -3 | tr '\n' ' ')" >&2; exit 22; }
[ "$(printf '%s\n' "$PL" | grep -cE "$GUARDED_RE")" = "0" ] || { echo "REFUSING: base..head touches a guarded path (backend/ static/ templates/ package*.json .github/ bicep/ Dockerfile HISTORY.md CLARIFICATIONS.md)" >&2; exit 22; }
[ "$(g diff --numstat "$BASE" "$HEAD_SHA" 2>/dev/null | tr '\t' ' ' | sort)" = "$(printf '%s\n' "$NUMSTAT" | sort)" ] \
  || { echo "REFUSING: base..head numstat is not the briefed table (+147/-15; the three edited tests 2 0 each, the new test 103 0, the counts file 3 3, uat-run.js 35 12)" >&2; exit 22; }
while read -r PP PH PM; do
  [ -n "$PP" ] || continue
  [ "$(blob "$HEAD_SHA" "$PP")" = "$PH" ] || { echo "REFUSING: $PP is not blob ${PH:0:8} at 6e947f4" >&2; exit 22; }
  if [ "$PM" = "-" ]; then
    [ -z "$(blob "$BASE" "$PP")" ] || { echo "REFUSING: $PP exists at d463f88 — it is briefed as ADDED" >&2; exit 22; }
  else
    [ "$(blob "$BASE" "$PP")" = "$PM" ] || { echo "REFUSING: $PP is not blob ${PM:0:8} at d463f88" >&2; exit 22; }
  fi
done <<EOF_BLOBS
$PATH_BLOBS
EOF_BLOBS

# 93 — the premises at source: lockfile, package.json and workflow the SAME blobs at M0 and the head and equal the pins; the counts (BASE 4934/303, HEAD 4941/304, M0 READ); deploy gate.
for S in "$MAIN_SHA" "$HEAD_SHA"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] \
    || { echo "REFUSING: ${S:0:7} does not carry lockfile 19477a9 / package.json 384805d / deploy-demo.yml 953b2a2 (ruling m, r0, r7)" >&2; exit 93; }
done
[ "$(blob "$HEAD_SHA" "$COUNTS_FILE")" = "$COUNTS_BLOB_HEAD" ] && [ "$(counts_at "$HEAD_SHA")" = "4941 304" ] || { echo "REFUSING: the head's counts file is not blob 9a723cd = 4941/304 (+7 cells, +1 suite)" >&2; exit 93; }
[ "$(blob "$BASE" "$COUNTS_FILE")" = "$COUNTS_BLOB_BASE" ] && [ "$(counts_at "$BASE")" = "4934 303" ] || { echo "REFUSING: the base's counts file is not blob a28458a = 4934/303" >&2; exit 93; }
[ "$MODE" != "0" ] || [ "$M0_COUNTS" = "4934 303" ] || { echo "REFUSING: mode 0 but M0's counts file reads '$M0_COUNTS', not 4934 303" >&2; exit 93; }
[ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" "vars.CI_DEPLOY_ENABLED == 'true'")" = "2" ] || { echo "REFUSING: deploy-demo.yml at M0 no longer gates BOTH jobs on vars.CI_DEPLOY_ENABLED == 'true' (r7)" >&2; exit 93; }

# 93U — tests/uat-run.js source premises the kit's r2c rests on (read at source with a positive control; the script is NEVER executed): the demo host is in main's script and
# NOT in the head's; the head's script has the require.main guard and exports; main's has neither.
[ "$(cntF "$BASE" "$UAT" 'azurecontainerapps')" -ge 1 ] && [ "$(cntF "$HEAD_SHA" "$UAT" 'azurecontainerapps')" = "0" ] \
  || { echo "REFUSING: the demo host fragment is not in main's $UAT or is still in the head's — RD-875's premise moved (93U)" >&2; exit 93; }
[ "$(cntF "$HEAD_SHA" "$UAT" 'require.main === module')" = "1" ] && [ "$(cntF "$BASE" "$UAT" 'require.main === module')" = "0" ] \
  && [ "$(cntF "$HEAD_SHA" "$UAT" 'module.exports')" -ge 1 ] \
  || { echo "REFUSING: $UAT at the head lacks the require.main guard / module.exports, or main already had the guard (93U)" >&2; exit 93; }

# 70 — the carried rulings and Tuesday's answers (REFUSALs where a ruling is missing).
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
grep -qF 'NOT RUN under ruling (o) EXTENDED' "$BRIEF" || { echo "REFUSING: ruling (o)'s EXTENDED words are not carried in this brief" >&2; exit 70; }
[ -s "$ANS1" ] && grep -qF 'load1 below 8 before every heavy run' "$ANS1" && grep -qF 'lock base locks-laptop-1017' "$ANS1" || { echo "REFUSING: Tuesday's ANSWER-1 (load 8, lock base) is not at $ANS1 as quoted" >&2; exit 70; }
[ -s "$ADD25" ] && grep -qF 'BEFORE you run `git remote remove origin`' "$ADD25" || { echo "REFUSING: gate 25's ADDENDUM-1 (the ref order) is not at $ADD25" >&2; exit 70; }

# 70N — machine-local premises, NOTEd (the gate records what it finds).
[ -d "$NPM_CACHE/index-v5" ] || echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
PB_NOW="$(fsha "$PREBUILD")"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
NODEV="$(node -v 2>/dev/null)"
[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as the builder read (T4) — the gate records it" >&2
GLV="$(gitleaks version 2>/dev/null)"
[ -n "$GLV" ] || echo "NOTE: gitleaks is absent — r7 would be NOT RUN" >&2
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
awk -v l="${LOAD1:-99}" 'BEGIN{exit !(l < 8)}' || echo "NOTE: 1-minute load is ${LOAD1:-unknown} (not below 8) — the gate waits in the queue, never in a hold (ruling p)" >&2

# 31 — the builder's STATUS (a CLAIM; ends with the READY line for the head), the PR text, gate 32's report/instruments (PINNED), standing references.
for f in "$STATUS_B355" "$PR101TEXT" "$BRIEF_B355" "$CLAR" "$BRIEF32" "$TEMPLATE" "$G32_REPORT" "$CHARTER" \
         "$G32_INST/qa-file32.sh" "$G32_INST/qa-floorlib32.sh" "$G32_INST/qa-holdlib32.sh" "$G32_INST/qa-loadwait32.sh" "$G32_INST/qa-h1-scan32.py" "$G32_INST/qa-h1-selftest32.sh" \
         "$G32_INST/qa-mail32.py" "$G32_INST/qa-mailread32.py" "$G32_INST/qa-revert30.py" "$G32_INST/qa-to.sh" "$G32_INST/qa-floorcount.py" \
         "$G32_INST/qa-netbelt.sb" "$G32_INST/qa-netbelt-nodns.sb" "$G32_INST/qa-names23.py" "$G32_INST/qa-plantcells-32.js" \
         "$B25_INST/qa-applymut.py" "$B25_INST/qa-lockcheck.py"; do
  [ -s "$f" ] || { echo "REFUSING: evidence, brief or tool absent: $f" >&2; exit 31; }
done
[ -d "$B355_EVID" ] || echo "NOTE: the builder's evidence folder $B355_EVID is absent (a CLAIM; the gate opens it only AFTER it holds its own number, r8)" >&2
tail -n 1 "$STATUS_B355" | grep -qF "READY FOR QA: B355 RD-874 + RD-875 @ $HEAD_SHA" || { echo "REFUSING: the builder's B355 STATUS no longer ends with the READY line for 6e947f4" >&2; exit 31; }
[ "$(fsha "$STATUS_B355")" = "40f080ef8ff805464de712919d3177b43f2e47e39bb733e6240b955fb09b8546" ] || echo "NOTE: the builder's B355 STATUS sha256 is not the drafter's 40f080ef… (the file is a CLAIM and changed since drafting; the gate reads it WHOLE)" >&2
[ "$(fsha "$PR101TEXT")" = "b8c5cfd0e5617ff3114c5d7b3fba244056222e639f1b33ae4895e03584072260" ] || echo "NOTE: the B355 PR-TEXT sha256 is not the drafter's b8c5cfd0… (the gate's r6 compares the LIVE PR body, not this file alone)" >&2
grep -qF 'STATUS: COMPLETE' "$G32_REPORT" && grep -qF 'G32-1' "$G32_REPORT" || { echo "REFUSING: gate 32's report does not read as delivered or does not carry G32-1 (the mechanism source must be a COMPLETE gate)" >&2; exit 31; }
[ "$(fsha "$B25_INST/qa-applymut.py")" = "$(fsha "$G32_INST/qa-applymut.py")" ] || echo "NOTE: gate 25's qa-applymut.py differs from gate 32's copy — the gate copies gate 32's (T4)" >&2
while read -r F H; do
  [ -n "$F" ] || continue
  [ "$(fsha "$G32_INST/$F")" = "$H" ] || { echo "REFUSING: gate 32's instrument $F is not sha256 ${H:0:12}… — a COMPLETE gate's file moved" >&2; exit 31; }
done <<EOF_G32T
$G32_TOOLS
EOF_G32T
grep -qF '## 3a. INSTRUMENT RULES' "$BRIEF32" || { echo "REFUSING: gate 32's brief has no section 3a — the H-rules carried by reference are missing" >&2; exit 31; }

# 10 / 17 — the report path from the brief's §11; no stale report; the brief names its sources.
REPORT="$(grep -oE 'Report: `[^`]*/report\.md`' "$BRIEF" | head -1 | sed -E 's/^Report: `//; s/`$//')"
[ "$REPORT" = "$EXPECT_REPORT" ] || { echo "REFUSING: the brief's §11 report path '$REPORT' is not $EXPECT_REPORT" >&2; exit 10; }
[ "$(grep -oF "$(dirname "$REPORT")" "$BRIEF" | grep -c .)" -ge 2 ] || { echo "REFUSING: T4 and §11 do not name the SAME report directory" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "2026-10-20_B336_SEAT-G23_nexusai-gate32-pr98-round2.md" "2026-10-21_B355_SEAT-R11_nexusai-rd874-rd875.md" "2026-10-21_B355_STATUS.md" "2026-10-21_B355_PR-TEXT.md" \
         "2026-10-20-gate32-b336-pr98-r2" "ADDENDUM-1" "qa-file32.sh" "qa-applymut.py" "qa-netbelt.sb" \
         "qa-assertcount-preload.js" "qa-mutlib30.sh" "qa-jestwrap.sh" "qa-names23.py" \
         "QA_AGENT_CHARTER.md" "locks-laptop-1017" "models_latest.json"; do
  grep -qF -- "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || { echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
[ -d "$CLAUDE_CONFIG_DIR" ] || { echo "REFUSING: Tuesday's claude store $CLAUDE_CONFIG_DIR is absent" >&2; exit 11; }

# 12 / 13 / 14 / 15 / 20 — tier, directive, brief path, pins, verdict route, key path, question route.
for T in 'TIER 2' 'MAIN-STAMP' 'NO GO' 'NO HOST NPM REGISTRY' 'npm_config_update_notifier=false' 'BOTH thresholds block' '--replace' 'qa-g33-' 'H-34' 'H-35' 'C-63' 'C-209' 'C-68' \
         'ROUND 1' 'ESCALATED TO TIER 1' 'S8a' 'G32-1' 'FORWARD-MERGE' 'never squash' 'SIBLING' 'CARRIED' 'THE PR TEXT' \
         'VOID' 'can fail' 'positive control' 'G33-<n>' 'N33-<n>' 'NOT TESTED' 'PRIOR WORK' 'No HTTP to any production or demo host' \
         'LEGITIMATE SHAPES' 'NOT RUN under ruling (o) EXTENDED' 'NEVER EXECUTED'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'TIER-2 GATE THROUGH CODE' 'ROUND 1' 'ESCALATED TO TIER 1' 'THE ESCALATION RULE' 'THE PROPERTIES' 'S8a' 'G32-1' 'sibling sweep' 'FORWARD-MERGE' 'THE PR TEXT' \
         'r0' 'r1' 'r1c' 'r2' 'r3' 'r4' 'r5' 'r6' 'r7' 'r8' 'C-209' 'C-190' 'C-68' 'T0' 'T1' 'NAMED NOT RUN' 'NOT RUN' '--replace' \
         'qa-g33-' 'locks-laptop-1017' 'jest lock' "Never trust the builder's logs" 'no HTTP to any production or demo host' 'One client only' 'NO docker object and NO az' 'no model call' \
         'MERGES GO FIRST' 'QUEUE, NEVER TAKE OVER' 'Sonnet' 'PROVISIONAL' 'CodeQL is NOT RUN by this gate' 'FINDINGS-ONLY' 'never squash' 'SAME commit' 'is NEVER executed'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$HEAD_SHA" "$HEAD_TREE" "$C1_SHA" "$BASE" "$BASE_TREE" "$LOCK_SHA_INST"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in $CHAIN_SHAS; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name commit ${S:0:7}" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9:-]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
case "$PROMPT" in *"/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
[ -s "$TUE/4_Credentials/.env" ] || { echo "REFUSING: the AgentMail key file $TUE/4_Credentials/.env is absent" >&2; exit 20; }
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi
if printf '%s\n' "$PROMPT" | grep -qF 'KK_T9_External_HDD'; then echo "REFUSING: the prompt names a T9 path — every path of this gate is on /Volumes/Laptop-DEV" >&2; exit 15; fi
[ "$(grep -oE 'qa-g33-[A-Za-z0-9_<>-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-g33- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-g33-[A-Za-z0-9_<>-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-g33- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED: the kit and the prompt must not instruct it.
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield" >&2; exit 41; fi
done

# 82 — THE MODEL RULE is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Opus 4.8' 'which rows ran on which model'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
done
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model'; do
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## MODEL RULE' "$BRIEF" && grep -qF 'H-28 (AMENDED)' "$BRIEF" && grep -qF '**H-34**' "$BRIEF" && grep -qF '**H-35**' "$BRIEF" \
  || { echo "REFUSING: brief lacks the MODEL RULE section or H-28 (amended)/H-34/H-35" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; T-slot form; clarification quotes.
WORDS="C-190 C-209 C-185 C-192 C-205 C-141 C-63 C-40 C-68 C-76 C-102 C-112 C-174 C-49 C-89 C-115 C-125 C-130 C-131 C-57 ADDENDUM%7
r2 r3 r4 r5 r6 r7 r8 M0 d463f88 6e947f4 a7e8f4f PR%#101 PR%#97 PR%#96 PR%#67 19477a9 RD-874 RD-875 RD-810 SEAT-R11 B355 S101O
L-R1 L-R7 L-Y1 H-1 H-3 H-4 H-6 H-14 H-17 H-20 H-21 H-24 H-27 H-28 H-29 H-31 H-33 H-34 H-35 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
_prebuilds --mirror EXCLUSIVE STOP VOID MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER SAME-PLACE%handover HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED
MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes TRACKED%child Prior%work FOREGROUND NEVER%push NEVER%merge Partner%Center npm%install
--offline ENOTCACHED qa-file32.sh -r<N> instrument never%fixes never%dismissed PROVISIONAL qa-g33 G33-<n> N33-<n> 1-minute%load%of%8 g33/ qa-applymut.py
qa-assertcount-preload.js qa-names23.py qa-jestwrap.sh qa-mutlib30.sh qa-plantcells-32.js forward%merge UAT_BASE settings_x.json M-port M-default M-cert no-op ESCALATION
H2 H4 H1a H1b H3 qa-g33-H3 node%--check --update-counts"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
# this kit's sections (gate 32's '## PRIOR ROUND', '## 3b', '## 7. THE GATED TREE' do not exist in a round-1 kit and are not required)
for H in '^## TIER' '^## 2a-T. LEGITIMATE SHAPES' '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## MODEL RULE' '^## Charter' \
         '^## 1. Target' '^### How to build your trees' '^## 2. Tier and severity' '^## 2b. ROWS' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' \
         '^## 8. CI, ALERTS, DEPLOY' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## PROVENANCE' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
[ -n "$WSTART" ] && [ -n "$WEND" ] && [ "$WSTART" -lt "$WEND" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|RELAYED|own actions' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED / RELAYED: $WUNMARKED" >&2; exit 19; }
for L in L-R1 L-R2 L-R3 L-R4 L-R5 L-R6 L-R7 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
for R in r0 r1 r1c r2 r3 r4 r5 r6 r7 r8; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
# the rulings: T0 T1 T3 T4 T5 are '**(Tn) …:** RULED: …'; THIS kit's T2 is '**(T2) tests/uat-run.js IS NEVER EXECUTED, … in any form** (binding…)' (no RULED word) — its own form is required
for n in 0 1 3 4 5; do
  grep -qE "^- \*\*\(T${n}\) [^*]*:\*\* RULED: " "$BRIEF" || { echo "REFUSING: brief lacks the ruling (T$n) as '**(T$n) …:** RULED: …'" >&2; exit 19; }
done
grep -qE '^- \*\*\(T2\) tests/uat-run\.js IS NEVER EXECUTED[^*]*\*\*' "$BRIEF" || { echo "REFUSING: brief lacks the ruling (T2) '**(T2) tests/uat-run.js IS NEVER EXECUTED, …**'" >&2; exit 19; }
# each clarification must still be in CLARIFICATIONS.md VERBATIM (the stale-quote check, unchanged); on the BRIEF side this kit paraphrases several, so it must carry the sentence
# verbatim OR the clarification's id (C-63 …) — gate 32's kit quoted all verbatim.
while IFS= read -r QL; do
  [ -n "$QL" ] || continue
  Q="${QL%|*}"; CID="${QL##*|}"
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  if [ -n "$CID" ]; then
    grep -qF -- "$Q" "$BRIEF" || grep -qF -- "$CID" "$BRIEF" || { echo "REFUSING: brief neither quotes '$Q' nor names $CID" >&2; exit 19; }
  else
    grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
  fi
done <<'CLAR_EOF'
The jest and docker lock (`session-tools/nexusai-lock.sh`) is first-in-first-out, and it takes over an ownerless lock after 30 s.|C-63
a FAILED ls-remote is UNKNOWN, never a value.|C-192
A check must be able to fail on the thing it claims to be about.|C-40
An explanation of why a fix works is a CLAIM: it gets a red proof, or it is marked UNVERIFIED in the artefact that carries it.|C-76
A declared limit is where the evidence stops — not a place it is cleared.|C-112
NEVER KILL BY PATTERN.|C-174
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.|C-190
`alerts_threshold = errors`, so ANY new alert whose RULE severity is `error` blocks, whatever its security severity.|C-190
A PR's CodeQL run CANNOT show a PRE-EXISTING main alert as fixed|C-209
A gate verdict is valid only at the head it ran on. If product code a cell reads or drives changes before that branch merges, the merge condition is not "verify passes" — it is RE-RUNNING THE AFFECTED CELLS on the new head, each named individually in the MERGED mail.|C-68
Gate (`qa-*`) tickets are never moved; the holder is never touched.|
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line read from the brief (ONE line); appended to the prompt at exec.
for w in 'DEADLINE' 'HEARTBEAT' 'qa-g33-' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER' \
         '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' 'never idles holding a lock' \
         'ONE focused hold at a time' 'FOREGROUND' 'Never two live holds' 'Every finding names its instrument' \
         'NOT TESTED' 'The tester never fixes' 'ONE CLIENT ONLY' 'no CodeQL alert dismissed' 'below a 1-minute load of **8**'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
NOTTESTED_LINE="$(grep -E '^  Not tested by this gate: ' "$BRIEF" | sed 's/^  //')"
[ "$(printf '%s\n' "$NOTTESTED_LINE" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: the brief must carry exactly ONE '  Not tested by this gate: …' line (§11)" >&2; exit 71; }
for w in 'the CodeQL closure of any alert' 'the full jest suite on Node 24' "the new test run against main's unchanged tests/uat-run.js" 'any execution of tests/uat-run.js' \
         'the settings-plant cells in the other 25 test files' 'the fallback-directory shape' 'compound mutants' 'the forward-merge head' \
         'the Playwright e2e specs' 'headed Chrome and every browser' 'Windows' 'the demo and any deployed revision' 'npm audit' 'the host npm registry'; do
  case "$NOTTESTED_LINE" in *"$w"*) ;; *) echo "REFUSING: the brief's NOT TESTED line lacks '$w'" >&2; exit 71 ;; esac
done
grep -qF 'and its LAST two lines, verbatim as mailed' "$BRIEF" || { echo "REFUSING: brief must fix the report's last lines as the two verdict lines" >&2; exit 71; }
for V in '`B359/PR101: <GO|GO WITH FINDINGS|NO GO|ESCALATED TO TIER 1> @ ' '`LANDING CHECKLIST: PR #101 '; do
  grep -qF -- "$V" "$BRIEF" || { echo "REFUSING: the brief's §11 lacks the verdict line '$V'" >&2; exit 71; }
done

# 76 / 77 / 79 — H-1's printer and forbidden idioms; H-4; H-7/H-8/H-21.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET:-…}' 'echo $SESSION_SECRET' 'printenv'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done
for w in 'H-4' 'heartbeat' 'within 90 s' 'max gap'; do grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat fragment '$w' (H-4)" >&2; exit 77; }; done
for w in 'H-7/H-8/H-21' 'FAILS LOUDLY' 'trap'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing fragment '$w' (H-7/H-8)" >&2; exit 79; }; done

# 38R — the negative-control seats are DERIVED now from the live cockpit panes: the claude descendant of each pane pid.
# ps, not pgrep: macOS pgrep hides the caller's own ancestors, so Tuesday's own claude would vanish when --check runs from her shell.
command -v tmux >/dev/null 2>&1 || { echo "REFUSING: tmux not found — cannot derive the negative-control seats" >&2; exit 38; }
PANES="$(tmux list-panes -a -F '#{pane_pid} #{@cockpit_name}' 2>/dev/null)"
[ -n "$PANES" ] || { echo "REFUSING: tmux list-panes returned nothing — cannot derive the negative-control seats" >&2; exit 38; }
PSTAB="$(ps -axo pid=,ppid=,comm= 2>/dev/null)"
[ -n "$PSTAB" ] || { echo "REFUSING: ps returned nothing" >&2; exit 38; }
claude_under() {   # prints the claude pids among the descendants (depth <= 5) of pane pid $1
  printf '%s\n' "$PSTAB" | awk -v root="$1" '
    { pid[NR]=$1; pp[NR]=$2; c=$3; sub(/^.*\//,"",c); cm[NR]=c }
    END { lvl[root]=0; for (d=1; d<=5; d++) for (i=1;i<=NR;i++) if ((pp[i] in lvl) && !(pid[i] in lvl) && lvl[pp[i]]==d-1) lvl[pid[i]]=d;
          for (i=1;i<=NR;i++) if ((pid[i] in lvl) && pid[i]!=root && cm[i]=="claude") print pid[i] }'; }
pane_pid_of() { printf '%s\n' "$PANES" | awk -v n="$1" '{p=$1; $1=""; sub(/^ /,""); if ($0==n) print p}'; }
NEG_SEATS=''; NEG_DESC=''; NEG_BUILDERS=0
COORD_NAME=''
for NAME in tuesday wednesday; do
  if [ -n "$(pane_pid_of "$NAME" | sed '/^$/d')" ]; then
    [ -z "$COORD_NAME" ] || { echo "REFUSING: panes named BOTH 'tuesday' and 'wednesday' are live — the coordinator's negative control is ambiguous" >&2; exit 38; }
    COORD_NAME="$NAME"
  fi
done
[ -n "$COORD_NAME" ] || { echo "REFUSING: no tmux pane named 'tuesday' or 'wednesday' — the coordinator's negative control is required" >&2; exit 38; }
[ "$COORD_NAME" = "tuesday" ] || echo "NOTE: the coordinator's pane is named '$COORD_NAME' on this machine — used as the coordinator's negative control" >&2
# Tuesday s126 2026-10-20 (B336 drafter Q1, ruled): no NexusAI builder need be live; any live Datasec claude seat is a valid negative control (a foreign process the gate must never touch).
# Gate 33 adds Datasec/NexusAI-R11 (the B355 builder, finished) to the candidate list; a missing pane is a NOTE, never a refusal.
for NAME in Datasec/NexusAI-O Datasec/NexusAI-W17 Datasec/NexusAI-L7 Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-P Datasec/NexusAI-R Datasec/NexusAI-R11 Datasec/Security-Composer-W13 Datasec/Security-Composer-G22 Datasec/HPSM-POC-D5 "$COORD_NAME"; do
  PP="$(pane_pid_of "$NAME")"
  NP="$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')"
  if [ "$NP" = "0" ]; then
    [ "$NAME" = "$COORD_NAME" ] || echo "NOTE: no tmux pane named '$NAME' — not a negative control this launch" >&2; continue
  fi
  [ "$NP" = "1" ] || { echo "REFUSING: more than one tmux pane named '$NAME': '$PP' — cannot derive its negative-control seat" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
  [ "$NAME" = "$COORD_NAME" ] || NEG_BUILDERS=$((NEG_BUILDERS + 1))
done
[ "$NEG_BUILDERS" -ge 1 ] || { echo "REFUSING: no live builder seat among Datasec/NexusAI-O/W17/L7/M/N/P/R/R11, Security-Composer-W13/G22, HPSM-POC-D5 — at least ONE negative control is required" >&2; exit 38; }
# fleet-monitor and every live 'QA/*' pane other than this gate's own (gate 29 is LIVE at drafting): a negative control when exactly one claude runs under it.
EXTRA="$(printf '%s\n' "$PANES" | awk '{p=$1; $1=""; sub(/^ /,""); print $0}' | grep -E '^(QA/|fleet-monitor$)' | grep -vxF "$ROUTE_NAME" | sort -u)"
while IFS= read -r PEER; do
  [ -n "$PEER" ] || continue
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER);"
    echo "NOTE: $PEER has a live claude — added as a negative control (FIFO, never touched)" >&2
  else
    echo "NOTE: $PEER has no single live claude — not a negative control" >&2
  fi
done <<EOF_PEERS
$EXTRA
EOF_PEERS
NEG_SEATS="${NEG_SEATS# }"
NCOUNT="$(printf '%s\n' $NEG_SEATS | sed '/^$/d' | wc -l | tr -d ' ')"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "$NCOUNT" ] || { echo "REFUSING: the derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }

# 86 — no live gate-33 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 33 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32S / 40 — LAST: the coordinator's stamp (0 '@NAME@' placeholders anywhere in the kit: MAIN_SHA x2 + STAMP_TIME x1; the LAST line reads
# 'READ-WHOLE-BY-TUESDAY: DONE …', never PENDING) and the answer route (Tuesday adds it, never this launcher).
NSLOT="$(grep -oE "$PH_RE" "$BRIEF" | grep -c .)"
LASTLINE="$(sed '/^[[:space:]]*$/d' "$BRIEF" | tail -n 1)"
if [ "$NSLOT" != "0" ] || ! printf '%s' "$LASTLINE" | grep -qE '^READ-WHOLE-BY-TUESDAY: DONE .+'; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
GUARDS='9 40 18T 18 6 18M 7 8 90 22 93 93U 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 79 38R 86'
SUMMARY="ls-remote attempts this run: $LSR_ATTEMPTS (C-192); origin main ${M_ORIGIN:0:7} (M0 ${MAIN_SHA:0:7} tree ${M0_TREE:0:7}; counts at M0 $M0_COUNTS; ancestry carries d463f88; the 2 PR commits not on M0; MODE $MODE; fast-forwardable: $FFABLE; landed since d463f88: $LANDED); PR101 ${HEAD_SHA:0:7} (tree ${HEAD_TREE:0:7}; branch and $PR_REF agree; 2 linear commits over d463f88; 6 paths = 5 M + 1 A, +147/-15, list sha256 ${PATHS_SHA:0:8}…, every blob pinned; head counts 4941 304, base counts 4934 303; lockfile/package/workflow blobs = M0's; uat-run.js: demo host gone, require.main guard present); gate-32 instruments x10 pinned; lock tool ${INST_NOW:0:12}…; model $MODEL"
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass ($GUARDS); stamp and/or route NOT complete." >&2
  echo "  $SUMMARY" >&2
  [ -z "$PROVISIONAL" ] || echo "  PROVISIONAL (unstamped slots, --check ran against):$PROVISIONAL" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$ROUTE_OK" = "1" ] || echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32S): $NSLOT at-sign placeholder(s) remain in the brief (MAIN_SHA x2 + STAMP_TIME x1), or its last line is not 'READ-WHOLE-BY-TUESDAY: DONE …' (it reads: '${LASTLINE:0:60}') — the coordinator reads the kit whole and stamps before launch" >&2
  [ "$STAMP_OK" = "1" ] || exit 32
  exit 40
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin at $PIN_TS ($LSR_ATTEMPTS ls-remote attempt(s), C-192): main = the stamped pin ${MAIN_SHA:0:12} exactly; the branch and $PR_REF at 6e947f4; T9 unmounted (18T)"
  echo "  $SUMMARY"
  echo "  stamped launch time: $S_LAUNCH"
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC"
  echo "  report: $REPORT"
  echo "  SUBJECT: $SUBJECT"
  echo "  NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT
$NOTTESTED_LINE

THE MODEL OF THIS SESSION (the --model, models_latest.json levels.sonnet.model_id): $MODEL.
WRITE YOUR ONE REPORT TO: $REPORT
VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192; Tuesday's stamped launch time $S_LAUNCH): refs/heads/main = $M_ORIGIN = the stamped MAIN pin M0 (tree $M0_TREE; counts file at M0 reads $M0_COUNTS; its ancestry carries d463f88; PR #101's two commits are not on it; what landed since d463f88: $LANDED; MODE $MODE; the head fast-forwardable onto M0: $FFABLE — mode 0 means main equals the PR's base, the gated tree is the head itself and main did not move, otherwise T0's ruling applies and the merged tree is r5(d)); refs/heads/$BR = $PR_REF = $HEAD_SHA (tree $HEAD_TREE). The head is 2 linear commits over d463f88 (a7e8f4f RD-874, 6e947f4 RD-875); its 6 paths are 5 modified and 1 added, +147/-15, every blob pinned: three test files +2/-0 each, the new rd875 test +103, tests/uat-run.js +35/-12 (the demo host fragment is gone from it and it carries the require.main guard and its exports) and the counts file +3/-3 (4934/303 to 4941/304); none is a backend, static, package, workflow or HISTORY path; the lockfile, package.json and deploy-demo workflow are the same blobs at M0 and the head. PR #97 reads ${P97_NOTED:0:8} and PR #67 ${P67_NOTED:0:8} as the drafter noted them (both also edit the counts file). Gate 32's instruments match their pins. The T9 is unmounted. The installed lock tool $LOCKTOOL sha256 $INST_NOW equals the pin and NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP is exported in your environment. These are the start-of-gate pins; take your own three readings anyway.
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS (the coordinator's pane is named '$COORD_NAME' on this machine):$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET (and the new test never needs UAT_BASE: it is dropped too). The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET
if [ -n "${UAT_BASE+x}" ]; then echo "UAT_BASE SET in the launcher's environment — unsetting before exec"; else echo "UAT_BASE UNSET"; fi
unset UAT_BASE
# ruling q / H-34: the gate's lock calls use the Laptop-DEV base while the T9 is unmounted.
export NEXUSAI_LOCK_BASE="$LOCK_BASE_LAPTOP"
# ruling (m): the gate's own npm calls inherit the notifier switch (the gate still passes it explicitly on every call).
export npm_config_update_notifier=false

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model "$MODEL" "$PROMPT"
