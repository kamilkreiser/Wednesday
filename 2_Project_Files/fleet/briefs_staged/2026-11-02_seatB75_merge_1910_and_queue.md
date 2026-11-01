# BRIEF: Seat B 75th, Secuura/Blockchain-B. MERGE gated PRs one at a time on Wednesday's head-pinned GOs: first PR 1910 (KS-1868 mcp-server), then each queue item Wednesday sends

## NEW SEAT: you are Seat B 75th (lane Secuura/Blockchain-B; Sonnet 5.5; trust $TMUX_PANE). You are a MERGE seat. The previous merge seat, Seat B 75th, merged FIVE PRs this morning (1904, 1906, 1905, 1908, 1907; every squash tree = its prediction; scored 0.95) and wrapped at 19:54Z; its tools (run_merge_b75.sh and the merge, mergeable poll, item1, GO-auth from authentication_results, chain-proof and behaviour-run tools) are in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatB-75th/tools/`: copy into your own folder and re-key to `_b75`. Read its HANDOVER first. **After the re-key, grep every copied file for hard-coded 40-hex/12-hex shas, launch stamps and PR numbers (1904, 1905, 1906, 1907, 1908) as well as names:** raise seats found this morning that a re-key carries a previous seat's develop pin and stamp assertions invisibly. **Paths in this brief:** P = `/Volumes/DevMASTER/!CODING/Secuura/Blockchain`. Never `cd`; absolute paths only.

