# Gate 189 commission — Secuura / Blockchain, PR 2001 (KS-1256 connector allow-list still fails open when the settings key is missing), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-04 22:5x AEDT. Model: Opus (routing v1.0 tier-1 gate: an authorisation / allow-list path on the gateway, plus a migration). Spark shadow: NOT run (Kam 16:42 "ignore the spark until further notice").

## What was ruled, so what this PR must be
- The defect (Seat W 24th, stack w24 at ee1e1b832115, KS-1256 comment 07:40Z): with Redis UP and the settings key EVICTED/missing, a restricted connector registered an out-of-scope document (201; 403 with the key present; 503 with Redis down). allkeys-lru is set in both compose files.
- Wednesday's design ruling (ANSWER to Seat E 35th, 08:08:12Z, inside Kam's 2026-10-27 design grant and his 09:16 "clear and close" instruction; Kam told on the panel bf-ae55c020a61a, hold offered, none received) = OPTION C: a Postgres settings row is the source of truth + a migration (057) seeding TODAY's defaults so a fresh env behaves exactly as now; PUT /api/admin/settings writes the DB then Redis; readers fall back to the DB on a Redis miss; 503 only when Redis is down, or when BOTH the key and the row are missing.
- Accepted at 08:18:55Z (E 35th PROGRESS 1): item 4 (backfill) and item 6 (a configured bypass is restored on eviction: on the ONE create cell Redis-up / key-missing / bypass-row, develop goes through the workflow gate and head skips it, 2 of 180 bypass cells). Item 6 is the ONE accepted more-permissive row; everything else must be base-or-stricter.

## Questions (tier 1: measure, do not take the READY's word)
1. **Scope:** `git diff --name-only <merge-base> <head>` = the 19 files the READY lists (+709/-28); name any that is not gateway/originate settings code, its tests, the migration, or the two docs fragments.
2. **Base vs head, the full matrix:** for every combination of Redis {up, down, throwing} x key {present, missing} x stored row {present, missing, unreadable} and each reader (create path, GET /api/connector/info, PUT /api/admin/settings), is any head outcome MORE permissive than develop? Reproduce the seat's 420-cell ratio (47 stricter / 373 same / 0 looser) with YOUR harness from the committed bytes, and separately the 180 bypass cells (2 differ, accepted). Any looser cell other than the accepted item-6 row = HOLD-FOR-KAM.
3. **Real Redis + real Postgres (the seat ran neither):** at least the headline cells for real. Postgres: `/opt/homebrew/opt/postgresql@15/bin/` (keg-only, installed tonight by Seat R 85th) with YOUR OWN data dir and socket under `<workdir>/tmp` on a 127.0.0.1 port you pick; never the default cluster dir /opt/homebrew/var/postgresql@15, never another seat's /private/tmp/r85t or /private/tmp/f30t. Apply migration 057 to it and read the seeded row. Redis: no local redis-server exists (Wednesday found none at /opt/homebrew/bin). You MAY run ONE throwaway Docker container named `g189-redis` from a redis image ALREADY present locally (`--pull never`; if none is present, say so and fall back to the seat's mocks), delete the key to simulate eviction, and REMOVE that container before you report. Touch no other container. Cells: key evicted + row present -> head allows only the allow-listed doc type (403 for the out-of-scope one); key evicted + row missing -> 503; Redis down -> 503; key present -> as develop.
4. **First boot unchanged:** on a FRESH database with 057 applied and an empty Redis, the readers behave exactly as develop does today with defaults (Platform S API-key creation must NOT 503). Measure it.
5. **PUT ordering + failure:** PUT writes the DB then Redis. Measure: DB write fails -> what is returned, and is Redis untouched? Redis write fails after the DB succeeds -> 503 and stale Redis (the seat's candidate 2): confirm and grade (LOW/MEDIUM), do not fix.
6. **Migration 057:** the number is free on develop 536642104002 (highest 056) and in the open PRs (R 85th's KS-1401 is 058; PR 1383 holds 049): re-measure. Is it idempotent / safe to re-run? Does it seed exactly the defaults the code uses today (read both, name file:line)? Down path, if the repo has one.
7. **Red-proof:** reproduce at least 4 of the seat's 11 mutants against the committed bytes (choose the ones on the DB-fallback branch and the 503 branch), count your own table, name survivors.
8. **Nothing secret leaks:** the settings row and the allow-list values appear in no log line or response that develop did not already expose (planted marker + positive control).
9. **Title/body:** title starts "Refs KS-1256:" and is <= 92 chars (count); no close-word before a key; the body's "Before this deploys" steps (the first-hit window, step 3) are present (read the body via the API if you can; else UNMEASURED).
10. **Merge:** merge-tree of the head onto develop 536642104002f506f61e2e9b6c98a32bf19c3b10 (rc + full tree). The branch was built on d92b849ece73 and develop has since moved (1796, 1968, 1798 merged): name any shared path with those (the READY says overlap 0). Re-pin at the end.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch the PR ref into YOUR clone only; never write to the checkout).
- **PR 2001** head `74ccf8666dc2673ed863451bb8eadc9dcd299098`, develop `536642104002f506f61e2e9b6c98a32bf19c3b10` (Wednesday's ls-remote 22:5x AEDT).
- E 36th's READY saved here as `ready_2001.txt` (read it whole). E 35th's HANDOVER and E 36th's evidence: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatE-35th/` and `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatE-36th/evidence/` (read-only).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate189-ks1256-pr2001/`. Dependencies only from an install matching the lock at the head; never link from the shared checkout's node_modules. DevMASTER ~143 GiB free; stop and report under 2 GiB.
- Live seats: E 36th (the author, idle), R 85th and F 30th (pushing through the shared lock). Do not touch their worktrees, processes, Postgres clusters or ports.
- NOT TESTED by design unless you do it: Node 24, a real deploy, kintsugi, real clients (Platform S). Say so.

## Verdict
Line 1 per gate_common section 6, for PR 2001, and the merge tree on 536642104002 for the merge seat. Then FOUND / TESTED / HOW with controls.

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
