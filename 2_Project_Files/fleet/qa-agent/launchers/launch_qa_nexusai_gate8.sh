#!/bin/bash
# launch_qa_nexusai_gate8.sh — cross-project QA agent, ONE gate (gate 8, lane A, batched, 2026-09-23) on Datasec/NexusAI,
# SIX targets, each off a DIFFERENT ancestor of main (none off main):
#   A — RD-531 + RD-497 (TIER 1): rd-531-497-s80i @ d7d6e7e, off 982a84f; chain 5366193 0081b72 d37d4a4 d7d6e7e.
#   B — RD-616 + RD-617 round 2 (TIER 1, NARROW, ROUND 2 OF 2): rd-616-617-s80i @ cc9616b, off 982a84f;
#       chain cd6cd55 f0519fd(gate 5's NO-GO head) ed6f3fc cc9616b. Round 2 changes no product file.
#   C — RD-638 (TIER 2): rd-638-export-always-ends-s80i @ ad81ef7, off 4bc4868; chain a46d336 0ab8a05 ad81ef7.
#   D — RD-631 (TIER 2): export-dir-stores-declared-s80i @ 153e472, off 6a32426; chain 4b685d6 4ff2d45 153e472.
#   E — RD-438 (TIER 1): rd-438-dot-segment-gate-s80i @ 63bb818, off 982a84f; chain 662faca 7a1a9ba 1ae1dfd 63bb818.
#   F — RD-510 (TIER 1, ADDED BY AMENDMENT): rd-510-listen-before-warmup-s80i @ 3f96a40, off 695ca5a;
#       chain 1b9f175 5c1af17 7dd2171 3f96a40. Its round 3 is test-only; the BRANCH is not (server entry point +106/-60).
#   COUPLED: three heads (B C D) rewrite the data-export module and four (A C E F) rewrite the server entry point.
#
# AUTHORITY: six READY FOR QA mails from S80I (NexusAI-I), sent copies in session-tools/s80i/ — mail-27-ready531.bWCe9P,
# mail-34-ready616.6hrVHD, mail-39-ready638.2gEBtM, mail-44-ready631.Z8UY2Q, mail-48-ready438.IaxqEL, mail-51-ready510.DIUy3J.
# Scope C-54/C-129/C-136 (A), C-97/C-134/C-140 (B), C-139 (D), C-54:346 (E); cap C-62 (B ONLY). Merges: Tuesday's GO (C-127).
#
# PATTERN: launch_qa_nexusai_gate7r2_rd645_rd641.sh. CHANGES:
#   - six heads, all re-pinned by ls-remote WITH main (18); six chains + exact parents (8); six deltas (22); ten counts (35).
#   - exit 26: main is NOT an ancestor of any head, and each head's merge-base is the commissioned one (four different bases).
#   - exit 67: B's round 2 changes no product file (data-export and email-service blobs identical at f0519fd and cc9616b).
#   - exit 73: the coupling premise by BLOB — the data-export module differs across B/C/D and from main; the server entry
#     point differs across A/C/E/F and from main. Read-only: no merge-tree, no object is written anywhere.
#   - exit 74: the NAMED MERGE-ORDER FACT is carried CORRECTED in the brief (RD-638 is the collider, not the RD-631 x RD-617
#     pair), and the prompt carries it too.
#   - exit 75: F's round-3 premise — 7dd2171..3f96a40 is counts only, and all three of F's non-counts blobs are identical
#     at 7dd2171 and 3f96a40 (none of F's evidence is at the gated head).
#   - exit 70: package-lock blob identical at main, all four bases and all six heads.
#   - exit 76: the coordinator's rulings carried where they must be — SESSION_SECRET UNSET widened to all six, the corrected
#     merge-order fact, F's THREE REDS prediction, and RD-654's "NOT PROVEN" wording unasserted.
#   - exit 38: negative-control seats 8360 (%44 NexusAI-I), 3434 (%0 Tuesday), 51683 (%52), 17056 (%53) — gate 7 r2's Vision
#     seat 1613 has exited and is NOT used.
#   - exit 32: SELF-CHECK stamped by the coordinator — LAST guard. Placeholder comparands BUILT BY CONCATENATION.
#   - exit 24 carried: the prompt must not carry the literal server path (RD-591 c.37901).
#   - no docker leg anywhere in this gate (no target has one); nothing here touches the image store.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-gate8' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep), grep, ps. No writes.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate8.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..76 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

