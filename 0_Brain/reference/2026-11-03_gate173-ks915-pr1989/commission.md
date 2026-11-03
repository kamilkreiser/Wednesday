# Gate 173 commission — Secuura / Blockchain, PR 1989 (KS-915 rebuild), TIER 1, ROUND 1 of 2

Written by Wednesday (19:0x AEDT 2026-11-03, the 15:4x seat); to be LAUNCHED by whichever Wednesday seat holds the floor once gate 172 (PR 1988) has finished (disk). Model: Opus (routing v1.0, tier-1 gate row).

## Subject (Seat E 31st's READY FOR GATE 08:03:34Z — re-pin it yourself, section 4)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`.
- PR 1989, branch `fix/ks-915-restore-local-secrets-readers`, head `ea41c34668ddc93f02a4dd997c365b9975a8adb3`. develop at the READY: `de8d208a8426747b3a752309e08167fa0de4b2ff` (re-read; it may have moved).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989/`.
- **Disk: DevMASTER ~16 GiB free at writing.** Clone small. If free space falls under 15 GiB, stop and report. Never run the script or compose against anything but a temp dir you created; compose's resolved output can carry values: keep it in a 0600 file in your workdir's ignored scratch, read names and host parts only, never echo or paste it.
- The predecessor PR 1982 (same ticket, E 30th) stays OPEN and untouched; gates 165/166 are the baseline: `0_Brain/reference/2026-11-03_gate165-ks915-pr1982/verdict.md`, `0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2/verdict.md` and its `harness/` + `results/` (the 28 slip forms). Read both verdicts whole.

## What the PR claims (builder's READY, read whole by Wednesday; CLAIMS — re-measure)
`Blockchain/Dev/scripts/restore-local-secrets.sh` rebuilt per Kam's card `secuura-pr1982-restore-script-round2-nogo-1103` = a ("Rebuild the check using the real tools' reading"). Before any write it asks dotenv (the copy node resolves from Blockchain/Dev, 16.6.1, version printed), a sandboxed bash `set -a` (set -r, empty PATH), and `docker compose config` through BOTH the Blockchain/Dev entry and the repo-root `docker-compose.local.yml` entry, then a canonical-line check, over Blockchain/Dev/.env (or its template), .env.local, the repo-root .env and the shell. Refuses (exit 3) if any reader reads NODE_ENV=production or a non-local DATABASE_URL / PGHOST / PGHOSTADDR / PGSERVICE; a reader that cannot run refuses and names `npm ci` / docker. Re-checks after bootstrap-env.sh; ADMIN_USER_PASSWORD / ALLOW_DEFAULT_SEED_PASSWORDS decided by what compose passes to auth; writes a gitignored temp copy, re-reads it with compose and dotenv, then replaces .env; 0600; never prints a value. Wednesday's rulings accepted in the plan (compose reads NODE_ENV only; fail closed on a missing reader with an actionable message; e12 reachability probe-only; the second compose entry). Builder figures: suite 267/267; script-absent 238/267 red; PR 1982's script 110/267 with every one of gate 166's 28 forms NOT refused there; 25 mutants, 21 killed, 4 surviving by design inside one reader and refused by the canonical-line check (a layered run kills each by its own cell).

## Your questions (the builder's list, which is right; answer each with counts)
1. For every one of gate 166's 28 forms and any new one you can construct: can the script WRITE while dotenv, bash set -a, or docker compose (either entry) reads production or a non-local database? (The class bar: head never writes where any real reader would reach production/remote.)
2. Does a reader that cannot run fail closed: docker absent, node absent, node_modules absent, compose config failing or answering an unexpected shape, a .env bash cannot parse or that ends the reading shell?
3. Can any path print or commit a generated value (stdout, stderr, the temp copy, the sandbox temp dir, compose's resolved output, a failing test cell)? Plant a sentinel and search every carrier.
4. Does a second run ever change a working set? Does --rotate leave an old value anywhere?
5. Does the output file, or any temp file, escape the gitignore?
6. Probe the new parts hardest: the sandboxed bash reader (can a .env line create a file, run a command, read outside, or hang it?), the repo-root .env + root compose entry, PGHOST/PGHOSTADDR/PGSERVICE, and the re-read of the temp copy before the rename.
7. Mutants: run them, count the raw table, name every survivor and whether it is equivalent or killed only by the layered run.

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

