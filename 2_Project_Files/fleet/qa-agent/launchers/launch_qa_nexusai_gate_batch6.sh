#!/bin/bash
# launch_qa_nexusai_gate_batch6.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch #6", lane 4: settings UI + brand,
# tests and docs), SIX targets, SIX verdicts, ONE report (2026-09-27), plus two OPTIONAL members Tuesday may include at stamp:
#   A — RD-693 (TIER 1 + REAL-BROWSER leg R11): rd-693-token-clear-on-leave-s85p @ ddf1b75 = 4a86c4a (cells, off 1904765) + the fix + counts.
#       static/js/entra-provisioning-ui.js +32/-0 (pagehide / pageshow-persisted clear). 4137/248. Lane-1 half RD-705 is batch 5a's, not here.
#   B — RD-286 (TIER 2 + browser leg): rd-286-ground-geometry-guards-s85p @ 1645c69, 10 commits (forward merge a09dd83 of 1904765).
#       dark-mode.css: exactly two declarations deleted (C-172) + three authorised comment changes; a tests/e2e spec outside verify. 4133/247.
#   C — RD-204 (TIER 2, tests only): rd-204-vendor-coverage-s84p @ fe47bb4 (forward merge 83e5a1b of 1904765) + counts. 4148/248.
#   D — RD-197 (TIER 2, tests only, option (b)): rd-197-emphasis-ground-guard-s84p @ 43e729c (forward merge cd589e0 of 1904765) + counts. 4142/248.
#   E — RD-686 (+RD-694 items 1-3) (TIER 2, words only): rd-686-694-brand-wording-s85p @ 8962a14, one commit on 1904765. 4133/247.
#   F — RD-692 (TIER 2, tests only): rd-692-provisioning-token-guards-s85p @ 4580829 = 078c8c0 + 3dcd1c0 + counts, on 1904765. 4138/248.
#   OPTIONAL G — RD-430 (re-pin pending, C-175) and OPTIONAL H — RD-694 item 4 (1d457ce, NOT on origin at drafting): OFF unless OPT_G_HEAD /
#       OPT_H_HEAD are set below AND the brief's "STATUS:" line for that member reads INCLUDED @ <the same sha> (guard 85).
#   Main at drafting 1904765. The six deltas are pairwise file-disjoint except scripts/verify-expected-counts.json, which A, C, D and F change
#   (six counts-only pairs). The gate RE-PINS main (M0), merges M0 + 686, 286, 204, 197, 692, 693 in its OWN scratch clone, regenerates counts
#   once (predicted counts(M0) + 33/+4; 4166/251 at 1904765), and runs two real-browser legs. Batch-3 and batch-4 gates were live at drafting.
#
# AUTHORITY: Tuesday's batch #6 commission (2026-09-27); READY mails from NexusAI-P, copies in briefs/. Merges: Tuesday's GO/RELEASE after a
# verdict at head (Kam 2026-09-25 ~22:0x "merge once tested", re-affirmed 2026-09-27 ~08:2x; C-175: the lane-4 seat is the merge author).
#
# PATTERN: launch_qa_nexusai_gate_batch4.sh (guard families 9 6 7 8 18 22 75 23 35 70 31 39 10 17 11 12-15 20 19 24 53 71 76 77 79 38 32 40),
# prompt EMBEDDED. CHANGES, each deliberate:
#   - 7: every head contains main 1904765 (no per-ticket bases).
#   - 8: chains exact, incl. the long lane-4 histories of RD-286 (10), RD-204 (8) and RD-197 (7).
#   - 23: EXPECTED OVERLAPS: {A,C,D,F} pairwise = counts only; every pair with B or E = nothing.
#   - 81 (REPURPOSED): the PALETTE is untouched — tokens.css and derive-brand-tokens.js byte-identical to main at every head (Kam's call).
#   - 83 (NEW): RD-693's product hunk is additions only (no existing clear touched).
#   - 84 (NEW): RD-286's comment-stripped dark-mode.css differs from main by exactly the two deleted background-color declarations (C-172).
#   - 85 (NEW): optional members G/H consistent between this launcher and the brief; an included head must be on origin.
#   - 78 (REPURPOSED): the token rule (H-19) instead of byte plants; 80 (REPURPOSED): the browser-leg rules (H-18) instead of docker.
#   - 82: the other-gates rule (batch-3, batch-4, batch-5a) in brief and prompt.
#   - 40: the routing line QA/NexusAI-batch6 must exist (Tuesday adds it; the drafter could not — outside the two output files).
#   - 32: SELF-CHECK stamp placeholder (see PH_STAMP; comparand built by concatenation). LAST refusal before --check exits.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-batch6' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote), grep, python3 (stdin only), ps, tmux, command -v.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch6.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..85 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

PH_STAMP='@STA''MP@'

# ---------------------------------------------------------------- OPTIONAL MEMBERS (Tuesday sets at stamp; empty = EXCLUDED)
OPT_G_HEAD=''     # RD-430 re-pinned head (40-hex), branch rd-430-remove-response-form-s84p
OPT_G_READY=''    # absolute path of RD-430's READY mail copy under briefs/
OPT_H_HEAD=''     # RD-694 item 4 head (40-hex; 1d457cef2a1b1a66454a3ce77d751be56fa8bbbc at drafting, NOT on origin), branch rd-694-fixture-about-s86p
OPT_H_READY=''    # absolute path of RD-694 item 4's READY mail copy under briefs/
G_BRANCH='rd-430-remove-response-form-s84p'
H_BRANCH='rd-694-fixture-about-s86p'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
BRIEF="$BRIEFS/2026-09-27_nexusai-gate-batch6-rd693-rd286-rd204-rd197-rd686-rd692.md"
READY_A="$BRIEFS/2026-09-27_nexusai-rd693-READY-mail.txt"
READY_B="$BRIEFS/2026-09-27_nexusai-rd286-READY-mail.txt"
READY_C="$BRIEFS/2026-09-26_nexusai-rd204-READY-mail.txt"
READY_D="$BRIEFS/2026-09-26_nexusai-rd197-READY-mail.txt"
READY_D2="$BRIEFS/2026-09-26_nexusai-rd197-correction-READY-mail.txt"
READY_E="$BRIEFS/2026-09-26_nexusai-rd686-694-READY-mail.txt"
READY_F="$BRIEFS/2026-09-26_nexusai-rd692-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_P="$NX/session-tools/s85p"
EV_P4="$NX/session-tools/s84p"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
PREV_B2="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/report.md"
B2_EV="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/evidence"
B1_EV="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch1/evidence"
PREV_FLOORLIB="$B1_EV/qa-floorlib.sh"
G7R1_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-27-gate-batch6/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch6'

