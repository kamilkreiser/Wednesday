SUBJECT: [QA -> Wednesday] TIER 2 GATE #1025 (KS-528) 9954a7069 — GO
TS: 2026-09-17T09:50:27.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
QA -> Wednesday: TIER 2 GATE, ROUND 1, Secuura/Blockchain PR #1025 (KS-528, Seat B)

1. BLUF

VERDICT: GO on 9954a7069a16987da140654337555c9a13268b1f, and on the merged tree 23b56bac07faf84165882176e63436e1c470826e over develop efaaa6034f036dd9538ee35b189217b1d08b90a9. Develop is unchanged at origin from 19:41:42 through the pre-mail re-read at 19:49:13 AEST.

The PR does what the ruling says and nothing else:
- One file changes. Only rows GHSA-wrjc-x8rr-h8h6 and GHSA-337j-9hxr-rhxg change, and only their expires and reason fields.
- Through the shipped isLapsed, both rows are live through 2026-10-01 AEST. They lapse at 2026-10-02T00:00:00.000Z, which is Fri 02 Oct 10:00 AEST.
- The shipped gates are green at head. Their output is identical with head's or develop's baseline on today's clock. Both gates go red when either target row is removed.
- The reason carries KS-528, Kam's ruling label verbatim, the landing 2026-10-01 and both halves of the slip rule.
- #1025 attaches to KS-528 only, as "contributes". KS-528 is In Progress.

0 findings against the PR. 7 records, none blocking. R7 is my own instrument fault, corrected in the open.

Head check first: at 19:41:42, ls-remote refs/pull/1025/head, the branch and the PR API head.sha all read 9954a7069a16987da140654337555c9a13268b1f. It had NOT moved. Re-read at 19:49:13: unchanged.

2. ITEMS 1-6

(1) Conservation by parse, from git blobs 45ef8220f -> e6f2184d2:
- Rows: 34 -> 34, 0 added, 0 removed.
- Altered: exactly wrjc and 337j, each on exactly [expires, reason].
- Each prior reason (249 chars) is an exact prefix of the new one (873 chars).
- Row order and field order (package, reason, ticket, decidedAt, expires) are kept. The other 32 rows are deep-equal, including field order. $comment is equal. There are 0 duplicate raw ids.
- Controls that did not move: jjmj 09-30, frvp 09-30, rgwj 09-24.
- The identity control fails as it should, and 12 of 12 planted alterations fired: expires, ticket, decidedAt, row swap, field-order x2, row removed, row added, $comment, prior reason edited, a wrong date, an untouched reason.

(2) Expiry, through the SHIPPED baseline-contract.mjs:
- The code: utcToday() = new Date().toISOString().slice(0,10), and isLapsed is expires <= utcToday(). That compares UTC date strings, so a row lapses at 00:00Z on its expires date.
- The freeze is proven: at every instant utcToday equals the frozen date, a far-future freeze returns 2031-06-15, and unfrozen returns 2026-09-17.
- Head: wrjc/337j live at every instant up to 2026-10-01T23:59:59.999Z (Fri 02 Oct 09:59:59.999 AEST), and LAPSED at 2026-10-02T00:00:00.000Z (10:00 AEST).
- Controls: jjmj and frvp LAPSE at 2026-09-30T00:00Z, rgwj at 2026-09-24T00:00Z, and on develop wrjc/337j LAPSE at 2026-09-30T00:00Z.
- The explicit-today arm agrees. Malformed expires fails closed.
- date -j: 2026-10-01 Thursday, 2026-10-02 Friday, +1000 AEST. DST starts Sun 04 Oct, after the lapse.

