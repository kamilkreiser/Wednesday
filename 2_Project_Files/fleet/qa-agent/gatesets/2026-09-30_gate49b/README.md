# Gateset 2026-09-30_gate49b — README for Wednesday

Written by the drafter, 2026-09-30 (all times from `date -u`). Every figure below comes from the kit's own output files, each named beside the figure. Final shape per Wednesday's re-scope (~07:40Z): **#1357 + #1359, merged by Seat D 1st on ONE GO, plus a separate NON-MERGE POST-MERGE AUDIT of #1358.**

## 0. What happened while drafting (facts, from the PULLS / commits API)
- 07:17:28Z / 07:17:44Z: PeterObeden merged #1351 and #1352 (merge commits; develop `377989cf3829` -> `3a0d9812262b`).
- **07:28:02Z: #1358 was merged by PeterObeden at 07:28:02Z as a merge commit, before any gate** (`a5ab2ca9aa11`, parents `3a0d9812262b` + `6cf5c3629cd6`). Measured: the 15 landed blobs == #1358's head (lockdelta L8); the merge's tree `c6a24bd71019` == the tree this kit had predicted for "#1358 alone".
- **07:38:55Z: PeterObeden opened #1360, "KS-1380: revert #1358 (15 lockfiles) at Peter's request"** (open, head `d0e99f181a4e` at 07:47Z). overlaps_1.out: it merges clean over develop and END and would leave **27 top-level @types copies disagreeing with packages/shared** — i.e. it would re-open KS-1380 and re-break the three images (a prediction, unbuilt).
- ~07:4xZ: PeterObeden merged #1353 (`d8b6c2a7a520`, first parent `a5ab2ca9aa11`). **develop is now `d8b6c2a7a520ad715417435cde235346c92f7acc` (tree `eeca25667bb9`), and still contains #1358.**
- **Base correction:** the re-scope named "develop 3a0d9812262b (tree c6a24bd71019)". That tree is `a5ab2ca9aa11`'s; `3a0d9812262b`'s tree is `00397fa4b449`. The kit pins the current develop `d8b6c2a7a520`, which contains #1358 (the audit needs that). **END is therefore `d485add27eabcbbcfa12242158d14cafd71bb01b`, not `21313c65b444`** (that END was over `a5ab2ca9aa11`; #1353 moved develop since). The prompt tells the gate to re-derive this first.

## 1. The PRs and the BLUF
| PR | author | ticket | tier | head | merge-base | files (+/-) | subject declared -> lands | per-step tree (merge order) |
|---|---|---|---|---|---|---|---|---|
| #1357 | Seat B 49th (ITEM 1a) | KS-1054 | T1 | `236f9dce38982c17bf5868f3a3ec17c08393d871` | `377989cf3829` | 2 (+31/-2) | 71 -> 79 | `fc3355d7d6ec68f410b8c3dd9bea0569ad767004` |
| #1359 | Seat B 49th (ITEM 1c) | KS-1054 | T1 | `acac1f5e28ea4c983891dc50d7ed4b08a34d7e39` | `377989cf3829` | 4 (+162/-2) | 81 -> 89 | `d485add27eabcbbcfa12242158d14cafd71bb01b` (= END) |
| audit #1358 | Seat D 1st | KS-1380 | T2 | `6cf5c3629cd6…` merged as `a5ab2ca9aa11` | — | 15 locks | no GO | — |

