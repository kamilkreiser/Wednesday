STARTABLE: YES

BLUF: ADDENDUM-2 tells the live seat (H117) to take b1204 `a26bee7e8b0426605955736ea78905960f5e45b1` as its base by the kit's own `-2` route: commit V locally as V0, new tree + branch `b1272/hpsmpoc-visual-round-2` at a26bee7e, merge main (M0b), `cherry-pick -n V0`, one commit, one push of the `-2` refspec; it names the fix round's lines that must survive; it asks for the red-first and e2e evidence re-run on M0b. The seat has pushed nothing (`heads/b1272` = 0 rows), so no force is needed anywhere.
The seat's STATUS is stale (last write 14:10, 112 min before drafting) but its heartbeat at 16:02 reads "srcplants2 running": it is in the plants part. Tuesday should expect the re-run to cost it a large share of its remaining time (Q-1).

FACTS (instrument; each at drafting 16:02 AEDT, `date`)
1. b1204 head = `a26bee7e8b0426605955736ea78905960f5e45b1` (`gh api -X GET .../git/matching-refs/heads/b1204`, 1 row). main = `77f56644...` unchanged (1 row). `heads/b1272` = 0 rows. Open PRs 0 (`pulls` length). Account kamilDatasec under the project's GH_CONFIG_DIR (`gh auth status`).
2. `compare 04c48316...a26bee7e` = status ahead, ahead_by 3, behind_by 0, merge base 04c48316 (forward, no force); 3 paths: AppShell.tsx +1 -1, shell-sidebar.spec.ts +97 -23, AppShell.sidebar.test.tsx +8 -0 (`--jq` over `.files[]`; sum matches the fix-round STATUS "+106 -24" = 97+8+1 and 23+0+1).
3. `compare a26bee7e...main`: main side 19 paths, 0 in the 3 (`comm -12`; control: 3-path list against itself = 3). So M0b (a26bee7e + main) cannot conflict on the fix round's paths. `compare main...a26bee7e` = diverged, ahead 4, behind 2, base a8497578 (matches the kit's 1 + 3 ahead, 2 behind).
4. Pointers printed by `grep -n` over `gh api` raw files at a26bee7e (control: `grep -c zzzqq` on AppShell.tsx = 0): AppShell.tsx:166 (the row class; no `print:` in the file: `grep -n 'print:'` printed no line); AppShell.sidebar.test.tsx:218 (new pin, directly under the :215 `max-w-7xl` pin); shell-sidebar.spec.ts :67 (RAIL/HOVER/CURRENT), :123 paintedRing, :504 floor row, :656 walkRail, :719/:727/:733 (expanded walk cells), :822/:830/:836 (collapsed), :928 footer-rule row, :1152 RING_ON_RAIL, :1288 ring row, :1298 `main` wait. Walk cells counted 3+1+1+3+1+1 = 10, equal to the fix-round STATUS "10 cells" (RELAYED).
5. Kit route read at kit line 29 (`-2` branch from the new head, merge main, cherry-pick V; "the stamp's BASE ROUTE slot (or an addendum) names the new head"), refspec line 31 (the `-2` refspec "only when the Stamp names it"; the addendum names it), landed-test line 43 (`compare 04c48316...main`; replaced in the addendum by `a26bee7e...main`), plant cap 12 at kit line 61: the kit lists 10 named plants, PO + PP2 make 12.
6. ADDENDUM-1 shape: no Stamp, no slots, no READ-WHOLE last line (`tail` of the file; 22 lines), so no slots.json and no READ-WHOLE line in ADDENDUM-2 (it ends on its STOP line). No person name, no card id, no B-number in the addendum text except inside the one STATUS file path (a path to a claim to read; the kit says files naming another B-number are readable claims).
7. Seat state (instrument: `ls`, `tail`): `.tools/wt-b1272-{fix,main,mut,ref}` exist; heartbeat line 350 at 16:02:22 "load1 6.19 srcplants2 running". Panes at drafting (`tmux list-panes -a -F '#{@cockpit_name}'`): Datasec/MPS-R172, Datasec/NexusAI-N98, Datasec/HPSM-POC-H117, fleet-monitor, tuesday: no other HPSM-POC seat is live. Port block 9710-9719 NOT re-checked by me (UNMEASURED).

DECISIONS
D-1 I did not use the kit's literal "create `-2` from the new head and cherry-pick V" alone: V may not be a commit yet (STATUS says "written and unit-green", no commit). So: commit V0 locally on the old branch, `cherry-pick -n V0`, commit once. Reason: the kit forbids amend/reset, and a commit message built from old-base runs would be wrong on the new base. Q-2.
D-2 Time: the addendum leaves the kit clocks (target 16:36, hard stop 18:06, from the seat STATUS Step 0) and gives the seat a STOP-with-resume route rather than extending them. Q-1.
D-3 The seat applies it at a "safe boundary" defined by a property (WORKING line written, plant tree clean, no listener, heavy slot released) with "at least" nothing open-ended.

QUESTIONS FOR TUESDAY
Q-1 Extend the hard stop? Default: no; the seat writes PROGRESS and RESUME and `STOPPED: NEEDS TUESDAY time` if it cannot finish by 18:06 (target 16:36 is already unreachable with a re-run).
Q-2 Allow the local V0 commit + `cherry-pick -n`? Default: yes (local only, never pushed).
Q-3 Should the seat finish its plants on the old base first (evidence of V on M0, 1 pass), then re-run on M0b? Default: addendum says apply at the next boundary and not start a new plant run, which cuts the old-base work off.
Q-4 If the gate passes and a26bee7e is squashed to main before the seat READY: the addendum tells it to STOP on `compare a26bee7e...main` ahead/behind 0; a squash is NOT an ancestor, so that test will not fire. Default: Tuesday sends the MAIN addendum on landing, and the seat's main check (`compare 77f56644...main` names a property path) catches it.

UNMEASURED
- Whether V is committed in the seat's tree, what the seat's current uncommitted state is (I may not read its tree; fence 3 and the seat's STATUS stops at 14:10).
- Whether V touches AppShell.tsx:166, :215-218 or the spec lines above (the conflict surface is DERIVED from the kit's property list, not from V).
- The round-2 gate's verdict; whether b1204 moves again.
- The elapsed wall time the re-run needs.

OUTSIDE THE FENCES: none. Reads: DRAFTER_RULES, the kit, ADDENDUM-1, both STATUS files, the heartbeat/ls of `.tools/b1272` (read-only listing), `gh api -X GET` only. Scratch copies of raw files and the patch were written to the session scratchpad, not the repo.
