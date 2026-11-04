# Gate 190 commission — Secuura / Blockchain, PR 2002 (KS-1401 migration 058: tenant isolation where 039 is already recorded), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-04 23:1x AEDT. Model: Opus (routing v1.0 tier-1 gate: a data migration with a backfill and row-level security on tenant data). Spark shadow: NOT run (Kam 16:42 "ignore the spark until further notice").

## What was ruled, so what this PR must be
- Kam, card `secuura-tenant-isolation-migration-ks1401-1005` = a (2026-10-05), as recorded by Wednesday's 19:23 boot note and carried in Seat R 85th's brief: write the migration now; EXISTING rows with no tenant take the PLATFORM DEFAULT tenant; apply it with the KINTSUGI deploy, never demo. UNMEASURED by this commission: the card's verbatim option text (the gate may read it: `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-tenant-isolation-migration-ks1401-1005`, a read command).
- Wednesday at R 85th's plan confirmation (19:5x): default tenant `a0000000-0000-4000-8000-000000000001` approved; NULL-only backfill; RLS ENABLE + FORCE + a policy; numbering 058 (057 is PR 2001's).
- R 85th's one change from PR 1383's draft: the policy is created BEFORE the backfill (a NOBYPASSRLS owner updates 0 rows on a forced table with 0 policies). Mutant M6 shows it.