MAIN_SHA='1904765007e9447ac6c980f9840c0689a02abe6c'      # origin main at drafting
M_5F26='5f2683cd198067016d56a32ec4e1f46f4e45dcc6'         # older main heads the long chains merged
M_748C='748cecec2a883a117560824ac5615c268dfe0800'
M_1166='11666d3c4f615190646914270016419fffa642e2'
M_7C47='7c47ec467f585e9db5daf3a82cdb96deae0b1e7a'

A_BRANCH='rd-693-token-clear-on-leave-s85p'
A_CELLS='4a86c4a5d6beb55135bc372bfe9ef6fdc915c0a6'
A_HEAD="${QA_A_HEAD_OVERRIDE:-ddf1b75f7c3c4aead2da2ce9b3c0b724fb4b3969}"
B_BRANCH='rd-286-ground-geometry-guards-s85p'
B_FWD='a09dd834e87e116e2fd37b07c2f0be7c40aa55aa'
B_C219='c21989085772a08128b7dfe9d55d0ced388a1f8b'
B_HEAD="${QA_B_HEAD_OVERRIDE:-1645c69eeb9a28a267b44b5ffe7fd5fdb51149b2}"
C_BRANCH='rd-204-vendor-coverage-s84p'
C_FWD='83e5a1b274a37c0a8e19d02ffa01e2ad1941ee4b'
C_A195='a19559f29a205924ad93a54b1727d0707c18b11f'
C_HEAD="${QA_C_HEAD_OVERRIDE:-fe47bb49124805a67ca79274104309e4c902041c}"
D_BRANCH='rd-197-emphasis-ground-guard-s84p'
D_FWD='cd589e098cbccf6351fb19b7159d61fe171aa63a'
D_3F91='3f912422c427e93291d6b0d1f3d8ded39935d82f'
D_9C74='9c742fa3d1db112ac5621c0b142845c7410328b8'
D_HEAD="${QA_D_HEAD_OVERRIDE:-43e729cbf056cd7ff064535372e7b2b2f23fcc5f}"
E_BRANCH='rd-686-694-brand-wording-s85p'
E_HEAD="${QA_E_HEAD_OVERRIDE:-8962a149798531b61eddd22361dec1261a372f4e}"
F_BRANCH='rd-692-provisioning-token-guards-s85p'
F_FIX='3dcd1c0ff8b0505f47b5288917b4732089b5c63a'
F_HEAD="${QA_F_HEAD_OVERRIDE:-4580829aa7ad1c1cfee969d89885b6d87e1205ca}"

A_CHAIN="$A_HEAD $A_CELLS
$A_CELLS $MAIN_SHA"
B_CHAIN="$B_HEAD $B_C219
$B_C219 fa72606738afde358a9bdf776eb137bf75c79596
fa72606738afde358a9bdf776eb137bf75c79596 1d588816cd868e14cccb25fcca21ff9d48f911bd
1d588816cd868e14cccb25fcca21ff9d48f911bd fc0278d4e5894d0a152225bcf31350fe0bcd2fb8
fc0278d4e5894d0a152225bcf31350fe0bcd2fb8 c2d84eca48af1249ad5e4baf80162e48e2879622
c2d84eca48af1249ad5e4baf80162e48e2879622 30332b10b0e152f072a3f270f071a93664c22a74
30332b10b0e152f072a3f270f071a93664c22a74 58b20d33fa38c896e929c62b0177ed74e38a20a8
58b20d33fa38c896e929c62b0177ed74e38a20a8 $B_FWD
$B_FWD e5f03b6dc46602b814a03fa53e4248d829235caa $MAIN_SHA
e5f03b6dc46602b814a03fa53e4248d829235caa $M_5F26"
C_CHAIN="$C_HEAD $C_FWD
$C_FWD 8bb4e73f6c9cde432ff89f73147a05007991f37a $MAIN_SHA
8bb4e73f6c9cde432ff89f73147a05007991f37a 82798e306dcbcea1d5d71eca2c975b6dd92aaad6 $M_748C
82798e306dcbcea1d5d71eca2c975b6dd92aaad6 $C_A195
$C_A195 cbe02436101b9bd913226619b86d7a8c468f09cd $M_5F26
cbe02436101b9bd913226619b86d7a8c468f09cd dfc92b4923247e2719fbf2ddfe3203460a4fb63f
dfc92b4923247e2719fbf2ddfe3203460a4fb63f 72cd3db7d1b160cd26599b6656eee662c56ffbd2 $M_1166
72cd3db7d1b160cd26599b6656eee662c56ffbd2 $M_7C47"
D_CHAIN="$D_HEAD $D_FWD
$D_FWD f4dd74d22ad15e52681c44d347c0d74d6e2ec682 $MAIN_SHA
f4dd74d22ad15e52681c44d347c0d74d6e2ec682 $D_9C74
$D_9C74 a08ca380205782b17bc1f4025edf39e311c72753 $M_5F26
a08ca380205782b17bc1f4025edf39e311c72753 $D_3F91
$D_3F91 7d87d74d0825c1fd96840213461e8b7a56545778 $M_1166
7d87d74d0825c1fd96840213461e8b7a56545778 $M_7C47"
E_CHAIN="$E_HEAD $MAIN_SHA"
F_CHAIN="$F_HEAD $F_FIX
$F_FIX 078c8c020fcaddc6bd8c363c83a22a899e9de762
078c8c020fcaddc6bd8c363c83a22a899e9de762 $MAIN_SHA"

COUNTS_FILE='scripts/verify-expected-counts.json'
UI='static/js/entra-provisioning-ui.js'
DARK='static/css/dark-mode.css'
A_EXPECTED_FILES="__tests__/rd693-token-cleared-on-leave.test.js
$COUNTS_FILE
$UI"
B_EXPECTED_FILES="$DARK
tests/e2e/rd286-ground-and-geometry.spec.js"
C_EXPECTED_FILES="__tests__/helpers/dom.js
__tests__/helpers/vendor-surface.css
__tests__/rd204-bootstrap-5.3.0-painting.json
__tests__/rd204-vendor-coverage.test.js
$COUNTS_FILE"
D_EXPECTED_FILES="__tests__/rd197-emphasis-on-notice-ground.test.js
$COUNTS_FILE"
E_EXPECTED_FILES="__tests__/helpers/css-colors.js
docs/BRAND.md"
F_EXPECTED_FILES="__tests__/rd692-provisioning-token-guards.test.js
$COUNTS_FILE"
G_EXPECTED_FILES="__tests__/dom-harness.test.js
__tests__/jsdom-instrument-limits.test.js
__tests__/rd430-response-form-removed.test.js
$COUNTS_FILE
static/js/settings.js
static/settings.html"
H_EXPECTED_FILES="__tests__/fixtures/rd200-js-brand-debt.json"

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
TOKENS_BLOB_SHORT='de6e0fe'       # static/css/tokens.css at main — the palette
DERIVE_BLOB_SHORT='d94423a'       # scripts/derive-brand-tokens.js at main
NEG_SEATS='62649 9959 20317 23230'   # NexusAI-M %19, -N %21, -P %22, Tuesday %0 — read 2026-09-27 09:31:51 AEST

