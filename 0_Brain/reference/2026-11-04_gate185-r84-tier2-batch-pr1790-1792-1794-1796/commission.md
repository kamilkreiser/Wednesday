# Gate 185 commission — Secuura / Blockchain, TIER 2 BATCH: PRs 1790 (KS-1340), 1792 (KS-1499), 1794 (KS-1600), 1796 (KS-1458), ROUND 1 of 2

Written by Wednesday 2026-11-04 18:59 AEDT. Model: Sonnet (routing v1.0 tier-2: test-only / comment / baseline / docs changes). Builder: Seat R 84th (refreshed all four today). Its READY, saved here as ready_r84_batch.txt: read the sections for these four PRs WHOLE.

## Heads (R 84th's READY; re-pin yourself) and develop
- PR 1790 head aa1f6b7739918ed76194970ed810e57f831099d0 · PR 1792 head f364327e266ce321bfeb6e3a52b045904d8d8527 · PR 1794 head 06fe8557ec43be6879a854c345b3829b9417b2e0 · PR 1796 head 759fd6fb19aaa22df4bd86dd61dcb6d4a9832fa8
- All four built on 5c1ca287ed74; develop is now c7abf98e51030f908050fede10a3546871d4f2c1 (Wednesday's ls-remote 18:5x AEDT); R 84th measured 0 shared files between each PR and 5c1ca287ed74..c7abf98e51030f908050fede10a3546871d4f2c1 (control fired).

## Questions per PR
1. Scope = the files R 84th lists for that PR (git diff --name-only); 1796's users.ts change is COMMENT LINES ONLY (prove it: the diff of users.ts has no non-comment line).
2. The tests prove what they claim: for test-only PRs, each new/changed cell fails on a deliberate break of the behaviour it pins (one mutant per PR, parsed first, restored byte-equal), and passes at the head. Count your raw table.
3. Suites: run each PR's named test files (anchored, cwd inside your workdir). The DB-gated suites of 1790/1792/1794 need PostgreSQL: if you cannot run them without Docker, say NOT RUN and rely on R 84th's counts (stated as its), do NOT start or touch Docker (other seats' containers are live).
4. Docs: fragments only (no edit to the two shared Projects Documents pages); docs-fragments check OK.
5. Pairwise: the four PRs share no file with each other (R 84th: 1 of 15 pairs shares a file, 1796 with 1798 only); merge-tree of EACH head onto c7abf98e51030f908050fede10a3546871d4f2c1 (rc + tree) and the batch order 1790 -> 1792 -> 1794 -> 1796 applied in sequence onto c7abf98e51030f908050fede10a3546871d4f2c1 (each rc 0; name each resulting tree).
6. Titles start "Refs KS-<that ticket>: ", <= 92 chars; no close word directly before a key in the commit message (PR bodies UNMEASURED if you have no gh login: say so).

## Verdict
Line 1 per PR (one line each, in the first four lines): GO / GO WITH NOTES / NO GO (<ids>), then the merge trees for the merge seat on c7abf98e51030f908050fede10a3546871d4f2c1 and the sequential trees. FOUND / TESTED / HOW with controls.

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