PH_SCTS='@SELFCHECK''_TS@'
PH_SCNOTE='@SELFCHECK''_NOTE@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_nexusai-gate8.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_nexusai-gate8.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
EVID_I="$NX/session-tools/s80i"
EVID_H="$NX/session-tools/s79h"
G7R1_DIR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645"
G7R1_FLOOR="$G7R1_DIR/evidence/qa-floorcount.py"
G7R1_FLOORLIB="$G7R1_DIR/evidence/qa-floorlib.sh"
G5_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/report.md"
G4_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/report.md"
G4_STALL="$QA_DIR/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/evidence/a3u-stall-evidence.txt"
G2_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-gate2-rd495-rd525-rd575/report.md"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-23-gate8/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"

MAIN_SHA='34f11f405fa4ffd301df1c1bf6559ee313c1797c'   # origin main at drafting — NOT any target's base
BASE_ABE='982a84f2d0c72596a2d389897439e1d8d3425068'   # A, B, E
BASE_C='4bc48686c022933543c85ab6d1e430b7062d6901'
BASE_D='6a32426a7aa7b847cd2ec0ab89f0ec3bdc2fe71e'
BASE_F='695ca5ac96994f1d1f16e9ad0a8c2d5f6f9b0538'

A_BRANCH='rd-531-497-s80i'
A_HEAD="${QA_A_HEAD_OVERRIDE:-d7d6e7eec9f62fbc75ad9971c8a14cb6be4826cb}"
A_CHAIN='d7d6e7eec9f62fbc75ad9971c8a14cb6be4826cb
d37d4a45e3a0946f39809e90d8676383cd48f191
0081b722732ea785f6ff630c8f2ac72f857379ca
536619301bff90f224223c78d7d8e91c2aa782f9'
A_PARENTS='536619301bff90f224223c78d7d8e91c2aa782f9 982a84f2d0c72596a2d389897439e1d8d3425068
0081b722732ea785f6ff630c8f2ac72f857379ca 536619301bff90f224223c78d7d8e91c2aa782f9
d37d4a45e3a0946f39809e90d8676383cd48f191 0081b722732ea785f6ff630c8f2ac72f857379ca
d7d6e7eec9f62fbc75ad9971c8a14cb6be4826cb d37d4a45e3a0946f39809e90d8676383cd48f191'

B_BRANCH='rd-616-617-s80i'
B_HEAD="${QA_B_HEAD_OVERRIDE:-cc9616b2b22aa5c65619f3c47d4742f2bf7664d6}"
B_R1='f0519fd2390c7d5f2103e72dddac3adc276df639'          # gate 5's gated head (NO-GO)
B_CHAIN='cc9616b2b22aa5c65619f3c47d4742f2bf7664d6
ed6f3fc1394ce29a2da8f26eb6c0724f9cb58163
f0519fd2390c7d5f2103e72dddac3adc276df639
cd6cd55735ceac4e931e0f3dea049279ed18bf63'
B_PARENTS='cd6cd55735ceac4e931e0f3dea049279ed18bf63 982a84f2d0c72596a2d389897439e1d8d3425068
f0519fd2390c7d5f2103e72dddac3adc276df639 cd6cd55735ceac4e931e0f3dea049279ed18bf63
ed6f3fc1394ce29a2da8f26eb6c0724f9cb58163 f0519fd2390c7d5f2103e72dddac3adc276df639
cc9616b2b22aa5c65619f3c47d4742f2bf7664d6 ed6f3fc1394ce29a2da8f26eb6c0724f9cb58163'

C_BRANCH='rd-638-export-always-ends-s80i'
C_HEAD="${QA_C_HEAD_OVERRIDE:-ad81ef735b68f6ef9c421759307581dc64a9ea56}"
C_CHAIN='ad81ef735b68f6ef9c421759307581dc64a9ea56
0ab8a05512771564ede54c7e980e7423779ecae2
a46d336edbba1b7a7713471b9eee414c9c8130b0'
C_PARENTS='a46d336edbba1b7a7713471b9eee414c9c8130b0 4bc48686c022933543c85ab6d1e430b7062d6901
0ab8a05512771564ede54c7e980e7423779ecae2 a46d336edbba1b7a7713471b9eee414c9c8130b0
ad81ef735b68f6ef9c421759307581dc64a9ea56 0ab8a05512771564ede54c7e980e7423779ecae2'

D_BRANCH='export-dir-stores-declared-s80i'
D_HEAD="${QA_D_HEAD_OVERRIDE:-153e4726c4a33801a53c6e0a8bdd0824f714777c}"
D_CHAIN='153e4726c4a33801a53c6e0a8bdd0824f714777c
4ff2d45eb8b689995d71221a49ba9f7418158541
4b685d6ad89d0be1d6a14ac96bd54a1ef6808dff'
D_PARENTS='4b685d6ad89d0be1d6a14ac96bd54a1ef6808dff 6a32426a7aa7b847cd2ec0ab89f0ec3bdc2fe71e
4ff2d45eb8b689995d71221a49ba9f7418158541 4b685d6ad89d0be1d6a14ac96bd54a1ef6808dff
153e4726c4a33801a53c6e0a8bdd0824f714777c 4ff2d45eb8b689995d71221a49ba9f7418158541'

