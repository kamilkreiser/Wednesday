# Gate 170 commission — Secuura / Blockchain, PR 1985 (KS-1961), TIER 1, ROUND 2 of 2 (DELTA)

Commissioned by Wednesday (15:4x AEDT 2026-11-03 rotation-successor seat). Model: Opus (routing v1.0, tier-1 gate row; gauge 7d 80%, the 80-90% band: a gate is an allowed cloud launch).

## Subject (Wednesday's ls-remote at 04:42:45Z — re-pin it yourself, section 4)
- Repo: Secuura/Distributed_Secuura (github). Read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`.
- PR 1985, branch `fix/ks-1961-gateway-fail-closed`, head `a0a91f65d0006d1adc69325002e6ddf69abffc2b`.
- develop `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8` (PR 1986's squash; it moved AFTER the builder merged develop `67309f28ab21` into the branch). Measure merge-tree against ca2b2aa, the CURRENT develop, and say whether the 1986 change touches any file this PR touches.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate170-ks1961-pr1985/` (this file is in it; leave it).
- **Disk: DevMASTER has ~22 GiB free (99% full).** Keep the clone small: `clone --shared`, and symlink node_modules from the read-only checkout instead of installing (gate 168 did this at 372 MB). If free space falls under 15 GiB, stop and report.

## Read first
1. Gate 168's verdict, whole: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate168-ks1961-pr1985/verdict.md` (its 9 rateLimit + 5 window input table under G168-F1 is the base of your F1 work; its harness is under `scripts/` there; reuse it by reading, do not edit that folder).
2. The builder's round-2 evidence, read-only: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatS-15th/evidence/ks1961/round2/` (red2_vs_round1, suite_head, mutants.out, ceiling_develop / ceiling_head, push/). These are the builder's claims. Re-measure them; do not quote them as results.
3. The PR body (GitHub API read, or the PR ref in your clone) for the round-2 "Ran" section and its 14-input develop/head table.

## What round 2 claims (the builder's READY, 04:39:20Z, verbatim intent)
Wednesday ruled after gate 168: a TRUTHY malformed rateLimit or window -> refuse (503); a FALSY value keeps develop's default path byte-for-byte. Also: F3 the guard's 429 write is in a try; F4 the KS-616 degrade log line carries the value's type only (behaviour unchanged); F5 a test kills mutant M9.

## Your questions (DELTA, round 2 of 2 — the cap: a NO GO here goes to Kam as a card, never a round 3)
- **F1 (the deciding one):** for EVERY one of gate 168's 9 rateLimit inputs and 5 window inputs, plus any malformed form you can add (truthy and falsy: '5', true, -1, 0, '', null, NaN, Infinity, {}, [], fractions, '120', etc.), is head's outcome EVER more permissive than develop's (`ca2b2aa`) for the same input? That means a higher effective ceiling over two or more bursts, or reaching the downstream handler where develop refused. Count the cells. Are falsy values byte-for-byte develop's path (same calls, same ceiling, same log)? Any head cell more permissive than develop = write HOLD-FOR-KAM (section 6), whatever its severity.
- **F3:** can the guard's 429 write still hang the login, leave an unhandled rejection, or leak thrown text to the client or the log?
- **F4:** does the degrade line still carry any value text? Is the degrade BEHAVIOUR unchanged against develop?
- **F5:** is M9 now killed? Re-run the mutants, count the raw table yourself, and name the survivors.
- **Also:** did round 2 introduce anything new? Red-first for the new cells (fail at round-1 head `1e8c43fcaf6c` or at develop by assertion, pass at a0a91f65). Run the touched suites at head.

## Not yours
No Redis, no booted gateway, no auth-service lockout (those are the builder's NOT DONE list; leave them under NOT tested). Do not re-gate G168-F2 (positive, held) beyond a smoke check that it still holds.

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

