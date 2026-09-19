Seat B 8th successor (Secuura/Blockchain), from Wednesday

⚠ ONE SEAT ON THIS INBOX. This brief is for **Seat B 8th**. Your job is to raise five held local-model test-only fixes as THREE PRs, one per test file. Seat B 7th wrapped at ~16:45Z on 2026-09-19 (~02:45 AEST 2026-09-20) after merging #1092-#1096. Wednesday is launching no other Secuura seat beside you. If a mail names another seat, it is not for you. You touch ONLY the files below, each in your own `s-b8-*` worktree. Never touch the kept `s-b2-*`, `s-b3-*`, `s-b4-*`, `s-b5-*`, `s-b6-*`, `s-b7-*`, `s-a13-deploy` or `s-a14-deploy` worktrees, and never the box.

## BLUF
**One job: raise FIVE test-only fixes that the local model wrote and Wednesday held (03:25 and 03:29 AEST on 09-20) as THREE PRs, one per test file (the grouping is below). Then mail me ALL three heads in ONE READY so I can gate them as ONE batch.** They touch three separate test files and zero product bytes. Nothing merges without my signed GO naming the head. Kam is away until Monday; his standing words are quoted below. **If my GO has not arrived by 23:00 AEST Sunday 2026-09-20 (13:00Z), you do not merge: you hand over holding** (the WEEK-INSTRUCTION lapses at the end of Sunday). This seat deploys nothing: test files do not change a runtime image, so there is no kintsugi step and nothing goes to demo.

## ITEM 0: boot, before any write
- Read Seat B 7th's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-7th-successor-2026-09-20.md`. Also read the top entry of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (Seat B 7th). Seat B 7th's raise method is YOUR method. Copy its scripts into your own `2026-09-20_seatB-8th/` record folder rather than editing them in place:
  - `2026-09-20_seatB-7th/raise/`: `raise8.py` (its generic `multi` kind: several patches on one test file, each staged against its own checker, then the combined whole-suite tamper run), `lanes8.sh`, `msgs8.py`, `commit8.py`, `wtadd8.sh`, `deps8.sh`, `batch_build8.sh`, `batch_suites8.sh`, `typecheck8.py`, `linear_reads8.py`, `push8.sh`, `bodies8.py`, `open_prs8.py`, `series8.py` (it handles a PR that Refs two tickets), `targets8.py` and `merge8.py`;
  - `boot/measure8.py` (item 0 as reads only), `boot/tickets_boot8.py`, `boot/open_prs8.py`, `boot/grant_verify.py`, `boot/linear.py`;
  - `mail/ready8.py`, `mail/watch8.sh`, and the sender in `mail/` (only `send.py.b6` is there, the 6th's copy; which file actually sent the 7th's `out-01`..`out-05` is unmeasured by me: confirm before you rely on it);
  - `tickets/linear_ops.py` (`state … --expect <name>` is a compare-and-swap).
  - There are NO repo writes inside a push window, anywhere.
  - Clear the `login_stub` listeners by exact path. None of this batch is a shell suite, but an in-hook preflight during a push is.
  - Locate every tamper by its `from` text plus a scope anchor, never by line number. This round (my count, below): the six single-line `from`s each match exactly ONCE at develop, so each is its own anchor. **The eleven GUARD tampers are NOT single lines:** `    requireSuperAdmin,` occurs 13 times in platform.ts, so each GUARD tamper's anchor is its 4-line BLOCK (`  router.<verb>(` / the path line / `    authenticateToken(),` / `    requireSuperAdmin,`, to the first three), and each block matches exactly once. One pair shares a line: FIRSTOF2NULLMIXED and FIRSTOF4NULL both plant admin.ts:1132 (one `from`, two different `to`s). Show each plant's sha256 equals the checker's record.
  - Use `merge8.py` for the merges. It never writes an archived key as `Refs`.
  - Avoid the recorded slips:
    - Seat B 4th's four: S1 the section regex with no control; S2 `grep -P` on BSD, which left the push specs empty; S3 a commit message that claims more than the head shows; S4 the linear_reads history sort on mixed None;
    - Seat B 5th's one: a `ps | grep -c` that counted its own grep;
    - Seat B 6th's: S1 a series driver that retried Linear 429 only (fixed: 5xx retried, resumes without re-pushing); S2/S3 an unquoted zsh `$VAR` that did not word-split (use an array or a function, with a control);
    - Seat B 7th's one: S1 `measure8`'s first all-eight numstat was read after its temp object dir was gone (read inside the temp context; a control proves the outside read fails).
