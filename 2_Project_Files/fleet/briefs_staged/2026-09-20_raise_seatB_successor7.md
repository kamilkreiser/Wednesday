Seat B 7th successor (Secuura/Blockchain), from Wednesday

⚠ ONE SEAT ON THIS INBOX. This brief is for **Seat B 7th**. Your job is to raise eight held local-model test-only fixes as FIVE PRs, one per test file. Seat B 6th wrapped at ~13:25Z on 2026-09-19 after merging #1084-#1091. Wednesday is launching no other Secuura seat beside you. If a mail names another seat, it is not for you. You touch ONLY the files below, each in your own `s-b7-*` worktree. Never touch the kept `s-b2-*`, `s-b3-*`, `s-b4-*`, `s-b5-*`, `s-b6-*`, `s-a13-deploy` or `s-a14-deploy` worktrees, and never the box.

## BLUF
**One job: raise EIGHT test-only fixes that the local model wrote and Wednesday held (23:51 on 09-19 and 00:06 on 09-20) as FIVE PRs, one per test file (the grouping is below). Then mail me ALL five heads in ONE READY so I can gate them as ONE batch.** They touch five separate test files and zero product bytes. Nothing merges without my signed GO naming the head. Kam is away until Monday; his standing words are quoted below. This seat deploys nothing: test files do not change a runtime image, so there is no kintsugi step and nothing goes to demo.

## ITEM 0: boot, before any write
- Read Seat B 6th's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-6th-successor-2026-09-19.md`. Also read the top entry of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (Seat B 6th). Seat B 6th's raise method is YOUR method. Copy its scripts into your own `2026-09-20_seatB-7th/` record folder rather than editing them in place:
  - `2026-09-19_seatB-6th/raise/`: `raise7.py`, `lanes7.sh`, `msgs7.py`, `commit7.py`, `wtadd7.sh`, `deps7.sh`, `batch_build7.sh`, `batch_suites7.sh`, `typecheck7.py`, `linear_reads7.py`, `push7.sh`, `bodies7.py`, `open_prs7.py`, `series7.py`, `targets7.py` and `merge7.py`;
  - `boot/measure7.py` (item 0 as reads only), `boot/tickets_boot7.py`, `boot/open_prs7.py`, `boot/grant_verify.py`;
  - `mail/ready7.py`, `mail/send.py`, `mail/watch.sh`.
  - There are NO repo writes inside a push window, anywhere.
  - Clear the `login_stub` listeners by exact path. None of this batch is a shell suite, but an in-hook preflight during a push is.
  - Locate every tamper by its `from` text plus a scope anchor, never by line number. This round every `from` matches exactly ONCE at develop (my count, below), so the `from` is its own anchor. Two pairs share a line: FIRSTOF3NULL and ALLNULL3 both plant admin.ts:1132, and NOJSON502 and NOJSON504 both plant documents.ts:1722. Each pair has one `from` and two different `to`s. Show each plant's sha256 equals the checker's record.
  - Use `merge7.py` for the merges. It never writes an archived key as `Refs`.
  - Avoid the recorded slips:
    - Seat B 4th's four: S1 the section regex with no control; S2 `grep -P` on BSD, which left the push specs empty; S3 a commit message that claims more than the head shows; S4 the linear_reads history sort on mixed None;
    - Seat B 5th's one: a `ps | grep -c` that counted its own grep;
    - Seat B 6th's: S1 a series driver that retried Linear 429 only (a 503 stopped it; `series7.py` now retries 5xx and resumes without re-pushing); S2/S3 an unquoted zsh `$VAR` that did not word-split (use an array or a function, with a control).
