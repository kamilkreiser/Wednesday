# B1743: Security Composer, what may be built on branches now
Clock: read 2026-11-19 17:10 to 17:35 AEDT (machine `date`). Project: `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec Security Composer` (Jira PCOMP; code repo `datasecau/Datasec-Security-Composer`, from `git remote -v`). Read-only. Nothing built, ticketed, commented or decided.

## ANSWER
3 buildable keys in 2 lanes: PCOMP-36 and PCOMP-37 (one lane, a new `content/baselines/` data file, on a branch stacked on the held L1 branch) and PCOMP-29 (a records-only crosswalk, optional, no branch). Everything else of the 13 is out. Drafter A is WRONG on the main point: L1 (PCOMP-31 to 35) is not "unbuilt"; it is built on draft PR #85 and only its landing is held, so there is nothing left to build there.

Allowance (the sentences, with line numbers, CLARIFICATIONS.md): build on a branch yes; merge to main NO sentence permits it; release NO; deploy NO.

## 1. THE RULINGS, WORD FOR WORD
CLARIFICATIONS.md of the project, 2,891 lines, read 2026-11-19.
- Line 1687 (C-92, card K6 (a), ruled 2026-10-20 14:00:26 AEDT): "**Permits now:** L1 and L2 may be built and merged on branches."
- Line 1688 (C-92): "**Forbids:** cutting or deploying that release, or rebuilding the examples, before Kam says the round has ended."
- Line 1297 (C-71 row COMP-1, ruled 2026-10-12 20:12:54): "(b) After Paul's current review round." and "Paul's review is not disturbed. The release waits; a deploy card comes to you when his round ends."
- Line 1742 (C-97, card pr85 round 3, ruled 2026-10-21 14:46:09): "**Forbids:** a fourth round ...; landing #85 before K6 (C-92) and the open Composer cards; cutting or deploying the release (C-92 stands unchanged)."
- Line 1783 (C-100, 2026-10-23 13:35): "**Permits now:** lane L2 may take its values from the approved template (C-89's forbid on L2 using the template before approval is lifted)."
- Line 1788 (C-100 (4)): "**Release timing** stays C-92's: L1 and L2 may be built and merged on branches; cutting or deploying the new content release waits until the owner says the reviewer's round has ended. Shipping the template as content (the code repo) also waits on L1 and on the words card."
- Line 1787 (C-100 (1)): the why-texts and customisation-texts "are still the sample's source wording ... Datasec's own rewording is lane L2-3 on a words card (K9 (a), C-95)".
- Line 1719 (C-95, K9 (a)): "**Permits now:** nothing ships. Every lane that adds customer-facing words (section texts, why-texts, customisation texts) opens a words card first."
- Line 1666 (C-90, K4 (a)): "The check is recorded, not concluded. L1 starts when Tuesday confirms it in the L1 brief." (B330 STATUS line 23 records that Tuesday confirmed it, s125 ruling 2.)
- Lines 1764, 1770, 1771 (C-99): the Essential Eight mapping review is held "until the reviewer's current review round ends"; "**Forbids:** nothing new. The mapping review and anything that waits on it (lane 3a, #249, #265) is not started before the reviewer's round ends."; "**Not settled here:** when the round ends (C-92 and C-71 COMP-1 (b) still say the owner says so)".
- Line 1298 (C-71 COMP-2, Guided): "(a) Hold them all." / "No Guided work until you turn it back on."
- No entry after line 1771 records the end of the round (headings and text searched; control: the same pattern finds lines 1682, 1762, 1771).

