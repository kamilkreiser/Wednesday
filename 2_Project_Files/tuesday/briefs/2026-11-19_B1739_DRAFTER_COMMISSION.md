# B1739 drafter commission — NexusAI lane N-J: RD-445 item 2 only (SEAT-N159)
Commissioned by Tuesday (s293), 2026-11-19. Drafter model: Sonnet (routing row C8). You DRAFT a kit; you build nothing.

Draft ONE builder kit `2_Project_Files/tuesday/briefs/2026-11-19_B1739_SEAT-N159_nexusai-lane-nj-marketplace-jwt-bypass.md`
(+ `.measured` sidecar; return the drafter report as TEXT in your reply, Tuesday saves it) in the FORM of
`2026-11-19_B1737_SEAT-N158_nexusai-lane-nf-browser-escapes.md` (read it whole) and with the lessons of the two newest
builder STATUS files folded in by name: `!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-19_B1733_STATUS.md`
(Corrections first) and `.../2026-11-19_B1737_STATUS.md` (it may still be running: read what is there, say what you read).
In particular: ONE lock acquisition (the seat tests its own judge and kept tools on a recorded fixture before the lock) and
a main move is absorbed inside the same acquisition. Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole (it names
/Volumes/Laptop-DEV in places: the volume is /Volumes/Datasec_DEV).

SCOPE (Tuesday's decision, a default under the standing backlog grant, NOT the product owner's; write it that way):
RD-445 item 2 ONLY, the ticket's first option: `backend/marketplaceJwt.js` REFUSES to honour `MARKETPLACE_SKIP_JWT=true`
when `NODE_ENV=production` (the token is verified as if the flag were unset) and logs loudly whenever the flag is on.
The flag is NOT removed (removal changes development and sandbox behaviour nobody has measured). Items 1 and 3 of the
ticket are NOT in this lane; the ticket stays open for them. Read RD-445 whole by Jira GET and quote item 2's sentence.
Source: sweep `2026-11-19_SWEEP-1115_datasec-actionable-lanes.md` lines 74 to 78 (measured at an older main: RE-MEASURE
every file, line and count at the current main) and `2026-11-19_SWEEP-1115_TUESDAY-ANSWERS.md` item 3.

BASE: the lane's base is NexusAI main AFTER the lane before it (B1737, lane N-F, branch of SEAT-N158) lands. It has NOT
landed. Measure every file and line at the current main (9373976efc7d93f522f97648beb608b4d3e16fb2 when this was written:
re-read it), say so, and leave the BASE slot for Tuesday's stamp. The kit REFUSES to start until the N-F pull request is
merged, and carries the re-measure rule: if an owned path differs between the stamped base and main at Step 0, STOP.
The expected-counts file (`scripts/verify-expected-counts.json`) is shared with N-F: the kit takes its base figures from
main at Step 0 (never from this commission) and regenerates them by the project's own command.

PARTITION: owned = `backend/marketplaceJwt.js`, the new test file(s) under `__tests__/`, the expected-counts file, and any
existing test that pins the OLD answer (flag on + production = accepted). NOT owned: `backend/server.js`,
`backend/marketplace-api.js` unless a measured need is shown (then it is a STOP question, not an edit), every `static/**`
file, every workflow, template and compose file (read-only: the kit CONFIRMS by program that none of them sets the flag,
each count with a control that fires, and names the frame: what was searched and what lies outside it, e.g. hosted app
settings, which nobody here can read).

REQUIRED CONTENT:
- An old-answer census BY PROGRAM: every test, fixture, script, doc and env sample that names `MARKETPLACE_SKIP_JWT` or
  `SKIP_JWT`, each listed as rewrite / unaffected / out of lane, with the grep and its control.
- How the test suite itself reaches the marketplace webhooks today: if existing tests rely on the flag, say under which
  NODE_ENV they run, so the change cannot silently turn them red or disarm them.
- Cells: production + flag -> the token is still verified (a bad token refused, a good one accepted); non-production +
  flag -> bypass as today, with the loud log line asserted; flag off -> unchanged in both environments. Plants with
  predicted red cells, each prediction dry-run by you on a scratch copy or marked UNMEASURED (never a guessed number).
- The exact log text is a DEFAULT of the change (operator-facing, not customer-facing); say so. No customer-visible word
  is added; if one would be, that is a STOP.
- Gate recommendation: G1 OPUS (an authentication bypass on a webhook surface), with the CodeQL step: the kit runs
  `2_Project_Files/tuesday/tools/codeql/pr_codeql_check.sh` twice (CQ-1 before the lock, CQ-2 before the push); see
  `tools/codeql/GATE_STEP.md`.
- PRIOR-WORK CHECK: what earlier work touched the marketplace token check (git log -S on the flag name, the tickets that
  name it), and why the flag exists.
- No ruling exists for this lane. Every choice is written as Tuesday's default. No text says the product owner decided.
- Every jest/vitest selector in JS-regex syntax; every expected tool output quoted from a real run or marked UNMEASURED.
- Test-cell counts: count INDENTED `test(` lines (`^[[:space:]]+test\(`), and print the column-1 count beside it.

HOW: read-only everywhere. NexusAI GH_CONFIG_DIR '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'
(verify the account reads kamilDatasec before the first call; every gh call `-X GET`). Jira GET only, credentials read by
name in-process from the project's `4_Credentials/.env`, never printed. In the project checkout: git read verbs only
(`--no-optional-locks`); any write verb runs in your own scratch. Pick a jest worktree slot no kit or gate named on
18-19 Nov (scan the briefs; taken include 5, 11, 12, 13, 14, 17, 18). Scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1739/`. No `cd`; the shell is zsh; absolute paths.
Never delete (quarantine). Clocks come from `date` in the same command, never typed.
First line of your reply: `STARTABLE: YES|NO - why`. Then the report: files, recommended slots, corrections to this
commission, D/Q defaults, UNMEASURED list.
