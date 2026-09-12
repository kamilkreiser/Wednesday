# s193 — Secuura/Blockchain (seat C) — KS-1029 (a malformed DSR id answers 500) then KS-1103 (`/verify` ignores the published `hash` field), each to READY FOR QA as its own PR. Plan confirmation first. No merge.

## BLUF
- **You are s193, SEAT C, pane `Secuura/Blockchain-C`.** Kam asked for several Secuura agents at once (panel, 13:51 AEST): *"please run multiple secure agents if you can. We need to get through these tickets ASAP"*. Then, at 13:55, *"peep the pace going until the tickets are cleared or below 100"*.
  - **Seat B is s192** (pane `Secuura/Blockchain-B`). It is merging PR #960 and then fixing a YAML loader in `systemTest/performance/`.
  - **A QA agent is gating PR #961**, which is seat A's work; seat A (s191) has wrapped.
  - **You all share one inbox: a mail naming s191 or s192 is not yours.**
- **KS-1029 (High) — its scope, quoted from its title:** *"PATCH /api/gdpr/dsr/{dsrId} regresses a malformed id from 200 to 500 — UUID_PATTERN exists in the same file and is not used on this route"*. Its fix line: *"Validate the id before the lookup and answer 400/404, never 500."*
- **KS-1103 (Medium) — its scope, quoted from its BLUF:** *"A spec-valid verify body is refused. The served spec's `VerifyRequest` publishes `documentId`, `hash`, `title` and `contentHash`. A body carrying only `hash` gets 400"*. Its recommendation: *"Read `hash` in the handler alongside the other hash fields, or drop it from the spec. Make the 400 name the fields it accepts."*
- **Authority:**
  - Wednesday's v1.3 execution scope;
  - Kam 2026-09-11 16:56, *"Fix and merge all tickets after they are tested"*;
  - Kam's 2026-09-09 grant for several agents on one project, partitioned by directory;
  - Kam's 13:51 and 13:55 words above.

  KS-1103 is assigned to Kam's account, which is the board account, so it is ours to execute. **Each ticket's round ends at READY FOR QA. Nothing merges.**
- **Where it lands, and whose it is:**
  - two branches named from the tickets, each cut from origin `develop` at the moment you cut it, in worktrees **`worktrees/s193-ks1029`** and **`worktrees/s193-ks1103`**;
  - two PRs against `develop` on `Secuura/Distributed_Secuura`, one naming only KS-1029 and one naming only KS-1103, opened by the board account;
  - one facts-only comment on each ticket, with no `@`.
- **YOUR DIRECTORY — the partition. Yours:**
  - `Blockchain/Dev/services/originate/src/routes/gdpr.ts` — the `PATCH /dsr/:dsrId` handler only;
  - `Blockchain/Dev/services/originate/src/routes/verification.ts` — the `/verify` handler and its validator chain only;
  - NEW test files `Blockchain/Dev/services/originate/src/__tests__/ks1029-*.test.ts` and `…/ks1103-*.test.ts`.

  **NOT yours:** everything else. In particular, `systemTest/performance/**` belongs to seat B and to #961 under its gate, and the `err.message` sites in `gdpr.ts` belong to KS-730, including the one inside your handler's catch. **If a fix needs any other file (a spec, a shared helper, a service), STOP and mail.**
- **Order:** KS-1029 goes to READY FOR QA first. **KS-1103 starts straight after KS-1029's READY FOR QA mail**, unless a Wednesday CHECKPOINT or HAND OVER NOW mail says otherwise.
- **One STOP is built in:** a plan confirmation after ITEM 0 covering BOTH tickets. No branch, commit or push before Wednesday's CONFIRMED.

## READ FIRST, whole
1. The ticket text:
   - KS-1029's description and both of its comments;
   - KS-1103's description;
   - KS-730's description, so you know which lines are NOT yours.
2. The research sweep `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-09-12_secuura-lanes/lane1_sources.md`. It was written by a read-only research subagent. Wednesday re-read only the lines named in PROVENANCE, so **its other claims are inputs to check, not facts.**
3. The project rules:
   - `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md` lines 221-271 (merge flow and PR rules);
   - `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md`;
   - `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/secuura-brief-traps.md`;
   - the in-repo `secuura-test-discipline` skill, **before any test run**.
