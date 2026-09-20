SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 10th): PR 3 KS-1272 UUID-DEDUP-1
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-20T13:09:38.000Z
MESSAGE_ID: <010001a0beefbf57-2669fbd9-54c1-494f-9975-2cfe909315d1-000000@email.amazonses.com>
CAPTURED: 2026-09-20T13:10:12Z by the batch 1102-1104 drafter, read-only by message id from wednesday-agent@ (key by name, never printed)
TEXT_SHA256: e778595cfedbd11a232a7df3dd4a765da6f86009fa862888854f315c1b52571d
READY FOR QA (Seat B 10th): PR 3 KS-1272 UUID-DEDUP-1 — #1104 at head 9b668edba63e1328ab113058b47953a11d2a3ed6 (read from origin in the same action), branch
feature/ks-1272-api-gateway-boot-the-platform-db-de-dup-delete-fails-22p02-uuid-dedup-1, built on develop
dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa (tree 1ccb80e0d66ab0ff12d5dbb61753b8c0c274e923), re-read at READY: UNMOVED (ls-remote dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa at 13:09Z; ruleset 18499832 re-read at READY, rules byte-identical to boot).
Ticket: Refs KS-1272, linkKind contributes (attachmentsForURL after the push and after the PR opened: post-push KS-1272 attachments [] -> post-PR [('1104','contributes','open')]; attachmentsForURL #1104 = [('KS-1272','In Progress','contributes')] — exactly the one ticket, contributes). Proposed tier 2
(a migration statement, no auth surface). PR 3 of 3, pushed LAST. HOLDING for your GO. Nothing merged, nothing deployed; kintsugi
takes this only as a later proven deploy, not this seat's; demo never.

THE FIVE THINGS A READY IS
1. PR number: #1104. Title "KS-1272 UUID-DEDUP-1: make the platform de-dup DELETE type-agnostic (IS NOT DISTINCT FROM)". Base
   develop. +86/-1, TWO files: Blockchain/Dev/services/api-gateway/src/startup-migrations.ts (1 1) and the NEW
   Blockchain/Dev/services/api-gateway/src/__tests__/ks1272-platform-dedup-uuid-tenant-id.test.ts (85 0). mergeable_state at READY:
   mergeable true / unstable (no checks run; the field carries no testing claim); reviews 0.
2. Head SHA read from origin in the same action: 9b668edba63e1328ab113058b47953a11d2a3ed6 = commits.tsv = the PR's head. Head tree 35eab598df96eeb5838414d72d986f2208eacc75
   = item 0b's PR-3-alone tree. Blobs: startup-migrations.ts cf371028fb564ca0e55d9d9501c3efa1211b5bd0 (develop ed3e521426e7…),
   the new test 2b91446416f826b69dbd5a0ab6f4123c96d06349 (ABSENT at develop).
3. Ticket: KS-1272 (Backlog Low at boot, 0 attachments, 0 comments; In Progress after the PR opened — the linear[bot] (actor GitHub) walked it Backlog -> In Progress at 13:08:19Z on the PR open; recorded, not moved back).
   Attachment: #1104 contributes. No comment posted.
4. Test Evidence block: in the PR body, every evidence line quoted verbatim from raise/ks1272.log. Summary:
   - Host: worktree s-b10-ks1272 at develop dc061f2bb, in-process, no stack, no Postgres.
   - Touched: the product file (ONE line) + the new test file. The narrowed product-byte hold, measured: `git diff --numstat` on the
     product file is exactly `1 1`; the diff is exactly your pair
       -           AND COALESCE(a.tenant_id, '') = COALESCE(b.tenant_id, '')`,
       +           AND a.tenant_id IS NOT DISTINCT FROM b.tenant_id`,
     at :1077 inside `const platformMigrations = [` (:1060); the 5-space twin at :473 (CORE_MIGRATIONS) is byte-UNCHANGED —
     5-space form 1 -> 1, 11-space form 1 -> 0; the file stays 1228 lines. The raise STOPs on anything else.
   - Ran (api-gateway/vitest), the red proof for a one-line product change = the new file's red-first / green:
       the TEST section of the canonical patch applied alone (`git apply --include`, strict): 3 cells; exactly the 🔴 cell red
         (an assertion: the platform summary read INCOMPLETE `[false, {applied:6, failed:1}]`), both CONTROL cells green = the
         checker's red_first.json (3 / 2 passed / 1 failed);
       the PRODUCT section applied: numstat exactly `1 1`; product blob = item 0b's; the two --include steps == the verbatim patch,
         proved by blob (both files' blobs equal item 0b's single-apply blobs);
       3/3 green = the checker's green_after.json;
       whole api-gateway 674 -> 677, NEW reds []; tsc --noEmit rc 0 — startup-migrations.ts IS in the api-gateway tsc program (the
         test file is not; targeted per-file type-check: 0 at head for both files, the new test's develop side 0 by construction,
         delta +0; planted TS2322 CAUGHT); eslint 0/0 on BOTH files.
       No tampers: the fix is one line and the cell's red/green IS the proof (your ANSWER). The checker dir holds no tamper_* files.
   - Connection census (evidence): api-gateway rule v2; this item's 3 runs: STOP-class 0; every established peer 127.0.0.1; zero
     :5432; the test's own fake Pool makes NO connection (its URLs are *.invalid and the fake never opens a socket — 0 attempts in
     the test-file runs). Removed after the last run.
   - Pre-push preflight (in-hook on this push): `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` shell suites 40 passed / 0 failed (of 40); push 13:02:08Z -> 13:07:56Z, rc 0 — skips are not a pass. Push protocol PROTOCOL-CLEAN (shape: first push: tracking ref added at origin's head 9b668edba…). login_stub
     listeners cleared: 4 cleared, 0 remaining (0 listeners on the box at READY).
   - NOT run / NOT covered: the platform suites (no stack). A REAL POSTGRES WAS NOT EXERCISED — the fake reproduces 22P02 by
     matching the ticket's quoted text; the kintsugi boot log was not re-read; docker/init-platform/01-platform-schema.sql untouched.
   - Migrations / config: the changed statement IS a startup migration (the platform list's KS-39 #4 de-dup, run by
     runStartupMigrations at boot); nothing under migrations/ and no config.
5. NOT done: the ticket's THIRD item — which tenant_id declaration is canonical (TEXT in the in-code CREATE vs UUID in
   docker/init-platform/01-platform-schema.sql) — is a ruling for Kam, stated as NOT DONE in the PR body and the commit message.
   No deploy, no kintsugi step by this seat, no ticket comment, no merge.

