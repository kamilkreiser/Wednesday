# Gate 188 ROUND 2 commission — Secuura / Blockchain, PR 2000 (KS-1561 verify presents the ORIGINAL registrant's certification), TIER 1, ROUND 2 of 2 (DELTA)

Written by Wednesday 2026-11-04 23:3x AEDT. Model: Opus (routing v1.0 tier-1 gate: what the public verify routes present as certified). Spark shadow: NOT run (Kam 16:42).

## Round 1, in one paragraph
Round 1 verdict (same workdir, `verdict.md`, line 1 "NO GO (G188-F1)") found G188-F1 MAJOR: the "original" (MIN(created_at)) was computed only over the 24 rows fetched by `ORDER BY certified_at DESC LIMIT 24`, so 24 later certified copies pushed the original out and the latecomer was presented again (measured on real PG 15). F2 MINOR (v1 tenant-local vs v2 cross-tenant scope) = filing candidate, not fixed; F3 INFO (seat mocks ignored ORDER/LIMIT); F4 INFO pre-existing. Read round 1's `commission.md` and `verdict.md` whole first.

## Round-2 rulings by Wednesday (what the fix must be)
- The original is computed over the FULL same-hash set, not the fetched frame (G188-F1). Trigger: only when a row-set read returned exactly VERIFY_ROWSET_LIMIT = 24 rows (a possible cut). Dedupe by row id. Tie bound 24 (at most 24 tied originals read; over 24: warn naming KS-1561, first 24 by id). (Seat F 30th's design, confirmed by Wednesday 10:04:05Z.)
- v2 tenant cap (Wednesday ruled option (b), 10:18:24Z): tenants are ranked by MIN(created_at) of their registry rows, then tenant_id, LIMIT 8 (was ORDER BY tenant_id). The stated residual: a tenant whose registry row is written late ranks late (cell CAP-LATE).
- Seat F 30th's READY (saved here as `ready_2000_r2.txt`, read it WHOLE) lists the new commit: 5 files (one new 30-cell test, verification.ts, verificationV2.ts, the two docs fragments).

## Questions (DELTA, tier 1)
1. **Scope of the round-2 commit:** `git diff d03b03046d76 f702d4da4b69 --name-only` = those 5 files; nothing else moved; the round-1 parts that HELD (D1a-D4a, v2 (A), the :195/:213 fixture edits) are byte-unchanged except where the fix had to touch them (name each touched hunk).
2. **G188-F1 on real PostgreSQL 15, re-run YOURSELF:** with YOUR OWN cluster (`/opt/homebrew/opt/postgresql@15/bin/`, data dir + socket under `<workdir>/tmp_r2`, a 127.0.0.1 port or socket only; never /private/tmp/f30t, never another gate's or seat's cluster). Reuse or copy Seat F 30th's harness (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatF-30th/pgcell/`, read-only: COPY into your workdir) or your round-1 harness. The 23 / 24 / 25 later-certified-copies table on all 5 paths (/verify, verify-file, cross-tenant, v2 local, v2 cross) at base d92b849ece73, round-1 d03b03046d76, round-2 f702d4da4b69. Expected: round-2 presents the uncertified original B at all three.
3. **The bounds and their edges:** tie cells at 24 and 25 tied originals (the warn line, first 24 by id); the original certified BEFORE every later copy; an original inside a small set (no extra read: count the queries). Is the extra read only triggered at exactly 24 rows? (A 23-row set must issue 0 extra reads.)
4. **v2 cap ranking:** CAP-8 (control), CAP-9, CAP-10, CAP-LATE on real PG. Then the question that matters for Kam: is ranking by MIN(created_at) ever MORE permissive than base (does it ever present a certification base did not)? And is CAP-LATE's residual worse than base (base presents latecomers there too)?
5. **Base vs head permissiveness over everything you ran:** count cells where round-2 presents a certification base did not (expected 0; the seat measured 0 of 23). Any > 0 = HOLD-FOR-KAM.
6. **Cost:** EXPLAIN on a realistic size (seed at least a few thousand rows for one hash and many hashes; not only 25 rows): does the new MIN(...) subquery use idx_documents_content_hash on a migrated DB (migration 001)? Any full scan on the hot verify path is a finding (grade it).
7. **Mocks honour ORDER/LIMIT now (G188-F3):** read the new test file's mock; confirm M0 (the naive-fixture control) behaves as claimed. Red-first on d03b03046d76: the seat claims 18 of 30 RED by assertion — reproduce.
8. **Mutants:** re-run at least M1 (trigger off), M3 (threshold 25), M5 (tie bound 1), M6 (MIN->MAX), M11 (tenant rank back to tenant_id) against the committed bytes; count your own table.
9. **Title/body:** title unchanged and <= 92 chars, starts "Refs KS-1561:"; the round-2 section in the body states the bound and the CAP-LATE residual (read via the API if you can; else UNMEASURED).
10. **Merge:** merge-tree of f702d4da4b69 onto develop 536642104002f506f61e2e9b6c98a32bf19c3b10 (rc + full tree). Re-pin at start and end.

## Subjects
- PR 2000 head `f702d4da4b69478e82d3d79ea4e8746fae47f2eb` (parent = round-1 head d03b03046d76591aec3e5a3aa4176fb4e5b78e04), develop `536642104002f506f61e2e9b6c98a32bf19c3b10` (Wednesday's ls-remote 23:3x AEDT).
- Read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (your existing round-1 clone under this workdir may be reused: fetch the new PR ref into it).
- Workdir (same as round 1): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/`. Write round 2's verdict as **`verdict_r2.md`** (never overwrite round 1's `verdict.md`); round-2 scratch under `tmp_r2/`, `runs_r2/` (add both to the workdir's .gitignore if absent).
- Live in parallel: gate 190 (another subagent, its own PostgreSQL under `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/tmp`), Seat B 92nd (merge seat, its clone), Seat F 30th (author, idle; its cluster at /private/tmp/f30t is STOPPED, do not start it). Touch none of them. You need no Docker.
- Node: the host's (state it); Node 24 NOT tested.

## Verdict
`verdict_r2.md` line 1 per gate_common section 6, for PR 2000 at f702d4da4b69, and the merge tree on 536642104002 for the merge seat. This is round 2 of 2: a NO GO now is the cap (gate_common section 8) and goes to Kam.

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