E_BRANCH='rd-438-dot-segment-gate-s80i'
E_HEAD="${QA_E_HEAD_OVERRIDE:-63bb818f6f341e8e04745dd822d2d8ca9ad05a30}"
E_FIX='1ae1dfd2fa01b09883d40839f7b9a1970fe01320'          # the CTRL-RAW instrument fix
E_CHAIN='63bb818f6f341e8e04745dd822d2d8ca9ad05a30
1ae1dfd2fa01b09883d40839f7b9a1970fe01320
7a1a9ba53b1b84a1f1d458fe8f19177f209bfb56
662facac076cd5f89bc9b8c8c14af4e351fcbdc5'
E_PARENTS='662facac076cd5f89bc9b8c8c14af4e351fcbdc5 982a84f2d0c72596a2d389897439e1d8d3425068
7a1a9ba53b1b84a1f1d458fe8f19177f209bfb56 662facac076cd5f89bc9b8c8c14af4e351fcbdc5
1ae1dfd2fa01b09883d40839f7b9a1970fe01320 7a1a9ba53b1b84a1f1d458fe8f19177f209bfb56
63bb818f6f341e8e04745dd822d2d8ca9ad05a30 1ae1dfd2fa01b09883d40839f7b9a1970fe01320'

F_BRANCH='rd-510-listen-before-warmup-s80i'
F_HEAD="${QA_F_HEAD_OVERRIDE:-3f96a40559387c7fb29499f9ce0b322729f3c1bd}"
F_R3='7dd21717dbe32d0dc902bbec69636c926836eda4'           # round 3 — where the builder's proof hold actually ran
F_CHAIN='3f96a40559387c7fb29499f9ce0b322729f3c1bd
7dd21717dbe32d0dc902bbec69636c926836eda4
5c1af17551653709e1af1c35681e7cd4f4bcdca7
1b9f1754d5abd3f7cc777d678d3582c0df6aaf17'
F_PARENTS='1b9f1754d5abd3f7cc777d678d3582c0df6aaf17 695ca5ac96994f1d1f16e9ad0a8c2d5f6f9b0538
5c1af17551653709e1af1c35681e7cd4f4bcdca7 1b9f1754d5abd3f7cc777d678d3582c0df6aaf17
7dd21717dbe32d0dc902bbec69636c926836eda4 5c1af17551653709e1af1c35681e7cd4f4bcdca7
3f96a40559387c7fb29499f9ce0b322729f3c1bd 7dd21717dbe32d0dc902bbec69636c926836eda4'

COUNTS_FILE='scripts/verify-expected-counts.json'
SERVER_FILE='backend/server.js'
EXPORT_FILE='backend/dataExport.js'
MAIL_FILE='backend/services/emailService.js'
CUST_FILE='backend/customerDataFiles.js'