SUBJECT_BASE='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-693 · RD-286 · RD-204 · RD-197 · RD-686 · RD-692'
SUBJ_SUFFIX=''
[ -n "$OPT_G_HEAD" ] && SUBJ_SUFFIX="$SUBJ_SUFFIX · RD-430"
[ -n "$OPT_H_HEAD" ] && SUBJ_SUFFIX="$SUBJ_SUFFIX · RD-694"
SUBJECT="${SUBJECT_BASE}${SUBJ_SUFFIX}"
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch6] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, browsers other than the installed Google Chrome, viewports other than those the gate names, Azure Container Apps and the demo, a real Entra SCIM client, the release pipeline's own image build and any registry, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "${1}:${2}" 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI — batch #6, lane 4, settings UI and brand, tests and docs — with SIX targets, SIX verdicts and ONE report: RD-693 (TIER 1), RD-286 (TIER 2), RD-204 (TIER 2), RD-197 (TIER 2), RD-686 (TIER 2) and RD-692 (TIER 2). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict; a finding that exists only in a COMPOSITION is graded on the merged tree and named against both tickets it joins.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-gate-batch6-rd693-rd286-rd204-rd197-rd686-rd692.md
Then the charter it names, then the six READY mails it names and the RD-197 correction mail (read each WHOLE), then the batch-2 gate report it names (2026-09-26-gate-batch2-rd428-rd444-rd200) — its finding A-F1 became RD-692, its note A-N5 became RD-693, its finding C-F1 became RD-694 (items 1-3 ride with RD-686), and its self-correction S-4 is how a real bfcache is measured. The brief's section 3a turns the earlier gates' lessons into rules H-1 to H-20 that bind you. Every builder statement is a CLAIM, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a: A, B, C, D, E, F) are required measurements, row by row, base and head in the same window.

THE TARGETS. RD-693: branch rd-693-token-clear-on-leave-s85p at ddf1b75f7c3c4aead2da2ce9b3c0b724fb4b3969 = red-first cells 4a86c4a5d6beb55135bc372bfe9ef6fdc915c0a6 on main 1904765007e9447ac6c980f9840c0689a02abe6c, then the fix and counts; the provisioning UI module gains a pagehide and a pageshow-persisted clear of the shown-once SCIM token, additions only. Its lane-1 half RD-705 (no-store on every HTML page) is gated elsewhere (batch 5a) — never grade it; measure only how it changes the bfcache leg if it is on M0. RD-286: branch rd-286-ground-geometry-guards-s85p at 1645c69eeb9a28a267b44b5ffe7fd5fdb51149b2, ten commits including a forward merge of main at a09dd834e87e116e2fd37b07c2f0be7c40aa55aa and the ruling-(a) state c21989085772a08128b7dfe9d55d0ced388a1f8b; the dark sheet loses exactly two duplicate background-color declarations (C-172) and carries three authorised comment changes, plus a tests/e2e spec outside verify. RD-204: branch rd-204-vendor-coverage-s84p at fe47bb49124805a67ca79274104309e4c902041c, forward-merged onto main at 83e5a1b274a37c0a8e19d02ffa01e2ad1941ee4b, plus counts; a coverage report of what the jsdom vendor stand-in leaves unpainted, built on a painting list derived once outside the repo. RD-197: branch rd-197-emphasis-ground-guard-s84p at 43e729cbf056cd7ff064535372e7b2b2f23fcc5f, forward-merged at cd589e098cbccf6351fb19b7159d61fe171aa63a, plus counts; option (b) only — option (a), the palette, is Kam's. RD-686: branch rd-686-694-brand-wording-s85p at 8962a149798531b61eddd22361dec1261a372f4e, one commit on main; the brand guide's rule 3 and the colour helper's header, words only. RD-692: branch rd-692-provisioning-token-guards-s85p at 4580829aa7ad1c1cfee969d89885b6d87e1205ca = 078c8c0 then 3dcd1c0ff8b0505f47b5288917b4732089b5c63a then counts; two guard cells for RD-428's token clears in a new file. The six deltas are file-disjoint except the counts file, which RD-693, RD-204, RD-197 and RD-692 all change — six counts-only pairs. The builders' merge-trees were mostly against older heads: run all fifteen pairs yourself in your own clone. The semantic overlaps U1 to U9 in the brief are UNMEASURED and are yours.

OPTIONAL MEMBERS. The brief's section 10 lists RD-430 (G) and RD-694 item 4 (H) with a STATUS line. A member whose STATUS reads EXCLUDED is not in this gate: do not gate it and do not merge it into your clone. If the launcher appended an INCLUDED paragraph below, that member is a target with its own verdict and the brief's section 10 rules bind it — including U9: a red RD-204 settings pin caused by RD-430 is a STOP to name and a QUESTION, never a re-pin by you.

MAIN IS MOVING. Main at drafting was 1904765007e9447ac6c980f9840c0689a02abe6c. RE-PIN main at your start and call it M0: it must be 1904765 or a descendant, and 1904765..M0 must share no path with the six deltas except the counts file (else STOP and ask). Moved static or test-helper files change what RD-204's pins, RD-197's sweep and the brand readers measure: re-run their named sets on M0. Your merged tree is M0 plus all six. If main moves again during your gate, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

RD-693 (TIER 1) — THE SHOWN-ONCE TOKEN MUST NOT OUTLIVE THE PAGE. POSITIVE CONTROL FIRST: the rd693 cells red at main's module (LEAVE, RESTORE, RESTORE WITHOUT A PAGEHIDE), green on the COMMITTED head — its builder's full verify ran on the cells commit plus an uncommitted fix, so yours is the first on the committed tree. Mutants M-A1 to M-A8, including a clear on visibilitychange. THE REAL-BROWSER LEG, the batch-2 gate's R11 re-run with its corrected method: launch Chrome with the default --disable-back-forward-cache removed (ignoreDefaultArgs), goBack waiting for 'commit', a pageshow recorder, and a LANDING CONTROL that a plain loopback page restores from bfcache before any row is read. Rows a1 to a14 at main, the head and the merged tree: the Back restore shows no token and says why, Forward, Reload, a blocked bfcache, a token already saved, the tab-switch journey an admin uses to paste the token into Entra (the token must SURVIVE a tab switch — a clear there is a Major regression), Graph mode, first-run-setup's instance with the identifier mask's own pageshow handler, the wire and storage audit, two restores in a row. Print a token only as first four and last four characters and its length, and mask it in every screenshot. rd692 re-run BY NAME on the merged tree.

