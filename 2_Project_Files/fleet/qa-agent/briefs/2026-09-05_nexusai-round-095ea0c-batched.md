# QA Agent Invocation Brief — Datasec / NexusAI, the batched round @ `095ea0c` (RD-245 root-cause fix · RD-155/F-2 · RD-296's behavioural wiring test · F-4/F-5/F-6/F-7 rewrites · RD-303 untracking · RD-307 quarantine) — through-code + real-browser pass

**R0 (client isolation):** this brief carries exactly one client's content — Datasec / NexusAI. Do not name or reference any other client, in the report or anywhere else. Your report goes under `projects/nexusai/`.

## Charter (read first, in full)

`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

Read it end-to-end before running anything. This brief supplies only WHAT and WHERE.

## 1. Target
- **Client / Project:** Datasec / NexusAI
- **Source tree (read-only, for root-causing):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files` — the builder (S33) is IDLE and holding for this gate; its tree is clean, 0/0 with origin. Still: **do not check out or modify its tree** — work from your own pinned worktree as the previous NexusAI pass did (`./scripts/qa-surface-up.sh 095ea0c <port>` creates one under `qa-worktrees/`).
- **Branch under test:** `rd-136-nga-defaults-s12` at **`095ea0cd3bb75628e71c348f59990d01ac5937e9`** — verified as that branch's head at origin by Wednesday with `git ls-remote` at 2026-09-05 09:5x AEST. **Pin to it**; report the head you observe at the end.
- **Commits in scope, oldest first (all above `b77feea`, which the previous pass used as its "old" baseline):** `1c5d3f7` (RD-155 F-2 — predicate widened; NEVER GATED) · `7147a4a` (RD-296 — gated by the previous pass at this SHA, PASS with F-1…F-5; do NOT re-run that pass) · `2b3fe32` (RD-245 F-1/F-3 — the root-cause fix) · `0f96323` (RD-303 untracking) · `e94adb9` (RD-307 quarantine + ignore) · `095ea0c` (F-5 post-condition rewrite, F-4 corpus, F-6/F-7 re-derivation, RD-296's F-2 behavioural wiring test).
- **Running target:** a LOCAL run of `095ea0c` you stand up (open mode, no auth shim). **Environment identity: LOCAL DEV, non-production; SQLite branch only** (no Log Analytics workspace). Ports: 3111 is held by a live builder surface — do not touch it; 3113/3114 were the previous pass's and are now stopped; pick free ports in the 31xx range and say which.
- **Production?** NO. Nothing here is deployed. **No deploy, no demo, no outbound authenticated call to any workspace, no synthetic feed (RD-118).**

## 2. Spec / DoD being tested against

**These are the BUILDER'S CLAIMS from its mails to Wednesday (READY FOR QA 2026-09-04T23:07Z for RD-245, 23:29Z for the round) and its QA-report responses. They are inputs to FALSIFY, not evidence.** Wednesday has verified only the branch head, the commit list, the diff stat, and that the six `.azure` files are no longer tracked.

### RD-245 — the root-cause fix (2b3fe32), built to Wednesday's ruling "(e)+(a)"
**Incident (from the real artefacts):** the two surviving settings generations were 23 ms apart, both written by the AI misunderstanding log (`setSetting('ai_misunderstanding_log', …)` at server.js:169, cap 500), which shared `settings.json`'s two-slot backup rotation with every real setting.
1. **(e)** `ai_misunderstanding_log` LEFT `settings.json` for its own file under the data dir, written by its own path, NOT part of `settings.json`'s rotation, and with no backup of its own.
2. **Migration on first read after upgrade:** if the new file is absent AND settings still carries the key → read once → write the new file → remove the key via the product's own writer → log ONE line naming what moved and how many entries. **Order: new-file-first, key-removal-second** (a crash between them duplicates for one boot, never loses). Never read-empty-and-move-on.
3. **Contract unchanged:** `/api/ai/audit-log` and `/api/ai/audit-log/summary` keep their behaviour; a test asserts the migrated log is served with the same entries, another asserts round-trip order (newest last).
4. **(a)** the identity guard compares EXCLUDING `*_updated_at` keys; its limit is stated in code and on the ticket (a guard against no-op rewrites, not the fix).
5. **NOT changed:** two generations; every real settings write still backs up. **Disclosed cost:** the migration's own settings write consumes one rotation slot, ONCE, on the upgrade boot.
6. **Privacy catch:** the log holds user QUERIES; `dataExport.js` and `dataErasure.js` (`PURGE_FILES`) are hardcoded filename lists — both updated to name the new file, with a test each. (Without this, moving the storage would have dropped user queries from data-subject export and right-to-erasure.)
7. **Four DO-NOT-BREAK persistence guarantees** (project CLAUDE.md) read and claimed PRESERVED: mount path unchanged; DB_PATH untouched; settings persist across image rebuilds (the new file sits on the same volume; the migration is what keeps an existing deployment's log); persistence sentinel untouched.
8. **15 new tests in `__tests__/backup-rotation-through-setsetting.test.js` drive `setSetting()`** — the product's own writer. Red-proofs: revert (e) → 4 fail; revert (a) → 1 fail; migration-reads-empty → 4 fail. The ruled regression is an EQUIVALENCE: two real `setSetting` changes with five audit appends interleaved must leave the backup generations EXACTLY as if the audit log had never been written, with its own control that the churn happened.
9. Verified by the builder on a COPY of the real incident file: 120 entries in settings → 120 returned → 120 in the new file, settings 20 keys → 18.

### RD-155 F-2 (1c5d3f7) — never gated
10. The earlier QA pass found RD-155 had widened the predicate AND moved the SELECTION; the fix at 1c5d3f7 is claimed to restore the selection while keeping the widened predicate ("only absence is absence" — `0` and `false` count as present). The builder's earlier claim (falsified by the previous pass's F-4): "the general rule subsumes the four named-key branches."

### The 095ea0c rewrites
11. **F-5:** the criterion-3 warning (fired in 2 of 9 states, 0 correct) replaced by a POST-CONDITION — rotate, then read what is on disk; a new suite enumerates all nine (current, prev) states plus a FAULT INJECTION.
12. **F-4:** "subsumed" is FALSE and now PINNED — a 48-case corpus (four named keys × 12 values) shows NINE divergences (six where the new rule is NARROWER: `[]`/`{}` under `authEnforced`/`logAnalyticsWorkspaceId`/`entraTenantId`; three BROADER: `firstRunComplete` = 0, 1, false). Behaviour kept; the claim corrected; the value list named in code.
13. **F-6/F-7:** the RD-245 red-proof re-derived against the real parent (`git show b806848^:backend/jsonStorage.js`): 2 fail / 3 pass; against the guard WITHOUT the emergency hoist: 1 fail / 4 pass. Every non-control test has a red proof.
14. **RD-296 F-2 (owed):** the four source-text matchers REMOVED; `__tests__/sustainability-wiring-behavioural.test.js` mounts the real router over a real temp SQLite, makes a real HTTP request, asserts `dataSource === 'local-database'`, with a control that rows were really read (10 impressions from 5 seeded jobs) and a red proof that reintroduces the direct-database read THROUGH THE ENDPOINT. **Builder-named hole:** a revert of the MOUNT alone (server.js handing the reader the database instead of the selector) will NOT red this file — that property is checked only by the log-line correlation.

### RD-303 (0f96323) and RD-307 (e94adb9) — Kam's rulings
15. Six `4_Credentials/.azure/` files untracked (`git rm --cached`), still on disk, no history rewrite; **the whole `4_Credentials/` directory is now ignored** (the earlier ignore block named four filenames that did not exist).
16. `data/.machine-id` moved to `data/_quarantine_2026-09-05/` with a README and a one-line restore, after a four-line proof with controls that nothing in that data dir is keyed by it (no `ENC:` values there — control: the same search finds them in three backend files and the real store; zero `.json` files for the encryption service to have written; the file postdates everything else by a day; the real store keys from `~/.printer-dashboard-machine-id`, a different SHA). Plus one ignore line for the quarantine path.
17. **Gate claim for the head:** `PASS — 1565/1565 across 93` (counts file regenerated 1566/92 → 1565/93, net −1 = four text matchers out, three behavioural in).

## 3. Scope

**Charter:** through-code on every commit above (except re-running the RD-296 pass) plus a real-browser pass on the surfaces this round touches, hunting: a migration that is correct on the happy path and lossy on the crash path or on a second boot; a privacy list updated by name but not by behaviour; an equivalence test that can pass by accident; a "preserved" guarantee read from the doc rather than exercised; a fault injection that cannot fail; an untracking that leaves a tracked twin; a quarantine that the next test run silently undoes.

**In scope — through-code:**
- **Claim 2 — the migration, all three paths:** (i) fresh install (no key, no file); (ii) upgrade (key present, file absent) — count and content preserved, key removed, one log line; (iii) **crash between new-file-write and key-removal** (simulate: file present AND key present) — must not double-append on the next boot, must not lose; (iv) a SECOND boot after a clean migration must be a no-op (no extra rotation slot). State which you MEASURED.
- **Claim 5 — the one-slot cost:** a real setting changed immediately before the upgrade boot must still have a surviving generation after it. Measure it.
- **Claim 6 — privacy lists by BEHAVIOUR, not by name:** drive the export and the erasure paths on a store with a migrated log — does the export CONTAIN the entries; does erasure REMOVE the file? A name in a list is READ ONLY; the export payload is MEASURED.
- **Claim 7 — guarantee 3 ("settings persist across image rebuilds"):** what does an image rebuild actually do to the data dir in this project (read DEPLOYMENT_GUIDE.md / mainTemplate.json / compose); is the new file on the same persistent volume by construction, or by assumption?
- **Claim 8 — the equivalence test:** can it pass by accident? Break (e) in a way the builder did not try (e.g. keep the log in settings but exempt it from backup by a flag) and see whether the test discriminates. Re-derive ONE of the three red-proofs independently.
- **Claim 4 — the guard excluding `*_updated_at`:** is the exclusion by key SUFFIX on every nesting level, or only top-level? Construct a nested `_updated_at`.
- **Claim 10 — RD-155 at 1c5d3f7:** the selection is restored — show it with the previous pass's own counterexamples (the five/six where the predicates diverged) and confirm the widened predicate still holds for `0` and `false`.
- **Claims 11–13:** the F-5 fault injection — can it fail? Remove the post-condition and confirm the suite goes red; confirm the nine states are the nine states (enumerate them yourself). F-4's nine divergences — confirm the corpus is in code and the pins go red if the predicate is "fixed" back.
- **Claim 14 — the behavioural wiring test:** confirm the four text matchers are gone (grep the test tree for string reads of server.js); confirm the builder-named hole is real (revert the mount alone → is anything red?) and say so as a KNOWN GAP, not a new finding, unless you find a cheap test that closes it.
- **Claims 15–16 — RD-303/RD-307:** `git ls-files 4_Credentials/` must be empty at the head; are there OTHER credential-shaped tracked files anywhere (`git ls-files | grep -iE 'credential|\.env|secret|\.azure|\.gh'`)? Does the whole-directory ignore hide a file CI or the deploy script needs? **AND THE ONE WEDNESDAY FOUND: `data/.machine-id` EXISTS AGAIN at the head's working tree (mtime 09:20, newer than the quarantined 08:34 copy) — the 095ea0c test run recreated it.** Establish which test(s) write it and whether the test suite writes the key seed into the REPO data dir on every run; if so, that is a finding with a fix-shape (tests run against a temp HOME / data dir), and the quarantine was of an instance, not of the cause. Do not move, read, copy or delete the file.
- **Claim 17:** re-run the gate on your pinned worktree; report your numbers beside the builder's.

**In scope — browser (REAL browser, Claude-in-Chrome, both modes):**
- The app boots on a data dir that carries a settings.json WITH the legacy `ai_misunderstanding_log` key (seed it) — after boot: the audit log page/endpoint shows the same entries; the settings UI still shows every real setting; 0 console errors.
- The Sustainability tab still renders (regression only — no figure diff needed; the previous pass measured that at 7147a4a and nothing in this round touches its data path; confirm by diff).
- Any surface RD-155's predicate drives (the "settings elsewhere" warning) — does it fire for a numeric/boolean setting and NOT for absence?

**Out of scope / do NOT touch:** the demo and the dev app; any deploy; the synthetic feed (RD-118); outbound calls to any workspace (RD-305 stays unmeasured, say so); `data/.machine-id` and the quarantine folder (observe only); RD-304/RD-306 (recorded, not this round's work); RD-297 (Kam ruled: leave); the builder's tree, 3111.

## 4. Credentials (POINTER ONLY — never values)
- `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/4_Credentials/.env` — source it only if the stand-up script needs it; never echo a value; never copy one into a report. No workspace credentials are in scope.

## 5. State-mutation & cleanup
- **Pattern: exclude-and-report-only** on shared state; your own worktree and temp data dirs are yours to seed. **NEVER `rm`, anywhere — STANDING (Kam's rule: cleanup means quarantine).** `mktemp -d` per attempt, abandon the old one; guard every expansion (`"${DIR:?unset}/…"`); if cleanup starts costing budget, stop and report NOT RUN with the blocker named.
- **Restore any file you tamper with byte-identically and prove it with a hash** — this round's subject is a file-rotation and migration mechanism; a tamper you do not restore is indistinguishable from the defect.
- Leave your worktree and surfaces in place; name the ports; retire = stop the process, never remove the tree.

## 6. Output boundary (fixed — not a choice)
**Findings, reports and recommendations ONLY.** No code, tests, fixtures, tickets or config changes anywhere. Fix-shapes and the regression test the owner should add, in prose. (Kam ruling 2026-08-11, absolute.)

## 6a. EVIDENCE CLASS ON EVERY FINDING THAT RECOMMENDS AN ACTION (mandatory)
**`MEASURED AT RUNTIME`** (driven and observed — name the probe) · **`PROBED`** (an adjacent call; say what it does NOT cover) · **`READ ONLY`** (from source/spec/config, not executed). A recommendation without one is incomplete. `1565/1565 across 93` is a claim about a suite, not about a migration that survives a crash or an export that contains a user's queries.

## 7. Known-fragile / known-changed areas
- **Known-fragile:** this project's guards have repeatedly been red-proofed in the shape of the defect that motivated them and shipped over a corpus of a different shape (RD-245's original fix is the canonical case — five green tests over a state machine the product does not have). The jsdom instrument cluster (RD-163/201/199) is suspect for contrast numbers — produce none.
- **Recent changes — do NOT flag as new:** RD-291, RD-294, RD-299, RD-301, RD-302, RD-282, RD-292's date humanising, RD-296 (gated), RD-297 (Kam: leave), RD-295 (answered by RD-296; human moves the state).
- **Known open gaps carried:** RD-304 (getDataSpan SQLite-only), RD-305 (two-consumer timespan format — unmeasured, one probe decides), RD-306 (LAW path discards the window; `take` before `order`; `created_at` defaults to now) — confirm or sharpen, do not re-discover. The builder-named hole in the wiring test (mount revert not caught) is a KNOWN gap.
- The QA project still has no launcher entry, no inbox and no wrap hook — Wednesday runs this hop by hand and reads your report from your own project tree.

## 8. Logistics
- **Session time-box:** one bounded pass; if the browser half cannot be completed, deliver the through-code half with the browser checks listed as NOT RUN.
- **Findings sink:** `projects/nexusai/reports/2026-09-05-s33-round-095ea0c-batched/report.md` with probe scripts in `evidence/` beside it. Findings numbered F-1…; severity Blocker/Major/Minor; each with its evidence class.
- **Escalation path:** back through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class items ALWAYS pause for Kam. Priority on any finding is the humans' call, never yours.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] NexusAI round @ 095ea0c — batched through-code + browser pass` — BLUF first, the report's path, findings by severity with evidence class, the NOT-TESTED list, the branch head you observed at the end.

---

PROVENANCE:
- 095ea0cd3bb7… is the branch head at origin; the five commits above b77feea and their subjects; the 18-file diff stat 7147a4a..head; `4_Credentials/.azure/*` six files removed from the index | `git ls-remote`, `git log --oneline b77feea..origin/rd-136-nga-defaults-s12`, `git diff --stat 7147a4a origin/…`, `git ls-tree` on the NexusAI repo (read-only) | read 2026-09-05
- `data/.machine-id` present at 09:20 (56 B) in the working tree AND a copy in `data/_quarantine_2026-09-05/` (08:34) with README.md | `ls -la` on the NexusAI tree (read-only, contents not read) | read 2026-09-05
- Claims 1–9 (RD-245), 11–17 (the round, RD-303/307, gate) | builder's mails `[Datasec/NexusAI -> Wednesday] READY FOR QA: RD-245 F-1/F-3 @ 2b3fe32 …` (2026-09-04T23:07:48Z) and `… READY FOR QA: the round @ 095ea0c …` (23:29:57Z) and `… ACK deploy timing …` (23:30:31Z) at wednesday-agent@agentmail.to | read 2026-09-05
- Claim 10 (RD-155 F-2 at 1c5d3f7, never gated; the previous pass's F-4 counterexamples) | the previous QA report `projects/nexusai/reports/2026-09-04-qa-rd245-rd155-through-code/report.md` and the builder's F-2 mail 2026-09-04T04:32Z (recorded in Wednesday's NEXT-PICKUP.md 09-04 §5 — Wednesday's project, not the QA project's) | read 2026-09-05
- The previous RD-296 pass (PASS, F-1…F-5, its own ports 3113/3114 now stopped, 3111 the builder's) | `projects/nexusai/reports/2026-09-05-s33-rd296-through-code-and-browser/report.md` and its mail 2026-09-04T23:19:46Z | read 2026-09-05
- Wednesday's (e)+(a) ruling and Kam's proceed / untrack-and-quarantine / once-after-rd245 rulings | Wednesday's ANSWER mails 22:57Z and 23:15Z and Kam's panel messages 09:15/09:28 AEST, `0_Brain/dashboard/data/chat_log.json` — Wednesday's project, not the QA project's | read 2026-09-05
- RD-245/296/303/307 in Testing; RD-297/RD-295 To Do | Jira REST search, project RD | read 2026-09-05
