# Commission: SCREEN EVERY SECUURA "IN PROGRESS" TICKET, 2026-11-15 15:1x AEDT

Commissioned by Wednesday. Kam, live board 2026-11-15, verbatim: 15:07:32 "please archive everything that is ready.  then work your way through the secuura tickets, in progress and backlog ASAP" and 15:08:26 **"there is a lot in 'in progress'. please complete and close these off"**.

Read-only: write ONLY `screen.md`, `inprogress.json` and `notes.md` in THIS folder (scratch here). Nothing posted, moved, commented, mailed, pushed; never write in `/Volumes/DevMASTER/!CODING`. No `cd`, no `rm`; absolute paths; `| head -N`; never print a secret (Linear key LINEAR_API_KEY in-process from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, Authorization without 'Bearer'; GitHub with GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config", repo Secuura/Distributed_Secuura). The count of In Progress tickets comes from a fully PAGINATED query (board_count.sh refuses over 250; state the page count and that `hasNextPage` ended false). Comments `first:50`, sorted client-side.

## For EVERY ticket in state "In Progress" on the Secuura team (key KS), one row in inprogress.json:
key, title, priority, assignee (name only: flag Peter / Stuart / Kam / the board account / none), updatedAt, newest comment time + its first 200 chars, linked PRs (attachments + PRs whose title/branch/body names the key: use ONE paginated GraphQL read of ALL PRs updated since 2026-09-01, open and closed, with title, headRefName, body excerpt, state, mergedAt) and each PR's state, and a BUCKET:
- **L — LANDED**: every PR for it is merged and the ticket text/comments show its scope complete (a "part 1" is not). Sub-flag whether Kam's Done rule allows Done now (card `secuura-done-rule-unit-pinned-deployed-no-live-check` = a: read it with `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-done-rule-unit-pinned-deployed-no-live-check`) or only "Tested Not Deployed".
- **P — OPEN PR**: an open PR carries it; note whether a gate verdict exists for the PR's CURRENT head (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/*gate*/verdict.md`, match the head's 12 hex with `/usr/bin/grep -l -i` + a positive control) -> P-GATED / P-UNGATED.
- **B — BUILDABLE**: no open PR, scope clear, not waiting on a human: an agent can build it. Give the likely code paths (from the ticket text; measure at develop `48883ba5976b` only for the top 30 by priority).
- **H — HUMAN**: waiting on Kam, Peter, Stuart, a credential, a deploy, production, money, external comms, or a decision; say which.
- **D — DUPLICATE/STALE**: superseded, duplicate (name the other key, proven at source), or premise gone (e.g. GitHub Actions retired 2026-08-27).
- **X — LIVE LANE (skip)**: KS-1699, KS-1934, KS-1935, KS-1910, KS-1897, KS-2185, KS-2192, KS-2189, KS-2188, KS-1900, KS-1899, KS-1684, KS-1993, KS-1994, KS-1914, KS-2030, KS-1749, KS-2103, and any ticket of B 176th's queue PRs (2089, 2220, 2221, 2222, 2098, 2079, 2223, 2224, 2081).

## screen.md
1. Counts per bucket (they sum to the paginated total; show the sum).
2. L list (key, PR(s), proposed state, one-line facts comment) — the board seat's archive queue.
3. P-GATED list (PR, head12, gate file + line 1) — merge-ready; P-UNGATED list — needs a gate.
4. B list grouped into code-disjoint LANES (3 to 6 lanes, path globs, pairwise disjoint, avoiding the live seats' paths: `services/anchoring/**`, `services/originate/src/routes/certifications.ts`, `services/billing/src/**`, `services/kyc/src/**`, `services/vc-issuer/src/**`, `systemTest/schemathesis/**`), with a model per lane from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md`.
5. H list grouped by who it waits on (Kam items worth a card, one line each).
6. D list with the proof.

## notes.md
Instruments, page counts, controls, and a final section UNMEASURED. Be honest about which rows rest on ticket text only.

Model: Sonnet. Return a 12-line summary: total, bucket counts, the top L and P-GATED counts, the proposed lanes, and the H items for Kam.