RD-286 (TIER 2 + BROWSER) — TWO DELETIONS THAT MUST MOVE NO PIXEL. Prove the comment-stripped declaration diff over main is exactly the two deleted background-color lines, and map each comment change to its ruling (C-168, C-175). Run the spec on a surface you stand yourself from your archive tree — never scripts/qa-surface-up.sh, which adds a worktree to the NexusAI repo — with its CAN-FAIL cells seen red then green; then an INDEPENDENT pixel compare of the rank tables and the whole Sustainability tab against the REAL base (main's dark sheet rendered in its own tree), both themes, two viewports, determinism first and a positive control that a one-pixel change is seen. Mutants M-B1 to M-B4. Rows p1 to p10. Say whether any brand reader reads the light hex values the new marker comments carry.

RD-204 (TIER 2) — WHAT "PAINTS" MEANS. Re-run the builder's T1, T2b and T3 with your own mutator, and T2 (the transparent tamper that did not tamper, C-103). Then the question its READY asks: does the reading of "paints" match Bootstrap 5.3.0's own semantics? The committed list counts custom properties while the excerpt judge counts only literal properties; .btn and .btn-close are listed as painting a ground; currentcolor is treated as painting nothing. Rows c1 to c11; name the direction of every mismatch — over-report is a Minor, under-report a Major. Re-derive the painting list with a COPY of the out-of-repo derivation script over a COPY of the fetched file and compare.

RD-197 (TIER 2) — EMPHASIS COLOURS ON THEIR OWN GROUND. POSITIVE CONTROL FIRST: M1 red, M2 green as the accepted limit with its NOT REACHED line, then 9/9 at the head itself. Rows d1 to d7; is FINDABILITY a control that can fail? Option (a) stays Kam's: record the ratios, never rule.

RD-686 (TIER 2) — WORDS AGAINST MEASUREMENTS. The READY says the probe snippets are in the commit message; they are not — write your own probes. Re-derive each claim E1 to E8 at main and on the merged tree, each with a positive control, and quote the sentence beside the number. Prove the helper change is comment-only. A sentence that claims the gate reads what it does not is a Major.

RD-692 (TIER 2) — THE TWO CLEARS NOBODY GUARDED. Re-derive M-A6 and M-A10, re-run the batch-2 gate's own M-A6 and M-A10 against the new AND the old cell files, and say whether the cells are the specification A-F1 asked for or a weakening to fit (C-98).

THE MERGED TREE — part of every verdict. In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; merges and commits in the clone ONLY): M0, then merge --no-ff 8962a14 (RD-686), 1645c69 (RD-286), fe47bb4 (RD-204), 43e729c (RD-197), 4580829 (RD-692), ddf1b75 (RD-693) — the drafter's proposal; your second clone proves order independence (O2: ddf1b75, 4580829, 43e729c, fe47bb4, 1645c69, 8962a14). Predict before each merge whether the counts file conflicts, and explain any clean merge with a side control; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Resolve the counts by REGENERATION, never by hand: npm run verify -- --maxWorkers=2 --update-counts ONCE on the tree after ALL merges. Predicted counts(M0) plus 33 tests and 4 suites — 4166/251 if M0 is 1904765 — a prediction; the measurement decides; also the per-step counts. C-112's condition stated beside the conclusion, MEASURED: no test file is predicted to be content-merged, so every test file should be byte-identical to a parent — prove it before relying on byte identity; the by-name C-68 runs are owed regardless. id-superset control with the batch-1 gate's copy of the C-57 script, seven parents: predicted exact pass, missing 0; ids from jest's JSON. On the merged tree: U1 to U8 (U9 if RD-430 is included), the per-step C-68 sets, the full verify, one mutant per ticket. C-89 on your clone. Record the repo's git count-objects before and after and account for any delta. Nothing leaves your clone.

THE BRAND LEG — brief section 11b. Any colour a change introduces must resolve, by value, to a style-guide token in the theme its rule applies to (docs/BRAND.md section 3, static/css/tokens.css, linked by no page). An OFF-GUIDE colour is a Major. Palette choices are Kam's: record, never rule. Extract added colour literals after comment stripping with a positive control that a planted #123456 is found and fails; measure the RD-693 sentence's rendered colour and ground in both themes on both pages.

CI AND DEPLOY, READ ONLY. Whether any of the six branches has a PR and M0's CI Build are UNVERIFIED by the drafter — read them with gh READ ONLY or say you could not. CI NOT RUN at a head with no PR. Read — never set — whether the deploy-demo workflow's master switch is on and what the last push-to-main runs did, and state what a merge push of each member would start. gh never merges, approves, comments, labels, re-runs, dispatches or opens anything.

