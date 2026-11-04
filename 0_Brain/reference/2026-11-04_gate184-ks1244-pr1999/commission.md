# Gate 184 commission — Secuura / Blockchain, PR 1999 (KS-1244 refuse a repeated x-api-key), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-04 17:40 AEDT. Model: Opus (routing v1.0 tier-1 gate: an authentication path on every route). Spark shadow: NOT run (Kam 16:42 "ignore the spark until further notice").

## What was ruled, so what this PR must be
- Kam, live board 2026-11-04 15:00 AEDT, card secuura-ks1244-repeated-api-key-1104 = a: "Build outright rejection" (a repeated x-api-key must not fall through to anonymous).
- Wednesday, inside that ruling (E 34th's plan confirmation, 04:36:56Z and 04:40:21Z mails): the status is 400; one header line carrying a comma (an empty segment included) counts as repeated; the requirement is that a refused request GAINS NOTHING from CSRF, versioning, audit or the spec gate; two production-mode cells (P1 cookie+no-CSRF-token POST; P2 bearerAuth GET without Bearer) must prove it.

## Questions (tier 1: measure, do not take the READY's word)
1. **Scope:** `git diff --name-only 5c1ca287ed74 <head>` = the 6 files E 34th lists; services/auth/src/routes/users.ts NOT among them.
2. **Refusal reaches every route before any key is used:** enumerate every app.use/route mount in api-gateway's index.ts at the head (read the file, with line numbers). For EACH mount ABOVE the refusal's mount point, say what a repeated-key request gets there and whether that is a gain over a no-key request (the versioning 307 at :515 is one: a repeated-key POST to /api/documents gets a 307 before the refusal; is anything forwarded, validated or logged with the key on that path?). Then drive it: P1 and P2 reproduced in YOUR clone in production mode, with their controls (no key; one valid key).
3. **No key value leaves the process:** read the REPEATED_API_KEY_REFUSED log call; prove with a planted distinctive key value that it appears in no log line, response body or forwarded request (grep the captured output; positive control: the same harness shows the value when you deliberately log it in a mutant copy).
4. **No regression for zero or one key:** api-gateway full suite at the head MERGED onto today's develop 307d9b4c762a (which now carries PR 1998's ks1234-production-mode-307.test.ts): counts, rc. Run the ks1234 file explicitly; it must stay 3/3.
5. **Comma rule cannot refuse a legitimate key:** find where API keys are generated (search the repo for the key format / generator) and state the character set. If a valid key can contain a comma, that is a FIX-BEFORE-MERGE finding.
6. **Red-proof:** reproduce at least M1 (front door unmounted), M2 (inner check dropped), M6 (status 401), M7 (value logged) and M8 (front door above versioning) against the committed bytes; count your own raw table; name any survivor and whether it is equivalent.
7. **Base vs head:** for zero-key, one-key and repeated-key requests on a sample of routes, is any head outcome MORE permissive than base? (Expected: none; repeated-key was the permissive one at base.) That count decides HOLD-FOR-KAM.
8. **Title/body:** title "Refs KS-1244: ..." ≤ 92 chars (count it); no close-word before a key; read the body if you can (G183-F2: the last gate had no gh login; if you cannot, say UNMEASURED).
9. **Merge:** merge-tree of the head onto develop 307d9b4c762a187c85afafc883a7972f7c28ebcd (rc + full tree). E 34th measured 3a89b8cdb6c6 on the PREVIOUS develop ed170905fddc; develop has moved again by PR 1998 (3 added files, none of E 34th's 6). Re-pin at the end.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch the PR ref into YOUR clone only, via the checkout's core.sshCommand; never write to the checkout).
- **PR 1999** head `defe782aaf61222b0eaab414091ef36373e4a046`, develop `307d9b4c762a187c85afafc883a7972f7c28ebcd` (Wednesday's ls-remote 17:40 AEDT).
- E 34th's READY saved here as `ready_1999.txt` (read it whole).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate184-ks1244-pr1999/`. Dependencies: only from an install that matches the lock at the head (zod 4.6.7); the shared checkout's installed tree does NOT match (zod 3.25.76) — do not link from it. DevMASTER has ~9 GiB free: keep your clone and node_modules small, stop and report if free space drops under 2 GiB.
- Docker is running for other seats (s-r84-pg, w23-*): do NOT use, stop or prune any container; you do not need Docker for this gate.
- NOT TESTED by design: Node 24 (the image line), the edge proxy, real clients (Platform S, the WhatsApp bot), any deploy. Say so.

## Verdict
Line 1: `GO` / `GO WITH NOTES` / `NO GO (<ids>)` / with HOLD-FOR-KAM if section 6's condition holds, for PR 1999, and the merge tree on 307d9b4c762a for the merge seat. Then FOUND / TESTED / HOW with controls.

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
