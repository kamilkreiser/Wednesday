# Gate 180 commission — Secuura / Blockchain, PR 1989 (KS-915 restore script), TIER 1, ROUND 3 of 3 (Kam's cap exception)

Written by Wednesday 2026-11-04 ~12:3x AEDT. Model: Opus (routing v1.0 tier-1 gate row: a secrets reader). Authority for a third round: Kam, live board 2026-11-04 09:33:42 AEDT, verbatim "Decision secuura-pr1989-gate174-cap-nogo-pgbouncer-1104: a — Allow one more round for F1 only (recommended)"; option (a)'s detail: "E 32nd's successor judges the five PGBOUNCER_* keys as plain integers in every reader (and refuses any newline), plus the one-line PATH lock for G174-F2; a narrow round-3 gate on just those; then merge on its GO". **There is no round 4: a NO GO here ships nothing and goes to Kam.** Spark shadow: NOT run (host unreachable from this network today).

## Scope — NARROW, by Kam's ruling
Gate exactly these, nothing else:
1. **G174-F1 (HIGH):** every reader judges PGBOUNCER_MAX_CLIENT_CONN, _DEFAULT_POOL_SIZE, _RESERVE_POOL_SIZE, _MAX_DB_CONNECTIONS, _MAX_USER_CONNECTIONS as plain integers (^[0-9]+$) and refuses any CR/LF in every value judge() reads (Wednesday's scope ruling: judged values only, not every environment value). Re-run gate 174's F1 forms (its verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/verdict.md) at the new head: each must be refused, and benign integer values accepted. Confirm the render oracle claim (a crafted value yields a second [databases] header in pgbouncer.ini at round 2, one at head).
2. **G174-F2 (LOW), built as shape (B) by Wednesday's design ruling:** `readonly PATH` before `set -r` in the bash reader plus a fail-closed refusal when the reader's stderr names PATH (count only). Prove: the PATH escape forms do not execute (unsandboxed control that DOES execute without the lock); the two same-line forms ("PATH=/usr/bin:/bin; POSTGRES_HOST=evil.example" and the PATH+= variant) are REFUSED, not under-read to the old value; a benign .env with ENV=, SHELL=, NODE_ENV=, MY_PATH= is accepted. On /bin/bash 3.2.57.
3. **The one surviving mutant:** e33_canon_value_pool_any SURVIVED (0/421). Decide: equivalent, or a real gap? If a real gap, is it reachable, and what severity?
4. **No regression:** the PR's whole suite at head, and gate 174's GO'd surfaces (G173-F1 host/port/db refusals, the credential-through-DATABASE_URL condition) still hold. Do NOT re-gate anything else.
Out of scope, named only (do not grade): G174-F3/F4/F5, G173-F2, the looping .env, entrypoint.sh:26-30 userlist echo (E 33rd's candidate).

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch PR refs into YOUR clone only, using the checkout's core.sshCommand; never write to the checkout).
- **PR 1989** head `df71e6b7c6258c6b01202d8fabedcdeafc445c95` (Wednesday did not re-read it after 12:09; E 33rd's ls-remote 01:30:06Z), previous head (round 2) `c71a6d106696`; develop `a01e579ca47be1ca60828537316823051730edf6` (one docs commit above the base ee1e1b832115 the branch merged).
- E 33rd's READY is saved here as `ready_1989_r3.txt` (read it whole; its cells, mutants table, F2 measurement).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate180-ks915-pr1989-r3/`. Disk: stop under 15 GiB free. Clone small (sparse, --shared).

## Verdict
Line 1: `GO` / `GO WITH NOTES` / `NO GO (<ids>)` for PR 1989, and the merge tree of the head onto develop a01e579ca47b (full 40-hex) for the merge seat.

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
