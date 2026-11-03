# Gate 178 commission — Secuura / Blockchain, PR 1994 (KS-1868 "PR 16"), TIER 1, ROUND 1 of 2

Written by Wednesday (the 01:5x seat) 2026-11-04 03:28 AEDT. Model: Opus (routing v1.0 tier-1 gate row: request-handling catches on PUBLIC routes). Gauge 94%: usage is a guide (Kam 2026-10-22, 10-29 "minimal but used when necessary"); a tier-1 gate is a necessary Claude use (no merge without a gate; no local tier gates a tier-1 change).

## Subject (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (it may NOT hold the PR objects; fetch them into YOUR clone only, using the checkout's core.sshCommand; never write to the checkout). Read origin by `git -C <checkout> ls-remote origin <ref>`, never `ls-remote <path>`.
- At commission (Wednesday's ls-remote 16:28:03Z): develop `ea5134d6b98c470615c59fca5d3ec30356adfbd7` (PR 1992's squash, merged ~16:2xZ); **PR 1994** head `74dc459edbb6cdef368f0bc74a54b081cc4b3835`. Per the seat: ONE commit whose parent is `79145a312f01` (develop before 1992 merged), 11 files +957/-8; ONE product file `services/nft-certificate/src/routes/nft.routes.ts` (8 hunks, passes O98-P2..P9) + 8 new test files + a fragment pair. Re-pin both yourself; measure the parent.
- READY mail saved whole: `ready_1994.txt` in this folder — read it first. Its FLAG is the seat's READING of the code ("read from the source and from the 16 red cells; no request was sent to a running service"), NOT a measurement.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate178-ks1868-pr1994/`. **Disk: DevMASTER ~23 GiB free; stop and report under 18 GiB.** Clone small (sparse `Blockchain/Dev`, `--shared` from the checkout). Gate 176's / 175's install method (their verdict.md "Install" sections, `../2026-11-03_gate176-ks1868-pr1992/`, `../2026-11-03_gate175-ks1868-pr1990-pr1991/`) is the model; link an earlier install ONLY if you hash-check the lock blobs equal at your head.
- **Load:** host load1 has been 8-13 tonight (Spotlight indexing a moved archive + two seats). Re-run a timed-out cell alone before calling it a failure, and say you did.
- The raise seat ran NO base-against-head recorder (Wednesday's ruling): the measuring is YOURS.

## Questions (answer each with counts; base = 79145a312f01, head = 74dc459edbb6)
1. **THE CLASS BAR (decides the weight).** Drive the REAL Express app/router for each of the eight handlers (GET /certificates/:id, GET /certificates, GET /tiers, POST /estimate, POST /verify/transaction, POST /verify/asset, POST /ipfs/pin, POST /ipfs/unpin) over real HTTP (supertest or a listening server), with the handler's dependency stubbed to throw each of the 17 value classes gate 175/176 used (ordinary Error, message getter throws, revoked Proxy, null, undefined, string, number, Object.create(null), {message: Symbol}, {message: BigInt}, {message: revoked Proxy}, {message: object whose toString throws}, Proxy whose get trap throws, thrown Symbol, name getter throws, readable message with throwing toString, plain {message}). Base vs head per handler x class: status, body, whether a reply was sent at all (time-bounded), and process health after. **Bar: does any head cell answer anything OTHER than what base answers for an ordinary Error (status AND body), or leak more than base-ordinary?** A head cell more permissive than base-ordinary (e.g. a 2xx, a success-shaped body, or more fields) = HOLD-FOR-KAM.
2. **The two PUBLIC routes** (the seat: `app.ts:48` lists POST /nft/verify/asset and /nft/verify/transaction as publicOps): confirm the public listing at head with the line; drive both through the app's real middleware stack (auth/public-ops gate included), not only the router; confirm no handler's change alters who can reach it.
3. **Unchanged neighbours:** the three-dot diff of nft.routes.ts has exactly 8 hunks (seat's count, with controls) and the catches for mint, record, privacy-options, supported-chains, IPFS upload, metadata size and platform-fee are untouched: confirm by your own diff and name each neighbour's line at head.
4. **Sentinel (KS-1346/1348 rule: types and field names, never values):** plant a sentinel in a thrown value; can any of the eight paths print, log or answer it where base did not? Count both trees.
5. **Red-first and suites:** the 16 red cells fail at base BY ASSERTION for the stated reason (the handler rejects, no reply) and not by a harness artefact (the seat's own suggested question 2); pass at head. Whole `services/nft-certificate` suite before and after with ratios (seat: 30 files / 209 tests -> 38 / 241, all pass). Mutants on the eight changed catch blocks (raw table; count it; name every survivor, equivalent or not).
6. **tsc with tests and eslint** for the service (seat: 0 -> 0 errors; eslint 0/0): confirm.
7. **Merge-tree onto TODAY's develop** (ea5134d6, i.e. with PR 1992 merged) — rc and tree; and onto develop + PR 1993 (head `8712cb115e0a`, next to merge): rc and tree. Paths shared with PR 1993's 10 files: count, with a planted control. Callers of the eight endpoints: your own `git grep` at head with a positive and a negative control (the seat found only the gateway description map api-gateway index.ts:834 and an e2e fixture).
8. **Express version and semantics:** the seat says Express 4.22.3 in the tree does not catch an async handler's rejection. Confirm the installed version from the lock blob and that claim (a rejected async handler leaves the request open under Express 4) with a control.

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
