From Tuesday (the Datasec coordinator seat) to SEAT-H68, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B937. Binding. Answers your STOPPED line "D-7: has B930 landed?".

**No. B930 has NOT landed.** Its PR is #249 (`b930/...`, head 7ae229e9), and its QA gate (G218, brief B941) is still running at 15:0x AEDT 2026-10-30. Check it yourself: `gh api -X GET 'repos/datasecau/HPSM-POC/pulls?state=closed&per_page=20' --jq '.[] | select(.number==249) | .merged_at'` prints nothing while it is open.

What moved since your base: PR #244 (H3 primitives) landed. HPSM-POC main is now `7365165d50193082ec3daf6eca137cd0ff0d4588` (parent `e21d8044`), and it changes only `web/src/components/customer/parts.tsx`, `parts.restyle.test.tsx`, `web/src/components/ui/Table.tsx` and `Table.test.tsx`. None of them is one of YOUR PATHS. Do not merge it now; the D-7 ADDENDUM will name the main you merge.

**What you do now:** nothing more on the branch. Stay parked, with your pushed head `0bcfb96` unchanged, and keep the D-7 rows RED exactly as your STATUS describes them. When #249 lands, Tuesday sends ADDENDUM-2. It will name the new main (ONE `git merge --no-ff --no-edit <main>`, never a rebase), give the D-7 tail lines (`returnPath.ts` RETURN_SEGMENTS "security", and the `nav-dead-ends.test.ts` floor of 5 with its comment), and tell you to re-run your checks and end with READY FOR QA.

Your Deferred item (the a11y and journey 30 s limit under load) and Open items (a) to (d) are noted by Tuesday. Tuesday files them; they do not need you.

Nothing else in B937 changes.
