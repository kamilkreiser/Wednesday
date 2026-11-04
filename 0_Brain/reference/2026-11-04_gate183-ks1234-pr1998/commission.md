# Gate 183 commission — Secuura / Blockchain, PR 1998 (KS-1234 production-mode 307 regression test), TIER 2, ROUND 1 of 2

Written by Wednesday 2026-11-04 16:44 AEDT. Model: Sonnet (routing v1.0 tier-2 gate row: tests + docs only, zero product bytes, no deploy surface). Spark shadow: NOT run (Kam 16:42 "ignore the spark until further notice").

## What Kam ruled, and so what this PR must be
Kam, live board 2026-11-04 15:00 AEDT, card secuura-ks1234-production-307-1104 = a: "Build a production-mode regression test". So the PR is a TEST that pins KS-1234's production behaviour (the 307 on POST /api/documents, then the /api/v1 hop reaching originate), red when that behaviour breaks. No product change is expected or allowed.

## Questions
1. **Scope:** `git diff --name-only 5c1ca287ed74..<head>` = exactly the three ADDED files T 10th lists (one api-gateway test, two Projects Documents fragments); 0 product bytes; neither shared Projects Documents page edited.
2. **The test proves what it says (red-proof, in YOUR clone):** reproduce at least M1 (307->302), M3 (production check removed), M5 (rewrite switched off) and M6 (the original KS-1234 parser order restored) from T 10th's table against the committed test bytes, each mutant parsed first and restored byte-equal. Count your own raw table; headline = table. Also reproduce T1 (a NODE_ENV=test boot reads 0/3), which shows the cells really boot in production mode.
3. **Suite:** the api-gateway package suite in your clone, anchored (`--root`), with modest workers: counts and rc. Run it TWICE and report ks1054-startup-migration-failure-on-health.test.ts both times (T 10th's READY "What you should weigh" item 2: it failed 2/2 with an earlier version of the file under load). Say whether the new file plausibly causes it, or whether it is load-only; UNMEASURED is an acceptable answer if you cannot separate them.
4. **Overlap with existing cover:** read ks1461-case-variants-keep-the-gateway-checks.test.ts:171-173. Does cell 1 add anything over it? A note, not a blocker, either way.
5. **Fragments:** `node` docs-fragments.mjs check (from the repo's own scripts) on your clone: OK; and plant one defect in a copy to see it FAIL.
6. **Title/body:** title starts "Refs KS-1234: " and is 92 characters or fewer (count it); no close-word; body quotes the card id.
7. **Merge:** merge-tree of the head onto develop 5c1ca287ed74b6353423a8c09e253abf3129233a (rc + full tree). Re-pin at the end; if develop moved, recompute and name it.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch the PR ref into YOUR clone only, via the checkout's core.sshCommand; never write to the checkout).
- **PR 1998** head `6bbe967acdda4273470abfe08af55b48fb678ff7`, develop `5c1ca287ed74b6353423a8c09e253abf3129233a` (Wednesday's ls-remote 16:44 AEDT, this commission).
- T 10th's READY saved here as `ready_1998.txt` (read it whole).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate183-ks1234-pr1998/`. Dependencies: clone node_modules only if the install matches the lock at the head (zod 4.6.7); the shared checkout's installed tree does NOT (zod 3.25.76, T 10th candidate b), so do not link from it.
- Another seat (E 34th, KS-1244) will soon touch api-gateway's request path; its PR does not exist yet. NOT your subject.
- NOT TESTED by design: the pre-push hook's legs 3/4/8 (need a running stack), Node 24, any deploy. Say so.

## Verdict
Line 1: `GO` / `GO WITH NOTES` / `NO GO (<ids>)` for PR 1998, and the merge tree for the merge seat. Then FOUND / TESTED / HOW with controls.

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