- **Carry Seat B 6th's MG-1 lesson.** Write `raise/targets.json` with EVERY PR key BEFORE the first merge. Each key holds exactly one equality target, and each target is its head's blob. Every MERGED line must read `1 gate equality target(s)`. `merge7.py` STOPs otherwise. Build targets.json and the merge messages with `targets7.py` from the gate's addendum.
- origin develop = `4273adfac57ab1a65b4a9983c566cc115faefc01`, tree `f76901ed9cfae15ce6580ff24ebcbbea22bd36fb`. That is my ls-remote read at 00:07 AEST 2026-09-20 (14:07Z on 09-19). It is #1091's squash, and all eight READYs were written AT this tip. Re-read it yourself. If develop has moved, re-run every apply-check and prediction below over the new tip and STOP on any change to a target or tamper file.
- **All eight canonical patches are `patch.diff`** in their run's `out.md.checker/` dir. Each READY header names its path, and all eight exist (my `ls` + sha256, 00:07 AEST). All eight are `mode=modify` on a test file that exists at develop, and all have 0 `-` lines. Use ONLY the header's CANONICAL PATCH path. Trust no other wording in a header.
- For each of the eight, measure the following, and let a changed file STOP that item only:
  - `git apply --check` strict at develop, with a reverse control;
  - the target blob and each tamper file's blob, at 4273adfac against develop.
- **Order-independence (two files carry more than one patch).** My both-order reads, in a scratch clone at 4273adfac:
  - **ks1238 file** (N90-1 + N83-2): both orders give blob `156f708272707fe2c13f9e5cfac9c2035bb42f9d`. Tip blob `0a37c1d56be8`; N90-1 alone `1cb8a72ddaa1`; N83-2 alone `7157d51b1bd7`.
  - **ks1215 file** (N91-1 + N83-6 + N91-2): all SIX orders give blob `6adc2820514ee191df201c1cbfea2062c9b12f14`. Tip blob `e2a4b12be53b`; N91-1 alone `38637220d155`; N83-6 alone `0bced4733ee7`; N91-2 alone `68beb8ee6699`. The KS-1238 pair alone (N91-1 + N83-6) gives `7007f002aa53` in both orders.
  - These equal the round-17 briefs' own proofs. Re-measure them yourself, every order.
- **Archived tickets:** KS-1062 and KS-739 are **Done + ARCHIVED**. Read each one's state, archivedAt and attachments at three points: before your first push, after its PR opens, and at READY. Report all three reads. **Never reopen a Done ticket.**
- **Branch names:** for every live ticket, read Linear's branchName and check it for any foreign key before you use it. My read at 00:08 AEST:
  - **KS-1238's branchName carries `ks-1215`** (`feature/ks-1238-f-1-four-properties-the-ks-1215-connector-bearer-fix-relies`). Rename both KS-1238 branches.
  - **KS-1282's branchName is new and clean:** `feature/ks-1282-get-apiplatformtenants-the-requiresuperadmin-guard`.
  - KS-1230's is clean.
  - The ks1215 test file name notwithstanding, keep `ks1215` and `ks-1215` out of every branch name, PR title and commit subject. They name a LIVE ticket (KS-1215, In Progress), and Linear links a key written in those places.
  - Run a zero-at-origin name check for each branch. My ls-remote at 00:08 AEST shows that `…-n80-1` and both `ks-1238-n83-*` branches already exist (merged).
  - **After EACH push and after each PR opens, measure `attachmentsForURL` for that PR.** It must show exactly the ticket(s) it Refs: none for the two archived items, and exactly KS-1238 + KS-1282 for PR 5. A link to KS-1215, KS-1248 or any other key is a STOP: report it before you push the next branch.
- Plan confirmation (QUESTION mail, topic `plan confirmation (Seat B 7th)`) goes out before the first write. It carries your D8 proposal: the ticket state of each item after merge. Wednesday's D8 is below; read each ticket now and report it.

## GROUPING: one PR per test file
| PR | test file | patches | ticket(s) | tier | per-PR tree over develop (my prediction) |
|---|---|---|---|---|---|
| 1 | api-gateway `ks1230-settings-write-validates-allowed-document-types.test.ts` | N86-1 | Refs KS-1230 | 2 | `d041e0287f7b` |
| 2 | api-gateway `ks1062-startup-migrations-tenant-summary-first-error.test.ts` | N88-1 | NO Refs (KS-1062 archived) | 2 | `fdd54f5b9093` |
| 3 | originate `ks739-transfer-custody-lookup-4xx-mapping.test.ts` | N89-1 | NO Refs (KS-739 archived) | 2 | `9acede956705` |
| 4 | api-gateway `ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts` | N90-1 + N83-2 | Refs KS-1238 | 1 | `a2880e5ea3ee` |
| 5 | api-gateway `ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts` | N91-1 + N83-6 (KS-1238) + N91-2 (KS-1282) | Refs KS-1238 + Refs KS-1282 | 1 | `019bd34ca03e` |

