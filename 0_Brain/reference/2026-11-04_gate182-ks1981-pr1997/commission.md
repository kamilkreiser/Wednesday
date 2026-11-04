# Gate 182 commission — Secuura / Blockchain, PR 1997 (KS-1981 owner swap), TIER 2, ROUND 1 of 2

Written by Wednesday 2026-11-04 ~16:0x AEDT. Model: Sonnet (routing v1.0 tier-2 gate row G2: config/tooling, no deploy surface). Spark shadow: NOT run (host unreachable from this network today).

## Scope — NARROW (two lines in one file)
Kam ruled card secuura-ks769-close-keep-owner-1104 = a (live board 15:00:31 AEDT): "Close KS-769 and open a new review ticket dated before 2027-01-01; the exclusion row points to it". Wednesday ruled (N4, inside that ruling) that the entry's owner sentence (line 182) changes with the key (line 201). Check:
1. **Exactly two lines changed:** `git diff 5c1ca287ed74..<head> -- Blockchain/Dev/scripts/audit/lock-discovery.mjs` shows lines 182 and 201 only, KS-769 -> KS-1981 in the same words; lines 202, 207 (the superseded record) and 235 (expires 2027-01-01) byte-identical to develop; no other file (`--name-only`).
2. **Readers unaffected:** every reader of the entry's `ticket` field (audit-locks.mjs, lock-discovery.mjs printers, lock-discovery.test.mjs:110) still works; run `npm run audit:contract` from Blockchain/Dev in YOUR clone: want 59/59 (the pinned count), and the red proof (blank the key in YOUR copy -> failures, restore -> 59/59) reproduced by you.
3. **KS-1981 exists and is the right owner:** read-only Linear GraphQL (key sourced inside the process from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env, never printed): KS-1981 Backlog, Low, due 2026-12-15, board account, title about the mobile-tree exclusion review.
4. **No deploy surface:** no Dockerfile, compose file or CI workflow names lock-discovery (grep with a positive control).
5. **Title/body:** title starts "Refs KS-1981: ", is 92 characters or fewer (count it); body states the two-line reason; no close-word that would auto-close a ticket on merge.
6. **Merge:** merge-tree of the head onto develop 5c1ca287ed74b6353423a8c09e253abf3129233a (rc and full tree; S 17th predicts d06376c19fe6737f16ac926719381caa7c4052a6 since the head's parent IS develop). Re-pin develop at the end; if it moved, recompute and name the tree for the merge seat.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch PR refs into YOUR clone only via the checkout's core.sshCommand; never write to the checkout).
- **PR 1997** head `f2c5865754ed54f4007dce64c0eea14a10095d3d`, develop `5c1ca287ed74b6353423a8c09e253abf3129233a` (Wednesday's ls-remote ~16:0x AEDT, this commission).
- S 17th's READY saved here as `ready_1997.txt` (read it whole).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate182-ks1981-pr1997/`. No dependency install beyond what audit:contract needs (node only).
- NOT TESTED by design: branch protection/rulesets; the pre-push hook's legs 3/4/8 (gateway/spec; untouched by this change). Say so.

## Verdict
Line 1: `GO` / `GO WITH NOTES` / `NO GO (<ids>)` for PR 1997, and the merge tree for the merge seat. Then FOUND / TESTED / HOW with controls.

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
