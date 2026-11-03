# Gate 171 commission — Secuura / Blockchain, PR 1987 (KS-1967), TIER 1, ROUND 1

Commissioned by Wednesday (17:1x AEDT 2026-11-03). Model: Opus (routing v1.0, tier-1 gate row; gauge 7d ~82%, the 80-90% band: a gate is an allowed cloud launch).

## Subject (from Seat F 27th's READY FOR GATE, 06:10:06Z — re-pin it yourself, section 4)
- Repo: Secuura/Distributed_Secuura (github). Read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`.
- PR 1987, branch `fix/ks-1967-lockout-fail-closed`, head `f1641944de444e0a6f402cce8d897fde0b3cc4e5` (one commit), develop `de8d208a8426747b3a752309e08167fa0de4b2ff`.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate171-ks1967-pr1987/` (this file is in it; leave it).
- **Disk: DevMASTER has ~19 GiB free (99% full).** Keep the clone small: `clone --shared`, and link node_modules from an install whose root lockfile is byte-identical to head's (gate 170 found the read-only checkout's lockfile differs from current heads and used gate 148's install instead; check, do not assume). If free space falls under 15 GiB, stop and report.

## What the PR claims (the builder's READY, read whole by Wednesday)
Product change: `Blockchain/Dev/services/auth/src/services/accountLockout.ts` only. While the session store has no client, or a read or write throws: `isLockedOut` and `recordFailure` throw ServiceUnavailableError (503, its existing text) instead of answering "not locked" / returning 0; `recordSuccess` stays non-fatal; all three catches log the thrown value's TYPE only. Every password door runs the check before any user lookup or password verification: /login (users and platform admins), wallet/verify and the social callback answer 503; /oauth/authorize answers its existing catch-all 500 (Wednesday's ruling D1: uniform, no new client text). With the store up, nothing changes. Builder's evidence: 26/46 new cells red on develop by assertion, 46/46 at head; a 68-cell base-vs-head recorder with 0 head cells more permissive and 0 store-down right/wrong differences at head (12 at base); 11/11 mutants killed; auth suite 1669/1669 at head; five existing test doubles completed with additions only. Builder's NOT done: no real Redis outage on a booted service; four platform suites not run; wallet and social driven through the credential gate, not at route level; one replica; KS-1965 (store down at boot) not covered; pre-push legs 3, 4, 8 skipped. These are CLAIMS: re-measure, do not quote.

## Ruling context (Kam's card secuura-auth-lockout-failopen-redis-down-1103 = a, 15:53:05: "Fail closed: refuse logins while the session store is down")
The class bar (gate_common section 5) applies with the store DOWN: no login outcome at head more permissive than base, and a right and a wrong password answer IDENTICALLY. With the store UP: head byte-equal to base for every door.

## Your questions
1. With the session store unavailable in every way you can produce (null client, every command throws, writes only throw, a reader that rejects after maxRetriesPerRequest, and slow as a control), is any login outcome at ANY door more permissive than base? Count cells.
2. Do a right and a wrong password ever answer differently while the store is down, at any door (status, body, headers, timing class, side effects such as an authorization code INSERT or a session row)?
3. Does any thrown text (plant a sentinel in the error message) reach a log line or a client body?
4. **Door census:** enumerate EVERY caller of isLockedOut / recordFailure / recordSuccess across the whole repo (not only services/auth) with a positive control, and say whether the builder drove each. A caller the builder did not drive is a finding.
5. With the store UP: are all doors byte-equal to base (status, body, the recordFailure / recordSuccess counts)?
6. Red-first: do the new cells fail at develop by assertion? Run the auth suite at head (twice). Run mutants, count the raw table, and name survivors.
7. The five completed test doubles: confirm additions only and that no assertion changed (diff them).

## Not yours
No booted stack, no real Redis daemon required (a stand-in that throws or returns null is fine; say which), no platform suites. Do not test the HIBP work (KS-1968): it is not in this PR.

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

