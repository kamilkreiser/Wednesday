GO WITH NOTES — MERGE (no HOLD-FOR-KAM). Merge tree d06376c19fe6737f16ac926719381caa7c4052a6 (merge-tree rc 0; equals the head's tree, as S 17th predicted)
# QA Gate 182 (Tier 2, round 1): PR 1997 / KS-1981 mobile-tree exclusion owner swap
## Subject
- Start pin: head f2c5865754ed54f4007dce64c0eea14a10095d3d, develop 5c1ca287ed74b6353423a8c09e253abf3129233a. End pin: identical (no movement).
- Host: macOS, Node v26.8.1. Clone at workdir repo/ (shared clone, PR ref fetched into it only). Method: diff, instrument runs of audit:contract with red proof, read-only Linear GraphQL, git grep with controls.
## Findings
### G182-F1 — LOW (note, not blocking): the entry still names KS-769 in its own comment
**FOUND** lock-discovery.mjs line 202 (byte-identical to develop, by the ruling) still reads "KS-769 is a decision (dead tree / live tree / dormant-and-kept)", directly under the new `ticket: 'KS-1981'` line 201. Line 207 is the superseded record (legitimately KS-769). Also audit-baseline.json row for GHSA-gcqx-w48m-w2h4 says "outside this gate (KS-769)".
**TESTED** Counted `KS-769` in Blockchain/Dev/scripts/audit/ at head: 3 hits (202, 207, baseline json). Not behavioural; no reader parses comments.
**HOW** git grep on the head ref; control: KS-1981 hits at 182 and 201.
### G182-F2 — INFO: KS-1981 is In Progress, not Backlog
**FOUND** Linear shows KS-1981 state In Progress (commission and READY said Backlog). Low priority (4), due 2026-12-15, team KS, title is the mobile/secuura-app exclusion review: all match. KS-769 also In Progress (close is pending the merge).
**TESTED** One GraphQL read, key sourced in-process, never printed. The "board account" creator was not checked.
### G182-F3 — INFO: PR body not read
**FOUND** gh in the Blockchain launcher config is not logged in and the anonymous API returns 404 (private repo), so the PR body and live title could not be read. The commit message states the two-line reason and has no close-word. The title as given in the READY mail is 80 characters (limit 92) and starts "Refs KS-1981: ".
## What passed (measured)
1. Diff vs develop: exactly 1 file; exactly lines 182 and 201, KS-769 -> KS-1981, same words. Lines 202, 207, 235 byte-identical (sed + shasum, 3 of 3).
2. npm run audit:contract at head: 59 tests, 59 pass, 0 fail, rc 0. Red proof (ticket blanked on line 201): 59 / 49 pass / 10 fail, rc 1. Restored (sha256 efa6f383...): 59/59, rc 0. Readers (audit-locks printers, lock-discovery.test.mjs:110) exercised by those suites. CI step in security-scan.yml pins the same expected-case-count (59).
3. KS-1981 exists, Low, due 2026-12-15, right title (see F2 for state).
4. No Dockerfile, compose file or workflow names lock-discovery (0 hits; control: the same grep without the filename finds scripts/audit in security-scan.yml and package.json names lock-discovery). The CI workflow runs audit:contract (a CI test surface, not a deploy surface).
5. Commit message: no close-word. Title length 80 (from mail). Body unverified (F3).
6. merge-tree head onto develop: rc 0, tree d06376c1... Develop did not move.
## NOT tested
- PR body and live title text (gh unauthenticated). Branch protection/rulesets. Pre-push hook legs 3, 4, 8 (gateway/spec; untouched). Schemathesis, Akto, Playwright, k6, service suites. Node 24 LTS (ran on 26.8.1 only).
- The repo clone had no npm install; I copied semver 7.8.5 from the host's npm into my ignored clone's node_modules because audit-locks imports it. Without it 7 audit-locks cases fail (environmental, not the PR).
- Spark shadow not run (commission).
## Plain answer for Kam
This change only swaps which ticket the mobile app's audit exclusion points to: from the old KS-769 to the new review ticket KS-1981, in a comment and in one data field. Nothing deploys and no user sees any difference. The exclusion's end date (1 Jan 2027) is untouched, and the audit self-tests still pass 59 of 59 and fail when the ticket is blanked. One tidy-up remains: a comment two lines below still mentions KS-769.
