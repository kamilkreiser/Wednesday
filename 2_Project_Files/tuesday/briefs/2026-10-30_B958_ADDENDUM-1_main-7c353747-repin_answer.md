From Tuesday (the Datasec coordinator seat) to SEAT-G225, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B958. Binding. The answer to your last line ("relaunch B958 re-stamped for 7c353747 with globals.css allowed, or do you want it read first?"). Tuesday read your STATUS and the sources below read-only, and touched nothing of yours.

**Answer: NO relaunch. RE-PIN in this seat. Pin main `7c353747a360353653dbf1aa2e7ea3cd3aa06cd4` and judge the comb (head `747eae29714c360e177af06ce9eb57c902032b92` merged onto `7c353747`, built in your own worktree) as the landing tree.** For this gate, the `globals.css` move is a named move, not a STOP. Your refusal was correct by your kit. This round has not started, so it is still round 1 of 2.

Facts Tuesday measured (repeat each yourself):
- `gh api -X GET repos/datasecau/HPSM-POC/compare/332dcc6f...7c353747 --jq '.files[].filename'` lists 4 files. The first is `web/src/app/globals.css` (PR #250: three `@source not` lines that keep unit-test files and `web/e2e` out of the Tailwind source scan). The other three are PR #248's `partner/ActionPlanScreen.tsx` and its restyle test, and `shell/HpLogo.test.tsx`.
- `pulls/254/files` lists 4 paths. Their intersection with those 4 is **0**.
- #250 removed 31 class rules whose classes no product file used as class text. Tokenised on whitespace, quotes and brackets, #254's 203 added patch lines hold **0** of those candidates. Control: the same tokenisation finds `min-h-11`, `gap-3` and `text-2xl` in those lines. #254's classes live in product files, which the scan still reads.

What changes in your run:
1. Replace every pin of main with `7c353747...`. Fetch once under your lock with the explicit refspec, then build comb with `merge-tree --write-tree` first (a conflict is a STOP).
2. In your CSS or class checks, confirm on the BUILT stylesheet of comb that every class #254 adds is emitted. Name any that is not; that would be a finding, not a STOP.
3. Your round count, overlap and CI reads are as the kit says. Also read open PRs #255 and #256 (new since your draft) with the same intersection program.
4. If main moves AGAIN before your verdict, name what moved. STOP only if a moved path is one of #254's 4 or on your kit's main-moves list other than `globals.css`, AND the comb no longer merges cleanly. Otherwise re-pin once more and say so. A second re-pin is a STOP.
5. Hard stop: your kit's minutes, counted from your re-start `date` (write the absolute clock in STATUS).

Everything else in B958 stands: tier 2, round 1 of 2, findings only. No merge, push, PR comment, Jira write, deploy or message. Landing is Tuesday's.
