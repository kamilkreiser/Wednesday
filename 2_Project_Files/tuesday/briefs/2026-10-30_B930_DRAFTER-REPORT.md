STARTABLE: YES after your stamp, BUT ONLY with Q-1 and Q-2 answered (content rulings; the kit refuses to start without them). Two sweep pointers were wrong; both are fixed in the kit (see Corrections).

# B930 drafter report (Opus 5.5, 2026-10-30 about 10:23 to 10:58 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B930_SEAT-H61_hpsmpoc-380-381-readiness-training.md` (152 lines; 9 four-underscore lines = 8 slots + the last line, by `grep -c -E '_''_''_''_'`, control 1; at-sign slot pattern 0; non-ASCII lines 0 by grep and by a python byte scan, control 1). Read-only everywhere else: gh `-X GET` under the project `.gh-config`; Jira GET through the sweep's `scratchpad/s1015/jr.py`; no `cd`, no hosted HTTP, no ref written, no message. Nothing written in the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H61` (Sonnet, C2:92, gate G2:109 tier 2), branch `b930/hpsmpoc-380-381-readiness-training` off `e21d8044`, ports 9620-9629, two commits: C1 My readiness (nav flip + `retiresWith` honoured + hub panels + relabels), C2 Training (route, screen, flag). Every statement, area name, band, module title comes from content at runtime; new words limited to a stamped list.

## Facts measured (instrument; control)
- main `e21d80442980fb61ad9fb11aaf393c0b20c0ad2d`; open PRs 0; `matching-refs/heads/b93` = only `b93/gate-b94-notes`; ports 9620-9629 listening 0; kit scan 130 files: `962x` 0, `H61` 0 (control `979x` 10); panes `%0 tuesday`, `%1 fleet-monitor`; load1 2.35 at 10:23.
- Jira GET: -380, -381 (0 comments each; scope and AC quoted in the kit), -394 (gather, NOT to be built, also asks "whether the Training page belongs in this stage": answered by the 10-29 10:43:51 ruling a, build all but the three held pieces, as RELAYED from the B891 stamp).
- `GlobalNav.tsx` (main tarball): `my-readiness` line 44, `training` line 45 (both `built:false`), `services` line 50; **`retiresWith` is never read by `shown` (lines 62-63)**.
- Content `playbook-placeholder.v0.6.1.json`: 4 deck areas (Firmware protection; User authentication & secure print release; Data protection; Centralized visibility, policy enforcement & monitoring), Q-RDY-01..16, bands 0/4/8/12. Modules: 11 in app order introduction ... appendix.
- Design (python3 -I): `MODS` indices 0,3,5,6,7,8 = Playbook, Customer engagement and discovery, Snapshot assessment, Scoring and evidence, Phase 2, Phase 3: two have no app module. Step labels "Discover and scope", "Assess and verify", "Advise and deliver" (and the & forms): 0 hits in content (control "Firmware protection" 1); the third step's description says "framework alignment" (held).
- Model: model-routing.md C2:92, G1:108, G2:109, G-cap:111, L6:85; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` default opus.

## Corrections to the sweep (what is true)
1. **Flipping `my-readiness` is not a one-line edit.** `shown` ignores `retiresWith`, so the flip alone shows both "Assessments" and "My readiness" (same href). Kit D-2: honour `retiresWith` in `shown` and move the snapshot `also` path.
2. **H7's YOURS is incomplete.** The flip breaks label pins in files no lane lists: `shell/AppShell.sidebar.test.tsx` 60, 74; `e2e/playbook.ts` 150 (`startReadiness` h1); `e2e/playbook-event-states.spec.ts` 56; and `e2e/shell-sidebar.spec.ts` 11, 370, 417, **which is H14's file** (H14 edits the line 320 row). The sweep's "0 shared files" holds for paths, not for this semantic coupling. Kit Q-3: H7 edits only those lines; H14's hunk is disjoint; the intersection check stops H7 if H14 touches its lines. `app/(app)/assessments/page.tsx` line 4 (metadata title) is also added.

## D-decisions (in the kit)
D-1 two commits; D-2 `retiresWith` honoured in `shown`; D-3 the hub interprets the newest COMPLETED run, panels absent with none; D-4 disabled native checkboxes carry state (no new words); D-5 no priorities panel when nothing is unchecked; D-6 pathway rows show module `title` + `subtitle`; D-7 Sonnet C2, G2, 240/360 minutes. Also: the lane must not import `partner/parts`, `customer/parts` or `ui/Table` (H3), so no rebase onto H3 is needed; it imports `moduleHref` from H11's `PlaybookShell.tsx` read-only.

## Q-questions for Tuesday (recommended default and reason)
- Q-1 step labels (BLOCKING, no seat default): recommend (a) the ticket's three labels exactly, no descriptions. Reason: the ticket names them as scope; the descriptions are the prototype author's and one names held content. Alternatives: (b) hold steps; (c) deck phase titles.
- Q-2 module ids (BLOCKING, no seat default): recommend (A) `introduction, foundations, snapshot-assessment, phase-2, phase-3, beyond-year-1` (the app list at positions 0,3,5,6,7,8). Reason: six distinct existing pages, literal reading of the ticket, titles from content. (B) by meaning gives five rows (no "Scoring and evidence" module).
- Q-3 extension paths join YOURS: recommend YES (they break when the flag flips).
- Q-4 allowed new strings ("Readiness interpretation", "Learning priorities", "Back to My readiness", plus existing labels reused as titles): recommend YES (the two headings are the ticket's own words).
- Gate: tier 2, round 1 of 2 on new class "readiness and training pages". Times: target READY 240, hard stop 360.

## For Tuesday, outside the lane
`shell/HomeScreen.tsx` line 9 keeps an "Assessments" tile linking to `/assessments` (no lane owns it; mounted by `app/(app)/home/page.tsx`). H9's line-50 tail unblocks once B930 merges.

## UNMEASURED
Suite counts at main; Chromium; rendering; whether every role sees a completed seeded self-assessment run in the mock; e2e runtime under 14 seats.

## Outside-the-fences disclosure
None breached. Scratch only: the main tarball extract and nothing else under `scratchpad/drafters/b930/`. The output path was corrected mid-task by Tuesday's correction.txt before any file was written; nothing exists in the project's Briefs folder from this drafter.
