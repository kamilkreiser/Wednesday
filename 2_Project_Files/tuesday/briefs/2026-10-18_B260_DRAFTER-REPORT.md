# B260 DRAFTER REPORT (HPSM-POC hosted deploy of the PR #158 squash)

**Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B260_SEAT-F_hpsmpoc-hosted-deploy-pr158.md`, 105 lines, UNSTAMPED: placeholder `@MAINSHA@` on 22 lines (30 occurrences). sha256 `c3c292991051cfcbfc74552c07252414559ee8e036bce000dc18d9b5c59b20f9` before this report was written.
**B number:** B260 was free in both folders (`tuesday/briefs/` and `HPSM-POC/1_Project_Definition/Briefs/`: 0 `B260` names).
**Template:** B256 brief (read whole) + its DRAFTER-REPORT + ANSWER-1 (CI green after a re-run) + ANSWER-2 (Next.js per-build keys expected) + `B256_STATUS.md` (read whole, 281 lines) + `B259_STATUS.md` (read whole) + `B258_STATUS.md` (read whole).

## Tuesday must stamp / decide
1. **Stamp `@MAINSHA@`** (all occurrences, 40 hex) after the merge, once `git cat-file -p <sha>` reads `tree a083966f7157f66d63604d3338d1c7f135bd5ea4` with one parent `787d159…`. The seat refuses if the joined placeholder survives or main differs. Keep a `.pre-stamp` copy as usual (the brief's refusal check uses it as its control).
2. **PR #158 is not mergeable yet:** open, `mergeable_state` blocked, `ci` 39076341763 and CodeQL "PR #158" 39076340180 in progress at 22:47Z. **The check-run named `CodeQL` read `completed neutral`** while `Analyze (csharp)` was still running. Confirm its final conclusion before you merge.
3. **Completion check:** the seat looks for Tuesday's record of it, and if none is found it notes that under Open (it does not block, as in B256).
4. **Web compare rule is new (Tuesday may want to rule it):** real server code changed, so the brief splits differing web files into three classes: build-id only; the 3 per-build-key files (ANSWER-2); server-bundle files that hold the guard/formGate code. Any `.next/static/` (browser) file that differs beyond the build id is a STOP. This assumes formGate/guard never reach a client chunk. Drafter evidence: both files are imported only by `web/src/server/bff.ts:14-15` and `web/src/server/auth/entra.ts:17`. Whether Next.js still puts them in a client chunk was NOT measured.
5. **Connection: close on hosted: NOT TESTED by design.** The template's live check is GETs only and exercises no form route, so the brief forbids any POST.

## Measured (drafter's own reads, UTC 2026-10-17T22:47Z = 09:47 AEDT 18 Oct)
- `ls-remote`: main `787d159089d8…`, `b258/bff-imports-zstd-census` `7fa59c5f65c9…`.
- `.tools/b259/repo` (read verbs, `--no-optional-locks`):
  - `rev-parse 7fa59c5^{tree}` = `a083966f7157f66d63604d3338d1c7f135bd5ea4` (= the 12-hex prefix at `B259_STATUS.md:16`).
  - `diff --stat 787d159 7fa59c5`: 10 files, +411 −27.
  - Risky pathspec: exactly `M infra/tests/test_deploy_hpsmpoc208.py`, `M scripts/deploy-package.py`.
  - `deploy-package.py` diff: only `read_oryx_tar` changes (the SKIPPABLE constant, the docstring, the skip loop).
  - `ImportEndpoints.cs`: one `catch` line plus 2 comment lines.
  - Added config-pattern lines in `api/src` + `web/src`: 0. `Program.cs` / `*Module.cs` changes: 0.
  - `ImportsEnabled` false at `appsettings.json:17`; the gates are at `AssessmentModule.cs:123` and `ImportEndpoints.cs:422`.
  - The 3 guard strings count 3 lines in `guard.ts` at both commits.
- `wt-B256/scripts/deploy-from-ci.sh` calls `deploy-package.py` `verify` (`:43`) and `live-check` (`:96`). So the new reader judges the live sites, and the brief has the seat compare the old and new readers on the hosted download.
- Way back: run 39001143811 artifacts `deploy-web-787d159…` 12089850327 (15,358,900 B, expires 2026-10-24T04:11:54Z) and `deploy-api-787d159…` 12089267777 (49,629,083 B, expires 2026-10-24T04:12:30Z), `expired=false`. Second fallback `72073da` (run 38974522883): web expires 2026-10-23T22:21:13Z, api 22:27:53Z, `expired=false`.
- `wt-B256` HEAD `787d159…`, 0 tracked changes; its `out/deploy-packages/787d159…/` holds api, web, live, RUN. `.tools/b260`, `.tools/wt-B260` and `.tools/.git-lock` are absent.
- Records `datasecau/HPSM-POC-analysis` main `2e284455cc75897a879a66ba9a55e06e714599cb`, 1,342 lines. C-105 is at `:1235`, C-108 at `:1272`, and C-111 (the B256 deploy) at `:1320`.
- Ports: `lsof` 6900–7199 shows only 7000 (`ControlCe`). Block 6990–6999 is assigned.
- Pane: `cockpit.sh status` lists `tuesday`, `Datasec/NexusAI-O`, `fleet-monitor`. `Datasec/HPSM-POC-F5` is free.
- `brief_seat.sh`: exports at 25-26; `PLAYWRIGHT` 0 hits (the brief tells the seat to set it).

## What differs from B256
- Base `787d159` (hosted `LnYu4WmaU5Sh4wYdmvgTN`, deployments web `861d71cb…` / API `e48377b2…`); target is a placeholder; tree `a083966f7157…`; range is 1 squash commit of 6 tickets.
- The risky pathspec fires on `scripts/deploy-package.py` and `infra/tests/…`, not `.csproj`. The seat reads the script diff whole and checks old and new live-check readers agree on hosted (magic `28b52ffd`, so the skip loop is not entered).
- API package: the same 121 paths; only the 5 DLLs and 5 PDBs differ; `deps.json` is expected equal. The Pkcs post-merge check stays as a regression guard.
- Web package: real server code changed. The new 3-class rule is above.
- NEW WORDS: the 3 guard refusal strings sit on added lines but already exist at `787d159`. The seat proves they are not new.
- Way back is `wt-B256` / `787d159` (before 2026-10-24T04:11:54Z). The second fallback `72073da` also undoes the Pkcs files.
- Explicit: runtime card `hpsmpoc-hosted-runtime-10013-1017` is OPEN (10.0.12 stays). `ImportsEnabled` is read before and after, and anything that would change it is a STOP. No form POST, so Connection: close stays NOT TESTED.

## Not done
- No `az` at all (the resource names and IDs are copied from B256's STATUS, which measured them on 10-17). No HTTP to the hosted site. No write under `!CODING/`. GitHub reads were GET only. One scratch file holds a copy of CLARIFICATIONS.md in the session scratchpad.
