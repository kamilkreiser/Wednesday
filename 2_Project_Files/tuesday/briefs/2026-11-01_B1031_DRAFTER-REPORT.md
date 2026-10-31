STARTABLE: YES (once Tuesday fills the 12 stamp slots; no blocker found)
# B1031 drafter report: SEAT-D43, HPSM-POC review site (UAT): dry run, first-click fix, keep-awake database

**BLUF.** Kit written: `2026-11-01_B1031_SEAT-D43_hpsmpoc-uat-deploy-firstclick-keepawake.md` (139 lines, sha256 `7ffa8c43...`, `.pre-stamp` byte-equal by `cmp`). Pin `S` = `77c3132e213b24616e6f1af9379d2fee66c889b7` (main head). It is the first commit that holds both approved changes (#266 = `de6f83fb`, #268 = `77c3132e`), and it does not hold PR #269. The order is: what-if dry run (read-only; stop if Azure refuses) -> CI packages to UAT -> a wake test on the real sleeping database -> ONE `az sql db update` (`--use-free-limit false --auto-pause-delay -1`) -> a 20-minute quiet-spell proof. **I chose a single database update over a template deploy (D-3).** The kit also ships other merged work: #265's product code and #267's one product line ride in the web package (slot 8). The demo is not touched at all.

## Facts (instrument; control)
- Main head `77c3132e`, 1 parent `e0b93957`, verification valid (`gh api -X GET commits/main` 10:09 AEDT under the project `GH_CONFIG_DIR`; account active).
- UAT runs `e8ac3f29` web + API, build `_GKBLKGPzs-8-0fDuudGc`, deployments `33f90a49...` / `14f6928d...`. Source: RELAYED from `Briefs/2026-10-31_B971_STATUS.md:273,144` and records C-250. Newest deploy STATUS is B971: `grep -l '^(DEPLOYED|ROLLED BACK|PARTIAL): '` listed B804, B810, B836, B874, B971.
- `compare e8ac3f29...77c3132e`: ahead 8, behind 0, 28 files, each commit one parent. Control: the reversed compare reads behind. 0 `api/` paths (control: `web/src` 22). Product files: `bff.ts`, `readRetry.ts`, `proxy.ts`, `SidebarMenu.tsx`, `remediation-store.ts`, plus the three infra files. Diffs read: 0 new customer-facing strings.
- PR #269 is open, base = `S`. `compare S...7f0d832d` ahead 4 behind 0 (control: reversed behind 4). So #269 is NOT in `S`.
- Gates: all 8 verdict lines read, and each head equals its merged head. The run for B1005 (#267) is named by branch.
- CI: run `41218555786` completed/success. All jobs success except dependency review, which was skipped. Deploy artifacts are not expired (they expire 11-07). Open code-scanning alerts 0 (control: fixed returns 1).
- Way back on disk: the `e8ac3f29` packages under `.tools/b971/repo/out/deploy-packages/`. sha256 `32c005e1...` / `a7ae7de7...`, which equals `B971_STATUS.md:47`.
- Tenant `ec01829b...`, subscription `a6b8fe11...`, login role Owner. Source: records `CLARIFICATIONS.md:26-28` (C-07). Which Datasec environment this is: not asserted (`:1912`).
- Model: Opus, `model-routing.md` lines 96, 47, 94, 145. `claude-opus-5-5` from `models_latest.json:17`.
- Seat suffix D43: `grep SEAT-D43` over the briefs found 0 (control: D42 found 3). B1031: 0 refs (control: B1028 found 2).
- Ports 9740-9749: 0 listeners (control: 13 without the range). Kit scan names only B971 (its seat is closed) and one control mention in B985.

## D-decisions (in the kit)
D-1 pin `S`. D-2 the dry run is a what-if of `S` plus a control what-if of PREV's template; only the database's two values may differ. D-3 the write is the database update, not a template deploy (B836 found 21 Modify and a masked app-settings rewrite). D-4 no setting write. D-5 the order above. D-6 the platform-image rule covers both apps, widened as in B971 ADDENDUM-1. D-7 ways back, plus a cost brake that the seat never runs. D-8 the facts about the database's wake. D-9 one attempt per write. D-10 no records.

## Q-questions (default applies if Tuesday is silent)
- Q-1 (slot 8): ship #265 (unknown-customer 404 on the security views; refusal of invisible-only evidence) and #267 (one product line) with the fix? Default **YES**: no sha holds #266 without them, and both are gated. `HOLD` deploys nothing.
- Q-2 (slot 7): a database update instead of a whole-environment template deploy? Default **YES**. A template deploy would need its own brief.
- Q-3 (slot 12): if the dry run is refused, still deploy the first-click fix? Default **STOP ALL**, as the card says.
- Q-4: if `az sql db update --help` lacks `--use-free-limit`, the seat STOPs and asks. Default: stop; no `az resource update`.
- Q-5 (slot 10e): run the wake test? It waits up to 45 minutes for a pause. Default **RUN**.

## UNMEASURED
Every hosted fact: no `az` and no HTTP from me. Whether the what-if passes or the update is accepted. Whether the `--use-free-limit` flag exists in the installed CLI. Today's UAT settings, images and database state. The real monthly cost. Whether #265's 404 renders as designed on the host.

## Outside the fences
None written. I made only read-only `gh api -X GET` calls and file reads. Scratch copies of infra and records are in `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/c9371317-968c-4c10-88d6-79a675bd3109/scratchpad/b1031/`.