FINDING 1 (a record discrepancy, measured, per your ACK not a STOP): the checker's section_2.opts names section_2.decl.diff (86
lines; its SUMMARY reads +86/-1); the CANONICAL patch.diff your READY names is 85 lines (= section_1 + section_2 byte-for-byte,
sha256 3f7d6d0be92787e47a48e88da5755e0e8e0251344de0f289e0353ad92b659a88). The one extra line is a DECL-SPLICE accommodation,
`const summary = () => lines.find((l) => l.includes('[startup-migrations] Tenant DB migrations')) || '';` — the word `summary`
appears in the 85-line test only in a comment and three it() titles, in no code line. THIS PR CARRIES THE CANONICAL 85-LINE FILE;
every measurement above is on it; the checker's PASS 7/7 was on the 86-line variant (you said you would tell the gate).

ARCHIVED-TICKET READS at READY, unchanged: KS-501, KS-1062, KS-1238, KS-1282 all Done + archived; no Refs/key anywhere; none
reopened. Guarded attachment lists equal boot at every read. KS-1172 / KS-1173 (live, foreign) named nowhere in branch/title/subject.

BOTH-ORDERS / ALL-ORDERS TREES (READY 2's duty, restated here for the three): PR1 66cb0c8234ae, PR2 ce51bd52adf8, PR3 35eab598df96;
PR1+PR2 in both orders d2387eabdba1 (= yours); ALL THREE in ALL SIX orders -> ONE tree d0c8bfd095b65861efc1a4e8524017235b42e382
(4 files, +98/-1) — measured at boot in a temp index + temp object dir with the read-tree-back and outside-objdir controls, and
REPRODUCED by the octopus batch worktree s-b10-batch (commit 8b467ed67, never pushed): tree d0c8bfd095b6 EQUAL, every changed path's
blob = its own branch's. On it: api-gateway 678/678 (674 + 1 + 3), originate 807/807, tsc 0 x2, census STOP-class 0.

FOR THE GATE TO MEASURE
- The product diff is exactly one pair at :1077; :473 unchanged; numstat `1 1`; blobs cf371028fb56 / 2b91446416f8.
- MG-1 for a TWO-file PR: targets.json will carry TWO equality targets for #1104 (one per file) — say so in the MERGE ADDENDUM,
  and merge11.py requires exactly one per PR file (1 / 1 / 2). Every MERGED line will read "N gate equality target(s)".
- Red-first is the proof: the checker's red_first.json and green_after.json counts = mine (3/2/1 and 3/3).
- FINDING 1 above. The 85-line file is what is raised.
- Deviation from verbatim: NONE in the apply (strict, correctly counted); the record discrepancy is FINDING 1.
- Not exercised: a real Postgres. The gate may want a kintsugi-side re-read of the boot log after a later deploy (not this seat's).

ALL THREE AT READY (ready11.py, same action): #1102 f5a599b07 open +4/-0 1 file Refs KS-1275 · #1103 47593b77b open +8/-0 1 file
Refs KS-1203 · #1104 9b668edba open +86/-1 2 files Refs KS-1272; all mergeable true / unstable, reviews 0; develop unmoved.
Ticket states at READY: KS-1275 In Progress (bot 12:55:23Z), KS-1203 In Progress (bot 13:01:43Z), KS-1272 In Progress (bot
13:08:19Z) — all three walked by the linear[bot] on PR open; I move none back before the last merge, per the brief. The four
archived keys unchanged. login_stub listeners on the box: 0.
Correction to READY 2: its push window was written as ending 13:01:20Z; the push.end record reads 13:01:12Z (13:01:20Z is the
verify line's stamp). READY 1's 12:55:04Z has the same shape: push.end 12:54:57Z. No other value changes.
The three PRs are now HOLDING for your gate — one batch or by tier is your call. No GO = no merge, whatever the clock says.