**Why PR 5 carries two tickets rather than splitting KS-1282 out.** All three patches share one test file AND one tamper file (`platform.ts`: REFRESHNOAUTH :254, IV_REGLIVEONLY :491, TENANTSGETUNGUARDED :219-222). One PR gives one head blob that all six orders already reach. The combined three-tamper run on that head is the only run that proves they do not cross-red. It also keeps the gate to one run per file (Kam's 09-18 09:22 words: minimise gate duplication). Its `attachmentsForURL` stays exact, as {KS-1238, KS-1282}. **Trade-off: one PR names two tickets. Splitting would give each PR a single ticket, but two PRs would edit one file, each one's tree would depend on which merged first, and the file would be gated twice.** If you see a reason to split, propose it in the plan and do not act on it. The split would be KS-1238 pair tree `ebfb6f76a058`, then KS-1282 alone `cf57d8e8f0ad` over develop, as siblings on develop, never stacked. After both merge, the file reaches the same `6adc2820514e`.

## QUEUE: five PRs, `Refs KS-<n>` (except PRs 2 and 3), linkKind `contributes`, NO closing phrase, a Test Evidence block each
The READYs are in MY tree, read-only to you: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_<ID>_*.diff.md`. Each header names its CANONICAL PATCH (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/<run>/out.md.checker/patch.diff`). Apply it verbatim. Run red-first, then green, then the tamper reds (all eight are test-only). STOP on any deviation from the READY header. PRs 1-3 are tier 2. PRs 4 and 5 are TIER 1.
1. **KS-1230 N86-1** (test-only, api-gateway, vitest). Run `2026-09-19_ks1230-ornith35b-night5`. Two cells: a NULL allow-list FIRST of three integrations is stored as null with the two after it unchanged, and three NULL allow-lists are all stored as null (admin.ts:1132).
   - FIRSTOF3NULL reds BOTH cells (declared), plant sha `928cd340d396`. ALLNULL3 reds the all-null cell, plant sha `166ac35794bd`.
   - Refs KS-1230.
