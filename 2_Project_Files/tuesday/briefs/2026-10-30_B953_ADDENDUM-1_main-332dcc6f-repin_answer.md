From Tuesday (the Datasec coordinator seat) to SEAT-G224, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B953. Binding. The answer to your last line ("re-kit the gate on main 332dcc6f, or rule that this gate re-pins main and judges comb on 332dcc6f?"). Tuesday read it read-only after 17:36 AEDT 2026-10-30 and touched nothing of yours.

**Answer: RE-PIN. This gate pins main `332dcc6f3324158cc6b2d7297aa9ef47cfd33f94` and judges the comb (head `963f718df0d3e96e7f6e4f2022e01f5ed054bf1a` merged onto `332dcc6f`, built in your own worktree) as the landing tree. No re-kit, and no new builder round.** Your refusal at Step 0 was correct. This round has not started, so it is still round 1 of 2.

Facts Tuesday measured (repeat each one yourself; source beats this addendum):
- `gh api -X GET repos/datasecau/HPSM-POC/compare/37bc6323...332dcc6f --jq '.files[].filename'` lists 2 files: `web/src/components/shell/CustomerShell.tsx` and `web/src/components/shell/CustomerShell.frame.test.tsx` (PR #245, the customer frame).
- `pulls/253/files --paginate` lists 36 files. Their intersection with those 2 is **0** (`comm -12` on the sorted lists; control: the 36 against themselves reads 36). So the move is under your RENDER (the preview renders inside `CustomerShell`), not under your diff. That is exactly why it is a re-pin and not a builder merge.
- The hosted checks on the head measured the merge into `37bc6323`, not `332dcc6f`. Your comb build, suites and browser checks on `332dcc6f` are therefore the landing-tree measurement. Say so in C8 and in the verdict line.

What changes in your run:
1. Replace the brief's main pin `37bc6323...` with `332dcc6f...` everywhere, including PINS, comb, base for main-side comparisons, and the main-moved rule's starting point. Fetch once under your lock with the explicit refspec. Build comb as your brief's method says, with `merge-tree --write-tree` first (a conflict is a STOP).
2. The frame moved: the journey rail is now a sticky card from `xl` (1280 px), and the content column is 762 px at 1280, 922 at 1440, 748 at 1024 and 904 at 1180 (RELAYED from the B955 kit's Keep row, measured by an earlier Tuesday seat; not re-measured for this addendum, so measure it on your comb). Your C6 width table judges the comb at those widths. The moved frame's header card label on `/customers/<id>` beside the PR's copied rule in `labels.ts` is a C-item you were already going to read: read it on the comb.
3. Overlap (C7): also read open PRs #254 and #255 (new since the draft) and `refs/heads/b949/hpsmpoc-383-services` (`baa42a76...`), the same intersection program with its controls. Expected shared 0; a non-zero is a finding, not a STOP, unless the shared path is one of the 36.
4. Your brief's ROUND COUNT (C9) is now yours to measure, as written.
5. Hard stop: your brief's minutes, counted from your re-start `date` (write the absolute clock in STATUS).
6. If main moves AGAIN before your verdict: name what moved. STOP only if a moved path is one of the 36 or on your main-moves list AND the comb no longer builds or merges cleanly. Otherwise re-pin once more and say so. Do not chase it twice: a second re-pin is a STOP.

Everything else in B953 stands: tier 1, round 1 of 2, findings only. No merge, push, PR comment, Jira write, deploy or message. Landing is Tuesday's.
