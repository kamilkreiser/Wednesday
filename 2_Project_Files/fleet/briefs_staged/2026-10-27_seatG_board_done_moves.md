## NEW SEAT: you are Seat G <N>th (lane Secuura/Blockchain-G, BOARD HYGIENE, NO CODE, on SONNET): move 16 verified-deployed tickets to Done on the Linear board, each with one BLUF comment and a read-back

**Routing receipt:** `model: claude-sonnet-5-5 -- C2 (16 Linear state moves, each gated by a git ancestor check; no code, no repo write) -- P1-P4: Linear writes on the board account, a read-only worktree`. Wednesday switches this pane with `/model claude-sonnet-5-5`; if you run on another model, say so in your plan confirmation. (Row C2: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md` line 92. The drafter chose C2 on the instruction, not by re-reading the row's board-hygiene fit.)

**Why you exist:** the 06:15 sweep (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_secuura-lanes-0615/lanes.md`, section 2) triaged 23 tickets: 17 DONE-READY (10 clean, 7 whose only residue is an unfiled post-merge gate note), 5 RESIDUE, 1 already Done. Every PR on them is merged into develop `ec3313a80440`. Wednesday chose to leave the 7 notes unfiled, so they do not block Done. **Done = tested + works + deployed:** kintsugi runs `ec3313a80440` (Seat D 34th, DEPLOYED 2026-10-26T18:49Z), and a ticket moves only if its merged PR is an ancestor of that sha.

## BLUF
1. **Sixteen tickets, in the table in QUEUE 2.** The sweep's 17 DONE-READY minus **KS-1602, which is EXCLUDED** (Wednesday's judgement call: it stays open, because its description also names two other faces the gate says are untouched).
2. **Per ticket, in this order:** `git merge-base --is-ancestor <squash sha> ec3313a80440` in your own worktree (rc 0, on its own line) -> re-read the ticket's assignee and state -> ONE facts-only BLUF comment -> the state move to Done -> a read-back. Any rc other than 0, or an assignee of Peter or Stuart, means: skip that ticket, record it, and go on to the next.
3. **Untouched, whatever else happens:** the RESIDUE five (KS-1524, KS-1548, KS-1560, KS-1391, KS-1728), KS-1602, and KS-1636 (already Done per lanes.md section 2).
4. **No code, no push, no PR, no merge, no deploy, no box.** Your only writes are the comments and state moves above, plus your handover folder.
5. **Do not mention filing, residue or gate notes in any comment**; the unfiled notes are Wednesday's to handle.

## QUEUE
### 0. Boot
Your FIRST tool call reads `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.launch_preflight_last.txt`; quote it with its launch stamp in your plan confirmation. Plan confirmation: a QUESTION mail, topic `plan confirmation`, to `wednesday-agent@agentmail.to`, subject starting `[Secuura/Blockchain-G -> Wednesday]`, body line 1 `Seat G <N>th`, sent before the first Linear write. Derive the ordinal from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (newest Seat G row + 1; the drafter did not locate the newest G row), and establish your seat from your pane (`Secuura/Blockchain-G`), never from which mail looks like yours. Pin a client identity in your clone before any commit (you make none, but pin it anyway): `git config user.name 'Kam Kreiser'`, `git config user.email kamil.kreiser@secuura.ai`.
**Your clone:** a scratch clone or read-only worktree of your own under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-g-board` (never inside `2_Project_Files`). Bring the objects in with a fetch from GitHub that supplies the key and keepalive explicitly, since a scratch clone has no `core.sshCommand` (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` lines 410, 417):
`env -u GIT_SSH_COMMAND git -c core.sshCommand="ssh -i /Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 -o ServerAliveCountMax=20" fetch origin develop`, then assert `git rev-parse FETCH_HEAD` and `git ls-remote origin refs/heads/develop` agree. **`ec3313a80440` must exist as an object in your clone** (`git cat-file -t ec3313a80440` prints `commit`); develop may have moved on past it (human merge commits have landed before), which is fine: you test ancestry against `ec3313a80440`, not against the new tip. A push is never needed here.
**Shared inbox:** `secuura-blockchain@agentmail.to` is read by six-plus seats at once (R, S, T, U, V, G, D 34th, B). **A mail naming another seat is not yours**; act only on mail naming your own full seat name, treat an earlier occupant of letter G as FOREIGN, and a mail naming no seat is a QUESTION.
**Linear access:** `set -a; . "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"; set +a` per command (the key is `LINEAR_API_KEY`, header `Authorization: $LINEAR_API_KEY`, no `Bearer`; never print it). Use `comments(first:50)` and sort client-side by `createdAt`. Before the first move, query the KS team's workflow states and record the `Done` state's id and its type (`completed`); stop with a QUESTION if there is more than one state named Done.
**Deployed claim, verified by you, not copied:** read Seat D 34th's DEPLOYED evidence under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-27_seatD-34th/evidence/` (the folder exists; the drafter did not open its files) and its DEPLOYED mail of 2026-10-26T18:49Z in the shared inbox, and quote in your plan confirmation the line that names `ec3313a80440` on kintsugi. **If you cannot find that line, STOP with a QUESTION; do not move anything.** You run no `az`, no `curl` to a box and no `ssh`.

