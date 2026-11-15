# Commission: SECUURA BOARD SCREEN for parallel build lanes, 2026-11-15 14:1x AEDT

Commissioned by Wednesday. Kam, terminal 2026-11-15, verbatim: "also, please work through as many secuura tickets as you can". Read-only: write ONLY `screen.md` and `notes.md` in THIS folder (scratch files here are fine; any git clone in a subfolder whose name contains `_work`). Nothing posted, mailed, moved, commented, pushed or written to Linear or GitHub. Never write inside any `/Volumes/DevMASTER/!CODING` checkout. No `cd`, no `rm` (hooks refuse both); absolute paths; bound every listing with `| head -N`; never print a secret or .env value (source keys inside a python process: Linear key LINEAR_API_KEY in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, Authorization header with NO 'Bearer'; GitHub reads with GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config", repo Secuura/Distributed_Secuura). Any board COUNT you report comes from `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/board_count.sh` (read its header first), never from a query with a limit you chose. Linear comments `first:50`, sorted client-side.

## The question
Which Secuura tickets (team key KS, states Todo / Backlog / In Progress with NO open PR) can an agent build NOW, and how do they group into **3 to 5 lanes on disjoint code**, so Wednesday can launch one build seat per lane in parallel?

## Exclusions (hard)
- Assigned to or owned by Peter or Stuart (client humans), or waiting on them / on Kam (a decision, a credential, a deploy, production, money, external comms).
- Anything with an OPEN PR already (read all open PRs with file lists; the B 176th drafter's census `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-15_drafter-seatB176/census.json` is 85 PRs at 13:5x — re-read, do not trust it blind).
- Paths owned by live seats: Seat AA 6th = `Blockchain/Dev/services/anchoring/**`; Seat B 176th's queue = the paths of PRs 2098, 2089, 2079, 2220, 2221, 2222, 2223, 2224 (merging now; avoid them until merged).
- KS-1699 (share/recertify: waits on Kam). Demo/UAT/production deploys. Migrations need a QUESTION, flag them.
- Tickets whose newest comment says done/merged/deployed (a ticket is a claim: read its comments, newest first).

## Produce `screen.md`
1. The board picture: counts by state from board_count.sh.
2. A table of candidate tickets: key, title, state, priority, the code paths it will most likely touch (measured by reading the ticket and grepping the repo at develop `48883ba5976b`), size (S/M/L), routing row from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md` (C1-C4, Sonnet vs Opus), and why it is agent-actionable.
3. **3 to 5 LANES**: each lane = an ordered list of 2-6 tickets sharing one code area; lanes pairwise disjoint in paths (state the path globs per lane and show the pairwise check). Recommended model per lane with its routing row.
4. A short "NOT NOW" list with the reason for each (waiting on a human, overlap, unclear).
## `notes.md`
Instruments used, and a final section headed UNMEASURED.

Model: Sonnet. Return a 12-line summary: board counts, the lanes (tickets + paths + model), and anything that blocks.