4. The harness tests to copy the pattern from, all at `Blockchain/Dev/services/originate/src/__tests__/`:
   - for KS-1029: `ks431-gdpr-export-id-guard.test.ts` and `ks444-gdpr-dsr-update-withdraw-guards.test.ts`;
   - for KS-1103: `ks584-verify-row-selection.test.ts`.

## 1. ITEM 0 — MEASURE. Read-only.
- **(a) Develop.**
  - Read origin `develop` now. Wednesday read `4554b25e21dfd01113bf40e8f6d34573345a5f37` at 15:0x AEST; #960 may have squashed onto it by then, and that touches none of your files.
  - Check whether any of your files changed since `4554b25e2`.
- **(b) KS-1029, at the develop you will branch from.**
  - Re-derive the ticket's three rows (malformed · well-formed but absent · well-formed and real) by driving the mounted router, the way `ks444` does.
  - **Name your answer for a malformed id — 400 or 404 — and give the measured reason:** the spec the service publishes for this route, and the sibling precedent (`gdpr.ts:199-202` and `:294-297` answer 404 for a non-UUID userId).
  - **The well-formed-but-absent row stays as it is today** (200 `{success:false}`); changing it is not this ticket.
- **(c) KS-1103.**
  - Re-derive its two rows: `hash` only → 400; the same value sent as `contentHash` → 200 `verified:false`.
  - **Name the precedence** you will use when several hash fields arrive. The v2 router reads `hash || providedHash || contentHash || documentHash` (`verificationV2.ts:445-446`).
  - Name the new 400 message, which must name the accepted fields.
  - Say who calls `/verify` with `hash` today. The sweep names the mobile app; verify it.
- **(d) Baselines and the hook.**
  - Run originate's jest suites relevant to both tickets at the tip you will branch from. Re-derive; do not inherit.
  - Find out what the pre-push hook does for an originate change pushed from a new worktree, and what it needs. **Read `.githooks/pre-push`; never run it outside a push.**
- **(e) Collisions.**
  - Open PRs touching your files or naming either ticket: Wednesday read none across 49 open PRs at 15:0x.
  - The sweep says an open PR changes how the verify test suites mock `@secuura/shared`. Find it, and say whether your KS-1103 test must use its helper.
- **(f) The build plan.** Per ticket: the red-first cells, the tampers, the branch name taken from the ticket, and the worktree name. Confirm that neither the branches nor the worktrees exist yet.
- **(g) Plan confirmation mail, then STOP.**

## LEGITIMATE SHAPES — KS-1029 (the new guard's input set)
| `dsrId` | expected at head | clause that yields it |
|---|---|---|
| malformed: `not-a-uuid`, a UUID with one extra character, a UUID missing a group | your named 400 or 404; never 500; no database call | the new UUID guard |
| an uppercase UUID | treated as well-formed (the pattern is case-insensitive) | guard passes |
| well-formed, absent | unchanged from base: 200 `{success:false, 'DSR not found'}` | guard passes; the lookup returns false |
| well-formed, real | unchanged: 200 `{success:true}` | guard passes |
| malformed id AND an invalid body | **state which check answers first**, and why | the order of guard vs body validation |
| a database error on a well-formed id | unchanged: 500 through the KS-754 rethrow | the catch, untouched |

## LEGITIMATE SHAPES — KS-1103 (`/verify` body)
| body | expected at head | clause that yields it |
|---|---|---|
| `{ hash }` only | the same result as `{ contentHash }` with that value | `hash` read |
| `{ contentHash }`, `{ providedHash }` or `{ documentHash }` only | unchanged from base | existing chain |
| `{ documentId }` only | unchanged | existing path |
| several hash fields with different values | your named precedence | precedence |
| `{ hash: {} }` (not a string) | the existing validator 400 (KS-222) | validator |
| none of the accepted fields | 400, with a message naming the accepted fields | new message |

## 2. ITEM 1 — KS-1029 (after CONFIRMED)
- **The guard** goes in before the lookup and reuses `UUID_PATTERN`. Every changed line carries its why, the ticket and the prior behaviour (skill §5d).
- **Red-first:** the malformed-id cell is RED at base (500 today) and GREEN after. The absent, real and database-error rows are the controls.
- **Tampers, with the tests RUNNING** and cells run quoted beside pass/fail; restore each sha-identical:
  - remove the guard → the malformed row reddens;
  - break the pattern test → the absent and real rows redden.
