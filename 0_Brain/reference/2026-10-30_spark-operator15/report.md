# Spark operator 15 report, 2026-10-30 (Secuura / Blockchain)

*The operator's own write was refused, so Wednesday saved this from its final message at 06:3x AEDT. It is condensed: every figure is the operator's, and every brief path is verified to exist.*

Base: origin develop `7152ac669d2d6af08be5b9dcd35132818377155d` (the operator ran `ls-remote` three times; develop did not move).
The operator's own logs and specs are in this folder: `spec1799.py`, `spec1816.py`, `spec1798.py`, `spec1733.py`, `run_all.sh`, the lint, dry-run and control logs, `overlap.txt`, and `holdready_dry_*.log`.

## BLUF
- **Four briefs are READY.** Each has lint rc 0, a dry-run OK, and a control PASS 7/7, byte-identical, with `apply_mode=strict`. `hold_ready --dry-run` reports strict=True on each control run. None touches a file in any of the 20 open PRs.
- **Queued by Wednesday:** `spark/queue.md` at the 06:3x line, after Wednesday read every + and - line.

| brief dir (night/briefs/) | ticket | tier | files | A4 reds |
|---|---|---|---|---|
| ks_1799_p1_message_getter | KS-1799 | test_only (jest) | test ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts; tamper target pgErrors.ts:57 | 1/9 |
| ks_1816_p2_reconciler_comments | KS-1816 | code_patch2 (vitest) | anchoring reconciler.ts (2 comment hunks) + NEW ks1816-reconciler-comments-match-the-code.test.ts | 2/5 |
| ks_1798_p1_gdpr_pgcode_hostile | KS-1798 | code_patch2 (jest) | originate routes/gdpr.ts:139 (a try around one read) + ks445-gdpr-write-guards.test.ts (+5 cells) | 3/20 |
| ks_1733_p1_status_case | KS-1733 item 2 | test_only (jest) | governance test ks1722-proposals-list-refuses-an-unusable-filter.test.ts; tamper target governance.types.ts:353 | 3/48 |

## TASK 1: why hold_ready refused ks_1815_p3_trailing_comment
- **The golden's hunk 1 is malformed.** `@@ -29,3 +29,6 @@` has 3 leading context lines and 0 trailing ones, so `git apply` anchors it at the end of the file (the file is 95 lines). The cause is in `gen/mk.py`, `mk2.py` and `mk_testonly.py`: `trim()` cuts trailing context at the first blank line. The checker passed the run only under the `-C1` fuzzy apply; its A2 line says "FUZZY".
- **input.json is NOT stale:** it is byte-equal to the tip file (cmp rc 0).
- **A fixed golden exists:** the helper is moved before `const GET_BY_ID` and the hunk becomes `@@ -28,4 +28,7 @@`. Strict `git apply --check` gives rc 0, and 12/12 cells pass, red under the tamper. It lives in the session scratchpad (op15/t1/briefs/ks_1815_p3_trailing_comment/) and **will not survive the session.**
- **The fix cannot be re-run under KS-1827:** the ticket is now Done, so the builder refuses it.
- **Options:**
  - (a) A new Backlog follow-up ticket (Refs KS-1827), then re-run the fixed brief.
  - (b) A hand-written HOLD from the passed run, naming apply_mode=fuzzy.
  - (c) The tool fixes below.
- **Proposed tool fixes (Wednesday's call):**
  - (1) The generators run a strict `git apply --check` of the golden against `git show $TIP:<path>` and abort on non-zero.
  - (2) `round.sh --control` FAILS when apply_mode is not strict.
  - (3) A scan found 28 older goldens with the same shape (ks_1240_p*, ks_1462, ks_1509, ks_1543, ks_1619, ks_1684*, ks_1701, ks_1732*). This is a lead, not a verdict: it was measured against today's file lengths.

## Policy flags
- ks_1733 pins "lower case only" for `?status=`, the tip's policy, which the ticket calls "as today". It is not a ruling.
- ks_1799's tamper is a message-keyed rethrow, a stand-in. The ticket's literal narrowing mutant also reddens B1 and B3, so the ticket's premise ("every existing cell stays green") is false for that mutant.
- ks_1816's comments sit in the KS-1384 / KS-1808 / KS-1810 area, so a trivial rebase is possible.

## Refused (the operator's clauses, short)
- **The partition:** KS-1840 and KS-1823 (R 65th); KS-1831..1835 (#1814); KS-1805/1806; KS-1770, KS-1418, KS-1415 p1 and KS-1807 (the Projects Documents html, in open PRs); KS-1793 (#1792); KS-1795 (#1790).
- **Auth, credential or money:** KS-1819, 1820, 1821, 1836, 1837, 1838, 1825, 1803, 1797, 1792, 1791, and KS-1804. KS-1804's note 2 is a spelled-out single-cell pin on a credential file; the operator refused it conservatively.
- **Decision-shaped:** KS-1815, 1800, 1796, 1764, 1761, 1775, 1593, 1567, 1501, 1778, 1839.
- **Need a live DB, a stack or a large generator:** KS-1824, 1587, 1786, 1826, 1782, 1781, 1794, 1787.
- **Reconciler behaviour family:** KS-1808..1811.
- **KS-1812 is ALREADY PINNED:** mutant X12 gives 16 reds. A board seat should close or comment it.
- **KS-1783:** the gap is in a test helper, and the fix spans three files.

## TO-ROUTE findings (all Claude-seat work)
- **Anchoring GETs without a tenant check:** thread-state (index.ts:1109), tx (:1165) and queue (:1303). This is an Opus tenant-design seat's work, after R 65th frees index.ts.
- **Q12 uppercase SUPER_ADMIN** sits in documents.ts, which is #1814's.
- **The DocumentRecord union lacks 'deleted'** (documentRepo.ts:29), although the SQL at :621/:650 and gdprService.ts:855 already use it. It is type-only and not on the board: file it first.

## UNMEASURED
- No model round has run on the four briefs yet.
- The fixed KS-1815 golden's full control (refused because KS-1827 is Done).
- The 28-hit scan was measured against today's file lengths.
- Stray control run dirs (about 335 MB each) are the operator's, left in place: `runs/*_ks_1815_p3_fixtest-control` and the four `-control` runs.