A_EXPECTED_FILES="__tests__/rd495-admin-routes-behind-the-gate.test.js
__tests__/rd497-admin-routes-below-the-gate.test.js
$SERVER_FILE
$COUNTS_FILE
static/admin.html
static/js/admin.js"
B_EXPECTED_FILES="__tests__/helpers/home-containment.js
__tests__/rd412-smtp-transport.test.js
__tests__/rd616-617-mail-secrets-at-rest-and-export-shapes.test.js
__tests__/rd624-home-per-file.test.js
$EXPORT_FILE
$MAIL_FILE
$COUNTS_FILE"
C_EXPECTED_FILES="__tests__/rd638-export-always-ends.test.js
$EXPORT_FILE
$SERVER_FILE
$COUNTS_FILE"
D_EXPECTED_FILES="__tests__/customer-data-lists-agree.test.js
__tests__/erasure-reaches-attachments.test.js
__tests__/rd631-export-directory-branch-declared-only.test.js
$CUST_FILE
$EXPORT_FILE
$COUNTS_FILE"
E_EXPECTED_FILES="__tests__/rd438-dot-segment-gate.test.js
$SERVER_FILE
$COUNTS_FILE"
F_EXPECTED_FILES="__tests__/rd510-listen-before-warmup.test.js
__tests__/rd523-aoai-redirect-refused.test.js
$SERVER_FILE
$COUNTS_FILE"

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
NEG_SEATS='8360 3434 51683 17056'   # NexusAI-I (%44), Tuesday (%0), %52, %53 at drafting 2026-09-23 08:00
MERGE_FACT='RD-638 is the collider'
NOTTESTED_LINE='Container legs: not run this gate — no target has one, and node:24-alpine is not in the local image store; a pull is HELD.'

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 8: RD-531+497 d7d6e7e · RD-616+617 cc9616b · RD-638 ad81ef7 · RD-631 153e472 · RD-438 63bb818 · RD-510 3f96a40'
SUBJECT_STEM='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 8:'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "$1:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
files_of() { g diff --name-only "$1^" "$1" 2>/dev/null | sort; }   # vs FIRST parent
blob() { g rev-parse "$1:$2" 2>/dev/null; }

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 6 — every pinned sha is a commit in the object store.
for S in $MAIN_SHA $BASE_ABE $BASE_C $BASE_D $BASE_F $A_CHAIN $B_CHAIN $C_CHAIN $D_CHAIN $E_CHAIN $F_CHAIN; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — each head's merge-base with main is the commissioned base, and the base is an ancestor of the head.
for TRIP in "A $A_HEAD $BASE_ABE" "B $B_HEAD $BASE_ABE" "C $C_HEAD $BASE_C" "D $D_HEAD $BASE_D" "E $E_HEAD $BASE_ABE" "F $F_HEAD $BASE_F"; do
  L="${TRIP%% *}"; R="${TRIP#* }"; H="${R%% *}"; B="${R#* }"
  g merge-base --is-ancestor "$B" "$H" 2>/dev/null || { echo "REFUSING: ${B:0:7} is not an ancestor of $L $H" >&2; exit 7; }
  [ "$(g merge-base "$MAIN_SHA" "$H" 2>/dev/null)" = "$B" ] || { echo "REFUSING: merge-base(main, $L) is not ${B:0:7}" >&2; exit 7; }
done

# 26 — main is NOT an ancestor of any head (the fact that governs the whole gate), and every base IS an ancestor of main.
for TRIP in "A $A_HEAD" "B $B_HEAD" "C $C_HEAD" "D $D_HEAD" "E $E_HEAD" "F $F_HEAD"; do
  L="${TRIP%% *}"; H="${TRIP#* }"
  if g merge-base --is-ancestor "$MAIN_SHA" "$H" 2>/dev/null; then
    echo "REFUSING: main ${MAIN_SHA:0:7} IS an ancestor of $L $H — the brief's stale-base premise is gone; re-brief" >&2; exit 26; fi
done
for B in $BASE_ABE $BASE_C $BASE_D $BASE_F; do
  g merge-base --is-ancestor "$B" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: base ${B:0:7} is not an ancestor of main" >&2; exit 26; }
done

# 8 — each chain exact; every parent list exact.
for TRIP in "A $BASE_ABE $A_HEAD" "B $BASE_ABE $B_HEAD" "C $BASE_C $C_HEAD" "D $BASE_D $D_HEAD" "E $BASE_ABE $E_HEAD" "F $BASE_F $F_HEAD"; do
  L="${TRIP%% *}"; R="${TRIP#* }"; B="${R%% *}"; H="${R#* }"
  eval "WANT=\"\$${L}_CHAIN\""
  GOTC="$(g log --format=%H "${B}..${H}" 2>&1)"
  [ "$GOTC" = "$WANT" ] || { echo "REFUSING: ${B:0:7}..$L is not exactly the commissioned chain. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }
done
while IFS= read -r LINE; do
  [ -z "$LINE" ] && continue
  c="${LINE%% *}"; p="${LINE#* }"
  GOT="$(g log -1 --format='%H %P' "$c" 2>/dev/null)"
  [ "$GOT" = "$c $p" ] || { echo "REFUSING: parents of $c are '${GOT#* }', not '$p'" >&2; exit 8; }
done <<< "$A_PARENTS
$B_PARENTS
$C_PARENTS
$D_PARENTS
$E_PARENTS
$F_PARENTS"

# 18 — RE-PIN: all six heads AND main at origin, by ls-remote, read NOW.
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$D_BRANCH $D_HEAD" "$E_BRANCH $E_HEAD" "$F_BRANCH $F_HEAD" "main $MAIN_SHA"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-brief" >&2; printf '%s\n' "$L" >&2; exit 18; }
done

