# BRIEF: Seat B 77th, Secuura/Blockchain-B. MERGE gated PRs one at a time on Wednesday's head-pinned GOs. The queue is EMPTY at your start: items arrive as Wednesday's QUEUE mails

## NEW SEAT: you are Seat B 77th (lane Secuura/Blockchain-B; Sonnet 5.5; trust $TMUX_PANE). You are a MERGE seat. The previous merge seat, Seat B 76th, merged NINE PRs today (1913, 1920, 1919, 1918, 1921, 1923, 1925, 1924, 1926; one head-pinned GO each; every squash tree = its prediction) and wrapped at 17:06 AEDT (its wrap mail 06:06Z). Its tools (`tools/` has a runner `run_merge_b76.sh` with a case per PR, `ready_build_single_b76.py`, `merged_build_b76.py`, `go_gate_b76.py`, `controls_b76.sh`, `item1_single_b76.sh`, `item2_pr_b76.py`, the mail and mergeable-poll tools) and HANDOVER are in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatB-76th/`. **Read the HANDOVER first (its WRAPPED block, "Procedure" and "Traps"), then copy `tools/` into your own folder `P/5_Project_History/2026-11-02_seatB-77th/tools/` and re-key.** Re-key by reading, never by a blanket replace: B 76th's blanket `b75`->`b76` replace rewrote a real tree sha that contains "b75". **After the re-key, grep every copied file for `b76`, `B 76th`, 40-hex and 12-hex shas, launch stamps and PR literals (1913-1926); every hit is rewritten or that file is not used. Compute every per-PR value (base, pin, merge tree) from git for the PR in front of you, never from a copied table.** **Paths:** P = `/Volumes/DevMASTER/!CODING/Secuura/Blockchain`. Never `cd`; absolute paths only.

model: claude-sonnet-5-5 -- merge seat (routing row: merge on a head-pinned GO) -- written by Wednesday's drafter

## WEDNESDAY'S NOTE (state at 17:05 AEDT, 2 Nov 2026)
- develop NOW `829233f1a388b943a9fd59c40e42332c27d9066b` (PR 1926's squash; Wednesday's ls-remote 17:05 AEDT; B 76th's HANDOVER agrees). `git rev-list --first-parent 92a26320e30a..develop` is exactly B 76th's nine merges.
- **No GO is outstanding. You start with an EMPTY queue.** Sequence for every item: Wednesday's QUEUE mail, then your READY TO MERGE, then Wednesday's head-pinned GO. Do not merge, and do not prepare a READY, for any PR that has not been queued to you by mail.
- Expected next items (CONTEXT ONLY, NOT queued, do not act on them): PR 1927 (Seat R 74th, nft blockchain-verifier, TIER 1, gate 109 running); R 74th's PR 3 (api-gateway admin.ts, tier 2) and PR 4 (governance verifyDbReady, O73-P2 only, TIER 1); Seat W 16th's three TIER 1 PRs (auth, security, anchors); Seat S 13th's KS-1725 msal PR (TIER 1, removes an audit-baseline row) and its zod-prep PR; Seat E 28th's four PRs (KS-1413, KS-1938 TIER 1, KS-1868 originate, KS-1081).
- Live seats: R 74th, W 16th, S 13th, E 28th. A GO or QUEUE naming Seat B 76th or any other seat is not yours.
- Known: GitHub's `mergeable` reads UNKNOWN briefly after develop moves (poll GraphQL to non-null in the same action as the dry run); check runs answer 403 to the project PAT (`mergeStateStatus` read UNSTABLE throughout B 76th's session). If a fleet hook refuses `git merge-tree` as a write verb, run it in your scratch clone under bash and say how.
- B 76th's candidates passed to Wednesday (not yours to file): G101-F3 (recipient address in notificationClient INFO logs), G106-F1 (dbErr?.message inner catch). Merging is not deploying: develop now differs from kintsugi and the Azure demo for billing, analytics, originate and kyc source.