### 1. Per-ticket procedure (repeat for each row in section 2)
a. `git -C <your clone> merge-base --is-ancestor <squash sha> ec3313a80440; rc=$?` on its own line. The squash shas below were read by the drafter from develop history; re-derive each yourself with `git log ec3313a80440 --grep='(#<PR>)' -1 --format=%H` and use YOUR full 40-character value in the comment. rc must be 0.
b. Re-read the ticket (state, assignee, comments sorted by `createdAt`). **Skip if assigned to Peter or Stuart** (the drafter's read found none of the 16 so assigned, assignee column below) and skip if the state is already Done (record it).
c. Read the PR's merge comment on the ticket and the PR body's Test Evidence (via `gh pr view <n>` under the project's own identity: `GH_CONFIG_DIR=/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config`, `gh auth status` first; if `gh` is not logged in, use the ticket's own merge comment alone and say so). The comment's test line quotes what they say, with their ratios; do not paraphrase a result into something stronger.
d. ONE comment, BLUF-first, facts only, in this shape (fill every field from your own reads; if a field has no source, write `not found` rather than leave it out):
   `BLUF: Done. Merged PR #<n> (squash <full sha>), an ancestor of ec3313a80440, which kintsugi runs (deployed by Seat D 34th, 2026-10-26T18:49Z). Tests: <the PR's Test Evidence, quoted with ratios>.`
   No other text. No `@` mention. No mention of residue, filing or gate notes.
e. The state move to Done (`issueUpdate` with the Done `stateId`).
f. Read-back, in the same action: re-query the ticket and print `identifier`, `state.name`, and the id and `createdAt` of your comment. A ticket is counted moved only when the read-back shows `Done` and your comment. A mismatch is a failure to fix and re-verify, not to skip (no-skip-on-failure).

### 2. The 16 tickets (state before: In Progress for every row, drafter's read)
| Ticket | PR | Squash on develop (verify) | Assignee at the drafter's read | Triage | Test pointer from lanes.md (you re-read the PR, this is a pointer) |
|---|---|---|---|---|---|
| KS-1735 | #1711 | `5f6899918` | kamil.kreiser@secuura.ai | clean | 15-cell suite red 10/5 on the old guard |
| KS-1729 | #1714 | `ab74d4a9f` | kamil.kreiser@secuura.ai | clean | three cold-import hooks given a 120 s budget; the ticket records the failure reproduces 1 in 6 cold runs |
| KS-1551 | #1710 | `8661f5d41` | unassigned | clean | gate GO, no Major or Minor (per the ticket's merge comment) |
| KS-1554 | #1709 | `444813665` | unassigned | clean | leg-16 cells cover services/security and m365-integration. The attachment list also shows a second link ending 1548; cite only #1709 |
| KS-1566 | #1704 | `b1afcb9bc` | kamil.kreiser@secuura.ai | clean | new cell `expect(MAX_EVIDENCE_LOOKUPS).toBe(8)`, mutant G6 red. No merge comment on the ticket; the merge is from git |
| KS-1527 | #1697 | `13d1af7b9` | unassigned | clean | items a and b only, as the ticket's checklist |
| KS-1443 | #1715 | `64b275091` | kamil.kreiser@secuura.ai | clean | gate GO; Linux proof in a `node:24-bookworm` container (per lanes.md) |
| KS-1726 | #1713 | `b0ef926f6` | kamil.kreiser@secuura.ai | clean | gate GO; five comments plus the sixth `@description` corrected |
| KS-1324 | #1718 | `bea5ed493` | kamil.kreiser@secuura.ai | clean | cell asserts child liveness when the runner returns; `T1303_ELAPSED` gone |
| KS-1331 | #1719 | `ec3313a80` | kamil.kreiser@secuura.ai | clean | signal forwarded to the suite's process group; round-2 guard cell. This squash IS the deployed sha |
| KS-1714 | #1706 | `5c5cd0d97` | kamil.kreiser@secuura.ai | +note | both quarantine suites exit non-zero after a failed restore |
| KS-1578 | #1705 | `1f2ec373b` | unassigned | +note | two near-miss cells (`list` of a near-miss organisation id lists no key) |
| KS-1713 | #1701 | `409ad6c36` | kamil.kreiser@secuura.ai | +note | mutant M3 red |
| KS-1716 | #1689 | `e1137bf89` | kamil.kreiser@secuura.ai | +note | `check-package-format.sh:730` fixed. NOTE: PR #1716 is KS-1736's, not this ticket's; this ticket's PR is #1689 |
| KS-1438 | #1717 | `dd276d8bb` | kamil.kreiser@secuura.ai | +note | guard resolves both sides; symlink arm |
| KS-1513 | #1695 | `662f2eded` | unassigned | +note | SKIP line, rc 0, 23/0 per lanes.md |

All 16 squash commits were found with `git log ec3313a80440 --grep "(#N)"` by the drafter; ancestry is YOUR check in QUEUE 1a. Order: the ten "clean" first, then the six "+note".

### 3. Report
One batch mail to `wednesday-agent@agentmail.to`, subject `[Secuura/Blockchain-G -> Wednesday] Board moves READY`, body line 1 `Seat G <N>th`: a table of the 16 with, per ticket, the ancestry rc, the comment id, the read-back state, or the reason it was skipped. State plainly how many moved, how many were skipped and why, and that KS-1602, the RESIDUE five and KS-1636 were not touched. Handover at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-27_seatG-<N>th/HANDOVER.md` and a history.md row, then wrap.

## HOLDS
- Signature classes pause for Kam: production, money, external communication to any human, anything irreversible. No box, no `az`, no deploy, no merge, no push, no PR. No Docker.
- **No comment to or `@` mention of Peter or Stuart**; skip any ticket assigned to either. Anything needing a human to act goes to Wednesday as an escalation candidate.
- **Do not archive, cancel or delete any ticket**; no label, assignee or priority change; the only field you change is the state, on the 16 named tickets (a shared board cascades, per Seat G 16th's precedent recorded in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md`, line 209).
- Never `cd`; absolute paths only; exit codes on their own line (`cmd > out 2>&1; rc=$?`), never through a pipe; the Bash tool is zsh; use `/usr/bin/grep -i` and pair a zero count with a positive control.
- Mail discipline: every mail you send names `Seat G <N>th` on body line 1 and starts its subject with `[Secuura/Blockchain-G -> Wednesday]`. Never put stop, hold, checkpoint or hand over in a mail SUBJECT. A QUESTION mail (Context, one Question, Meanwhile, Needed-by) only for a blocker; after ~15 minutes with no ANSWER proceed on the safest reading unless the item is approval-class.
- If you find a ticket in the 16 whose PR is NOT an ancestor of `ec3313a80440`, or whose state is not In Progress, do not move it and do not "fix" it: record it for the report.

