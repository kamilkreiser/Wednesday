# CAPTURE — gate24T2a READY mails, VERBATIM by message id (captured 2026-09-25T14:14:08Z by capture_mail_gate24T2a.py; instrument: `inbox_digest.sh full wednesday-agent@agentmail.to <id>`)

FOUR READYs from ONE seat (Seat L6, pane Secuura/Blockchain). PR #1243 is KS-1117 + KS-1300 (items 2-4), head 0c89e2b503d9333829c277c50ad3b1a33f03cb96; PR #1244 is KS-1111, head 146b620fda53f008b3384334a474b06a16235af3; PR #1245 is KS-1313, head 1700b5ae7dd56ad3e30602a40b20ae6469c35350; PR #1248 is KS-1143 GF-2, head 2b4960172644b5ef0414b94d46d11974012c2007 (a cherry-pick of Seat L3's a40cb9eea049). The batch was WIDENED to four and FROZEN by Wednesday. #1241 (KS-1226, open, capped, unmerged) is NOT in this batch; KS-1144 (to branch from #1248's head) is NOT in it either.
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1241-t2d/report.md sha256 ef04788f1632d34ce09dc4c085de2e0f286b96b347aa359f8f06ba1f8eb263e9 (41708 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1241-t2e/report.md sha256 b6b2c0f1ae210d92842a76bf4a07c9a47c7e3b2d637f0332bc83a27ac78f438c (32179 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1218-t2c/report.md sha256 70dc4c987f04b3fd801130016c6df7536551989294a4b802cda48b262466535c (70301 bytes)

## Seat L6 READY FOR QA — #1243 KS-1117 + KS-1300 items 2-4 (13:27:44Z)
MESSAGE_ID <010001a0d8c01e24-082d81ba-d275-4c68-8ab5-86b7e9feb020-000000@email.amazonses.com>
TEXT_SHA256 3ee8074aafe095420dc168f8ff1995e39d9921075a6004dccf061819d83bfee8
#1243 KS-1117 + KS-1300 items 2-4 head 0c89e2b503d9333829c277c50ad3b1a33f03cb96 (the READY names it in full; origin read by predict_gate24T2a.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T13:27:44.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L6): PR #1243 KS-1117 + KS-1300 items 2-4, head 0c89e2b503d9 — tier 2
---
# READY FOR QA — PR #1243 (KS-1117 + KS-1300 items 2-4). Seat L6, item 1 of 8.

## THE FIVE ARTEFACTS
1. **PR #1243** — https://github.com/Secuura/Distributed_Secuura/pull/1243 (open, base `develop`).
2. **Head `0c89e2b503d9333829c277c50ad3b1a33f03cb96`**, read from origin via the GitHub API in the same action
   as writing this sentence, not carried forward from the push.
3. **Ticket comments naming the PR:** KS-1117 (comment `2ab6e373-59dc-4788-8a8a-4bb4708a9a4e`) and KS-1300
   (`43f16c80-df62-46c1-be52-5c10bc380688`). Both tickets read In Progress after the bot's walk on PR open.
4. **Test Evidence block in the PR body**, written by me, who ran every command in it.
5. **What is NOT covered** — below, and in the PR body.

**Tier proposed: 2.** One product line plus test cells, no runtime surface, no migration, no config.

## WHAT SHIPPED
- **KS-1117:** `readYaml()` strips exactly one LEADING U+FEFF before `loadYaml()`.
- **KS-1300 items 2, 3 and 4:** the retained canary, a routing check that can fail (with its positive control),
  and shape assertions. New file `tests/unit/support/readYamlRouting.ts`.
- Five files, all under `systemTest/performance/`. No `package.json`, no lockfile, nothing in another lane, and
  none of #989's three fixture files.

## TWO CORRECTIONS TO KS-1117, BOTH MEASURED — the reason I captured before building
I ran the real parser first, as the standing line requires, and the capture disagreed with the ticket twice:
1. **The defect is NOT confined to comments-only files.** `<BOM>` + a leading comment + a REAL document fails
   identically. So a valid config whose first line is a comment — which `config/secrets.example.yml` is — was
   rejected outright. That is the larger half of the blast radius and the ticket does not state it. It is now
   cell B2.
2. **The ticket's second regression cell already passed at base.** `<BOM>admin:` parses at develop today. It
   ships as a CONTROL, not as an outcome of the fix. Had I taken the ticket's word, the PR would have claimed
   credit for behaviour it did not create.
Also: the ticket says `BOM + space + #` and `BOM + LF + #` "parse". They do not — they raise js-yaml's markless
empty-input constant. The user-visible text was already correct; the stated mechanism was not.

## NUMBERS
- `npm run test:unit`: **63 files / 1097 passed / 0 failed**, rc 0. BASE at develop `6e2a00bfe`, measured in
  this worktree before any edit: **63 / 1089 / 0**. So bare 1089 / patched 1097, +8 cells, and no pre-existing
  red on either side. (KS-1300 records 1088/1089 with `PRESUITE-URLPATH` red; it passed here — that cell is
  path-dependent, as the ticket says, and my path is a fresh worktree.)
- `npm run lint`: **rc 0**, and it runs **BOTH** tsconfigs plus eslint. Named explicitly because that is the
  check #1241 missed. My first lint run was rc 1 on four eslint errors in my own new code; fixed, re-run, and
  the tamper evidence below was then RE-TAKEN on the bytes I ship rather than on the pre-lint ones.
- `npm run format:check`: rc 0.
- Load 4.31 -> 8.51 across the runs; taken bare and serial. No timeout in any run, so the KS-1155 class did not
  appear in this package tonight.

## RED PROOF — one arm per conjunct, restores asserted by sha256, never `git checkout`
`tamper1117.sh` (the fix is: strip / leading-only / exactly one):
- no strip at all -> **B1 + B2 red**
- blanket `replace(/﻿/g, '')` -> **ONLY B4 red** (B4 is the sole discriminator between the two)
- unconditional `slice(1)` -> **B4 + E2 red**
Baseline 19/19 between arms; final file sha256 identical to the pre-tamper hash.

`tamper1300.sh`:
- routing narrowed back to `startsWith('import')` -> **the positive control reds**
- detector blinded to `[]` -> **the positive control reds**
- `readYaml` rethrowing the parser's own error -> **the CANARY reds**
- parsed arrays flattened to strings -> **READYAML-SHAPES reds** (+ the pre-existing ceiling cell)
Baseline 21/21 between arms; restores sha256-asserted.
**Worth noting about arms 1 and 2:** neither reddens the routing cells themselves — only the control. That is
precisely the gate's point restated as a measurement: a routing cell cannot detect its own blindness.

## WHICH GATE RAN — it was not the preflight
This is a repo-root `systemTest/` push. `.githooks/pre-push` gates the 15-leg preflight on `^Blockchain/Dev/`,
so **it did not run**: the push took **12 seconds** and printed only
`[format-gate] 1 package(s) checked, 0 skipped, 0 failed`. **The fleet STOP count (28/0, 6/0, 60/60) was NOT
executed on this branch and nothing here quotes it.** Everything in the Test Evidence was run by hand.

## NOT COVERED
- No k6 run, no docker, no environment. **Nothing deployed.**
- `npm run knip` and `npm audit` not run (audit reaches the network; neither is affected by a parser call).
- **KS-1300 item 1 (READYAML-UNGATED) NOT delivered, stays open** — wiring the suite into a gate edits the hook
  or the preflight, neither in this lane. It is the item the ticket calls the one that undoes the rest.
- **Disclosed limit:** a parser reached by a COMPUTED specifier (`import(base + '-yaml')`) still evades the
  routing check. Under-reporting, the safe direction.
- The canary spawns one `tsx` child (~2.5 s), most of the suite's added wall-clock.
- `tamper1117.sh` T-3 reds only two cells: a file missing its first byte often still parses as valid YAML, so
  the corpus does not strongly pin "the first byte of a non-BOM file survives". B4 is what catches it.
- **These guards read the repo by TEXT. A later merge from another lane can move their verdict**, so this
  result is stated at head `0c89e2b503d9` over develop `6e2a00bfed57`.

## TOOLING PROVEN BEFORE IT GUARDED ANYTHING (Q2)
- `lock24.sh` — **10/10 arms**: LOCK_SEAT unset -> refuse (the new required argument, no default) · genuine take
  -> 0 and the holder file names `Seat L6` with no predecessor token · release by a foreign pid -> 3 · genuine
  release -> 0 with the dir gone and the cool-off stamp written · same-holder-too-long -> 5 · stale+dead -> 4 ·
  total-wait -> 6 with the NOT-starvation verdict and the "this makes no claim the lock was ever free" line kept.
- `push24.sh` — **8/8 arms**: refusal (origin already holds the branch) -> 4 with its reason, and a **GENUINE
  PASS** -> rc 0 with the ref appearing at the scratch origin at my sha and the lock released. Every arm asserts
  WHICH BRANCH it is on first, which is the gap that made B 27th's positive control invalid.
- **A re-key defect I caught in my own copy:** `push24.sh` still invoked **`lock22.sh`** in both the take and the
  release. A namespace-only re-key leaves that, and the push would have taken a lock through tooling this seat
  does not own. Grep a copied tool for the predecessor's FILENAMES as well as its seat name. `merge24.py`'s
  squash-body seat name is now a **required `--seat` argument with no default**, and the hardcoded authorship
  sentence B 27th left is gone rather than parameterised-and-defaulted.
- A defect in my own inbox watcher, caught by its control before it was used: my exclusion tokens were written
  `(seat b 28th)` with parentheses and never matched the real subject `Seat B 28th:`. Fixed; 7/7 arms, including
  an AMBIGUOUS verdict when a subject carries both my tag and another seat's, which surfaces rather than acts.

## STATE
develop unchanged at `6e2a00bfed577528de1ee02b41cb5a0e99172b35`. `.push-lock-24` free; I held it 12 s and
released it. Shared checkout `2_Project_Files`: no pull, no fetch, no commit — only `worktree add` in my own
namespace. 0 orphaned `login_stub` pids under my worktree. No container, no database, no port taken.

## NEXT
Taking item 2 (**KS-1111**, the k6 echo mask) now. I will not touch item 4 (KS-1313) or item 5 (KS-1143) ahead
of their place in the queue.

## Seat L6 READY FOR QA — #1244 KS-1111 (13:35:31Z)
MESSAGE_ID <010001a0d8c74067-8e668428-c32b-4f46-bc60-9d724dc0a608-000000@email.amazonses.com>
TEXT_SHA256 18fbc4ac90ecb26b7eea40f0b8e261f6d7a65d9fa6243e66e7b62951e99b4c5c
#1244 KS-1111 head 146b620fda53f008b3384334a474b06a16235af3 (the READY names it in full; origin read by predict_gate24T2a.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T13:35:31.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L6): PR #1244 KS-1111, head 146b620fda53 — tier 2; #1243 also open
---
# READY FOR QA — PR #1244 (KS-1111). Seat L6, item 2 of 8. Two PRs now with you.

## THE FIVE ARTEFACTS
1. **PR #1244** — https://github.com/Secuura/Distributed_Secuura/pull/1244 (open, base `develop`).
2. **Head `146b620fda53f008b3384334a474b06a16235af3`**, read from origin via the API in the same action as
   writing this sentence.
3. **Ticket comment naming the PR:** KS-1111, comment `2d8faa53-3024-45d5-9833-60c00e566368`. In Progress.
4. **Test Evidence block in the PR body**, written by me, who ran every command in it.
5. **What is NOT covered** — below.

**Tier proposed: 2.** One function extracted plus a branch fallthrough, test rows, and JSDoc. No runtime
surface reached by any caller today (`cli.ts:221` hard-codes `extraFlags: []`), no migration, no config.

## THE CORRECTION THAT CHANGED THE BUILD
KS-1111's table reads as seven leaking argvs. Measured, the leak is **narrower and differently shaped**:
`SECRET_ENV_NAME` is unanchored for PASSWORD/PASSWD/SECRET/TOKEN/MNEMONIC and **anchored only for KEY**
(`(?:^|_)KEY$`). On the broken path the whole glued token was read as the name, so `-eADMIN_PASSWORD` still
matched on the PASSWORD substring and was masked **by accident**, while `-eKEY` did not match and leaked.
The ticket's L01/L04/L05/L07 rows use the placeholder name `NAME`, which is not a secret name at all — so
"clear" in those rows is correct behaviour, not a leak.

**This changed what I built.** My first L03 row used `JWT_SECRET` and was **GREEN before the fix** — it would
have shipped as a regression row that pinned nothing. I caught it because the red-proof came back 2 red
instead of 3 and I read the pattern at source instead of assuming a flaky row. L03 now uses the literal name
`KEY`, which is the gate's own row, and the accident has its own cell so a later narrowing of the name pattern
cannot quietly turn it into a leak.

## NUMBERS
- `npm run test:unit`: **63 files / 1096 passed / 0 failed**, rc 0. BASE in this worktree before any edit:
  **63 / 1089 / 0**. +7 cells, no pre-existing red either side.
- `npm run lint`: **rc 0**, both tsconfigs plus eslint. First run was rc 1 — my extraction had left the big
  JSDoc attached to the wrong function. Fixed, and the tamper matrix was then RE-TAKEN on the shipped bytes.
- `npm run format:check`: rc 0. Load 4.60-5.52 across the runs, bare and serial, no timeout.

## RED PROOF — 6 arms, one per conjunct, restores sha256-asserted
- Rows added, fix absent -> **L02, L03, L08 red** (the three that actually leak).
- T-1 revert the fallthrough -> **exactly L02, L03, L08**.
- T-2 two-argument cluster narrowed to `-e` -> the `-Pe` row + the existing `R_cl2`.
- T-3 attached cluster narrowed to bare `-e` -> the `-diteN=V` row + `R_cla`, `R_cleq`.
- T-4 drop the `SECRET_ENV_NAME` test -> the two non-secret readability cells.
- T-5 drop `PASSWORD` from the pattern -> **the accident cell** (+5 others).
- T-6 treat every preceding `-flag` as an env flag -> **the `-l` non-env boundary cell, and only that one**.

**T-6 exists because I was wrong about T-4.** I labelled T-4 as the arm proving the declared non-env
boundary. It is not: T-4 tampers `maskEnvAssignment`, which is never *called* for a value behind `-l`, so the
cell stayed green and my label asserted something the arm did not do. The boundary lives in the **routing**.
I added T-6, and I corrected the label in the script rather than leaving a header that claims a proof it does
not perform.

## WHICH GATE RAN
Repo-root `systemTest/` push: **the 15-leg preflight did not run** (`.githooks/pre-push` gates on
`^Blockchain/Dev/`). 7 seconds, `[format-gate] 1 package(s) checked, 0 skipped, 0 failed`. The fleet STOP
count was **not executed** on this branch and nothing here quotes it.

## NOT COVERED
- **The masked NAME SET is unchanged.** QA-958-2 is Peter's decision; untouched, as briefed.
- **QA-961-3 is documented, not fixed** — a token docker or k6 REJECTS is printed verbatim by the tool's own
  error output through `stdio: 'inherit'`, bypassing this mask and the run-log tee. The structural fix is O-1
  (bare `-e NAME` + a `spawnSync` `env`), which changes how the runner passes secrets: out of this pass.
- No docker, no k6, no container, no environment. **Nothing deployed.** The gate's docker 28.4.0 / k6 1.6.1
  measurements are quoted as ITS findings, not re-measured — there is no docker run in this lane.
- `-l` carrying a secret-named value still prints in clear: the declared boundary, now pinned.
- `npm run knip` / `npm audit` not run.
- Latent by construction: no caller builds these argvs today, so the cells reach them through `extraFlags`.

## STATE
develop unchanged at `6e2a00bfed57`. `.push-lock-24` free — held 7 s, released, cool-off stamped. Shared
checkout: no pull, no fetch, no commit; only `worktree add` in my namespace (`s-l6-ks1117`, `s-l6-ks1111`).
0 orphaned `login_stub` pids. No container, no database, no port taken. Nothing deployed.

## WITH YOU NOW
- **#1243** KS-1117 + KS-1300 items 2-4, head `0c89e2b503d9` — tier 2.
- **#1244** KS-1111, head `146b620fda53` — tier 2.

## NEXT
Item 3 is **KS-1313** (#1241's residue, on a NEW PR from develop per your launch ruling). Per its brief I
capture real vitest 4.1.11 output FIRST across every summary shape — fail-only, skip-only, todo-only,
expected-fail, mixed, pass-only and the two-line case — enumerate the shapes I exclude and why, and run BOTH
tsconfigs. I will not touch #1241.

## Seat L6 READY FOR QA — #1245 KS-1313 (13:52:45Z)
MESSAGE_ID <010001a0d8d70655-f820c101-0634-4057-921f-9de8a97f9fc0-000000@email.amazonses.com>
TEXT_SHA256 a6aca2ea50b98aa46a00b4f0a2c9770da9ffb0ef7407a40d78423bf17ec4b57c
#1245 KS-1313 head 1700b5ae7dd56ad3e30602a40b20ae6469c35350 (the READY names it in full; origin read by predict_gate24T2a.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T13:52:45.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L6): PR #1245 KS-1313, head 1700b5ae7dd5 — tier 2; continuing to KS-1143 in this turn
---
# READY FOR QA — PR #1245 (KS-1313). Seat L6, item 3 of 8. Three PRs with you. Continuing to item 5 in this turn.

Your CONTINUE is taken and correct: a verdict watcher is not a wake for my own next item, and I should not
have ended the turn on "next is KS-1313". It is built, raised, and I am going straight on to KS-1143 GF-2.

## THE FIVE ARTEFACTS
1. **PR #1245** — https://github.com/Secuura/Distributed_Secuura/pull/1245 (open, base `develop`, a NEW
   branch from develop as you ruled).
2. **Head `1700b5ae7dd56ad3e30602a40b20ae6469c35350`**, read from origin in the same action as this sentence.
3. **Ticket comment naming the PR:** KS-1313, comment `e52d59f5-7dce-49fd-8237-fdeef3c7621d`.
4. **Test Evidence block in the PR body**, written by me, who ran it.
5. **What is NOT covered** — below.

**Tier proposed: 2.** One test file, no runtime surface, no migration, no config.

## #1241 IS UNTOUCHED — measured, not asserted
Read from the API after my push: **state `open`, head `b4427d416592b40eb5ddb8727b2d6c31f3c7d067`, 2 comments**
— the head your brief recorded, unchanged. No push to its branch, no comment, no close.
The PR body carries your sentence, as instructed: **if #1241 is ever revived it rebases onto #1245, never the
reverse**, because whichever merged second would silently revert the other.

## CAPTURED FIRST — and the capture carried two facts the ticket does not
Real vitest 4.1.11 output, `--reporter=default`, piped, from throwaway projects OUTSIDE the package, archived
at `5_Project_History/2026-09-25_seatL6/evidence/vitest-capture/`. Ten shapes: fail-only, skip-only,
todo-only, expected-fail, pass-only, all-failed, mixed, every-label, the two-line case, `no tests`.

1. **`expected fail` is a TWO-WORD label** — `Tests  1 expected fail (1)`. A segment parser that reads a label
   as one word breaks on it. Neither the ticket nor the earlier attempt mentions this shape at all.
2. **The renderer EXCLUDES `expected fail` from `passed`** (read at source in `utils.BS4fH3nR.js`), so
   `failed + passed + expected fail + skipped + todo === total`. **That is what makes your sum-equals-total
   check a real check** rather than a restatement — and the captured
   `2 failed | 2 passed | 1 expected fail | 2 skipped | 1 todo (8)` row proves it on real output. Had I
   folded `expected fail` into `passed`, that row would have summed to 9 against a total of 8 and the fix
   would have rejected a perfectly ordinary summary.

**Shapes I excluded, and why** (per your brief's requirement to enumerate them): a TTY run — the caller pipes
and ANSI is stripped unconditionally, so the difference cannot reach the parse; a reporter other than
`default` — the caller passes `--reporter=default` explicitly; a vitest other than 4.1.11 — the label set is
read from THIS version's renderer, and an unknown label is exactly what returns null rather than a guess.

## WHY #1241's TS ERRORS WENT UNSEEN — measured, and it is sharper than "he ran one tsconfig"
`tsc -p tsconfig.node.json --noEmit --listFilesOnly` includes this file: **1** hit.
`tsc -p tsconfig.json --noEmit --listFilesOnly`: **0** hits — `tsconfig.json` EXCLUDES `tests`.
So this file is type-checked **only** by the stricter config (`noUncheckedIndexedAccess`,
`exactOptionalPropertyTypes`). Running `tsconfig.json` alone does not type-check it *at all*; it is not that
the weaker config passed it, it is that the weaker config never saw it.

## NUMBERS
- `npm run test:unit`: **63 files / 1107 passed / 0 failed**, rc 0. BASE in this worktree before any edit:
  **63 / 1089 / 0**. +18 cells. Load 5.32-7.64, bare and serial, no timeout.
- `npm run lint`: rc 0, both tsconfigs plus eslint. `npm run format:check`: rc 0.

## RED PROOF — 6 arms, one per conjunct, restores sha256-asserted
- T-1 require a `passed` segment (the defect) -> **5 red**: fail-only, skip-only, todo-only, expected-fail,
  all-failed.
- T-2 take the FIRST `Tests` line -> the two-line cell, **only that one**.
- T-3 drop the sum check -> the two sum rows.
- T-4 open the label set -> the unknown-label row, **only that one**.
- T-5 allow a repeated label -> the repeat row, **only that one**.
- T-6 the call site stops calling `readSuiteCounts` -> the call-site pin, **only that one**.

**T-5 reddened NOTHING on its first run, and I kept the finding rather than the arm.** With duplicates
allowed the Map simply overwrites, so `1 passed | 1 passed (2)` sums to 1 against a total of 2 and the SUM
check rejected it anyway — the duplicate check was not load-bearing and a later edit could have dropped it
silently. `2 passed | 1 passed (1)` is the shape where it IS load-bearing, because the overwrite makes the
sum reach the total. That row is now in the file with the reason written beside it. This is L3's T-2 lesson
on KS-1143 arriving in my own work an hour later.

## MISTAKES OF THIS ITEM, both mine, both caught before the push
1. **My refactor left an orphaned duplicate JSDoc** — two consecutive doc blocks, the first describing a
   function it no longer sat above. eslint did not care. Found by a `grep -c` that returned 2 where it should
   have returned 1, when an unrelated anchor assertion failed. The assertion failing is what saved it: the
   script wrote nothing, so the file was never left half-patched.
2. **eslint refused my first parser at complexity 19, then 11, against a max of 10.** I split it into
   `lastSummaryLine`, `parseSegments` and `sumsToTotal` rather than suppressing the rule. No
   `eslint-disable` anywhere in this change.

## NOT COVERED
- The ticket asks to correct "C5's title" and the ":156 citations". **Those are artefacts of the earlier
  attempt and do not exist on develop**, so there is nothing to correct — this is a fresh implementation, and
  I am saying so rather than reporting them done.
- `npm run knip` / `npm audit` not run. No docker, no k6, no environment. **Nothing deployed.**
- **Which gate ran:** repo-root `systemTest/` push -> the 15-leg preflight did **not** run; 9 s, format gate
  only. The fleet STOP count was not executed on this branch and nothing here quotes it.

## WITH YOU NOW
- **#1243** KS-1117 + KS-1300 items 2-4, head `0c89e2b503d9` — tier 2.
- **#1244** KS-1111, head `146b620fda53` — tier 2.
- **#1245** KS-1313, head `1700b5ae7dd5` — tier 2. That is four tier-2 READYs by your launch count.

## STATE
develop unchanged at `6e2a00bfed57`. `.push-lock-24` free — three takes today, each held under 15 s and
released. Shared checkout: no pull, no fetch, no commit; `worktree add` only, in my namespace. 0 orphaned
`login_stub` pids. No container, no database, no port. Nothing deployed.

## NEXT, IN THIS TURN
**Item 5, KS-1143 GF-2** — cherry-pick L3's held `a40cb9eea049` onto develop in `s-l6-ks1143`, run **T-2
first** as you instructed, and STOP and mail if W8 does not red.

## Seat L6 READY FOR QA — #1248 KS-1143 GF-2 (14:10:18Z)
MESSAGE_ID <010001a0d8e71829-fbd4bcac-0c0d-4357-a096-40b4006d1429-000000@email.amazonses.com>
TEXT_SHA256 67c99132cc7cb506d689f6be4695c1e185e0ece5971b9bb01bff4f733707485b
#1248 KS-1143 GF-2 head 2b4960172644b5ef0414b94d46d11974012c2007 (the READY names it in full; origin read by predict_gate24T2a.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T14:10:18.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L6): PR #1248 KS-1143 GF-2, head 2b4960172644 — tier 2; preflight 12/15, 3 legs SKIPPED
---
# READY FOR QA — PR #1248 (KS-1143 GF-2). Seat L6, item 5 of 8. Four PRs with you. Going straight to KS-1144.

## THE FIVE ARTEFACTS
1. **PR #1248** — https://github.com/Secuura/Distributed_Secuura/pull/1248 (open, base `develop`).
2. **Head `2b4960172644b5ef0414b94d46d11974012c2007`**, read from origin in the same action as this sentence.
3. **Ticket comment naming the PR:** KS-1143, comment `bac4c257-ca17-48d5-b4d2-a5b4b6000d14`.
4. **Test Evidence block in the PR body**, written by me, who ran it.
5. **What is NOT covered** — below.

**Tier proposed: 2.** One test file, one commit, no runtime surface, no migration, no config.

## 🔴 THE GATE DID NOT COME BACK CLEAN, AND I AM NOT QUOTING IT AS ONE
This is a `Blockchain/Dev/` path, so the hook ran — 7 minutes. Verbatim:

```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```

**12 of 15 legs ran, nothing failed, legs 3/4/8 skipped** because the local stack is not up. I have not started
the stack: doing so is an environment action this lane was not commissioned for, and three of my four PRs
never reach these legs at all. Say the word and I will bring it up and re-push, or rule that 12/15 with
nothing failed is what a `packages/shared` test-only change gets.

**The fleet STOP count, all three matched:**
- `pre_push_hook_base.test.sh` — **28 passed, 0 failed**
- `pre_push_hook_base_fixture_guard.test.sh` — **6 passed, 0 failed**
- shell suites — **60 passed, 0 failed, 0 skipped (of 60)**
- no line starting `FIXTURE BUILD FAILED`.
`packages/shared` was **built before the push**, which is what makes the runner read 60/0 and not 59/1.

⚠ **My first read of that count was wrong and I caught it with a control.** A `sed` window pinned to line
numbers picked up the NEIGHBOURING suite's summary and reported the fixture guard as **15**. The extraction is
now anchored to each suite's `=== …test.sh ===` header, and it has a control that returns NOT FOUND for a
header that does not exist. The three numbers above are from the anchored read.

## THE TAKE-OVER, AND WHAT I CHANGED ABOUT IT
`a40cb9eea049` cherry-picked onto develop `6e2a00bfe`, clean, one file, one commit.

**I amended the commit message before pushing.** It carried `922 -> 924`, `baseline 11 passed` and
`tampers 4/4 red` — all measured on a tree stacked on #1215's pre-squash head, which this commit no longer
sits on. A commit body lands on develop permanently, so it must not assert a measurement its own tree cannot
reproduce. The amended message carries THIS tree's numbers and says why. Tree verified identical across the
amend; only the message moved.

## NUMBERS — base MEASURED, not inferred
develop's blob for the file was written into place, the suite run, then the file restored from my saved byte
copy and the restore verified by sha256.

| | base | head |
|---|---|---|
| `packages/shared` `npm test` | 47 files / **928** / 0 failed | 47 files / **930** / 0 failed |
| ks781 file alone | — | **238** passed |
| `npm run build` (tsc) | rc 0 | rc 0 |
| `npm run lint` | rc 1 | rc 1, findings **byte-identical** (`diff` empty; control fires) |
| timeouts | — | **0**, at load 8.09 -> 7.45 |

`npm run lint` is red on develop too — the pre-existing `no-control-regex` at `:539`, already on BACKLOG.md.
I am reporting rc 1 rather than hiding it, and proving the finding set did not change.

## RED PROOF — 4 arms, all red, restores sha256-asserted
- **A1 run FIRST, on your instruction** — continuations accept ANY argument -> **W8 only**. **It red.** So the
  fixture survived the rebase and the matrix is READ. Had it not, I was to STOP and mail.
- A2 revert the fix, walk the whole body -> W7 **and** W8.
- A3 `parserContinuations` returns nothing -> W2, W3 **and** the undeclared-parser census.
- A4 W7's expectation flipped -> **W7 only**.
Baseline 238/238 between arms; final sha256 identical to the pre-tamper hash.

**A3 reds three cells here, not two.** The earlier run was filtered to the wrapper family; mine runs the whole
file. A difference in the scope of the run, not in the product — said plainly rather than left as a mismatch.

**My script is new, not an edit of the predecessor's**, and differs in three ways each forced by something its
version could not do here: its restore copies from a path in ITS session's scratchpad and only PRINTS two
hashes for a human to compare (mine exits 9 on a mismatch); its runner pipes vitest into grep, so any rc is
grep's (mine redirects and reads `$?`); and A1 is moved to the front.

## AN ENVIRONMENT GAP, FOUND ON THE WAY IN — reporting, not fixing
`packages/shared` declares `"test": "vitest run"` but does **not** declare `vitest` in its own dependencies or
devDependencies, and neither does `Blockchain/Dev`. It resolves only from the workspace-root lockfile
(vitest 4.1.11). **`npm ci` run inside the member installs 7 packages and no `.bin`, so the suite exits 127** —
which reads like a broken tree rather than a missing install. The working install is `npm ci` at
`Blockchain/Dev`. Control: three other seats' worktrees also have no vitest binary under `packages/shared`.
**Not fixed** — `package.json` is out of lane and under the no-package.json HOLD. Do you want a ticket?

## NOT COVERED
- **The indirect-invocation false negative stays out of scope** by your ruling. The disclosed limit is
  unchanged and in the code: a continuation passed by NAME is not a function expression, so a guard inside it
  reads `false` — under-reporting, the safe direction. GF-1 stays closed by #1212.
- This guard reads the whole `services/` + `packages/` tree by TEXT, so a later merge from another lane can
  move its verdict. Stated at head `2b4960172644` over develop `6e2a00bfed57`.
- Legs 3, 4, 8 of the preflight did not run. No environment, no docker, no database. **Nothing deployed.**

## WITH YOU NOW
- **#1243** KS-1117 + KS-1300 items 2-4, `0c89e2b503d9` · **#1244** KS-1111, `146b620fda53` ·
  **#1245** KS-1313, `1700b5ae7dd5` · **#1248** KS-1143 GF-2, `2b4960172644`. All tier 2.

## STATE
develop unchanged at `6e2a00bfed57`. `.push-lock-24` free — four takes, each released; this one held 7 min for
the in-hook preflight. Shared checkout: no pull, no fetch, no commit. 4 orphaned `login_stub` pids reaped by
cwd under my own worktree, 0 left. No container, no database, no port.

## NEXT, IN THIS TURN
**Item 6, KS-1144** — J2's missing positive control and the `:4650` assertion that cannot fail. Per your Q5
ruling it branches from **#1248's head**, not develop, as a **declared overlap** on the same file, with the
equality target the MERGED blob.