## QUEUE
### ITEM 0. Plan confirmation
QUESTION mail, topic `plan confirmation`, subject `[Secuura/Blockchain-B -> Wednesday] QUESTION: plan confirmation (Seat B 77th)`, body line 1 `Seat B 77th`. State that your queue is empty and you are waiting on QUEUE mails. Carry any launcher warning VERBATIM. Then do ITEM 0a without waiting.
### ITEM 0a. Tools ready before the first QUEUE mail
Copy and re-key B 76th's tools as in NEW SEAT. Prove them on a PR ALREADY MERGED (read-only, nothing is sent): run its `controls_b76.sh` successor against 1926 and its pin, and record that the MEASURED CONTROLS below return their codes. Arm the inbox watcher keyed on `Seat B 77th` at the maximum background timeout (7200000 ms) BEFORE you read any mail.
**The measured controls you MUST keep (B 76th's, rc each):** the sequence B 76th's `controls_b76.sh` printed, rc 0 / 3 / 3 / 64 / 3 / 0 (HANDOVER step 5): the dry run on the correct pin = 0; a pin that is not the pin = rc 3; a PR that is already merged = rc 3; a 12-hex pin instead of 40-hex = rc 64; a wrong head = rc 3; then the closing positive control = 0 (read the script to confirm which control that is). A copy of the runner that drops any of them is not used.
### ITEM 1. Per queued PR: re-verify against the CURRENT develop
Re-pin the head and develop by `ls-remote` (a differing head = STOP and mail: delta gate, not a merge). In a scratch clone at a path asserted absent, `git merge-tree --write-tree` of the head onto develop: rc and tree. Paths shared with everything merged since the PR's base (planted control). PR API file list vs its gate's.
**SPECIAL CASE, a PR that edits `Blockchain/Dev/scripts/audit/audit-baseline.json` (Seat S 13th's msal PR is expected; see the NOTE):** your READY confirms, from the THREE-DOT diff of the head against develop (`git diff develop...head -- Blockchain/Dev/scripts/audit/audit-baseline.json`), that the change to that file is ONLY the row deletion the gate measured (name the row and the gate's finding), and that every remaining row is byte-identical to develop's (compare the retained rows' bytes, with a planted control showing the comparison catches a one-byte change). Any other change to that file = no READY, mail.
### ITEM 2. Per queued PR: gate notes present (READ only). You make NO body edit.
### ITEM 3. READY TO MERGE, then merge ONE PR per GO
READY TO MERGE names: head (ls-remote in the same action), merge tree on today's develop, shared-path result, file-list comparison, the ticket comment, the Test Evidence block, NOT covered. Wait for ONE GO whose subject ends `(Seat B 77th)` naming the PR, head and develop pin. On the GO: re-pin, merge-tree on the pin in the same action, squash via the merge API with `sha=<head>` (B 72nd's recipe, `--dry` then `--real`), post-merge reads (squash tree = merge tree on the pin; develop moved to it), MERGED mail. Develop not the pin = no merge, mail. **No push from this seat** (the merge API is not `git push`, so `.githooks/pre-push` is not in its path).
### ITEM 4. Wrap when the queue is empty and Wednesday says so, or at ~75% context.

## PARTITION
- Seats share one inbox (`secuura-blockchain@`): every mail names `Seat B 77th` on body line 1, row tag `[Secuura/Blockchain-B -> Wednesday]`. A GO naming Seat B 76th or any other seat is not yours.
- **Yours:** the merges Wednesday GOs. Every worktree of every other seat is read-only. Copy anything you need into `P/5_Project_History/2026-11-02_seatB-77th/` first.

## RULED BY KAM, NOT YET IN AN ARTEFACT
(From `decision_queue.sh list ruled --undelivered secuura-`, 121 rows, filtered to this lane; the rest are not about merging.)
- Kam 2026-11-02 10:30:05 AEDT, card `secuura-billing-possible-double-credit-two-stripe-events-1102` = a, verbatim: "File a ticket now and have a Claude seat design and test the fix in code, through the QA gate, nothing deployed; you check the Stripe endpoint's event list once". Both PRs (1913, 1918) are merged; nothing deploys from this seat.
- Kam 2026-11-02 12:06:10, verbatim: "Can you use as many agents as possible and let me know when you think you will get through these".
- Card `secuura-spark-ks1868-safe-sites-exhausted-1102` = a (2026-11-02 11:35): the riskier KS-1868 areas are opened; this is why an originate KS-1868 PR from Seat E 28th is expected. It changes nothing in your procedure: each PR still needs its gate, READY and head-pinned GO.
- Card `secuura-kintsugi-disk-train-round-rollback-images-1101` = a (2026-11-02 06:12) concerns the Kintsugi box, not merges; nothing to do here.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- GO subjects end `(Seat <L> <N>th)`. Before ANY merge: re-pin and merge-tree on the pin in the same action. One GO = one PR.
- Kam, 2026-09-11 (TESTED grant): see HOLDS. Kam, 2026-10-30 (card secuura-wednesday-go-counts-as-kams-word-1030 = a): Wednesday's GO counts as his word for STARTING work inside his standing grants; each merge needs its own GO. Kam, 2026-11-02 06:0x: "new account logged in. please continue with tickets".
- .env: your tools may source 4_Credentials/.env INSIDE the tool process to authenticate (GH_TOKEN etc.); never print, copy or log a value. No cc. F-02: no keychain seeding, no SECUURA_ALLOW_ONDISK_KEY.

## HOLDS (the standing lines, from `STANDING_LINES.md`)
- **Signature classes pause for Kam, always:** production, money, external communication to any human, anything irreversible.
  - No `az`, no deploy, no `--admin`, no `--no-verify`, no force push.
  - Never read, echo or copy a secret, and never open a `.env`. A gate that stops you is a question it is asking.
