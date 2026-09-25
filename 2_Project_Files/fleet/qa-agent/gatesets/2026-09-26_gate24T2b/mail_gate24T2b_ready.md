# CAPTURE — gate24T2b READY mails, VERBATIM by message id (captured 2026-09-25T15:12:33Z by capture_mail_gate24T2b.py; instrument: `inbox_digest.sh full wednesday-agent@agentmail.to <id>`)

SEVEN READYs from THREE seats. PR #1249 is KS-1144, head 6eb283d058184f1f0fabdc3c3184a817db4fb94b (STACKED on #1248 2b4960172644b5ef0414b94d46d11974012c2007, which is in the RUNNING gate24T2a batch); PR #1250 is KS-1302 + KS-1303, head c78f4093fb531bceb94a8e9defb59350d8c60b73; PR #1251 is KS-1147, head 8020adae99129f4b7194fef32f1ea5b762819d90; PR #1252 is KS-1275 + KS-1299, head ca7337fa04e04e5438bc79a5abe215424fcb33ef; PR #1253 is KS-1297, head 6b88e4f03e82e3da0672efb1bb757ba5da912d6a; PR #1254 is KS-1155, head da0c94968a7423c340b3a3b76244bda536d1f6d2; PR #1255 is KS-1301, head 59245ff0b11c6b760ba5e2a9daedc5927e915e10. The batch is FROZEN at seven (#1254 and #1255 added by Wednesday mid-draft). NOT in it: #1248 (gate24T2a), and Seat L5's widen items KS-1201 / KS-1296 / KS-906 / KS-1139 (no PR on origin at pin; READY mails not read by the drafter). Seat L5's DECLARED COUNTS mail is captured last, as context.
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks828-900-981-04807ea0e-tier2-r1/report.md sha256 46b0fd1882b44ca7aea877284bd2c6c3ab48575291e5ebe4c40ffe615be9230b (37866 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1234-t1-r1/report.md sha256 a97d15478b66c1aed19cb8d5f602a9fb9d3484add12b58f93061a8c272b2a563 (51396 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks924-901-980-103c235b4-tier2-r2/report.md sha256 e59f549bd3e7e7d324ce8303a2e4584d9005e67ed552a8ac5f9a17cb2f5772d3 (35221 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-16-ks1123-1002-a376756ab-ks1165-1003-c5488a689-tier2-r1/report.md sha256 6c269c90e9bb800f66d957ceb62273361aed8c09a2ceea1b8a102d3382f63163 (45637 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1218-t2c/report.md sha256 70dc4c987f04b3fd801130016c6df7536551989294a4b802cda48b262466535c (70301 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1239-t1-r2/report.md sha256 86dbbcab15858b6d81b5f629fffb24ec2c5e790e5d5e3fa5ef4861311c0f068b (39941 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1241-t2d/report.md sha256 ef04788f1632d34ce09dc4c085de2e0f286b96b347aa359f8f06ba1f8eb263e9 (41708 bytes)

## Seat L6 READY FOR QA — #1249 KS-1144, STACKED on #1248 (14:22:34Z)
MESSAGE_ID <010001a0d8f25099-86861d1a-705b-4d79-9b56-6911dba50d23-000000@email.amazonses.com>
TEXT_SHA256 e467792279598a1f1920508467017763a1bdc24290dce4cf2fb7cfdaceffca89
#1249 KS-1144 head 6eb283d058184f1f0fabdc3c3184a817db4fb94b (the READY names it in full; origin read by predict_gate24T2b.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T14:22:34.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L6): PR #1249 KS-1144 stacked on #1248, head 6eb283d05818 — tier 2; one ticket proposal NOT followed, with the measurement
---
# READY FOR QA — PR #1249 (KS-1144). Seat L6, item 6 of 8. Five PRs with you. Going to KS-1147 in this turn.

## THE FIVE ARTEFACTS
1. **PR #1249** — https://github.com/Secuura/Distributed_Secuura/pull/1249 (open, base `develop`).
2. **Head `6eb283d058184f1f0fabdc3c3184a817db4fb94b`**, read from origin in the same action as this sentence.
3. **Ticket comment naming the PR:** KS-1144, comment `ffa40d2b-87d7-479c-a472-69a75dcdc05b`.
4. **Test Evidence block in the PR body**, written by me, who ran it.
5. **What is NOT covered** — below.

**Tier proposed: 2.** One test file, control scaffolding only, no product predicate, no runtime surface.

## ⚠ STACKED — the declared overlap you ruled at Q5
Branched from **#1248's head `2b4960172644`**, not develop, same file. #1248 changes the PRODUCT predicate
(the guard walk); this changes J2's CONTROL scaffolding. **The equality target for #1249 is the MERGED blob,
not the head blob, and #1248 merges first.** That is stated at the top of the PR body so a merge seat cannot
miss it.

## 🔴 I DID NOT FOLLOW ONE OF THE TICKET'S PROPOSALS, AND THIS IS THE REASON
KS-1144 GF-4 says the assertion `recorded once, not once per export site` **cannot fail**, because `exported`
is a `Map<string, Set<string>>` and a Set cannot hold `jsonParser` twice, and proposes dropping it.

**Measured: that reading is wrong.** `addExport` maps an `exportedAs` of `default` back to the **local** name.
So the CONTROL fixture — the modifier export PLUS `export { jsonParser as default }` — adds the string
`jsonParser` **twice**, and only the Set makes the answer carry it once. **Replacing that Set with an array
reds that cell alone: 1 failed / 237 passed**, measured on this branch's base before I changed anything.

So the line is a **live pin on de-duplication**, not a tautology. I kept it, wrote the measurement beside it
in the code, and made it arm B2 of the matrix so the pin is demonstrably live. The finding's premise is true
(a Set cannot hold it twice) — it is the conclusion that does not follow, because the Set is the thing under
test, not a fact about the world.

If you would rather have the ticket's proposal as written, say so and I will drop it — but I would be removing
the only cell that notices if `exported` ever stops de-duplicating.

## GF-3 — done, and the finding restated as a measurement
The walk was inline in J2 with nothing showing it could find anything. It is now `defaultShapesOf(source)`
with four control cells: one per shape, plus all three at once, plus the object-literal default asserted
INVISIBLE — without that last one, J2's `toEqual([])` on the real module would be asserting the absence of
something the walk never looks for.

**Arm B1 disables the walk. It reds the four new controls and does NOT red J2.** Before this change that same
tamper reddened nothing at all. That is the finding, measured rather than repeated.

## NUMBERS
- `packages/shared` `npm test`: **47 files / 934 passed / 0 failed**, rc 0, **0 timeouts**, load 6.84.
  Base = #1248's head, measured at **930**. So **930 → 934**, exactly the four new cells. (#1248 is 928 → 930
  over develop, so the stack is 928 → 934.)
- tsc rc 0. eslint rc 1, findings **identical to develop's set** (`diff` empty, control fires) — the one error
  is the pre-existing `no-control-regex` at `:539`, red on develop too and already on BACKLOG.md.

## RED PROOF — 4 arms, all red, restores sha256-asserted
- B1 the three `shapes.push(...)` disabled -> **the four new controls, and NOT J2**.
- B2 `Set` -> array in `addExport` -> the `recorded once` control, **only that one**.
- B3 the walk also sees an object-literal default -> the exclusion assertion + J2.
- B4 J2's own expectation flipped -> J2, **only that one**.

## WHICH GATE RAN — again NOT a clean pass
6 min 20 s. `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4, 8 skipped, local
stack not up. Fleet STOP count: `pre_push_hook_base` **28/0**, fixture guard **6/0**, shell suites
**60 passed, 0 failed, 0 skipped (of 60)**, no `FIXTURE BUILD FAILED`. Read anchored to each suite's section
header, with a control returning NOT FOUND for a header that does not exist.

**My question from the last mail stands:** do you want the local stack brought up so legs 3/4/8 run, or is
12/15-nothing-failed what a test-only `packages/shared` change gets? Two more of my PRs will hit this.

## NOT COVERED
- **R-2 is context only**, no change asked, untouched.
- The three default shapes cannot all be legal TypeScript in one module, which is why they are `it.each` rows
  as well as one combined fixture; `createSourceFile` parses the combined one, `tsc` would not accept it.
- This guard reads the whole tree by TEXT — a later merge from another lane can move its verdict.
- No environment, no docker, no database. **Nothing deployed.**

## WITH YOU NOW
**#1243** `0c89e2b503d9` · **#1244** `146b620fda53` · **#1245** `1700b5ae7dd5` · **#1248** `2b4960172644` ·
**#1249** `6eb283d05818` (stacked on #1248). All tier 2.

## STATE
develop unchanged at `6e2a00bfed57`. `.push-lock-24` free — five takes, each released, cool-off honoured.
Shared checkout: no pull, no fetch, no commit. 4 orphaned `login_stub` pids reaped by cwd, 0 left. No
container, no database, no port.

## NEXT, IN THIS TURN
**Item 7, KS-1147** — the ks860 escaped-host boundary, a separate file, so a PR of its own from develop.

## Seat L5 READY FOR QA — #1250 KS-1302 + KS-1303 (14:30:58Z)
MESSAGE_ID <010001a0d8fa01cc-8afa79ce-7b25-448c-a500-a2d6c75f30d8-000000@email.amazonses.com>
TEXT_SHA256 2fca8cf3ddd3380e7a3cfdbe8fea11b671a30977561f096a605af5d9fec04e36
#1250 KS-1302 + KS-1303 head c78f4093fb531bceb94a8e9defb59350d8c60b73 (the READY names it in full; origin read by predict_gate24T2b.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T14:30:58.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L5): PR #1250 KS-1302 + KS-1303, head c78f4093fb53 — 55/0 confirmed in-hook
---
# READY FOR QA (Seat L5): PR #1250 KS-1302 + KS-1303, head c78f4093fb53 — tier 2, preflight 12/15

## BLUF — the five artefacts
1. **PR `#1250`** (https://github.com/Secuura/Distributed_Secuura/pull/1250), open, base `develop`,
   2 files, +119 / −5.
2. **Head `c78f4093fb531bceb94a8e9defb59350d8c60b73`**, read from origin by `ls-remote` **and**
   from the GitHub API in the same action as writing this sentence. Both agree.
3. **Ticket comments naming the PR — TWO, one per key:** KS-1302 comment
   `ededa074-38a9-4885-849f-497ea9216637`, KS-1303 comment `a168426c-6686-4661-be83-7930c44f256c`.
   Both tickets In Progress.
4. **Test Evidence block in the PR body, written by me, who ran every test in it.**
5. **What was NOT covered — five items, below.**

**Tier 2.** Nothing merged.

## NAME THE GATE — this one DID run the preflight
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` ·
`legs 3 4 8 — local stack not up.` **Quoted as INCOMPLETE, never as a pass** — the tool itself
prints "This is NOT a pass. Do not quote it as one."

**All four declared counts confirmed LIVE in that gate, by the patched runner doing the running:**
- `pre_push_hook_base` **28 passed, 0 failed**
- `pre_push_hook_base_fixture_guard` **6 passed, 0 failed**
- `run_shell_suites` **55 passed, 0 failed** — the re-declared k=6 figure
- **`shell suites: 60 passed, 0 failed, 0 skipped (of 60)`**
Plus 13 code guards OK, production-guard **23 / 23** services, 7 portability rules over 102 scripts.

**One figure I had to attribute before trusting it:** a `  10 passed, 0 failed` in the same log is
`systemTest/__tests__/quarantine_call_sites.test.sh`, not the fixture guard — they share a verdict
format. Read as the guard it would have looked like an undeclared 6→10 delta.

## RED / GREEN
- **GREEN**, patched runner: `run_shell_suites: 55 passed, 0 failed`, rc 0.
- **RED**, pre-patch runner `7912bb9d…` via `RUNNER_SH`: **52 passed, 3 failed**, rc 1 — cells 2, 4
  and 5, **one arm per conjunct**. The three preconditions/controls hold on both sides.
- **The other 49 pre-existing cells are byte-identical between the two runs.**

## THE MISTAKE INSIDE MY OWN RED PROOF, disclosed
My first KS-1303 fixture was `sleep 15 >/dev/null 2>&1 &`. I redirected the child's output **for
tidiness**, which removed its grip on the pipe — the entire mechanism under test — and **the cell
PASSED against the unfixed runner.** Now `sleep 15 &`, with the reason written into the suite
beside the fixture. Same family as Seat L4's #1218 round 1.

## BASE MOVEMENT — checked, not assumed
develop moved `6e2a00bfe` → `14cc526d10ee` (#1246) → `77c6426b96d9` (#1247, mine) under this
branch. Via the compare API, **no fetch, no ref write**: 2 commits, 4 files, **zero overlap** with
either of my two paths. Base-invariant, so no merge-in.

## NOT COVERED — five things
1. **Legs 3, 4, 8 did not run** (no local stack). 12/15.
2. **No survey of the 60 suites for existing background children.** The fix removes the mechanism;
   it does not audit for instances.
3. **The 16 pre-existing `/tmp/rss.*` directories are NOT cleaned up.** New ones stop; old ones
   stay. "Never delete" applies and nobody asked.
4. **The `INT`/`TERM` arms of the trap are NOT exercised by a cell** — only `EXIT`, clean and
   failing. Signalling the runner mid-run from inside its own suite is a fixture I judged too
   flaky to be worth it. The trap lists them; that much is unverified.
5. **No measurement on Linux.** Everything is macOS `/bin/bash` 3.2.57.

## Also worth knowing for whoever tests this
This host's `TMPDIR` is **49 chars**, under the runner's 80-char threshold, so a plain run creates
no `/tmp/rss.*` at all — a cell that merely runs the runner proves nothing. That is why cell 1 is
a precondition asserting the substitution fired and the runner named its directory.

## Shared state
Shared checkout unmoved: HEAD `3bad652d17cf`, local `develop` `3bad652d17cf`, porcelain 17. No
fetch, ever. Shared `.git/config` **byte-identical across the push** (`7f1a685039…`). 4 leaked
`login_stub.mjs` listeners from this worktree were reaped by command+cwd+ppid re-verified in the
same action; **0 of mine remain**. The push waited **337 s** behind Seat L6 — the fairness
machinery working, holder named at every poll.

## MEANWHILE — not ending my turn on this
**Item 4's push is IN FLIGHT as a background job** (`feature/ks-1297-…-l5-1`, head
`6b88e4f03e82`; its in-hook fixture guard will read **10/0**, my declared count). While it runs I
am **building item 2 (KS-1296)**. Then items 5, 7, 6.

*Seat L5, 2026-09-25. Evidence: `raise/s-l5-ks1302-push.out`, `proof/ks1302_green.out`,
`proof/ks1302_red.out`, `proof/push_item3.out`.*

## Seat L6 READY FOR QA — #1251 KS-1147 (14:35:55Z)
MESSAGE_ID <010001a0d8fe8c77-18c17d2b-62a7-43b7-aa2b-4d3150eb398f-000000@email.amazonses.com>
TEXT_SHA256 f7dbae117ce5f7a32517e36cb34544fd104cef9b6133d984b0f23c413d155f1f
#1251 KS-1147 head 8020adae99129f4b7194fef32f1ea5b762819d90 (the READY names it in full; origin read by predict_gate24T2b.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T14:35:55.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L6): PR #1251 KS-1147, head 8020adae9912 — tier 2; ticket's fix shape shipped over mine, with the measurement
---
# READY FOR QA — PR #1251 (KS-1147). Seat L6, item 7 of 8. Six PRs with you. KS-1155 next, in this turn.

## THE FIVE ARTEFACTS
1. **PR #1251** — https://github.com/Secuura/Distributed_Secuura/pull/1251 (open, base `develop`).
2. **Head `8020adae99129f4b7194fef32f1ea5b762819d90`**, read from origin in the same action as this sentence.
3. **Ticket comment naming the PR:** KS-1147, comment `c3bee428-c57d-4090-a060-3850222ace30`.
4. **Test Evidence block in the PR body**, written by me, who ran it.
5. **What is NOT covered** — below.

**Tier proposed: 2.** One guard file, one commit. Independent of the ks781 stack: same package, different
file, branched from develop, no overlap to declare.

## TWO MEASUREMENTS CHANGED WHAT SHIPPED, and the second is the third instance of one pattern today
**1. My first fixture was unrepresentative and failed for the wrong reason.** A bare
`app.listen(0, \"127.0.0.1\")` snippet has no opening quote, so the mask enters `dq` at the first `\"` and
reaches EOF still inside it. The cell failed on a **desynchronised mask announcement**, nothing to do with
the host check. This file already records that exact trap for docblock body lines — *a fragment that never
occurs without its delimiters is not a fixture* — and I walked into it anyway. The cells now feed the whole
enclosing literal, which is the shape the gate described.

**2. My stricter regex was not load-bearing, so the TICKET'S proposal ships instead of mine.** I had made
the closing escape repeat the opener's, so a mismatched pair (`\"127.0.0.1"`) stayed a violation. **Relaxing
that to independent escapes reddened NOTHING — 25/25.** No representative fixture distinguishes the two,
because a mismatched pair does not occur in a well-formed source file.

**That is the third time today a tamper found nothing and the honest move was to change the claim rather
than keep the code:** L3's inherited W8 on KS-1143, my duplicate-label check on KS-1313, and this. In the
first two the answer was to find the fixture that discriminates; here there is no such fixture, so the
strictness comes out. Both outcomes are the same rule — untested strictness in a guard is not a guard.

## NUMBERS — base MEASURED, not inferred
develop's blob written into place, the suite run, then restored and the restore verified by sha256.

| | base | head |
|---|---|---|
| `packages/shared` | 47 files / **928** / 0 failed | 47 files / **930** / 0 failed |
| tsc | rc 0 | rc 0 |
| eslint | rc 1 | rc 1, findings **byte-identical** (`diff` empty; control fires) |
| timeouts | — | **0**, at load 4.78 |

eslint's one error is the pre-existing `no-control-regex` at `:539`, red on develop too and on BACKLOG.md.

## RED PROOF
Before the fix: the escaped-host cell **red**, the control cell (a wrong or missing host stays a violation)
**green**. So the new cells discriminate the fix, not the file.

Tamper matrix, 3 arms, all red, restores sha256-asserted:
- **C1** revert the widening -> the escaped-host cell, **only that one**.
- **C2** stop checking the ADDRESS -> the wrong-host control, **only that one**.
- **C4** host check never matches -> 6 cells, including the tree census and the pre-existing
  accepted-spelling control.
(C3 was the fourth arm; it became the shipped form, per point 2 above, and is recorded in the script.)

**The tree census is green at this head**, so the widening has not made a real offender invisible. C2 is the
arm that would catch that, and it reds.

## WHICH GATE RAN — again NOT a clean pass
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4, 8 skipped, local stack not up.
Fleet STOP count: `pre_push_hook_base` **28/0**, fixture guard **6/0**, shell suites **60 passed, 0 failed,
0 skipped (of 60)**, no `FIXTURE BUILD FAILED`.

**Third mail asking the same question, so I will state it as a decision you can take once:** three of my PRs
have now come back 12/15. Either the local stack goes up and these get re-pushed, or 12/15-nothing-failed is
the standing verdict for a test-only `packages/shared` change. I have not started the stack because that is
an environment action this lane was not commissioned for.

## NOT COVERED
- **Nothing on develop trips this today** — the guard's boundary, recorded as R-5, not a live defect.
- Tg-D (`listen(3000)` with no host passing `\s*0\s*`) is the regex's declared narrowness — port 0 only —
  and is untouched.
- The guard reads the whole tree by TEXT; a later merge from another lane can move its verdict.
- No environment, no docker, no database. **Nothing deployed.**

## WITH YOU NOW — six
**#1243** `0c89e2b503d9` · **#1244** `146b620fda53` · **#1245** `1700b5ae7dd5` · **#1248** `2b4960172644` ·
**#1249** `6eb283d05818` (stacked on #1248, merged second) · **#1251** `8020adae9912`. All tier 2.

## STATE
develop unchanged at `6e2a00bfed57`. `.push-lock-24` free — six takes, each released, cool-off honoured.
Shared checkout: no pull, no fetch, no commit. 0 orphaned `login_stub` pids. No container, no database,
no port. Nothing deployed.

## NEXT, IN THIS TURN
**Item 8, KS-1155** — the guard timeout budget through the `vitest.config.ts` override you accepted at Q6.
One file, zero guard files, no loosened assertions, `uptime` beside every run, and the ticket's
"0 timeouts at load >= 30" bar stated **UNMET** — tonight's load is nowhere near 30 and I will not
manufacture it.

## Seat B 28th READY FOR QA — #1252 KS-1275 + KS-1299 (14:43:58Z)
MESSAGE_ID <010001a0d905ead3-23523114-c544-4596-97ee-a17b191f02d6-000000@email.amazonses.com>
TEXT_SHA256 49dfedf768e97a9bc86e1bb7ead0a06881f09673be19ce0557fba900ee3e327e
#1252 KS-1275 + KS-1299 head ca7337fa04e04e5438bc79a5abe215424fcb33ef (the READY names it in full; origin read by predict_gate24T2b.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T14:43:58.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 28th): #1252 KS-1275 + KS-1299 head ca7337fa04e0 — 5 red arms; leg 8 (served-spec) is among the 3 skipped
---
READY FOR QA (Seat B 28th): #1252 KS-1275 + KS-1299 at head ca7337fa04e04e5438bc79a5abe215424fcb33ef

## BLUF
Item 2 READY. Two published descriptions corrected, yaml regenerated, and #1123's sentence-pinning
cell replaced by two property cells. Not merged. Preflight INCOMPLETE 12/15 (legs 3, 4, 8 — local
stack), and **leg 8 is the served-spec-vs-yaml check, i.e. the one most related to this change**;
stated in the PR body and both ticket comments rather than buried. develop is `77c6426b96d9`, my base.

## THE FIVE ARTEFACTS
1. **PR #1252** — https://github.com/Secuura/Distributed_Secuura/pull/1252 (open, base develop, 1 commit).
2. **Head, read from origin in the same action:** `ca7337fa04e04e5438bc79a5abe215424fcb33ef`
   (GET /pulls/1252 -> head.sha, and `ls-remote` agrees). 3 files, +56 −14; GitHub's own /files list
   matches the three I intended.
3. **Ticket comments naming the PR:** KS-1275 `82e55642-18d7-4eb0-8484-2cbb537ed8c1`,
   KS-1299 `4eb28af2-b6d5-440f-94d6-1e88d22fea55`. Both re-counted 0 -> 1 after posting.
4. **Test Evidence: in the PR body, written by me, who ran it.**
5. **NOT covered: below, same words as the PR.**

## KS-1275 — the pin moved from the SENTENCE to the PROPERTY
The description enumerated the excluded verbs inline; it now points at `lifecycleActions.ts` and
`docs/VOCABULARY.md` and names no verb. #1123's `DESCRIPTIONVERBLIST` parsed that sentence
(`split(' etc.')[0].split(' ').pop().split('/')`), so removing the list reds it by construction.
**I measured it going red BEFORE replacing it** — 1 failed / 11 passed, parse yielding
`["re-synchronised."]` — so the change was proven to reach the cell rather than assumed to.
Replaced by `DESCRIPTIONPOINTSATSOURCE` (description names both sources and no dedicated-route verb;
verb set read from the registry, asserted non-empty) and `EXCLUSIONHOLDS` (no dedicated-route verb is
in LIFECYCLE_EVENT_ACTIONS; both sides asserted non-empty). `ORDERTHROUGHSPEC` untouched, green.

**FIVE RED ARMS, ONE CONJUNCT EACH**, per your standing line. Each flips exactly one term with the
others held true; each reddens EXACTLY ONE cell and leaves the other twelve green; every restore
verified by sha256 against the pre-tamper hash:
  A1 drop the enum pointer -> DESCRIPTIONPOINTSATSOURCE
  A2 drop the vocabulary pointer -> DESCRIPTIONPOINTSATSOURCE
  A3 a dedicated-route verb creeps back into the description -> DESCRIPTIONPOINTSATSOURCE
  B1 add `revoke` to LIFECYCLE_EVENT_ACTIONS -> EXCLUSIONHOLDS
  B2 the registry read matches nothing -> EXCLUSIONHOLDS reds **rather than passing vacuously**
B2's anchor is byte-identical to a line in the sibling cell (`:161` vs `:175`), so the unique-anchor
guard REFUSED it and I tampered by LINE NUMBER with the content asserted and the sibling proved
unmoved. Untampered re-run after all five: 13/13, rc 0.

## KS-1299 — mirrored, not reworded
The v2 description said v1 reads `hash` LAST "so its legacy bodies keep their answer". #1223 corrected
exactly that in `routes/verification.ts` (KS-1118 F-3) and the spec never followed. Now: an alias-carrying
body keeps its lookup value, but a body pairing `hash` with `documentId`/`documentData` takes the HASH
strategy on v1 too; documentId-only, documentData-only and alias-only bodies unchanged.

## RAN
- originate jest `--runInBand`: **870 passed / 870, 74/74 suites**, rc 0. Baseline 869 at `6e2a00bfe`;
  **the +1 is accounted** — one cell replaced by two — and I checked the base move `6e2a00bfe..77c6426b9`
  adds NO originate test cell (it is `.githooks/pre-push` plus my own merged comment-only change), so
  869 is the right comparison rather than an assumed one.
- `npm run lint` (= `eslint src`, the whole script): rc 0.
- `tsc --noEmit` rc 0; re-run with `exclude: []` and the edited test file asserted present in the
  program (705 files, `--listFilesOnly`) because the project tsconfig excludes `src/__tests__`: rc 0.
- `npm test -w packages/shared`: 47 files / 928 tests, rc 0.
- `generate-openapi --check`: **PASS**, and **it also passed on the base BEFORE I edited** — so the
  yaml's +13/−6 is attributable to this change alone and carries no foreign drift.
- Push: rc 0, 7m02s. STOP count matched exactly — `pre_push_hook_base` 28/0,
  `pre_push_hook_base_fixture_guard` 6/0, shell suites 60/0/0 of 60. No `FIXTURE BUILD FAILED`.

## NOT COVERED
- **Preflight INCOMPLETE — 12/15 legs, 3 SKIPPED** (legs **3** spec-auth, **4** path resolvability,
  **8** served-spec consistency), each `local stack not up on http://localhost:6882`. A skip is not a
  pass. **Leg 8 matters here specifically:** it compares served `/api/docs/openapi.json` against the
  on-disk `.yaml` — the artefact this PR regenerates — so the check closest to my change is one of the
  three that did not run. `generate-openapi --check` covers source-vs-disk, NOT served-vs-disk.
- No cell pins KS-1299's wording. It is prose about a precedence rule already pinned behaviourally
  (#1149, #1170/#1223); a text-matching cell would recreate the sentence-pinning problem KS-1275
  removes in the same PR. Deliberate, and said rather than left implicit.
- No integration/e2e: no runtime surface. The executable accepted-verb set is unchanged, which
  `EXCLUSIONHOLDS` asserts.
- `migrations/037` untouched, as the brief required.

## PUSH PROTOCOL — SELF-RULED BENIGN
Lock taken at poll 24 after **117 s** behind Seat L6 (`feature/ks-1147-ks860-escaped-host-l6-r24-1`,
healthy: pid alive, heartbeat fresh). Snapshot diff, every line attributed:
- **config 2 lines:** `branch.feature/ks-1147-…-l6-r24-1.{remote,merge}` — Seat L6's `-u` upstream block.
- **refs 7 lines:** `-l6-` (ks1155, plus L6's tracking ref for ks1147), `-l5-` (ks1201, ks906, and
  ks1296 moving `6e2a00bfe` -> `ff90fbf9d`), and my own
  `refs/remotes/origin/feature/ks-1275-…-r24-b-1` at my sha.
- **worktree:** `s-l5-ks1201` and `s-l5-ks906` added, an `s-l5-ks1296` HEAD move, a
  `locked initializing` cleared — all `s-l5-*`.
**Nothing touches my branch, my worktree or develop**, and origin holds my branch at my sha. Both
attribution conditions hold, so ruled benign under your 2026-09-17 11:09:40Z ruling and recorded here.

## NEXT, IN THIS TURN
Item 3: **KS-1301** — port #1237's four presence cells to `sign-cert` and `sign-wallet`, one red arm
per route. Reading #1237 (`e119781ac`, 28 lines in the ks1213 suite) first. Not ending my turn here.

— Seat B 28th

## Seat L5 READY FOR QA — #1253 KS-1297 (14:51:05Z)
MESSAGE_ID <010001a0d90c6d1b-1e17e28b-da49-4329-bfd4-d797404c9b82-000000@email.amazonses.com>
TEXT_SHA256 26538e5da7f4262d09f52878ee6755354c3db61fa5fa37fe74889c8b084742e3
#1253 KS-1297 head 6b88e4f03e82e3da0672efb1bb757ba5da912d6a (the READY names it in full; origin read by predict_gate24T2b.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T14:51:05.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L5): PR #1253 KS-1297, head 6b88e4f03e82 — fixture_guard 10/0 as declared
---
# READY FOR QA (Seat L5): PR #1253 KS-1297, head 6b88e4f03e82 — fixture_guard 10/0 as declared

## BLUF — the five artefacts
1. **PR `#1253`** (https://github.com/Secuura/Distributed_Secuura/pull/1253), open, base `develop`,
   1 file, +115 / −3.
2. **Head `6b88e4f03e82e3da0672efb1bb757ba5da912d6a`**, read from origin by `ls-remote` and from
   the GitHub API in the same action as writing this sentence. Both agree.
3. **Ticket comment naming the PR — KS-1297 comment `eb1cc744-c3bd-4ca0-8934-1b10006cff09`**, which
   also carries the facts-only correction to the ticket's text that you asked for.
4. **Test Evidence block in the PR body, written by me, who ran every test in it.**
5. **What was NOT covered — five items, below.**

**Tier 2.** Nothing merged.

## THE DECLARED COUNT CAME IN EXACTLY
`fixture_guard` **10 passed, 0 failed** — the figure I declared before the push, produced by the
patched guard itself inside the hook. Alongside it in the same gate:
`pre_push_hook_base` **28/0** · `run_shell_suites` **49/0** (this worktree carries the base runner;
the 55 figure belongs to #1250) · **shell suites 60 passed, 0 failed, 0 skipped (of 60)** ·
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` · `legs 3 4 8 — local stack
not up.` **Quoted as INCOMPLETE, never as a pass.**

## THE RULING APPLIED, and the ticket corrected
NB-1218-c is pinned to the **subshell family**, as you ruled. The seven-row call-site table is in
the PR body and in the ticket comment, and the comment states plainly that the defect class is
**"a call site that runs `build_fixture` in a subshell"**, not "errexit suspended" — because
`build_fixture` aborts with an explicit `exit 2` and the subject has no `set -e`, so `|| true`,
`if` and `&&` are all already safe. A cell on the ticket's literal wording could not have failed.

The PR body also says, as you directed, that **`repo_state()` hashed HEAD + refs + config only**,
which is exactly why NB-1218-b's worktree write was unpinned — and that anchoring `:181` is a
**narrowing** rather than a tightening.

## RED / GREEN — three arms, one per conjunct, each isolated
- **GREEN 10/0.**
- anchors reverted in a copy → **9/1**, cell 7 alone.
- `repo_state` un-widened in a copy → **9/1**, cell 8 alone.
- one call site wrapped in a subshell (**`c1`**, chosen so the other cells' line-anchored seds still
  apply) → **8/2**, cell 9 and its own control, nothing else.
- A coarser fourth arm wrapping **`c0`** reads **5/5**; I report the breakdown rather than the
  number, because it additionally reds cells 1, 2, 4 and 10 — their seds are anchored on
  `^build_fixture "$WORK/c0"…`, which the wrap no longer matches, so **cells 4 and 10 correctly
  detect that their own tamper did not apply.** That is those guards working, and it is why the
  `c1` arm is the one I quote.

## THE MISTAKE INSIDE MY OWN WORK, disclosed
**Cell 7's first draft could not fail.** It asserted that a prefixed line fails `grep -c '^…'` and
satisfies `grep -c '…'` — facts about **grep**, true on every machine forever. Restructured: the
assertion is now static over the suite's own bytes (both counts anchored, 2 of 2, 0 loose) and the
grep demonstration is demoted to the control reported beside it. **That is the second of four such
checks I caught in myself this round; all four were caught by writing the control, none by
re-reading.** The other three are in the handover.

## NOT COVERED — five things
1. **NB-1218-c is pinned STATICALLY, not behaviourally.** The cell reads the call sites; it does
   not run the suite under a wrapped call site and assert the abort survives, because at develop it
   would not — that is the gap itself.
2. **NB-1218-b is pinned for an unstaged edit and an index change**, not for every conceivable
   worktree mutation. A change leaving both `status --porcelain` and `ls-files -s` identical would
   still slip through; I did not try to enumerate one.
3. **The 12-of-12 call-site census covers `pre_push_hook_base.test.sh` only.** If another suite
   ever calls `build_fixture`, this cell does not see it.
4. **Legs 3, 4, 8 did not run** (no local stack). 12/15.
5. **No measurement on Linux or on bash ≥ 4.** Everything is macOS `/bin/bash` 3.2.57.

## Shared state
Shared checkout unmoved: HEAD `3bad652d17cf`, local `develop` `3bad652d17cf`, porcelain 17, no
fetch ever. **Shared `.git/config` byte-identical across the push** (`9ec0d98156…`). Ref count
1404 → 1406. **4 leaked `login_stub.mjs` listeners from this worktree reaped** by
command+cwd+ppid re-verified in the same action; 0 of mine remain. The push waited **704 s** for
the lock behind L6 then B 28th — the holder changed, so the queue was moving, and my poller named
it every 5 s.

## MEANWHILE — a live background job, not a narrated next step
**A sequential push driver is running** (`proof/push_driver.out`), one push per lock take:
item 5 (KS-1201) → item 2 (KS-1296) → item 7 (KS-906) → item 6 (KS-1139). All four are committed
and their counts are declared in my previous mail. **All 7 queue items are now built.** A READY
follows per PR as each lands. **The handover is written** at
`5_Project_History/HANDOVER-seatL5-2026-09-25.md`, including the two push-tool fixes you asked me
to carry forward.

*Seat L5, 2026-09-25. Evidence: `raise/s-l5-ks1297-push.out`, `proof/ks1297_green.out`,
`proof/ks1297_red_anchor.out`, `proof/ks1297_red_reposate.out`,
`proof/ks1297_red_subshell_c1.out`, `proof/ks1297_callsite_shapes.out`.*

## Seat L6 READY FOR QA — #1254 KS-1155, LANE COMPLETE (14:58:12Z)
MESSAGE_ID <010001a0d912f347-003f074b-3a44-4a73-a111-6df887f37c32-000000@email.amazonses.com>
TEXT_SHA256 d2f11ac9abc375998033a9d300089e62befa931c2dd1d16bc6733f20ffc264a7
#1254 KS-1155 head da0c94968a7423c340b3a3b76244bda536d1f6d2 (the READY names it in full; origin read by predict_gate24T2b.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T14:58:12.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L6): PR #1254 KS-1155 — LANE COMPLETE, all 8 items, 7 PRs, nothing deployed
---
# READY FOR QA — PR #1254 (KS-1155). **LANE COMPLETE: all 8 queue items built, 7 PRs, nothing merged, nothing deployed.**

## THE FIVE ARTEFACTS
1. **PR #1254** — https://github.com/Secuura/Distributed_Secuura/pull/1254 (open, base `develop`).
2. **Head `da0c94968a7423c340b3a3b76244bda536d1f6d2`**, read from origin in the same action as this sentence.
3. **Ticket comment naming the PR:** KS-1155, comment `1b79094b-7578-4063-9f4a-ebd9cc204d42`.
4. **Test Evidence block in the PR body**, written by me, who ran it.
5. **What is NOT covered** — below, and it includes a "done when" I am explicitly NOT claiming.

**Tier proposed: 2.** Fix-shape 1, scoped to touch **zero guard files**: `vitest.config.ts` plus two new
files under `src/__tests__/`.

## PROVEN END TO END, NOT ASSERTED
The SAME 6 s cell appended to a walker and to a non-walker, in one run:
`✓` in `ks860-…` (60 s budget) · `×  Test timed out in 5000ms` in `ssrf-guard`. Both restored byte-exactly,
sha256 asserted. The probe is **not** a standing cell — a 6 s cell would be paid on every run forever.

## THE GAP I MEASURED AND THEN CLOSED — the one worth reading
My first version passed every cell I had written. Then I removed `setupFiles` from the config and **nothing
reddened**. The cells checked the LIST and the PREDICATE; neither is evidence the setup file is ever
*loaded*, so the budget could have been unhooked in silence with the suite still green. There is now a cell
pinning the wiring, and its tamper arm reds. Without that measurement I would have shipped a budget nothing
proved was connected.

## ⚠ TWO TAMPER ARMS DID NOT APPLY AND PRINTED A CLEAN PASS
D4's anchor named the setup file when the symbol lives in the test file; D2's replacement was malformed. In
both cases the tamper's assertion failed, python exited, and the **unguarded** call let the arm report a
green run. **A tamper that silently does not apply reads exactly like a guard that cannot fail** — the same
family as a check that cannot fail, arriving through the instrument rather than the subject. Every arm now
exits on a failed tamper, and the matrix I am reporting is from the corrected run.

## NUMBERS
`packages/shared` **48 files / 933 passed / 0 failed**, rc 0, **0 timeouts**, at load 5.57.
Base measured in the same worktree before any change: **47 / 928 / 0** at load 7.67.
tsc rc 0. eslint rc 1, findings **identical to develop's set** (`diff` empty, control fires).

**Tamper matrix, 6 arms, all red**, restores sha256-asserted across all three files: D1 drop a walker ->
the equality cell names it · D2 add a non-walker -> equality + predicate control · D3 budget == default ->
"this is a raise" · D4 break the derivation markers -> the non-vacuity cell · D5 match the whole path ->
the directory-name control · D6 remove the wiring -> the wiring pin.

## 🔴 A "DONE WHEN" I AM NOT CLAIMING
KS-1155's first bar is a full `packages/shared` run **at load >= 30** reading 0 timeouts. Tonight's load was
**4.8-9.2**. My run is green with 0 timeouts at that load, which is **a different measurement**. I did not
manufacture load 30 and the bar stays open on the ticket. The second bar (a merge seat no longer needing a
solo re-run) follows from the budget but is a claim about future runs, so it is stated as intent.

Also out of scope and named: `threadToken.test.ts` (fix-shape 3, CPU-bound crypto, its own budget line) and
the vc-issuer `db.retry` half of the class, a different package.

## WHICH GATE RAN — NOT a clean pass
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4, 8 skipped, local stack not
up. Fleet STOP count: `pre_push_hook_base` **28/0**, fixture guard **6/0**, shell suites **60 passed, 0
failed, 0 skipped (of 60)** — **still 60/0 with the new `setupFiles` entry in place**, so this change has
not disturbed the fleet count. No `FIXTURE BUILD FAILED`.

# THE LANE, COMPLETE

| PR | key(s) | head | tier | gate that ran |
|---|---|---|---|---|
| #1243 | KS-1117 + KS-1300 items 2-4 | `0c89e2b503d9` | 2 | format only (systemTest path) |
| #1244 | KS-1111 | `146b620fda53` | 2 | format only |
| #1245 | KS-1313 | `1700b5ae7dd5` | 2 | format only |
| #1248 | KS-1143 GF-2 | `2b4960172644` | 2 | preflight 12/15, 3 skipped |
| #1249 | KS-1144 (stacked on #1248) | `6eb283d05818` | 2 | preflight 12/15, 3 skipped |
| #1251 | KS-1147 | `8020adae9912` | 2 | preflight 12/15, 3 skipped |
| #1254 | KS-1155 | `da0c94968a74` | 2 | preflight 12/15, 3 skipped |

**#1249 merges after #1248** — declared overlap, same file, equality target the MERGED blob.

**FOUR TICKETS WERE WRONG OR INCOMPLETE, each caught by measuring before building:**
- **KS-1117** understates the blast radius — a BOM before a leading comment AND real content fails too, so
  `config/secrets.example.yml` itself was unreadable. Its second regression cell already passed at base.
- **KS-1111**'s table overstates — the name pattern is unanchored except for `KEY`, so most secret names
  were masked BY ACCIDENT on the broken path. My first regression row was green before the fix.
- **KS-1313** omits `expected fail` — a two-word label, excluded from `passed` by the renderer. Folding it
  in would have made the sum check reject ordinary summaries.
- **KS-1144** says an assertion cannot fail. It can: swapping its Set for an array reds that cell alone. I
  kept the assertion against the ticket's proposal, with the measurement in the code.

**THREE TIMES A TAMPER FOUND NOTHING** and the honest move was to change the claim, not keep the code:
the inherited W8 case on KS-1143, my duplicate-label check on KS-1313 (found the discriminating fixture),
and KS-1147's escape-matching (no representative fixture exists, so the strictness came out and the
ticket's simpler shape shipped).

**MY OWN MISTAKES, all caught before a push:** a tamper arm labelled as proving a boundary it never reached;
an orphaned duplicate JSDoc left by a refactor; a first STOP-count read that picked up the neighbouring
suite's line and reported 15 instead of 6; an unrepresentative ks860 fixture that failed on a mask desync
rather than on the thing under test; and the two non-applying tamper arms above. Each is written into the
PR or the code rather than quietly fixed.

**I amended one commit before pushing** — KS-1143's carried the previous author's numbers, measured on a
base it no longer sits on. A commit body lands on develop permanently.

## STANDING QUESTIONS FOR YOU
1. **The preflight legs.** Four PRs came back 12/15. Start the local stack and re-push, or is
   12/15-nothing-failed the standing verdict for test-only `packages/shared` changes?
2. **`packages/shared` does not declare vitest.** It resolves only from the `Blockchain/Dev` workspace-root
   lockfile, so `npm ci` inside the member installs 7 packages and no `.bin` and the suite exits 127 —
   reads like a broken tree. Out of lane (`package.json`). Ticket?
3. 🔴 **The fuse.** Both audit rows lapse `2026-09-30T00:00Z`. From then `audit:gate` and `audit:locks`
   refuse every `Blockchain/Dev` push — that is #1248, #1249, #1251 and #1254. Kam's own word only.

## STATE
develop unchanged at `6e2a00bfed57`. `.push-lock-24` free — seven takes, each released, cool-off honoured.
Shared checkout `2_Project_Files`: **no pull, no fetch, no commit** all session; `worktree add` only, in my
own namespace. 0 orphaned `login_stub` pids. No container, no database, no port taken. **Nothing deployed.**

Holding for gate verdicts. Records in `5_Project_History/2026-09-25_seatL6/`.

## Seat B 28th READY FOR QA — #1255 KS-1301 (15:07:10Z)
MESSAGE_ID <010001a0d91b2915-eb1ec62a-d8a8-4e8c-8728-927b0216b971-000000@email.amazonses.com>
TEXT_SHA256 093b425936b000e8426b35ce44c83db496950c38f1b833cff1732b9f5a8d3917
#1255 KS-1301 head 59245ff0b11c6b760ba5e2a9daedc5927e915e10 (the READY names it in full; origin read by predict_gate24T2b.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T15:07:10.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 28th): #1255 KS-1301 head 59245ff0b11c — 2 red arms, route isolation measured; PROTOCOL CLEAN
---
READY FOR QA (Seat B 28th): #1255 KS-1301 at head 59245ff0b11c6b760ba5e2a9daedc5927e915e10

## BLUF
Item 3 READY, test-only. #1237's presence-not-truthiness pin ported to /sign-cert and /sign-wallet,
ONE RED ARM PER ROUTE with isolation measured both ways. **This push was PROTOCOL CLEAN** — config
diff 0, and the only ref change was my own tracking ref. Not merged. develop `77c6426b96d9`, my base.

## THE FIVE ARTEFACTS
1. **PR #1255** — https://github.com/Secuura/Distributed_Secuura/pull/1255 (open, base develop, 1 commit).
2. **Head, read from origin in the same action:** `59245ff0b11c6b760ba5e2a9daedc5927e915e10`
   (GET /pulls/1255 -> head.sha, and `ls-remote` agrees). 1 file, +23 −0.
3. **Ticket comment naming the PR:** KS-1301 `2f9b93a6-d32e-4dc2-87c8-ceeb86ba3564`, re-counted 0 -> 1.
4. **Test Evidence: in the PR body, written by me, who ran it.**
5. **NOT covered: below.**

## THE GAP, MEASURED RATHER THAN QUOTED
The relabel guard is **byte-identical at three call sites** in `routes/documents.ts`:
  `:2029` /version  — pinned by #1237 (its QVT cells)
  `:2663` /sign-cert  — unpinned
  `:2932` /sign-wallet — unpinned
So the distinction hardest to get right had no coverage on two of its three call sites. Four cells per
route, as the ticket asked: present `null`, present `''`, present `false`, plus a control proving an
ABSENT documentType is still accepted (201, stored and served as the source type). **The control is
what makes these pin a DISTINCTION rather than a refusal** — without it a guard that refused
everything would pass. Built as one describe per route over the suite's existing WRITERS table.

## ONE RED ARM PER ROUTE, ISOLATION MEASURED
  arm: truthiness at :2663 (/sign-cert)   -> own route 3 red | sibling 0 | #1237 /version QVT 0
  arm: truthiness at :2932 (/sign-wallet) -> own route 3 red | sibling 0 | #1237 /version QVT 0
The tamper is `metadata.documentType && …`. Because the line is byte-identical at all three sites a
content replace would be AMBIGUOUS, so each arm tampers **by line number** with the other two guard
lines asserted unmoved. Every restore sha256-verified; `documents.ts` byte-identical to its pre-tamper
state at commit time (checked against a saved copy, not assumed); untampered re-run 122/122.

⚠ **An instrument correction worth carrying.** My first classifier read route attribution off jest's
`✕` lines. **That line carries the TEST name only, with no `describe` prefix** — so with the route in
the describe title, it reported "0 red for this route, 3 for the other" on BOTH arms. The counts were
right and the isolation claim was unsupported. Re-read from `--json` `fullName` (`describe > test`),
where the route is present. Route isolation was the whole point of the arm, so measuring it off a line
that cannot express the route would have been a false pass with the right-looking numbers.

## RAN
- originate jest `--runInBand`: **877/877, 74/74 suites**, rc 0. Baseline **869** at `77c6426b9` in the
  same worktree; **+8 = 2 routes × 4 cells**, fully accounted. Suite file 114 -> 122.
- `npm run lint` (= `eslint src`): rc 0, 0 errors.
- `tsc --noEmit` rc 0; re-run with `exclude: []` and the edited test file asserted in the program
  (705 files, `--listFilesOnly`) because the project tsconfig excludes `src/__tests__`: rc 0.
- `npm test -w packages/shared`: 47 files / 928 tests, rc 0.
- Push rc 0, 7m46s. STOP count matched exactly: `pre_push_hook_base` 28/0,
  `pre_push_hook_base_fixture_guard` 6/0, shell suites 60/0/0 of 60. No `FIXTURE BUILD FAILED`.

## NOT COVERED
- **Preflight INCOMPLETE — 12/15 legs, 3 SKIPPED** (legs 3, 4, 8; `local stack not up`). None of the
  three bears on a test-only change, but they did not run and I am not rounding that up to a pass.
- No live signing path: the issuer-certs upstream is the suite's loopback stub and CIP-8 verification
  is stubbed true, as elsewhere in this suite. The cells prove the GUARD's shape, not the signing.
- `/version`'s guard is untouched, so #1237's own cells are re-run here, not re-proved.
- No integration/e2e cell; no runtime surface changed.

## PUSH PROTOCOL — CLEAN, for once
Lock taken poll 1, 0 s wait. Snapshot diff: **config 0 lines**, refs **1 line** —
`refs/remotes/origin/feature/ks-1301-…-r24-c-1` at my sha, mine. No foreign ref, no foreign worktree,
nothing on develop. The other two seats were quiet during my window, so there is nothing to attribute.

## SESSION SO FAR
#1246 KS-1312+KS-1298 **MERGED** (develop `14cc526d10ee`) · #1252 KS-1275+KS-1299 **READY** ·
#1255 KS-1301 **READY**. Nothing deployed. Every push matched the STOP count; every preflight read
INCOMPLETE 12/15 with legs 3/4/8 skipped, stated in each PR body.

## NEXT, IN THIS TURN
Item 4: **KS-1159** — the ks1061 shared-mock guard is a text scanner blind to `jest.doMock`, double
quotes and subdirectories (its `testFiles()` is non-recursive). Three red arms, T6b/T6c/T7, per the
gate's own probes. Not ending my turn here.

— Seat B 28th

## Seat L5 DECLARED COUNTS for items 2, 5, 6, 7 (14:46:54Z) — NOT in this batch; context for the next
MESSAGE_ID <010001a0d908983b-1d9957c7-1c7d-497d-a4ec-ed29a0401559-000000@email.amazonses.com>
TEXT_SHA256 1f4cbc97627450525c2b6dff3b73de342bf7ae051e2c7379da1690d9be475393

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T14:46:54.000Z
Subject: [Secuura/Blockchain -> Wednesday] DECLARED COUNTS (Seat L5): items 2, 5, 6, 7 built — 5->7, 16->18, unchanged, 15->16
---
# DECLARED COUNTS (Seat L5) before pushing items 2, 5, 6 and 7 — all four built, all four proved

## BLUF
**All 7 queue items are now BUILT and COMMITTED.** Item 1 merged, item 3 is PR #1250, item 4's
push has the lock right now, and these four are committed and awaiting the lock. Declaring every
count first, as you required — anything else at the push is a STOP.

| item | key(s) | commit | suite it changes | count | preflight |
|---|---|---|---|---|---|
| 2 | KS-1296 | `ff90fbf9d7e3` | `run_migrations_failure_exit_code` | **5 → 7** | RUNS (Blockchain/Dev) |
| 5 | KS-1201 | `d1db0d41ac52` | `bootstrap_login_diagnosis` | **16 → 18** | **SKIPPED** (systemTest-only) |
| 6 | KS-1139 | `62e69d23b250` | none | **all unchanged** | RUNS (Blockchain/Dev) |
| 7 | KS-906 | `8a2a28f50eb3` | `no_tracked_credentials_root` | **15 → 16** | RUNS (Blockchain/Dev) |

**For items 2, 6 and 7 the three fleet-STOP figures are UNCHANGED: `pre_push_hook_base` 28/0,
`fixture_guard` 6/0, shell suites 60/60.** None of them touches a suite in that triple, and none
adds a suite FILE, so the denominator stays 60. Item 5 executes **no preflight leg at all** — the
second of the two you and I predicted — so its READY will name what I ran by hand and will not
quote the triple.

**One thing worth stating for the fleet:** items 2, 5 and 7 change *cells inside* suites that are
**not** in the STOP triple, so when they merge **the fleet STOP count does not move**. Only items
3 (`run_shell_suites` 49→55) and 4 (`fixture_guard` 6→10) change it, and I flagged both already.

## Item 2 (KS-1296) — 5 → 7
Two cells, and `EXPECTED_CELLS` 4 → 6 so the suite's own completeness guard still means something.
- **GREEN 7/0.** **RED on the base: 6 passed, 1 failed** — exactly the new cell 5, and **the run
  took 61 s**, which measures this ticket's own claim that "it costs 60 seconds before it lies".
- Cell 6 is the control that matters and it passes on **both** sides: a `pg_isready` that is
  PRESENT but always refuses must still reach exit 2 and still blame the database. Without it the
  new guard could have swallowed the real case.
- Cell 5 carries its own precondition: on a box that HAS `pg_isready` in `/usr/bin` it cannot test
  a missing binary, and it says so rather than passing quietly.
- Exit 4 is free — measured, the script used 1, 2, 3 only — and its own documented exit-code table
  at `:22-26` gains a fourth row. An undocumented exit code is the next reader's puzzle.
- The retry-shortened copy used by cell 6 has its substitution **verified applied**, because a sed
  that silently matched nothing would make the cell assert about the unmodified script and take a
  minute doing it.

## Item 5 (KS-1201) — 16 → 18, and NO preflight leg
- **Base suite run in place LEAKS EXACTLY 4** — the ticket's number, reproduced.
- **GREEN 18/0 with 0 leaked.**
- **RED, one call site put back inside `$( )`: 14 passed, 4 failed** — the regression cell fails
  and the control still fires. The other 3 failures are B1's banner assertions, which have an
  empty `port` to talk to: the same single defect, not separate ones.
- **The control comes FIRST inside the cell**, because "0 survived" is the shape of zero that
  cannot fail: a stub is started deliberately and the count must read non-zero before the absence
  means anything. Your Seat L4 suspected this predicate was unfalsifiable and the measurement
  refuted it; this now settles it on every run instead of relying on that memory.
- Selection is by the stub's **absolute path**, never the basename and never `pgrep -f`, either of
  which would also match another seat's live stubs and this script's own command line.
- Probe copies had to run from the suite's own directory (`$HERE` resolves `support/`); they were
  named `.probe.sh` so the runner's `*.test.sh` glob cannot reach them, and **removed** — porcelain
  back to exactly my one modified file, 0 probes left.

## Item 6 (KS-1139) — no suite changes; and the honest limit
8 sites → `COUNT=$((COUNT + 1))`. 8 lines changed of 8, **every changed line asserted to be an
arithmetic counter** so a stray edit would show.
- **Per-site, from each file's own bytes: BASE returns non-zero at 8 of 8, HEAD at 0 of 8**, and
  the counter VALUES are identical at every site — the fix changes status, not effect.
- The whole `if/elif/else` region (179-233) runs end to end on both, **driven once per branch**
  (UPDATED / SKIPPED / GENERATED / SKIPPED-when-already-generated), same counts on BASE and HEAD.
- **`sync-secrets.sh` was never executed and `az` was never run.** The region deliberately
  excludes `:177`, the `az keyvault secret show` line. `az` sits first on PATH as a shim that logs
  every call; **the log is EMPTY**, and a deliberate call afterwards makes it read 1 — so the zero
  is a measurement.
- **NOT COVERED, recorded as you ruled:** the errexit DEATH is **UNREPRODUCED-ON-THIS-HOST**,
  cited from bash COMPAT 45. The five-shape table goes in the PR body.

## Item 7 (KS-906) — 15 → 16
The ticket asks three things and **the first is already done**: the explicit precondition it wants
exists at `:200-211` from KS-916 F-02. What remained was to drop the inert `cd` and rename the case.
- **Plus one cell**, because dropping an inert line cannot go red and this would otherwise ship
  with no red proof at all. CASE 6b pins the property the `cd` was gesturing at: the leg's answer
  is independent of the caller's cwd.
- ⚠ **My first CASE 6b could not fail.** It compared `/tmp` with `$WORK/c6` — **both outside any
  repository** — so a cwd-dependent leg would have answered identically from both. It now uses
  `/tmp` and `$HERE` (inside this checkout). **Verified red** against a copy of the leg with
  `-C "$DEV_DIR"` removed: from `/tmp` "not inside a git work tree", from inside the checkout it
  scans the real repo. That arm reds 9 cells because such a leg is fundamentally broken; CASE 6b
  is among them with the right message, which is the point.

## FOUR TIMES THIS ROUND I WROTE A CHECK THAT COULD NOT FAIL
Recording it as a pattern rather than four separate slips, because the countermeasure is the same
one every time and it is not re-reading:
1. item 3's KS-1303 fixture redirected away the pipe it was testing;
2. item 4's cell 7 asserted facts about `grep`;
3. `merge24.py`'s wrong-head arm tampered a key the tool never reads;
4. item 7's CASE 6b compared two cwds that were both outside a repository.
**All four were caught by writing the control, none by re-reading.** Also two arms of item 6's
proof were vacuous before they were honest — Arm C hard-set the very variables its four drives
were supposed to vary, and reported the same branch three times.

## MEANWHILE
**A sequential push driver is starting now as a background job**: item 5 first (it skips the
preflight, so seconds), then 2, 7, 6 — **one push per lock take**, each with the config baseline
read inside the lock. Item 4's push currently holds the lock. READYs follow per PR as each lands.

*Seat L5, 2026-09-25. Evidence: `proof/ks1296_redgreen.out`, `proof/ks1201_redgreen.out`,
`proof/ks1139_prove.out`, `proof/ks906_green.out`, `proof/ks906_red.out`.*
