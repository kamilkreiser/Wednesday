# Gateset 2026-09-29_gate43 — README for Wednesday

Written 2026-09-29T08:03Z by the drafter (times from `date -u`). Every figure below is read from the kit's own output files, each named beside it.
The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory (text files only) and scratch under its session scratchpad `g43_sp/` (`clone` — `git clone --shared --no-checkout` of Wednesday's `screen0929/base` clone, fetched from origin ONLY there with the Secuura deploy key; the synthetic control commits, made by plumbing in that clone; the control plants under `controls_<HHMMSS>/`). It did NOT write the routing line (§4).
The Secuura checkout was touched by read verbs only (`ls-remote` in the launcher, the repin and the final read). GitHub: REST GET only (gh_read_1.out / gh_read_1.json, gh_body_<n>.md; the launcher's compares; the repin's PULLS reads). AgentMail: ONE read-only listing of wednesday-agent@ (_mail_list_1.out) and seven by-id GETs (capture_mail_gate43.py); no seen-state touched, nothing sent. No npm install, suite, tsc or eslint was run by the drafter (§6).

**gate43 = FIVE PRs from Seat B 44th (wrapping); the MERGER is Seat B 45th. T1: #1341, #1342 (full weight). T2: #1343, #1344, #1345 (through-code). Merge order: 1341, 1342, 1343, 1344, 1345 — each squash on the previous tip. All five merge cleanly AS-IS; none needs a rebase.**

| PR | tickets | tier | head (ls-remote pull/head == branch == API == fetched) | parent | behind develop | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1341 | KS-1375 (+ Refs KS-1368) | T1 | `bf0dfa64a424a3979d8efcb683ce18972a386b1c` | `2cb858335472` | 1 | 3 | 72 -> 80 |
| #1342 | KS-1369 | T1 | `add62ea8114627ef386d5399c4011e33e097e784` | `2cb858335472` | 1 | 2 | 80 -> 88 |
| #1343 | KS-1371 | T2 | `6600514d61efd90387cdeb9316635c3ae83a241b` | `2cb858335472` | 1 | 2 | 61 -> 69 |
| #1344 | KS-1359 | T2 | `ca4aab7f3b33eaafc7ef9dae8891e11c0e46816b` | `0aa9b52c691b` | 0 | 2 | 61 -> 69 |
| #1345 | KS-1360 | T2 | `052f4a3b9c56f78a5fa907a2db8e320105410a54` | `0aa9b52c691b` | 0 | 2 | 62 -> 70 |

Pane `QA/Secuura-batch1341` (**NOT routed by the drafter** — §4). GO string, as the GO mail's SUBJECT: `GO (Seat B 45th): merge 1341 1342 1343 1344 1345 on gate43`. Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-29-batch1341-g43/`. Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE43 batch #1341-#1345 (Seat B44 -> B45, round 43; T1: KS-1375 fail closed + KS-1369 proxy crash guard; T2: KS-1371, KS-1359, KS-1360)`.

## 1. BLUF
- **Kit: READY to launch once the routing line is added (§4).** Launcher `--check` rc 0 (launcher_check_1.out: `all guards pass:` — 5 of 5 heads at branch AND pull/head, 5 of 5 GitHub compares == the pins, 29 by-name keywords). Repin `--dry-run` rc 0 (repin_dryrun_1.out: `DRY RUN COMPLETE 2026-09-29T08:02:56Z`; `BOTH INSTRUMENTS AGREE with the pin, 5 of 5`; census `20 other open PR(s) read | 0 touch a kit path or carry a kit key`; the routing line reported absent — the only thing the real run would refuse on).
- **Pins** (pin_1.out, rc 0, ls-remote at 2026-09-29T07:33:47Z): develop `0aa9b52c691bb852e3fd1b796514fe9122ebc054` (tree `09c593f29fd4…`) == the commission's. Every head == its branch == the PULLS API head (gh_read_1.out) == the fetched ref.
- **The develop move under #1341-#1343** (pin (C), measured on `2cb858335472..0aa9b52c691b`): 1 path, `Blockchain/Dev/scripts/audit/audit-baseline.json` (#1340); it reaches NONE of their paths. So "main moved" but not "in a way that reaches my cells": **no rebase needed**; the GitHub compare for each still reads ahead 1 / behind 1 and GitHub reports `mergeable: True` (state `unstable`, CI does not start on this account) for all five.
- **Overlap — MEASURED, and the author's figure corrected** (pin (D)): `10 pair(s) checked, 0 overlapping | 11 path(s) in total, 11 distinct`. The author's "15" (Seat B 44th's STATUS for #1341: "#1339 and the six share ZERO files; control 30 vs 15") counts SIX branches; the sixth (KS-1054, `-b43-6`) is NOT at origin (ls-remote of `*b43-*`/`*b44-*`/`*b45-*` shows five plus #1339's and #1340's), so its 4 paths are a claim by subtraction. Zero overlap among the five is true on the tree measured (develop `0aa9b52c691b`).
- **END_TREE `dd70cc631be4f2f9d8ac6c8744acf109931e4ee1`** (pin (F)/(G)): every one of the five merges ALONE onto develop cleanly (E); the chain 1341 -> 1342 -> 1343 -> 1344 -> 1345, each a squash (`merge-tree` + `commit-tree -p <tip>`) on the previous tip, is clean at every step with diff(tip, new) == that PR's own paths and every blob+mode == its head's; diff(develop, END) == the union of the 11 paths, every END blob == its head blob; `11 files changed, 464 insertions(+), 12 deletions(-)`. The REVERSE order reaches the same tree (`dd70cc631be4…`, == END_TREE: True).
- **Controls, both ways** (controls_gate43.sh, one unedited script, sha256 `c354f7499462…` before the first run and after the second, controls_sha.txt):
  - normal (controls_1.out, rc 0): `SUMMARY gate43: 50 controls, OK 50, MISMATCH 0`
  - `--invert` (controls_2.out, rc 1): `SUMMARY gate43: 50 controls, OK 0, MISMATCH 50` (every control can fail).
- **Test census** (testrefs_1.out, rc 0, `git grep -l` at END `dd70cc631be4`): **23 test files** reference a changed product file by PATH or same-service IMPORT (list in the prompt and COMMISSION.md). Two sit OUTSIDE the changed services: packages/shared `ks781-p3-3-body-parser-order.test.ts` (reads `services/wallet-connector/src/server.ts`, #1345's file, as source — line 1925) and packages/shared `scopes.test.ts` (a comment naming #1342's proxy.ts). Controls inside: CT-POS (each PR's own test found), CT-NEG (a nonsense path finds 0), CT-TREE (4 of the batch's new test files absent at develop).
- **Key scan** (keyscan_1.out, rc 0): `KEYSCAN PASS: 31 checks over 5 PRs, 0 FAIL, 0 FLAG line(s)`. Every PR title == its declared subject; subject keys == the primary key only; no `(#n)`; landed 80 / 88 / 69 / 69 / 70 (all <= 92); mandated bodies `Refs KS-1375` + `Refs KS-1368` · `Refs KS-1369` · `Refs KS-1371` · `Refs KS-1359` · `Refs KS-1360`; no foreign hyphenated key on any live surface (title, PR body, head commit message). #1342's head COMMIT subject ("…onProxyReq returns early…") differs from its PR title; the squash lands the TITLE.
- **Heads re-read at the end** — final_lsremote_1.out (2026-09-29T08:04:13Z): develop `0aa9b52c691b`, pull heads #1341 `bf0dfa64a424` / #1342 `add62ea81146` / #1343 `6600514d61ef` / #1344 `ca4aab7f3b33` / #1345 `052f4a3b9c56` — every pin still current: **True**.

## 2. Doubts and contradictions the drafter found (each READ or MEASURED as stated)
1. **15 vs 11 paths** (MEASURED, above). Not a defect of the five; the author's number is over a sixth, unpushed branch.
2. **#1341: `services/vc-issuer/src/services/revocationResolvers.ts` still documents the OLD contract at the head** (READ, `git show bf0dfa64a424:…`, lines 46-52: "`found: false` … the verifier then ABSTAINS rather than failing closed"); #1341 does not touch that file (`git diff --quiet 2cb858335472 bf0dfa64a424 -- <file>` rc 0). Its commit message says "The superseded ABSTAIN contract in the resolver's doc comment is rewritten" — true only of verifier.ts's doc. The prompt makes the gate rule it (STALE-DOC-RESOLVERS-1341).
3. **#1341: the ruling closes an id NO authority holds; the id-swap to ANOTHER LIVE credential's id is not named** (READ): `ks1352…test.ts` C2 builds `{ ...document, id: <other> }` and verified TRUE at the base, so the proof does not bind `id` on that path. A revoked credential resubmitted with a genuine unrevoked id gets `found: true, revoked: false`. The prompt makes the gate measure it on a stood-up vc-issuer (ID-SWAP-TO-LIVE-1341).
4. **#1342 skips the BODY re-stream too when headers are sent** (READ: the guard returns before every write in the hook, and the new H2 cell asserts "writes no body"). The failure mode to rule out is an upstream request that never ends; the prompt requires a real-socket probe with a 5 s time-box (HEADERSSENT-REAL-SOCKET-1342, UPSTREAM-NOT-HUNG-1342).
5. **Couplings across PRs** (READ): #1341 edits `ks1352-revoked-credential-fails-verify.test.ts`, which imports `../routes/status` — the file #1343 changes; #1342 and #1344 both change api-gateway. Path-disjoint is not behaviour-disjoint: only the suites at END prove each pair together (SUITES-AT-END).
6. **The consumers of verifier.ts** (READ, `git grep` at END): vc-issuer routes/credentials.ts, routes/presentations.ts, services/revocationResolvers.ts, and **services/prism/src/index.ts** — prism configures no storedRecordResolver, so it must be unchanged; the prompt adds prism's suite.
7. **#1343's refusal message is unpinned** (the seat's own A2, disclosed in its commit message and STATUS) — the gate rules whether it blocks a T2.
8. **Every push preflight read 12/15 legs, 3 skipped (legs 3, 4, 8)** (the PR bodies, READ). Quoted as a ratio by the seat; the gate says what those legs would have covered.
9. **GitHub `mergeable_state: unstable`** on all five (gh_read_1.out) — `mergeable: True`; CI jobs do not start on this account (the same as gate42 / gate42b).

## 3. Pins and what the gate owes
- The prompt `2026-09-29_secuura-batch1341.prompt.txt` (25012 bytes, sha256 `95a230253bac…`) carries Wednesday's requirements by 29 keywords (fill_gate43.py `KW`); the launcher refuses a prompt missing any (exit 33), the tickets (32), a tier line (7), the HOLDS (39), the GO (26), the addendum rules (25), the verdict subject / report dir (23), develop / END_TREE in full (31). `## MERGE ADDENDUM` must be ONE LINE at the end of the report.
- Requirements, by name: (1) red at base / green at head / a tamper that reds for the right reason, per PR, with named tampers; (2) whole suites of packages/shared, vc-issuer, api-gateway, wallet-connector (+ prism) at develop, each head and END, and tsc per tree; (3) every census test RUN; (4) subjects / bodies; (5) #1345 hang / timeout / open-handle grep, with a control that prints; (6) overlap, chain, END, rebase-or-not; T1 extras for #1341 and #1342.
- Launcher `launch_qa_secuura_batch1341.sh` (12082 bytes, sha256 `c36f2b027b6e…`); capture `mail_gate43_ready.md` (76896 bytes, sha256 `73cf28bdf5db…`: the five STATUS "branch N of 6 RAISED" mails — Seat B 44th sent no single READY for the batch — Wednesday's ANSWER to the fifth, and the LAUNCH BRIEF to Seat B 43rd); COMMISSION.md (filled).

## 4. Routing line — NOT added
Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (after line 149, `QA/Secuura-batch1340…`). Back up the file first:
```
QA/Secuura-batch1341|coagent@agentmail.to|yes
```
Until the line is present, the launch action's step 0 refuses with rc 1 (control R1 measures that refusal on an empty routing file; R8 shows the same run with the line present passes step 0 and stops at 3b). The dry run found no other refusal.

## 5. Controls: `controls_gate43.sh <scratchpad> [--invert]`
- PN0-PN5 + PNZ, pin_gate43.py: the real subject as a simulation (PASS, 0 overlapping pairs, END `dd70cc631be4…`); a head it was not given (refuses, names #1343); a PLANTED OVERLAP — a synthetic commit on #1344's head that appends to #1342's proxy.ts (the matrix PRINTS `OVERLAP #1342 x #1344` and the chain refuses on the blob) — the control that makes the zero-overlap line able to print; a planted CONFLICT on the exact line #1342 edits (`step #1344 NOT clean`); a develop move that reaches a PR's cells (`(C) #1343: the develop move touches its own path`); the reverse-order END; the real pins sha256-unchanged after all of it.
- TR0-TR3, testrefs_gate43.py: the real census (23 files, PASS); the same census at develop (PASS, and the new ks1369 test NOT listed); a census pointed at nothing (G43_TR_GLOB) must FAIL CT-POS; the cross-package ks781 file is listed.
- KS0-KS7, keyscan_gate43.py: `(#n)` suffix, a foreign key in a subject, over-length, a missing `Refs KS-1368`, `Closes`, a foreign `KS-5` in a body, and a FLAG that must print on a planted PR body (`KS-662`).
- L0-L15, the launcher: wrong head (6), moved develop (17), wrong compare paths (10), a foreign-seat GO (26), an unfilled token (8), a dropped keyword (33), a capture without #1345's head (20), a dropped HOLD (39), the real launch path non-TTY (21), develop not in full (31), a tier line (7), a ticket line (32), the addendum MG-1 rule (25), the verdict subject (23), a MOVED KIT (2).
- R0-R8, the launch action: dry run (0) and its census line; real run without the routing line (1); a kit-path overlap via G43_OVERLAP_EXTRA against the real open PRs (15, names #572…); a title-key overlap via G43_TITLE_KEY=KS-1297 (15, names #1253); the DISJOINT OUT-OF-KIT line made to print via G43_WIDEN_RX on the real dependabot PRs (0); a stale head pin (11); a moved develop (10); a bad scratchpad (9); a real run with a routed temp file stopping at 3b (0).
- Not controlled: the usage gate (5), `cockpit.sh add` (7), the override refusal (4) on a real launch, a `mergeable=False` refusal, and the REAL re-pin across a develop move (step 3b's pin -> testrefs -> fill path; the dry run's refusal rc 10 is controlled, the write path is not, because it rewrites the kit's own files).
- Side effects, kept: the R1 / R8 real runs write `launch_<HHMMSS>.*` step outputs into this kit (three runs: 0747/0748 the drafting run, 0752/0753 controls_1, 0758/0801 controls_2); TR1 writes `testrefs_gate43.0aa9b52c691b.json`; the PN simulations write `pins_gate43.SIM-{real,ovl,cfl,mov}.json`.

## 6. Could not measure
No suite, tsc, eslint, install or runtime probe was run by the drafter: every red / green / suite / tsc figure in the commit messages, PR bodies and STATUS mails is the seat's claim. Not measured: the tampers; the #1345 hang grep; the id-swap-to-live probe; the real-socket proxy probe; the e2e / playwright specs the SYMBOL census names (need a stood-up stack); the sixth branch's paths (not at origin). Linear was not read (no ticket state checked).

## 7. Files
- Config: kit.json · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md
- Pins: pin_gate43.py -> pin_1.out (+ .rc), pins_gate43.json (+ .SIM-*.json from controls) · final_lsremote_1.out
- Reads: gh_read_gate43.py -> gh_read_1.out, gh_read_1.json, gh_body_1341..1345.md · _mail_list_gate43.py -> _mail_list_1.out
- Checks: testrefs_gate43.py -> testrefs_1.out (+ .rc), testrefs_gate43.json · keyscan_gate43.py -> keyscan_1.out (+ .rc)
- Capture: capture_mail_gate43.py -> capture_1.out, mail_gate43_ready.md
- Prompt and launcher: prompt_gate43.TEMPLATE.txt, launcher_gate43.TEMPLATE.sh.txt, fill_gate43.py -> 2026-09-29_secuura-batch1341.prompt.txt + launch_qa_secuura_batch1341.sh (fill_1.out), launcher_check_1.out
- Launch: repin_and_launch_gate43.sh -> repin_dryrun_1.out (+ .rc) · launch_<HHMMSS>.* (written by controls R1 / R8)
- Controls: controls_gate43.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt

## 8. The ONE launch command (after the routing line, §4)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate43/repin_and_launch_gate43.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate43/launch_qa_secuura_batch1341.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/35f90900-da39-4310-a097-bf496fc89a5b/scratchpad
```
- For a dry run, append `--dry-run` (repin_dryrun_1.out is one, rc 0). Argument 2 may be ANY existing Claude session scratchpad (`/private/tmp/claude-501/*/scratchpad*`); if `g43_sp/clone` is absent there, pin_gate43.py rebuilds it on a re-pin.
- If develop moves, the launch re-pins in the same action (step 3b: pin -> testrefs -> fill). It refuses rc 10 if the move reaches any PR's own paths or any chain step is unclean. A moved head refuses rc 11. Any other open PR touching one of the 11 paths or titled with a kit key refuses rc 15; a seat-branch PR (e.g. KS-1054 raised by Seat B 45th) that is path-disjoint is printed DISJOINT OUT-OF-KIT and does not refuse.
- Final re-read of the heads: final_lsremote_1.out (2026-09-29T08:04:13Z): develop `0aa9b52c691b`, pull heads #1341 `bf0dfa64a424` / #1342 `add62ea81146` / #1343 `6600514d61ef` / #1344 `ca4aab7f3b33` / #1345 `052f4a3b9c56` — every pin still current: **True**.