2. **KS-1062 N88-1** (test-only, api-gateway). Run `2026-09-19_ks1062-ornith35b-night4`. One cell: when every tenant is skipped, all are counted skipped and the summary is complete with none migrated (startup-migrations.ts:1202).
   - ALLSKIPPEDZERO reds it, plant sha `37872084b6f9`.
   - **KS-1062 is Done + ARCHIVED:** no `Refs`, no magic word, and no archived key in the branch name, title or commit. Never reopen it (the #1067/#1075/#1079/#1088 precedent). The body may name KS-1062 in prose as the origin.
3. **KS-739 N89-1** (test-only, originate, jest). Run `2026-09-19_ks739-ornith35b-night7`. Three cells: a non-JSON 422 from the recipient lookup is still 400 VALIDATION_ERROR (documents.ts:1674), and a non-JSON 502 and a non-JSON 504 are each still 502 BAD_GATEWAY from the upstream branch, not the catch (:1722).
   - NOJSON422 (`f645833929d6`), NOJSON502 (`2265f3417115`) and NOJSON504 (`5cab73f735fe`) each red exactly their own cell.
   - **KS-739 is Done + ARCHIVED:** no `Refs`, no magic word, no archived key in the branch name, title or commit. Never reopen it (the #1066/#1075/#1082/#1089 precedent). Prose only.
4. **KS-1238 N90-1 + N83-2, ONE PR** (AUTH surface, **TEST FILES ONLY**, zero product bytes, **TIER 1**), on the ks1238 file.
   - **N90-1** (run `2026-09-19_ks1238-ornith35b-night7`): a found-document double makes the anchoring-verify forward (verification.ts:597-598) reachable. One cell: a valid key plus a REVOKED session JWT, with the exchange refused, sends no Bearer to originate or to anchoring verify. RAW598 is a 2-line BLOCK tamper that reds exactly that cell (plant `33f70ca97352`).
   - **N83-2** (run `2026-09-20_ks1238-ornith35b-night`): it adds a third key `CREATE_KEY` (documents:write, exchange refused) and a recorder line for originate's `POST /api/documents`. One cell: document create with a REVOKED JWT reaches originate with no Bearer (verification.ts:1297). RAW1297 reds exactly that cell (plant `d5188b1d3fb6`).
   - Re-run BOTH tampers over the pair applied together, against the whole api-gateway suite. Each must red exactly its own cell, and 0 new at develop.
   - **The pair has 16 `+` lines and 0 `-` lines, all in the test file. STOP on any product byte in the diff.** Refs KS-1238 only.
5. **KS-1238 N91-1 + N83-6 and KS-1282 N91-2, ONE PR** (AUTH surface, **TEST FILES ONLY**, **TIER 1**), on the ks1215 file. Refs KS-1238 AND Refs KS-1282, each its own Refs line.
   - **N91-1** (KS-1238 (iii), run `2026-09-19_ks1238-ornith35b-night6`): a super-admin JWT on POST /api/platform/tenants reaches tenant-provisioning and refresh-tenants with its own post-auth Bearer. This pins TODAY's platform.ts:254 (the READY: "presumes :254 kept"). REFRESHNOAUTH reds exactly that cell (`8dd8cfd7bca2`).
   - **N83-6** (KS-1238 (iv), run `2026-09-20_ks1238-ornith35b-night2`): register-connector with a LIVE user JWT on a REFUSED exchange sends no caller Bearer to /api/tenants, /api/keys or /api/audit. IV_REGLIVEONLY (a one-line insert on the platform.ts:491 anchor) reds exactly that cell (`23b787888893`).
   - **N91-2** (KS-1282, run `2026-09-20_ks1282-ornith35b-night`): a connector key is refused 403 FORBIDDEN on GET /api/platform/tenants, and nothing is forwarded. TENANTSGETUNGUARDED is a 4-line BLOCK (`  router.get(` / `    '/api/platform/tenants',` / `    authenticateToken(),` / `    requireSuperAdmin,`, to the first three) at :219-222. It matches once. It reds exactly that cell (`ecda4905a89e`). **It pins ONE of the 13 `requireSuperAdmin` guards in platform.ts, the :222 one.**
   - Each adds its name to the file's RAN/COMPLETENESS ledger, above three DIFFERENT trailing lines (:409, :410, :412).
   - Re-run ALL THREE tampers over the three applied together, against the whole api-gateway suite. Each must red exactly its own cell (1 of the suite), and 0 new at develop. STOP if any tamper reds anything outside its declared cell.
   - **STOP on any product byte.** KS-1215 is prose at most.
- **Push order:** PRs 1-3, then 4, then 5. **Auth goes last.** Last round the bot walked KS-1238 from Backlog to In Progress when its PR opened (Seat B 6th, 11:41:00Z). Record it if that happens again, for KS-1238 or KS-1282. Do not move either back before the last merge. D8 below governs the state after merge.
- Build the all-five tree over develop: an octopus merge in a batch worktree (`s-b7-batch`), never pushed. **My prediction for you to measure, not adopt:** applying all eight patches to 4273adfac's tree gives tree `458cff7174a2c9090a14c9d5ed71e3a17c3792e4` (5 files, +66/-0), in forward and reverse patch order.
- Run the affected suites: api-gateway, originate, and tsc for both if each has a tsc gate (an honest NOT-run line otherwise). State each suite's count delta against the cells the patches add. My arithmetic comes from each READY's reported cell counts. These are PREDICTIONS for you to measure, not adopt:
  - **api-gateway 646 → 654**: N86-1 +2, N88-1 +1, N90-1 +1, N83-2 +1, N91-1 +1, N83-6 +1, N91-2 +1. The round-17 briefs measured 651/651 with the five KS-1238/KS-1282 patches alone, which is consistent with this.
  - **originate 803 → 806**: N89-1 +3.
  - Per file: ks1230 11 → 13, ks1062 6 → 7, ks739 22 → 25, ks1238 9 → 11, ks1215 22 → 25.
- **After EVERY shell-suite run** (any in-hook preflight during a push): clear the `login_stub.mjs` listeners YOU started, by exact path, and record the count.

## THE ROUND ENDS AT ONE READY
ONE mail, topic `READY (Seat B 7th): five PRs, one batch`, carrying:
- every PR number, head sha, branch, ticket(s) and tier;
- the predicted all-five tree oid over develop, and the develop sha it was built on;
- the batch suite results;
- the archived-ticket reads (KS-1062, KS-739) before and after;
- each PR's attachmentsForURL read;
- a "For the gate to measure" list. At minimum it carries:
  - the order-independence of each multi-patch file: ks1238 both orders, ks1215 all six;
  - PR 5's combined three-tamper run and PR 4's combined two-tamper run;
  - each tamper's match count and plant sha, including the two shared-line pairs (FIRSTOF3NULL/ALLNULL3, NOJSON502/504);
  - the RAW598, RAW1297, REFRESHNOAUTH, IV_REGLIVEONLY and TENANTSGETUNGUARDED reads at source (auth, tier 1);
  - that N91-2 pins the :222 guard only, and that N91-1 pins today's :254;
  - the KS-1238 branch renames, and that `ks1215`/`ks-1215` appear in no branch, title or commit subject;
  - **whether KS-1238's F-1 list is now complete, left for the GATE to rule by name.** Seat B 6th's handover lists four open items: (iii) the super-admin cell for platform.ts:254 (N91-1), (iv) register LIVE+REFUSED (N83-6), verification.ts:598 (N90-1), and :1297 (N83-2). This batch carries a patch for each. You do not rule it;
  - any deviation from verbatim.
Then HOLD for my GO. When it comes:
- Merge one PR at a time in the GO's order with `merge7.py`: sha-pinned, re-predicted over the then-current develop, and blob-gated against the gate's addendum.
- Before the first merge, write targets.json with all five keys (MG-1).
- Re-read ruleset 18499832 before the first merge. It had 0 approvals, and its `pull_request` rule carries `require_extra_approval_for_unattributed_changes: true` (Seat B 6th's read). If either has changed, STOP and mail.

## HOLDS
- Nothing deployed by you and nothing to demo. Test files change no image.
- No messages to humans beyond rule 7 at wrap, and only if something merged: KS-485 @peter and KS-772 @stuart.jamieson. Each is a test block, facts only. Read the mentions back.
- Raise nothing beyond these eight fixes. That excludes KS-1280, KS-1279, KS-730, KS-1250 and KS-692. It also excludes the other 12 `requireSuperAdmin` guards and N84-1. **Never reopen a Done ticket.** File no tickets for NOT-PINNED rows your own gate may surface. Auth last.
- **KS-1238 stays Backlog/open** unless the GATE rules it COMPLETE by name. Only on that ruling does it go Done + archived, after the last merge. The seat never decides completeness, and does not propose Done in the plan.
- **KS-1282 stays open.** N91-2 pins one guard of thirteen, and whether one pin completes it is Kam's call. Do not propose Done for it.
- **Nothing about /unrevoke** (its -1 and its index-after-404 ordering, N84-1). Both are Wednesday's questions for Kam on Monday. Pin nothing and propose no ruling.
- Never `--no-verify`, `--admin` or a force-push of a shared branch. Never delete; quarantine instead. Never call `/api/seen`, even though the SessionStart hook says to.
- Auth product EDITS are Kam's. PRs 4 and 5 are test-only: if a product byte appears in either diff, STOP.

## MERGE AUTHORITY, quoted from YOUR project's CLAUDE.md lines 233-238
*"We approve our own work; the author merges once it is TESTED"* (Kam, 2026-09-11) · *"TESTED = a QA gate verdict (GO or GO WITH FINDINGS) at the PR's current head + a Test Evidence block + our own suites."* · *"Wednesday's GO, naming the head SHA, is the approval."*

## RULED BY KAM, NOT YET IN AN ARTEFACT
These cards come from `decision_queue.sh list ruled --undelivered`, filtered to Secuura/Blockchain: 23 cards, the same 23 as Seat B 6th's brief. The secuura-prefixed Platform_S card `secuura-ps-759-760-merge-owner` is excluded. None of them rules on these five PRs. I carry them because the queue shows no delivered mark. Each line gives the card id, the ruled time, and the chosen option as stored. Two labels are stored cut short ("…your 18" and "…read the 10"), and they are quoted exactly as stored. Artefact: none is named on any card, and you land none of them. If you find one that bears on your five, say so in the plan.
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
Kam's panel words, carried from Seat B 6th's brief:
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday read this back to Kam as kintsugi only, not demo, with the signature classes still pausing. Kam acknowledged at 14:16 with no correction. The WEEK-INSTRUCTION is live to the END of today, Sun 2026-09-20. Merges rest on the TESTED grant quoted above: merge only on Wednesday's signed GO naming the head, after the gate.
- 2026-09-18 09:22, panel: minimise gate duplication; batch file-disjoint changes into one gate.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-19: Refs + contributes, never Closes, no closing phrase. One batch gate. Merges go one at a time, sha-pinned, each re-predicted over the then-current develop.
- 2026-09-19 (Seat B 2nd): no repo writes anywhere inside a push window. Any diff line you cannot attribute to your own action is a STOP.
- 2026-09-19 (the #1050-#1060 gate): locate tampers by a scope anchor + `from` text, never by line number.
- 2026-09-19 00:16Z (D2, Seat B 3rd): archived tickets are never reopened. No archived key goes in a branch, title or commit magic word. **Archived tickets get no `Refs`:** for this seat that means KS-1062 and KS-739 (merge7's rule too).
- 2026-09-19 (Seat B 6th, MG-1): targets.json holds every PR key before the first merge, and every MERGED line reads `1 gate equality target(s)`.
- 2026-09-20 (D8, for this round):
  - KS-1230 keeps its current state after merge. It read In Progress at 00:08 AEST; read it again in your plan.
  - **KS-1238 stays Backlog** unless the gate rules COMPLETE. If the bot walks it on PR-open, return it to Backlog after the last merge and verify the state. If the gate rules COMPLETE by name, it goes Done + archived after the last merge instead.
  - **KS-1282 stays open.** It read Backlog at 00:08 AEST. If the bot walks it on PR-open, return it to Backlog after the last merge and verify the state.
  - KS-1062 and KS-739 are untouched. KS-1215 and KS-1248 are prose only and untouched.
- 2026-09-19 08:52Z (the #1077-#1083 GO) and the #1084-#1091 gate: NOT-PINNED rows go to the local model and NO tickets are filed for them. This batch is eight of those rows (N86-1, N88-1, N89-1, N90-1, N91-1, N83-2, N83-6, N91-2), all of which came back through the local model.
- 2026-09-19 02:41Z / 05:28Z / 08:52Z: rule-7 handovers to Peter/Stuart are test blocks, **facts only**.
- 2026-09-19: **clear any `login_stub.mjs` listeners you start, by exact path, after EVERY shell-suite run**, and record the count cleared. Never kill a listener you did not start.
- Auth product edits are Kam's; KS-1238 and KS-1282 here are test-only. Nothing goes to demo. This seat deploys nothing.

PROVENANCE:
- origin develop = 4273adfac57ab1a65b4a9983c566cc115faefc01, tree f76901ed9cfae15ce6580ff24ebcbbea22bd36fb (= #1091's squash, and Seat B 6th's predicted all-eight tree) | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 14:07:14Z (00:07 AEST), YOUR checkout, read-only; tree via rev-parse in a --shared scratch clone | read 2026-09-20
- the eight canonical patches exist, each at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/<run>/out.md.checker/patch.diff`. Runs and sha256: 2026-09-19_ks1230-ornith35b-night5 074cf04271ec (+10), 2026-09-19_ks1062-ornith35b-night4 4420bf9021b6 (+4), 2026-09-19_ks739-ornith35b-night7 b97934e86a26 (+18), 2026-09-19_ks1238-ornith35b-night7 fa799b570859 (+7), 2026-09-19_ks1238-ornith35b-night6 8a12edde92d5 (+6), 2026-09-20_ks1238-ornith35b-night a54519ecfc07 (+9), 2026-09-20_ks1238-ornith35b-night2 d993ff9e457e (+6), 2026-09-20_ks1282-ornith35b-night a9285782ab18 (+6). Each touches exactly one file under `__tests__/`, 5 distinct files in total, and none has a `-` line | ls + shasum -a 256 + grep on each, run 00:07 AEST, my project | read 2026-09-20
- apply-check at 4273adfac: all eight pass `git apply --cached --check` strict (rc 0), and each reverse control (`-R --check`) is refused (rc 1). Single-patch trees: N86-1 d041e0287, N88-1 fdd54f5b9, N89-1 9acede956, N90-1 b12c84b83, N91-1 e1b9b1764, N83-2 962925c2c, N83-6 309da08e2, N91-2 cf57d8e8f. Per-PR trees: PR4 a2880e5ea3ee (both orders), PR5 019bd34ca03e (all six orders), KS-1238-pair-only ebfb6f76a058. All eight together give tree 458cff7174a2c9090a14c9d5ed71e3a17c3792e4 (5 files, +66/-0) in forward and reverse order | a `git clone --shared` of YOUR checkout into Wednesday's drafter's session scratchpad, write verbs there only, with a temporary GIT_INDEX_FILE, run 00:08 AEST | read 2026-09-20
- file blobs: ks1238 file tip 0a37c1d56be8, both orders 156f708272707fe2c13f9e5cfac9c2035bb42f9d; ks1215 file tip e2a4b12be53b, all six orders 6adc2820514ee191df201c1cbfea2062c9b12f14, KS-1238 pair 7007f002aa53; these equal the round-17 briefs' own proofs | same scratch clone, run 00:08 AEST; /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1238-N83-2.md, KS-1238-N83-6.md, KS-1282-N91-2.md (Collision sections), my project | read 2026-09-20
- tamper `from` counts at develop, each exactly ONE: FIRSTOF3NULL + ALLNULL3 admin.ts:1132 (shared line), ALLSKIPPEDZERO startup-migrations.ts:1202, NOJSON422 documents.ts:1674, NOJSON502 + NOJSON504 documents.ts:1722 (shared line), RAW598 verification.ts:597 (2-line block), RAW1297 verification.ts:1297, REFRESHNOAUTH platform.ts:254, IV_REGLIVEONLY platform.ts:491, TENANTSGETUNGUARDED platform.ts:219 (4-line block). Plant sha256s come from each run's `tamper_*.plant.out`, and each record's pre-plant byte count equals the develop file (platform.ts 44888, verification.ts 70976, admin.ts 74087, startup-migrations.ts 57305, documents.ts 146712). Develop sha256: platform.ts 7d04a92ca724, verification.ts 43d29242eda1 | each run's input.json tampers matched line-exact against `git show 4273adfac:<file>` in the scratch clone, plus /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/<run>/out.md.checker/tamper_*.plant.out, run 00:09 AEST, my project | read 2026-09-20
- cell counts per file (READY SUMMARY lines, cells after one patch): ks1230 13, ks1062 7, ks739 25, ks1238 10, ks1215 23. The round-17 briefs report api-gateway 651/651 with the five KS-1238/KS-1282 patches combined | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_{KS-1230-N86-1,KS-1062-N88-1,KS-739-N89-1,KS-1238-N90-1,KS-1238-N91-1,KS-1238-N83-2,KS-1238-N83-6,KS-1282-N91-2}_*.diff.md, held by Wednesday 23:51 (09-19) and 00:06 (09-20), and each run's input.json, my project | read 2026-09-20
- Linear reads, 14:08:47Z: KS-1238 Backlog Medium, unassigned, 4 attachments (#1091, #1090, #1083, #1076), last comment 2026-09-19T13:11Z, branchName carries `ks-1215`; KS-1282 Backlog Medium on kamil.kreiser@secuura.ai, 0 attachments, 0 comments, branchName `feature/ks-1282-get-apiplatformtenants-the-requiresuperadmin-guard` (clean); KS-1230 In Progress Medium, same assignee, 6 attachments, branchName clean; KS-1215 In Progress High, live; KS-1248 In Progress Medium, unassigned | Secuura Linear GraphQL, a read-only query run by Wednesday's drafter with the key from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env (your tree), sourced transiently and never copied | read 2026-09-20
- KS-1062 Done ARCHIVED 2026-09-13T05:35:48Z (1 attachment, #932); KS-739 Done ARCHIVED 2026-09-14T08:33:49Z (1 attachment, #919) | same query, issue by identifier, 14:08:47Z | read 2026-09-20
- KS-485 Todo High and KS-772 Todo High, both live. My comment read (`comments(last:3)`) did NOT return Seat B 6th's 09-19 rule-7 comments. That is the known selector trap: Linear's comments connection is newest-first, so `last:N` returns the OLDEST N. The newest comment on either is therefore unproven here; read comments with `first:50` and sort client-side | same query, 14:08:47Z | read 2026-09-20
- origin branch names: `feature/ks-1230-…-n80-1`, `feature/ks-1238-n83-3-…`, `feature/ks-1238-n83-5-…`, `feature/pin-startup-migrations-skipped-tenants-counted-loop-continues` and `feature/pin-transfer-custody-nonjson-400-503-lookup` exist; no `ks-1282` branch exists | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin 'refs/heads/*', YOUR checkout, read-only, 00:08 AEST | read 2026-09-20
- kept worktrees s-b2-* through s-b6-*, s-a13-deploy, s-a14-deploy; no s-b7-* exists | ls /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/.git/worktrees/, YOUR checkout, read-only, 00:10 AEST | read 2026-09-20
- Seat B 6th's final state (#1084-#1091 merged, develop 4273adfac), its method scripts (`raise/*7.*`, `boot/measure7.py`), its slips, MG-1, the ruleset read, KS-1238's four open F-1 items (gate facts comment `60c1e1f7`), KS-1282 filed, and N84-1 and /unrevoke -1 kept for Kam | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-6th-successor-2026-09-19.md, the history.md top entry, `2026-09-19_seatB-6th/mail/04-merged.txt` + `05-wrap.txt`, and the `raise/`, `boot/`, `mail/` listings, your own tree, read 00:05-00:10 AEST | read 2026-09-20
- the 23 undelivered Secuura/Blockchain cards and their stored ruled_choice labels (22 with the secuura- prefix, excluding the Platform_S one, plus ks661-vocab) | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered, run 00:09:26 AEST, and /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/decisions.json, my project | read 2026-09-20
- the WEEK-INSTRUCTION, status live, valid_until 2026-09-20 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md, read 00:10 AEST, my project | read 2026-09-20
- the TESTED grant and the merge-authority sentence | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md lines 233-238, sed run 00:10 AEST | read 2026-09-20

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-20 00:13
- Eight fixes, five PRs, five distinct test files, zero product bytes. The count reads eight fixes / five PRs in the BLUF, the GROUPING table, the QUEUE and the READY section.
- PR 5 is the only PR with two tickets (Refs KS-1238 + Refs KS-1282), and its attachmentsForURL target is {KS-1238, KS-1282} wherever it appears.
- KS-1062 and KS-739 have no Refs wherever they appear (the table, QUEUE items 2 and 3, the Wednesday rulings). Every other item carries Refs and never Closes.
- The tip is stated once: all eight at 4273adfac, measured by the seat.
- PRs 4 and 5 are tier 1, test-only and pushed last. KS-1238 stays Backlog unless the gate rules COMPLETE, and KS-1282 stays open. PRs 1-3 are tier 2.
- The tamper counts are one match each everywhere. The two shared-line pairs are named as shared lines, not as ambiguities.
- /unrevoke appears only as nothing-about-it. KS-1280, KS-1279, KS-730, KS-1250, KS-692, N84-1 and the other 12 guards appear only as not-in-this-batch. Demo and kintsugi appear only as not-yours.
- KS-1215 and KS-1248 are prose-only and untouched. The KS-1215 trap is named for both the branchName and the ks1215 file name.