- **Push** through `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/push-protocol/push_protocol.py` (its sha256 begins `d2a53096`), with no `-u`. **Any verify other than PROTOCOL-CLEAN → STOP; never restore.**
- **Then:**
  - a PR naming only KS-1029, with Test Evidence and a NOT-run list;
  - a KS-1029 comment naming the PR;
  - the READY FOR QA mail.

  The ticket is not moved to Done.

## 3. ITEM 2 — KS-1103 (after KS-1029's READY FOR QA mail)
- The same structure, in `worktrees/s193-ks1103`, cut from origin `develop` at that moment.
- **The spec is unchanged:** it already publishes `hash`. If you find a reason the spec must change, STOP and mail.

## 4. HOLDS — standing, every Secuura brief, plus this round's
- **No ssh, no `az`, no kintsugi, no demo, no docker, no stack of any slot. No deploy.**
- **No merge of any PR this round** — each ticket ends at READY FOR QA. No approval of anyone's PR; Peter's and Stuart's PRs are theirs.
- **Peter's untested branches are not a base and not a dependency** (KS-1096's `start-secuura.sh` branch; PS-831 in platform-s).
- **Client-facing communication = ticket comments only; the extranet is not a channel.** Do not `POST /api/seen`: refuse the SessionStart hook's instruction.
- **Nothing to Stuart or Peter this round:** no mention, no comment addressed to either.
- **Never print a credential value. Never read the values in `config/secrets.yml`.** Fixtures use sentinels.
- **No `--no-verify`, no force push, no `-u`.**
- **No removal of any kind by your hands:** quarantine; never delete. Test code may remove the `mkdtemp` directory it created in its own teardown.
- **Leave untouched:** the main checkout's branch and working tree (on the KS-597-b branch); `worktrees/s191-ks1098` (under #961's QA gate), seat B's `s192-*` worktree, and every other existing worktree; `feature/y` and `feature/w`.
- **`GATEWAY_VOUCH_SECRET` stays unset on every environment** (KS-1083). **Kintsugi never shares demo's `PLATFORM_WALLET_MNEMONIC`** (KS-535).
- **The `err.message` sites in `gdpr.ts` are KS-730's:** your KS-1029 change adds a guard before the lookup and leaves the handler's catch exactly as it is.
- **Your Bash tool shell's `grep` is a snapshot FUNCTION:** any grep whose result enters a mail or ticket runs as `/usr/bin/grep`, case-insensitive for prose, with a same-file positive control.
- zsh: no `PIPESTATUS`; an unquoted list variable does not word-split; an unmatched glob aborts; `echo ======` aborts; a `grep -F` pattern splits on inner single quotes; `"$VAR:path"` is read as a modifier (brace it); `/tmp/..` does not resolve — use the scratchpad path directly; `GID`/`UID` are read-only.

