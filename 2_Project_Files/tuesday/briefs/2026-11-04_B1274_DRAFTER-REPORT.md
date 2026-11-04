STARTABLE: YES (after Tuesday's stamp; the Build of the merge is still running, so the seat polls; Q-1 and Q-2 have defaults)

# B1274 drafter report: SEAT-R171 (records), NexusAI, the landing of #165 (RD-902) + the gap ticket
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-04_B1274_SEAT-R171_nexusai-records-165-rd902.md` (122 lines, shape of B1235/R161), `2026-11-04_B1274_slots.json` (12 keys, valid JSON, no angle-bracket placeholders, only `@NOW@` and `@SEAT@` as variables, no attestation of a Tuesday read). R171 was free (last seen R170; scan of the non-`.pre-` SEAT kits of 11-03 and 11-04: `R171` and `B1274` 0 files other than this kit, control `R170` 3 files).

## BLUF
Order of the seat's writes: (C) create the gap ticket from the byte-approved text (embedded in the kit between two marker lines, sha256 pinned and re-hashed by the seat), (D) append C-236 in a NEW section 72, (E) one comment on RD-902, (F) one move RD-902 to Testing, (G) HISTORY.md entry on `records/b1274`, pushed by the seat; Tuesday opens and lands the PR. The ticket comes BEFORE the C-entry because C-236 and the comment name the new key.

## Facts re-measured (date printed 13:28 to 13:34 AEDT)
- PR #165 (`gh api -X GET`, project GH_CONFIG_DIR): merged true, merge commit `cc4666dc7b06f04f49b384fe6245cfa2f5585be9`, merged_at 02:26:48Z (13:26:48 AEDT), parents `efcf86c5...` + `bcdf835f...`, tree `633018b0...` (the review's merge-result tree prefix, `B1260_STATUS.md:23`; prefix only compared), +421/-11, 4 files (rd436 funnel test +7/-6, rd902 test +397, server.js +14/-2, counts +3/-3; sums 421 and 11 add up). Main = cc4666dc; open PRs 0; `pulls/99999` 404.
- Head `bcdf835f` check-runs: 8 runs, 7 names, all success. Deploy demo 41760801261 completed skipped. Build 41760801259 and Push on main 41760800868 in_progress at drafting (UNMEASURED; seat polls 75 min).
- Verdicts: `B1246_STATUS.md:1` NO GO round 1 of 2 (four Majors `:147-:150`); `B1260_STATUS.md:1` NO GO round 2 of 2, `:19` class census 1 prior hit (B1246), `:245` the one new Major (MK, `server.js:20993`), `:222` gate leg NOT MET, `:265-:267` product change correct, residue ticketed.
- Ticket figures against their sources by `grep -n` (all matched): 20993 `:245`; 24 / 1008 `residue.md:11` and `B1260_STATUS.md:57,247`; 219/180/399/17 `residue.md:12`, `B1260_STATUS.md:246`; MK1 quote `residue.md:17` (whole string substring-checked); fix shape `:16`; not-measured `:15`; `server.js:462` `STATUS:208,250`, `residue.md:20`; "nine" = `STATUS:140` ("9 gate sites"); "same answer" `residue.md:21`. Only "regenerate it once, never by hand" has no line of its own (`STATUS:186` says the builder regenerated once): kit calls it UNSOURCED-BUT-APPROVED. ticket.md sha256 = `7c9a065e...5e2ea6` (matches the B1271 pin; the embedded span re-hashes to it, control with one flipped byte differs). Title is 87 chars.
- Gap not yet ticketed: `project = RD AND ( ... )` for `labels = "b1260-finding"`, summary phrase "RD-902 follow-up", `text ~ "riskConditionAdminPasses"`, `text ~ "MK1"` all 0 hits; controls `key = RD-902` 1, nonsense 0. (Hazard I hit and the kit warns about: the helper's `search` returns `(issues, pages)`; the second element is a page count, not the hit count.)
- Jira (scratch copy of the b1210 helper, heartbeat in my scratchpad; creds read in-process): RD-902 To Do, Task, Low, labels b894-2026-10-29 + operations, 1 comment (40692), links 0, Done-when "if changed, the sync is off the read path with a red-first cell and a gate". RD-922 Testing, 2 comments. RD-916 To Do, 0 comments.
- CLARIFICATIONS.md 2504 lines: `## 71.` `:2498`, `**C-235.` `:2500` (B1235's records entry is already in), so this entry is **C-236, section 72** (not C-235). HISTORY.md at main: 9570 lines, blob f51de3e9 (contents sha equals `git hash-object` of the decoded file), B1235 heading `:9540`.
- Panes at drafting: tuesday, Datasec/HPSM-POC-H117, Datasec/MPS-G338, Datasec/HPSM-POC-G337, fleet-monitor; NexusAI pattern 0. Ports 9800-9999: 0 listeners.
- Model: `model-routing.md:98` row C8 (its words name no records job; precedent B1235/B1253/B1256/B1265), `models_latest.json:23` claude-sonnet-5-5, `brief_seat.sh:24` default opus, so `BRIEF_SEAT_LEVEL=sonnet` is inside the quotes, `WED_USAGE_STOP=100` outside and inside.

## (3) RD-902's own ticket state under the project's rule
`NexusAI/CLAUDE.md:302` code change -> Testing (a person then moves it to Release Ready); `:303` decision/docs -> Done. #165 is a merged, not-deployed code change, so Testing, not Done. A ticketed gap does not change that: C-62 (`CLARIFICATIONS.md:581`) says a Major at round 2 of 2 is ticketed, the landed part stands, the residue is fixed where the work goes next, and only a third round needs the product owner's word; nothing in it says the ticket is Done. RD-902's own Done-when names "a red-first cell and a gate"; the cells are MET, the gate leg is NOT MET (`STATUS:222`). Note C-62 was written for a GO WITH FINDINGS round 2; this round was NO GO, so the landing rests on the product owner's ruling and the kit says so in C-236. The G-cap row (`model-routing.md:111`) agrees ("ship the closed instances, ticket the residue"). The kit does the move by the `In Review` entry that lands on Testing, as RD-917 and RD-922.

## (4) RD-916 (read-only)
RD-916 = "RD-913 follow-up: the scoped jest transform in package.json has no cell for its default entry and names its plugin instead of resolving it, so a bare jest run from outside the repository root cannot load it (low)". To Do, Low, 0 comments, labels b1069-finding, b1088-2026-11-02, qa-gate-finding. Test and config only (a red-first cell for the default entry; move the jest block to a jest.config.js using require.resolve), moves `scripts/verify-expected-counts.json` by one cell; Done-when also allows the product owner leaving it. Actionable now: yes in principle (C-234, `CLARIFICATIONS.md:2494`, queues "RD-902 then RD-916"; open PRs 0, no builder pane live), NOT commissioned. Ordering risk: the new gap cell also moves the counts file, so the two builders must serialise (rebase on the committed pair). It has no recorded decision for the leave-it branch.

## D-decisions (mine)
- D-1: Ticket before C-entry (the key is a fact both later texts use); a ticket HOLD makes the texts say "held".
- D-2: The ticket text is embedded, not referenced, because the seat may not read Tuesday's tree (hard rule 1); extraction by two marker lines, hash pinned.
- D-3: Labels copied from RD-916's pattern: `ai-assistant`, `b1260-finding`, `b1274-2026-11-04`, `qa-gate-finding`; Task; priority Medium (see Q-2); no parent, no component, no link.
- D-4: Comment says nothing the cap rule does not support; "no go" wording, no gate/seat/brief/B-digit/person words (scanned by my own script: AUTH only the waived "coordinating" once; BLUF, REC, DET 0 in every class; ASCII). The review's merge-result tree is claimed only as a prefix match.
- D-5: C-62 and the cap rule are paraphrased, never quoted (both headings carry a person's name); CLAUDE.md:302 quoted with the name omitted, as C-233/C-235.
- D-6: Ruling worded "relayed", board time 12:37:24 typed once in C-236's heading as relayed; the decision store was not read, kit says not to claim it agrees.
- D-7: Closed list: RD-902 once, gap ticket once, RD-922/RD-917/RD-916 once each as "not touched".

## Q-questions for Tuesday
- Q-1: The approved ticket text uses the word "gate" seven times (ticket lines 8, 10, 11, 13, 25, 27, 28), which the usual Jira-text rule bans. Default: waive the word for those exact hash-pinned bytes only, all other classes still scanned. Alternative: reword to "independent review" and re-approve (changes the pinned sha256).
- Q-2: Priority Medium (the text says Major, restrictive; RD-902 itself is Low). Default Medium.
- Q-3: Sonnet for a records seat rests on precedent, not on the table's words. Default: Sonnet.
- Q-4: Link the new ticket to RD-902 ("Relates to")? A link is a write on RD-902. Default: no link (the title and the comment name each other).
- Q-5: Move RD-902 to Testing (default yes) rather than leave it To Do until the gap cell is built.

## UNMEASURED
Build and Push-on-main conclusions for the merge, CodeQL on the merge commit, the ruling and its store time (relayed), the transitions list of RD-902 (seat reads), whether the b1235 scripts run after renaming (nobody ran code), `ticket.md` text correctness beyond the grep-checked figures, how the 24 divergences split by cell.

## Outside the fences / disclosures
Reads only: gh GETs, Jira GETs through a scratch copy of the b1210 helper (heartbeat path in my scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f218458d-a253-43ed-9ef3-33b5c309207c/scratchpad/`), tmux, lsof, raw files under the NexusAI tree and Tuesday's briefs/model-routing. No decision_queue, no fenced trees, no hosted host. One hook refusal on a leading `cd` (no effect). The ticket kit B1271's own folder was read for `ticket.md` only. No Write outside the three output files (scratch scripts in the scratchpad).