# 22 — each delta is EXACTLY the commissioned file set.
for TRIP in "A $BASE_ABE $A_HEAD" "B $BASE_ABE $B_HEAD" "C $BASE_C $C_HEAD" "D $BASE_D $D_HEAD" "E $BASE_ABE $E_HEAD" "F $BASE_F $F_HEAD"; do
  L="${TRIP%% *}"; R="${TRIP#* }"; B="${R%% *}"; H="${R#* }"
  eval "WANT=\"\$${L}_EXPECTED_FILES\""
  GOT="$(g diff --name-only "$B" "$H" 2>/dev/null | sort)"
  [ "$GOT" = "$(sorted "$WANT")" ] || { echo "REFUSING: $L's delta over ${B:0:7} is not the commissioned file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done

# 35 — counts at main, at every base, and at every head. SIX DIFFERENT HEAD NUMBERS — never one number for the batch.
for PAIR in "$MAIN_SHA 3937 227" "$BASE_ABE 3860 219" "$BASE_C 3868 220" "$BASE_D 3868 220" "$BASE_F 3863 220" \
            "$A_HEAD 3870 220" "$B_R1 3871 220" "$B_HEAD 3872 221" "$C_HEAD 3870 221" "$D_HEAD 3872 221" \
            "$E_HEAD 3865 220" "$F_HEAD 3867 221"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 50 — every chain TIP is counts-only, and the named instrument commits are what the brief says.
for PAIR in "A $A_HEAD" "B $B_HEAD" "C $C_HEAD" "D $D_HEAD" "E $E_HEAD" "F $F_HEAD"; do
  L="${PAIR%% *}"; H="${PAIR#* }"
  [ "$(files_of "$H")" = "$COUNTS_FILE" ] || { echo "REFUSING: $L's head is not counts-only" >&2; exit 50; }
done
[ "$(files_of "$E_FIX")" = "__tests__/rd438-dot-segment-gate.test.js" ] || { echo "REFUSING: ${E_FIX:0:7} (the CTRL-RAW fix) changes more than the rd438 cell file" >&2; exit 50; }
[ "$(files_of "$F_R3")" = "__tests__/rd523-aoai-redirect-refused.test.js" ] || { echo "REFUSING: ${F_R3:0:7} (F round 3) changes more than the rd523 cell file" >&2; exit 50; }
[ "$(files_of 4ff2d45eb8b689995d71221a49ba9f7418158541)" = "__tests__/erasure-reaches-attachments.test.js" ] || {
  echo "REFUSING: 4ff2d45 (D's fixture fix) changes more than the erasure-reaches-attachments cell file" >&2; exit 50; }

# 67 — B's ROUND 2 changes no product file (the reason the narrow re-gate is narrow).
GOT="$(g diff --name-only "$B_R1" "$B_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "__tests__/helpers/home-containment.js
__tests__/rd616-617-mail-secrets-at-rest-and-export-shapes.test.js
__tests__/rd624-home-per-file.test.js
$COUNTS_FILE")" ] || { echo "REFUSING: f0519fd..B is not the three test files + counts. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 67; }
for P in "$EXPORT_FILE" "$MAIL_FILE"; do
  [ -n "$(blob "$B_R1" "$P")" ] && [ "$(blob "$B_R1" "$P")" = "$(blob "$B_HEAD" "$P")" ] || {
    echo "REFUSING: $P differs between f0519fd and B — round 2 is not product-free; re-brief" >&2; exit 67; }
done

# 70 — package-lock identical at main, every base and every head (one node_modules serves every tree).
for S in $MAIN_SHA $BASE_ABE $BASE_C $BASE_D $BASE_F $A_HEAD $B_HEAD $C_HEAD $D_HEAD $E_HEAD $F_HEAD; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 73 — THE COUPLING PREMISE, BY BLOB. Read-only: no merge-tree, no object written anywhere.
#   the data-export module: changed by B, C and D, each differently, and none equal to main's.
for PAIR in "B $B_HEAD" "C $C_HEAD" "D $D_HEAD"; do
  L="${PAIR%% *}"; H="${PAIR#* }"
  [ -n "$(blob "$H" "$EXPORT_FILE")" ] || { echo "REFUSING: the data-export module is unreadable at $L" >&2; exit 73; }
  [ "$(blob "$H" "$EXPORT_FILE")" != "$(blob "$MAIN_SHA" "$EXPORT_FILE")" ] || {
    echo "REFUSING: $L no longer changes the data-export module — section 8's premise is gone; re-brief" >&2; exit 73; }
done
[ "$(blob "$B_HEAD" "$EXPORT_FILE")" != "$(blob "$C_HEAD" "$EXPORT_FILE")" ] \
  && [ "$(blob "$C_HEAD" "$EXPORT_FILE")" != "$(blob "$D_HEAD" "$EXPORT_FILE")" ] \
  && [ "$(blob "$B_HEAD" "$EXPORT_FILE")" != "$(blob "$D_HEAD" "$EXPORT_FILE")" ] || {
  echo "REFUSING: two of B/C/D carry the SAME data-export blob — the three-way premise is false; re-brief" >&2; exit 73; }
#   the server entry point: changed by A, C, E and F, and NOT by B or D.
for PAIR in "A $A_HEAD" "C $C_HEAD" "E $E_HEAD" "F $F_HEAD"; do
  L="${PAIR%% *}"; H="${PAIR#* }"
  [ "$(blob "$H" "$SERVER_FILE")" != "$(blob "$MAIN_SHA" "$SERVER_FILE")" ] || {
    echo "REFUSING: $L no longer changes the server entry point — section 8's premise is gone; re-brief" >&2; exit 73; }
done
for PAIR in "B $B_HEAD $BASE_ABE" "D $D_HEAD $BASE_D"; do
  L="${PAIR%% *}"; R="${PAIR#* }"; H="${R%% *}"; B="${R#* }"
  [ "$(blob "$H" "$SERVER_FILE")" = "$(blob "$B" "$SERVER_FILE")" ] || {
    echo "REFUSING: $L touches the server entry point after all — re-brief section 8" >&2; exit 73; }
done
#   every head rewrites the counts file, from a base blob it shares with nobody else's head.
for PAIR in "A $A_HEAD" "B $B_HEAD" "C $C_HEAD" "D $D_HEAD" "E $E_HEAD" "F $F_HEAD"; do
  L="${PAIR%% *}"; H="${PAIR#* }"
  [ "$(blob "$H" "$COUNTS_FILE")" != "$(blob "$MAIN_SHA" "$COUNTS_FILE")" ] || {
    echo "REFUSING: $L's counts file equals main's — the C-57 premise is gone; re-brief" >&2; exit 73; }
done

# 74 — the NAMED MERGE-ORDER FACT is carried CORRECTED in both files (the commission's pairing was wrong at source).
grep -qF "$MERGE_FACT" "$BRIEF" || { echo "REFUSING: brief does not carry the corrected merge-order fact ('$MERGE_FACT')" >&2; exit 74; }
grep -qF "$MERGE_FACT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not carry the corrected merge-order fact" >&2; exit 74; }
grep -q 'NAMED MERGE-ORDER FACT' "$BRIEF" && grep -q 'NAMED MERGE-ORDER FACT' "$PROMPT_FILE" || {
  echo "REFUSING: both files must label it the NAMED MERGE-ORDER FACT" >&2; exit 74; }
