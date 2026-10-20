## NEW SEAT: you are Seat D 26th (lane Secuura/Blockchain-D, a RAISE seat): raise two held Spark test-only passes as two PRs (KS-1116 and KS-1679). Tier 2, stop at READY FOR GATE

**Routing receipt:** `model: claude-sonnet-5-5 -- C1 (raise a held local PASS as a PR; test-only, product untouched) -- P1-P4 no (Wednesday's classification from the commission; not re-derived by the drafter) -- gauge 78% (statusline 7d, read 13:5x)`. Row C1 text read at `fleet/specs/model-routing.md:91`. If either patch turns out to need a product line, STOP and say so; that is no longer a C1 job.

**Why you exist:** the Spark (local model, screen 21) produced two PASSes from today's gate notes. Wednesday read both patches at source and held them. They are raised by their own lane because Seat C 32nd is on KS 1695 and Seat R 59th is on the m365 files (PARTITION). Seat D 25th is wrapped (as stated in the C 32nd brief); no predecessor of yours holds this work. Screen report: `0_Brain/reference/2026-10-18_spark-screen/SCREEN_21.md` (154 numbered lines in the drafter's read; read the Method, Design choices table and Things-to-read sections).

**develop, read by the drafter:** `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src ls-remote origin refs/heads/develop` at **13:49:27 AEDT, 2026-10-20** returned **`f01ba49da56d3d55204caa02ab3348f94d63b9c0`** (the same sha both READY files name as their tip). It may move before you start; re-read it and re-run `git apply --check` per patch before any claim. Line numbers below name THAT tree (`git show f01ba49da56d:<path>`).

---
## BLUF
1. Raise **two PRs, two branches, file-disjoint, from live develop**: PR A = KS-1116 (vc-issuer, +6/-0 in one test file), PR B = KS-1679 (originate, +12/-0 in one test file). Each patch is the Spark's `patch.diff` byte-for-byte; **zero product bytes in either PR**.
2. **Tier 2 (test-only; Sonnet gates).** `Refs`, never `Closes`: both tickets stay open (Done needs more than these cells).
3. Stop at **READY FOR GATE, one mail per PR**. No merge without Wednesday's GO naming the head sha.
4. **PR A's body must say plainly:** the new "EXTENDS the row's tenant" row is proved ONLY by hand mutants (the checker plants one tamper, the role-prefix one, and the EXTENDS row stays green under it). Your own re-run of those mutants is the evidence; say what you ran.

## QUEUE (in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/`)

### 0. Boot
Read the launch preflight file in your FIRST tool call (STANDING LINES below) and quote it, with its own launch stamp, warnings included, into your plan confirmation. Establish your seat from your own pane (`tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'`). Cut a fresh clone per WORK CLONE below. Send the plan confirmation before your first write.