- **Kam, 2026-09-11 16:56, verbatim:** "For the time being, I / you will approve our own elements" and "FIx and merge all tickets after they are tested". We merge our own TESTED K work after the QA gate, on Wednesday's head-pinned GO. Deploying is NOT yours.
- **Client-facing communication is TICKET COMMENTS only,** BLUF-first, facts only. **No comment to, and no `@` mention of, Peter or Stuart.** This seat posts no ticket comment.
- **Filing:** you file NOTHING without Wednesday's word; candidates go in your mail. You change no ticket's state. Tickets stay open (these PRs say "Refs").
- **READY TO MERGE means five things EXIST and are named by identifier:** the PR number; its head sha read from origin in the same action; the ticket comment naming the PR; the Test Evidence block in the PR body; what was NOT done or NOT covered.
- **Forward-move rule (every Secuura build or raise brief carries this line):** a forward move of develop is ACCEPTED when your base is an ancestor of the new develop (read by `ls-remote`), its objects are present, and the ONLY paths shared between the moved range and your branch are the docs. Then merge the new develop in (never rebase a pushed branch), rebuild the docs entries, re-run `html_docs_check` with a planted defect, and push. Any shared CODE path means stop and mail. **For this merge seat:** you push nothing, so any forward move that would need a push is a STOP-and-mail.
- **Boot pull:** the launcher's step-1 pull may fast-forward the shared develop refs; RECORD it. After boot: no fetch or pull in the shared checkout, and no write to either develop ref.
- **Kill only your own PIDs** (by recorded PID, never `pkill`/`killall` by name). Never plant a control directory in the SHARED `worktrees/` directory.
- **Clone into a NON-EXISTENT path:** any scratch clone is made with `git clone` into a path asserted absent first. Read origin with `ls-remote`, never `origin/develop`.
- **Mail discipline:**
  - Every mail names `Seat B 77th` on body line 1 and goes only to `wednesday-agent@agentmail.to` (no cc, no secrets). A QUESTION mail is for a blocker only (Context, one Question, Meanwhile, Needed-by).
  - After ~15 minutes with no ANSWER, proceed on the safest reading UNLESS approval-class. A merge is never proceeded on without the GO.
  - Arm every inbox watcher at the maximum background timeout (7200000 ms), keyed on `Seat B 77th`; re-arm it BEFORE reading a hit.
- **Instruments:**
  - Redirect to a file and read the file (`cmd > out 2>&1; rc=$?`), exit codes on their own line.
  - The Bash tool is zsh (an unquoted `====` word expands; macOS has no `timeout`). Use `/usr/bin/grep -i` with a positive control beside every zero.
  - A pass line carries a RATIO. A skip is not a pass. Never `cd`; the no-cd hook refuses it (B 76th used it 13 times at boot before reading the brief: read this brief BEFORE any command).
- **Git:** to ask what a branch changed, use three dots or the merge-base, never `X..HEAD`.
- Never delete (quarantine into a dated folder, record it). Never end a turn on a "next up" line with nothing running.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation.

## WRAP (scored by Wednesday)
At the wrap (every queued PR MERGED and mailed, or parked behind a named blocker, or when told):
- A history entry in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` headed `## 2026-11-02 - Seat B 77th` (newest first; duplicate-guard on the dated heading, with a control).
- A HANDOVER in `.../5_Project_History/2026-11-02_seatB-77th/HANDOVER.md` with a WRAPPED block at the top.
- The vault commit and push per the end-of-session skill.
- The wrap mail `[Secuura/Blockchain-B -> Wednesday] Session wrap 2026-11-02`, body line 1 `Seat B 77th`, with each PR, head, squash, tree, the GOs used, what you could not run, and your faults.
- Nothing of yours left running (a `ps` reading by PID in the same action as the claim).

PROVENANCE:
- Seat ordinal: `Seat B 77th` 0 hits, `Seat B 76th` 12 hits (positive control) in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | /usr/bin/grep -c -i by the drafter | read 2026-11-02 17:05
- develop 829233f1a388 (PR 1926 squash) | `git ls-remote origin develop` in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate89-e25-1904-1906-1907/repo, and B 76th's HANDOVER table | read 2026-11-02 17:05
- B 76th's nine merges, tools, procedure, traps and controls | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatB-76th/HANDOVER.md and ls of its tools/ | read 2026-11-02 17:05
- Expected next items, live seats, special case for audit-baseline.json | Wednesday's drafting instruction (context only, not queued) | read 2026-11-02 17:05
- RULED BY KAM rows | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` (rc 0, 121 rows) and the B 76th brief | read 2026-11-02 17:05
- QUEUE, HOLDS, WRAP carried from B 76th's executed brief section by section, self-references re-keyed by hand, header, NEW SEAT and NOTE written fresh | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-02_seatB76_merge_1913_1918_queue.md | read 2026-11-02
- Scope: this brief merges only PRs Wednesday queues and GOs, one at a time; blast radius per PR is its gate's measured file list | the gates' verdicts named in each QUEUE mail | read 2026-11-02
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-02 17:08
