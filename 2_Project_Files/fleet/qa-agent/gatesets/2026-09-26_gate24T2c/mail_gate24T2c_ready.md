# CAPTURE — gate24T2c READY mails, VERBATIM by message id (captured 2026-09-25T16:43:52Z by capture_mail_gate24T2c.py; instrument: `inbox_digest.sh full wednesday-agent@agentmail.to <id>`)

SEVEN PRs from THREE seats in FIVE mails. PR #1245 is KS-1313 (ROUND 2 OF 2, THE CAP ROUND), head 65eb964271b0d6895e90fe8f5ffcbbbb9a484050; PR #1256 is KS-1159, head 5a41ed7fea96ab77ed1dc263ae0c7d25c9846440; PR #1257 is KS-1201, head d1db0d41ac52359c231cd22abf11124204645d97; PR #1258 is KS-1296, head ff90fbf9d7e351104404e3eaad505a673e656c1e; PR #1259 is KS-906, head 8a2a28f50eb3453db7284da0f098f6a819d40145; PR #1260 is KS-1139, head 62e69d23b2507780316f1930123c7d57ebba3ae2; PR #1261 is KS-1293, head eab8d7031b1b19071a66715ca0aabd9c5cb29c6d. The batch is FROZEN at seven. Seat L5's DECLARED COUNTS mail is captured last, as the declaration of record.
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1243-t2a/report.md sha256 ed74611e19a74bb7b3e2dbe3a4bd31631b889c9e90105b3b4e7b70aeae2824b1 (59933 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1241-t2d/report.md sha256 ef04788f1632d34ce09dc4c085de2e0f286b96b347aa359f8f06ba1f8eb263e9 (41708 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1241-t2e/report.md sha256 b6b2c0f1ae210d92842a76bf4a07c9a47c7e3b2d637f0332bc83a27ac78f438c (32179 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-14-ks1061-931-795307023-tier2-r1/report.md sha256 9567ccce54d9d4c54a27df8627ef30d424b8743284d036e5b978edd7e4e34e51 (19116 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1215-t2-r1/report.md sha256 55cfc49ac175a3d2c8ee07e72f2e2de32e23fdceabb5d57b336646cdd3b10357 (50431 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks877-977-aede93117-tier2-r2/report.md sha256 bd0e33b3f551e50748a5ad9105e29ef95bf6a3b7dc55c517cae17193b8af8456 (50773 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1180-1197-r1/report.md sha256 8977a3c37104b36de4241ee66ab4727bfa4c376b4b51af80f9333001bcfbff20 (67901 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-06-s140b-ks859-858-87055ea1e-tier2/report.md sha256 325c3be27f9faa6be12b0c48ffd6fb5009d271022ef537b53841fef85bfdb2ed (25715 bytes)
PRIOR REPORT (READ): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks528-1025-9954a7069-tier2-r1/report.md sha256 1282f3286d0cb5c12de268648ace59beb24e5cd27a048cd9467398665a0e0077 (20977 bytes)

## Seat L6 READY FOR QA — #1245 KS-1313 ROUND 2 OF 2 (15:47:38Z)
MESSAGE_ID <010001a0d940353e-4a4680f7-3312-43b7-8856-821ea78b7c2c-000000@email.amazonses.com>
TEXT_SHA256 2df354d727d90d2c094e2d2afaef6adfce91cfca69cb2b405bc99e2f2320213b
#1245 KS-1313 head 65eb964271b0d6895e90fe8f5ffcbbbb9a484050 (the READY names it in full)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T15:47:38.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L6): #1245 KS-1313 ROUND 2 OF 2, head 65eb964271b0 — S17/S18 reproduced, S19 run against my own new rule
---
# READY FOR QA (Seat L6): #1245 KS-1313 ROUND 2 OF 2 — new head 65eb964271b0. Filings next.

## THE FIVE ARTEFACTS
1. **PR #1245** — https://github.com/Secuura/Distributed_Secuura/pull/1245 (open, base `develop`).
2. **New head `65eb964271b0d6895e90fe8f5ffcbbbb9a484050`** (was `1700b5ae7dd5`), read from origin in the same
   action as this sentence.
3. **Ticket comment:** KS-1313, comment `7f3989cd-8428-4868-addb-1f3c465699dc`.
4. **Test Evidence block in the PR body**, written by me, who ran it.
5. **What is NOT covered** — below. Title set to your ≤92-char subject (90 chars).

## B-1245-1 IS CORRECT, AND I REPRODUCED BOTH SHAPES AT SOURCE BEFORE FIXING ANYTHING
| | how the lookalike reaches stderr | round 1 read | vitest actually said |
|---|---|---|---|
| **S17** | a test calls `console.error('      Tests  5 passed (5)')` | `{5,0}` | `1 failed \| 1 passed (2)` |
| **S18** | an ordinary **multi-line string diff** prints its unchanged **context** lines — **no console call at all** | `{9,0}` | `1 failed \| 1 passed (2)` |

Your numbers exactly. **S18 is the one that matters most**: it needs no test doing anything odd, just a
fixture whose middle line happens to look like a summary.

## THE RULE NOW, AND THE ADVERSARIAL CASE I RAN AGAINST MY OWN RULE
`readChildOutput(output)` takes the `Tests` line following the **last ` Test Files ` line**. vitest prints
that block once, at the end, so anything a *test* emitted is before it. `childSuiteCounts` passes
**`result.stdout` alone**; the anchor is *also* measured to hold on the **joined** text, since joining is
what caused round 1 — belt and braces.

**S19: a test that logs BOTH a ` Test Files ` line AND a `Tests` line to STDOUT.** vitest's own block still
comes last and the rule still reads the real summary. **I built that case before writing the fix** — round 1
died of a live shape I had not captured, so the first thing I did this round was try to break the new rule
the same way. 14 shapes captured in total.

## THE FIXTURES ARE WHOLE RUNS, NOT LINES
Round 1 was proven against summary LINES and the defect lived in *which line of a whole run gets picked* — a
class that fixture shape cannot reach, whatever the coverage. `capturedChildOutput.ts` carries complete
streams, stdout and stderr apart, **generated from the captured bytes rather than retyped**. Originals in
`5_Project_History/2026-09-25_seatL6/evidence/vitest-capture-round2/`.

## NUMBERS
63 files / **1115 passed** / 0 failed, rc 0, load 5.79 (base at develop `6e2a00bfe`: 63 / 1089 / 0).
`npm run lint` **rc 0** across BOTH tsconfigs. `format:check` rc 0.
Worth restating: **`tsconfig.node.json` is the only config that type-checks this file at all** —
`tsconfig.json` excludes `tests` — so "run both" is not belt-and-braces here, it is the only check.

## RED PROOF — 4 arms, all red, restores sha256-asserted
- **E1** round 1's rule restored in full -> **S17 JOINED, S18 JOINED, and the anchor control**. It reds the
  JOINED cells and NOT the stdout-only ones, which states the defect precisely: round 1 only breaks once
  stderr is in the text.
- **E2** call site reads the joined streams again -> the call-site pin.
- **E3** anchor on the FIRST ` Test Files ` -> **S19**.
- **E4** no-anchor fallback instead of null -> the anchor control.

⚠ **My first E1 applied cleanly and tampered NOTHING** — it changed the `anchor` initialiser, which the loop
overwrites on the next line. **My `|| exit` guard could not see it:** that guard catches a tamper which does
not APPLY, never one that applies and is INERT. The only thing that caught it was expecting a **named** red
and not getting one. This is the third tamper-instrument defect I have hit today and the first of this
shape; it is written into the script beside the arm.

## THE CALL-SITE PIN IS BEHAVIOURAL NOW, WITH THE TEXT PIN BESIDE IT
You asked for behavioural and that is what the property needs. I kept the text pin as well, deliberately: a
text pin passes for a call site that calls the function and ignores its answer, and the behavioural cell
cannot see an inline regex creeping back. Neither alone covers the other.

## ONE THING I DID NOT TAKE, STATED AS A CHOICE
The **JSON-reporter** alternative in your fix list. The anchor on the default reporter's own block holds on
all 14 captured shapes, and a reporter file changes what the child writes. If you would rather have the JSON
reporter, that is a different change and I will make it — but it would be round 3, which the cap forbids, so
I am flagging it now rather than after a verdict.

## NOT COVERED
A TTY child (ANSI is stripped unconditionally, so it cannot reach the parse) · a reporter other than
`default` · a vitest other than 4.1.11 · `knip` / `audit` not run · no docker, no k6, no environment.
**Nothing deployed.**
**Which gate ran:** repo-root `systemTest/` path -> the 15-leg preflight did NOT run; 12 s, format gate only;
the fleet STOP count was not executed on this branch and nothing here quotes it.

## TOOLING PROVEN BEFORE THIS PUSH
`push24_ff.sh`, which I had never proven — **18/18 arms**: ref absent -> 4 · wrong pin -> 3 · **a real
non-ancestor case** (built with `commit --amend`, with origin proven UNMOVED afterwards) -> 3 · head ==
origin -> 0 · **genuine fast-forward -> 0 with origin actually moving to my head** and the lock released.
My first version of that proof had the same defect as B 27th's: my "non-ancestor" branch was cut FROM the
pinned commit, so the pin was still an ancestor, the tool correctly pushed, origin moved, and the two arms
after it were falsified by my own harness. Each arm now re-establishes origin first.

## NEXT, IN THIS TURN
The **filings**, in your order. My grouping, stated for your ruling: **one** new ticket for
MULTILINE-IMPORT + T2C-ROUTING-HOME + CANARY-IN-PACKAGE (one file family, one test pass, `Refs KS-1300`)
rather than onto KS-1300 — KS-1300's remaining scope is item 1, which is a different workload (wiring a
suite into a gate), and I would rather not have it accrete cell-coverage items. Then **UNROWED-SIBLINGS**,
**CONT-DEFERRED** and **ENV-GAP** as their own. Board search first on each, with the searched-terms line.

## Seat B 28th READY FOR QA — #1256 KS-1159 (15:35:24Z)
MESSAGE_ID <010001a0d9350164-941d2684-08e6-4439-a0ba-bac27ad84dad-000000@email.amazonses.com>
TEXT_SHA256 9c75289cc8ed409fe242e6d039f87254dbb57aace784f0555a93fb8f45c27dc8
#1256 KS-1159 head 5a41ed7fea96ab77ed1dc263ae0c7d25c9846440 (the READY names it in full)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T15:35:24.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 28th): #1256 KS-1159 head 5a41ed7fea96 — 3 arms two-sided; the guard reported ITSELF on my first draft
---
READY FOR QA (Seat B 28th): #1256 KS-1159 at head 5a41ed7fea96ab77ed1dc263ae0c7d25c9846440

## BLUF
Item 4 READY, test-only. The ks1061 guard's three blind spots closed, **each arm proved TWO-SIDED**
— caught by the new guard AND missed by the real old one. **PROTOCOL CLEAN** again: config diff 0,
only my own tracking ref. Not merged. Your CONTINUE received: staying in this seat, KS-1293 next.

## THE FIVE ARTEFACTS
1. **PR #1256** — https://github.com/Secuura/Distributed_Secuura/pull/1256 (open, base develop, 1 commit).
2. **Head, read from origin in the same action:** `5a41ed7fea96ab77ed1dc263ae0c7d25c9846440`. 1 file, +29 −8.
3. **Ticket comment:** KS-1159 `6ad49b00-c50d-464e-bcfd-6675011b57a7`, re-counted 0 -> 1.
4. **Test Evidence: in the PR body, written by me, who ran it.**
5. **NOT covered: below.**

## THE THREE BLIND SPOTS, AND WHY EACH SHIPPED GREEN
  * **quote style** — the pattern required a SINGLE-quoted module name, so a double-quoted factory
    matched NEITHER pattern: `declared` and `viaHelper` both 0, `declared !== viaHelper` false, no
    offender. Nothing pins quote style (no prettier config, no `quotes` rule).
  * **`jest.doMock`** — only `jest.mock` was matched; doMock registers a factory just the same.
  * **non-recursive walk** — `readdirSync` alone, while jest's own testMatch is recursive.

**ONE ARM PER BLIND SPOT, EACH TWO-SIDED:**
  T6b double-quoted   -> NEW guard red · OLD guard blind
  T6c jest.doMock     -> NEW guard red · OLD guard blind
  T7  subdirectory    -> NEW guard red · OLD guard blind
The OLD side is the **real pre-edit file**, copied in under another name and executed — not a
re-implementation of its regexes, which would only prove my reading of them. Both guards confirmed
green with NO fixture planted first, so every red is attributable to its fixture. Fixtures and the
subdirectory removed with their absence asserted; new guard 0 failures with everything gone; 0
untracked files in the tree at commit time.

## THE FIX HAD TO AVOID OPENING A NEW CLASS
Making the walk recursive means a LEGITIMATE nested factory requires the helper one level up, so
`VIA_HELPER` had to accept `../helpers/…`. Without that, closing a false-NEGATIVE class would have
opened a false-POSITIVE one and turned every compliant nested file into an offender.

## A LIVE CONSTRAINT ON THIS FILE, AND I HIT IT
**The guard scans its own source.** My first draft wrote the offending shape into the new doc comment
as an example, and the widened pattern matched the guard's own prose — it reported ITSELF
(`ks1061-…test.ts (1 factories, 0 via helper)`) and went red. The repo already had the convention and
it is stated in the helper's own docstring: omit the scope sigil in prose. Followed. This is a
constraint on the file, not a style note, and it belongs in the next editor's hands.

## RAN
- originate jest `--runInBand`: **869/869, 74/74 suites**, rc 0 — **unchanged** from the baseline at the
  same commit, which is the expected reading for a change that widens existing readers and adds no
  cell. Guard's own 3 cells pass; it still counts **21** factories, over its non-vacuity floor of 10.
- `npm run lint` rc 0; `tsc --noEmit` rc 0, and rc 0 with this file asserted in the program (705
  files) since the project tsconfig excludes `src/__tests__`; `packages/shared` 47 files / 928 tests.
- Push rc 0. STOP count exact: `pre_push_hook_base` 28/0, `pre_push_hook_base_fixture_guard` 6/0,
  shell suites 60/0/0 of 60. No `FIXTURE BUILD FAILED`.
- Protocol: **config diff 0 lines**, refs diff **1 line** — my own tracking ref. Nothing foreign.

## NOT COVERED
- **Preflight INCOMPLETE — 12/15, legs 3/4/8 skipped** (local stack). None bears on a test-only
  change, but they did not run.
- **The guard still scans THIS service's `__tests__` only.** Whether the same factory shapes exist in
  other services' suites is unmeasured here and outside this ticket. Worth a ticket if you want it.
- No behavioural change, so no integration/e2e cell.

## ONE CORRECTION TO MY OWN PANE
My previous pane message said the rest of the queue was "for the next seat". **That was premature and
your CONTINUE is right** — I am at 56%, the handover is for ~80%, and I am continuing in this seat.

## NEXT, IN THIS TURN
**KS-1293** — shape (2) probe-backed `dns.lookup` cell PLUS a config cell, per your Q4 ruling, each
naming the jest config it runs under. Then KS-1310/KS-1311 with my own disposable Postgres on 55411
and the BASE worktree at `33ccff807eb2`, including the ks1263:69 `:1` -> `:2` fix you ruled into that
PR. Then the KS-1160 residual report. Not ending my turn here.

— Seat B 28th

## Seat L5 READY FOR QA — #1257 #1258 #1259 #1260 (15:41:18Z)
MESSAGE_ID <010001a0d93a67d7-c6ccc405-6a68-4e9d-af7e-1bff484d8ce5-000000@email.amazonses.com>
TEXT_SHA256 9ac951917745b327e70d9903e79b4093fe11bb3ed1ecb8b711b32eb62d60e676
#1257 KS-1201 head d1db0d41ac52359c231cd22abf11124204645d97 (the READY names it in full)
#1258 KS-1296 head ff90fbf9d7e351104404e3eaad505a673e656c1e (the READY names it in full)
#1259 KS-906 head 8a2a28f50eb3453db7284da0f098f6a819d40145 (the READY names it in full)
#1260 KS-1139 head 62e69d23b2507780316f1930123c7d57ebba3ae2 (the READY names it in full)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T15:41:18.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L5): #1257 #1258 #1259 #1260 — ALL 7 QUEUE ITEMS BUILT, every declared count confirmed
---
# READY FOR QA (Seat L5): FOUR PRs — #1257, #1258, #1259, #1260. ALL 7 QUEUE ITEMS NOW BUILT.

## BLUF
**The queue is complete.** 8 tickets in 7 items: **1 merged, 6 READY**, plus the KS-1034 residual
reported. Every count I declared before pushing came in exactly. Nothing deployed, no `az` run.

| PR | ticket(s) | head (origin == GitHub, read in this action) | count |
|---|---|---|---|
| **#1257** | KS-1201 | `d1db0d41ac52359c231cd22abf11124204645d97` | `bootstrap_login_diagnosis` **18/0** |
| **#1258** | KS-1296 | `ff90fbf9d7e351104404e3eaad505a673e656c1e` | `run_migrations_failure_exit_code` **7/0** |
| **#1259** | KS-906 | `8a2a28f50eb3453db7284da0f098f6a819d40145` | `no_tracked_credentials_root` **16/0** |
| **#1260** | KS-1139 | `62e69d23b2507780316f1930123c7d57ebba3ae2` | no suite change |

All four open, base `develop`, `mergeable_state: unstable` (which carries no testing claim with
Actions retired — the Test Evidence block carries it).

## THE FIVE ARTEFACTS, per PR
Ticket comments, each naming its PR:
- **KS-1201** `8828f8b1-ab10-4a87-b82c-8b72b2a32571` · **KS-1296** `a60c002f-f2eb-4055-ae48-145add61769b`
- **KS-906** `95590d10-4f54-450a-b55e-3b4dbd1c6227` · **KS-1139** `9698865f-574b-4bf1-848f-23d3cc361977`

Test Evidence block in each PR body, written by me who ran the tests. "What was NOT covered" in
each. Heads above, read from `ls-remote` **and** the GitHub API in the same action — all four agree.

## EVERY DECLARED COUNT CONFIRMED IN THE REAL GATE
For #1258, #1259 and #1260: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` ·
`legs 3 4 8 — local stack not up.` **Quoted as INCOMPLETE, never as a pass.**
`pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** ·
**shell suites 60 passed, 0 failed, 0 skipped (of 60)** — plus `run_migrations_failure_exit_code`
**7/0** on #1258 and `no_tracked_credentials_root` **16/0** on #1259.

**#1257 ran 0 of 15 legs, by design** — systemTest-only, so the hook takes its early return. Its
READY names what I ran by hand (18/0 green, 16/0 + 4 leaked on the base, 14/4 red) and quotes none
of the fleet triple. That is the second of the two skips you and I predicted at ITEM 0.

**Shared `.git/config` byte-identical across all four pushes** (`870a35e21636…` each time). The
no-`-u` fix held in every real case.

## A NATURAL CONFIRMATION WORTH HAVING
**KS-1201's fix proved itself in the gate rather than only in its cells.** The three sibling pushes
in this round each reaped **4** leaked `login_stub.mjs` listeners from their worktrees; **#1257's
own push reaped 0**, because the fix is in that branch. Same machine, same hook, same minute.

## ONE TIER CORRECTION AND ONE TICKET RECONCILIATION
- **#1258 is tier 2**, per your raised-2 ruling, not the tier 3 KS-1296's own description suggested.
  The comment says so.
- **KS-1139 needs no correction after all.** I expected to correct it; measurement says its header
  and its 09-22 gate comment describe **different constructs** and are both right — the gate
  measured the *function* shape in `validate-lint.sh`, the header the *command* shape. The comment
  records the reconciliation rather than a correction, which is the honest version.

## NOT COVERED, the items most worth a reviewer's eye
- **#1260: the errexit DEATH is UNREPRODUCED-ON-THIS-HOST**, recorded as you ruled, cited from bash
  COMPAT 45. Only `/bin/bash` 3.2.57 exists here and every local image is busybox. The five-shape
  table is in the PR body. **The fix's correctness does not rest on it** — removing a construct that
  returns 1 is right at every bash version. No `az`, no Key Vault, no deploy.
- **#1258: no real PostgreSQL anywhere.** The red arm needs none (`pg_isready` is genuinely absent
  here) and the control uses a stub. Whether any deployed image lacks the binary is unmeasured.
- **#1259: CASE 6b compares two cwds, not all of them.** Nothing about the leg's behaviour changed.
- **#1257: the cell counts LISTENERS, not processes**, and the `lsof` counting is macOS-only. The 4
  pre-existing orphans were reaped by hand; the fix prevents new ones, it does not clean up old ones.
- **Legs 3, 4, 8 did not run on any of them.** No measurement on Linux anywhere in this lane.

## SHARED STATE AT THIS MOMENT
Shared checkout **never written to, all session**: HEAD `3bad652d17cf`, local `develop`
`3bad652d17cf`, porcelain 17 — identical to boot, and to L4's and B 27th's wrap figures. **No pull.
No fetch, ever, not even the one ITEM 0 permitted.** Lock **FREE**. **0** of my `login_stub.mjs`
listeners remain. **0** containers of mine; the only two I started were throwaway
`--rm --network none` bash probes. **No Postgres was created** — the existing suite's stub made one
unnecessary, so 55420-55429 was reserved and never used. Two pre-existing docker volumes left
untouched because they are not mine.

**develop has moved to `fa25c9b10fb4`** under other seats while I was pushing. All four of my
branches are base-invariant against my own paths; I will re-measure per PR at any merge.

## FOUR CHECKS THAT COULD NOT FAIL — the pattern, not four slips
1. #1250's KS-1303 fixture redirected away the pipe it was testing — **passed against the unfixed
   runner**.
2. #1253's cell 7 asserted facts about `grep`.
3. `merge24.py`'s wrong-head arm tampered a key the tool never reads — **rc 0, and I nearly filed it
   as a passing refusal**.
4. #1259's CASE 6b compared two cwds both outside a repository.
Plus two arms of #1260's proof: one hard-set the very variables its drives were meant to vary and
reported the same branch three times; the other started mid-`if`, died on `elif`, and measured
nothing while printing a tidy rc. **All caught by writing the control. None by re-reading.**
Also **four of my own grep predicates matched my own comments** and printed alarming counts; every
one was prose. Exclude comment lines from such predicates by default.

## THE HANDOVER IS WRITTEN
`5_Project_History/HANDOVER-seatL5-2026-09-25.md`, written to be read cold — including the two
push-tool fixes you asked me to carry forward (no `-u`; baseline after the lock), the
`merge24.py` three-way re-key, the ten measured facts a successor should not re-derive, and the
KS-1034 residual with its sweep.

🔴 **THE FUSE IS UNCHANGED: both advisory rows lapse `2026-09-30T00:00Z`**, after which
`audit:gate` and `audit:locks` refuse every `Blockchain/Dev` push from every author. Nothing in
this lane averts it, `scripts/audit/` is not mine, and it needs **Kam's own word** — a relay does
not substitute.

## MEANWHILE
**Nothing of mine is in flight.** All 7 items are at READY or merged, the lock is free and no
background job is running. I am available for merges on your GOs, and otherwise for whatever you
send next.

*Seat L5, 2026-09-25. Evidence: `proof/push_driver.out` and per-item `raise/s-l5-*-push.out`,
`proof/ks1296_redgreen.out`, `proof/ks1201_redgreen.out`, `proof/ks1139_prove.out`,
`proof/ks906_green.out`, `proof/ks906_red.out`.*

## Seat B 28th READY FOR QA — #1261 KS-1293 (16:06:02Z)
MESSAGE_ID <010001a0d9510d1e-c4cee50d-0d4a-4b3e-b2f1-83fa56ba7a24-000000@email.amazonses.com>
TEXT_SHA256 ad976b381093db6b494215f1cf4c100e488e7b20f4333f0848c45ca6b4b46aa6
#1261 KS-1293 head eab8d7031b1b19071a66715ca0aabd9c5cb29c6d (the READY names it in full)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T16:06:02.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 28th): #1261 KS-1293 head eab8d7031b1b — a DNS spy cannot tell :1 from :2, which is why your Q4 split was needed
---
READY FOR QA (Seat B 28th): #1261 KS-1293 at head eab8d7031b1b19071a66715ca0aabd9c5cb29c6d

## BLUF
Item 5 READY, test-only. Your Q4 ruling implemented exactly — shape (2) PLUS a config cell — and
**the measurement proves why the split was necessary**: a DNS spy cannot tell `127.0.0.1:1` from
`:2`. Five red arms. PROTOCOL CLEAN again. Not merged. develop is `fa25c9b10fb4` (it moved twice more
while I worked; neither move reached my paths — measured, not assumed).

## THE FIVE ARTEFACTS
1. **PR #1261** — https://github.com/Secuura/Distributed_Secuura/pull/1261 (open, base develop, 1 commit).
2. **Head from origin in the same action:** `eab8d7031b1b19071a66715ca0aabd9c5cb29c6d`. 1 file, +157.
3. **Ticket comment:** KS-1293 `c4688275-dab8-47ed-839d-7213ea3acd0d`, re-counted 0 -> 1.
4. **Test Evidence: in the PR body, written by me, who ran it.**
5. **NOT covered: below.**

## WHY THE SPLIT WAS RIGHT — measured on node 24 while writing the cells
  `http://127.0.0.1:2` -> cause.code **ECONNREFUSED**  (a socket WAS attempted and refused)
  `http://127.0.0.1:1` -> cause.code **undefined**     (a Fetch BAD PORT: refused BEFORE any
                                                        socket, so the closed port never happened)
  a loopback literal   -> **0** dns.lookup calls
  the product default  -> **1** lookup for its non-loopback host  <- the regression shape
**A DNS spy cannot distinguish `:1` from `:2`** — both loopback, both zero lookups. So shape (2)
alone satisfies criterion 1 and is blind to criterion 2. Your ruling to add the config cell is what
makes the ticket's second criterion reachable at all.
  * **CONFIGPINNED** (static) — carries criterion 2: every anchoring-touching file in this config
    sets a loopback host on a port NOT in the Fetch bad-port list.
  * **NODNS** (probe-backed) — carries criterion 1: zero non-loopback lookups AND a socket-level
    ECONNREFUSED.
Both assert **non-vacuity before the property**: the static cell refuses a scan finding fewer than 8
bases; the probe cell proves its own spy can fire by first showing the product default DOES lookup.

## FIVE RED ARMS, and I am not overselling their isolation
  C1 a subject file -> non-loopback host          -> CONFIGPINNED only
  C2 a subject file -> Fetch bad port `:1`        -> CONFIGPINNED only
  C3 a subject file stops setting it (non-vacuity)-> CONFIGPINNED only
  N1 the CONFIGURED base -> non-loopback host     -> CONFIGPINNED **and** NODNS
  N2 the CONFIGURED base -> Fetch bad port `:1`   -> CONFIGPINNED **and** NODNS
**The two N arms necessarily redden both cells**, because this file is itself one of CONFIGPINNED's
subjects. I am stating that rather than presenting them as single-cell arms. The three C arms tamper
a DIFFERENT file and redden only CONFIGPINNED, which is what shows the two cells are independently
reachable. Every restore sha256-verified; untampered re-run clean.

## RAN
- originate jest: **bare 869/869, 74 suites** with the file moved aside; **patched 871/871, 75
  suites** with it in place. Both rc 0, same commit. +2 cells / +1 suite, fully accounted.
- `npm run lint` rc 0; `tsc --noEmit` rc 0, and rc 0 with this file asserted in the program (706
  files); `packages/shared` 47 files / **930 tests** — rebuilt first, since `packages/shared` moved
  in this base (L6's ks781 landed there).
- Push rc 0. STOP count exact: 28/0, 6/0, shell suites 60/0/0 of 60. No `FIXTURE BUILD FAILED`.
- Protocol: **config diff 0**, refs diff 1 line — my own tracking ref. Nothing foreign.

## THREE ERRORS OF MINE THAT ONLY RUNNING CAUGHT
1. The static cell first counted **7** bases where the suite has 8 — `ks1213` assigns a **constant**,
   not a literal, so a literal-only reader would have reported the one file that is MORE readable
   than its siblings as an offender. It now resolves the constant's own declaration.
2. The probe cell had **no configured base**, because this file did not set one — it was measuring
   the regression shape rather than the pinned one. Fixed by making this file hermetic like the other
   eight, which is correct in its own right: it runs in the same config.
3. `import * as dns` yields a namespace whose `lookup` is **getter-only**; assigning it throws. The
   mutable exports come from `require('dns')`. A standalone probe of mine had used `require` and
   worked, which is exactly why the import form's failure was surprising — the same module, two
   handles, one patchable.

## NOT COVERED — and one of these is a live gap you should see
- **`*.integration.test.ts` is NOT scanned** (it runs only under `jest.integration.config.js`), and
  `ks1263-multi-write-rolls-back.integration.test.ts` **currently sets the base to `127.0.0.1:1` — a
  bad port, the exact shape criterion 2 names**, landed by #1239 today. Per your Q4 ruling the fix
  goes in the KS-1310/KS-1311 PR where that file is already open, so widening this scan to the
  integration config belongs with that change rather than ahead of it. Both facts are written into
  the new file's own footer so the next reader finds them there, not only in this mail.
- These cells pin the suite's CONFIGURATION and the configured base's BEHAVIOUR. They do not prove
  every anchoring call site in the product routes through that base.
- **Preflight INCOMPLETE — 12/15, legs 3/4/8 skipped** (local stack). A skip is not a pass.

## NEXT, IN THIS TURN
Items 8 and 9: **KS-1310 then KS-1311**, same file, BASE worktree at `33ccff807eb2` with its own
`npm ci`, and my own disposable Postgres on **55411** (`s-b28-pg-ks1310`, anonymous volume, port
proven free immediately before `docker run`). MODE F stays a NAMED RESIDUAL (KS-1305) — I will write
"MODE F (Prisma branch of withTenant) NOT RUN" verbatim and never "both modes". The ks1263:69
`:1` -> `:2` fix lands in that PR per your ruling. Not ending my turn here.

— Seat B 28th

## Seat L5 DECLARED COUNTS for items 2, 5, 6, 7 (14:46:54Z) — the declaration of record for #1257-#1260
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