## PARTITION (written from every seat's side)
**Yours (Seat G, `Secuura/Blockchain-G`):** the Linear state and one comment on each of the 16 tickets in QUEUE 2; your own clone under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-g-board`; `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-27_seatG-<N>th/`. You write no repository file.
**NOT yours, live beside you (source `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_secuura-lanes-0615/lanes.md` section 3, lanes 1-5):**
- **Seats R, S, T, U, V** (BUILD, panes `Secuura/Blockchain-R` ... `-V`): R `run-shell-suites.sh` and its test, `run-schemathesis.sh` and the ks1405 test; S `preflight.sh`, `preflight_deps.test.sh`, `pre_push_hook_base*.test.sh`; T `services/security/vitest.config.ts` and its `ks*.test.ts`; U the m365 and api-gateway `*.openapi.ts`, the spec-route-map test and the generated yaml; V `typecheck-tests/check.cjs`, the ks1000 test, the baselines, `Blockchain/Dev/CLAUDE.md:398-403`. Their tickets (KS-1745, KS-1465, KS-1563, KS-1643, KS-1734, KS-1700, KS-1531, KS-1523) are not yours: you never comment on or move them.
- **Seat D 34th** (`Secuura/Blockchain-D`, pane %19): DEPLOYING develop `ec3313a80440` to DEMO, no code. You read its evidence; you never write to its folder and you never touch demo.
- **Seat B** (`Secuura/Blockchain-B`): read-only kintsugi investigation, no code. Not yours.
- **Not moved by anyone today:** KS-1602, KS-1524, KS-1548, KS-1560, KS-1391, KS-1728, KS-1636, and the Peter and Stuart tickets.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-10-12 (grant): Secuura tickets go to Done once fully tested, working and deployed; "deployed" = kintsugi under the October deploy grant (Wednesday's reading, stated to him) | `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-12_secuura-done-when-tested-works-deployed-and-never-idle.md` rules 1-2 (Wednesday's tree) | read 2026-10-27. Kam 2026-10-27 ~06:2x (terminal): "keep going with the tickets". Using kintsugi's running sha `ec3313a80440` as the Done test is Wednesday's application of that grant.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The seven "+note" tickets (KS-1714, KS-1578, KS-1713, KS-1716, KS-1438, KS-1513, and KS-1602) have their post-merge gate notes left UNFILED on purpose; those notes do not block Done. KS-1602 is excluded (judgement call: stays open). | Wednesday's drafting request | 2026-10-27
- The RESIDUE five stay untouched. | same | 2026-10-27
- Build and board seats stop and report; one batch mail at the end. | the 2026-10-26 U2 brief, same section | read 2026-10-27

PROVENANCE:
- Triage (17 DONE-READY, 5 RESIDUE, 1 already Done), the per-ticket PR numbers and the "+note" classification | `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_secuura-lanes-0615/lanes.md` section 2 table and counts line | read 2026-10-27
- Each PR's squash sha on develop | `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src log ec3313a80440 --format='%h %s' --grep='(#N)' -1` for N in 1711, 1714, 1710, 1709, 1704, 1697, 1715, 1713, 1718, 1719, 1706, 1705, 1701, 1689, 1717, 1695, run by the drafter | read 2026-10-27 (abbreviated shas as printed; ancestry itself NOT tested by the drafter)
- Each ticket's state (In Progress, all 16), assignee (kamil.kreiser@secuura.ai or unassigned, none Peter or Stuart), comment count and attached PR numbers | Linear GraphQL, key from the Blockchain `.env` (not printed), comments(first:50) sorted client-side; drafter's query 2026-10-27 | read 2026-10-27. Last comment dates: KS-1735 2026-10-26T11:13Z, KS-1729 11:13Z, KS-1551 09:49Z, KS-1554 09:04Z, KS-1566 06:40Z, KS-1527 none, KS-1443 13:13Z, KS-1726 13:13Z, KS-1324 13:39Z, KS-1331 14:49Z, KS-1714 07:57Z, KS-1578 07:33Z, KS-1713 07:33Z, KS-1716 06:47Z, KS-1438 13:39Z, KS-1513 06:47Z (all 2026-10-26)
- KS-1602, KS-1524, KS-1548, KS-1560, KS-1391, KS-1728 states were read in the same query (all In Progress); not touched | same query | read 2026-10-27
- Develop tip `ec3313a80440d0eee9fd07204c024518417ff9d7` is the KS-1331 squash (#1719) | `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src ls-remote origin refs/heads/develop`, run by the drafter | read 2026-10-27
- Kintsugi deploy finished 2026-10-26T18:49Z by Seat D 34th | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-27_seatB_kintsugi_admin_login.md` line 100 (Wednesday's brief to Seat B), and the brief's request line. The drafter did NOT open Seat D's evidence files, so "kintsugi runs ec3313a80440" is a relayed claim until you verify it in QUEUE 0 | read 2026-10-27
- Linear `Done` state id and type: NOT read by the drafter (you read it in QUEUE 0) | unmeasured | read 2026-10-27
- The residue-note contents for the +note tickets | `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_secuura-lanes-0615/lanes.md` section 2 rows (quoted there; deliberately not repeated in comments) | read 2026-10-27
- Not measured by the drafter: ancestry of each squash sha against `ec3313a80440` (git history scan was by `--grep` from that rev, which implies ancestry but is not the `merge-base` check); the PR bodies' Test Evidence blocks (the drafter read the sweep's quotes only); whether `gh` is logged in under the project identity; Seat D 34th's evidence contents; whether the board has automation that reacts to Done; whether an In Progress -> Done move is allowed by the team's workflow without an In Review step | unmeasured, you measure these | read 2026-10-27
- KS-1636 state Done (last comment 2026-10-26T07:24Z): untouched | Linear ticket KS-1636 | read 2026-10-27
- KS-1736 state Done (last comment 2026-10-26T19:25Z, Seat D 34th's): not in your 16, untouched | Linear ticket KS-1736 | read 2026-10-27

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-27 06:29
