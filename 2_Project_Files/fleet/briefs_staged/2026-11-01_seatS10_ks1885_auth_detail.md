# BRIEF: Seat S 10th, Secuura/Blockchain-S. One High-class auth ticket: KS-1885 (social sign-in callback echoes the exchange error)

## NEW SEAT: you are Seat S 10th (lane Secuura/Blockchain-S; Opus; trust $TMUX_PANE, Wednesday writes the pane id from the launcher's "pane ... added (%NN)" line at send)

Fix ONE ticket, KS-1885, as ONE PR at tier 1. It ends at READY FOR GATE. Nothing merges, nothing deploys, no box. Nothing goes to Peter or Stuart.

model: claude-opus-5-5 -- C3 (auth/identity surface, token-bearing error text), gate G1 tier 1. Routing row: security-design builds stay Opus. Gauge UNMEASURED by the drafter.

**Drafted 2026-11-01 by a Sonnet drafter for Wednesday; Wednesday reads it whole before it is sent.** Every read below names its instrument. Where it says UNMEASURED the drafter did not measure it. Lines marked `DRAFTER QUESTION:` are Wednesday's to resolve before send. A seat that finds one still standing treats the stated default as the instruction and says so in its plan confirmation.

## WEDNESDAY'S NOTE AT SEND (read this first; it SUPERSEDES the brief where they differ)
- **Pane id:** trust `$TMUX_PANE`. Live panes at send are Wednesday's list. Live seats when drafted: Wednesday and Seat R 71st. Seat E 24th (mcp-server) may launch in parallel.
- **Develop pin:** `d7691f35312ea158f043e87a3227e477cccb183d` (Wednesday's `ls-remote origin develop`, 2026-11-01 21:27). Develop moves all day. You re-read it yourself at ITEM 0, and every file:line below is "read at develop d7691f35" and is yours to re-read. The object may NOT be in the shared object store: use Seat R 70th's method (see ITEM 0, Worktree), never fetching into the shared checkout.
- **START AUTHORITY.**
  - Card `secuura-wednesday-go-counts-as-kams-word-1030` = a, verbatim: "Yes: Wednesday's GO counts for starting work inside my standing grants (recommended)".
  - Kam, 2026-11-01 21:27, verbatim: "please spin up as many agent agents as possible and use the spark as much as you can to work through tickets".
  - Kam, 2026-11-01 21:32, verbatim: "yes .  override the limit and continue to 100%.  if you reach it, I will log in with a new account".
  - Your plan confirmation goes to Wednesday, and her GO is the start. Signature classes still pause for Kam.
- **Ordinal:** `Seat S 9th` is the highest S in history.md at drafting. You are Seat S 10th. **Re-run that check yourself** (PROVENANCE has the instrument) and, if a `Seat S 10th` heading already exists, STOP and mail.
- **Machine load:** launch when load1 < 7; suites one at a time below load 8.
- **Docs: the FRAGMENT scheme is LIVE (Wednesday's read, answering DRAFTER QUESTION 1).** The 10-31 docs hold is over. Seats R 69th/R 70th raised seven PRs today, each with ONE fragment pair (flow + cheat) under `Projects Documents/fragments/flow/` and `.../cheat/`, per develop's `.claude/skills/secuura-test-discipline/SKILL.md` section 4; all seven merged. Follow SKILL.md section 4 at your base: no section numbers, no edit to the two assembled pages, `node Blockchain/Dev/scripts/docs-fragments.mjs check` ends OK, and a planted defect on a scratch copy fails. **This SUPERSEDES every 'two HTML docs / highest + 1' line below.**
- **Drafter questions answered:** (2) pane id = trust `$TMUX_PANE`; (3) R 70th's exact method: `git clone --shared --no-checkout <2_Project_Files> <your base path asserted absent>`, set origin to GitHub, fetch develop into THAT clone with the explicit key, assert origin/develop = the pin, then `git worktree add` siblings from it; (4) status code unchanged by default, and any change is approval-class, as written; (5) noted.

## BLUF
1. **What.** In `services/auth/src/routes/auth.ts`, the social sign-in callback (`GET /api/auth/social/:provider/callback`) answers 400 with `exchangeErr.message` echoed in a `detail` field (the screen puts the lines at `:1076-1081`; re-read them). The screener's mechanism: the message is echoed unless the error is a `SyntaxError`; a newline in `access_token` makes `fetch` throw a `TypeError` whose message contains the token (QA gate 43: github, google, linkedin and microsoft_personal exposed; facebook not). A token in a response body is the defect.
2. **The fix shape is yours to design.** The direction: log the real error server-side, return a CONSTANT to the caller. Mirror the KS 1410 pattern of constant 500 bodies, and the constant-detail pattern KS 1791 already used on the same lines (per the screen). **The ticket body is read first, and its acceptance criteria WIN over this paragraph.**
3. **One PR, tier 1, red-first.** Adapters in `providers/social/*` need no edit per the screen (taken from the ticket text, not re-read in code by the screener). Your partition is `services/auth/src/routes/auth.ts` plus your new test(s) only.
4. **Sweep the file.** Check EVERY OTHER `detail:` and `.message` echo in `auth.ts` and list them in your plan confirmation. You fix only what the KS 1868 / KS-1885 scope covers (read both tickets). The rest are candidates in your mail. You file nothing.
5. **READY FOR GATE** with the five artefacts (HOLDS), then the wrap. Wednesday's head-pinned GO is the only merge authority.

## WHAT I READ (develop d7691f35; `Blockchain/Dev/` prefix omitted; line numbers are the screener's, re-read them)
- **Board screen, "board screen 21:3x, read by Wednesday",** `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_board-screen-2127/screen.md`, LANE 1 entry (the drafter read lines 15-17 and the UNMEASURED section):
  - Tier 1 (auth/identity). Title "Social sign-in callback echoes any exchange error whole".
  - Files at develop: `services/auth/src/routes/auth.ts` (`:1076-1081`, the `detail` line) plus one new test in `services/auth/src/__tests__/`.
  - "Not in an open PR (auth PRs touch only routes/users.ts and one ks1006 test)" at the screen's basis, 19 open PRs, 60 distinct files.
  - UNMEASURED by the screener: KS-1885's adapter list was taken from the ticket text, not re-read in code. No fix was run; no test or mutant executed.
- **The drafter did NOT open `auth.ts`, the ticket, KS 1791's change, KS 1410's pattern, or any adapter.** All of that is yours.

## QUEUE (in order; each item ends in a mail to Wednesday)

### ITEM 0 (before any code)
- **Launch preflight.** Read `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.launch_preflight_last.txt` in your FIRST tool call and quote it with its launch stamp. Every warning or F-xx line goes VERBATIM into the plan-confirmation mail.
- **Pane and identity.** Pane check against the brief's pane id, then the identity self-check.
- **Develop.** In SEPARATE calls: `git ls-remote origin refs/heads/develop` (key and keepalive via `-c core.sshCommand=...`, `GIT_SSH_COMMAND` unset), compared to the sha in WEDNESDAY'S NOTE and to `d7691f353122`.
- **Open PRs.** The open-PR list (`gh pr list` from your launcher shell and `git ls-remote origin 'refs/pull/*/head'`) against your file set (PARTITION), with a planted control (a file list that DOES contain `Blockchain/Dev/services/auth/src/routes/auth.ts`; if the control fails the zero means nothing). The screen said auth PRs touched only `routes/users.ts` and one ks1006 test: re-read, do not trust.
- **Existing branches.** `git ls-remote origin 'refs/heads/*'` filtered for `ks-1885`, `ks-1791` and `ks-1868`, with a positive control. A branch for KS-1885 that already exists is a STOP and a mail.
- **Re-read the ticket.** KS-1885 and KS 1791 and KS 1868 (read-only Linear, `comments(first:50)` sorted client-side). **Read the KS-1885 body whole before you design anything; its acceptance criteria win.** A newer comment from Kam or Wednesday with a ruling or a question is a STOP and a QUESTION.
- **Rulings.** Run `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` and report every card dated after 2026-10-31 that names auth, social, sign-in, callback, token, error echo, detail, or the push gate.
- **Worktree (Seat R 70th's method).** The develop pin may not be in the shared object store, and you never fetch into the shared checkout. Make ONE `--shared` base clone at a path you assert NON-EXISTENT first, under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/` (suggested `.../worktrees/s-s10-base`), then your working tree from it at the develop sha you read. Never reuse another seat's directory. Never plant a control directory in the shared `worktrees/` directory. Record the paths.
  - Branch: Linear's suggested name for KS-1885, copied from the ticket, with `git ls-remote origin 'refs/heads/feature/ks-18*'` asserted to show none of yours at creation.
- **Install.**
  - `npm ci --ignore-scripts`; `npm run build --workspace=packages/shared`; assert `packages/shared/dist/index.js`.
  - `bash scripts/preflight/deps-present.sh` AND `... --self-test`, both rc 0.
  - `npm ci --ignore-scripts` in every `systemTest/*` dir enumerated from `git ls-tree` (refuse on 0).
  - `git config core.hooksPath .githooks` read back; identity pinned per command and read back from the commit.
  - A short private `TMPDIR` such as `/tmp/s10`.
- **Commit, PR title and body.**
  - Commit subjects and PR titles start with the ticket's real full key copied from the branch name, `Refs KS-1885: ...`. Never a placeholder, never a Conventional Commits `type(scope):` prefix (KS-1878; STANDING_LINES).
  - **The commit-subject check STOPS the chain above 92 characters.** Measure the subject (`printf %s "$subj" | wc -c`) before you commit, and keep it at or below 92.
  - Your own ticket is `Refs KS-1885`, hyphenated, never `Closes`. Every other ticket id is written "KS 1234" with a space (KS 1791, KS 1868, KS 1410 and so on).
  - **The PR body is script-checked BEFORE the PR is created** (hyphenated foreign keys, `Refs` line, the required sections). Run your checker on the body file, show its rc, and only then create the PR.

### ITEM A. Plan confirmation (a QUESTION mail, topic `plan confirmation`, to `wednesday-agent@agentmail.to`, subject starting `[Secuura/Blockchain-S -> Wednesday]`, body line 1 `Seat S 10th`)
It carries:
- the launcher warnings verbatim;
- your re-read of the callback at your pin (file:line, what the 400 body carries today, which errors reach it);
- the acceptance criteria of KS-1885, quoted;
- **the trace of the callers, which you do yourself:** who consumes the `detail` field (the web client, the extranet, any test, any doc, `systemTest/**`, the OpenAPI source). A client that reads `detail` and would now see a constant is named. Do not rely on the screener's "no external input".
- your design: what is logged (and that the log line itself does not carry the token: a logger meta that includes the raw message just moves the leak to the log), what the constant is, and whether the status code changes (default: it does not);
- **the sweep list:** every other `detail:` and `.message` echo in `services/auth/src/routes/auth.ts`, by line, each marked IN SCOPE (KS 1868 / KS-1885 covers it, fixed in this PR) or CANDIDATE (not covered, in your mail only);
- the cell matrix with a proposed mutant for EVERY cell.

### ITEM B. The PR
- **Red-first.** Show every cell RED at the untouched base before the fix, GREEN after. The decisive cell: an exchange that throws an error whose message contains a sentinel token string (the `fetch` TypeError case, with a newline in `access_token`) must produce a response body that does NOT contain the sentinel, anywhere (assert on the serialised body, not only on `detail`). Cover the providers the screen names (github, google, linkedin, microsoft_personal) and facebook as the control that was not exposed. Use mocked fetch and mocked adapters only: no real provider, no network.
  - A positive control for the sentinel assertion: the same cell run against the base must FAIL, which shows the cell can see a leak.
  - The existing `SyntaxError` path and the success path still answer what they answered before.
  - Run the whole auth suite with ratios (cells of expected, files). Name every red by file and cell. A red you cannot show pre-existing by a control run on develop at your base is a STOP.
  - Run `tsc --noEmit` including test files, eslint on new and changed files, and the repo's own gates.
- **Mutants** (each must PARSE before it runs, kept outside `__tests__` and the test-types ratchet's globs, each sha256-restored, one anchor per replacement asserted to be 1; STANDING_LINES "A TAMPER'S RESTORE NEEDS A UNIQUE ANCHOR"):
  - the constant replaced by the thrown message again (the sentinel cell goes red);
  - the constant replaced by a template that includes `String(exchangeErr)` (the sentinel cell goes red);
  - the log line moved into the response, or the sentinel placed in the log meta only if your design says the log is clean (the log cell goes red);
  - the `SyntaxError` carve-out widened or dropped, if your design keeps one;
  - the status code changed.
  - A multi-clause guard is red-proved by flipping each conjunct separately.
- **Docs in the SAME commit:** ONE fragment pair (flow + cheat) for this PR, per SKILL.md section 4 at your base (WEDNESDAY'S NOTE). Use a unique slug starting `KS-1885-`, no section number, and no edit to the assembled pages. `docs-fragments.mjs check` ends OK, with a planted-defect control on a scratch copy that fails.
  - If the auth OpenAPI source (`services/auth/src/auth.openapi.ts`) declares this response, say whether it needs the change and make it in the same commit only if the repo's spec gate requires it. `services/auth/**` beyond `routes/auth.ts` is otherwise not yours: if the spec gate forces a second auth file, STOP and mail.

### ITEM C. Open it, READY FOR GATE
- Open the PR (`Refs`, never `Closes`).
- **Gate notes go into the PR body by PATCH only.** Once the PR exists, NO further push for notes: edit the body by the API (PATCH), read it back, and re-run the body checker on the result. A push after the PR exists is for a code change only, by Wednesday's word.
- Post ONE facts-only comment on the ticket naming the PR (no `@` mention; read back by comment id). Change no ticket's state or assignee.
- READY FOR GATE means the five artefacts below (HOLDS) by identifier, plus what was NOT done.
- In the PR body, under "Before this deploys":
  - Nothing deploys from this seat.
  - Name the exact callers who succeed today and would see a changed body: any client that reads `detail` from the social callback's 400 (from your caller trace).
  - No comms to Platform S or to Peter or Stuart is yours.
- Mail Wednesday after the PR, then the HANDOVER, the history entry and the wrap mail.

## PARTITION (seats share one inbox, `secuura-blockchain@`, so every mail names "Seat S 10th" on body line 1 and uses your own row tag `[Secuura/Blockchain-S -> Wednesday]`)
**YOURS, write** (all under `Blockchain/Dev/` in `Secuura/Distributed_Secuura`):
- `services/auth/src/routes/auth.ts` (the social callback's error path, and any other echo in this file that KS 1868 / KS-1885 scope covers, per your sweep).
- New `services/auth/src/__tests__/ks1885-*.test.ts` (one or two files).
- Your one fragment pair under `Projects Documents/fragments/flow/` and `.../cheat/` (per ITEM B); your worktrees and the record folder `5_Project_History/2026-11-01_seatS-10th/`.
- `git diff --name-only` against the merge-base (three dots) shows only these. No migration, no manifest or lockfile, no `docker-compose.yml`, no deploy files.

**READ-ONLY to you:** `services/auth/src/providers/social/**` (the screen says no edit needed; if you find one is needed, STOP and mail), `services/auth/src/routes/users.ts` and every other file in `services/auth/**` not named above, `services/originate/**`, `services/anchoring/**`, `services/security/**`, `services/mcp-server/**` (Seat E 24th's lane if launched), `docs/**`, `migrations/`, `deployment/`, `systemTest/**`, every `package.json` and lockfile, `services/api-gateway/src/middleware/auth.ts`, all other services, and `packages/shared/**`.

**Live seats and held files at drafting:** Seat R 71st holds the demo-service `persona.ts`, `governanceService.ts` and the nft-certificate `minting.service.ts`; none is yours. Seat E 24th (mcp-server) may launch in parallel; none of its files is yours.

**Open PRs:** the screener read 19 open PRs, 60 distinct files, at 2026-11-01 21:27, and none of the candidate files was among them (the auth PRs touched only `routes/users.ts` and one ks1006 test). Re-run the overlap yourself before each push with a planted control.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Card `secuura-wednesday-go-counts-as-kams-word-1030` = a (start authority, above).
- Kam 2026-11-01 21:27 and 21:32, verbatim quotes in WEDNESDAY'S NOTE.
- Every other ruled `secuura-` card without a delivered mark concerns other work; any that bears on KS-1885 you name in your plan confirmation (your ITEM 0 rulings read).

## HOLDS (the standing lines, carried from `STANDING_LINES.md`; sections cited by name: READY FOR QA, INSTRUMENTS, HOLDS that go in every brief, Repo-specific Secuura/Blockchain, A VERDICT LINE IS A CLAIM ABOUT WHAT RAN, WHAT DID MY BRANCH CHANGE IS A THREE-DOT QUESTION, A TAMPER'S RESTORE NEEDS A UNIQUE ANCHOR, TOUCHING A FILE THAT WAS REPAIRED IN THE LAST DAY, a multi-clause guard is red-proved per conjunct)
- **Signature classes pause for Kam, always:** production, money, external communication to any human, anything irreversible.
  - **Mocks only: no request against any real identity provider, database, box or tenant.** Never use or echo a real token; the sentinel is a made-up string.
  - No `az`, no deploy, no `--admin`, no `--no-verify`, no force push (`.githooks/pre-push` refuses a non-fast-forward; catch up by MERGING develop in, never rebasing a pushed branch).
  - Never read, echo or copy a secret or open a `.env`. A gate that stops you is a question it is asking.
- **Kam, 2026-09-11 16:56, verbatim:** "For the time being, I / you will approve our own elements" and "FIx and merge all tickets after they are tested". We merge our own TESTED K work after the QA gate, on Wednesday's head-pinned GO. **You do not merge.** The deploy grant belongs to the separate Opus deploy seat, not to you.
- **Client-facing communication is TICKET COMMENTS only,** BLUF-first, facts only. The extranet is INPUT ONLY. **No comment to, and no `@` mention of, Peter or Stuart; nobody else messages them.**
- **Filing:** you file NOTHING. Candidates go in your mail. Search the board by SYMBOL and path first and say what you searched. Filings carry an ASSIGNEE: our board account (`kamil.kreiser@secuura.ai`). You change no ticket's state.
- **Assignment:** read KS-1885's assignee at ITEM 0; a ticket on Peter or Stuart stays theirs and is a STOP.
- **Ticket-comment channel:** the only comment you post is the facts-only READY comment naming the PR, read back by comment id. Anything else goes in your mail to Wednesday.
- **READY FOR GATE means five things EXIST and are named by identifier:** the PR number; its head sha read from origin in the same action as writing the sentence; the ticket comment naming the PR; the Test Evidence block in the PR body, written by you; what was NOT done or NOT covered. A branch is not a PR.
- **Docs rule:** test changes ship with their fragment pair in the same commit (SKILL.md section 4; WEDNESDAY'S NOTE).
- **Forward-move rule (every Secuura build or raise brief carries this line):** a forward move of develop is ACCEPTED when your base is an ancestor of the new develop (read by `ls-remote`), its objects are present, and the ONLY paths shared between the moved range and your branch are your own fragment files (with unique fragment names, normally none); then merge the new develop in (never rebase a pushed branch), re-run `docs-fragments.mjs check` with a planted defect, and push. Any shared CODE path means stop and mail.
- **Commit subjects and PR titles start with the ticket's real, full key** (KS-1878), at most 92 characters. No placeholder, no Conventional Commits prefix. Foreign keys are spaced ("KS 1791").
- **Trace the callers yourself.** A caller list, a "no other consumer" claim, or a "not in an open PR" line from the screener, the ticket or this brief is a lead, not a fact. Read the consumers and say what you ran.
- **Boot pull:** the launcher's step-1 pull may fast-forward the shared develop refs; RECORD it. After boot: no fetch or pull in the shared checkout and no write to either develop ref.
- **Partition from both sides, kill only your own PIDs** (by recorded PID, never `pkill`/`killall` by name). A throwaway database or container you start is removed by its recorded id (none is expected; the tests are mocked).
- **Clone into a NON-EXISTENT path:** any scratch clone is made into a path asserted absent first. Read origin with `ls-remote`, never `origin/develop`; read repo files from a sha or your own worktree, never from the Secuura MAIN checkout's working tree.
- **Mail discipline:** every mail names `Seat S 10th` on body line 1, subject starts `[Secuura/Blockchain -> Wednesday]` (your lane tag `Secuura/Blockchain-S]` is also accepted), goes only to `wednesday-agent@agentmail.to` (no cc, no secrets). Never put stop, hold, hand over or checkpoint in a SUBJECT. A QUESTION mail is for a blocker only (Context, one Question, Meanwhile, Needed-by).
  - After ~15 minutes with no ANSWER proceed on the safest reading UNLESS approval-class. Any widening of who may call a route, any change to `packages/shared`, and any change that alters the status code or the shape of an auth response a client depends on is approval-class: ask.
  - **An inbox watcher exits on its first match.** Arm every watcher at the maximum background timeout (7200000 ms); SINCE = the timestamp of the newest mail you READ; after it fires, re-arm it with the new SINCE before you do anything else, or you are deaf.
- **Shared inbox:** act only on mail naming `Seat S 10th`; a GO is acted on only when its subject names your number. A mail naming another seat (S 9th, R 71st, E 24th, T, F, V, U, W and any predecessor S seat) is not yours. Prove your matcher on real subjects of other seats and of Seat S 9th, with your own subject as the control.
- **Instruments:** redirect to a file and read the file (`cmd > out 2>&1; rc=$?`), exit codes on their own line. macOS has no `timeout`. The Bash tool is zsh (`$pipestatus[1]`, an unmatched glob aborts the command). A `pgrep -f` pattern matches your own command line. Use `/usr/bin/grep -i` with a positive control beside every zero. A pass line carries a RATIO (`13/13 legs ran`). A skip is not a pass. A verdict that prints "0 checked" is a FAIL. A mutant must parse before it runs.
- **Git:** to ask what YOUR branch changed use three dots or the merge-base, never `X..HEAD`. A hyphenated foreign key in a PR title, body or commit message ATTACHES the PR to that ticket (space it).
- **PUSH TRANSPORT and queue:**
  - If the launcher printed F-02, push with `git -c core.sshCommand="ssh -i <the project's deploy key> -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 -o ServerAliveCountMax=20" push ...`, `GIT_SSH_COMMAND` UNSET. A push's result is the tool's `.rc` plus an `ls-remote` of the ref.
  - Pushes go through the first-come queue (`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/push_queue.sh join "Seat S 10th"`, poll `turn`, your own `mkdir` lock, release holder-then-rmdir, `leave`). Do not hold the queue for more than one push at a time.
  - **No push after the PR exists** except for a code change on Wednesday's word. Gate notes are a body PATCH (ITEM C).
- Never delete (quarantine into a dated folder, record it). Never `cd`; absolute paths only. A short `TMPDIR`. Never end a turn on a "next up" line with nothing running.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation.

## WRAP (scored by Wednesday)
At the real wrap (the PR READY FOR GATE and mailed; or when told):
- A history entry in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` headed `## 2026-11-01 - Seat S 10th` (newest first; duplicate-guard on the DATED HEADING with a control; adjust the date to the real wrap day).
- A HANDOVER in `.../5_Project_History/2026-11-01_seatS-10th/HANDOVER.md`.
- The vault commit and push per the end-of-session skill.
- The wrap mail `[Secuura/Blockchain-S -> Wednesday] Session wrap 2026-11-01` carrying the PR number and head, the fragment slug, the cells and mutants with ratios, the sweep list with each CANDIDATE, the caller trace, what you could not run, and your faults.
- Nothing of yours may be left running at the wrap (a `ps` reading by PID in the same action as the claim).

## UNMEASURED IN THE BRIEF (with the closing instrument)
(a) The drafter ran no test, build, mutant or `tsc`, and did not open `auth.ts`, the ticket, KS 1791's diff or any adapter. Closed by your runs and reads.
(b) Whether any client reads the callback's `detail`. Closed by your caller trace.
(c) Whether the screener's "facebook not exposed" and the four-provider list hold at your pin. Closed by your cells (a provider that differs is reported, not assumed).
(d) Whether the develop pin is in the shared object store. Closed by the base clone at ITEM 0.
(e) The docs shape: closed by Wednesday's note (the fragment scheme is live).

PROVENANCE:
- Seat ordinal: `Seat S 8th` 3, `Seat S 9th` 2, `Seat S 10th` 0 hits (case-insensitive count). The highest found is `Seat S 9th` (its heading `## 2026-10-31 - Seat S 9th` is at history.md line 177), so the next free is `Seat S 10th`. Control: the 8th and 9th counts are non-zero. The seat re-runs this. | `/usr/bin/grep -i -c "Seat S <ordinal>"` over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md, one run per ordinal; heading lines by `grep -n`. Lane S registered at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/launchers.conf:23 | read 2026-11-01
- Develop pin `d7691f35312ea158f043e87a3227e477cccb183d`; the screen states `ls-remote origin develop` equalled it at 21:27 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_board-screen-2127/screen.md line 3 (board screen 21:3x, read by Wednesday; the drafter ran no ls-remote) | read 2026-11-01
- KS-1885 facts: Tier 1; title "Social sign-in callback echoes any exchange error whole"; `GET /api/auth/social/:provider/callback` puts `exchangeErr.message` in the 400 body unless it is a SyntaxError; a newline in access_token makes fetch throw a TypeError containing the token; QA gate 43: github, google, linkedin, microsoft_personal exposed, facebook not; file `services/auth/src/routes/auth.ts` `:1076-1081`; one new test in `services/auth/src/__tests__/`; adapters need no edit; fix shape is the constant-detail pattern KS 1791 used on the same lines | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_board-screen-2127/screen.md, LANE 1 entry, lines 15-17 | read 2026-11-01
- "Not in an open PR (auth PRs touch only routes/users.ts and one ks1006 test)"; 19 open PRs, 60 distinct files, with a positive control reported by the screener | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_board-screen-2127/screen.md lines 13 and 17 | read 2026-11-01
- UNMEASURED by the screener: the adapter list was taken from the ticket text, not re-read in code; no fix, test or mutant was run | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_board-screen-2127/screen.md lines 55-57 | read 2026-11-01
- Live seats and held files (Seat R 71st: persona.ts, governanceService.ts, minting.service.ts; Seat E 24th may launch on mcp-server) | the job statement from Wednesday for this brief; the screen's exclusions line (persona.ts, governanceService.ts, minting.service.ts, KS-1384) at /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_board-screen-2127/screen.md line 14 | read 2026-11-01
- Start authority quotes (card `secuura-wednesday-go-counts-as-kams-word-1030` = a; Kam 21:27 and 21:32 on 2026-11-01) | the job statement from Wednesday for this brief, verbatim; the card itself not re-read by the drafter | read 2026-11-01
- Standing lines carried (docs rule, forward-move rule, KS-1878 commit-subject rule, assignee rule, mail discipline, push queue, instruments) and the brief's structure | copied from the merged-and-scored security-lane brief /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-31_seatS9_ks1881_1871_1860_1861_security.md, read whole; /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md NOT re-read by this drafter | read 2026-11-01

## DRAFTER NOTES
- **Kept from the Seat S 9th brief, on purpose:** the section order (NEW SEAT, WEDNESDAY'S NOTE, BLUF, WHAT I READ, QUEUE, PARTITION, HOLDS, WRAP, UNMEASURED, PROVENANCE) because it scored 0.95; the whole HOLDS block (signature classes, Kam's 2026-09-11 quote, comments-only client channel, no filing, five READY artefacts, forward-move rule, KS-1878 subject rule, mail discipline, shared-inbox matcher, instruments, git three-dot rule, push queue and F-02 transport); the mutant discipline (parse first, sha256 restore, unique anchor, per-conjunct); the docs-in-same-commit rule; the PARTITION shape with a planted overlap control; the PROVENANCE line format.
- **Cut:** everything specific to the four S 9th tickets (gateway role gate, tenant design tickets, option-set mails, three more PRs, D1/D2, the Seat R 66th branch and #1843 collision). Only one PR, so "each PR" and the order-of-PRs logic are gone.
- **Added from today's lessons:** the 92-character subject check, the pre-creation script check of the PR body, gate notes by PATCH only with no push after the PR exists, the single-match watcher with re-arm, and "trace the callers yourself" (as a plan-confirmation item and as a HOLD).
- **Changed on purpose:** the docs hold is not carried as a standing fact. It dated 2026-10-31 and may have lifted, so Wednesday states the docs shape at send, with a safe default (copy the newest merged PR's shape). Worktree method follows the job statement (Seat R 70th's one `--shared` base clone); the drafter did not read R 70th's own record, so the clone steps are stated generically.
- **Left to the seat deliberately:** the exact fix design, the constant string, and the status code (default: unchanged). The drafter opened none of `auth.ts`, the ticket body or KS 1791.
- **Unverified by the drafter:** the screener's line numbers, the provider list, and "not in an open PR". I read only the screen's LANE 1 entry and its UNMEASURED section, and the brief says so.
- **No SELF-CHECK line**, as instructed.

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-01 21:37
