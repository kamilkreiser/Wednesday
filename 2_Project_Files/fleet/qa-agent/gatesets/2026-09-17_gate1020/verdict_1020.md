SUBJECT: [QA -> Wednesday] TIER 2 GATE #1020 (KS-769) 71bd80a35 — GO WITH FINDINGS
FROM: CoAgent <coagent@agentmail.to>
TS: 2026-09-17T06:20:56.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

QA TIER 2 GATE, ROUND 1: Secuura/Blockchain PR #1020 (KS-769), head 71bd80a35b406b9c99c7b96955a7521032d33c20
Session 16:02:44 to 16:19:22 AEST (from `date`). Verdict mail sent 2026-09-17 16:20:54 AEST (06:20:54Z); pre-send re-read in the send script: ls-remote refs/pull/1020/head = 71bd80a35…, develop = d7e95cd9f…, attachmentsForURL(pull/1020) = [KS-769 contributes].

VERDICT
- On 71bd80a35: GO WITH FINDINGS.
- On the merged tree (head onto develop d7e95cd9f153e9036ed77935a73c93504fa6e3dc, still origin develop at 06:18:06Z): GO WITH FINDINGS. Merged tree 4d406fb1c8421dace115e013c06348b21b0998d4 == head tree.
- No finding is against #1020. F1 targets TICKETS. F2 targets pre-existing preflight summary text.

BLUF
- #1020 changes exactly one value, '2026-09-17' -> '2026-10-19', plus 4 comment lines. Measured through the shipped code:
  - base is red on legs 5 and 7; head is green;
  - the fuse is live through 2026-10-18T23:59:59.999Z and lapses at 2026-10-19T00:00:00.000Z = Mon 19 Oct 11:00 AEDT, which is 11 h 00 m after the end of Sunday 18 Oct in Sydney;
  - '2026-10-19' is the earliest YYYY-MM-DD value that keeps all of Sunday live. '2026-10-18' dies Sun 11:00 AEDT, 13 h early (measured). So the value matches the ruling as you read it. The "end of Sunday" wording is a RECORD.
- F1 (Major, TICKETS KS-1024 + KS-763, then KS-528, KS-530, KS-729):
  - From 2026-09-24T00:00Z = Thu 24 Sep 10:00 AEST, preflight leg 6 (audit-gate rc 1, 9 LAPSED) and leg 7 (audit-locks rc 1, 10 LAPSED) refuse every push touching Blockchain/Dev.
  - From 2026-09-30T00:00Z = Wed 30 Sep 10:00 AEST: 14 and 15 LAPSED.
  - Leg 5 and lock-discovery stay green. The 1 ms-before controls are green.
  - #1020 neither causes nor worsens it: audit-baseline.json is byte-identical base vs head.
