# Open-PR gate census, Secuura/Distributed_Secuura, 2026-11-11 (read-only; GitHub REST + brief + verdict files)
Open PRs: 84 (73 kksecura, 10 dependabot, 1 StuJam-Secuura). Full rows: census.tsv (same folder).

## Counts per class
- Q (queued by B 132nd at its current head): 60. All 60 queue heads equal the PR's live head (12-char).
- G (verdict at CURRENT head, not queued): 12.
- S (verdict only for an OLDER head): 0 found (see UNMEASURED).
- N (no verdict found): 1.
- O (author not kksecura, report only): 11 (10 dependabot, 1 StuJam-Secuura).

## G, not queued (verdict head == live head; all opened/updated 6-8 Nov, so gated but never queued)
2159 KS-2111 (gate 301, GO WITH NOTES) | 2090 KS-692, 2089 KS-1493, 2088 KS-1797 (gate 252 tier-2 batch: GO, GO, GO WITH NOTES)
2087 KS-1600 (gate 251) | 2085 KS-2074, 2081 KS-1171 (gate 248) | 2080 KS-1670, 2067 KS-2071 (gate 246)
2079 KS-657 (gate 241) | 2064 KS-1205 (gate 253 r2) | 2059 KS-1410 (gate 250 r2).
Action for Wednesday: these need a MERGE-queue decision, not a gate lane (why unqueued is not in the inputs: held? superseded? merged-by-other-route?). Not read: each verdict's verdict word for the last six; only 2159, 2090, 2089, 2088, 2085, 2080, 2067 verdict words seen.

## N (needs a gate)
PR 887, author kksecura, head 3aee3deed2e3, Linear KS-961 ("run the workspace suites on the PR, advisory and non..."). Files (2): .github/workflows/pr-platform-suites.yml, Blockchain/Dev/docs/DEV-PROCESS.md.
Tier guess from paths: 2 (CI workflow + docs, no product source). Caution: a workflow file runs with repo secrets/permissions, so the gate may reasonably raise to tier 1; decide at commissioning.
It is an old PR (created 2026-09-07, last updated 2026-09-30); it also appears in 2026-11-09 priority-triage notes (not a verdict).

## S
None found. 0 PRs have a verdict for an older head only.

## BATCHES (N+S, file-disjoint, <=4 tier-2 per batch, tier-1 one per batch)
- Batch CENSUS-A (tier 2 guess, one PR): PR 887 (KS-961). Nothing else to batch with.
Total: 1 batch.

## O (report only)
10 dependabot bumps (PRs 575, 635, 639, 649, 945, 946, 947, 948, 949, 1965: dotenv, cbor, radix dropdown, pg, axe-core, fluentui icons, jest-dom, vite 6->8, prisma, @types/office-js) and StuJam-Secuura PR 1129 (docs(history) 2026-09-21 local rebuild). No gate action by this seat.

## UNMEASURED
- Verdict-to-PR matching: a verdict counted for a PR only if the PR number appears in the first 600 chars of verdict.md or in the folder name, and the live 12-char head appears in the file. A batch verdict that names a PR deeper in the file would be missed (that is how the first pass wrongly showed 6 G PRs as N; I corrected those by grepping the batch files; the same blind spot could hide an S).
- S = 0 is therefore a weak zero: older-head verdicts were not searched by number beyond that rule, and no positive control for an S was run.
- Q class trusts the brief's QUEUE rows (60 PRs, head from the first backticked 12-hex); gate verdict presence for Q rows not re-checked.
- Verdict words for the G rows listed above as not read. Tier guesses in census.tsv for G rows are path-only and differ from the gates' own tiers (e.g. 2087, 2081, 2064, 2059 were gated tier 1).
- Reference dir scan covered *.md files with gate/verdict/report/calib in the path (1066 files); other locations (Linear comments, PR comments, outside reference/) not read.
- PR draft flags, mergeability and CI state not examined.
