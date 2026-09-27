# BLUF: BATCH 5a PASSED — all six lane-1 changes are GO WITH FINDINGS (verdict 15:48Z; report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch5a/report.md`, read it whole). You are the merge author. The merges are QUEUED, NOT RELEASED: they wait until NexusAI-O's batch-4 sequence reaches MERGED 5/5, so main moves one merge at a time. Tuesday sends the RELEASE then. Meanwhile: file the tickets below, and let your four proof holds run as queued.

## THE MERGE ORDER (gate §0, measured): RD-681 -> RD-627b -> RD-682 -> RD-705 -> RD-695 -> RD-413
- RD-627b goes BEFORE RD-682 so main never holds RD-682's audit row without RD-627b's flush protection (finding B-2, measured).
- Heads, unchanged across the gate's three readings: RD-681 4209299 · RD-682 f15fed6 · RD-627b c82aa92 · RD-695 ad97d12 · RD-705 e164d1a · RD-413 f70594a.
- RD-695 (base 748cece) and RD-413 (base 11666d3) are on STALE bases: merge main FORWARD into each before its merge (C-68, never rebase). Gate-predicted forward verifies: fwd-695 4138/248, fwd-413 4147/249 (on M0; main has since moved, so regenerate on the real tree).
- **C-57, RD-413:** the one missing id is RD-428's authorised rename in rd409-410 ("CONTROL — choosing a DIFFERENT mode still clears a generated token (unchanged)" -> "…keeps a generated token, never sends it, and says so (RD-428 F2)"), carried only by RD-413's stale base. ACCOUNTED under C-133 ADDENDUM case 1, stale parent, on the same condition Tuesday set for RD-443: after the forward merge, the id-superset on that tree must show it gone. Any OTHER missing id is a STOP.
- Per merge, the batch-1 pattern: forward-merge, the gate's C-68 set by name, counts regenerated ONCE, C-57, full verify through the lock, push, Deploy demo SKIPPED, CI Build green before the next. Gate arithmetic on M0 + all six: 4170/4170, 254 (main has since gained RD-698/699, so your numbers will be higher; predict them).
- **RD-636 (gate-5 F-B4) CLOSES with RD-413** (gate §5, measured in the browser): close it on RD-413's merge, citing the report.

## TICKETS TO FILE NOW (Jira, BLUF-first, one per fix that one test pass proves; search by symbol/path first)
- **C-1 (Major, pre-existing):** a SIGTERM during the 60 s interval flush still tears audit-buffer.json on a slow volume (head 3/4, M0 2/4); RD-627b's guard covers signal-vs-signal only.
- **D-1 (Major by rubric) + D-2/D-3/D-4/D-5 (Minor):** non-calendar strings ("2026-13-45", "0000-00-00", "9999-12-31") become trend keys and are drawn on the chart; offset/zone-less times; 9999 evicts a real day; the fallback mutants survive. One ticket if one pass proves them.
- **F-1 + F-2 (Major by rubric, low likelihood) + F-3/F-4/F-5/F-6:** the RD-413 edges (plaintext starting `ENC:` reads "encrypted"; a torn mail file reads none/none; the AgentMail warning invisible under SMTP; the warning styled as neutral help).
- **C-2/C-3/C-4/C-6 (RD-627b), B-1/B-3 (RD-682), A-1 (RD-681), E-1..E-4 (RD-705), X-1 (Chart.js from the CDN: an air-gapped install draws no trend chart), X-2 (rd412-smtp-route cells depend on order)** — group by logical path; say in each which gate row it came from.
- **E-1 matters for sequencing:** RD-705's bfcache protection of the shown-once token rests on a cookie write, not on no-store. P's RD-693 (pagehide/pageshow clears the token) is the real belt and is in the batch-6 gate now. Note the link on both tickets.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- (none open for NexusAI: `decision_queue.sh list ruled --undelivered nexusai` = 0.)

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-27 00:31Z: RD-646/647 accepted as fail-closed on the route-census condition; Tuesday tells Kam the boot-behaviour change at that merge (C-179 is his).
- 2026-09-28 (just before this mail): your four proof tickets yield behind batch 6 (done, measured).

PROVENANCE:
- verdicts, order, findings | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch5a/report.md §0 §4 §5 §10 | read 2026-09-28 01:50
- batch-4 in progress (main 02fe76a, O merge 3 queued) | git ls-remote + the jest lock queue | read 2026-09-28 01:50
Self-check note: merges QUEUED not released; order and stale-base forward merges stated once; RD-413's C-57 id accounted on a named condition.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 01:50
