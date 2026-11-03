# Gate 179 commission — Secuura / Blockchain, BATCHED: PR 1995 (KS-1320) + PR 1996 (KS-1343), TIER 2 documentation, ROUND 1 of 2 each

Written by Wednesday 2026-11-04 ~09:4x AEDT. Model: Sonnet (routing v1.0 tier-2 gate row: docs only). ONE gate session for two disjoint docs PRs (Kam 2026-09-18: minimise gate duplication). Give each PR its OWN verdict section and its own GO / GO WITH NOTES / NO GO line. Spark shadow: NOT run (the Spark host does not resolve from this network today; stated, not skipped silently).

## Subjects (re-pin both yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (it may not hold the PR objects; fetch them into YOUR clone only, using the checkout's core.sshCommand; never write to the checkout). Read origin by `git -C <checkout> ls-remote origin <ref>` (a read verb).
- develop at commission: `ee1e1b83211504f96ebccba325d1ef7139bc83cc` (Wednesday's ls-remote 09:23:28 AEDT; R 82nd's read 22:39:24Z equal).
- **PR 1995** (KS-1320, Seat R 81st): head `15c32a6ef6b6d37b812dfc2b7329e12c87202b03` (per R 81st's READY 16:53Z, NOT re-read by Wednesday today), one commit on `ea5134d6b98c`, `Blockchain/Dev/CONTRIBUTING.md` +3/-1: tells a PR author the 92-character squash-subject limit.
- **PR 1996** (KS-1343, Seat R 82nd, PARTIAL: notes N-1286-4/-7/-8 only): head `6ccdccb07199e8260f675ad2dd851ea42025a4bc` (R 82nd's ls-remote 22:39:24Z = PR API head), one commit on `ea5134d6b98c`, MULTI-TENANCY.md +3/-2 and RLS-FAIL-CLOSED-PLAN.md +1/-1. READY mail saved in this folder as `ready_1996.txt` (read it whole).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate179-ks1320-ks1343-pr1995-pr1996/`. Disk: DevMASTER ~21 GiB free; stop and report under 15 GiB. Clone small (sparse, `--shared` from the checkout). No dependency install is needed for a docs gate.

## Questions (answer each with counts and the lines you read; base = each PR's parent, head = the PR head)
### Both PRs
1. **Truth of every changed sentence (decides the verdict):** for each added or changed sentence, open the code, config or doc it describes AT HEAD and say whether it says only what the repository shows. A sentence about behaviour is checked against the code path, not against the ticket. Quote file:line for each check. A sentence that claims more than the code shows = NO GO; one that is true but unclear = NOTE.
2. **What it says was not checked:** each PR says what it did NOT verify (R 82nd's item 5; the new RLS sentence says the live app's settings were not checked). Is that limit stated in the doc text itself where a reader needs it?
3. **Scope:** the diff touches only the named files (`git diff --stat`), no code, test, config or fragment; PR 1996's PARTIAL is stated in its body and its KS-1343 comment (`fa23c3ab-f025-4503-8095-72e765f019f1`), and the five other notes (N-1286-3/-5/-6/-9/-10) are NOT claimed done.
4. **Merge:** merge-tree of each head onto develop `ee1e1b832115` (rc and tree, full 40-hex), and of PR 1996 onto develop-plus-PR-1995 (0 shared paths, with a planted control). Name the expected squash trees for the merge seat.
5. **Body hygiene:** PR title starts `Refs KS-NNNN: ` and is <= 92 chars; Test Evidence block present; no close-words that would auto-close a ticket (planted control); no `@` mention; no secret-shaped string.
### PR 1995 only
6. Is the 92-character figure true for this repo's squash-subject rule? Find where the limit is enforced or documented (tool, hook, CONTRIBUTING, merge tool) and quote it; if nothing enforces 92, say so.

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