FULL VERIFY of each head and of the merged tree through the lock, SESSION_SECRET UNSET (verify needs Chrome, C-61). Predicted ddf1b75 4137/248, 1645c69 4133/247, fe47bb4 4148/248, 43e729c 4142/248, 8962a14 4133/247, 4580829 4138/248, merged counts(M0) plus 33/4. Every failure by NAME; re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, parse every mutated CSS file with the parser the cells use, each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-20 (brief section 3a) — earlier gates broke each of these once. H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it before the first hold and scan every hold's logs afterwards, the scan's own control planting a DIFFERENT marker. H-3: a LANDING CONTROL for every hook, interceptor, pageshow recorder, planted rule and seed. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant; report the max gap per hold (at most 120 s). H-6: every extractor, census, clip and pixel differ gets a positive control; quote every path (the QA path has spaces and a bang); the browser aborts every non-loopback request, and a CDN render, if you need one, is run separately and labelled. H-7 and H-8: mutants only through a quoted tool with a negative control; the exact new text present and the old text absent once it is removed. H-10: prove the phenomenon is reachable before measuring its absence. H-11: every script under /bin/bash, every sha:path braced. H-12: list every modified test file before the C-57 control. H-13: NUL-safe censuses. H-14: a redactor for hyphen or space separators. H-15: no inline loops under zsh. H-18: the bfcache method above. H-19: the token rule above. H-20: C-174 — stop only pids you spawned or that descend from your own claude pid; never pkill -f, never kill by pattern.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (git archive into a fresh mktemp dir under projects/nexusai/qa-trees/batch6.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive, count-objects); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean, or merge-tree --write-tree without your own scratch object directory, and never work in its 2_Project_Files checkout, any builder worktree or qa-worktree (C-28). A sha missing from the local object store is UNMEASURED — never fetch it. Scratch edits and scratch git repos ONLY under your own mktemp dirs. Findings-only: no fixes, no pushes, no deploys, no commits outside your clone, no tickets, no edits in NexusAI, never merge anything anywhere the fleet can see (merges are Tuesday's GO and the lane-4 seat's hands). Nothing to Partner Center, the demo or production. No Azure (no az at all), no public host, no registry. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 13 of the brief exactly. QUEUE, NEVER TAKE OVER: NexusAI builder seats and other gates share session-tools/nexusai-lock.sh with you. Every jest run — including jest --listTests — every browser run and every server you boot goes through it with a tag starting qa-b6- (C-110; C-141 gate-class, and its ADDENDUM 2, 3 and 4: each new qa ticket earns a fresh, self-applied yield; use --after only to sit directly behind a queued merge ticket or your own previous ticket, never to jump anyone), the lock held once per multi-run measurement as a tracked child of your seat. No docker is needed; never take the docker lock. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying foreign in the same run, and count your own Chrome processes; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every server boot, page load, key press, browser close, jest run, spec run and verify has a per-step DEADLINE, every server and browser is stopped in a finally by pid, a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

THE OTHER GATES. The batch-3 gate (lane 2) and the batch-4 gate (lane 3) were live at drafting and a batch-5a gate may start; they share the jest lock. You never touch their worktrees, trees, clones, processes, lock tickets or reports. Between gates the queue is plain FIFO: never jump, interrupt, move or signal one of their tickets; wait while they hold (C-141 does not cover gate tickets among themselves). Their servers count as FOREIGN in your counter — record them. If their merges move main, apply the main-is-moving rule.

RE-PIN at start, mid and end: all six branches and main (and any included optional member) — three timestamped readings with the branch name beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. The lane-4 seat is working other tickets now: if a branch moves, your verdict still names the pinned sha and you say so.

QUESTIONS: your routing name is QA/NexusAI-batch6. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch6] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch6/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject given on the VERDICT SUBJECT line at the end of this prompt, exactly. Lead the body with ONE line per ticket in the form "RD-<n>: <GO|GO WITH FINDINGS|NO GO> @ <short sha> — <one sentence>", then one line naming M0, the merged counts and the R11 result. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, the throwaway secret, a canary or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section, every declared limit L-A1 to L-A3, L-B1 to L-B5, L-C1 to L-C4, L-D1 to L-D3, L-E1 to L-E2 and L-F1 to L-F2 discharged with a measurement or left standing and named (C-112), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. Prior work: every C-49 question in the brief answered. That section must carry this line verbatim:
Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, browsers other than the installed Google Chrome, viewports other than those the gate names, Azure Container Apps and the demo, a real Entra SCIM client, the release pipeline's own image build and any registry, and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$F_HEAD"; do
  [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$S' is not a full 40-hex sha" >&2; exit 9; }
done

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$MAIN_SHA" "$M_5F26" "$M_748C" "$M_1166" "$M_7C47" "$A_CELLS" "$A_HEAD" "$B_FWD" "$B_C219" "$B_HEAD" \
         "$C_FWD" "$C_A195" "$C_HEAD" "$D_FWD" "$D_3F91" "$D_9C74" "$D_HEAD" "$E_HEAD" "$F_FIX" "$F_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — every head contains main-at-drafting.
for PAIR in "RD-693 $A_HEAD" "RD-286 $B_HEAD" "RD-204 $C_HEAD" "RD-197 $D_HEAD" "RD-686 $E_HEAD" "RD-692 $F_HEAD"; do
  N="${PAIR%% *}"; H="${PAIR#* }"
  [ "$(g merge-base "$MAIN_SHA" "$H" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: $N ${H:0:7} does not contain main 1904765" >&2; exit 7; }
done

# 8 — chains exact, parents exact (main..head).
chk_chain() { local head="$1" want="$2" label="$3" got
  got="$(g log --format='%H %P' "${MAIN_SHA}..${head}" 2>&1)"
  [ "$got" = "$want" ] || { echo "REFUSING: 1904765..$label is not the commissioned chain. Got:" >&2; printf '%s\n' "$got" >&2; exit 8; }; }
chk_chain "$A_HEAD" "$A_CHAIN" "RD-693 (4a86c4a, ddf1b75)"
chk_chain "$B_HEAD" "$B_CHAIN" "RD-286 (10 commits, forward merge a09dd83)"
chk_chain "$C_HEAD" "$C_CHAIN" "RD-204 (8 commits, forward merge 83e5a1b)"
chk_chain "$D_HEAD" "$D_CHAIN" "RD-197 (7 commits, forward merge cd589e0)"
chk_chain "$E_HEAD" "$E_CHAIN" "RD-686 (one commit)"
chk_chain "$F_HEAD" "$F_CHAIN" "RD-692 (078c8c0, 3dcd1c0, 4580829)"

# 18 — RE-PIN NOW by ls-remote: the six ticket branches exactly the pinned heads (REFUSE on mismatch).
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$D_BRANCH $D_HEAD" "$E_BRANCH $E_HEAD" "$F_BRANCH $F_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
# 18b — main: may move (batch-3/4/5a merges). It must be 1904765 or a descendant IN THE OBJECT STORE, and must not touch the six deltas.
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}')" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 1904765 — main was rewritten; re-brief" >&2; exit 18; }
ALLD="$( { printf '%s\n' "$A_EXPECTED_FILES" "$B_EXPECTED_FILES" "$C_EXPECTED_FILES" "$D_EXPECTED_FILES" "$E_EXPECTED_FILES" "$F_EXPECTED_FILES"; } | sed '/^$/d' | grep -vxF "$COUNTS_FILE" | sort -u)"
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$ALLD") <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 1904765..${M_ORIGIN:0:7} and touched a file of the six deltas: $HIT — the merged-tree premise changes; re-brief" >&2; exit 18; }
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 1904765, $(printf '%s\n' "$MOVED" | sed '/^$/d' | wc -l | tr -d ' ') paths, none in the six deltas) — the gate re-pins M0 itself; if RD-705 is on it, the brief's row b9 applies" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$MAIN_SHA" "$A_HEAD" "$A_EXPECTED_FILES" "RD-693 (1904765..ddf1b75)"
chk_delta "$MAIN_SHA" "$B_HEAD" "$B_EXPECTED_FILES" "RD-286 (1904765..1645c69)"
chk_delta "$MAIN_SHA" "$C_HEAD" "$C_EXPECTED_FILES" "RD-204 (1904765..fe47bb4)"
chk_delta "$MAIN_SHA" "$D_HEAD" "$D_EXPECTED_FILES" "RD-197 (1904765..43e729c)"
chk_delta "$MAIN_SHA" "$E_HEAD" "$E_EXPECTED_FILES" "RD-686 (1904765..8962a14)"
chk_delta "$MAIN_SHA" "$F_HEAD" "$F_EXPECTED_FILES" "RD-692 (1904765..4580829)"

