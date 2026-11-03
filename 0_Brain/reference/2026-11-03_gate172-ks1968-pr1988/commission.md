# Gate 172 commission — Secuura / Blockchain, PR 1988 (KS-1968 B1), TIER 1, ROUND 1

Commissioned by Wednesday (18:5x AEDT 2026-11-03). Model: Opus (routing v1.0, tier-1 gate row; gauge 7d ~84%, the 80-90% band: a gate is an allowed cloud launch).

## Subject (Seat F 28th's READY FOR GATE 07:46:47Z — re-pin it yourself, section 4)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`.
- PR 1988, branch `fix/ks-1968-hibp-wire-in`, head `ba973c53ecc3bfa5ff21d71b967c9d4344ad3d52` (one commit, 7 files, +349/-18), develop `de8d208a8426747b3a752309e08167fa0de4b2ff`.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate172-ks1968-pr1988/` (this file is in it).
- **Disk: DevMASTER ~16 GiB free.** Clone small (`clone --shared`); link node_modules from an install whose root lockfile and packages/ tree are byte-identical to head's (gate 171 used gate 148's install after hashing; check, do not assume). **If free space falls under 15 GiB, stop and report.**
- **ABSOLUTE: no request to the real HaveIBeenPwned service (api.pwnedpasswords.com) from anything you run.** Stub fetch in every cell; run suites under an outbound guard that blocks and counts requests to that host (the builder's is at `/private/tmp/f28t/hibp_guard.mjs`; read it, or write your own), and report its count (must be 0, with a positive control proving the guard fires).

## What the PR claims (builder's READY, read whole by Wednesday; these are CLAIMS — re-measure)
At register (after the existing strength check) and at reset (after the token and the account are validated, just before hashing), `isPasswordBreached(pw)` is called behind `HIBP_ENABLED`; a breached password is refused with a 422 VALIDATION_ERROR carrying ONLY Kam's sentence "This password has appeared in a data breach, choose another" (one details entry on the password field). A breach-service outage (throw, 2 s timeout, non-200) ALLOWS the password (Kam's option a, by design). Only the 5-hex-character SHA-1 prefix leaves the process (k-anonymity). vitest.setup.ts sets HIBP_ENABLED='false' only when unset. isPasswordBreached's catch logs the error TYPE only (four ks1868 cells C3, R4, R5, R6 changed on purpose from 'text' to 'type'). Change-password (users.ts) is NOT in this PR (B2, blocked on PRs 1798/1796).

## Ruling context
Kam's card `secuura-hibp-breach-check-never-runs-1103` = a (15:53:02): "Wire it in: refuse a breached password at sign-up, reset and change-password; if the breach service is down, allow it (as written)". The fail-OPEN on outage is his explicit choice, so it is NOT a HOLD-FOR-KAM condition. Kam's sentence is the only new user-facing text allowed.

## Your questions
1. Register and reset: is a breached password refused with ONLY Kam's sentence (exact bytes, status, details shape)? Is a clean password accepted? Is any other new user-facing string introduced anywhere (grep the diff)?
2. k-anonymity: capture the outgoing request in a stub and prove the URL path is `/range/` + exactly 5 hex chars, and the password, the full SHA-1 and the 35-char suffix appear nowhere in URL, headers or body.
3. Outage: throw, timeout (2 s), non-200 → password allowed at both routes. Switch: HIBP_ENABLED='false' → no lookup at all; unset in tests → setup sets 'false'; an explicit value is left alone.
4. Reset ordering: an invalid token → 404 and NO lookup; a refused (breached) reset leaves the token UNCONSUMED and nothing hashed or written (read the store after).
5. Register ordering: a weak password → the strength 422 and no lookup.
6. Logging: plant a sentinel in the error the breach call throws; it must reach no log line and no body (type only).
7. Red-first at develop by assertion; auth suite at head twice under the outbound guard (count 0); mutants (raw table counted, survivors named); tsc and the KS-1000 ratchet (the builder hit TS6059 with a literal import of vitest.setup and switched to a non-literal one — check it does not hide the file from the ratchet).
8. Is there any OTHER caller that sets a password and now differs in behaviour (enumerate password-setting routes repo-wide; POST /api/users/admin/create is a known candidate the PR leaves alone — confirm unchanged).

## Not yours
Change-password (B2). PR 1987 (KS-1967, already gated). No booted stack, no real breach service, no platform suites.

---

# gate_common.md (pasted whole, per its own rule; source: 2_Project_Files/fleet/qa-agent/gate_common.md)

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

