# Gate 175 commission — Secuura / Blockchain, BATCHED: PR 1990 + PR 1991 (KS-1868), TIER 1, ROUND 1 of 2 each

Written by Wednesday (the 19:1x seat) 2026-11-03 ~22:0x AEDT. Model: Opus (routing v1.0 tier-1 gate row). ONE gate session for two disjoint PRs (Kam 2026-09-18: minimise gate duplication, batch disjoint same-tier PRs). Give each PR its OWN verdict section and its own GO / GO WITH NOTES / NO GO line; one PR's verdict never decides the other's.

## Subjects (re-pin both yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (it does NOT hold the PR objects; fetch them into YOUR clone only, using the checkout's core.sshCommand; never write to the checkout). Read origin by `git -C <checkout> ls-remote origin <ref>`, never `ls-remote <path>`.
- develop at commission: `1cbf260548e7fd534603725f9fc6b05c5cdd9907` (Wednesday's ls-remote, 21:5x AEDT).
- **PR 1990** (KS-1868 "PR 13", Seat R 79th): head `5550a714f5e2962e062af4893d2a3277b30ca110`, one commit on 1cbf2605, 12 files +551/-5, packages/shared: tenant-rate-limiter.ts, tenant-pool-manager.ts, tenant-context.ts, vault/key-vault.ts, db/auto-migrate.ts (+ tests, fragments). READY mail saved whole: `ready_1990.txt` in this folder.
- **PR 1991** (KS-1868 "PR 12", Seat R 79th): head `a44e59c5f9dfcddb4343e41686d90d5134b2d1d6`, one commit on 1cbf2605, 12 files +811/-11, services/shared: security/redis-security-store.ts (rate-limit, brute-force, CSRF stores), cache/cache-middleware.ts, cache/redis-client.ts, cache/connection-pool.ts (+ tests, fragments). O99-P1 (regenerated O96-P6, catch parameter renamed `caught` on purpose) is in it. READY mail: `ready_1991.txt`.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991/`. **Disk: DevMASTER 25 GiB free at writing; stop and report under 18 GiB.** Clone small (sparse `Blockchain/Dev`, `--shared` from the checkout); you may link node_modules from gate 171's or 172's install ONLY if you hash-check the lock blobs equal at your heads (gate 172's verdict shows the method); the gate 148-170 clones have been moved to G-DRIVE and are gone.
- The raise seat ran NO base-against-head recorder (Wednesday's ruling): the measuring is YOURS.

## Questions (answer each with counts; base = 1cbf2605, head = the PR head)
### PR 1990
1. **KEY MATERIAL (decides the weight):** `SecretsManager.getSecret` (key-vault.ts) for a vault error whose `message` read throws: base rejects (the read throws inside the catch); head falls through to the environment fallback and CACHES the env value. `services/auth/src/services/jwt.ts` reads `jwt-private-key` and `jwt-key-id` through it with its own try/catch falling back to env. Build a recorder with the REAL key-vault module and the REAL jwt.ts call path: for {ordinary Error, message-getter-throws, revoked Proxy, null, string, number, ...12 values}, what does getSecret return / throw, what does jwt.ts end up with, is anything cached that would outlive a recovered vault, and is the outcome at head EVER a different key source than at base? Is any outcome at head more permissive than base (a key read where base refused, or a stale cached key served)?
2. Tenant rate limiter: base ends with an exception and no answer for a hostile value; head calls next() (fail-open, as for an ordinary Error). Confirm by driving the real middleware; state base vs head per value class. Is head more permissive than base for any value whose base outcome was "request refused"?
3. TenantPoolManager.refreshConfigs (originate db.ts:280 awaits it), extractTenantContext (503), runMigrations (rollback + stop): base vs head per value class; any caller that now proceeds where base stopped?
### PR 1991
4. **The three security stores (decides the weight):** for each value class, allow or deny at base and head for RedisRateLimitStore.get/increment, RedisBruteForceStore.get/set, RedisCSRFStore.generate/validate, driven with the REAL module over a stand-in redis client that throws each value. The class bar: head is never MORE permissive than base. At base the hostile value made each method THROW (the caller's handling of a throw decides the effective outcome): read each store's callers (the middleware that uses them) and say what the request saw at base (refused? 500? allowed?) vs at head (allowed for rate limit / brute force). If a caller turned a base THROW into a REFUSAL, head's fail-open is MORE permissive: report it as a finding with the caller's line.
5. cacheMiddleware, redis-client connect, ConnectionPool.createConnection/removeConnection: base vs head; O99-P1's `caught` rename changes no behaviour?
### Both
6. Can any path print or log a thrown value's message where base did not (KS-1346/1348 rule: types and field names, never values)? Plant a sentinel in a thrown value and search every log line and response.
7. Red-first: each PR's new cells on base code fail by assertion and pass at head; whole touched-package suites before/after with ratios; mutants on the changed catch lines (raw table, count it; name every survivor, equivalent or not).
8. Merge-tree of each head onto develop (rc and tree) and onto develop-with-the-OTHER-PR-applied (disjoint by path: confirm 0 shared paths, planted control).

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