- **Carry the MG-1 lesson.** Write `raise/targets.json` with EVERY PR key BEFORE the first merge. Each key holds exactly one equality target, and each target is its head's blob. Every MERGED line must read `1 gate equality target(s)`. `merge8.py` STOPs otherwise. Build targets.json and the merge messages with `targets8.py` from the gate's addendum.
- origin develop = `c87458bdd8a9dd5ae3a082612e467cda5539aebc`, tree `458cff7174a2c9090a14c9d5ed71e3a17c3792e4`. That is my ls-remote read at 03:38:18 AEST 2026-09-20 (17:38:18Z on 09-19). It is #1096's squash, and all five READYs were written AT this tip. Re-read it yourself. If develop has moved, re-run every apply-check and prediction below over the new tip and STOP on any change to a target or tamper file.
- **All five canonical patches are `patch.diff`** in their run's `out.md.checker/` dir (for test_only runs that dir holds `patch.diff` and no `section_N.diff`). Each READY header names its path, and all five exist (my `ls` of each dir + sha256, 03:39 AEST). All five are modify-in-place on a test file that exists at develop, and all have 0 `-` lines. Use ONLY the header's CANONICAL PATCH path. Trust no other wording in a header.
- For each of the five, measure the following, and let a changed file STOP that item only:
  - `git apply --check` strict at develop, with a reverse control;
  - the target blob and each tamper file's blob, at c87458bdd against develop.