grep -q 'AUTO-MERGES' "$PROMPT_FILE" || { echo "REFUSING: the prompt must say the RD-631 x RD-617 pair AUTO-MERGES" >&2; exit 74; }
grep -q '^## 8. THE MERGE ORDER' "$BRIEF" || { echo "REFUSING: brief lacks section 8 THE MERGE ORDER" >&2; exit 74; }

# 75 — F's round-3 premise: 7dd2171..3f96a40 is counts only, and none of F's evidence is at the gated head.
GOT="$(g diff --name-only "$F_R3" "$F_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$COUNTS_FILE" ] || { echo "REFUSING: 7dd2171..F is not the counts file only. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 75; }
for P in "$SERVER_FILE" '__tests__/rd510-listen-before-warmup.test.js' '__tests__/rd523-aoai-redirect-refused.test.js'; do
  [ -n "$(blob "$F_R3" "$P")" ] && [ "$(blob "$F_R3" "$P")" = "$(blob "$F_HEAD" "$P")" ] || {
    echo "REFUSING: $P differs between 7dd2171 and F — F's proof ran at 7dd2171, so the brief's identity claim must hold" >&2; exit 75; }
done
grep -q 'the BRANCH is not' "$BRIEF" || grep -q 'NOT test-only' "$BRIEF" || {
  echo "REFUSING: brief must say F's branch is NOT test-only even though its round 3 is" >&2; exit 75; }
grep -q 'ROUND 3 IS TEST-ONLY BUT THE BRANCH IS NOT' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say F's round 3 is test-only but the branch is not" >&2; exit 75; }

