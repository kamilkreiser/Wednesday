# Seat R 78th's three UNANSWERED QUESTIONs to Wednesday (ITEM 4a, 4b, 4c)

Status source: R 78th HANDOVER FINAL block, `FIRST ACTIONS` item 1 (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatR-78th/HANDOVER.md` line 13): "ITEM 4a, 4b, 4c are UNANSWERED ... File or comment ONLY on Wednesday's ANSWER." The drafter did not search the inbox for an ANSWER (no mail access): a later ANSWER, if any, is UNMEASURED. The mail files below were read whole on 2026-11-03; each has a `.sent.out` beside it (not read). The product-file line numbers in the facts are R 78th's, quoted from its mail; the drafter did NOT re-read the product files (they live in R 78th's worktrees/develop; local develop ref is stale): UNMEASURED by the drafter.

Wednesday answers. Nothing here is answered by the drafter.

---

## 4a: stale "in-memory session fallback" wording

File: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatR-78th/mail/question_4a.txt`

Verbatim:

```
Seat R 78th
Context: gate 160 G160-F4 and R 77th's open item (a). The text "in-memory session fallback" is false (auth has no in-memory session store): session.ts:86 log line, routes/health.ts:30, index.ts:9, :172 and :255, and PR 1977's new test file, which pins the stale text as its INIT constant, so a wording change needs a matching test edit (after PR 1977 merges). Gate 160 G160-F5 adds a nice-to-have for the same PR: a null cell and a null-message cell (9 of 26 mutants survive, LOW).
Board search: 'in-memory session fallback' 0 hits; 'in-memory fallback' 4 hits, none about auth sessions (KS-1018 verification store, KS-1233 platform-settings, KS-1194 auth verification requests, KS-1731 vc-issuer paging); 'initRedisSession' 0; 'Redis not connected' 0. So nothing on the board covers it. Board search method: read-only Linear search of Secuura-PK (title and description, any state) by tools/board_search_r78.py; its controls held on every run (positive: 'Billing' finds 40 and the phrase "recipient's email address" finds KS-1937; negative: a random token finds 0). Output: evidence/board_search_item4*.out.
Question: do you want a Low ticket filed for the stale wording (and the F5 null cells as a line in it)? I file nothing unless you say so.
Meanwhile: continuing the other ITEM 4 searches; nothing built.
Needed-by: none.
```

Facts it rests on (each with its instrument):
- Gate 160 verdict G160-F4 (stale wording) and G160-F5 (9 of 26 mutants survive, LOW): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/verdict.md`, cited in the R 77th/R 78th briefs; the drafter did not re-open the verdict for this file (UNMEASURED by the drafter).
- Sites: session.ts:86, routes/health.ts:30, index.ts:9/:172/:255 (R 78th's reading, question_4a.txt line 2); the R 77th brief (`2026-11-03_seatR77...` as carried in the R 78th brief line 63) lists the same set.
- PR 1977 MERGED as squash `32921f7921c2` (HANDOVER line 6), so the "after PR 1977 merges" condition is met; the test file pinning the text is then on develop.
- Board search: 0 hits for the phrase (question_4a.txt line 3; outputs in `evidence/board_search_item4*.out`, not re-read).
- Open-PR overlap: Open PRs 1987 and 1988 touch services/auth (accountLockout.ts, routes/auth.ts, password.ts, vitest.setup.ts per the Seat B 85th brief lines 37-39); `routes/health.ts` is not in either list, `session.ts` and `index.ts` UNMEASURED against them.

Options it offers:
- (a) File one Low ticket for the stale wording, with the F5 null cells as a line in it.
- (b) File nothing (R 78th's default).
- The mail names no third option. If Wednesday wants the wording FIXED rather than ticketed, that is a new build (the wording change needs a matching edit of the PR 1977 test's INIT constant), not an R 79th raise item unless she says so.

---

## 4b: issuerCertSweep unguarded catches

File: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatR-78th/mail/question_4b.txt`

Verbatim:

```
Seat R 78th
Context: gate 161 G161-F4 and F8, the E7 survivor, and R 77th's open item (c). In services/auth issuerCertSweep.ts: the ISSUER_CERT_EXPIRING_SOON publish .catch (lines 127-133) is still unguarded and crashes the process for hostile values at base and head (LOW: the real publishEvent never rejects); the two outer .catch handlers of startIssuerCertSweep (lines 171-183) are unguarded but unreachable from the body at head; and the ACS catch survivor E7 (the catch returns true and the tests never check that SMTP was tried). PR 1978's flow fragment says a failed event publish is a logged warning, which holds for EXPIRED only. The brief says held pass O89-P6 waits on issuerCertSweep.ts.
Board search: 'issuerCertSweep' 0 hits, 'EXPIRING_SOON' 0, 'startIssuerCertSweep' 0. Nothing covers it. Board search method: read-only Linear search of Secuura-PK (title and description, any state) by tools/board_search_r78.py; its controls held on every run (positive: 'Billing' finds 40 and the phrase "recipient's email address" finds KS-1937; negative: a random token finds 0). Output: evidence/board_search_item4*.out.
Question: file one Low ticket for these sites, or leave them to O89-P6's ruling? I file nothing unless you say so.
Meanwhile: nothing built.
Needed-by: none.
```

Facts it rests on:
- Gate 161 findings G161-F4, F8 and the E7 mutant survivor: the gate 161 verdict (path not given in the mail; UNMEASURED by the drafter).
- issuerCertSweep.ts lines 127-133 and 171-183 (R 78th's reading in the mail).
- Held pass O89-P6 exists: `ls` of `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night` printed `READY_KS-1868-KS-1868-O89-P6_spark-dsv4flash_BRIEFED-CODEPATCH2-AUTH-ISSUER-CERT-SWEEP-FIRE-AND-FORGET-CATCHES-MESSAGE-COERCE-PASS-7of7_2026-11-03.diff.md` (drafter, 2026-11-03). Its name says "FIRE-AND-FORGET-CATCHES"; the drafter did not open it, so whether it covers the sites R 78th lists (the EXPIRING_SOON publish catch :127-133 and the two outer catches :171-183) is UNMEASURED. That is the fact the question turns on.
- R 77th HANDOVER line 93 (as printed by grep): PR 10 "shares `issuerCertSweep.ts` with held O89-P6" (PR 1978 touched the file).
- Board search: 0 hits on three phrases (mail line 3).

Options it offers:
- (a) File one Low ticket for the unguarded sites (EXPIRING_SOON publish catch, the two outer catches, the E7 survivor).
- (b) Leave them to O89-P6's ruling (an O89-P6 raise would cover its own hunks; whatever it does not cover stays unfiled).
- Note the dependency: if (b), whether O89-P6 is raised in the R 79th round is Wednesday's call; this round's census does NOT include O89-P6 (operators 91-98 only).

---

## 4c: auth.integration.test.ts 10 s hook timeout vs KS-1748

File: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatR-78th/mail/question_4c.txt`

Verbatim:

```
Seat R 78th
Context: R 77th's open item (b). PR 1977's body records that auth.integration.test.ts lost 56 cells in its before run to the 10 s beforeAll hook under fleet load (a skip, not a pass; it passed when re-run alone). Gates 160 and 161 ran the suite with cwd = services/auth and saw 0 failures and 0 skips on it.
Board search: KS-1748 (Backlog, "CLASS: a module-level beforeAll that imports a router pays the cold Vite transform inside the hook budget ... no ticket owns the pattern") is the class home; its description and its two comments name other locations in services/auth but 0 mentions of auth.integration.test.ts. Related and already on the board: KS-1602 (In Progress, security), KS-1734 and KS-1729 (Done), KS-825 (Backlog, auth suite green not deterministic; its text has no hook-timeout wording), KS-1474. I have NOT checked that the hook's cost is a router import; that is PR 1977's body wording. Board search method: read-only Linear search of Secuura-PK (title and description, any state) by tools/board_search_r78.py; its controls held on every run (positive: 'Billing' finds 40 and the phrase "recipient's email address" finds KS-1937; negative: a random token finds 0). Output: evidence/board_search_item4*.out.
Question: a comment on KS-1748 naming this location (my preference, since the class has an owner ticket), a new ticket, or nothing? I post nothing unless you say so.
Meanwhile: nothing built.
Needed-by: none.
```

Facts it rests on:
- PR 1977's body wording (56 cells lost to the 10 s beforeAll hook under fleet load; passed alone): PR 1977 is MERGED (HANDOVER line 6); body not re-read by the drafter (UNMEASURED).
- Gates 160 and 161 clean runs (0 failures, 0 skips) with cwd = services/auth: the R 78th mail line 2; verdicts not re-read.
- KS-1748 content and the related tickets (KS-1602, 1734, 1729, 825, 1474): R 78th's board search (mail line 3, `evidence/board_search_item4c.out`, not re-read). R 78th states it did NOT verify that the hook cost is a router import.
- New fact from outside the mail: PR 1987 (Seat F 27th, queued to Seat B 85th) lists `services/auth/src/__tests__/auth.integration.test.ts` among its changed files (`open_prs_start.json` for PR 1987, drafter read 2026-11-03), so that test file is currently being edited by an open PR; a comment on a ticket does not touch it, but any build on that file is excluded this round.

Options it offers:
- (a) A comment on KS-1748 naming auth.integration.test.ts as a new location (R 78th's preference; the class has an owner ticket).
- (b) A new ticket.
- (c) Nothing.
