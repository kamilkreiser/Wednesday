# Gate 191 commission — Secuura / Blockchain, PR 2003 (KS-1958: a revoked credential verifies as valid when the credential store read fails), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 07:0x AEDT. Model: Opus (routing v1.0 tier-1 gate: a credential-revocation / verify path). Spark shadow: NOT run (Kam 2026-11-04 16:42 "ignore the spark until further notice").

## What was ruled, so what this PR must be
- The defect (gate 152 G152-F1, `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968/verdict.md` lines 29-38 and 68; ticket KS-1958): in vc-issuer, when this process's memory copy is stale-unrevoked and the DB READ throws, `getById` falls back to memory and the verifier returns verified TRUE for a revoked credential.
- Authority: Wednesday's reading of Kam's fail-closed rulings (cards secuura-auth-lockout-failopen-redis-down-1103 = a, secuura-pr1970-gateway-failopen-1103 = a), reported to Kam on morning card wed-morning-fleet-activity-1105. Gate 152 had said "needs Kam's ruling"; the PR body states that conflict and the availability cost. If you find the fail-closed choice has a consequence the PR body does NOT state (anything beyond "verify reads false while the DB read fails"), that is HOLD-FOR-KAM.
- Accepted design (Wednesday's ANSWER to the seat, 19:32Z): `getById(id, {failClosedOnReadError})`; with the option, DB available and the read THROWS -> a NEW CredentialStoreReadError with a FIXED message (no DB text reaches a public response); without it, unchanged. Only `revocationResolvers.ts:55` passes it; `revoke()` keeps the old read. Boundary 1 (no DB: memory only) unchanged. Boundary 2 (DB healthy, zero rows, then memory) deliberately OUT of scope (the seat measured 0 DELETE/TRUNCATE on vc_credentials_store at the base). The five 'unreadable thrown value' guards must stay byte-equal.

## Questions (tier 1: measure, do not take the READY's word)
1. **Scope:** `git diff --name-only <merge-base> <head>` = the 5 files in the READY; name any other.
2. **Base vs head, the full matrix:** gate 152's scenarios A, B, B-control, C, D x the three thrown shapes (ordinary Error, revoked Proxy, getter-throws message) x both routes that wire revocationVerifierConfig (credentials, presentations). Predicate: any head cell verified TRUE where base was FALSE = a Major. Count it yourself ("N of M"); do not reuse the seat's table.
3. **Leak:** the verify response at head for a failed read: does any DB error text, stack or driver message appear anywhere in the serialized body or headers? Planted distinctive DB error message + a positive control that shows your search finds it in a log or in base's behaviour.
4. **revoke() and the siblings unchanged:** prove `revoke()` with a failing SELECT behaves exactly as at base, and getRecordById / getByHash / getReadableByHash unchanged (diff + one cell each).
5. **Boundary 2 reasoning:** re-measure "0 DELETE/TRUNCATE on vc_credentials_store" at the head (git grep with a positive control); state whether ANY code path can leave a row missing while memory holds it (store()'s failed INSERT is the seat's named case). If you find one, say whether it reopens the fail-open; that is a finding, not a block, unless it is the SAME exploit shape.
6. **Availability cost, measured:** with the DB read failing, an UNREVOKED credential: head verified false (the stated cost). Anything else changed (latency, retries, an exception escaping a route as 500)? An uncaught throw becoming a 500 is a finding.
7. **Red-proof:** reproduce at least 3 of the seat's 4 mutants against the committed bytes (m1 mandatory), plus ONE of your own; name survivors.
8. **Suites:** whole vc-issuer workspace at head (the seat: 758 of 758), tsc incl. tests, eslint on the touched files, docs-fragments check with a planted defect.
9. **Title/body:** title starts "Refs KS-1958:" and is <= 92 chars (count); no close-word before a key; the body carries the authority line, the CONFLICT and the availability cost (read the body via the API).
10. **Merge:** merge-tree of the head onto develop 035685291b9d58ae6ea8ba5f05adf9379f9c2944 (rc + full tree id) for the merge seat.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch the PR ref into YOUR clone only; never write to the checkout).
- **PR 2003** head `8b140178276457116714892fe0cf73b9f1e92c8c`, develop `035685291b9d58ae6ea8ba5f05adf9379f9c2944` (Wednesday's ls-remote 07:0x AEDT, 20:0xZ).
- F 31st's READY saved here as `ready_2003_batch.txt` (the second mail in that file; read it whole). The seat's record: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-05_seatF-31st/`.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate191-ks1958-pr2003/`. Dependencies only from an install matching the lock at the head; never link from the shared checkout's node_modules. DevMASTER ~135 GiB free.
- Live seats: D 52nd (demo deploy, box only), F 31st (wrapping; its PR-B worktree s-f31-ks1986 is NOT yours). Do not touch their worktrees, processes, ports or clusters. No contact with demo or kintsugi.
- NOT TESTED by design unless you do it: Node 24, a real deploy, a real second replica. Say so.

## Verdict
Line 1 per gate_common section 6, for PR 2003, and the merge tree on 035685291b9d for the merge seat. Then FOUND / TESTED / HOW with controls.

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
