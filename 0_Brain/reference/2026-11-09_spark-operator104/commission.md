# Spark operator 104 — commission (Wednesday, 2026-11-09 00:0x AEDT). Secuura only.

## BLUF
Kam, panel 2026-11-08 20:26 (verbatim): "please check that the spark is running flash 4 and keep it active as much as possible". The Spark has been idle since 23:30 (operator 103: pool exhausted under the rules, written reason). Two jobs, in order: (1) the ONE allowed rebrief of KS-2022 with its full scope, IF its remaining files are free; (2) a fresh screen of tickets filed since 103's screen (KS-2105 and above), plus anything 103 listed as skipped whose blocker has since merged. Target 4 held passes; never pad; a thin pool is a finding with counts.

## Read first (whole)
1. Operator 103's commission and report, and operator 102's commission and report: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_spark-operator10{2,3}/. EVERYTHING in 102's commission binds you (read-first list, classes, flow, counter, limits, deliverable shape), as amended by 103's, except what this file changes.
2. KS-2022 at source (description and every comment, newest first), and KS-810's closing comment, which names stale paragraphs.

## Job 1: KS-2022, round 2 of 2 (the counter: original + ONE rebrief, then a Claude seat)
- Round 1 was O102-P1: 2 of 4 stale gate citations (ks796 test, auth.openapi.ts). Sites 3 (routes/mfa.ts:130 per the 22:4x seat's note) and 4 (services/accountLockout.ts:71) were skipped because held READYs (KS-938, O85-P1) and passwordLoginGate.ts (held KS-1467) covered those files.
- FIRST, measure whether that is still true: is each of those held READYs still held in night/, raised as an open PR, or merged at the pin? Check every open PR's file list for the four files plus any file KS-810's stale paragraphs live in. State it as a table: file · holder (READY name / PR number / none) · how you read it.
- If ANY of the four sites' files is still held by another READY or listed by an open PR: do NOT brief the rebrief. Record it as BLOCKED with the table; the ticket waits for that holder to merge. The O102-P1 READY stays held as it is.
- If all are free: write ONE brief covering all four sites plus the stale paragraphs, exact edits by line with the line's current text at the pin, at most 3 edit points per brief (split into two briefs if needed, both count as round 2). The new READY supersedes O102-P1: say so in its name and in your report, and do NOT delete O102-P1 (quarantine is Wednesday's call).

## Job 2: fresh screen
- New tickets since 103's tickets.json (KS-2105 and up, including KS-2109..KS-2116 filed tonight), and 103's skipped rows whose stated blocker was a PR now merged (develop moved: 2077 and 2072 merged tonight). Read each candidate whole and the file at the tip before briefing. Same exclusions: no file a held READY changes, no file an open PR lists (scan with a planted control at start and before each round); a test-only pin whose read-only product is elsewhere is allowed, flagged for re-run at raise time (Wednesday's 23:3x ruling to 103).

## Limits
- Pin: develop 7eda23b34d3b7a413ca8f9c0945c7843708ce9f4 at 00:00:01 AEDT (Wednesday's ls-remote). Merge seat B 100th is merging tonight: re-pin per round and record it.
- Disk: DevMASTER read 24 GiB free at 00:00. Under 18 GiB = STOP. Load1 under 8 before each round.
- The drainer is not a standing process: start queue.sh per batch, leave nothing running.
- No push, no PR, no ticket write, no mail. You hold READYs; a Claude seat raises them.
- Stop at 4 held, a genuinely exhausted pool (with counts), or about 2 h.

## Deliverable
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator104/report.md: BLUF; Job 1 table and outcome; each held pass (name, hold_ready line, what it does NOT cover); skipped list with one reason each; UNMEASURED. Plus the queue.md comment line if the pool ends empty. Final message: BLUF + held names + done.md row times only.