# 31 — builder evidence and prior-gate evidence on disk.
for f in "$EVID_I/mail-27-ready531.bWCe9P" "$EVID_I/mail-34-ready616.6hrVHD" "$EVID_I/mail-39-ready638.2gEBtM" \
         "$EVID_I/mail-44-ready631.Z8UY2Q" "$EVID_I/mail-48-ready438.IaxqEL" "$EVID_I/mail-51-ready510.DIUy3J" \
         "$EVID_I/mail-09-rd631void.4SOehQ" "$EVID_I/mail-29-rd438.NKukGM" "$EVID_I/mail-50-rd510r3.d4XdI2" \
         "$EVID_I/rd531-hold-s80i-run8.out" "$EVID_I/rd616r2-hold-s80i-run10.out" "$EVID_I/rd638-hold-s80i-run11.out" \
         "$EVID_I/rd631-hold-s80i-run12.out" "$EVID_I/rd438r2-hold-run4.out" "$EVID_I/rd510r3-hold-run1.out" \
         "$EVID_I/expect-rd438-r2.txt" "$EVID_I/expect-rd631-s80i.txt" "$EVID_I/expect-rd510-r3.txt" \
         "$EVID_I/rd438r2-verify.log" "$EVID_I/rd631-verify.log" "$EVID_I/rd510r3-verify.log" \
         "$EVID_H/expect-rd531-497.txt" "$EVID_H/expect-rd616-r2.txt" "$EVID_H/expect-rd638.txt" \
         "$NX/session-tools/c57-id-superset.sh" \
         "$G5_REPORT" "$G4_REPORT" "$G4_STALL" "$G2_REPORT"; do
  [ -s "$f" ] || { echo "REFUSING: evidence absent: $f" >&2; exit 31; }
done

# 39 — gate 7 round 1's floor instrument, which the brief prescribes, is on disk and named.
[ -s "$G7R1_FLOOR" ] && [ -s "$G7R1_FLOORLIB" ] || { echo "REFUSING: gate 7 round 1's floor instrument missing" >&2; exit 39; }
grep -qF "$G7R1_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G7R1_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 — all six tiers declared in BOTH files.
for T in 'RD-531 + RD-497 is TIER 1' 'RD-616 + RD-617 (round 2) is TIER 1' 'RD-638 is TIER 2' 'RD-631 is TIER 2' \
         'RD-438 is TIER 1' 'RD-510 is TIER 1'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'TARGET A — RD-531 + RD-497 (TIER 1' 'TARGET B — RD-616 + RD-617 (TIER 1' 'TARGET C — RD-638 (TIER 2' \
         'TARGET D — RD-631 (TIER 2' 'TARGET E — RD-438 (TIER 1' 'TARGET F — RD-510 (TIER 1'; do
  grep -qF "$T" "$PROMPT_FILE" || { echo "REFUSING: prompt does not declare '$T'" >&2; exit 12; }
done
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
grep -qF "$G5_REPORT" "$BRIEF" || { echo "REFUSING: brief must name gate 5's report (B's prior round)" >&2; exit 14; }
for S in $MAIN_SHA $BASE_ABE $BASE_C $BASE_D $BASE_F $A_HEAD $B_HEAD $C_HEAD $D_HEAD $E_HEAD $F_HEAD $B_R1 $E_FIX $F_R3; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF "$PH_SCTS" "$PROMPT_FILE" || grep -qF "$PH_SCNOTE" "$PROMPT_FILE"; then echo "REFUSING: the prompt carries a self-check placeholder" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" && grep -qF "$SUBJECT_STEM" "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; both files must carry the verdict subject, which must begin with '$SUBJECT_STEM'" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
grep -q 'QUESTION: <topic>' "$PROMPT_FILE" && grep -qi 'no inbox routing line' "$PROMPT_FILE" || { echo "REFUSING: prompt must carry the question route" >&2; exit 20; }

# 19 — the words the prompt must carry (% is a space).
WORDS="RD-531 RD-497 RD-616 RD-617 RD-638 RD-631 RD-438 RD-510 RD-654 RD-655 C-62 C-68 C-57 C-133 C-112 C-127 C-136 C-139
C-140 C-141 C-142 C-129 C-54 C-110 C-122 C-28 SESSION_SECRET%UNSET POSITIVE%CONTROL%FIRST CTRL-RAW CTRL-WARM M-guard M-anon
M-fixture M-m3 M-route M-638 M-497 T1%ONLY THREE%REDS,%NOT%ONE NO%PATH%FILTER merge-tree commit-tree GIT_OBJECT_DIRECTORY
id-superset CI%NOT%RUN NOT%TESTED QUEUE,%NEVER%TAKE%OVER node%--check VOID EXCLUSIVE qa-gate8- DEADLINE HEARTBEAT
2%minutes 5%minutes finally 3870/220 3872/221 3870/221 3865/220 3867/221 3937/3937 NOT%PROVEN"
for w in $WORDS; do
  w="${w//%/ }"
  grep -q -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, NOT YET IN AN ARTEFACT' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks section 2a LEGITIMATE SHAPES" >&2; exit 19; }