- **GO (the GO mail's SUBJECT):** `GO (Seat D 1st): merge 1357 1359 on gate49b` — Seat D 1st merges #1357 -> #1359. Pane `QA/Secuura-batch1357` (**not routed**, section 4). Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-30-batch1357-g49b/`. Verdict subject: `[QA -> Wednesday] GATE49B #1357 #1359 (Seat D1 merger; T1 KS-1054 broken python3 fails closed + T1 KS-1054 rc-1 wording) + POST-MERGE AUDIT #1358 (T2 KS-1380)`.
- **Kit: READY to launch once the routing line is added** — launcher `--check` rc 0 (launcher_check_1.out, launcher_check_2.out); dry run rc 0 (repin_dryrun_1.out: `BOTH INSTRUMENTS AGREE with the pin, 2 of 2`, census `0 touch a kit path …`; the only report is the missing routing line).
- **Controls:** normal rc 0 `155 controls, OK 155, MISMATCH 0`; `--invert` rc 1 `155 controls, OK 0, MISMATCH 155` — one unedited script (controls_sha.txt: the same sha256 before run 1, after run 1 and after run 2).
- **Pins** (pin_1.out rc 0): both PRs 9 behind develop, the move reaches NONE of their 6 paths; DISJOINT (1 pair, 0 shared paths; they share two directories, not a path); END `d485add27eab` (`6 files changed, 193 insertions(+), 4 deletions(-)`) in both orders; modes 8 of 8 (three scripts 100755, three suites 100644, controls `.githooks/pre-push` 100755 / `preflight.sh` 100644); #1359 == the two goldens byte-for-byte (8 of 8, at the golden base AND at develop); #1357's blobs == the READY's `a46419eb4163` / `ac3ed60625d0`.
- keyscan_1.out `KEYSCAN PASS: 12 checks over 2 PR(s), 0 FAIL, 0 FLAG`. claims_1.out: Kam's ruling (a) VERBATIM in #1357's body; 56 drafted sentences over all FIVE drafts (drafts_gate49b.md). capture_1.out `CAPTURE OK`: 49 mails, exactly one READY each for #1357 / #1359 / #1358, each naming its head in full and its base.
- **Audit prediction** (lockdelta_1.out, the post-merge instrument: head = the merge commit, base = its first parent) `LOCKDELTA PASS: 0 FAIL of 28 checks`: 27 moves (1 PROD: root `@types/pg`), ADDED/REMOVED 0, registry-true, ranges 49/49, L8 landed == head; agreement 15 of 27 disagree at the first parent, 0 at develop and END; 0 Dockerfiles copy the root lock.

## 2. What the gate must rule
1. CLEAN-MERGE, DISJOINT, END-TREE, ORDER-INDEPENDENT, MODES, EXEC-BITS, COLLISION-CENSUS (per-step trees recorded for the merger).
2. **#1357 (T1), BEHAVIOUR FIRST**: the predicate executed on every python3 / body case at develop and head; RED-FIRST on macOS + `python:3.12-slim` (P10/P10b); CALLERS-READ; RULING-VERBATIM.
3. **#1359 (T1), BEHAVIOUR FIRST**: each caller's line and counter on rc 0/1/2; GOLDENS-BYTE-EQUAL; RED-FIRST (M1/N1; M2/M3/N2/N3 green both sides); NO-COUNTER-CHANGE; MESSAGE-TRUE.
4. **POST-MERGE AUDIT of #1358 — a separate, non-merge section, no GO**, opening with the statement verbatim: images analytics / billing / governance BUILD at develop (`-p g49bprobe-dev`, kyc the previously-green control; the merge's first parent FAILS as the discriminating control, `-p g49bprobe-pre`), landed == head, ranges, registry, lock agreement green, legs 6/7/contract rc 0, the four suites (packages/shared built first; `vitest run`), tsc NOT a red-proof, the census incl. #1360 and #649.
5. SHELL-RUNNER (63 incl. the two new suites), SHARED-BUILT-FIRST (the leg-14 trap, in the prompt for every suite run).
6. Subjects / bodies / commits (KS-1054 only). 7. All FIVE drafted comments line by line (#1358's three against develop, where #1358 now is): post as-is / amended / do not post; NO-REPEAT-49AFF833. 8. Follow-ons, fuse, ITEM 2 out of scope; TIERING; DISK-ENOSPC; REPORT-HASH-LAST; the `## MERGE ADDENDUM` LAST, ONE line with each PR's head, declared subject and per-step tree.

**The four pre-gate findings, in the prompt:** #1359's body `deploy.sh` / `deploy-all.sh` "+2/−2" vs numstat +3/−1 each (and `-` vs `—`); #1359's KS-1054 draft cites `deploy.sh:857` / `deploy-all.sh:312` — the messages are at :859 / :314 at the head; Kam's card cites `deploy-all.sh:281` as a /health check — at develop it is `local actual="$3"`; dependabot #649 (pg + @types/pg) conflicts on the root lock. Also named: #1360 (the open revert of #1358).

## 3. Pins and what the gate owes
- Prompt `2026-09-30_secuura-batch1357.prompt.txt` (38850 bytes, sha256 `181f05483a4d…`), **44 by-name keywords** (fill_gate49b.py `KW`), each checked as a TOKEN.
- Launcher `launch_qa_secuura_batch1357.sh` (14757 bytes, `698dd39f2443…`) refuses on: a keyword (33); a ticket statement (32); tiers / FROZEN at TWO / rounds (7); BEHAVIOUR-FIRST (34); authority (36); the leg-14 trap (37); the client-comment rule (38); **the POST-MERGE AUDIT section and its verbatim statement (40)**; the HOLDS + named exceptions (39); the GO string / merge seat / order (26); the addendum rules + REPORT-HASH-LAST (25); verdict subject / report dir (23); develop / END in full (31); kit files / placeholders / 2 rows (8); heads in capture + prompt (20); a moved head (6); the compare (10); develop moved (17); non-TTY (21); overrides (16); a moved kit (2).
- Named exceptions: X1 registry reads of `npm ci` / `npm audit`; X2 none (no lock is regenerated in this gate); X3 builds `-p g49bprobe-dev build analytics billing governance kyc` and `-p g49bprobe-pre build analytics billing governance`, build only, left in place; X4 npm-registry GETs; X5 read-only Linear (comment `49aff833` by id, newest comments of KS-1054 / KS-1395 / KS-1387 / KS-1380, attachments citing #1357 / #1359 / #1358) — the only real `.env` read, by key name.
- Capture `mail_gate49b_ready.md` (264885 bytes, `9b80526fb050…`). gate49a's report `ddbb07ecd9de…`, gate48b's `5ae77e86d1ea…` == kit.json (the fill refuses otherwise).
- `reported_overlaps` is EMPTY (no open PR touches the 6 kit paths or carries KS-1054). The 11 PRs on #1358's locks (#1360 + 10 dependabot) are the audit's census: reported, never refusing.
- **If #1360 merges before launch**, develop no longer carries #1358's locks: the launch action's re-pin refuses at lockdelta L6 (develop disagreeing) — rc 10, the premise changed; the audit section must then be re-ruled by Wednesday.

## 4. Routing line — NOT added
Back up the file first. Then add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (currently 160 lines, the last `QA/Secuura-batch1356|coagent@agentmail.to|yes`):
```
QA/Secuura-batch1357|coagent@agentmail.to|yes
```

## 5. Controls: `controls_gate49b.sh <scratchpad> [--invert]`
- **Final shape:** controls_1.out **rc 0: `155 controls, OK 155, MISMATCH 0 | ssh-denied retries 0`**; controls_2.out `--invert` **rc 1: `155 controls, OK 0, MISMATCH 155`**. The run before it (`superseded_controls_1_7_final_regex2.*`, 153/155) failed only on two stale regexes of the harness itself (PN0s expected 15 subset paths, R0c 10 expected overlaps); fixed before these runs. `launcher_check_2.out` rc 0 and `repin_dryrun_1.out` rc 0 were re-run AFTER the controls.
- **Coverage:** PN0-PN8 (pin: real heads, disjointness, reverse order, the subset, per-step tree, modes, goldens, claimed blobs; plants: a shared path -> (D), deploy.sh recorded 100644 -> MODE MISMATCH, a one-character edit -> golden DIFFERS, packages/shared's lock -> (K), check-startup-migrations.sh -> (L), a develop move on deploy.sh -> (C), an unrelated move -> PASS); LD0-LD5 (the audit instrument on plants of the MERGE COMMIT: an extra entry -> L2 + L8, kyc @types/pg back -> L3 + L6, a flag -> L2, a flipped integrity -> L5, the first parent as head -> L0); OV0 (+ CT-CLEAN / CT-CONFLICT on a #1359 path / CT-AGREE; #1360 and #649 rows); KS0-KS8; CL0-CL1; L0-L24 + LK1-LK44 (every launcher exit code incl. each keyword and the audit section's three phrases); R0-R8 (launch action: census, OVERLAP_EXTRA -> #649 refuses, #1360 title key -> refuses / sequenced / wrong head, DISJOINT, stale head, moved develop, bad scratchpad, routing); PNZ / KJZ / PRZ.
- **History, kept as `superseded_*`:** three earlier runs on earlier shapes (a harness regex slip; the 3-PR two-GO shape run 149/149 + inverted with a #1351 head race; the one-GO run stopped by the #1358 merge), and every instrument output from the 3-PR shape (`*_2_twoGO`, `*_3_devmoved`, `*_4_threePR`, `*_5_recordKey`, `*_6_dev1353`), the 3-PR templates and controls (`superseded_*_3shape*`), and `kit.json.pre-*` copies.

## 6. Could not measure (the drafter)
No suite, predicate run, image build, audit leg, install or served-file read: those are the seats' claims until the gate runs them. No Linear read (comment `49aff833` is known only from Wednesday's brief). #1360's effect is a git read (merge-tree + lock parse), unbuilt.

## 7. Files
kit.json · COMMISSION.TEMPLATE.md -> COMMISSION.md · pin_gate49b.py -> pin_1.out, pins_gate49b.json · gh_read_gate49b.py -> gh_read_1.out/.json, gh_body_{1357,1359,1358}.md · capture_mail_gate49b.py -> capture_1.out, mail_gate49b_ready.md · lockdelta_gate49b.py (post-merge audit) -> lockdelta_1.out · overlaps_gate49b.py -> overlaps_1.out, overlaps_gate49b.json · keyscan_gate49b.py -> keyscan_1.out · claims_gate49b.py -> claims_1.out, drafts_gate49b.md · prompt / launcher templates + fill_gate49b.py -> the prompt, the launcher, COMMISSION.md · repin_and_launch_gate49b.sh -> repin_dryrun_1.out · controls_gate49b.sh -> controls_1.out / controls_2.out, controls_sha.txt · final_lsremote_1.out.

## 8. Re-pin recipe (a NEW HEAD on #1357 or #1359)
The launch action refuses rc 11 on a moved head. 1. `cp kit.json kit.json.pinned-<old 12-hex>`. 2. `python3 -c "import json;p='kit.json';K=json.load(open(p));K['prs']['<n>']['head']='<new 40-hex>';json.dump(K,open(p,'w'),indent=1)"` (for #1357 also `claimed_blobs` from the new READY; #1359 must stay byte-equal to the goldens or pin (M) refuses). 3. Run `pin_gate49b.py <sp>` -> `gh_read_gate49b.py` -> `lockdelta_gate49b.py <sp>` -> `overlaps_gate49b.py <sp>` -> `keyscan_gate49b.py <sp>` -> `capture_mail_gate49b.py` (needs the seat's new READY naming the new head) -> `claims_gate49b.py <sp>` -> `fill_gate49b.py`, renaming each previous output `superseded_*`. 4. Update `L0n` / `PN0l` patterns in the controls, run both ways, `--check`, dry run. A develop move is re-pinned by the launch action itself (rc 10 if it reaches a kit path, or if develop stops carrying #1358's locks).

## 9. The ONE launch command (after the routing line in section 4)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-30_gate49b/repin_and_launch_gate49b.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-30_gate49b/launch_qa_secuura_batch1357.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/cab52cfa-6cf1-4ddd-807b-05202d63388e/scratchpad
```
