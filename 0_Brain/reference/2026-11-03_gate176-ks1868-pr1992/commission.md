# Gate 176 commission — Secuura / Blockchain, PR 1992 (KS-1868 "PR 14"), TIER 1, ROUND 1 of 2

Written by Wednesday (the 22:16 seat) 2026-11-03 ~23:2x AEDT. Model: Opus (routing v1.0 tier-1 gate row: a security surface, the SSRF guard). Gauge 91%: usage is a guide (Kam 2026-10-22), and a tier-1 gate is a "necessary" Claude use (no local tier gates a security surface).

## Subject (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (it may NOT hold the PR objects; fetch them into YOUR clone only, using the checkout's core.sshCommand; never write to the checkout). Read origin by `git -C <checkout> ls-remote origin <ref>`, never `ls-remote <path>`.
- develop at commission: `1cbf260548e7fd534603725f9fc6b05c5cdd9907`; **PR 1992** head `651f25b0d0e23f53eadede35e38c21fa2c31a599` (both Seat R 80th's ls-remote 12:19:16Z, not re-read by Wednesday; re-pin them yourself). One commit on 1cbf2605, 9 files +384/-4, packages/shared: `security/ssrf-guard.ts`, `security/secrets-manager.ts`, `blockchain/event-indexer.ts` (+ tests, fragments). Passes O96-P7, O96-P8, O97-P6, O97-P9 (built by Seat R 79th, pushed by Seat R 80th). READY mail saved whole: `ready_1992.txt` in this folder — read it first; its FLAG section is the seat's reading of the code, NOT a measurement (it says "read from source; nothing driven").
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992/`. **Disk: DevMASTER ~21 GiB free; stop and report under 18 GiB.** Clone small (sparse `Blockchain/Dev`, `--shared` from the checkout). Gate 175's install method (verdict.md "Install" in `../2026-11-03_gate175-ks1868-pr1990-pr1991/`: `npm ci --ignore-scripts` per package from its own lock blobs, vitest pinned to develop's root lock in an ignored `scratch/vt`) is the model; you may link gate 175's install ONLY if you hash-check the lock blobs equal at your head.
- **Load: host load1 is 15-20 tonight** (another seat's 84-mutant run, a G-DRIVE copy). Timeouts are the host, not the code: re-run a timed-out cell alone before calling it a failure, and say you did.
- The raise seat ran NO base-against-head recorder (Wednesday's ruling): the measuring is YOURS.

## Questions (answer each with counts; base = 1cbf2605, head = 651f25b0d0e2)
1. **THE SSRF GUARD (decides the weight).** Drive the REAL `ssrf-guard.ts` with a stand-in resolver (dns lookup) and a stand-in request layer, both throwing each of the value classes gate 175 used (17: ordinary Error, message getter throws, revoked Proxy, null, undefined, string, number, Object.create(null), {message: Symbol}, {message: BigInt}, {message: revoked Proxy}, {message: object whose toString throws}, Proxy whose get trap throws, thrown Symbol, name getter throws, readable message with throwing toString, plain {message}). For `resolvePublicAddresses`, `assertResolvedHostPublic` and `safeOutboundRequest`: base vs head outcome per class. **The class bar: is any head outcome an ALLOWED address or a SENT request where base-ordinary refused or sent nothing?** Also drive hostile addresses (private, loopback, link-local, IPv4-mapped IPv6, DNS returning a mix of public and private) with ordinary errors, so the guard's own refusals are shown unchanged by this PR. If any head cell allows what base refused, write HOLD-FOR-KAM.
2. **The four non-test callers** the seat names (`services/m365-integration/src/index.ts` 1286, 1495; `services/originate/src/routes/webhooks.ts` 172, 459): read them at head (and drive `dispatchEvent`'s loop at webhooks.ts ~527-552 if you can with stand-ins). Does head change what a caller does with a refused or failed result? Is the seat's caller census complete (your own `git grep`, with a positive and a negative control)?
3. **security/secrets-manager.ts `getSecret`** (vault catch -> environment fallback): base vs head per class, with `useEnvironment` on and off. Does head ever return a secret where base refused? Confirm or refute the seat's "no non-test importer of this class" by your own grep.
4. **EventIndexer.handleError**: base vs head per class through the five catch sites (133, 210, 232, 321, 329) and its `onError`; does head ever swallow what base propagated in a way that skips a block, or retries forever?
5. **Sentinel (KS-1346/1348 rule: types and field names, never values):** plant a sentinel in a thrown value; can any path print, log or answer it where base did not? Count both trees.
6. **Red-first and suites:** the PR's new cells on base code fail by assertion and pass at head; whole `packages/shared` suite before and after with ratios (the seat reports 1447 -> 1463 tests, the same 3 failures: KS-879 walk, threadToken, CIP-8 = KS-1727); mutants on the changed catch lines (raw table, count it; name every survivor, equivalent or not).
7. **tsc with tests:** the seat reports 24 -> 25 errors, the extra a TS1378 top-level await in a new test file. Confirm, and say whether it matters for any runner the repo uses.
8. Merge-tree of the head onto develop (rc and tree; the seat reports group tree `0a2814d535d7`). Paths shared with the two PRs merging tonight (1990: packages/shared tenant-rate-limiter / tenant-pool-manager / tenant-context / vault/key-vault / db/auto-migrate; 1991: services/shared): count them, with a planted control.

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
