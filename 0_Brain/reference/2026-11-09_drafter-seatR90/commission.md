# Drafter commission: Seat R 90th brief (Secuura/Blockchain BUILD seat, Opus). Wednesday, 2026-11-09, the 10:01 successor seat.

## Output
Write ONE file: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_seatR90_build.md . Do NOT stamp it (no SELF-CHECK line): Wednesday reads it whole and stamps it last. Do not send, launch or mail anything.

## Read first (whole)
1. /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-08_drafter_common.md (any 'Spark OFF' line is STALE; never copy it).
2. The last R build brief as the SHAPE template: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-08_seatR89_build.md , and R 89th's HANDOVER (find it under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/ as *seatR-89th*/HANDOVER.md; read-only) for the lane's tooling, worktree and push-driver family.
3. The model routing table: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md (name the row in the brief's model line; ids from /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/models_latest.json).
4. Sources for the four items (read each; quote what you carry with its path):
   - KS-2141: the Spark counter is SPENT (two A2 failures); the golden diff applies as is: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-tier-test-only-bash/ks_2141_probe/golden.diff (and the probe folder beside it). Today's note entries 08:34 and 09:36 in /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-11-09.md.
   - KS-2127 (push-gate hook, bash, three sites) and KS-2131 (auth-gate cells): the Spark operator reports that routed them to a Claude seat: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator110/report.md and 2026-11-09_spark-operator111/report.md.
   - api-gateway/src/index.ts lines ~327-329 stale role lists: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator109/report.md (job 1) and Wednesday's ruling that kept it OUT of T's D5 (search briefs_staged/ for 2026-11-09_T1*_*.md mentioning 327). Find or name the ticket for it; if none exists, the brief says 'no ticket: the seat searches the board first and asks Wednesday before filing'.
5. /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-17_guard-against-reinventing-prior-work-check.md is Datasec's, ignore it; DO carry the Secuura standing lines from the R89 brief.

## What the brief must carry
- QUEUE in this order: (1) KS-2141 from the golden diff (tier 2 test-only bash; one PR); (2) KS-2127 (tier 1: a push-gate hook is a guard; red-proof both ways: the guard still refuses what it exists to catch); (3) KS-2131 (tier 1: auth gate); (4) the index.ts role-list item ONLY AFTER PR 2111 (KS-2109, Seat T 19th's D5, at gate 275 GO WITH NOTES, in Seat B 111th's merge queue) is MERGED, read at the PR API in the same action: it touches the same file. Each item ends at READY FOR GATE; no merge (Seat B merges on Wednesday's GO).
- PARTITION from both sides: files owned now by Seat B 111th's queue (PRs 2106, 2109, 2104, 2108, 2110, 2111, 2112, 2092, 2073, 2066, 2075, 2052, 2095, 2096, 2093, 2094, 2097, 2098, 2101, 2102, 2099, 2100, A3 group), PR 2113 (KS-2055 half 1, transfer index.ts, at gate 276), Seat T 19th/T 20th (KS-2055, KS-2123, KS-2132..2134, KS-2138 item 1, KS-2129, KS-2130), Seat U 20th (KS-2059), Spark operator 113 (KS-1902, KS-1794, KS-918, KS-1718). The seat checks every open PR's file set via the GitHub API before each push and QUESTIONs Wednesday on any overlap.
- Model line: claude-opus-5-5, with its routing row (tier-1 security surfaces are Opus by v1.0).
- Every Linear key named carries a provenance line (read-only, key sourced transiently, never printed) or 'not re-read: read it first'. No typed merged/open PR lists other than the facts above with their sources.
- An UNMEASURED section.

## Final message
The output path, the queue in one line per item, and every fact you could NOT verify.