- F2 (Minor, preflight.sh:688-702 KS-991 branch; pre-existing, blob identical base/head; NOT #1020):
  - When leg 1 cannot run, the closing verdict says "an environment condition, not a finding about your change" even when legs 5 and 7 really failed (measured at base).
  - Replicated in the drafter's GS/out/P_preflight_base.out.

ITEMS 1-8
1. Red-proof (own clone, node v24.7.0, spec reporter "ℹ" lines).
   - base d7e95cd9f: lock-discovery 10/5/5 rc 1; audit:contract 59/49/10 rc 1; audit-locks rc 3 "expires 2026-09-17 — the fuse has LAPSED"; audit-gate rc 0.
   - head: 10/10/0; 59/59/0 (= expected-case-count 59); audit-locks rc 0, "43 standalone lockfiles (45 tracked … 45 - 1 - 1 = 43)"; audit-gate rc 0.
   - The 5 lock-discovery reds, and the 5 extra gate-exit-codes reds, are exactly the names the drafter listed (full names in the report §1).
   - Tampers at head, text anchor count 1, sha256 restored to 8f0b073a4e11… after every row, porcelain 0:
     - T1 '2026-09-17': 5 fail, locks rc 3, contract 10 fail.
     - T2 '2026-09-16': 5 fail, rc 3.
     - T3 'soon': 5 fail, rc 3 "not an ISO".
     - T4 '2026-09-18': green.
     - T5 comment removed: green.
   - My own tampers:
     - Q1a '2026-10-18' at 2026-10-17T23:59:59.999Z: live (locks rc 1 = baseline rows, not 3).
     - Q1b '2026-10-18' at 2026-10-18T00:00Z (Sun 11:00 AEDT): 5 fail, locks rc 3 LAPSED.
     - Q1c CONTROL, head value at the same instant: 10/10/0, rc 1 not 3.
     - Q2 '2026-10-19 ' (trailing space): 5 fail, rc 3 "not an ISO".
   - All measured = predicted.
2. Clock through the code.
   - Argument: isLapsed(REAL,'2026-10-18') false, '2026-10-19' true. Control {expires:'2026-10-18'} on '2026-10-18' true.
   - Process clock: my own preload (NODE_OPTIONS --import, frozen no-arg Date/Date.now, per-process log).
     - Controls: 2020-01-01 -> utcToday 2020-01-01, and a spawned child sees it. The log shows the lock-discovery.test.mjs worker and the audit-locks.mjs process "applied".
     - At 2026-10-18T23:59:59.999Z (Mon 10:59:59.999 AEDT): utcToday 2026-10-18, validateOutOfScope passes, lock-discovery 10/10/0, locks rc 1 (18 baseline rows), NOT rc 3.
     - At 2026-10-19T00:00:00.000Z (Mon 11:00:00 AEDT): utcToday 2026-10-19, THROWS LAPSED, lock-discovery 10/5/5 (same 5 names), locks rc 3 "expires 2026-10-19 — the fuse has LAPSED".
   - Sydney conversions: zoneinfo and BSD date TZ=Australia/Sydney agree. AEDT from Sun 4 Oct.
3. Nothing else changed.
   - 1 commit, 1 file (whole repo). Blob 2f54840ce -> 3dd903b52.
   - numstat = -w numstat = 5 1. The plain and -w patches are byte-identical (cmp). Control: a whitespace-only change differs under -w.
   - esbuild whitespace-minified, comment-free parse: exactly one span differs, "09-17" -> "10-19". Control: literal put back = IDENTICAL to base. Control: a one-char ticket change is detected.
   - Runtime: reason and ticket IDENTICAL.
   - audit-baseline.json, baseline-contract.mjs, expected-case-count, all other scripts/audit and scripts/preflight files, and .githooks/pre-push are blob-identical.
4. Real preflight.sh, whole, in my own clone's worktrees (GATEWAY_URL=http://127.0.0.1:1, curl rc 7), online.
   - head (rc 1, 351 s):
     - leg 5 "OK — 59 audit-contract cases pass (expected 59)"
     - leg 6 "OK — no advisories outside the triaged baseline"
     - leg 7 "OK — no standalone-lock advisories outside the triaged baseline"
   - base (rc 1, 273 s):
     - leg 5 "FAIL — the audit-contract suites are red…"
     - leg 6 OK
     - leg 7 "FAIL — the lock-advisory gate REFUSED to report a verdict" (fuse LAPSED)
   - Both trees: legs 3/4/8 SKIP (stack), legs 2 and 9–13 and 15 OK, leg 1 DEPS MISSING, and leg 14 FAIL "packages/shared is not built" plus ks949 FAILED. Legs 1 and 14 fail from the environment (fresh worktree, no install), identically on both trees.
   - The PR moves exactly legs 5 and 7 from FAIL to OK. No leg 5-7 SKIPPED.
5. Fuse census (JSON parse of audit-baseline.json plus git grep over Blockchain/Dev/scripts).
   - 21 dated baseline rows plus this PR's entry. 15 lapse within 14 days:
     - 2026-09-24: 10 rows (KS-1024 x7, KS-763 x3);
     - 2026-09-30: 5 rows (KS-528 x3, KS-530, KS-729).
   - Measured at head under the process clock, live registry:

     | clock | audit-gate | audit-locks | audit:contract | lock-discovery |
     |---|---|---|---|---|
     | 09-23T23:59:59.999Z (control) | rc 0 | rc 0 | 59/59/0 | 10/10/0 |
     | 09-24T00:00Z | rc 1, 9 | rc 1, 10 (+ colord GHSA-2wm5-q62r-hmrv) | 59/59/0 | 10/10/0 |
     | 09-29T23:59:59.999Z | rc 1, 9 | rc 1, 10 | 59/59/0 | 10/10/0 |
     | 09-30T00:00Z | rc 1, 14 | rc 1, 15 | 59/59/0 | 10/10/0 |

   - The 09-24 pair was replicated with a corrected preload (npm really on the real clock): identical.
   - Leg 5 stays green because gate-exit-codes drives the gates through AUDIT_BASELINE_PATH fixtures and a stub (READ). No contract case reads the real rows' expiries.
   - Hook READ: pre-push runs preflight when the diff touches Blockchain/Dev and exits 1 on a preflight FAIL.
   - Target: the tickets, not #1020.
6. Merged tree: develop still d7e95cd9f (ls-remote 06:03, 06:05 and 06:18Z; branches API). merge-tree --write-tree gives 4d406fb1c… == head tree. Control: develop with develop gives the develop tree. No separate re-run needed.
7. linkKind, re-read 06:18:06Z and again by the send script immediately before this POST (result below):
   - attachmentsForURL(pull/1020) = exactly KS-769 (In Progress, completedAt null) contributes. Control pull/99999 = 0.
   - Closing-phrase regex (controls "Fixes KS-769", "closes #12" and "Resolved: KS-1" hit; "Refs KS-769" does not) found 0 hits in the title, body, commit message, 1 linear[bot] comment, 0 review comments and 0 reviews.
   - The ruling is ON KS-769: comment bb69813e 05:30:26Z "Kam ruled this ticket dormant: 'Dormant but kept'". It records the value '2026-10-19', 11:00 AEDT, and "13 hours early".
8. Disjointness (PR files API, 06:06Z and 06:18Z, identical): 21 open PRs, and none of the 20 others (incl. #1018 267bd8624 2 files, #1019 8b8996f8b 3 files) shares a file or touches scripts/audit/, scripts/preflight/ or .githooks/pre-push.

RECORDS
- R1 (correction to brief D3, Wednesday's input): GS/fakeclock.mjs does NOT leave npm on the real clock on this host.
  - Measured: QA_FAKE_ANNOUNCE printed "[fakeclock] 2020-01-01T00:00:00.000Z … /opt/homebrew/bin/npm". argv1 is the unresolved bin symlink, which the regex misses.
  - My v1 preload had the same miss. The v2 re-measure shows no verdict change.
- R2: the comment's "end of Sunday 2026-10-18 Sydney time" names the intent. The actual lapse is 11 h later. The comment's next line, the commit message and KS-769 state the true instant. Not a finding.
- R3: the brief says 19 other open PRs; I count 20. None was created after 05:46Z, so it is a miscount.
- R4 (my own instrument faults, publicly corrected; none reached a verdict):
  - the unit probe passed findTrackedLocks()'s object instead of .locks, reading "THROWS: undefined";
  - the first esbuild parse kept inner comments;
  - the v1 preload npm miss.
  - Each was voided by rename and re-run.
- R5 (Polish, pre-existing): validateOutOfScope says "missing expires (not an ISO …)" for a present, malformed value.
- R6 (policy, not the gate's): the card said "your reason on KS-769"; reason is unchanged and Kam gave no further reason.

Checkout readings (Secuura 2_Project_Files):
- 16:03:11 AEST: porcelain 0, .git/config sha256 d7e7298b02c45f52…, refs 918, worktrees 111.
- 16:18:45 AEST: porcelain 0, d7e7298b02c45f52…, 918, 111.
- Never pushed, never ran the hook, never ran preflight in the checkout, never entered Seat A's worktree.

MERGE ADDENDUM
squash 71bd80a35 onto develop d7e95cd9f (still origin develop at 06:18:06Z; file-disjoint from #1018/#1019 and all 20 other open PRs); #1020 attaches to KS-769 only, linkKind contributes, and KS-769 stays open (Refs, never Closes); equality target lock-discovery.mjs blob 3dd903b52; the fuse lapses 2026-10-19T00:00Z = 11:00 AEDT Mon 19 Oct; audit:contract 59/59 and audit-locks rc 0 with 43 scanned (re-measure); Records: R1 (drafter fakeclock does not exempt npm; no verdict effect), R2 (end-of-Sunday wording vs 11:00 AEDT Monday lapse, value correct), R3 (20 not 19 other open PRs), R4 (three QA instrument self-corrections), R5 (validator "missing expires" wording, pre-existing), R6 (reason unchanged; policy). Findings for the owners, not this merge: F1 (TICKETS KS-1024/KS-763 by Thu 24 Sep 10:00 AEST; KS-528/KS-530/KS-729 by Wed 30 Sep 10:00 AEST) and F2 (preflight env-fail tail text, pre-existing).

NOT TESTED
- Not applicable:
  - Schemathesis, Akto, Playwright, k6, docker or any stack, preflight legs 3/4/8 (SKIP by design), and any service or package suite: no product byte changed.
  - A persona or UI pass: no user flow.
- Preflight legs 1 and 14 were NOT measured green: fresh worktree, no root npm ci, no packages/shared build. Identical on base and head. The seat's legs 1 and 14 green is not independently reproduced.
- Not run under a non-Sydney machine TZ (UTC-vs-Sydney equivalence is READ).
- The merged tree was not re-run separately (tree-hash-identical).
- audit:contract under tamper: T1 only.
- Seat A's records folder: not opened.
- Fuses outside Blockchain/Dev/scripts: not swept.
- mergeable_state "unstable": not investigated.
- KS-769's Backlog -> In Progress history walk: not queried.
- Gate results depend on the live registry at 06:08–06:13Z.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks769-1020-71bd80a35-tier2-r1/report.md (evidence/ alongside)