- **Order-independence (the ks1215 file carries three patches).** My reads, strict `git apply --cached` (no `--recount`, no fuzz, no whitespace option) in a scratch clone at c87458bdd:
  - tip blob `6adc2820514e` (= #1096's equality target); N95-1 alone `f9bff1b332af`; N96-1a alone `63d5c6876d82`; N96-1b alone `7c56fdbdcfde`;
  - N95-1 + N96-1a both orders `86d7faeae0e3`; N95-1 + N96-1b both orders `f47c8eadf237`; N96-1a + N96-1b both orders `6292bafe5906`;
  - **all SIX orders of the three give blob `fe235c8aa1d85d28d73a4853890c840bd59e0a7a`.**
  - These equal the round-18 briefs' own Collisions proofs. Re-measure them yourself, every subset and every order.
- **Archived ticket:** KS-1062 is **Done + ARCHIVED**. Read its state, archivedAt and attachments at three points: before your first push, after its PR opens, and at READY. Report all three reads. **Never reopen a Done ticket.**
- **Branch names:** for every live ticket, read Linear's branchName and check it for any foreign key before you use it. My read at 17:39:38Z (03:39 AEST):
  - **KS-1238's branchName still carries `ks-1215`** (`feature/ks-1238-f-1-four-properties-the-ks-1215-connector-bearer-fix-relies`). Never use it; rename the PR 3 branch (the #1052 trap: it would attach LIVE KS-1215 as `closes`).
  - **KS-1282's is clean:** `feature/ks-1282-get-apiplatformtenants-the-requiresuperadmin-guard`.
  - **KS-1230's is clean:** `feature/ks-1230-put-apiadminsettings-stores-a-connectors` (`-n45-5` … `-n86-1` suffixes already exist at origin; use a new suffix, e.g. `-n92-1`).
  - The ks1215 test file name notwithstanding, keep `ks1215` and `ks-1215` out of every branch name, PR title and commit subject. They name a LIVE ticket (KS-1215, In Progress), and Linear links a key written in those places.
  - Run a zero-at-origin name check for each branch. My ls-remote at 03:39 AEST: no `ks-1282` branch exists; four `feature/pin-startup-migrations-*` branches already exist (`…-all-tenants-skipped-summary-complete`, `…-skipped-tenant-summary-meta`, `…-skipped-tenants-counted-loop-continues`, `…-tenant-summary-first-error`), so PR 2's name must differ from all four.
  - **After EACH push and after each PR opens, measure `attachmentsForURL` for that PR.** It must show exactly the ticket(s) it Refs: {KS-1230} for PR 1, NONE for PR 2, exactly {KS-1238, KS-1282} for PR 3. A link to KS-1215, KS-1248, KS-1062 or any other key is a STOP: report it before you push the next branch.
- Plan confirmation (QUESTION mail, topic `plan confirmation (Seat B 8th)`) goes out before the first write. It carries your D-list proposal, including the ticket state of each item after merge. Wednesday's dispositions are below; read each ticket now and report it.

## GROUPING: one PR per test file
| PR | test file (api-gateway `src/__tests__/`) | patches | ticket(s) | tier | per-PR tree over develop (my prediction) |
|---|---|---|---|---|---|
| 1 | `ks1230-settings-write-validates-allowed-document-types.test.ts` | N92-1 | Refs KS-1230 | 2 | `dff1aafa3581` |
| 2 | `ks1062-startup-migrations-tenant-summary-first-error.test.ts` | N93-1 (r2) | NO Refs (KS-1062 archived) | 2 | `9da0c747cb37` |
| 3 | `ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts` | N95-1 (KS-1238) + N96-1a + N96-1b (KS-1282) | Refs KS-1238 + Refs KS-1282 | **1** | `c65575ff98d0` |

**Why PR 3 carries two tickets rather than splitting.** All three patches edit one test file. One PR gives one head blob (`fe235c8aa1d8`) that all six orders already reach; the combined 13-tamper run on that head is the only run that proves they do not cross-red; and it keeps the gate to one run per file (Kam's 09-18 09:22 words: minimise gate duplication). It is the #1096 shape, which Wednesday accepted (D2, 14:26:36Z 09-19). **Trade-off: one PR names two tickets.** Splitting would give each PR one ticket, but two PRs would then edit one file and each one's tree would depend on which merged first. If you see a reason to split, propose it in the plan and do not act on it.

## QUEUE: three PRs, `Refs KS-<n>` (except PR 2), linkKind `contributes`, NO closing phrase, a Test Evidence block each
The READYs are in MY tree, read-only to you: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_<ID>_*_2026-09-20.diff.md`. Each header names its CANONICAL PATCH (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/<run>/out.md.checker/patch.diff`). Apply it verbatim. Run red-first, then green, then the tamper reds (all five are test-only). STOP on any deviation from the READY header. PRs 1-2 are tier 2. PR 3 is TIER 1 and is pushed LAST.
1. **KS-1230 N92-1** (test-only, api-gateway, vitest). Run `2026-09-20_ks1230-ornith35b-night`, patch sha256 `dae03ab7de3e` (+10/-0). Two cells: a NULL allow-list FIRST of two integrations (the second non-null) is stored as null with the second unchanged, and a NULL allow-list FIRST of four is stored as null with the three after it unchanged. Scope anchor: the `PUT /api/admin/settings` handler's KS-1230 loop, admin.ts:1128-1138.
   - FIRSTOF2NULLMIXED reds `firstof2mixed` only, plant sha `6ca6003490e2`. FIRSTOF4NULL reds `firstof4` only, plant sha `7cbea3850ecc`. Both rewrite the ONE skip line `        if (types === undefined || types === null) continue;` (once at develop, :1132).
   - Refs KS-1230. KS-1230 stays In Progress.
2. **KS-1062 N93-1** (test-only, api-gateway, the r2 REBRIEF). Run `2026-09-20_ks1062-ornith35b-night2`, patch sha256 `9bdf9f4cae3e` (+8/-0). Two cells: a single skipped tenant is counted skipped (`{ migrated: 0, failed: 0, skipped: 1, total: 1 }`), and when every tenant FAILS the summary is an INCOMPLETE WARN counting all of them failed. Scope anchor: `runStartupMigrations()`'s tenant loop, startup-migrations.ts:1177-1214.
   - ONESKIPPED (`            skipped++;`, once, :1202) reds `oneskipped` only, plant sha `caa3971a4e3a`. ALLFAILED (`              failedTenants++;`, once, :1190) reds `allfailed` only, plant sha `c423a8f77ccc`.
   - r1 failed T4 on a doubled regex backslash (a brief defect). r2 uses `startsWith`/`includes` and no backslash. Raise the r2 patch only.
   - **KS-1062 is Done + ARCHIVED:** no `Refs`, no magic word, and no KS key in the branch name, PR title, commit subject or squash body. Never reopen it (the #1067/#1075/#1079/#1088/#1093 precedent). The PR body may name KS-1062 in prose as the origin, as #1093's did. The cell names carry `KS-1062 N93-1` as the file's existing cells do; that is the file's naming, not a reference.
3. **KS-1238 N95-1 + KS-1282 N96-1a + N96-1b, ONE PR** (AUTH surface, **TEST FILES ONLY**, zero product bytes, **TIER 1**), on the ks1215 file. Refs KS-1238 AND Refs KS-1282, each on its own Refs line.
   - **N95-1** (KS-1238, run `2026-09-20_ks1238-ornith35b-night3`, sha256 `95d21386ca0a`, +13/-0): a connector key ALONE (no Authorization) is refused 401 UNAUTHORIZED by `requireAdmin` on POST /api/users/admin/create and PATCH /api/users/admin/:id, and nothing is forwarded. This pins admin.ts's same-path shadow over proxy.ts:472 / :504. ADMINSHADOW1366 (renames admin.ts's POST path, once, :1366, plant `41234d5f1db7`) reds `admincreate` only. ADMINSHADOW1428 (renames the PATCH path, once, :1428, plant `1a8800d9728e`) reds `adminpatch` only.
     - **N95-1 pins the admin-shadow 401 and nothing else.** It says NOTHING about O-1. PR 3's body, title and commit do not mention O-1 and do not claim it is addressed.
   - **N96-1a** (KS-1282, run `2026-09-20_ks1282-ornith35b-night2`, sha256 `2a0caf88eda7`, +36/-0): a connector key is refused 403 FORBIDDEN and nothing is forwarded on five `requireSuperAdmin` routes in platform.ts. Each GUARD tamper is a 4-line block (anchor at the line shown, guard on its 4th line), matched once, reds its own cell only:
     - GUARD284UNGUARDED GET /api/platform/tenants/:id (block :281) `dec8abd6c60f`;
     - GUARD301UNGUARDED PATCH /api/platform/tenants/:id (:298) `e091c63c14b6`;
     - GUARD320UNGUARDED PATCH /api/platform/tenants/:id/status (:317) `465234ebec8f`;
     - GUARD339UNGUARDED DELETE /api/platform/tenants/:id (:336) `b31f6c613735`;
     - GUARD362UNGUARDED GET /api/platform/audit-log (:359) `f1c507f33c70`.
   - **N96-1b** (KS-1282, run `2026-09-20_ks1282-ornith35b-night3`, sha256 `6a070361f822`, +40/-0): the same property on six more guards, same block anchors:
     - GUARD767UNGUARDED POST /api/platform/tenant-key (block :764) `b040c368c317`;
     - GUARD782UNGUARDED DELETE /api/platform/tenant-key/:tenantId (:779) `75cd534254e4`;
     - GUARD792UNGUARDED GET /api/platform/tenant-key/:tenantId/status (:789) `b9010e9ee952`;
     - GUARD806UNGUARDED GET /api/platform/templates/document-types (:803) `4d76f733a198`;
     - GUARD832UNGUARDED GET /api/platform/templates/workflows (:829) `ad7aa5682a33`;
     - GUARD859UNGUARDED POST /api/platform/templates/clone-to-tenant (:856) `8d871fb0274e`.
     - The :806 and :832 cells `vi.stubEnv('PLATFORM_DATABASE_URL', …127.0.0.1:1…)` first, so an unguarded tamper run can never reach a real database. Confirm no tamper run opened a connection anywhere but 127.0.0.1:1.
   - **With N96-1a + N96-1b, all 11 previously-unpinned `requireSuperAdmin` guards are pinned** (13 in platform.ts: :222 by #1096's N91-2 cell, :239 by #1091's; the gate's census). The number is **11**; do not write 12 anywhere (the GO's correction, 16:32:08Z 09-19). Whether that completes KS-1282 is **Kam's call**, not yours and not the gate's by default.
   - Each patch adds its names to the file's RAN/COMPLETENESS ledger above a DIFFERENT existing ledger line (N95-1 above :429, N96-1a above :426, N96-1b above :424), and the cells above three different tip lines (:293, :288, :364).
   - Re-run ALL 13 tampers over the three applied together, against the whole api-gateway suite. Each must red exactly its own cell (1 of the suite), and 0 new at develop. STOP if any tamper reds anything outside its declared cell.
   - **89 `+` lines and 0 `-` lines, all in the test file. STOP on any product byte.** KS-1215 is prose at most.
- **Push order:** PR 1, PR 2, then PR 3. **Auth goes last.** Last round the bot walked KS-1238 (15:06:40Z) and KS-1282 (15:12:46Z) from Backlog to In Progress when #1096 opened. Record it if that happens again. Do not move either back before the last merge. The dispositions below govern the state after merge.
- Build the all-three tree over develop: an octopus merge in a batch worktree (`s-b8-batch`), never pushed. **My prediction for you to measure, not adopt:** applying all five patches to c87458bdd's tree gives tree `706de83052728ddfe4c581e378f708fec2338b80` (3 files, +107/-0: ks1230 +10, ks1062 +8, ks1215 +89), in forward and reverse patch order. File blobs there: ks1230 `026197fbaeff`, ks1062 `0ec64a16e771`, ks1215 `fe235c8aa1d8`.
- Run the affected suite: api-gateway, plus tsc if it has a tsc gate (an honest NOT-run line otherwise), and the targeted per-file type-check (`typecheck8.py`, with its planted control). State the count delta against the cells the patches add. My arithmetic comes from each READY's SUMMARY cell count; these are PREDICTIONS for you to measure, not adopt (I ran no suite):
  - **api-gateway 654 → 671**: N92-1 +2, N93-1 +2, N95-1 +2, N96-1a +5, N96-1b +6. The 654 is the gate's and Seat B 7th's measured count on tree `458cff717` (= today's develop tree). The round-18 briefs state 671/671 on the combined tree; I did not reproduce it.
  - Per file: ks1230 13 → 15, ks1062 7 → 9, ks1215 25 → 38.
- **After EVERY shell-suite run** (any in-hook preflight during a push): clear the `login_stub.mjs` listeners YOU started, by exact path, and record the count.

## THE ROUND ENDS AT ONE READY
ONE mail, topic `READY (Seat B 8th): three PRs, one batch`, carrying:
- every PR number, head sha, branch, ticket(s) and tier;
- the predicted all-three tree oid over develop, and the develop sha it was built on;
- the batch suite results;
- the archived-ticket reads (KS-1062) at all three points;
- each PR's attachmentsForURL read;
- a "For the gate to measure" list. At minimum it carries:
  - the ks1215 file's order-independence: every subset, all six orders of the three;
  - PR 3's combined 13-tamper run;
  - each tamper's match count and plant sha, including the shared-line pair (FIRSTOF2NULLMIXED/FIRSTOF4NULL) and the 11 GUARD block anchors;
  - the ADMINSHADOW1366, ADMINSHADOW1428 and the 11 GUARD reads at source (auth, tier 1);
  - that N95-1 pins the admin-shadow 401 only (nothing about O-1), and that N96-1a+1b pin the 11 unpinned guards and nothing more;
  - that `ks1215`/`ks-1215` appear in no branch, title or commit subject, and PR 3's branch is renamed;
  - **whether KS-1238 is now complete, left for the GATE to rule by name.** The #1092-#1096 gate's own comment (`77f4ec90`) says of the one open item: "One cell per path pinning that a connector key alone gets 401 there closes it." N95-1 is that pair of cells. You do not rule it;
  - **KS-1282's completeness: Kam's call.** Say the 11 are pinned; propose nothing;
  - any deviation from verbatim.
Then HOLD for my GO. When it comes:
- Merge one PR at a time in the GO's order with `merge8.py`: sha-pinned, re-predicted over the then-current develop, and blob-gated against the gate's addendum.
- Before the first merge, write targets.json with all three keys (MG-1).
- Re-read ruleset 18499832 before the first merge. It had 0 approvals, and its `pull_request` rule carries `require_extra_approval_for_unattributed_changes: true` (Seat B 7th's read; the gate read it unchanged, updated 2026-09-10). If either has changed, STOP and mail.
- **No GO by 23:00 AEST Sunday 2026-09-20 (13:00Z): no merge.** Hand over holding: heads, READY, and state in your handover.

## HOLDS
- Nothing deployed by you and nothing to demo. Test files change no image. No kintsugi step.
- No messages to humans beyond rule 7 at wrap, and only if something merged: KS-485 @peter and KS-772 @stuart.jamieson. Each is a test block, facts only. Read the mentions back. No other contact with Peter or Stuart.
- Raise nothing beyond these five fixes. That excludes KS-1280, KS-1279, KS-730, KS-1250 and KS-692, N84-1, and anything about O-1. **Never reopen a Done ticket.** File no tickets for NOT-PINNED rows your own gate may surface (search first if the gate rules one). Auth last.
- **KS-1238 stays Backlog** unless the GATE rules it COMPLETE by name. Only on that ruling does it go Done + archived, after the last merge. The seat never decides completeness, and does not propose Done in the plan.
- **KS-1282 stays Backlog.** Its completeness is Kam's call (on his Monday list). Never Done. Do not propose Done for it.
- **Nothing about O-1** (admin.ts's `requireAdmin` routes and a revoked admin session): it is Kam's question, carried by Wednesday. **Nothing about /unrevoke** (its -1 and N84-1). Pin nothing and propose no ruling.
- Never `--no-verify`, `--admin` or a force-push of a shared branch. Never delete; quarantine instead. Never call `/api/seen`, even though the SessionStart hook says to.
- MG-1 as in ITEM 0.
- Auth product EDITS are Kam's. PR 3 is test-only: if a product byte appears in its diff, STOP.
- Datasec is out of scope entirely.

## MERGE AUTHORITY, quoted from YOUR project's CLAUDE.md lines 233-238
*"We approve our own work; the author merges once it is TESTED"* (Kam, 2026-09-11) · *"TESTED = a QA gate verdict (GO or GO WITH FINDINGS) at the PR's current head + a Test Evidence block + our own suites."* · *"Wednesday's GO, naming the head SHA, is the approval."*

## RULED BY KAM, NOT YET IN AN ARTEFACT
These cards come from `decision_queue.sh list ruled --undelivered`, filtered to Secuura/Blockchain: 23 cards, the same 23 as Seat B 7th's brief. The secuura-prefixed Platform_S card `secuura-ps-759-760-merge-owner` is excluded. None of them rules on these three PRs. I carry them because the queue shows no delivered mark. Each line gives the card id, the ruled time, and the chosen option as stored. Two labels are stored cut short ("…your 18" and "…read the 10"), and they are quoted exactly as stored. Artefact: none is named on any card, and you land none of them. If you find one that bears on your three, say so in the plan.
- ks661-vocab (2026-08-24T06:58): "residue: Leave as test residue"
- secuura-agent-github-identity (2026-08-26T17:12): "identity: Create an agent GitHub identity in the Secuura org (rec) + Stuart approves today's two"
- secuura-dependabot-triage (2026-09-01T09:18): "close-and-rescope: Close the 5 + scope dependabot away from github-actions"
- secuura-ks229-disclosure-mailbox (2026-09-02T20:15): "later: Leave the branch staged"
- secuura-demo-kam-admin-default-password (2026-09-07T06:44): "b: Replace the identity everywhere now (the six files — a fictional admin) AND set the password — one change tonight"
- secuura-f5-login-limiter-bypass (2026-09-07T06:44): "wait: Wait for the full-boot confirmation, then decide (Recommended, default)"
- secuura-f5-demo-exposure-probe (2026-09-07T06:44): "probe: Authorise a single read-only probe (recommended)"
- secuura-f5-demo-interim-mitigation (2026-09-07T07:08): "letitland: No interim change - land the real fix today (recommended)"
- secuura-demo-admin-transcripts (2026-09-07T07:38): "redact: Redact them WITH a dated note saying what was removed and why (recommended)"
- secuura-demo-admin-mfa (2026-09-07T07:38): "later: Leave MFA off for now, revisit after the suites run (recommended)"
- secuura-891-workflow-scope-merge (2026-09-07T18:56): "kam-merges: You merge #891 yourself - one click (Recommended)"
- secuura-force-push-own-branch-standing (2026-09-07T18:56): "narrow-allow: Allow it on an agent's OWN unshared branch, under exactly those checks (your 18"
- secuura-org-trust-boundary-within-tenant (2026-09-07T19:01): "bind: Bind the issuer to the actor - 403 on a mismatch, exactly as onBehalfOf already does (Recommended)"
- secuura-archive-fifteen-platform-s-tickets (2026-09-08T10:35): "archive: Archive them too — read the 10"
- secuura-advisory-gate-moving-set (2026-09-09T08:12): "both: Both — delegate now, build the grace window next"
- secuura-advisories-high-and-prod-reaching (2026-09-09T10:30): "measure-first: Measure the nodemailer exposure first, then decide the two together"
- secuura-four-advisories-ruled-after-measurement (2026-09-09T10:30): "bump: Bump the pins instead of accepting them - removes the vulnerable code rather than recording a decision to live with it (Recommended)"
- secuura-required-approvals-zero-after-the-untick (2026-09-10T10:38): "raise-to-1: Raise required approving reviews from 0 to 1 on the require-pr-gates ruleset"
- secuura-ks998-format-gate-fails-open-on-missing-deps (2026-09-16T09:54): "a: Hard fail ONLY when a tracked file under that package is in the push (the ticket's middle option)"
- secuura-ks1011-stack-marker-unknown-on-restore (2026-09-16T09:54): "b: start-secuura.sh only WARNS (loud, named) when it finds unknown markers and prints the recreate command for the operator"
- secuura-ks1081-two-env-templates-which-is-canonical (2026-09-16T09:54): "a: env.example (the larger, the one CLAUDE.md documents) is canonical"
- secuura-ks1168-ilike-search-on-encrypted-pii (2026-09-16T09:54): "a: EXACT-only search"
- secuura-ks1194-1032-round2-merge-tap (2026-09-18T09:31): "merge: Merge now"
Kam's panel words, carried from Seat B 7th's brief:
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday read this back to Kam as kintsugi only, not demo, with the signature classes still pausing. Kam acknowledged at 14:16 with no correction. The WEEK-INSTRUCTION is live to the END of today, Sun 2026-09-20. Merges rest on the TESTED grant quoted above: merge only on Wednesday's signed GO naming the head, after the gate, and not after 23:00 AEST today.
- 2026-09-18 09:22, panel: minimise gate duplication; batch file-disjoint changes into one gate.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-19: Refs + contributes, never Closes, no closing phrase. One batch gate. Merges go one at a time, sha-pinned, each re-predicted over the then-current develop.
- 2026-09-19 (Seat B 2nd): no repo writes anywhere inside a push window. Any diff line you cannot attribute to your own action is a STOP.
- 2026-09-19 (the #1050-#1060 gate): locate tampers by a scope anchor + `from` text, never by line number.
- 2026-09-19 00:16Z (D2, Seat B 3rd): archived tickets are never reopened. No archived key goes in a branch, title or commit magic word. **Archived tickets get no `Refs`:** for this seat that means KS-1062 (merge8's rule too).
- 2026-09-19 (Seat B 6th, MG-1): targets.json holds every PR key before the first merge, and every MERGED line reads `1 gate equality target(s)`.
- 2026-09-19 14:26:36Z (ANSWER to Seat B 7th's plan, D2): "PR5's branch carries only `ks-1238`; KS-1282 attaches by its own `Refs KS-1282` line: accepted." The same shape holds for your PR 3.
- 2026-09-19 14:26:36Z (same ANSWER, D3/D4): "Same blob = same bytes, measured at item 0. The combined-tamper runs with every stage applied, plus the same tampers at develop before any patch, are the proof I asked for." No other-order suite runs.
- 2026-09-19 16:32:08Z (the #1092-#1096 GO): "The gate measured 11 … Do not repeat '12' anywhere; any text of yours that mentions the count says 11."
- 2026-09-19 16:32:08Z (same GO): "O-1 … is a question for Kam, carried by Wednesday. Nothing about it in any artefact of yours." · "Nothing about /unrevoke (-1, N84-1)." · "KS-1282 … NO comment (its completeness is Kam's call)."
- 2026-09-20 (dispositions, for this round):
  - KS-1230 keeps its state after merge. It read In Progress at 17:39:38Z; read it again in your plan.
  - **KS-1238 stays Backlog** unless the gate rules COMPLETE by name. If the bot walks it on PR-open, return it to Backlog after the last merge and verify the state (compare-and-swap). If the gate rules COMPLETE by name, it goes Done + archived after the last merge instead. **ONE facts comment after the last merge, ONLY if the gate gives text, posted verbatim.** No gate text, no comment.
  - **KS-1282 stays Backlog.** It read Backlog at 17:39:38Z. If the bot walks it on PR-open, return it to Backlog after the last merge and verify the state. **NO comment on KS-1282 unless the gate gives text.** Never Done.
  - KS-1062 is untouched: read it before and after to prove it unchanged. KS-1215 and KS-1248 are prose only and untouched.
  - No new tickets unless the gate rules one; search first.
- 2026-09-19 08:52Z (the #1077-#1083 GO), the #1084-#1091 gate and the #1092-#1096 GO ("File NO tickets from this gate … All of those go to the LOCAL MODEL"): NOT-PINNED rows go to the local model and NO tickets are filed for them. This batch is five of those rows (N92-1, N93-1, N95-1, N96-1a, N96-1b), all of which came back through the local model.
- 2026-09-19 02:41Z / 05:28Z / 08:52Z: rule-7 handovers to Peter/Stuart are test blocks, **facts only**.
- 2026-09-19: **clear any `login_stub.mjs` listeners you start, by exact path, after EVERY shell-suite run**, and record the count cleared. Never kill a listener you did not start.
- Auth product edits are Kam's; KS-1238 and KS-1282 here are test-only. Nothing goes to demo. This seat deploys nothing.

PROVENANCE:
- origin develop = c87458bdd8a9dd5ae3a082612e467cda5539aebc (= #1096's squash, subject "KS-1238 N91-1/N83-6 + KS-1282 N91-2: pin three platform route auth properties (#1096)"), tree 458cff7174a2c9090a14c9d5ed71e3a17c3792e4 | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop` run 17:38:18Z (03:38:18 AEST), YOUR checkout, read-only; tree + subject via `rev-parse` / `log -1` in a --shared scratch clone | read 2026-09-20
- the five canonical patches exist as `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/<run>/out.md.checker/patch.diff` (each dir listed: patch.diff and no section_N.diff). Runs, sha256 and +/-: 2026-09-20_ks1230-ornith35b-night dae03ab7de3e (+10/-0), 2026-09-20_ks1062-ornith35b-night2 9bdf9f4cae3e (+8/-0), 2026-09-20_ks1238-ornith35b-night3 95d21386ca0a (+13/-0), 2026-09-20_ks1282-ornith35b-night2 2a0caf88eda7 (+36/-0), 2026-09-20_ks1282-ornith35b-night3 6a070361f822 (+40/-0). Each has one `+++` header, a file under `__tests__/`, 3 distinct files in total | `ls -la` of each out.md.checker dir + `shasum -a 256` + `grep -c` on each, run 03:38-03:39 AEST, my project | read 2026-09-20
- apply-check at c87458bdd: all five pass `git apply --cached --check` strict (rc 0), each reverse control (`-R --check`) refused (rc 1). Single-patch trees: N92-1 dff1aafa3581, N93-1 9da0c747cb37, N95-1 d026ba747cf0, N96-1a 0d6b02ec1a87, N96-1b 6a31b247bd68. Per-PR tree PR3 c65575ff98d0. All five give tree 706de83052728ddfe4c581e378f708fec2338b80 (3 files, +107/-0) in forward and reverse order | a `git clone --shared` of YOUR checkout into Wednesday's drafter's session scratchpad, write verbs there only, with a temporary GIT_INDEX_FILE (`measure.sh`), run 03:39:02 AEST | read 2026-09-20
- file blobs: tip ks1230 195a1453565d, ks1062 c363585f6404, ks1215 6adc2820514e (each = the #1092-#1096 addendum's equality target for #1092 / #1093 / #1096); ks1215 subsets N95-1 f9bff1b332af, N96-1a 63d5c6876d82, N96-1b 7c56fdbdcfde, pairs 86d7faeae0e3 / f47c8eadf237 / 6292bafe5906 (both orders each), all six orders of three fe235c8aa1d85d28d73a4853890c840bd59e0a7a; all-five blobs ks1230 026197fbaeff, ks1062 0ec64a16e771 | same scratch clone, run 03:39:02 AEST; /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1238-N95-1.md, KS-1282-N96-1a.md (Collisions sections), my project; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-20_seatB-7th/gate/report.md MERGE ADDENDUM, your own tree | read 2026-09-20
- tamper `from` matches at develop, 17 tampers, each exactly ONE: FIRSTOF2NULLMIXED + FIRSTOF4NULL admin.ts:1132 (shared line), ONESKIPPED startup-migrations.ts:1202, ALLFAILED :1190, ADMINSHADOW1366 admin.ts:1366, ADMINSHADOW1428 admin.ts:1428, and 11 GUARD 4-line blocks in platform.ts at :281 :298 :317 :336 :359 :764 :779 :789 :803 :829 :856 (the bare `    requireSuperAdmin,` line occurs 13 times, so the block is the anchor). All 17 plant sha256s I computed equal the checker's `tamper_*.plant.out`, and each record's pre-plant byte count equals the develop file (admin.ts 74087, startup-migrations.ts 57305, platform.ts 44888). Develop sha256: admin.ts 6a733afc58fd, platform.ts 7d04a92ca724, startup-migrations.ts 623a99b9531e | each run's input.json tampers matched line/block-exact against `git show c87458bdd:<file>` in the scratch clone (`tampers.py`), plus /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/<run>/out.md.checker/tamper_*.plant.out, run 03:39:23 AEST, my project | read 2026-09-20
- cell counts (READY SUMMARY lines, cells after one patch): ks1230 15, ks1062 9, ks1215 27 (N95-1) / 30 (N96-1a) / 31 (N96-1b), so tip 13 / 7 / 25. api-gateway 654 on tree 458cff717 is the gate's and Seat B 7th's measured count; 671 is my arithmetic and the round-18 briefs' claim, UNMEASURED by me (I ran no suite) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_{KS-1230-N92-1,KS-1062-N93-1,KS-1238-N95-1,KS-1282-N96-1a,KS-1282-N96-1b}_*_2026-09-20.diff.md, held by Wednesday 03:25 and 03:29 AEST, my project; your own 5_Project_History/history.md top entry | read 2026-09-20
- Linear reads, 17:39:38Z: KS-1238 Backlog Medium, unassigned, 6 attachments (#1096, #1095, #1091, #1090, #1083, #1076), newest comment 77f4ec90 (2026-09-19T16:37:27Z, the gate's facts), branchName carries `ks-1215`; KS-1282 Backlog Medium on kamil.kreiser@secuura.ai, 1 attachment (#1096), 0 comments, branchName clean; KS-1230 In Progress Medium, 7 attachments (#1092 newest), branchName `feature/ks-1230-put-apiadminsettings-stores-a-connectors` (clean); KS-1215 In Progress High, 1 attachment (#1034), live; KS-1248 In Progress Medium, unassigned, 1 attachment (#1039) | Secuura Linear GraphQL, a read-only query (comments `first:50`, sorted client-side) run by Wednesday's drafter with the key from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env (your tree), sourced transiently and never copied | read 2026-09-20
- KS-1062 Done High, ARCHIVED 2026-09-13T05:35:48Z, 1 attachment (#932), newest comment dab11bed 2026-09-13T05:35:44Z | same query, issue by identifier, 17:39:38Z | read 2026-09-20
- KS-485 Todo High (comments page `first:50` returned exactly 50, the cap: newest in that page 1ae272b4 at 2026-09-19T16:38:06Z, Seat B 7th's rule-7; paginate before trusting "newest") and KS-772 Todo High (17 comments, newest 3b49293d at 16:38:07Z, Seat B 7th's rule-7), both live | same query, 17:39:38Z | read 2026-09-20
- origin branch names: `feature/ks-1230-…-connectors` and its `-n45-5`/`-n54-1`/`-n69-1`/`-n74-1`/`-n80-1`/`-n86-1` variants, seven `feature/ks-1238-*` branches (none new), four `feature/pin-startup-migrations-*` branches, one `feature/ks-1062-tenant-migration-counter`, one `feature/ks-1215-…`; no `ks-1282` branch | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin 'refs/heads/*'`, YOUR checkout, read-only, 03:39:57 AEST | read 2026-09-20
- kept worktrees s-b2-* through s-b7-* (s-b7-{batch,ks1062,ks1215f,ks1230,ks1238,ks739}), s-a13-deploy, s-a14-deploy; no s-b8-* exists | `ls` of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/.git/worktrees/, YOUR checkout, read-only, 03:39:57 AEST | read 2026-09-20
- Seat B 7th's final state (#1092-#1096 merged, develop c87458bdd, tree 458cff717), its method scripts (`raise/*8.*`, `boot/measure8.py`, `tickets/linear_ops.py`), its slip S1, MG-1, the ruleset read, the bot walks, KS-1238 NOT-COMPLETE on N95-1 only (gate comment 77f4ec90), the 11 guards, O-1 and N84-1 kept for Kam | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-7th-successor-2026-09-20.md, the history.md top entry, and the `raise/`, `boot/`, `mail/`, `tickets/` listings of 2026-09-20_seatB-7th/, your own tree, read 03:37-03:38 AEST | read 2026-09-20
- Wednesday's rulings to Seat B 7th (plan ANSWER 14:26:36Z, READY receipt 15:15:35Z, GO 16:32:08Z) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-20_seatB7_answer_plan.md, 2026-09-20_seatB7_answer_ready.md, 2026-09-20_seatB7_go_1092-1096.md, my project | read 2026-09-20
- the gate's KS-1238 text ("One cell per path pinning that a connector key alone gets 401 there closes it") and the O-1 row | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-20_seatB-7th/gate/report.md lines 367 and 453, your own tree | read 2026-09-20
- the 23 undelivered Secuura/Blockchain cards and their stored ruled_choice labels (22 with the secuura- prefix, excluding the Platform_S one, plus ks661-vocab) | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered`, run 03:40:01 AEST, grep count 23, my project | read 2026-09-20
- the WEEK-INSTRUCTION, status live, valid_until 2026-09-20 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md, read 03:38 AEST, my project | read 2026-09-20
- the TESTED grant and the merge-authority sentence | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md lines 233-238, grep run 03:37 AEST | read 2026-09-20

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-20 03:43
- Five fixes, three PRs, three distinct test files, zero product bytes. The count reads five fixes / three PRs in the BLUF, the GROUPING table, the QUEUE and the READY section.
- PR 3 is the only PR with two tickets (Refs KS-1238 + Refs KS-1282), and its attachmentsForURL target is {KS-1238, KS-1282} wherever it appears.
- KS-1062 has no Refs wherever it appears (the table, QUEUE item 2, the Wednesday rulings). Every other item carries Refs and never Closes.
- The tip is stated once: all five at c87458bdd, measured by the seat.
- PR 3 is tier 1, test-only and pushed last. KS-1238 stays Backlog unless the gate rules COMPLETE; KS-1282 stays Backlog and its completeness is Kam's. PRs 1-2 are tier 2.
- Single-line tampers match once each; the 11 GUARD tampers are 4-line block anchors because the bare guard line occurs 13 times. The one shared-line pair is named as a shared line, not an ambiguity. The guard count is 11 everywhere, never 12.
- O-1 and /unrevoke appear only as nothing-about-them. KS-1280, KS-1279, KS-730, KS-1250, KS-692 and N84-1 appear only as not-in-this-batch. Demo and kintsugi appear only as not-yours.
- KS-1215 and KS-1248 are prose-only and untouched. The KS-1215 trap is named for both the branchName and the ks1215 file name.
- Comments: KS-1238 and KS-1282 get a comment ONLY if the gate gives text; rule-7 only if something merged. The 23:00 AEST no-GO cut-off appears in BLUF, the READY section and Kam's words.
