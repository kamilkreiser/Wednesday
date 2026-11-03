# Gate 174 commission — Secuura / Blockchain, PR 1989 (KS-915 rebuild of restore-local-secrets.sh), TIER 1, ROUND 2 OF 2 (THE CAP)

Written by Wednesday (the 22:16 seat) 2026-11-04 ~00:3x AEDT. Model: Opus (tier-1 gate row: a secrets-writing script that must never write while any reader resolves a non-local database). Gauge 92%: usage is a guide (Kam 2026-10-22); a tier-1 gate is a necessary Claude use.

**THIS IS ROUND 2 OF 2 under Kam's rebuild card (`secuura-pr1982-restore-script-round2-nogo-1103` = a, "Rebuild the check using the real tools' reading", 15:52) and the two-NO-GO cap (learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md).** If you write NO GO, Wednesday ships the closed instances and tickets the residue; there is no round 3 without Kam. So: **be exact about which findings are FIX-BEFORE-MERGE (a write while a non-local database resolves, a printed or committed generated value, a reader that cannot run failing OPEN) versus follow-ups.** Do not hold for anything that is a known, stated limit in the PR body unless you measure it to be worse than stated.

## Subject (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch into YOUR clone only, using the checkout's core.sshCommand; read origin by `git -C <checkout> ls-remote origin <ref>`).
- develop `1cbf260548e7fd534603725f9fc6b05c5cdd9907`; **PR 1989** head `c71a6d106696706309efbd4ece7952fc5dacbd2c` (Seat E 32nd's ls-remote 13:2xZ; re-pin). History: ea41c34668dd (round 1, gated by gate 173) -> 30a85b970 (merge of develop, tree 1ae2502f9c50 = gate 173's end tree) -> c71a6d106696 (the fix). Three-dot vs develop = the four PR files. PR 1982 (87c9e7488fd7) must stay untouched.
- **Gate 173's verdict, harness and results are your baseline:** `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989/` (verdict.md, harness/, results/q6.txt n01-n05, results/q7b_survivors.txt, results/q2345.txt, results/q1_pgbouncer_render.txt, results/mutants_applied.txt, harness/classify.js). READ verdict.md WHOLE FIRST, then `ready_1989_r2.txt` here (the seat's READY, whole).
- **What was asked of this round** (Wednesday's 09:18Z ANSWER as carried in Seat E 32nd's brief, plus Wednesday's 11:30Z plan-confirmation ANSWER, both in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/`: `2026-11-03_seatE32_ks915_fixround_gate173.md` ITEM 1, and `2026-11-03_answer_E32_plan_confirmation.md`): G173-F1 (every database-address variable compose passes, in both entries, judged by every reader; POSTGRES_HOST/PORT/DB added to judge(), the bash printf, the canonical-line and canonical_shell lists; POSTGRES_DB as a plain identifier); G173-F5 (kill m06, m11, m12, m13, m16; m36 if cheap); G173-F4 (report truthfully or refuse; the seat chose report); G173-F3's one-line `history` fix; G173-F2 and the looping-.env hang stay NAMED LIMITS. Wednesday's CONDITION: credentials (APP_DB_USER/PASSWORD, POSTGRES_USER/PASSWORD) are judged only through the composed URLs, so that route has ONE guard (the compose reader); the script must REFUSE when that reader cannot run.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/`. **Disk: DevMASTER ~22 GiB; stop under 18 GiB.** Use THROWAWAY values only: never a real credential; gate 173 printed a 40-char prefix of a scratch password to its session output — do not print any generated or scratch secret value, even a prefix.
- **Load: host load1 ~8-15 tonight.** Re-run a timed-out cell alone before calling it a failure.

## Questions (counts; round-1 head = ea41c34668dd, round-2 head = c71a6d106696)
1. **G173-F1 CLOSED?** Re-run gate 173's n01-n05 and gate 166's 28 forms at c71a6d106696 with the real compose (both entries) and dotenv: refused / accepted, .env byte-identical, rc. Then forms NEITHER gate nor the seat tried, at least: POSTGRES_HOST with a trailing dot or IPv6 literal or `postgres.<remote>`; POSTGRES_PORT with a leading zero, `+`, whitespace, or 65536+; POSTGRES_DB with unicode or a length extreme; the remote host in `.env` AND in the shell at once with different values; an `override` / extra `-f` file, `COMPOSE_FILE`, `--env-file` (the seat lists these as NOT covered: measure whether they are a real write path or genuinely out of scope). **Any form where the script WRITES while compose or dotenv resolves a non-local database = FIX-BEFORE-MERGE.**
2. **Wednesday's condition:** drive the credential route (a hostaddr/service/host change through APP_DB_PASSWORD and each of the other three credential keys) with the compose reader WORKING (refused?) and with it BROKEN in every way you can make it fail (docker absent, `compose config` rc != 0, rc 0 with garbage or truncated JSON, a hang): does the script refuse every time, .env byte-identical? **A broken-reader path that proceeds = FIX-BEFORE-MERGE.**
3. **The census pin cell:** does it fail when compose passes a NEW address-shaped key nobody judged (plant one)? Is its reviewed list equal to what YOUR `docker compose config --format json` gives, both entries?
4. **G173-F5:** confirm m06, m11, m12, m13, m16, m36 are killed by re-applying them yourself. Then the 19 survivors: re-classify each (equivalent by reading / layered-equivalent driven / reachable and permissive). **A reachable permissive survivor is a finding.**
5. **G173-F4 (report truthfully):** cells ra0-ra3: does the note print exactly when auth under the root entry would not get the written values, and never otherwise? Exit unchanged?
6. **G173-F3 line:** `enable -n history kill; HISTFILE=/dev/null` before `set -r`: does it close the `history -w` escape on bash 3.2.57? Any other builtin escape left in restricted mode (`fc`, `command`, `builtin`, `exec`)?
7. **Leaks:** across every cell you run, 0 generated or scratch secret values (48-hex or any length) in stdout, stderr, logs, the repo, or git objects; the output file gitignored; a second run byte-identical.
8. **Suites + red-first:** the PR suite 331/331 at head and the seat's red-first figures (29/331 at round-1 head, 292/331 with the script absent); shell suites before/after.

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
