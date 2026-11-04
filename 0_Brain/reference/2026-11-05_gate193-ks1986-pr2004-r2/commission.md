# Gate 193 commission — Secuura / Blockchain, PR 2004 (KS-1986: verify v1 judges the original registration across tenants; ROUND 2 fix for G192-F2), TIER 1, ROUND 2 of 2

Written by Wednesday 2026-11-05 08:xx AEDT. Model: Opus.
**TIER 1, reason:** a public verify path's certification and tenant-disclosure behaviour (routing v1.0 tier-1 gate); this round re-gates the exposure finding G192-F2 on that same path.
**Round count:** round 2 of 2 under the cap (gate 192 was round 1 and ended GO WITH NOTES — HOLD-FOR-KAM, not a NO GO; the two-NO-GO cap per gate_common section 8 is not yet reached, but this is the last round the cap allows).
**A rotation KILLS it:** you run as a subagent of Wednesday's seat; if that seat rotates while you run, you are killed mid-run. Write `verdict.md` EARLY as a stub (line 1 `NO GO (INCOMPLETE: killed before finish)`), then rewrite it as each question closes, so a kill leaves a truthful partial file rather than none. Stop every background process (postmaster included) before each rewrite you expect to be your last.
**Gate-specific part overrides gate_common section 8's "delta only" default:** question 3 asks for the FULL gate-192 matrix again.