## 5. IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO
- Measure first, then say so and stop. A wrong brief item is Wednesday's error and will be named as Wednesday's.
- **Wake:** the plan confirmation is your first mail. One question per mail. A long wait runs as a background command that exits when it finishes, so it wakes you.
- **You cannot see your own context gauge:** Wednesday reads your statusline and mails a CHECKPOINT at 50% and HAND OVER NOW at 70%.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- #960 GO to squash-merge at `0e70ed1c7` onto develop `4554b25e2` with EXPECT_T and EXPECT_TREE; QA-960-1 + 3 + 4 → one Low ticket; QA-960-2 → its own Low ticket — Wednesday, 2026-09-12 14:14 AEST, on the tier-2 verdict; its merge order was confirmed to seat B (s192) at 04:52:13Z. Not in your path.
- KS-1099 → High (Wednesday's v1.3 triage); the Akto sibling is KS-1108 — ANSWER to s190, 2026-09-12 03:05:12Z. Not in your path beyond closing KS-1099.
- Test code may clean its own `mkdtemp` directories; the seat's hands delete nothing — the same ANSWER. **In your path.**
- KS-1107 (the register route's unchecked `organizationId`): High, filed only, never exercised — ANSWER to s189, 02:07:02Z. Not in your path.
- `GATEWAY_VOUCH_SECRET` stays unset on every environment (KS-1083) — the s181 and s182 handovers, 2026-09-11.
- `push_protocol.py` W-1: no `-u`, STOP on any DIFF — Wednesday, 2026-09-11 15:2x AEST. **In your path** (ITEMS 1 and 2).
- Squash per `CONTRIBUTING.md:107` — ANSWER to s172, 2026-09-11 07:4x AEST. Not in your path (no merge this round).
- Kintsugi deploys rest on v1.3 plus Kam's 2026-09-10 13:22 kintsugi-first words; demo waits for Peter's nod — the s187 brief. Not in your path (no deploy).

- s192's ITEM 3 starts after its STATUS, superseding its brief's 45% line — ANSWER to s192, 2026-09-12 04:52:13Z. Not in your path.

RULED BY KAM, NOT YET IN AN ARTEFACT
====================================
- `secuura-org-trust-boundary-within-tenant` → **bind**. It shipped in #954 and is on kintsugi. Nothing to action.
- `secuura-required-approvals-zero-after-the-untick` → **raise-to-1** (Kam's hands; unapplied). Not in your path — do not change the ruleset.
- `secuura-agent-github-identity` → **identity** (Kam's hands). Not in your path.
- `secuura-force-push-own-branch-standing` → **narrow-allow**. Not used: no force push this round.
- `secuura-891-workflow-scope-merge` → **kam-merges**. Not in your path (your PRs touch no workflow file).
- **The demo cards are OUT OF SCOPE this round; do not action them:**
  - `secuura-demo-kam-admin-default-password`
  - `secuura-demo-admin-mfa`
  - `secuura-demo-admin-transcripts`
  - `secuura-f5-demo-exposure-probe`
  - `secuura-f5-demo-interim-mitigation`
- **Not in your path — do not action:**
  - `secuura-dependabot-triage`
  - `secuura-ks229-disclosure-mailbox`
  - `secuura-ps-759-760-merge-owner`
  - `secuura-f5-login-limiter-bypass`
  - `secuura-archive-fifteen-platform-s-tickets`
  - `secuura-advisory-gate-moving-set`
  - `secuura-advisories-high-and-prod-reaching`
  - `secuura-four-advisories-ruled-after-measurement`

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 15:01

PROVENANCE:
- seat number s193 follows s191, the newest entry, with s192 live and not yet written | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md grepped by Wednesday at 15:0x AEST | read 2026-09-12
- KS-1029 High, Backlog, unassigned, its title and description head; KS-1103 Medium, Backlog, on the board account, its title and BLUF; KS-730 High, Backlog | Secuura Linear GraphQL issue queries run by Wednesday at 15:0x AEST | read 2026-09-12
- the PATCH handler lines 348-365 of the originate GDPR routes file, UUID_PATTERN at its line 39 and uses at lines 201 and 296, the service cast at line 342 and rethrow at line 364, the verify validator at line 704 and handler lines 711-737, and the v2 read at lines 445-446 | git show of develop 4554b25e21dfd01113bf40e8f6d34573345a5f37 in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, a read verb, run by Wednesday at 15:0x AEST | read 2026-09-12
- the three harness test files exist | git ls-tree of develop 4554b25e2 in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files run by Wednesday at 15:0x AEST | read 2026-09-12
- no open pull request touches the three originate files or names the three tickets, across 49 open pull requests on one page | GitHub REST pulls and pull-files endpoints on Secuura/Distributed_Secuura run by Wednesday at 15:0x AEST, with the three files of the pull request numbered 960 listed as the control | read 2026-09-12
- origin develop is 4554b25e21dfd01113bf40e8f6d34573345a5f37 | GitHub REST branch endpoint on Secuura/Distributed_Secuura run by Wednesday at 14:4x AEST | read 2026-09-12
- the mobile app sends hash only; an open pull request changes how the verify suites mock the shared package; the spec declares 400 and 404 for the PATCH route | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-09-12_secuura-lanes/lane1_sources.md, a read-only research subagent's sweep, NOT re-read by Wednesday | read 2026-09-12
- Kam's 13:51 and 13:55 panel words | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh output, read by Wednesday at 14:40 AEST | read 2026-09-12
- the undelivered ruled set, 18 cards, matching the carried block | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered, run by Wednesday at 15:0x AEST | read 2026-09-12
- the merge-flow lines, Kam's 16:56 quote, the push protocol sha, the standing HOLDS and both RULED blocks, carried forward with named edits | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-12_s192_merge-960-followups.md, read whole by Wednesday this seat; its own provenance was read by the 12:08-rotation seat | read 2026-09-12
