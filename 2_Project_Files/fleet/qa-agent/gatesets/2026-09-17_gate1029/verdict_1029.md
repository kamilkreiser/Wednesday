auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
QA -> Wednesday: TIER 2 GATE ROUND 1, PR #1029 (KS-1180 part 1, Seat A) @ cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc
Gate 2026-09-17 22:21:30 -> 22:40:32 AEST (close reading); mail built 22:40:55 AEST. Clocks from `date`.
Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1180-1029-cd3580e1f-tier2-r1/report.md (NOT-TESTED.written-first.md at 22:22:27, before any run)

VERDICT: GO WITH FINDINGS on `cd3580e1f` as the delta over its merge-base `20ab16f9a`; the same verdict on my merged tree `38dd44d8c7a4db0a60980e1a120233a12704ac5e` over then-current develop `bb848b8283eb5ee6a6180067315b76f1321e7b6b` (#1030). 1 Polish (P-1029-1, TICKET) + 8 Records. No Blocker, Major or Minor.

BLUF
- The new witness discriminates (MEASURED AT RUNTIME). 34 / 34 rows came out as predicted (17 rows x head + merged tree, whole api-gateway suite each), with 0 VOID, 0 timeouts, 0 load failures and 0 re-runs. All 88 ks1072 reds sit in their predicted class by failure message, and the decoded titles match.
  - Tier 1 answering the hash each cell expects (the #1016 GT2) = 5 WITNESS at head, 0 on the pre-PR blob `4ad1cdcd1`.
  - The new control can fail: deaf listener 1 CONTROL; double read 5 WITNESS + 1 CONTROL.
- What it does NOT prove: "asked once" is not "answered". D-T1-ALSO-READ (tier 1 answers + one discarded anchor-store read) stays green, 56/551 at head and 57/556 merged.
  - My row Q-T2-DISCARD bounds it: asked once, answer discarded, nothing else answers = 5 STATUS reds. So the blind spot needs tier 1 to answer.
  - The message "KS-1180: tier 2 answered…" over-claims: P-1029-1 Polish, closed by KS-1180's tier-1 half.
- develop MOVED TWICE after drafting, into api-gateway:
  - #1028 (KS-744, `middleware/auth.ts` + ks744 test) merged 11:50:57Z.
  - #1030 (KS-1211, vitest lock 4.1.11) merged 12:18:53Z.
  - Items 1 and 3 were re-run on the merged tree.
  - Counts now: develop 57/555 -> head 56/551 -> merged 57/556, all green.
  - All runs used the farmed vitest 4.1.10 (4.1.11 NOT TESTED).

ITEMS 1-6 (plain statements)
1. YES, the ks1072 cells now red AT THE WITNESS whenever tier 2 did not answer because tier 1 did.
   - D-GT2X: 5 WITNESS (`expected []`) on both trees.
   - The seat's GT2: 5 WITNESS.
   - The old source guard stayed green on the same shape (D-GT2X@PRE 0) and on a double read (D-GREREAD@PRE 0).
   - The seat's GT2 does NOT discriminate: D-GT2-SEAT@PRE = 5 OLD-GUARD (`expected 'none' to be 'persisted'`), so its "the #1016 gate's GT2" label is wrong (R-1029-1).
   - The control can fail (D-DEAF-MISS 1 CONTROL; D-DOUBLE-ALWAYS 5W+1C).
   - D-ENV-LIVE: 5 WITNESS while tier 2 answered (over-strict, unreachable today, fails closed; R-1029-2).
   - My own rows:
     - Q-DEAF-HIT: 5 WITNESS (the helper's listener is load-bearing).
     - Q-T2-DISCARD: 5 STATUS, plus 20 other-file STATUS reds.
     - Q-D4-LEAK: 1 STATUS; the leaked listener is counted (2) and later cells stay green.
     - Q-D4-NOLEAK: probe reds `expected 1 to be 2`.
     - So D4 is measured: harmless (R-1029-3).
   - The witness proves tier 2 was ASKED once, not that it ANSWERED (P-1029-1).
2. YES, test-only, and the merge-ins brought only develop.
   - merge-base..head = the ks1072 test only (`4ad1cdcd1` -> `d9c98320e`, +16 -3).
   - patch-id `d99b1ba3c8e1e5f3` is equal for d7e95cd9f..a4dc0d8ee, 20ab16f9a..cd3580e1f and merge-base..head.
   - merge-tree a4dc0d8ee x 81ee4b729 = `02f3ab417` = tree(7553821fc); merge-tree 7553821fc x 20ab16f9a = `5138ce742` = tree(cd3580e1f); 0 conflicts.
   - First-parent diffs = develop's deltas by name set (7 = 7, 17 = 17) AND patch-id (`32ecd72a7f07a0c8`, `6b11d554c180397c`); every brought blob = develop's blob.
   - Second-parent sides = the test only. Controls fired (False x2).
   - No byte came in that develop did not bring.
3. MEASURED.
   - api-gateway vitest: develop `bb848b828` 57/555 · head 56/551 · merged 57/556, 0 failed, 0 pending. The READY's 56/551 holds.
   - tsc --noEmit -p . rc 0 on all 3 trees (it type-checks 0 test files).
   - Test-including program (config OUTSIDE services/, --listFilesOnly shows ks1072 in the program): errors in the ks1072 file develop 1 (TS18046 at (124,10)) -> head 0 -> merged 0.
   - Totals are 33 -> 32 -> 32. The drafter's 31 -> 30 differ by +2 lines (one ks815 TS2345) because config placement changes the visible @types/node (20.19.43 vs 26.1.0); the ks1072 metric is unchanged (R-1029-7).
   - Plant: 2 errors, restored sha-identical. P-1016-2 CLOSED.
   - eslint on the ks1072 test: 0/0 on all 3 trees; the firing control gives @typescript-eslint/no-unused-vars (severity 1).
4. YES.
   - attachmentsForURL(pull/1029) = KS-1180 `contributes` only (controls: pull/1028 -> KS-744, pull/99999 -> 0). Re-read 22:40:05-22:40:24, unchanged.
   - KS-1073 NOT linked (only pull/1005 closes).
   - 0 closing phrases in the title, body, all 3 commit messages and the issue comment (planted controls 1 each).
   - KS-1180 STAYS In Progress on merge. §5f's Done rule concerns runtime-behaviour changes; this PR is test-only.
   - What holds KS-1180 open is its own unfinished scope: the tier-1 half, P-1005-1..4, R-1005-2. No ticket moves to Done.
5. MERGE ADDENDUM below.
6. Schemathesis / Akto (and Playwright / k6): NOT REQUIRED.
   - Measured: the net delta is 1 file under src/__tests__/ (GitHub files API, name set and patch-id).
   - `routes/verification.ts` blob `28fb58343` is identical at head, develop and merged; no route, spec, middleware, config or package byte changes.
   - Neither tool exercises a vitest file.

FINDINGS
- P-1029-1 POLISH (test-claim accuracy). MEASURED (D-T1-ALSO-READ green; Q-T2-DISCARD bounds it).
  - Target: PR message `ks1072…test.ts:128` + PR BLUF "witnesses the tier directly"; TICKET KS-1180 tier-1 half.
  - SHIPS-WITH, disposition TICKET. Oracle: Claims.
- R-1029-1 RECORD, seat evidence: tamper.py's GT2 is not the #1016 GT2 and does not discriminate (D-GT2-SEAT@PRE 5 OLD-GUARD). SHIPS-WITH, no PR action. Oracle: History.
- R-1029-2 RECORD: the listener counts every stub request (D-ENV-LIVE 5 WITNESS while tier 2 answered). Unreachable today: ks864a/ks1195 set ANCHORING_SERVICE_URL but not to this stub, and files are isolated. TICKET.
- R-1029-3 RECORD: a status red leaves postTier2's listener attached (measured; harmless). try/finally would tidy it. TICKET.
- R-1029-4 RECORD: each listener is independently pinned (Q-DEAF-HIT, D-DEAF-MISS); a hit-only URL filter is still unpinned (READ). TICKET.
- R-1029-5 RECORD, Wednesday / merge seat: develop moved (#1028, #1030); addendum counts changed; vitest 4.1.11 untested.
- R-1029-6 RECORD, Wednesday: the drafter's classifier labels OLD-GUARD reds TXHASH (tamper_rows.json D-GT2-SEAT@PRE); the brief's table is right.
- R-1029-7 RECORD, instrument: including-program totals depend on config placement (+2, ks815 only).
- R-1029-8 RECORD, Wednesday: the Secuura checkout .git/config sha256 changed 09959c342094001c -> f9ef2cb7e4b9fa5a (mtime 22:32:42) during the gate; refs 939 -> 940; another writer (my checkout verbs were read-only; none ran at 22:32:42). Not a #1029 matter.

PREDICTION SLIPS
- Wednesday's brief: develop 75ad0e55c -> bb848b828; #1028 open -> landed; compare behind 1 -> 3; addendum "56/550 at develop" -> 57/555. D1 graded RECORD, not Polish. The verdict graded D2 against the message -> GO WITH FINDINGS.
- Drafter: TXHASH class slip (R-1029-6); totals 31 -> 30 instrument-dependent.
- Seat / READY: GT2 mislabel; "witness tier 2" over-claims (P-1029-1). Every numeric claim holds.
- Me: one zsh `=word` echo slip (harmless). 34/34 predictions held.

BOUNDS (checkout, read-only): three readings, start 22:23:08 / mid 22:33:17 / close 22:40:02.
- porcelain 0 / 0 / 0; .git/worktrees 112 / 112 / 112; refs 939 / 940 / 940.
- config 09959c342094001c / f9ef2cb7e4b9fa5a / f9ef2cb7e4b9fa5a.
- branch feature/ks-597-b-caller-scoped-externalref (all three).
- origin develop bb848b828 (all three); refs/pull/1029/head = cd3580e1f = pin (all three).
- api-gateway .vite/vitest mtime 2026-08-17 20:54:28 (all three).
LISTENERS: start 17 LISTEN / 0 node / 0 login_stub.mjs.
- Mid 19: 1 node = my own transient vitest (pid 8401, cwd my merged tree, 127.0.0.1 only).
- Close 18: 1 node = NOT mine (pid 19871, cwd /private/tmp/claude-501/search17o/clone2/…/services/auth; untouched, exited by 22:40:32).
- All sampled node binds during my T0 runs were 127.0.0.1. 0 node processes of mine left; 0 login_stub.mjs started by me.
- docker info rc 0 (run once; no container).

MERGE ADDENDUM
"squash `cd3580e1f` onto develop `bb848b8283eb5ee6a6180067315b76f1321e7b6b` (#1030; `75ad0e55c` at draft) (tree `38dd44d8c7a4db0a60980e1a120233a12704ac5e`; drafter: merged tree `1227ecc82` over `75ad0e55c`); the squash touches exactly ONE file; #1029 attaches to KS-1180 only, linkKind `contributes`, no closes, KS-1073 not linked — KS-1180 stays In Progress on merge (open: the tier-1 half, P-1005-1..4, R-1005-2); equality target after the squash: `services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts` blob `d9c98320e`; api-gateway vitest 57/555 at develop `bb848b828` (56/550 at `75ad0e55c`; develop gained the ks744 file via #1028) -> 56/551 at head -> 57/556 merged (re-measured, vitest 4.1.10 farm); test-including tsc errors in the ks1072 file 1 -> 0 (merged 0; drafter 1 -> 0); dispositions: P-1029-1 TICKET (KS-1180 tier-1 half; SHIPS-WITH), R-1029-1 SHIPS-WITH (seat evidence, no PR action), R-1029-2 TICKET, R-1029-3 TICKET, R-1029-4 TICKET, R-1029-5/-6/-7/-8 Wednesday records; NEW: Q-DEAF-HIT (the helper's listener is load-bearing, 5 WITNESS), Q-T2-DISCARD (asked-once-not-answered reds 5 at STATUS when nothing else answers, so the D2 blind spot needs tier 1 to answer), Q-D4-LEAK/NOLEAK (a status red leaks exactly one listener, harmless), #1028 + #1030 landed into api-gateway (merged tree re-gated: 17/17 rows, 57/556); Records for KS-1180's facts comment at merge: P-1016-1 fixed by the anchor-store witness (discrimination measured: tier-1-answers-the-expected-hash reds 5 at head, 0 at the pre-PR blob, on head and on the merged tree), P-1016-2 closed (measured: the ks1072 TS18046 1 at develop -> 0 at head and merged, plant fired), the witness proves tier 2 was asked once, not that it answered — the open tier-1 half closes that, a status red in `postTier2` leaves its listener attached (harmless; try/finally would tidy it), and the witness counts every stub request, so a live-scan base pointed at the stub would red while tier 2 answered (unreachable today, fails closed)."

NOT TESTED (same prominence as the findings)
- vitest 4.1.11 (develop's new lock): all runs used the farmed 4.1.10; nothing was installed.
- GitHub's actual squash (predicted by merge-tree over bb848b828 only); any develop move after 22:40:32.
- A real anchoring or originate service, any stack/container/edge/browser (KS-535 HOLD). The subject is the in-process harness with loopback stubs.
- Schemathesis / Akto / Playwright / k6: not run (not commissioned; ruled NOT REQUIRED).
- Persona / UI / accessibility / auth-state / network-failure dimensions: NOT APPLICABLE (one server-side test file).
- The ks1073 file and KS-1180's other half: context only.
- Flakiness statistics: one run per row/suite; nothing was noisy, so nothing was re-run.
- A hit-only URL filter in postTier2's listener: READ only.
- The test-including program under the api-gateway-root placement at bb848b828: not run (probe rule).
- eslint beyond the ks1072 test; preflight / pre-push hook / push: not run.

Nothing was pushed, filed, commented or ticked; no Linear/GitHub write; nothing to Peter or Stuart. Clone: /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Testing-Agent-MAIN/c11c3e2d-7bc2-4337-837e-9951238317c2/scratchpad/gate1029_qa_odr3blfl (disposable; probe config quarantined by rename).