## Questions (tier 1: measure, do not take the READY's word)
1. **Scope:** `git diff --name-only <merge-base> <head>` = the 4 new files the READY lists (+759/-0); the migration's sha256 prefix 92d368fb4ae7.
2. **Read 058 whole, with line numbers.** For each of the four tables: what it backfills (NULL-only? which column? to which value?), what RLS it enables, FORCE, the policy's exact USING/WITH CHECK terms, the bypass GUC, lock_timeout, and the absent-table behaviour (RAISE). State what an app connection that is NOT platform_admin and has no tenant GUC set can read/write on each table before and after 058.
3. **Real PostgreSQL 15 (yours, not the seat's):** `/opt/homebrew/opt/postgresql@15/bin/` with YOUR OWN data dir and socket under `<workdir>/tmp`, a 127.0.0.1 port you pick; never /opt/homebrew/var/postgresql@15, never /private/tmp/r85t, /private/tmp/f30t or any other seat's cluster. Build the schema from develop's migrations through 056, plant rows (NULL tenant, tenant A, tenant B) on each of the four tables, apply 058 through the repo's real runner (run-migrations.sh and/or runStartupMigrations), then measure: NULL rows now carry the default tenant; tenant A reads only A's rows (and the default tenant's? state exactly); tenant B cannot read A's; the platform-admin arm reads all; writes with the wrong tenant are refused. Reproduce the seat's P-cells (no over-blocking of a tenant's own rows).
4. **ORDER WITH PR 2001's 057 (the question the seat could not answer — both PRs are open, built on bases without each other):** with 058 applied and 057 NOT yet present, then 057 added later (PR 2001 merging second), does the repo's runner apply 057? Does it refuse, skip or apply out of order? And in the other order (057 then 058)? Read the runner's ordering/recording logic (file:line) and DRIVE both orders on your cluster using PR 2001's 057 file at its head 74ccf8666dc2 (fetch refs/pull/2001/head into your clone). A gap that leaves 057 unapplied after 058 is FIX-BEFORE-MERGE or a merge-order rule for Wednesday: say which, with the evidence.
5. **Re-run safety:** is 058 idempotent (applied twice, or applied where 039 is recorded but some of its effects are missing — the KS-1401 title case)? What does the runner do if 058 fails mid-way (transaction? partial state?). Measure one failure (e.g. the lock_timeout path or a planted absent table) and read the state after.
6. **Base vs head permissiveness:** for every reader role you can construct (app role without GUC, app role with tenant A, platform_admin, the migration owner), is any head outcome MORE permissive than base? (Expected: none; head adds isolation.) Then the reverse, which matters here: name every head cell that is STRICTER and could break a live path (an app query that runs without a tenant GUC today). Read the gateway/originate code for queries on these four tables that run without setting the GUC (grep by table name at the head, list file:line) and say whether each still works after 058. An over-block on a live path is FIX-BEFORE-MERGE.
7. **What merging does by itself:** merging puts 058 on develop. Measure (read the code, compose files and deploy scripts at the head) which environments apply migrations automatically on boot (the gateway's runStartupMigrations? run-migrations.sh in an entrypoint?), and whether any of them deploys from develop WITHOUT a human step. If merging alone can apply 058 to kintsugi or demo, say so plainly: Kam's ruling says the apply happens WITH the kintsugi deploy, never demo, so an automatic apply on demo is HOLD-FOR-KAM.
8. **Red-proof:** reproduce at least 5 of the seat's 12 mutants (include M1 NULL guard, M2 FORCE, M4 default tenant, M6 order, MC4 platform_admin arm) against the committed 058, count your own table, name survivors (MC1/MC2 are claimed equivalent: check that claim).
9. **Title/body:** title "Refs KS-1401: migration 058 restores tenant isolation where 039 is already recorded" (count <= 92); no close-word before a key; the body carries the apply plan (kintsugi only, DEFAULT_TENANT_ID read before apply, STOP if different) — read the body via the API if you can; else UNMEASURED.
10. **Merge:** merge-tree of the head onto develop 536642104002f506f61e2e9b6c98a32bf19c3b10 (rc + full tree). Re-pin at the end.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch PR refs into YOUR clone only; never write to the checkout).
- **PR 2002** head `eec20acf0b257d6313331d01042abcad2a1d7fb0`, develop `536642104002f506f61e2e9b6c98a32bf19c3b10` (Wednesday's ls-remote 23:1x AEDT). PR 2001 (057) head `74ccf8666dc2673ed863451bb8eadc9dcd299098` (for question 4 only; gate 189 is gating PR 2001 itself — do not duplicate its questions).
- R 85th's READY saved here as `ready_2002.txt` (read it whole). R 85th's evidence: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatR-85th/` (read-only).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/`. DevMASTER ~143 GiB free; stop and report under 2 GiB.
- Live: gate 189 (another subagent) may be running its own PostgreSQL cluster under `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate189-ks1256-pr2001/tmp` and a container g189-redis: never touch them; pick a port that is free at the moment you start (`lsof -iTCP -sTCP:LISTEN`). Seats R 85th (author, wrapping), E 36th and F 30th: do not touch their worktrees, processes or clusters. You do not need Docker.
- NOT TESTED by design unless you do it: kintsugi's real data (NULL counts, its DEFAULT_TENANT_ID — the deploy seat reads those), Node 24, a real gateway container. Say so.

## Verdict
Line 1 per gate_common section 6, for PR 2002, and the merge tree on 536642104002 for the merge seat, plus a one-line MERGE-ORDER rule relative to PR 2001 if question 4 needs one. Then FOUND / TESTED / HOW with controls.

---

# gate_common.md: the common section of every QA gate commission

Paste this file WHOLE into every gate commission (Agent-tool subagent or cockpit seat), after the
gate-specific part (subject, questions, cells). It is client-neutral: the client, repo, PR, head and
the questions live in the gate-specific part, never here.

Why this file exists (2026-11-03): the common section lived in a session scratchpad and died with it,
so gates 161-165 were briefed by copying gate 160's verdict. A mechanism is recorded by its PATH
(lesson 2026-09-07). Edit this file, never a copy.

## 1. Role
- You are a QA GATE. Findings only. You never fix, commit, push, open or edit a PR, post a comment,
  write a ticket, send mail, deploy, or tell any human anything. Your output is one verdict file.
- You report to Wednesday only, as your final message (section 7).

## 2. Where you may write (the workdir)
- Your workdir is the folder the gate-specific part names, under
  `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/<YYYY-MM-DD>_gate<N>-<ticket>-pr<n>/`.
  Write NOTHING outside it.
- At creation, before anything else, write `<workdir>/.gitignore` with at least:
  `repo/`, `scratch/`, `home/`, `tmp/`, `mut/`, `runs/**/*.bin`. Clones, throwaway trees and any
  generated credential stay ignored. The verdict, harness and results are tracked.
- YOUR SHELL'S CWD IS WEDNESDAY'S TREE, not your workdir. A relative runner scans and writes into it
  (gate 119, 2026-11-02, wrote `node_modules/.vite/...` into Wednesday's root). So:
  - anchor every runner: `vitest --root <dir>`, `npm --prefix <dir>`, `jest --rootDir <dir>`,
    `npx --prefix <dir>`; or `cd` inside a `bash -c '…'` whose path is in your workdir;
  - **AND start every test or app process with its CWD inside your workdir** (`bash -c 'cd <workdir>/cwd && …'`):
    `--root` does NOT stop code under test writing RELATIVE paths into the process cwd. Gates 183 and 184
    (2026-11-04) both appended production-logger lines to Wednesday's `logs/combined.log` this way, with
    `--root` set correctly;
  - run untrusted or stateful steps under `env -i` with `HOME=<workdir>/home` and
    `TMPDIR=<workdir>/tmp` (keep TMPDIR short: socket paths over ~104 bytes break tsx IPC).
- STOP every background process you started before you report (list them; kill by pid; never by
  basename; never pid 1). Wednesday runs `gate_stray_check.sh` before the next GO and it refuses on
  any stray file.

## 3. The client checkout is READ-ONLY to you
- READ git verbs only on the project's checkout: `ls-remote`, `show`, `log`, `diff`, `cat-file`,
  `ls-tree`, `merge-base`, `rev-parse`, `grep`. NEVER `fetch`, `pull`, `worktree`, `checkout`,
  `merge-tree --write-tree`, `commit`, `stash`, `gc` there: those write its `.git`.
- For anything that writes: `git clone --shared <checkout> <workdir>/repo`, then
  `git -C <workdir>/repo fetch origin refs/pull/<n>/head` (a PR ref cannot be truncated, a branch
  name can) and run write verbs only inside `<workdir>/repo`.
- Never print, copy or write a secret value. Results show counts, truncated hashes, modes and key
  names only. If a harness must hold a generated value, it stays in an ignored folder.

## 4. Subject: pin it, at the start AND the end
- `git ls-remote origin refs/pull/<n>/head refs/heads/develop` at the start and again at the end;
  write both into the verdict. If the head moved, say so first and stop.
- `git merge-tree --write-tree <develop> <head>` (in your clone) on the CURRENT develop: rc and tree.
- State host versions you ran on (Node, TypeScript, the test runner) and what you did NOT run on.

## 5. Method: what makes a measurement count
- **The class bar (fix-a-thrown-value / error-path PRs):** head must end in exactly the state base
  reaches with an ORDINARY Error, at every changed site. Count cells; name any head cell MORE
  permissive than base-ordinary. That count decides HOLD-FOR-KAM (section 6).
- **Red first:** the PR's new tests (and your own cells) fail at base by ASSERTION, pass at head.
  A cell that passes at base is not proving the fix; say which.
- **Drive the real thing** where you can: the real module by blob, the real route over HTTP, a real
  database. Say plainly what was read and not driven.
- **Every zero needs a control that would have produced a non-zero, run in the same action**, from a
  source independent of the thing you are testing (a different file or syntax you did not write).
  A zero from an instrument that could not fire is not a zero.
- **Mutants:** run them, then COUNT THE RAW TABLE yourself; headline = table, or say it differs.
  Name each survivor and whether it is equivalent.
- **Never re-implement a tool to check the tool**: read its lines, or make it print what it computed.
- Never `grep -r` / `find` over `/Volumes/DevMASTER/WEDNESDAY` or any local-model `runs/` or `night/`
  tree. Open named files. If a call runs past ~2 minutes, it is stopped or its reason is written.

## 6. The verdict file: `<workdir>/verdict.md`
Line 1, exactly one of:
- `GO — MERGE` · `GO WITH NOTES — MERGE (no HOLD-FOR-KAM)` · `GO WITH NOTES — HOLD-FOR-KAM (<reason>)`
  · `NO GO (<FIX-BEFORE-MERGE ids>)`

Then:
- `# QA Gate <N> (Tier <t>, round <r>): PR <n> / <ticket> <subject>`
- Subject block (section 4), method in one paragraph.
- `## Findings`: one `### G<N>-F<k> — <SEVERITY>[ — FIX-BEFORE-MERGE]: <one line>` each, with three
  fields: **FOUND** (the claim), **TESTED** (scope: what was and was not exercised), **HOW** (the
  instrument, the command, the controls). Pre-existing findings say PRE-EXISTING (base = head).
- `## What passed (measured)`: per question, the counts.
- `## NOT tested`: everything a reader might assume you covered and you did not. A reachability or
  exposure word ("reachable", "in production", "any caller") appears in a finding only if it was
  measured; otherwise it is listed here.
- `## Plain answer for Kam`: 3-6 plain sentences, no jargon, what a merge would change for users.

HOLD-FOR-KAM is WRITTEN when: any head outcome is more permissive than base-ordinary; or the change
touches a signature class (production, money or payouts, a message to a human, anything
irreversible). Wednesday RULES whether it holds; you only state the condition and the evidence.

## 7. Report back to Wednesday (your final message, short)
- The verdict's first line, the verdict path, findings by severity (ids), mutant counts, the head
  and develop you measured at start and end, every background process stopped (pids), and any stray
  file you know you wrote outside the workdir (there should be none).

## 8. Rounds
- Tier 1 / tier 2 per `0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`. Round 2 is
  a DELTA: it re-tests the round-1 FIX-BEFORE-MERGE items and the forms that held, not the whole PR,
  unless the gate-specific part says otherwise. Two NO GO rounds on one class is the cap.