### 1. PR A: KS-1116, BM1 NOTE 1 (vc-issuer, vitest)
- **Held file:** `READY_KS-1116-BM1NOTE1-1_spark-dsv4flash_BRIEFED-TESTONLY-OWNERSHIP-PASS-7of7_2026-10-20.diff.md`. Canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1116_p1/out.md.checker/patch.diff` (one section, `section_1.diff`; apply with plain `git apply -p1`, strict).
- **File:** `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1116-presentation-and-credential-reads-bound-to-the-creator.test.ts`, one hunk at `@@ -131,6 +131,12 @@`, three rows added to the existing `NOT_THE_ROWS_TENANT_ADMIN` refusal table: an `ORG_VIEWER`, a `SYSTEM_SERVICE`, and an `ORG_ADMIN` whose tenant EXTENDS the row's tenant (`${T1}0`). Product `src/ownership.ts` untouched.
- **What it pins:** gate BM1's NOTE 1 on #1652: two predicate regressions the existing cells could not see (a role that only BEGINS with `ORG` or `SYSTEM`; a compare in the other direction, `claim.startsWith(rowTenant)`).
- **The checker's numbers (the Spark's instrument, at tip `f01ba49da56d`; yours must be re-measured, not copied):** red-first 7 failed / 140 run; green-after 140/140; whole `services/vc-issuer` suite total 291 -> 300, failed 0, no NEW red.
- **Mutants to re-run yourself** (SCREEN_21 Design-choices table; every one compile-clean by `tsc --noEmit` against the unmutated baseline FIRST, restore asserted by sha256 with a unique anchor):
  - BM4 (the checker's tamper), `ownership.ts:92`: `if (role === null || !(TENANT_ADMIN_ROLES.has(role) || role.startsWith('ORG') || role.startsWith('SYSTEM'))) return false;` (reds 7 cells: the two new role rows in each of three tables plus one more).
  - BM4a (ORG prefix only) and BM4b (SYSTEM prefix only): 4 cells each. BM4c `endsWith('_ADMIN')`: 7 cells (the older TENANT_ADMIN / SUPER_ADMIN rows bite).
  - BM1 `claim(user?.tenantId).startsWith(rowTenantId)` and BM1b `includes` on `ownership.ts:93` (the tenant compare line, `return rowTenantId !== null && claim(user?.tenantId) === rowTenantId;`): 4 cells each (the new EXTENDS row in three tables, plus one more). **These two are the only proof of the EXTENDS row.** Record each one's red cell NAMES.
  - Prior-pin regressions JM11 `rowTenant.startsWith(claim)` and JM8 (role set widened): 7 cells each (the old rows still bite).
  - SCREEN_21 gives the cell counts, not the exact mutant source text for BM1, BM1b, JM11, JM8. Write each one yourself from the description and say what you wrote; do not claim to have reproduced the Spark's text.

### 2. PR B: KS-1679, BF1 N1 (originate, jest)
- **Held file:** `READY_KS-1679-BF1N1FALSY-1_spark-dsv4flash_BRIEFED-TESTONLY-CERTIFICATIONS-PASS-7of7_2026-10-20.diff.md`. Canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1679_p2/out.md.checker/patch.diff` (one section).
- **File:** `Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts`, one hunk at `@@ -165,6 +165,18 @@`, a pure insertion of 12 lines (a two-line comment and one cell, `RED KS-1679 R6`) between cells R5 and C3. The cell plants `''`, `null`, `0`, `false` for both `certificationId` and `certifiedAt` and asserts each is dropped from the row AND logged exactly once. Product `src/routes/certifications.ts` untouched.
- **What it pins:** gate BF1's N1: every planted value in the earlier cells was truthy, so a truthiness log gate survives.
- **The checker's numbers (the Spark's instrument, at `f01ba49da56d`; re-measure, do not copy):** red-first 1 failed / 14 run; green-after 14/14; whole `services/originate` suite total 1576 -> 1577, failed 0, no NEW red.
- **Mutants to re-run yourself** (all in `certifications.ts`, `tsc --noEmit` first; the drafter confirmed at `f01ba49da56d` that `:654` is `if (droppedCertificationId !== undefined) {` and `:657` is `if (droppedCertifiedAt !== undefined) {`):
  - The checker's tamper, `:654`: `if (droppedCertificationId) {` -> R6 only.
  - M7, `:657`: `if (droppedCertifiedAt) {` -> R6 only.
  - M8: `if (droppedCertificationId != null) {` -> R6 only. M9: `if (typeof droppedCertifiedAt === 'string') {` -> R6 only.
  - M10: gate `if (false as boolean) {` on certificationId -> R4 and R6.
  - Each must red BY ASSERTION (`0 passed and 0 failed` is a load failure, not a red).
- **Known type-check caveat (SCREEN_21 Findings):** in the Spark's scratch clone `tsc --noEmit` printed exactly one error at the unmutated tip (`TS2305`, a symbol missing from a stale shared dist); the checker's own baseline and A7 were rc 0. In your fresh clone build `packages/shared` first (WORK CLONE step 3). Compare each mutant to YOUR unmutated baseline, not to the Spark's.

