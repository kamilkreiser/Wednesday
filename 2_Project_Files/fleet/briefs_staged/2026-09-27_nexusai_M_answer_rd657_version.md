# BLUF: RD-657 ruled as you recommended. /api/health reads package.json's version (one source), and package.json on main becomes "2.2.1". Queue it behind rd-443's merge, as you said.

Why "2.2.1" and not a dev suffix: "version" names the release line a build belongs to, and 2.2.1 is the live listing's package (C-161). The EXACT build is already identified separately: rd327 reports a build digest on public health. So version plus digest together say "2.2.1 line, this build". Say that in the READY, in one sentence.

Conditions:
1. Re-anchor rd327's R7 cell to "health reports package.json's version", as a C-131-shape re-anchor with its red proof: a mismatched package version reddens it.
2. A cell proving ONE source: grep-free. Change package.json's version in a copy and show health follows it.
3. The NEXT release number stays Kam's (it is the Partner Center VERSION field). The release process bumps package.json at that release. Record that rule as a C-number.
4. The IMAGE_VERSION wiring waits until the Dockerfile is free (rd-418); add it to your queue, not to this ticket.

Sequencing: all three accepted. RD-650 stacks on RD-646/647. RD-688 waits for rd-695 and reuses trendDayOf, never _jobDate's created_at fallback. RD-628's hold stays queued.

-- Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 10:38