# 75 — the counts-only tips are counts-only; each forward merge adds nothing beyond the ticket's own files.
for PAIR in "$C_FWD $C_HEAD RD-204" "$D_FWD $D_HEAD RD-197" "$F_FIX $F_HEAD RD-692"; do
  set -- $PAIR
  [ "$(g diff --name-only "$1" "$2" 2>/dev/null)" = "$COUNTS_FILE" ] || { echo "REFUSING: $3's tip ${2:0:7} over ${1:0:7} is not counts-only" >&2; exit 75; }
done
[ "$(g diff --name-only "$MAIN_SHA" "$A_CELLS" 2>/dev/null)" = "__tests__/rd693-token-cleared-on-leave.test.js" ] || { echo "REFUSING: RD-693's red-first commit 4a86c4a is not cells-only" >&2; exit 75; }
chk_fwd() { local fwd="$1" want="$2" label="$3" got
  got="$(g diff --name-only "$MAIN_SHA" "$fwd" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label's forward merge differs from main by more than the ticket's own files. Got:" >&2; printf '%s\n' "$got" >&2; exit 75; }; }
chk_fwd "$C_FWD" "$C_EXPECTED_FILES" "RD-204"
chk_fwd "$D_FWD" "$D_EXPECTED_FILES" "RD-197"
chk_fwd "$B_FWD" "tests/e2e/rd286-ground-and-geometry.spec.js" "RD-286"

# 23 — EXPECTED OVERLAPS: {A,C,D,F} pairwise = counts only; every pair with B or E = nothing.
DA="$(g diff --name-only "$MAIN_SHA" "$A_HEAD" 2>/dev/null | sort)"
DB="$(g diff --name-only "$MAIN_SHA" "$B_HEAD" 2>/dev/null | sort)"
DC="$(g diff --name-only "$MAIN_SHA" "$C_HEAD" 2>/dev/null | sort)"
DD="$(g diff --name-only "$MAIN_SHA" "$D_HEAD" 2>/dev/null | sort)"
DE="$(g diff --name-only "$MAIN_SHA" "$E_HEAD" 2>/dev/null | sort)"
DF="$(g diff --name-only "$MAIN_SHA" "$F_HEAD" 2>/dev/null | sort)"
for PAIR in A_B A_C A_D A_E A_F B_C B_D B_E B_F C_D C_E C_F D_E D_F E_F; do
  X="${PAIR%%_*}"; Y="${PAIR#*_}"; eval "SX=\"\$D$X\""; eval "SY=\"\$D$Y\""
  COMMON="$(comm -12 <(printf '%s\n' "$SX") <(printf '%s\n' "$SY") | tr '\n' ' ' | sed 's/ $//')"
  case "$PAIR" in
    A_C|A_D|A_F|C_D|C_F|D_F) WANT="$COUNTS_FILE" ;;
    *) WANT="" ;;
  esac
  [ "$COMMON" = "$WANT" ] || { echo "REFUSING: deltas $X and $Y share '${COMMON:-<nothing>}', expected '${WANT:-<nothing>}'" >&2; exit 23; }
done

# 35 — counts at every pinned sha.
for PAIR in "$MAIN_SHA 4133 247" "$A_CELLS 4133 247" "$A_HEAD 4137 248" "$B_FWD 4133 247" "$B_C219 4133 247" "$B_HEAD 4133 247" \
            "$C_A195 4037 242" "$C_FWD 1 1" "$C_HEAD 4148 248" "$D_3F91 4012 237" "$D_9C74 4037 242" "$D_FWD 1 1" "$D_HEAD 4142 248" \
            "$E_HEAD 4133 247" "$F_FIX 4133 247" "$F_HEAD 4138 248"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree), main-now included.
for S in "$MAIN_SHA" "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$F_HEAD"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 81 — THE PALETTE IS UNTOUCHED (Kam's call; RD-197 option (a) stays his): tokens.css and derive-brand-tokens.js identical to main at every head.
TOK_MAIN="$(blob "$MAIN_SHA" static/css/tokens.css)"; DER_MAIN="$(blob "$MAIN_SHA" scripts/derive-brand-tokens.js)"
[ "${TOK_MAIN:0:7}" = "$TOKENS_BLOB_SHORT" ] && [ "${DER_MAIN:0:7}" = "$DERIVE_BLOB_SHORT" ] || { echo "REFUSING: main's tokens.css/derive-brand-tokens.js are not ${TOKENS_BLOB_SHORT}/${DERIVE_BLOB_SHORT} — re-brief" >&2; exit 81; }
for S in "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$F_HEAD"; do
  [ "$(blob "$S" static/css/tokens.css)" = "$TOK_MAIN" ] && [ "$(blob "$S" scripts/derive-brand-tokens.js)" = "$DER_MAIN" ] || {
    echo "REFUSING: the palette (tokens.css or derive-brand-tokens.js) differs from main at ${S:0:7} — a palette change is Kam's; re-brief" >&2; exit 81; }
done

# 83 — RD-693's product hunk is ADDITIONS ONLY (no existing token clear is touched).
NS="$(g diff --numstat "$MAIN_SHA" "$A_HEAD" -- "$UI" 2>/dev/null | awk '{print $1" "$2}')"
[ "$NS" = "32 0" ] || { echo "REFUSING: RD-693's change to $UI is not +32/-0 (got '${NS:-nothing}')" >&2; exit 83; }

# 84 — RD-286: comment-stripped dark-mode.css differs from main by EXACTLY the two deleted background-color declarations (C-172).
D84="$(python3 - "$REPO" "$MAIN_SHA" "$B_HEAD" "$DARK" <<'PY'
import subprocess, re, sys, difflib
repo, a, b, p = sys.argv[1:5]
def blob(s):
    return subprocess.run(['git', '--no-optional-locks', '-C', repo, 'show', s + ':' + p], capture_output=True, text=True).stdout
def strip(t):
    t = re.sub(r'/\*[\s\S]*?\*/', '', t)
    return [l.strip() for l in t.split('\n') if l.strip()]
d = [x for x in difflib.ndiff(strip(blob(a)), strip(blob(b))) if x[:2] in ('- ', '+ ')]
print('|'.join(sorted(d)))
PY
)"
[ "$D84" = "- background-color: #1c1c1c;|- background-color: #262626;" ] || { echo "REFUSING: RD-286's declaration delta is not exactly the two C-172 deletions (got '${D84:-nothing}')" >&2; exit 84; }