What is allowed, exactly:
- BUILD on a branch: yes (C-92 line 1687; C-100 line 1788).
- MERGE: the words are "merged on branches". They do not say "to main". C-97 line 1742 forbids landing #85 (the L1 PR) before the round question. C-100 line 1788 puts "shipping ... as content (the code repo)" behind L1 and the words card. So: no sentence permits a merge to main of L1 or L2. I read "merged on branches" as "merged into branches", never main. A merge of a data-only file to main is an inference nobody has ruled; treat it as NOT allowed.
- RELEASE (cut): no, until the owner says the round has ended (lines 1688, 1788).
- DEPLOY: no (same lines), and Composer deploys only on its own card.
- Direction check vs drafter A: A wrote the allowance as "built and merged on branches" (matches line 1687) and in its card "build work that is allowed on branches". That is the right width for the allowance. A went WIDER than the text in two places: (1) "The build chain L0-1, L1, L2 can start on branches now" (L1 is already built; L2-3 and L2-4 are not buildable, below); (2) "no content release exists to cut today" (the release is built and tested on b330, only not cut: PR #85 title "HOLD K6: L1 SM 3.16 content catalogue (release built, not cut)").
- Holds in force, and which of the 13 keys they touch:
  - Reviewer's round (C-71 COMP-1 (b), C-92, C-99): PCOMP-19, 20, 92 (labelled held), and the release timing of 31 to 39. Of the 13, only 19, 20, 92 hold on it as work. A is right.
  - Guided hold (C-71 COMP-2): touches none of the 13. (Its ten keys: 68, 69, 72, 75, 84, 85, 86, 87, 88, 90, from A's list; not re-read here.)
  - Held PR #85 (draft, HOLD K6): touches PCOMP-31 to 35 (it IS their work) and is the base L2 needs.

## 2. THE TICKETS (Jira GET 2026-11-19, description, every comment, status, links; none has a link; all Backlog)
Clock check: PCOMP-19, 20, 92 carry the label `held` (positive control for the label read); PCOMP-29 and 31 to 39 carry only `composer-seed-1023` and `plan-comp-<row>`, no `held`, no `needs-kam`.

Main = `b4681297d974ac3d8e74a4a12baeb9ea41962c52` (gh GET 17:11:42; control `pulls/9999` 404). `content/baselines/` is absent at main (404; control: `content/sources` lists). PR #85: open, draft, head `851057291ffb019baee6c3c51a50d7b8833f5b3a`, base `308b7aa6`, 14 commits, 57 files, branch `b330/sm316-content-catalogue`, last updated 2026-10-21 11:15Z; main is 43 commits ahead of that base ("diverged"); the API says mergeable_state clean. Gate B424: GO WITH FINDINGS at 85105729 (C-97, line 1742). It is the only open PR.

| Key | Asks | Waits on (per ticket) | Real state | Says WHAT to change? | Unapproved words? | Content source |
|---|---|---|---|---|---|---|
| PCOMP-29 L0-1 | Records crosswalk: sample's 132 rows to SM 3.16 ids to the 123 registry controls; flags 11 absent and M106 | "Depends: nothing"; ticket says the SM catalogue lives on a sibling project's branches, "the coordinator's call" | Not started; no crosswalk exists (the only folder in `1_Project_Definition/Content/` is the template). L1 was told NOT to wait for it (brief B330 line 145, Tuesday s125 ruling 1) and built its own registry-to-SM map | Yes: one row each, SM id and sub-setting id where known | No (internal map) | Seeds in project: `Briefs/2026-10-20_B314_evidence/extract/map132.txt`, `map132_sm316.txt`; ids now also in the Composer repo on b330: `content/sources/sm_316_catalogue.json` (3,099 lines) and `packages/content/src/sm-map.ts` (679 lines). No sibling-project read is needed |
| PCOMP-31 L1-1 | SM 3.16 ids as a cited source + registry/SM map | L0-1 "not started"; round times release | BUILT: commit f53f251b on PR #85 | n/a | n/a | n/a |
| PCOMP-32 L1-2 | Items and typed fields for 66 controls | same | BUILT: 8d7fdf97 on PR #85 | n/a | n/a | n/a |
| PCOMP-33 L1-3 | New controls for 11 absent rows | same + Q-P1 for M106 | BUILT except M106 (not added, no SM item): 8d7fdf97 | n/a | n/a | n/a |
| PCOMP-34 L1-4 | Sub-settings stay sub-settings | same | BUILT: 1351fdf8 | n/a | n/a | n/a |
| PCOMP-35 L1-5 | Shared Items as real items | same | BUILT: 8d7fdf97 | n/a | n/a | n/a |
| PCOMP-36 L2-1 | Per item: class, target value per field, severity, remediation, unsupported handling, from the APPROVED template; DRAFT | L0-3 approved (done, C-100); L1 "not built; its branch is under hold" (comment 39948) | Not started. L1 exists on b330 | Yes for the five columns; the template has them as columns (class, severity, remediation, unsupported). "Target value per field" is thin: the template `target` is the sample's prose and only 53 SM ids are typed fields on b330 (B330 STATUS BLUF) | Only if prose targets are copied: they are the sample's wording (C-95 forbids it "in anything shipped") | `1_Project_Definition/Content/2026-10-20_hpsm-baseline-template-DRAFT/hpsm-baseline-template_DRAFT.json` (137,914 bytes, 132 rows, status APPROVED) |
| PCOMP-37 L2-2 | The 28 CONDITIONAL/MANUAL items carry "variable" + the Composer question or control decision that sets them | same | Not started | Yes: `variable` is true on exactly 28 rows (counted by program, 28); the setting question or control decision is per row, to be chosen from existing question ids | No, if it names ids and writes no new sentence | same template + question registry in the repo |
| PCOMP-38 L2-3 | Why-text and customisation-text and 8 section owner lines "as Datasec words" | words card (K9, C-95) | Not started; no words card ruled (searched the file after line 1800 for why-text, customisation-text, L2-3: 0; control: 6 hits before) | Says what, but the words are Datasec's own and nobody has approved any | YES | the template holds only the sample's wording |
| PCOMP-39 L2-4 | 7 solution-compatibility exceptions (gap D36) as content dependency edges | L1 | Not started | NO. Gap analysis row D36 (line 144) names its decision as "Kam: policy"; the edge type, determinant and constraint (types.ts REQUIRES, CONFLICTS ...) per exception are policy choices. The template has no row for the seven exceptions as such | Possibly (edge descriptions) | the client's source document, which this seat did not open |

PCOMP-19, 20, 92: held on the round; confirmed (labels `held`, comments 39936, 39937, and C-71). Not buildable.

## 3. LANES, in dependency order
Lane 1 (no predecessor): PCOMP-29, optional.
- Files: new folder under `1_Project_Definition/Content/` (the BACKLOG row #328 says `Content/2026-10-20_sro-template/`); no code repo, no branch. Size M. Gate tier: review (records), per the ticket. Rests: files in the project folder; the C-92 sentence does not apply (not a content release); nothing forbids it.
- Waits on: nothing. The ticket calls the catalogue source the coordinator's call; the ids are now in the Composer repo (b330) so no sibling-project file needs reading, but who may read b330 for this is Tuesday's call.
- STOPS if: it needs a sibling project's files; any row cannot be matched (flag it, do not guess).
- Honest note: its only consumer in the plan (L1) was built without it, so value is low. Tuesday decides whether it is worth a seat.

Lane 2: PCOMP-36 + PCOMP-37 together (one new data file and one README under `content/baselines/`; both tickets name the same area, so two branches would collide on the README).
- Files: new `content/baselines/<file>.json` + `README.md`; no existing file touched (at main, `content/baselines/` does not exist; b330 tree `content/` has guided-wording, release-demo, release-draft, sources only). Size M. Gate tier guess: the plan says tier 1; I guess a tier-2 style data-only review is enough because no code or release is cut, but that is Tuesday's call.
- Base: branch stacked on `b330/sm316-content-catalogue` head `851057291ffb019baee6c3c51a50d7b8833f5b3a` (the items and fields it keys on exist only there: 137 items on b330, 55 on main).
- Rests: on a branch, NOT merged, no release, no deploy. Permitted by line 1687 and line 1788 ("built and merged on branches"); values from the approved template permitted by line 1783. A draft PR marked HOLD (as #85 is) is the project's pattern but is my suggestion, not a ruling.
- Waits on: nothing it needs is unbuilt. The finished lane then waits for PR #85 to land and for the owner's word that the round ended before it can enter any release.
- STOPS if: PR #85's head moves (rebasing it onto main changes shas and B424's verdict "expires if the head moves", C-97 line 1743); a row would need a sentence, not an id or an enumerated value (the sample's `target`, `why_source_wording`, `customisation_source_wording` and the reviewer names in `_meta` must NOT be copied); the content text tests at b330 may reject a name or ruling word in provenance (INTERNAL pattern, brief B330 line 66); the typed field is missing so the target value cannot be stated without inventing it (leave NEEDS_TARGET, carry the row, say so); the numbers the owner has not confirmed with the reviewer (question Q-P5: 16 chars, 10 min, 50 jobs, 25 MB, 60 s; the send is the owner's, C-96/C-99) must be flagged as proposals, not standards.
- Honest limit: L2-1's "target value per field" will be only partly fillable; a builder must be told that partial is the expected result.

## 4. NOT BUILDABLE, and why
- PCOMP-31 to 35: already built (PR #85). Nothing to build. Their Jira text ("Not started", "waits on L0-1") is stale. The landing is held (C-97 line 1742).
- PCOMP-38: needs Datasec's own words that no card has approved (C-95 line 1719; C-100 line 1787).
- PCOMP-39: the content is a policy decision (gap D36 "Kam: policy"), not ruled.
- PCOMP-19, 20, 92: held on the reviewer's round.
- Guided ten: Guided hold, none of the 13.

## 5. DRAFTER A, RIGHT AND WRONG
RIGHT: only 19, 20, 92 hold on the round; PCOMP-29 carries no hold; C-92 permits building on branches and times only the release; the allowance quote; PCOMP-29's catalogue source being the coordinator's call (now mostly moot).
WRONG: (1) "PCOMP-31 to 35 wait on L0-1 / unbuilt lane": L1 is built; 14 commits, gated GO WITH FINDINGS at 85105729; L1 did not wait on L0-1 (Tuesday s125). (2) "the L0-1 -> L1 -> L2 chain is buildable on branches today": only L2-1 and L2-2 (and L0-1 as records) are; L2-3 and L2-4 are not; L1 needs nothing. (3) "no content release exists to cut today": it is built, not cut. (4) A's card says "the new content has not been built yet"; the L1 part has been, and is not landed. This matters for the card A1: its sentences "the new content release ... has not been built" should be corrected before Kam reads it. Not in my remit to edit.

## FOUND
- Allowance and holds as above. Nothing records the end of the round.
- L1 built on held draft PR #85 (b330, head 85105729, 14 commits, gate GO WITH FINDINGS); Jira PCOMP-31 to 39, BACKLOG rows #331 to #339 and the C-record still say "not started" or "L1 not built" (BACKLOG row #336 itself says "PR #85 open under hold K6"): the records contradict themselves.
- Buildable: PCOMP-36, 37 (lane 2) and PCOMP-29 (lane 1, optional).

## TESTED (and NOT tested)
TESTED: reads only. Jira GET of 13 issues (description, comments, labels, links), by program, credentials read in-process by name (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN); gh -X GET of main, PR list, PR #85 body, files, commits, compare, contents; template JSON counts by program (132 rows, 28 variable, status all APPROVED); line-numbered quotes of the clarifications file; B330 STATUS and brief lines.
NOT tested: that the b330 branch builds or its tests pass today (no test run; B423 STATUS says 3,213 passed at 85105729, relayed); that PR #85 rebases onto main without conflict (the API's "clean" is GitHub's own flag only); that `content/baselines/` would pass `content:check` or the content text scans; whether the owner has told anyone the round ended (the records say nothing, he may have); the client source document for the seven exceptions (not opened); Jira state beyond the 13 keys plus A's list; the Guided ten were not re-read; PCOMP-94 (the five questions) not re-read; no host, no az, no decision_queue.sh call.

## HOW
Folder verified by listing `/Volumes/Datasec_DEV/!CODING/Datasec/` (the parent listing also showed other projects; none was opened beyond this one). A_REPORT.md and the reviewer-round card read whole. CLARIFICATIONS.md searched with `/usr/bin/grep -n -i` and read at lines 1286 to 1330, 1592 to 1735, 1736 to 1800, 2596 to 2606. Scripts and ticket dumps in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1743/` (`jira_get.py`, `PCOMP-*.txt`). The local checkout `2_Project_Files` is stale (local main 0b2fca43, behind 103), so every code fact above is from `gh -X GET` under the project's own GH_CONFIG_DIR, not from the local tree. One `decision_queue.sh list` call returned unrelated old cards; none used.
