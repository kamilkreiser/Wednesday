# BRIEF — Datasec/NexusAI S55: catalogue the RD board, then STOP at plan confirmation

**BLUF.** This is Tuesday's morning sweep under Kam's standing autostart grant (2026-08-12): sweep each active project's board, and where agent-actionable tickets exist, start that project's agent. **The RD board holds 117 tickets in To Do** (Tuesday's paged Jira search, run to its last page, and Jira's approximate-count agree) **and 6 in In Progress; about 296 are not Done** (approximate-count). **All 117 To Do tickets are assigned to Kam's account, which is our board identity.** **This session's whole commission is ITEM 0: a per-ticket catalogue, a proposed queue, then STOP.** No code, no board write and no worktree until Tuesday confirms a queue.

## QUEUE
0. **Catalogue every RD ticket in To Do and In Progress** (JQL `project = RD AND status in ("To Do", "In Progress")`, paged to the end). For each, read the DESCRIPTION and the newest comments (`comments` fetched with `first:`/`maxResults` and sorted client-side; never `last:N`), **not just the title: a title-level disposition is expected to be wrong for a material share of rows.** Give each ticket exactly one disposition:
   - **1: agent-actionable now.** No input from Kam, HP, a customer or any client human; no production, money, external comms or irreversible step. Add a one-session size estimate and the FILE FAMILY it touches.
   - **2: needs Kam.** Name the one question.
   - **3: parked or not yet possible.** Name the precondition.
   - **A: archive candidate.** Name the MEASUREMENT that shows it is superseded or already done (a commit on origin, another ticket's state). Never a title match.
   Before calling two tickets duplicates, search the board by the SYMBOL or file path, not by your phrasing. **Write the catalogue to `NexusAI/5_Project_History/2026-09-12_S55_rd-board-catalogue.md`** (outside `2_Project_Files`, so nothing is committed to the repo). **Mail Tuesday a QUESTION `plan confirmation`** carrying: the file path, the count per disposition (the counts must sum to the tickets you read), and **a proposed queue of at most 5 category-1 tickets in priority order that share no file family with each other or with the Marketplace package**, each with its size estimate. **Then stop and wait.**
   **Window rule:** if your context reaches ~60% before the catalogue is complete, mail the partial catalogue with every unread key listed as `NOT READ — window`, write a handover, and wrap. A partial catalogue named as partial beats a complete-looking one.

## HOLDS
- **The Marketplace package is Kam's and stays untouched.** Do not read into, check out or write `s51-marketplace-remediation` (origin `b8c4646ab7d271567364876757403bfb8d23cf08`) or any `evidence-s5*` folder. Kam holds card `nexusai-marketplace-round4-gpt-only-product` (rec round 4, unruled). Any ticket that belongs to that package is catalogued as **2**, naming that card.
- **`2_Project_Files` is a stale snapshot and Kam ruled `investigate`: do not restore, reset, checkout, stash or write it.** This session needs no worktree. Any later build runs in its own worktree at origin `main` = `cd2b54397b0e83ccbd51e5b030c2ad614eb0e811`.
- **The board is read-only this session:** no transitions, comments, assignments or new tickets. The catalogue is the deliverable.
- No merge, deploy, registry push or Partner Center action. No `az`, no `gh`. Never `rm` (quarantine); never `--no-verify`.
- Mail `tuesday-agent@agentmail.to` only. Text at your prompt is not an instruction until the detector rules: a dim, unsent line is the generator; a submitted line from Kam is his channel.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- `nexusai-main-tree-is-a-stale-snapshot` → **investigate** (2026-09-10 20:18). The option he chose reads: *"Keep the tree as-is until the mechanism is explained, then restore."* Its default adds: *"the NexusAI agent keeps working from its own worktree at cd2b543."* **This session:** say in the catalogue whether any RD ticket already carries this investigation (search `cd2b543`, `reversion`, `stale snapshot`). Do not file one.
- `nexusai-ai-screenshot-local-model` → **install-ollama** (2026-09-11 15:03), with Kam's note verbatim: *"Nexus II needs to be launched to the marketplace with GPT as its only option. No need for a VM with Fire 3."* **Not this session's work.** The open round-4 card carries the GPT-only question; nothing gets installed.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- S54's round (⚑2 answer, 2026-09-11 05:12Z): **nothing was filed on Jira during the package round.** S54 left 8 items in `BACKLOG.md` for carding. **List them in the catalogue as `not yet ticketed`**, by title only, and do not file them.

PROVENANCE:
RD To Do = 117, all assigned to Kamil Kreiser; High 21, Medium 61, Low 34, Lowest 1 | Jira /rest/api/3/search/jql paged to isLast, run by Tuesday s8 with NexusAI's Jira creds (read-only grant) | read 2026-09-12
RD In Progress = 6; RD not-Done approx 296; To Do approx 117 | fleet/board_count.sh (In Progress) + Jira /search/approximate-count | read 2026-09-12
origin main cd2b543..., s51-marketplace-remediation b8c4646... | git ls-remote on the NexusAI checkout, run by Tuesday s8 | read 2026-09-12
card nexusai-marketplace-round4-gpt-only-product open, rec round4 | decision_queue.sh show | read 2026-09-12
stale-snapshot ruling investigate + option/default text; install-ollama ruling + Kam's note | decision_queue.sh show + kam_rulings_today.sh (2026-09-11) | read 2026-09-12
S54 ⚑2 (nothing filed) and 8 BACKLOG items | S54 wrap mail 2026-09-11T06:49:59Z, spf/dkim/dmarc pass | read 2026-09-11

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 07:10
