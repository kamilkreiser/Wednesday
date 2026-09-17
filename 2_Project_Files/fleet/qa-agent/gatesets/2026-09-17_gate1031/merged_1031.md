auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
**MERGED #1031 (KS-1213) on your GO (13:13:41Z): squash `732c13459d76f5b05ade94bb91de7e47585b0e7d`, merged_at 13:15:35Z.**
- Verified at origin: develop = the squash; parent `27e53ec3a` = pre-merge develop (unmoved since your read, so no STOP path was touched); tree `007cca4290fb313744e4c076116241f2a00538eb` = your prediction.
- All three blobs are equal: `documents.ts` e3eeb5a68, `certifications.ts` 20934ee94, the ks1213 test 808282689.
- **Originate jest on the merged develop: 64 suites / 741 tests, 0 failed, 0 pending**; ks1213 85 / 85.
- KS-1213 stays In Progress. Facts comment `c8ff0ab1-91e6-46f6-a38b-f980ccd1ebf1`.
- **Filed:**
  - **KS-1228** (D1 + Q-ISSUE-AFTER-OBO, Medium): provenance before refusals. It is one class with an existing `BACKLOG.md` entry for `/share` and `/transfer-custody`, which has no ticket, so KS-1228 names all of them.
  - **KS-1229** (the drafter's 6 + the gate's Q ×3 + R-a, Low, test-only, local-model candidate).
**A slot is free (open: #1032, #1034).** Nothing of this lane can use it yet: QUEUE item 4 (KS-805 + the KS-839 contract sentence) waits for #922, which is still OPEN. I idle on the watcher.

## Recommendation
Route **KS-1229** to the local model if you agree. The free slot sits idle until #922 merges or you mail other work (KS-1204 and KS-1101 are owed but need your mail to start).

## Detail
- **Pre-step** (`merges/merge-1031.prestep.out`), then `--do-merge` (`merges/merge-1031.out`):
  - ls-remote: develop 27e53ec3a, pull/1031 be8596a29 (= GO).
  - merge-tree 007cca429 = GO. Predicted blobs OK ×3. develop→predicted files = exactly the three #1031 files (the script stops on any other set).
  - attachmentsForURL(pull/1031) = [KS-1213 contributes In Progress]; KS-1203 not linked. Closing-phrase scan: 0 hits over 6 texts; the control fires.
  - Merge PUT with sha pin: http 200. At origin: develop == squash, parent == pre-merge develop, tree == predicted, 3 blobs OK.
  - My slip: the script's subtree line still printed the label "api-gateway subtree", but the value it compared was `services/originate` (a8624aca6, equal to the head's).
- **Originate run** (records `merges/1031-postmerge/`): my worktree `raise-0916-a` detached at `732c13459` (porcelain 0). 27e53ec3a..732c13459 touches 0 package files, so its install (from the #1029 step) is develop's.
  - `npx jest --json` in `services/originate` with jest 29.7.0: rc 0, 64 / 741 / 0 / 0; load 3.1 → 6.5; 12 s.
  - Porcelain 0 after; the worktree is back on the KS-1215 branch (fd81a75f0, pushed as #1034).
- **KS-1213 comment records:**
  - the exact rule (case / whitespace / NBSP / combining / confusables / non-strings incl. null, '', true, false, arrays, objects / form-encoded → 400 BAD_REQUEST before any derived row, certification, sign call, holder stub or anchor);
  - L01 (an echoed legacy served label is now 400);
  - L03 STILL OPEN (legacy inheritance with no caller type still served as the legacy label, propagating along the chains);
  - the out-of-repo caller residual (0 in-repo callers);
  - R-b, R-c; and pointers to KS-1228 and KS-1229.
  - Readback 5/5 anchors.
- **KS-1228** (Medium, Backlog, our account, related KS-1213, Refs KS-1213):
  - `/version` `handleOnBehalfOf` at `documents.ts:1951` (develop 732c13459) records provenance before the type 400, the hash 400 and the 404 (V-OBO, V-OBO-404, V-OBO-HASH on develop and head). Issue is correct today but unpinned (Q-ISSUE-AFTER-OBO 0 reds).
  - Fix-shape plus regression cells for all four call sites (`/share` :2136, `/transfer-custody` :1595).
  - Search: `handleOnBehalfOf` 2 (KS-566 archived, PS-616; neither on this ordering); `recordActionProvenance` 0; `action_provenance` 16 (none on writing before a refusal); `version:watermark` 1 (KS-661).
  - The `BACKLOG.md` entry "`/share` and `/transfer-custody` write an action_provenance row BEFORE the 404/403" (2026-09-01) is the same class. It lives in a repo file, not a board ticket, so I cited it in KS-1228 rather than editing BACKLOG.md.
- **KS-1229** (Low, Backlog, our account, related KS-1213, Refs KS-1213): one row per gap with the tamper, the measured consequence and the pinning cell (X-ISSUE-AFTER-HOLDER / X-ISSUE-AFTER-ANCHOR first, then X-ISSUE-LOOSE, X-SIGNCERT-AFTER-UPSTREAM, X-VERSION-TRIM, X-SIGNWALLET-SERVED, Q-SIGNCERT-UNTYPED-SOURCE-SKIP, Q-VERSION-TRUTHY, Q-SIGNWALLET-AFTER-VERIFY) plus R-a. Search `ks1213-a-derived-writer`: 0.
- Searches recorded in `tickets/search-1031-findings.txt`.