# 85 — OPTIONAL MEMBERS: launcher and brief agree; an included head is a pushed commit containing main with the expected delta.
chk_opt() { local key="$1" name="$2" head="$3" ready="$4" branch="$5" want="$6" L
  if [ -z "$head" ]; then
    grep -qF "### OPTIONAL $key — $name STATUS: EXCLUDED" "$BRIEF" || { echo "REFUSING: OPT_${key}_HEAD is empty but the brief does not read 'OPTIONAL $key — $name STATUS: EXCLUDED'" >&2; exit 85; }
    return 0
  fi
  [[ "$head" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: OPT_${key}_HEAD '$head' is not a full 40-hex sha" >&2; exit 85; }
  grep -qF "### OPTIONAL $key — $name STATUS: INCLUDED @ $head" "$BRIEF" || { echo "REFUSING: OPT_${key}_HEAD is set but the brief does not read 'OPTIONAL $key — $name STATUS: INCLUDED @ $head'" >&2; exit 85; }
  [ "$(g cat-file -t "$head" 2>&1)" = "commit" ] || { echo "REFUSING: optional $name head $head is not in the object store" >&2; exit 85; }
  [ "$(g merge-base "$MAIN_SHA" "$head" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: optional $name head does not contain main 1904765" >&2; exit 85; }
  L="$(g ls-remote origin "refs/heads/$branch" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${head}[[:space:]]refs/heads/${branch}\$" || { echo "REFUSING: optional $name: origin refs/heads/$branch is not $head (unpushed or moved)" >&2; exit 85; }
  [ "$(g diff --name-only "$MAIN_SHA" "$head" 2>/dev/null | sort)" = "$(sorted "$want")" ] || { echo "REFUSING: optional $name delta is not the brief's expected set" >&2; exit 85; }
  [ -n "$ready" ] && [ -s "$ready" ] && grep -qF "${head:0:7}" "$ready" || { echo "REFUSING: optional $name READY mail missing or does not name ${head:0:7}" >&2; exit 85; }
  grep -qF "$ready" "$BRIEF" || { echo "REFUSING: the brief does not name optional $name's READY path" >&2; exit 85; }
  [ "$(blob "$head" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: optional $name package-lock differs" >&2; exit 85; }
  [ "$(blob "$head" static/css/tokens.css)" = "$TOK_MAIN" ] || { echo "REFUSING: optional $name changes the palette" >&2; exit 85; }
}
chk_opt G RD-430 "$OPT_G_HEAD" "$OPT_G_READY" "$G_BRANCH" "$G_EXPECTED_FILES"
chk_opt H RD-694 "$OPT_H_HEAD" "$OPT_H_READY" "$H_BRANCH" "$H_EXPECTED_FILES"

# 31 — builder evidence, prior report, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$READY_D2" "$READY_E" "$READY_F" "$CLAR" "$PREV_B2" \
         "$EV_P/rd693-hold.log" "$EV_P/rd692-hold.log" "$EV_P/rd686-verify.log" "$EV_P/rd286-hold.log" "$EV_P/rd286-verify.log" \
         "$EV_P/rd204-hold.log" "$EV_P/rd204-t2b.log" "$EV_P/rd197-mverify.log" "$EV_P/yield-log.md" \
         "$EV_P4/rd197-proof.log" "$EV_P4/rd204/derive-families.js" "$EV_P4/rd204/bootstrap-5.3.0.min.css" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$PREV_FLOORLIB" "$B1_EV/qa-floorcount.py" "$B1_EV/qa-dispatch.sh" "$B1_EV/qa-holdlib.sh" "$B1_EV/qa-mutate.py" \
         "$B1_EV/qa-c57-id-superset.sh" "$B1_EV/qa-netbelt.sb" "$B1_EV/qa-ssprint.sh" "$B1_EV/qa-h1-scan.py" \
         "$B2_EV/qa-a-browser.js" "$B2_EV/qa-a-lib.js" "$B2_EV/qa-png.js" "$B2_EV/qa-netbelt-ctl.js" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
for PAIR in "$READY_A $A_HEAD" "$READY_B $B_HEAD" "$READY_C $C_HEAD" "$READY_D $D_HEAD" "$READY_E $E_HEAD" "$READY_F $F_HEAD"; do
  R="${PAIR% *}"; H="${PAIR##* }"
  grep -qF "${H:0:7}" "$R" || { echo "REFUSING: $(basename "$R") does not name ${H:0:7}" >&2; exit 31; }
done
grep -qF 'ignoreDefaultArgs' "$B2_EV/qa-a-browser.js" || { echo "REFUSING: the batch-2 browser instrument no longer carries the bfcache fix (ignoreDefaultArgs)" >&2; exit 31; }

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PREV_B2" "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$READY_D2" "$READY_E" "$READY_F"; do
  grep -qF "$P" "$BRIEF" || grep -qF "${P#$QA_DIR/}" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-693 is TIER 1' 'RD-286 is TIER 2' 'RD-204 is TIER 2' 'RD-197 is TIER 2' 'RD-686 is TIER 2' 'RD-692 is TIER 2' 'One verdict PER ticket'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-693 (TIER 1)' 'RD-286 (TIER 2)' 'RD-204 (TIER 2)' 'RD-197 (TIER 2)' 'RD-686 (TIER 2)' 'RD-692 (TIER 2)' 'SIX verdicts'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$F_HEAD" "$MAIN_SHA" "$A_CELLS" "$B_FWD" "$B_C219" "$C_FWD" "$D_FWD" "$F_FIX"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT_BASE" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject exactly" >&2; exit 15; }
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 19 — the words the prompt must carry (% is a space); and the brief's sections.
WORDS="RD-693 RD-286 RD-204 RD-197 RD-686 RD-692 RD-705 RD-430 RD-694 RD-428 A-F1 A-N5 C-F1 S-4 H-1 H-20 M0 MAIN%IS%MOVING COMPOSITION
POSITIVE%CONTROL%FIRST M-A1 M-A8 M-B1 M-B4 T1 T2b T3 C-103 M1 M2 E1 E8 a1 a14 p1 p10 c1 c11 d1 d7 U1 U9 R11 bfcache ignoreDefaultArgs
'commit' LANDING%CONTROL tab%switch visibilitychange first-run-setup qa-surface-up.sh REAL%base currentcolor OPTIONAL%MEMBERS EXCLUDED INCLUDED
git%clone%--shared REGENERATION 4166/251 4137/248 4133/247 4148/248 4142/248 4138/248 id-superset C-57 C-68 C-89 C-104 C-112 C-98
C-125 C-141 C-110 C-28 C-61 C-172 C-174 C-168 C-175 BRAND OFF-GUIDE tokens.css Kam's node%--check VOID EXCLUSIVE QUEUE,%NEVER%TAKE%OVER DEADLINE
HEARTBEAT 2%minutes 5%minutes SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED CI%NOT%RUN deploy-demo Prior%work FOREGROUND
batch-3 batch-4 FIFO qa-b6- finally"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## RULED BY KAM, NOT YET IN AN ARTEFACT' '^## PRIOR ROUND' '^### THE UNMEASURED INTERACTIONS' '^### The proposed MERGE ORDER' \
         '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 7. TARGET D' \
         '^## 8. TARGET E' '^## 9. TARGET F' '^## 10. OPTIONAL MEMBERS' '^## 11. THE MERGED TREE' '^## 11a. THE BROWSER LEGS' '^## 11b. THE BRAND LEG' \
         '^## 12. CI and DEPLOY' '^## 13. Floor discipline' '^## WRONG OR UNVERIFIED' '^## PROVENANCE'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A3 L-B1 L-B5 L-C1 L-C4 L-D1 L-D3 L-E1 L-E2 L-F1 L-F2; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
  case "$PROMPT" in *"$L"*) ;; *) echo "REFUSING: prompt lacks declared limit $L (C-112)" >&2; exit 19 ;; esac
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b6-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main is moving'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 76 — the brief carries the ONE safe SESSION_SECRET printer verbatim and names the forbidden idioms.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}' 'docker inspect'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done