### 3. Per PR (both)
- **Apply and show:** `git apply --check` then `git apply -p1` of the canonical patch at live develop; show the patch == the READY file's diff block (byte compare), the pre-image blob of the test file at live develop, and that only that one file changed (three-dot: `git diff --stat origin/develop...HEAD`).
- **Whole service suite before and after, keyed by cell NAME** (vc-issuer for A, originate for B): report suite files / cells / failed at the landing parent and at your head, **0 vanished**, and the new cells by name. A green is not "N passed": print the ratio and treat `0 total` as a load failure.
- **Type-check the test file in its OWN program.** `services/vc-issuer/tsconfig.json` excludes `src/__tests__` (read at `f01ba49da56d`); `tsc -p` in originate excludes test files too (KS 1090). Use a child tsconfig with `exclude: []` and the listed-file count as the control; do not accept a `tsc` rc 0 that never saw the file. Run the package lint too (`npm run lint`).
- **Re-run the Spark's mutants** (lists above) for that PR, on a restored-by-sha256 file with a unique anchor (`grep -c` the anchor first).
- **Overlap census** on the touched test file against open PRs (Wednesday holds no GitHub identity and did not check this). SCREEN_21 flags rebase risk: the KS-1116 test file may be edited by KS 1683 / KS 1684 work; the KS-1679 test file by anything on KS-1679.
- **Predict the landing tree** on live develop and quote it beside the develop sha it was computed against; re-predict at READY and again immediately before any merge.
- **PR bodies:** PR A names only KS-1116 hyphenated; PR B names only KS-1679 hyphenated; every foreign key written spaced or bare (`KS 1683`, `KS 1695`, `KS 1682`). Run a key scanner over title, body and every commit message before pushing (copy a predecessor's `keyscan*` tool re-keyed to your seat; scan PROSE as well as names). `Refs KS-1116` / `Refs KS-1679`, never `Closes`. Declared squash subject never carries a `(#n)` suffix. Keep branch commits and the squash body free of any attribution trailer the GO forbids (the check is on the SENT body).
- **PR A body states:** test-only; zero product bytes; BM1 NOTE 1; the EXTENDS row is proved by hand mutants only (name which, and the cells that red), because the checker plants one tamper. **PR B body states:** test-only; zero product bytes; BF1 N1; the cell loops 8 requests (4 falsy values x 2 keys) and the `[key, planted, ...]` prefix names the failing pair; it does NOT cover the KS 1508 and KS 1660 gates, which have the same shape (SCREEN_21 Things-to-read 4).
- **READY FOR GATE: one mail per PR** (STANDING_LINES "READY FOR QA"): PR number, **head sha read from origin (`ls-remote`) in the same action**, a ticket comment naming the PR (BLUF), the Test Evidence block you ran, what was NOT covered, and the predicted landing tree **beside its develop sha**. Then stop.

### 4. What you do NOT measure or claim
State honestly in each READY: the Spark's numbers are the checker's, yours are separate; no open-PR identity existed for Wednesday's read; the gate decides the tier; nothing here was deployed or run against a live service (test-only).

## THE MEASUREMENT RULE (standing)
**A figure travels with its referent, or it does not travel.** A line number names its tree; a count names its moment, its corpus size AND its instrument; a landing tree is quoted beside the develop sha it was computed against; a transition is measured at BOTH ends or not claimed. Any figure older than the last merge is stale by default.

## PARTITION
**Yours:**
- `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1116-presentation-and-credential-reads-bound-to-the-creator.test.ts` (the one hunk).
- `Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts` (the one hunk).
- Product files `vc-issuer/src/ownership.ts` and `originate/src/routes/certifications.ts` are **mutant targets in your scratch clone only; they are never committed changed.** Assert byte-unchanged (sha256 against the tip's) before each commit.

**NOT yours (live or waiting; do not touch):**
- **Nothing in `Blockchain/Dev/services/m365-integration/**`**, including its tests (Seat R 59th, per the G 13th brief; not re-read live). The KS 1682 test cells in the Spark screen are R's, not yours.
- **certifications.ts route or documents** (Seat C 32nd, KS 1695): no edit to `routes/certifications.ts`, `documents.ts` or `documentRepo.ts` beyond the scratch mutants above.
- **Nothing in auth** (Seat G 13th: auth `session.ts`, the reset-password / change-password routes, `gdprService.ts`).
- Any other vc-issuer file, including the KS 1683 / KS 1684 route work (named by the screen as live; not read live).
- `2_Project_Files` of the project: READ-ONLY (KS-907).

You share ONE inbox with every Secuura seat (`secuura-blockchain@agentmail.to`): **a mail naming another seat is not yours.** Subjects you send never carry the words hold / stop / checkpoint (routing tokens); they carry `[Secuura/Blockchain-D -> Wednesday]` and your seat's name. (The `-D` lane tag is the drafter's inference from the C lane's `Secuura/Blockchain-C`; it was not read from a D-lane artefact.)

## PROTOCOL AND MAIL
- **Plan confirmation first (QUESTION mail, topic `plan confirmation`).** Wednesday confirms against this brief. It carries: the launch preflight file VERBATIM with its stamp; the clone facts read back (`git config --get core.hooksPath`, `git config --show-origin user.email`, `git config --get core.sshCommand`, `packages/shared/dist/index.js` asserted); the develop sha you cloned; the per-patch `git apply --check` result; your type-check method for each test file; and the mutant list for each PR. A plan that DEVIATES (a product line, a third file, a wider hunk) pauses for Wednesday and Kam.
- **Mid-session questions:** one question per mail, subject `[Secuura/Blockchain-D -> Wednesday] QUESTION: <topic>`; body sections Context (1-3 lines + paths) / Question / Meanwhile (`continuing with <x>` or `BLOCKED`) / Needed-by. Re-check your inbox every ~3 minutes when blocked. The answer comes as `[Wednesday -> Secuura/Blockchain-D] ANSWER: <topic>` (topic mirrored exactly). Approval-class items always pause for Kam.
- Mail every state change; a turn never ends on an unmailed report or on a "next up" line with nothing running.
- **Client-facing communication is ticket comments only, BLUF.** The extranet is INPUT ONLY (you never `POST /api/seen`). Nobody is messaged outside the fleet.
- No secrets in any mail.

## HOLDS
- **A fresh clone has NO pre-push gate.** Before any push: `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`, then read back `git config --get core.hooksPath`.
- **Identity:** `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai` LOCALLY before the first commit; read back `git config --show-origin user.email` (must say `file:.git/config` and the Secuura address).
- **Hook-aware push route.** Before naming ANY push route, read `.githooks/pre-push` at the develop you cloned and cite the line. The prior drafts' reads (at older trees, not re-read by this drafter): a pushed sha that is not the checked-out HEAD is refused; a non-fast-forward push to a branch that exists at origin is refused; a brand-new branch skips that check. Push a NEW branch from the checked-out HEAD. To catch up with develop, MERGE develop in; never rebase a pushed branch. Never `--no-verify`, no force push, no `--admin`, no `ALLOW_FORCE`.
- **After `git apply`, check the disk exec bit of every 100755 file (and `test -x .githooks/pre-push`) before any push.**
- Merge only on Wednesday's head-pinned GO after a gate verdict. No deploy, no `az`, no box, no Docker on this Studio. Signature classes pause for Kam: production, money, external communication, anything irreversible.
- Put the gate's notes into each PR body's Known residue BEFORE merging and read the body back.
- A control must be able to fail; never delete (quarantine); never edit a running script. Rotate inside your 80-90% band at a clean boundary, handover first.

## WORK CLONE
No clone is adopted for you. Cut ONE fresh clone from GitHub under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/deploy-clones/seatD26-<12-hex of the develop sha>` (an absolute path outside the project checkout; check the folder for an existing clone of that name and do not reuse another seat's). Use `git worktree` or a second branch in it for the second PR only if you can keep the two branches' working trees clean; otherwise cut two. The project's deploy key is `3_Access_Keys/github_deploy_rw`. Then, each READ BACK and quoted in the plan confirmation:
1. `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`, then `git config --get core.hooksPath`.
2. `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai`, then `git config --show-origin user.email`.
3. `npm ci --ignore-scripts`, then `npm run build --workspace=packages/shared`, then ASSERT `packages/shared/dist/index.js` exists (never trust the rc). For originate also `npm run generate --workspace=services/originate` (the bare `prisma generate` is not on PATH).
4. `npm ci` in EVERY `systemTest/*` package the repo carries, enumerated from git (`git ls-tree -r --name-only HEAD | grep -E '^systemTest/[^/]+/package\.json$'`, REFUSE if the count is 0; the repo-ROOT `systemTest/`), because the pre-push format gate refuses a package whose deps are absent.
- **Network git has no `core.sshCommand` fallback in a fresh clone:** every fetch, ls-remote and push supplies the key and keepalive explicitly (below), `GIT_SSH_COMMAND` unset.
- A `clone --shared` scratch clone's `origin` is the LOCAL checkout; read `git remote -v` and assert any fetched sha equals the `ls-remote` value you meant.

## STANDING LINES CARRIED (from the C 32nd brief, which carried fleet/STANDING_LINES.md; the drafter did not re-open STANDING_LINES.md itself)
- **SECUURA PUSH TRANSPORT:** when the launcher printed F-02 (keychain not seeded, on-disk fallback off) it did NOT write its keepalive `core.sshCommand`, so any push whose hook runs past ~6 min dies with the gate passing. Push with `git -c core.sshCommand="ssh -i <the project's deploy key> -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 -o ServerAliveCountMax=20" push ...`, `GIT_SSH_COMMAND` unset. *(The preflight file the drafter saw carried F-02 and KS-907 with stamp `2026-10-20T02:13:13Z`, which is NOT your launch. Read yours.)*
- **NEVER export `GIT_SSH_COMMAND` in a shell that runs a push tool**; run push tools with `env -u GIT_SSH_COMMAND`.
- **A push's result is the push tool's own `.rc` file plus an `ls-remote` of the ref**, never a harness or task exit code.
- **A FRESH CLONE HAS NO PRE-PUSH GATE; a FRESH CLONE CANNOT RUN the originate SUITE UNTIL `@secuura/shared` IS BUILT; every scratch clone pins the CLIENT's git identity LOCALLY.** WORK CLONE steps 1-3.
- **Seat identity:** read your pane id from `$TMUX_PANE`; a bare `tmux display -p` returns the client's active pane. **Read the launch preflight file in your FIRST tool call.**
- **Read a repo file from a SHA, never from the Secuura MAIN checkout's working tree** (it sits far behind develop).
- **Secuura/Blockchain: no force push, ever.** **Drive hygiene (Kam 2026-10-05):** at WRAP remove or move the worktrees and clones YOU created for merged work, report GB freed.
- **A MULTI-CLAUSE GUARD IS RED-PROVED BY FLIPPING EACH CONJUNCT SEPARATELY** (applies to `ownership.ts:92-93`: role test, tenant-not-null, tenant equality); **A TAMPER'S RESTORE NEEDS A UNIQUE ANCHOR**; **A checker's verdict prints how many items it CHECKED**; INSTRUMENTS (redirect to a file and read `$?`, never through a pipe; zsh has `$pipestatus[1]`, no `timeout`); "WHAT DID MY BRANCH CHANGE IS A THREE-DOT QUESTION"; "MAIN MOVED vs MAIN MOVED IN A WAY THAT REACHES MY CELLS"; "Never end a turn on a 'next up' line with nothing running". Read these at their headings in `fleet/STANDING_LINES.md`.
- **Traps carried (from the C 32nd brief's G 12th list):** a runner's label set cross-checked against the FAILED COUNT (print PARSER FAILURE when they disagree); a zero from a flag-scalar grep in zsh is the instrument, not the answer; a guard that counts a token in its own prose (count the CODE form); `--reporter=basic` is not a vitest reporter; a census is scoped to what it keyed on (state what yours keyed on); a survivor is not always a gap (drive the input).

## RULED BY KAM, NOT YET IN AN ARTEFACT
- `decision_queue.sh list ruled --undelivered secuura-` read by Wednesday 2026-10-20 13:1x AEDT: 87 older ruled cards carry no delivered mark in the store. None of them commissions or governs these two PRs. Nothing below is a new ruling.
- Context, not yours to act on: Kam's KS-1116 rulings (bind-creator 2026-09-13; (a) on owner-less reads 2026-10-20) are built and merged (#1648, #1649, #1652); these PRs add refusal rows to the table that encodes ruling (a) and change no behaviour.
- SCREEN_21 question 2 (the `started_ok` carve-outs for the In Progress tickets) is CONFIRMED by Wednesday: accepted, no veto.

PROVENANCE:
- develop `f01ba49da56d3d55204caa02ab3348f94d63b9c0` | `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src ls-remote origin refs/heads/develop` | read 2026-10-20 (13:49:27 AEDT)
- KS-1116 In Progress, priority 3, 4 comments, last update 2026-10-19T23:32:05Z (the last comment is the #1652 merge note), assignee the board account; attachments #1652, #1649, #1648 | Linear GraphQL, read by the drafter with the Secuura key read transiently from the project's `.env`, read-only | read 2026-10-20 (13:49 AEDT)
- KS-1679 In Progress, priority 3, 4 comments, last update 2026-10-20T00:17:09Z (the last comment is the #1656 merge note), no assignee; attachments #1656, #1646 | Linear GraphQL, read by the drafter with the Secuura key read transiently from the project's `.env`, read-only | read 2026-10-20 (13:49 AEDT)
- Both held READY files read whole; PR A patch `+6/-0` and PR B patch `+12/-0`, one section each, product untouched, strict apply clean at `f01ba49da56d`, red-first 7/140 and 1/14, green-after 140/140 and 14/14, suites 291 -> 300 and 1576 -> 1577 with no NEW red | the two READY files (checker artefacts copied verbatim by Wednesday's `hold_ready.py`, written 13:48 AEDT) | read 2026-10-20 (the checker's instrument at `f01ba49da56d`; the drafter did not re-run it)
- Mutant list and cell counts for both PRs | `0_Brain/reference/2026-10-18_spark-screen/SCREEN_21.md` Design-choices table | read 2026-10-20 (the screen sub-agent's hand runs at `7e3b9362e08b`, not re-run by the drafter)
- `ownership.ts:92` and `:93` (the tamper line and the tenant compare) and the `vc-issuer/tsconfig.json` exclusion of `src/__tests__` | `git show f01ba49da56d:Blockchain/Dev/services/vc-issuer/...` | read 2026-10-20
- `certifications.ts:654` and `:657` (the two log gates) | `git show f01ba49da56d:Blockchain/Dev/services/originate/src/routes/certifications.ts` (sed 650-660) | read 2026-10-20
- Spark briefs and pins for both (tier `test_only`, `started_ok` carve-outs) | `local-model/night/briefs/ks_1116_p1/` and `ks_1679_p2/` (`spark.pins`, `KS-1679.md`) | read 2026-10-20 (`ks_1116_p1/KS-1116.md` was NOT read by the drafter)
- Routing row C1 | `fleet/specs/model-routing.md:91` | read 2026-10-20
- Partition owners (R 59th m365, C 32nd KS 1695 certifications and documents, G 13th auth) | the C 32nd brief `2026-10-20_seatC32_ks1695_pr1.md` PARTITION and the user's commission to the drafter | read 2026-10-20; whether those seats are live NOW is unread
- Launch preflight stamp `2026-10-20T02:13:13Z` (F-02, KS-907 2 other live sessions) | `Blockchain/4_Credentials/.launch_preflight_last.txt` | read 2026-10-20 (NOT your launch)
- Open-PR overlap on either test file, KS 1683 / KS 1684 state, `.githooks/pre-push` line numbers at `f01ba49da56d`, STANDING_LINES.md itself | not read by the drafter | not read 2026-10-20

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-20 13:51