grep -q '^## 7a. TARGET F' "$BRIEF" || { echo "REFUSING: brief lacks section 7a (TARGET F, the amended sixth target)" >&2; exit 19; }
grep -q '^## WRONG AT SOURCE' "$BRIEF" || { echo "REFUSING: brief lacks the WRONG AT SOURCE section" >&2; exit 19; }
if grep -qi 'backend/server\.js\|backend/dataExport\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains a literal product file path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi

# 53 — DEADLINE / HEARTBEAT, both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'DEADLINE' "$FL" && grep -q 'HEARTBEAT' "$FL" && grep -q '2 minutes' "$FL" && grep -q '5 minutes' "$FL" && grep -q 'finally' "$FL" || {
    echo "REFUSING: $FL lacks the DEADLINE / HEARTBEAT rule" >&2; exit 53; }
done
# 59 / 60 / 61 — lock tag, parse-before-red, exclusive trees.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'qa-gate8-' "$FL" || { echo "REFUSING: $FL lacks the lock tag prefix qa-gate8-" >&2; exit 59; }
  grep -q 'node --check' "$FL" && grep -qi 'VOID' "$FL" || { echo "REFUSING: $FL lacks parse-before-red" >&2; exit 60; }
  grep -q 'EXCLUSIVE' "$FL" || { echo "REFUSING: $FL lacks tree exclusivity" >&2; exit 61; }
done
# 65 — the positive control, both files.
grep -q 'POSITIVE CONTROL FIRST' "$BRIEF" && grep -q 'POSITIVE CONTROL FIRST' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt must both require the positive control first" >&2; exit 65; }

# 71 — the NOT TESTED line, verbatim in both.
grep -qF "$NOTTESTED_LINE" "$BRIEF" && grep -qF "$NOTTESTED_LINE" "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt must both carry the NOT TESTED line verbatim" >&2; exit 71; }

# 76 — the coordinator's rulings carried where they must be.
grep -q 'EVERY JEST RUN OF THIS GATE RUNS WITH SESSION_SECRET UNSET' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must widen the SESSION_SECRET UNSET ruling to the whole gate" >&2; exit 76; }
grep -q 'true of all five, not only RD-631' "$BRIEF" || {
  echo "REFUSING: brief must record that the SESSION_SECRET ruling is widened past RD-631" >&2; exit 76; }
grep -q 'EXPECT THREE REDS, NOT ONE' "$BRIEF" && grep -q 'EXPECT THREE REDS, NOT ONE' "$PROMPT_FILE" || {
  echo "REFUSING: both files must carry F's THREE REDS prediction" >&2; exit 76; }
grep -q 'BROADER THAN SURGICAL' "$BRIEF" && grep -q 'BROADER THAN SURGICAL' "$PROMPT_FILE" || {
  echo "REFUSING: both files must say F's M-anon mutant is broader than surgical" >&2; exit 76; }
grep -q 'NOT PROVEN' "$BRIEF" && grep -q 'RD-654' "$BRIEF" && grep -q 'RD-655' "$BRIEF" || {
  echo "REFUSING: brief must carry RD-654 / RD-655 with the NOT PROVEN wording" >&2; exit 76; }
if grep -qi 'the orphaned call retries because\|the retry is caused by\|proven retry' "$BRIEF"; then
  echo "REFUSING: the brief asserts RD-654's mechanism — the ruling forbids it" >&2; exit 76; fi
grep -q 'C-62' "$BRIEF" && grep -q 'applies to TARGET B only' "$BRIEF" || {
  echo "REFUSING: brief must scope the C-62 cap to TARGET B only" >&2; exit 76; }
grep -q 'do not assume one number across the batch' "$BRIEF" || {
  echo "REFUSING: brief must carry the coordinator's per-target counts warning" >&2; exit 76; }

# 38 — the brief names ALL negative-control seats; advisory if one is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 10 before launch" >&2
done

M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not ${MAIN_SHA:0:7} — section 8's merge predictions name it: re-brief before launch" >&2

# 32 — the coordinator stamps the self-check. LAST.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (6 7 26 8 18 22 35 50 67 70 73 74 75 31 39 10 17 11 12 13 14 15 20 19 24 53 59 60 61 65 71 76 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  six heads at origin with main (18); six chains + parents exact (8); none based on main, every base an ancestor (26)"
  echo "  deltas (22); twelve counts incl. six different head numbers (35); tips counts-only + instrument commits (50)"
  echo "  B round 2 product-free (67); package-lock ${LOCK_BLOB:0:7} everywhere (70); coupling premise by blob (73)"
  echo "  corrected merge-order fact carried (74); F round-3 premise + branch-not-test-only (75); rulings carried (76)"
  echo "  evidence (31); gate 7 r1 floor instrument (39); report absent (17); NOT TESTED line (71); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
