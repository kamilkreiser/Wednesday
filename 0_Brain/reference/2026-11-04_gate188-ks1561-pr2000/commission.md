# Gate 188 commission — Secuura / Blockchain, PR 2000 (KS-1561 verify certifies only for the original registrant), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-04 20:31 AEDT. Model: Opus (routing v1.0 tier-1 gate: a verify/certification surface every verifier, including Platform S, reads). Spark shadow: NOT run (Kam 16:42 "ignore the spark until further notice").

## What was ruled, so what this PR must be
- Kam, live board 2026-11-02 12:44:29 AEDT, card secuura-ks1561-duplicate-hash-certifier-1102 = a: "Certify only for the org holding the ORIGINAL registration (agent build; live verify)", detail "Stops the later registrant outranking the original. Some legitimate re-registrations stop showing as certified." Options b (list every registrant, labelled) and c (docs only) were NOT chosen.
- Wednesday, inside that ruling (ANSWERs to Seat F 29th, saved here as f29_definition_question_and_plan.txt for the question; the rulings are restated now): D1 (a) original = the rows tied at MIN(created_at) over the hash's row set; D2 (a) a certification is presented only from an ELIGIBLE row = an original row, OR a KS-1557-trusted lineage row whose parent_document_id is an original, OR a row with the SAME non-null issuer_organization_id as an original, OR the SAME non-null owner_user_id; unknown identity is NOT a match (fail closed); D3 v2 follows the same eligibility, and (ruling A, 08:5xZ) a CERTIFIED non-eligible match is LEFT OUT of v2's matches and count entirely (no field of it presented); uncertified non-original rows stay listed; D4 the registry hash lookup orders by created_at ASC, id. Fixture-only edits accepted on ks584-p3-verify-list.test.ts :195 and :213 (0 changed expect lines). No response field added or removed; no migration.

## Questions (tier 1: measure, do not take the READY's word)
1. **Scope:** `git diff --name-only <merge-base> <head>` = the 6 files in the READY; no services/api-gateway file, no migration, no config.
2. **The ruled outcome, built by YOU, not copied from the seat's cells:** Seat J's case (org B registers H first, row anchored; org A registers H later and certifies its own copy; both org NULL, owners differ). Measure base vs head on /verify (hash path), verify-file, the cross-tenant lookup and v2: base presents "certified by A"; head must present B's row, isCertified false, no certification, and v2 must not list A's certified copy.
3. **Over-blocking (the P side), each base vs head:** original holder certifies its own row; the same owner re-registers and certifies the later row; same non-null issuer_organization_id; a KS-1557-trusted lineage child of the original; rows tied at the earliest created_at; a single certified registrant; two certified holders where the original also certified (head shows the original's, not the newest). Every one must still present a certification on head.
4. **No other path presents an ineligible certification:** enumerate every reader of isCertifiedStatus, buildCertification, siblingCertification and certification_metadata in originate's routes/verification.ts and routes/verificationV2.ts at the head (file:line), and state for each whether eligibility applies or why it cannot present a later certification (the by-id strategy respondExistenceOnly is stated unchanged by the seat: check that claim).
5. **v2 ruling (A):** an ineligible certified match is absent from matches AND from the count; no status/certifiedAt/issuer of it appears anywhere in the response (grep the serialized body for a planted issuer name); matches[0] equals v1's answer on the same data.
6. **Base-vs-head direction:** head is NEVER more permissive than base on any cell you run (a certification presented on head where base presented none = a Major). State the predicate and the ratio.
7. **Fixture edits :195 and :213:** the diff to ks584-p3-verify-list.test.ts touches only fixture lines (owner_user_id), 0 expect lines; each cell still tests what its title says.
8. **Your own mutants (independent of the seat's 17):** at least three, e.g. drop the tie rule, drop the same-owner clause, invert MIN to MAX; each parses, a matching cell goes RED, restored by sha256.
9. **Merge tree** of the head onto develop 17c559555f31 (rc and full tree) for the merge seat.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch the PR ref into YOUR clone only, via the checkout's core.sshCommand; never write to the checkout).
- **PR 2000** head `d03b03046d76591aec3e5a3aa4176fb4e5b78e04`, develop `17c559555f31386fe4ec7a816677a2903db9cd76`; the PR's merge-base is `d92b849ece732cd04e283bfcb0ee9e8bd6989631` (Wednesday's ls-remote 20:31 AEDT).
- F 29th's READY saved here as `ready_f29.txt` (read it whole).
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/`. Dependencies: only from an install matching the lock at the head; do NOT link the shared checkout's node_modules (it is behind the lock).
- DISK: DevMASTER had ~2.6 GiB free at 20:2x AEDT. A `clone --shared` plus one install is fine; STOP and write the verdict as INCOMPLETE if df reads under 2 GiB. No second install.
- Docker is running for other seats: do NOT use, stop or prune any container; you need no Docker. A PostgreSQL 15 keg now exists on this laptop (keg-only, /opt/homebrew/opt/postgresql@15) if you want a real-engine read of the changed SELECTs; any cluster you start lives under your workdir's tmp, unix socket only, stopped by recorded PID.
- NOT TESTED by design: Node 24, kintsugi or demo, the live verify after deploy, real Platform S traffic. Say so.

## Verdict
Line 1: `GO` / `GO WITH NOTES` / `NO GO (<ids>)` / with HOLD-FOR-KAM if section 6's condition holds, for PR 2000, and the merge tree on 17c559555f31 for the merge seat. Then FOUND / TESTED / HOW with controls.

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