# 77 — the heartbeat is a separate child, aborted if absent at 90 s, max gap reported.
for w in 'separate child' 'within 90 s' 'max gap'; do
  grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat rule fragment '$w' (H-4)" >&2; exit 77; }
done

# 78 — the token rule (H-19): print only first4…last4, mask screenshots, scan evidence.
for w in 'H-19' '<first4>…<last4>' 'mask it in every screenshot'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the token rule fragment '$w' (H-19)" >&2; exit 78; }
done

# 79 — quoted mutant tool with a negative control; insertion-aware landing rule (H-7, H-8).
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing rule fragment '$w' (H-7/H-8)" >&2; exit 79; }
done

# 80 — the browser-leg rules (H-18, section 11a) and C-174 (H-20).
for w in 'H-18' "ignoreDefaultArgs: ['--disable-back-forward-cache']" "waitUntil: 'commit'" 'non-127.0.0.1' 'H-20' 'pkill -f' 'Never run `scripts/qa-surface-up.sh`'; do
  grep -qF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the browser-leg rule fragment '$w' (section 11a / H-18 / H-20)" >&2; exit 80; }
done
[ -d "/Applications/Google Chrome.app" ] || echo "NOTE: no /Applications/Google Chrome.app on this machine — verify (C-61) and both browser legs will fail or be NOT RUN" >&2

# 82 — the other-gates rule in brief and prompt.
for w in 'batch-3' 'batch-4' 'plain FIFO' 'never touch' 'gate tickets among themselves'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the other-gates rule fragment '$w'" >&2; exit 82; }
done
case "$PROMPT" in *"THE OTHER GATES"*"batch-3"*"FIFO"*) ;; *) echo "REFUSING: prompt lacks the other-gates rule" >&2; exit 82 ;; esac

# 38 — negative-control seats named in the brief; advisory if one has exited or a pane's claude changed.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 13 before launch" >&2
done
if command -v tmux >/dev/null 2>&1; then
  for N in M N P; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check. LAST refusal, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 18b 22 75 23 35 70 81 83 84 85 31 39 10 17 11 12 13 14 15 20 19 24 53 71 76 77 78 79 80 82 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7}, $C_BRANCH == ${C_HEAD:0:7}, $D_BRANCH == ${D_HEAD:0:7}, $E_BRANCH == ${E_HEAD:0:7}, $F_BRANCH == ${F_HEAD:0:7} at $PIN_TS (18)"
  echo "  main ${M_ORIGIN:0:7} (1904765 or a descendant; moved paths touch none of the six deltas) (18b)"
  echo "  every head contains 1904765 (7); chains exact (8); deltas exact (22); tips/forward merges (75); overlaps counts-only among A,C,D,F (23); counts at sixteen shas (35)"
  echo "  package-lock ${LOCK_BLOB:0:7} everywhere (70); palette ${TOKENS_BLOB_SHORT}/${DERIVE_BLOB_SHORT} untouched (81); RD-693 additions only (83); RD-286 two deletions (84)"
  echo "  optional G=${OPT_G_HEAD:-EXCLUDED} H=${OPT_H_HEAD:-EXCLUDED} (85); evidence (31); H-1 (76); H-4 (77); H-19 (78); H-7/H-8 (79); browser (80); other gates (82)"
  echo "  subject: $SUBJECT"
  echo "  route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

OPT_PARA=''
[ -n "$OPT_G_HEAD" ] && OPT_PARA="$OPT_PARA
OPTIONAL MEMBER INCLUDED — RD-430 (G): branch $G_BRANCH at $OPT_G_HEAD, READY $OPT_G_READY. It is a target with its own verdict (RD-430: GO / GO WITH FINDINGS / NO GO); merge it into your clone after RD-197; the brief's section 10 G and U9 bind it."
[ -n "$OPT_H_HEAD" ] && OPT_PARA="$OPT_PARA
OPTIONAL MEMBER INCLUDED — RD-694 item 4 (H): branch $H_BRANCH at $OPT_H_HEAD, READY $OPT_H_READY. It is a target with its own verdict (RD-694: GO / GO WITH FINDINGS / NO GO); merge it into your clone after RD-686; the brief's section 10 H binds it."

PROMPT="$PROMPT
$OPT_PARA

VERDICT SUBJECT (use exactly): $SUBJECT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$D_BRANCH = $D_HEAD; refs/heads/$E_BRANCH = $E_HEAD; refs/heads/$F_BRANCH = $F_HEAD; refs/heads/main = $M_ORIGIN (a descendant of 1904765 whose movement touches none of the six deltas). These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