## BLUF
- develop NOW `03977e89a343ad7362760e4fb0270602fb6da5ce` (Wednesday's ls-remote 06:52 AEDT; every seat's and operator's read since agrees). Kam 2026-11-02 ~06:0x, verbatim: "new account logged in.  please continue with tickets"; ~07:0x: "carry on with the plan and please make sure the spark is 100% busy or as close as possible".
- **PR 1910** (KS-1868, services/mcp-server/src/http-server.ts nine route catches, tier 2), author Seat V 14th. Head `9f00640d134b` (V 14th's READY mail; re-pin the full sha by ls-remote). Gate 92 (Sonnet) = **GO WITH NOTES, nothing fix-before-merge** (verdict `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate92-ks1868-pr1910/verdict.md`; develop = its merge-base, so the merge tree should equal the head tree). V 14th is PATCHing gate 92's notes into the body now: check for them in ITEM 2; if absent at your READY, say so and do not merge.
- NOT YET (each gets a queue item when cleared): PR 1909 (E 26th, gate 91 GO WITH NOTES; a test-only forward push F1+F3 is coming, then Wednesday's delta check), PR 1911 (E 26th, auth TIER 1, gate 93 Opus running), and PRs from Seats F 21st (billing, TIER 1), S 11th (security, TIER 1), U 8th (four PRs) as they are gated.
- Known: GitHub's `mergeable` reads UNKNOWN briefly after develop moves (poll GraphQL to non-null in the same action as the dry run); check runs answer 403 to the project PAT. A fleet hook may refuse `git merge-tree` as a write verb in some shells (gate 92 met it): if so, run it in your scratch clone under bash and say how.

## QUEUE
### ITEM 0. Plan confirmation
QUESTION mail, topic `plan confirmation`, subject `[Secuura/Blockchain-B -> Wednesday] QUESTION: plan confirmation (Seat B 75th)`, body line 1 `Seat B 75th`. Carry any launcher warning VERBATIM. Then start ITEMS 1-2 (read-only) without waiting.
### ITEM 1. Re-verify against the CURRENT develop
Re-pin the head and develop by `ls-remote` (a differing head = STOP and mail: delta gate, not a merge). In a scratch clone at a path asserted absent, `git merge-tree --write-tree` of the head onto develop: rc and tree. Paths shared with everything merged since the PR's base (planted control). PR API file list vs its gate's.
### ITEM 2. Gate notes present (READ only). You make NO body edit.
### ITEM 3. READY TO MERGE, then merge ONE PR per GO
READY TO MERGE names: head (ls-remote in the same action), merge tree on today's develop, shared-path result, file-list comparison, the ticket comment, the Test Evidence block, NOT covered. Wait for ONE GO whose subject ends `(Seat B 75th)` naming the PR, head and develop pin. On the GO: re-pin, merge-tree on the pin in the same action, squash via the merge API with `sha=<head>` (B 72nd's recipe, `--dry` then `--real`), post-merge reads (squash tree = merge tree on the pin; develop moved to it), MERGED mail. Develop not the pin = no merge, mail. **No push from this seat** (the merge API is not `git push`, so `.githooks/pre-push` is not in its path).
### ITEM 4. Wrap when the queue is empty and Wednesday says so, or at ~75% context.

## PARTITION
- Seats share one inbox (`secuura-blockchain@`): every mail names `Seat B 75th` on body line 1, row tag `[Secuura/Blockchain-B -> Wednesday]`. A GO naming Seat B 74th or any other seat is not yours.
- **Yours:** the merges Wednesday GOs. Every worktree of every other seat is read-only. Copy anything you need into `P/5_Project_History/2026-11-02_seatB-75th/` first.

## RULED BY KAM, NOT YET IN AN ARTEFACT
(none that bind a merge seat. Kam 2026-11-02 ~06:0x, verbatim: "new account logged in.  please continue with tickets" — the authority for this launch; it changes no hold.)

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- GO subjects end `(Seat <L> <N>th)`. Before ANY merge: re-pin and merge-tree on the pin in the same action. One GO = one PR.
- Kam, 2026-10-30 (card, Wednesday's GO counts as his word for STARTING work inside his standing grants): start ITEMS 0-2 on this brief; each merge needs its own GO.
- .env: your tools may source 4_Credentials/.env INSIDE the tool process to authenticate (GH_TOKEN etc.); never print, copy or log a value (SUPERSEDES "never open a .env" below for that case only). No cc. F-02: no keychain seeding, no SECUURA_ALLOW_ONDISK_KEY.

## HOLDS (the standing lines, from `STANDING_LINES.md`)
- **Signature classes pause for Kam, always:** production, money, external communication to any human, anything irreversible.
  - No `az`, no deploy, no `--admin`, no `--no-verify`, no force push.
  - Never read, echo or copy a secret, and never open a `.env`. A gate that stops you is a question it is asking.
- **Kam, 2026-09-11 16:56, verbatim:** "For the time being, I / you will approve our own elements" and "FIx and merge all tickets after they are tested". We merge our own TESTED K work after the QA gate, on Wednesday's head-pinned GO. Deploying is NOT yours.
- **Client-facing communication is TICKET COMMENTS only,** BLUF-first, facts only. **No comment to, and no `@` mention of, Peter or Stuart.** This seat posts no ticket comment.
- **Filing:** you file NOTHING without Wednesday's word; candidates go in your mail. You change no ticket's state. KS-1868 stays open (these PRs say "Refs").
- **READY TO MERGE means five things EXIST and are named by identifier:** the PR number; its head sha read from origin in the same action; the ticket comment naming the PR; the Test Evidence block in the PR body; what was NOT done or NOT covered.
- **Forward-move rule (every Secuura build or raise brief carries this line):** a forward move of develop is ACCEPTED when your base is an ancestor of the new develop (read by `ls-remote`), its objects are present, and the ONLY paths shared between the moved range and your branch are the docs. Then merge the new develop in (never rebase a pushed branch), rebuild the docs entries, re-run `html_docs_check` with a planted defect, and push. Any shared CODE path means stop and mail. **For this merge seat:** you push nothing, so any forward move that would need a push is a STOP-and-mail.
- **Boot pull:** the launcher's step-1 pull may fast-forward the shared develop refs; RECORD it. After boot: no fetch or pull in the shared checkout, and no write to either develop ref.
- **Kill only your own PIDs** (by recorded PID, never `pkill`/`killall` by name). Never plant a control directory in the SHARED `worktrees/` directory.
- **Clone into a NON-EXISTENT path:** any scratch clone is made with `git clone` into a path asserted absent first. Read origin with `ls-remote`, never `origin/develop`.
- **Mail discipline:**
  - Every mail names `Seat B 75th` on body line 1 and goes only to `wednesday-agent@agentmail.to` (no cc, no secrets). A QUESTION mail is for a blocker only (Context, one Question, Meanwhile, Needed-by).
  - After ~15 minutes with no ANSWER, proceed on the safest reading UNLESS approval-class. A merge is never proceeded on without the GO.
  - Arm every inbox watcher at the maximum background timeout (7200000 ms), keyed on `Seat B 75th`.
- **Instruments:**
  - Redirect to a file and read the file (`cmd > out 2>&1; rc=$?`), exit codes on their own line.
  - The Bash tool is zsh (an unquoted `====` word expands). Use `/usr/bin/grep -i` with a positive control beside every zero.
  - A pass line carries a RATIO. A skip is not a pass. Never `cd`; the no-cd hook refuses it.
- **Git:** to ask what a branch changed, use three dots or the merge-base, never `X..HEAD`.
- Never delete (quarantine into a dated folder, record it). Never end a turn on a "next up" line with nothing running.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation.

## WRAP (scored by Wednesday)
At the wrap (both MERGED and mailed, or parked behind a named blocker, or when told):
- A history entry in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` headed `## 2026-11-02 - Seat B 75th` (newest first; duplicate-guard on the dated heading, with a control).
- A HANDOVER in `.../5_Project_History/2026-11-02_seatB-75th/HANDOVER.md` with a WRAPPED block at the top.
- The vault commit and push per the end-of-session skill.
- The wrap mail `[Secuura/Blockchain-B -> Wednesday] Session wrap 2026-11-02`, with each PR, head, squash, tree, the GOs used, what you could not run, and your faults.
- Nothing of yours left running (a `ps` reading by PID in the same action as the claim).

PROVENANCE:
- Seat ordinal: `Seat B 75th` 0 hits, `Seat B 74th` 3 hits (control) in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | Wednesday's /usr/bin/grep -c -i | read 2026-11-02
- develop 03977e89a343 | Wednesday's git ls-remote of origin's develop branch, run in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate89-e25-1904-1906-1907/repo at 06:52:37 AEDT, and gate 92's START/END reads | read 2026-11-02
- PR 1910 head 9f00640d134b, author Seat V 14th | V 14th's READY FOR GATE mail 20:52Z and gate 92's START/END ls-remote | read 2026-11-02
- Gate 92 = GO WITH NOTES, nothing fix-before-merge, tier 2 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate92-ks1868-pr1910/verdict.md | read 2026-11-02
- KS-1868 state (In Progress, Low, on the board account; umbrella, 'Refs' only; scope: this brief merges one PR narrowed to nine catches in mcp-server http-server.ts) | Linear ticket KS-1868 as read by Seat S 11th at its boot (plan confirmation 20:43Z) | read 2026-11-02
- B 74th's tools, HANDOVER and score | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatB-74th/ and /Volumes/DevMASTER/WEDNESDAY/0_Brain/projects_index/scoreboard.md | read 2026-11-02
- QUEUE, PARTITION, HOLDS, WRAP carried from B 74th's executed brief, re-keyed, grepped for B 74th's state | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-02_seatB74_merge_1904_1906_and_queue.md | read 2026-11-02

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-02 08:50