(3) Shipped gates from Blockchain/Dev, live registry, 19:43:57-19:44:33:
- G1 (head/head): audit-gate rc 0, "33 distinct advisories reported, 34 baselined", 0 CLEANUP.
- L1: audit-locks rc 0, 43 locks, "32 advisories match, 32 already baselined".
- C1: npm run audit:contract rc 0, "ℹ pass 59" of "ℹ tests 59", fail/cancelled/skipped/todo 0 (same on develop).
- Equality: G1 = G2 (head tree + develop's baseline via AUDIT_BASELINE_PATH) = G3 (develop). L1 = L2 = L3. All True.
- Negative controls: head minus wrjc gives audit-gate rc 1 and audit-locks rc 1, NEW exactly GHSA-wrjc-x8rr-h8h6. Head minus 337j gives rc 1 and rc 1, NEW exactly GHSA-337j-9hxr-rhxg.
- Frozen clocks, reading the LAPSED list, not the rc:
  - head at 2026-10-01T23:59:59.999Z: gate and locks both rc 1, LAPSED 9 (other rows), neither wrjc nor 337j;
  - head at 2026-10-02T00:00:00.000Z: rc 1 and rc 1, LAPSED 11, including wrjc and 337j "(expired 2026-10-02)";
  - develop at 2026-10-01T23:59:59.999Z: rc 1, LAPSED 11, including wrjc and 337j "(expired 2026-09-30)".
- The freeze was scoped to the gate script and proven per run (stderr prints the frozen new Date() and Date.now() with the pid). The npm child was not frozen: counts at frozen instants equal the real-clock counts.

(4) Reason text. The appended 624 chars are identical on both rows and contain:
- KS-528;
- "RE-DATED 2026-09-17";
- the ruling label, byte-equal to answer_kam_rulings_1831.md: "Commission the v7 migration AND date both rows to its planned landing (recommended)", at 18:31:25 AEST, with the card id;
- landing 2026-10-01;
- the lapse instant, stated correctly;
- the slip rule, both clauses: "reports to Wednesday before then" and "does not re-date again on its own".
Forbidden-class regexes, each proven on a planted positive first (8 of 8), found 0 key prefixes, 0 hex runs, 0 secret assignments, 0 PEM, 0 mnemonic-shape runs, 0 Peter/Stuart and 0 closing phrases in the reason, PR title, PR body and commit message. The only hits were base64-ish over-matches on the card id and a file path, read by eye: not credentials.
Ruling on the READY's "slip -> report, no second re-date": that literal string is absent, but its meaning is present. RECORD, not a finding.

(5) Linking. Read 19:46:01 and re-read 19:49:15, just before this mail:
- attachmentsForURL(pull/1025) = 1: KS-528 [In Progress], linkKind 'contributes', status open, completedAt None.
- Controls: pull/1021 -> KS-1211 contributes (merged); pull/99999 -> 0.
- KS-528: state started, completedAt null, 1 attachment. Its only state transition is 2026-09-17T09:21:22.262Z, bot GitHub, Backlog -> In Progress.
- Closing phrases (5 closing forms hit, 3 non-closing miss): 0 in the title, 0 in the body ("Refs KS-528" x1), 0 in the commit, 0 in the one linear[bot] comment.
- No ticket moves to Done on #1025.

(6) Merge and overlap:
- In my own clone, merge-tree --write-tree efaaa6034 9954a7069 = 23b56bac07faf84165882176e63436e1c470826e. That is the head tree; the drafter's 23b56bac0 held. The develop x develop control gives 38ea11907 = develop's tree.
- The merged baseline blob is e6f2184d2. Develop delta: none. Re-computed at 19:49:13: same tree.
- Open PRs: 21 (20 others). 0 of 20 touch audit-baseline.json, 0 share any file with #1025, 0 touch scripts/audit/. #1025's own file list contains the baseline (instrument control).
- Seat B's PR-3 is NOT open.

3. MERGE ADDENDUM

squash 9954a7069 onto develop efaaa6034f036dd9538ee35b189217b1d08b90a9 (merged tree 23b56bac07faf84165882176e63436e1c470826e; drafter 23b56bac0 while develop = efaaa6034; file-disjoint from every open PR: 0 of 20); #1025 attaches to KS-528 only, linkKind contributes, no closes. KS-528 stays In Progress (Refs, never Closes; the v7 migration MIG-1 is the fix; no ticket to Done). Equality targets after the squash: Blockchain/Dev/scripts/audit/audit-baseline.json blob e6f2184d2 (34 rows; wrjc/337j expires 2026-10-02); audit-gate rc 0 33 reported / 34 baselined, 0 CLEANUP; audit-locks rc 0, 32 match / 32 baselined; audit:contract 59/59 (re-measure). Seat B's PR-3 takes develop in after this merge. Records:
- R1: the literal "slip -> report, no second re-date" is absent from the bytes; both clauses are present in prose.
- R2: the ruling label is verbatim; the option key "migrate-and-date" is absent, and the card id is present.
- R3: the bytes and relay say 18:31:25, but Wednesday's decision store reads ruled_ts 18:31:32.038 (per the brief). QA did not read the store. For Wednesday.
- R4: the READY's "0 of 19" is now 0 of 20, because #1026 opened. No slip.
- R5: "rows 11 and 12" is the fixability-table numbering (status_fixability_table.md:91). In the file the rows sit at positions 15 and 16.
- R6, Polish, prose only: the commit message says "Their audit-baseline rows lapsed 2026-09-30", past tense for a lapse that has not happened yet. The squash message may reword it. Its advisory claim "fixed only in react-router 7.18.0" matches the GitHub advisory API (both first patched in 7.18.0).
- R7, QA instrument fault: my first LAPSED parser only read audit-gate's line format, so audit-locks' frozen runs read 0 ids. I caught it by reading the raw files, then re-parsed entry by entry with a positive control (s05b). All numbers above are from the corrected parse.
If develop moves before the squash: re-run merge-tree, and prove the baseline, scripts/audit/* and root-lock blobs are unchanged.

4. NOT TESTED (same prominence as the findings; NOT-TESTED.written-first.md was written at 19:41:04, before any run)
- docker, stack, kintsugi, demo, image: not-applicable (config-only; forbidden by bounds).
- preflight.sh whole, and the seat's in-hook preflight 12/15: not-applicable and forbidden. I ran legs 5/6/7 directly. The other legs were NOT RUN.
- Unit, service, frontend and platform suites: not-applicable (no code or lock byte moved).
- The react-router v7 migration (MIG-1), and whether it can land by 2026-10-01: not-applicable here (separate TIER 1 gate). Seat B throughput, the date's main risk, is UNMEASURED.
- Browser, persona, accessibility, network-failure and auth-state dimensions: not-applicable (nothing user-facing).
- Whether carrying two medium advisories to 02 Oct is acceptable: a risk ruling, not tested.
- A real clock reaching the instants: frozen-clock runs only.
- Wednesday's decision-store ruled_ts (R3): not read.
- The GitHub squash itself, and gates on the real merge commit: pre-merge, so not testable. Targets are in the addendum.
- Seat B's stub-kill claim: not tested.
- Registry drift after 19:44:33: not controlled; the merge seat re-measures.
- The other lapsing rows (6 on 09-24, 3 on 09-30), used as controls only: every Blockchain/Dev push goes red from Thu 24 Sep 10:00 AEST unless PR-3..PR-8 land. Out of this PR's scope; stated so it is not silent.

Secuura checkout readings, start 19:41:39 / close 19:49:17 (no change between them):
- porcelain 0 / 0
- .git/config sha256 d7e7298b02c45f5267520f79985ae97abe51ac3d8b82a7e8cb35c50059a09f66 / same
- for-each-ref 929 / 929
- .git/worktrees entries 112 / 112

No push, preflight, hook, docker, az or mnemonic. I never entered any worktrees/ directory. GitHub and Linear: GET/query only. No token printed.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks528-1025-9954a7069-tier2-r1/report.md
Evidence: the same folder, under evidence/ (s01-s09 scripts and outputs).

QA agent (findings only)

