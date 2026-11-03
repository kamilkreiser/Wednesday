# Gate 177 commission — Secuura / Blockchain, PR 1993 (KS-1868 "PR 15"), TIER 1, ROUND 1 of 2

Written by Wednesday (the 22:16 seat) 2026-11-03 ~23:5x AEDT. Model: Opus (routing v1.0 tier-1 gate row: a security surface, the credential verifier). Gauge 92%: usage is a guide (Kam 2026-10-22); a tier-1 gate is a "necessary" Claude use.

## Subject (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (it may NOT hold the PR objects; fetch them into YOUR clone only, using the checkout's core.sshCommand; never write to the checkout). Read origin by `git -C <checkout> ls-remote origin <ref>`, never `ls-remote <path>`.
- develop at commission: `1cbf260548e7fd534603725f9fc6b05c5cdd9907`; **PR 1993** head `8712cb115e0ac48f401865a8549a8847cf39a28c` (Seat R 80th's ls-remote 12:56:07Z, not re-read by Wednesday; re-pin them yourself). One commit on 1cbf2605, 10 files +378/-4: `packages/shared/src/vc/verifier.ts` (verifySignature outer catch), `packages/shared/src/prism/identus-client.ts` (resolveDID), `packages/shared/src/resilience/service-client.ts` (healthCheck), `services/api-gateway/src/routes/health-dashboard.ts` (checkService) (+ tests, fragments). Passes O95-P6, O95-P7, O95-P8, O97-P8 (built and pushed by Seat R 80th from held Spark patches). READY mail saved whole: `ready_1993.txt` — read it first; its FLAG is the seat's reading of the code ("read from source; nothing driven"), NOT a measurement.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993/`. **Disk: DevMASTER ~21 GiB free; stop and report under 18 GiB.** Clone small (sparse `Blockchain/Dev`, `--shared` from the checkout). Gate 176's verdict + harness (`../2026-11-03_gate176-ks1868-pr1992/`) and gate 175's install method are your models; you may link a previous gate's install ONLY if you hash-check the lock blobs equal at your head. This PR also touches `services/api-gateway`: install it from its own lock blob.
- **Load: host load1 is 15-20 tonight** (another seat's mutant run, a G-DRIVE copy). Re-run a timed-out cell alone before calling it a failure, and say you did.
- The raise seat ran NO base-against-head recorder: the measuring is YOURS.

## Questions (answer each with counts; base = 1cbf2605, head = 8712cb115e0a)
1. **THE CREDENTIAL VERIFIER (decides the weight).** Drive the REAL `VerifiableCredentialVerifier.verify()` with the signature check's inner path made to throw each of gate 175/176's 17 value classes (ordinary Error, message getter throws, revoked Proxy, null, undefined, string, number, Object.create(null), {message: Symbol}, {message: BigInt}, {message: revoked Proxy}, {message: object whose toString throws}, Proxy whose get trap throws, thrown Symbol, name getter throws, readable message with throwing toString, plain {message}). Per class at base vs head: does verify() resolve or reject, what are `checks.signature` and `verified`? **The class bar: is any head outcome `verified: true` or `checks.signature: true` where base did not verify?** Also drive a VALID credential and an INVALID-signature credential with no throw, both trees, to show the ordinary verdicts are unchanged. If any head cell verifies what base did not, write HOLD-FOR-KAM.
2. Who calls `verify()` / `VerifiableCredentialVerifier` outside `packages/shared/src/vc/` (the seat says none; `vc/index.ts:10` re-exports it)? Your own grep with a positive and a negative control. If a caller exists, read what it does with a rejection at base vs a `verified: false` at head.
3. `IdentusClient.resolveDID`: base vs head per class; does a hostile value ever yield a non-null didDocument? Callers via `prism/did-manager.ts` (89, 128, 181) and `prism/resolver.ts` (140): does any caller treat `didDocument: null, error: 'notFound'` as anything but not found?
4. `ServiceClient.healthCheck` and api-gateway `checkService` + the `/dashboard` handler (Promise.allSettled, counts fulfilled): base vs head per class; does head ever report a down service as up, or change the overall status?
5. **Sentinel (KS-1346/1348 rule: types and field names, never values):** plant a sentinel in a thrown value; can any path print, log or ANSWER (the dashboard JSON especially) it where base did not? Count both trees.
6. **Red-first and suites:** the PR's new cells on base code fail by assertion and pass at head; whole `packages/shared` and `services/api-gateway` suites before/after with ratios (seat: shared 1447 -> 1459 tests, the same 3 failures; api-gateway 1566 -> 1570, all pass); mutants on the changed catch lines (raw table, count it; name every survivor, equivalent or not).
7. tsc with tests: the seat reports 24/24 (shared) and 25/25 (api-gateway), byte-equal lists; confirm.
8. Merge-tree of the head onto develop (rc and tree; the seat reports 844fb7714826 as its patch-group tree — say what frame that is, or that it does not reproduce, as gate 176 found for PR 1992). Paths shared with PRs 1990, 1991, 1992 (all GO, merging tonight): count them, planted control; the 4-PR group tree in both orders.

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
