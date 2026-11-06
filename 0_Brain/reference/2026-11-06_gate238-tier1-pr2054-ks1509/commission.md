# Gate 238 commission: Secuura / Blockchain, PR 2054 (KS-1509), TIER 1, round 1 of 2, narrow

Written by Wednesday 2026-11-06. Model: Opus, row G1. Why: gate 235's stop line fired. A stored block height of 0 now reads null, and Platform S's verify page shows 'Block 0' for 0 and hides the row for null (gate 235 F1, READ ONLY, its snapshot is not a git repo). Not a re-run: read /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-06_gate235-tier2-pr2054-2057/verdict.md first, and its 2054 evidence, and reuse them. Head 7bd7697c86ad29f2f5e3fc898e4bcc8935940704.

QA GATE: findings only; fix nothing; write nothing outside this folder; no box; no docker; post nothing; network only for git fetch. Absolute paths, never cd. Disk about 25 GiB and falling: reuse gate 235's clone at /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-06_gate235-tier2-pr2054-2057/ read-only if usable, or one small clone. A commit voids this verdict.

## Questions
1. What does each caller see, field by field, for a document whose anchoring is pending, at develop and at the head: every route that returns the height, the published spec, the three portals, and Platform S at the snapshot, saying plainly what the snapshot can and cannot show about the deployed Platform S? Is the 'no response shape' claim true?
2. Is a null better or worse for that caller than 0, in behaviour rather than taste: does anything treat 0 or null as proof of anchoring, confirmation or failure? Name the lines. Was a document at height 0 ever shown as anchored at block 0, which is the defect?
3. Does this change anything a client team relies on, Stuart's Platform S above all? If it needs a word to that team or a ruling, say so; that is not yours or the seat's to decide.
4. Is the direction Wednesday gave on 2026-10-12, null stays null, still right on what you find? It is a coordinator's ruling and may be wrong.
5. routes/anchors.ts:79 and the other places the ticket's 'seven' count. Merge tree on current develop.

## Output
verdict.md: line 1 GO, GO WITH NOTES or NO GO, line 2 the head, then BLUF, findings with severity, file:line, FOUND / TESTED / HOW, what was NOT tested, your own conduct. Final message: the verdict line plus one line per finding.