## What this round is, so what the PR must be
- Authority: Kam's card (RULED a at 09:05:06, see the next line) `secuura-pr2004-ks1986-gate192-hold-1105` (read `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-pr2004-ks1986-gate192-hold-1105`, READ verb only, read 2026-11-05). Its DEFAULT (card text): "Wednesday commissions the narrow fix round for (2) and its re-gate (reversible, no merge), and files (1) as a ticket; the merge waits for your tap." Option (a): "when the cross-tenant read fails, v1 shows 'not certified' instead of falling back to the chain."
- **Kam RULED card 1105 = a** (live board 2026-11-05 09:05:06 AEDT, verbatim: "Decision secuura-pr2004-ks1986-gate192-hold-1105: a — Fix (2) first, ticket (1)"; option a's detail: "... Then re-gate and merge ..."). So a clean verdict from you leads to the merge on Wednesday's head-pinned GO, without another tap from Kam. A HOLD-FOR-KAM in your verdict still goes back to him.
- Round-1 record (read 2026-11-05): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/verdict.md`. G192-F1 (original's tenant absent from the registry set or past the 8 cap: v1 shows another tenant's later certification; v2 already does) is NOT fixed by this round; the card's default tickets it. G192-F2 (cross-tenant read failure with every local row certified: v1 falls to the chain fallback, presenting the chain's certification with issuer org UUID and issuer name; canary hit 2 of 2 v1 paths) is what this round fixes.
- **The round's claim (Seat F 33rd, relayed by Wednesday; you VERIFY, you do not trust):** a boolean `crossTenantReadFailed` is set true ONLY on `judgeAcrossTenants`' read-failure return (line ~677 at 577f668f4786); the chain-fallback guard in BOTH v1 callers (verify-file ~943, `/verify` ~1412) becomes `rows.length === 0 && !crossTenantReadFailed`; the existing not-found body is REUSED UNCHANGED; line 682 (`originals.length === 0` on a SUCCESSFUL read) is NOT changed and is claimed unreachable (the seat probes it). Line numbers are the seat's/Wednesday's, from gate 192's head; re-read them at `4432db224a5867fdb6afaabf56df08cdf640d067`.
- **Seat's figures to RE-MEASURE (not trust):** red 4 of 34; unit 95 of 95; PG15 HEAD(577f)->FIXED: NEW 0 of 60, DIFFERENT 0 of 60, LESS 6 of 60 (claimed to be exactly the chain-fallback rows); BASE->FIXED: NEW 0 of 60, DIFFERENT 8 of 60; v2 equal 18 of 18; canaries 0 of 54 with a control.

## Questions (tier 1: measure, do not take the READY's word)
1. **Scope of the delta.** `git diff --name-only 577f668f478679a3e4965a28fba6b96a9e2212d6 4432db224a5867fdb6afaabf56df08cdf640d067` must be exactly: `verification.ts`, the KS-1986 test file, the KS-1986 FLOW fragment. The CHEAT fragment must be UNTOUCHED (Wednesday's ruling; note G192-F5's stale "Not measured here" line lives in CHEAT and so stays stale, by ruling: do not raise it as a defect, state it as a one-line note). Also: `4432db224a5867fdb6afaabf56df08cdf640d067` = 4432db224a5867fdb6afaabf56df08cdf640d067 with parent 577f668f478679a3e4965a28fba6b96a9e2212d6 (1 commit on top, no merge commit); numstat of the delta by file; the changed lines of verification.ts quoted in the verdict (the new flag's declaration, its single set site, both guards). Name any other path or hunk. Also confirm gate 192's original scope facts still hold on the full range `035685291b9d..4432db224a5867fdb6afaabf56df08cdf640d067` (5 files, the 2/2 existing-test change untouched), 0 api-gateway files, no migration, `verificationV2.ts` untouched.
2. **G192-F2 closed.** Copy gate 192's PG harness (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/pgcell/g192-pg15.harness.test.ts` and `tools/compare.py`, `tools/mutants.py`; COPY into YOUR workdir, never run in gate 192's workdir) and re-run, on YOUR OWN real PostgreSQL 15 cluster (keg `/opt/homebrew/opt/postgresql@15`; socket only, `listen_addresses` empty; use a socket dir and port DIFFERENT from gate 192's `/private/tmp/g192/s` / 55492, e.g. `/private/tmp/g193/s` / 55493; record the postmaster pid and stop it), the cells `G-CHAIN-UP-REGISTRY-DOWN` and `G-TENANT-POOL-THROWS-ALL-CERTIFIED` on BOTH v1 paths at base, at 577f, and at `4432db224a5867fdb6afaabf56df08cdf640d067`. Required at `4432db224a5867fdb6afaabf56df08cdf640d067`: chain calls **0** (instrument: the global-`fetch` stub's call counter, as gate 192); no planted issuer UUID and no planted issuer name anywhere in the whole serialized body or ANY header; the response body is the existing not-found body. **Control that can fail:** the same cell at 577f must still show chain calls 1 and the planted values in body (the instrument fires), and `G-CONTROL-NO-LOCAL-CHAIN-UP` must still show the planted values at head (see 3). Also cover the other read-failure forms the new flag claims to catch: registry DB missing, one tenant DB missing, `getPool` throwing for a tenant, each with local rows, with the chain both up and down: name each form and whether it reaches the flag's single set site (read the code, then drive it).
3. **Nothing else moved.** The full gate-192 matrix (27 cells x 2 v1 paths = 54 rows plus the v2 cells, 66 PG rows in gate 192's mutant table) at base `035685291b9d`, at 577f, and at `4432db224a5867fdb6afaabf56df08cdf640d067`; run `compare.py` for each pair. Predicates, counted by YOU as "N of M": (a) NEW (head presents a certification where the comparison base presented none): must be 0. (b) DIFFERENT, 577f->`4432db224a5867fdb6afaabf56df08cdf640d067`: expected 0 (the seat's claim); BASE->`4432db224a5867fdb6afaabf56df08cdf640d067`: the seat says 8 of 60; name each of the 8 and say whether it is the original holder's own, or G192-F1's latecomer (gate 192 counted 10 DIFFERENT over 54 rows: 4 original holder's, 4 latecomer's/G192-F1, 2 chain/G192-F2; expected now: the 2 chain rows turn LESS, leaving 8, and the seat's "60" vs gate 192's "54" row count must be reconciled: say which cells the 6 extra rows are). (c) LESS 577f->`4432db224a5867fdb6afaabf56df08cdf640d067`: the seat says 6 of 60 and that they are exactly the chain-fallback rows; check each is a chain-fallback row (not some other row that went LESS). (d) v2 equal across all three: expect 18 of 18 (v2 is untouched). (e) `G-CONTROL-NO-LOCAL-CHAIN-UP` (no rows anywhere, registry up) still presents the chain answer, with its planted issuer values, at base AND 577f AND head: this is the PRE-EXISTING chain-branch exposure (G192-F2's control) and must be UNCHANGED, not "fixed"; if head hides it there, the guard is wider than claimed: that is a finding. (f) The disclosure search (planted foreign title, org name, owner id, issuer UUID, issuer name; whole body and headers) over all D-B2 cells: 0 hits in DB-sourced rows as in gate 192, with gate 192's controls (`G-CONTROL-LOCAL-CANARY`, mutant that drops the scrub) still firing.
4. **Line 682 reachability** (`originals.length === 0` on a successful read, claimed unreachable). (a) Read the code that reaches it at `4432db224a5867fdb6afaabf56df08cdf640d067` and say which input would be required (a registry row for a tenant whose originals read succeeds with zero rows while the caller holds a local row). (b) YOUR OWN attempt to construct it at PG15: a registry row pointing at a tenant that holds no document for the hash; a registry row whose tenant row was deleted after registry write; a hash form mismatch (`sha256:` prefix vs bare, per G192-F4); a tenant whose rows are all revoked or filtered by the originals query. Report each attempt and its outcome (reached / not reached), driven, not argued. (c) The seat's probe evidence (read the seat's record, path from `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/ready_2004_r2.txt`): what it ran and what it showed. If you reach line 682 with a local certified row and the chain up and the chain fallback then runs, that is a Major (G192-F2 reopened through the other door); if reaching it only yields the not-found body, state it as reachable-and-harmless. If you cannot reach it, say what you tried, and write "unreachable" ONLY if the code makes it so; otherwise "not reached by N attempts".
5. **Mutants on the new flag and guard** (run on the committed bytes; each anchor count 1; restore and check the blob equals `4432db224a5867fdb6afaabf56df08cdf640d067`'s; then count the RAW table yourself): (m1) flag never set; (m2) flag set but guard reverts to `rows.length === 0` in the verify-file caller only; (m3) same in the `/verify` caller only; (m4) flag set on every `judgeAcrossTenants` return, not just read failure (this must kill: a successful read with no original would then skip the chain); (m5) flag set on the registry-read failure form only (the tenant-pool-throws form unflagged) and the reverse; (m6) guard inverted (`|| crossTenantReadFailed`); (m7) the not-found body altered (a different message). Mark each KILLED or SURVIVED with the cell that killed it; for every survivor judge equivalence in writing (try to build an input that separates it; say what you tried).
6. **G192-F1 ticket.** The seat filed it. READ the board ticket (read only; the gate holds no Linear write and posts nothing): confirm it exists, carries facts only (G192-F1's cells `G-ORIGINAL-UNREGISTERED`, `G-CAP-9-SKEWED`, v1 and v2 both, reachability marked "read, not measured"), names no ruling, and does not claim a fix. Take the id and URL from `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/ready_2004_r2.txt`. If the READY gives none or the board cannot be read from your seat, write UNMEASURED and name the instrument that closes it (a Wednesday-side `linear_*` read).
7. **PR body.** Read the PR title and body live if you hold a read identity; otherwise from the seat's read-back files named in `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/ready_2004_r2.txt` (and say which). Confirm: lines 1-2 UNCHANGED from round 1 (line 1 = Kam's release line, card wed-morning-fleet-activity-1105 = a, 07:07:25 AEDT; line 2 = the supersede of the commit body's "HOLD: do not merge ..." line); a line "For Kam (card secuura-pr2004-ks1986-gate192-hold-1105)" naming that the not-found body is REUSED unchanged (quote the line); G192-F4 and G192-F5 appear as notes only (not as claims of a fix); title still `Refs KS-1986:` and <= 92 chars (count); 0 close words before a key. Anything in the body that promises more than the delta does is a finding.
8. **Merge tree.** In YOUR clone, `git merge-tree --write-tree e899463d2a0b1b30f2cff46b23d001622620029a 4432db224a5867fdb6afaabf56df08cdf640d067` (re-read develop with `git ls-remote` at start and end; the value here is Wednesday's 08:1x AEDT 2026-11-05 read): rc, full tree id; shared paths with `035685291b9d..<develop>` (with a planted control, as gate 192); per-path blob of the PR's 5 files in the merge tree vs the head blob.
9. **Suites and static checks, at `4432db224a5867fdb6afaabf56df08cdf640d067`:** the three KS-1986 unit files (seat: 95 of 95) and the whole originate suite (gate 192 at 577f: 2,475 of 2,475 tests, 210 of 210 suites; expect more tests now: report both numbers and the difference); `tsc --noEmit -p services/originate` and tsc over verification.ts + the test files with jest types (planted control must fail); eslint on the touched files (planted control); `docs-fragments.mjs check` clean plus a planted dangling `<!--ref:...-->` that must give rc 1. **Red proof:** the seat's NEW/changed tests against 577f product bytes: report red N of M, every red by assertion (0 TypeError, 0 `error TS`); the seat says 4 of 34.

## HOLD-FOR-KAM rule (this gate)
Beyond gate_common section 6: ANY change to what a user reads other than the reused not-found body, and ANY unstated consequence of the guard (a case where a user who got a certification at 577f or base now gets something else, other than the chain-fallback cells), is written HOLD-FOR-KAM. State the condition and evidence; Wednesday rules. Also write HOLD-FOR-KAM if the not-found body is not byte-equal to the existing branch's body in both callers.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch the PR ref into YOUR clone only; never write to the checkout).
- **PR 2004** head `4432db224a5867fdb6afaabf56df08cdf640d067` (`4432db224a58`), claimed = `4432db224a5867fdb6afaabf56df08cdf640d067`; parent (round-1 head) `577f668f478679a3e4965a28fba6b96a9e2212d6`; built base `035685291b9d58ae6ea8ba5f05adf9379f9c2944`. Develop `e899463d2a0b1b30f2cff46b23d001622620029a` (Wednesday's ls-remote 08:1x AEDT 2026-11-05; the gate re-reads it). If the head you read is not the claimed one, say so first and stop.
- The seat's READY: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/ready_2004_r2.txt` (read whole). Gate 192's workdir `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/` is READ-ONLY to you (harness and runs to copy and compare against; its `runs/pg_base2.jsonl` and `runs/pg_head2.jsonl` are the round-1 numbers). Seat F's earlier records under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-05_seatF-32nd/` and the 33rd's folder named in the READY may be read.
- **Workdir:** `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/` = `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/`. (gate_common section 2's naming pattern is `<date>_gate<N>-<ticket>-pr<n>`; this folder carries a `-r2` suffix, as Wednesday created it. Use it as given.) Dependencies only from an install matching the lock at the head (`npm ci --ignore-scripts` in your clone, then `npm run build -w @secuura/shared`); never link from the shared checkout's node_modules.
- Live seats (Wednesday's `tmux list-panes` 08:2x AEDT): D 52nd (demo deploy, box only), K 14th (KS-1959, a different PR), F 33rd (PR owner). B 93rd has WRAPPED. A gate 194 (KS-1959) may run in parallel in its own workdir: not yours. Do not touch their worktrees, processes, ports or clusters. No contact with demo or kintsugi.
- Never post: the gate does not push, merge, comment on the PR or any ticket, send mail, or write to any board; it only READS the PR, the card and the ticket. (gate_common section 1 is exact: findings only, one verdict file.)

## NOT TESTED by design unless you do it (say so in the verdict)
Node 24 (gate 192 ran on Node v26.8.1; say what you ran). A real deploy, demo, kintsugi, real Platform S traffic, the real anchoring service (the chain is a global-fetch stub), production data volume. G192-F1 (not fixed here) and how many production hashes it reaches. The real tenant manager / RLS. Lineage walks, `/verify`'s by-documentId strategy, `verificationV2.ts` beyond base = head. The four platform suites and the KS-380 preflight. Upper-case client hashes stored raw. CI checks on the PR. Add anything else a reader might assume you covered.

## Verdict
`verdict.md` in `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/`. Line 1 per gate_common section 6, for PR 2004, and the merge tree on develop e899463d2a0b for the merge seat. Then FOUND / TESTED / HOW with controls; `## What passed (measured)` numbered to match the questions above; `## NOT tested`; `## Plain answer for Kam` (3-6 plain sentences: what a merge would change for users, and that G192-F1 remains open and ticketed). Finding ids `G193-F<k>`. Final message per gate_common section 7, including the head and develop at start and end, the pids stopped, and any stray file outside the workdir (there should be none). Start the workdir with `.gitignore` (gate_common section 2) before anything else.


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
