# B166 drafter report: hosted deploy of MPS main 12f8e566 (seat K2)
Drafted 2026-10-17 09:28–09:45 AEDT by a Tuesday drafter. Datasec / MPS Commercial Calculator only. I wrote two files, both in Tuesday's tree: the brief and this report. I wrote nothing under `!CODING/`. I ran no `az`, made no HTTP request to the hosted site, and ran no fetch, checkout or push in the project repo. Git use was `--no-optional-locks` read verbs only. `gh` use was `api` GETs plus one `run view --log` (a GET), all with the project's `GH_CONFIG_DIR`. I printed no secret.

**Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B166_SEAT-K2_mps-hosted-deploy-12f8e56.md` (60 lines, modelled on B156).

## Measured (this session)
- **Main:** `ls-remote` = `12f8e566398bc83ea5c2be4d662f64ee9fbdbbfe` at 09:28:51 AEDT; `gh api …/git/ref/heads/main` gives the same. Tree `0a0400618f54…`, one parent `798fe98493cd…` (#72). `0f8ad97` is an ancestor (rc 0).
- **Range 0f8ad97..12f8e566:** 31 commits (first-parent 31 = all 31), PRs #43–#73. `gh compare` gives ahead 31 / behind 0 / 147 files. Local shortstat: 147 files, +8,605 / −905.
- **Infra, .github, scripts, tools, settings:** `infra` and `.github` have 0 changes. `scripts` + `tools` have 10 changed files (listed in assert 5). `appsettings*` 0. `migrat` 0 at both ends.
- **Config keys:** `MpsCalc:` keys 13 = 13 and wide form 14 = 14 (`diff` rc 0 for both). No new key.
- **Stores:** 22 `src` files changed. The store readers among them are `CatalogueOverlayStore.cs` (#59) and `ReferenceStoreDocument.cs` (#69; its new field is optional with default `[]`, `:83`). `QuoteFileStore.cs` is unchanged.
- **Rollback hazard (found):** snapshots are read with `ApiJson.Options`, which has `UnmappedMemberHandling.Disallow` (`QuoteFileStore.cs:365`, `ApiJson.cs:20`, the same at both ends). Quote files use `ReferenceStore.JsonOptions`, which has no such rule. So after a rollback, `0f8ad97` would refuse a post-deploy snapshot that carries a new member. The brief makes the rollback precondition cover snapshots explicitly.
- **PRE-1 in the deploy:** `deploy-from-ci.sh:96-123` @12f8e566. The overlay VFS path is `:28`; the copy is written at `:111-113`; the 404 line is `:116`; the STOP is `:122`. The script has no fallback, and a STOP means nothing was deployed.
- **[B105-4] overlay path setting:** B156's end copy of the settings (`B156_evidence/30_end_appsettings.tsv`, 2 columns, name + value) holds `MpsCalc__CatalogueOverlay__Path` equal to the bicep value `/home/data/catalogue-overlay/` (`showcase.bicep:83`). I compared it in memory and printed only "EQUAL". The seat re-asserts it live.
- **CI on 12f8e566:** 8 of 8 completed success. ci run `38967822861` (push, main, attempt 1); CodeQL run `38967822674` (4 Analyze jobs). Open code-scanning alerts on main: 0.
- **CI artifact:** `deploy-mpscalc-12f8e566…`, 3,144,013 B, not expired, expires 2026-10-23T21:17:27Z. Package job: SDK 10.0.402 / runtime 10.0.13; `mpscalc.zip` sha256 `cdfe793e…1d00`, 3,142,810 B, 50 files.
- **Artifact contents:** I downloaded it with `gh api …/artifacts/12076051906/zip` into Tuesday's scratchpad and diffed it against the rollback zip:
  - Files: 50 = 48 + exactly the 2 Pkcs paths. wwwroot stays at 8.
  - Changed: 5 files. `runtimeconfig` is byte-equal.
  - Pkcs: deps.json has 2 `Pkcs/10.0.13` keys, fileVersion `10.0.1326.50504`.
  - Bundle: `index-CUvXVpZl.js`.
- **Rollback package:** B156's `0f8ad97` zip re-hashed read-only: `7a5262fb…8570`, 2,865,185 B, 48 files (8 wwwroot). `.RUN` = `38840260381`; worktree HEAD `0f8ad97`, porcelain 0.
- **List W (words):** I counted strings in the CI package and in B156's live copy (`.tools/qa-B156/live`, 48 files) as the control:
  - New words present: 23 of 23 (19 web + 4 server words read as UTF-16LE in the DLLs); control 0/23.
  - Retired words: 0 of 2 present; control 2 of 2.
  - Each string has its source `file:line` at 12f8e566 in the brief.
- **B156's word tools, run on the CI package** (read-only; `python3 -I` on my scratch copy):
  - `words156.py`: A 4/4, B 0/3, C 5/5, C-ctl 1/1, D 10/10.
  - `fbwords73.py`: 5/5.
  - `words55.py`: **52/54**. A18 and A19 are absent because the Home sentence is now templated (`Dashboard.tsx:101`, list W item 31). The brief expects 52/54, so B156's 54/54 would otherwise have been a false STOP.
- **Shared machine:**
  - Panes: `Datasec/MPS-LD` %17, `Datasec/MPS-LE` %18, `Datasec/MPS-V2` %40 (B165). No `Datasec/MPS-K2` pane exists (`tmux list-panes -a -F '#{@cockpit_name}'`).
  - Heavy slots: **only `.tools/heavy-slot-1` exists**, held by B165 at 09:31:21. Slots 2 and 3 do not exist.
  - The root checkout is on `b03/api`.
  - `cockpit.sh add` takes any `<name>` string (`:225-228`); B156 used `Datasec/MPS-K`. It refuses when the name is already present and goes through `usage_gate.sh` (`:151`).

## UNMEASURED (left to the seat)
- **Hosted state since B156:** served bundle, store counts, whether `overlay.json` exists, settings, posture, host runtime patch.
- **Pre-swap counts:** P-1, PRE-1, and the count of negative-value drafts (card consequence 7). The seat counts negatives from its backup in memory, counts only. If it cannot place the field path with a working control, it writes UNMEASURED.
- **Which Pkcs assembly the running app loads.** No probe is allowed (it would be a setting change). B160 FOUND 2 measured that the API loads neither Pkcs nor Xml on any measured path.
- **New start-log lines** that #59/#62–#66 may add.
- **Anything that needs a signed-in browser:** Acting-as gone for a 4-role sign-in, the (i) hints, rendered proposals (a proposal GET writes an event), and a refused negative shown on screen (needs a write).
- **POST-1 response keys** after #51.

## Traps (put into the brief)
1. **`words55.py` reports 52/54 on the new package.** A18/A19 are templated now. Expect 52/54 and explain it; a 54/54 expectation would STOP a good deploy.
2. **`deploy` rc 1 now also means "PRE-1 stopped, nothing deployed".** The seat then checks against B156's package to prove `0f8ad97` is still live, and writes STOPPED. B156's "whatever it returns, run `check`" would have checked the wrong package.
3. **If `overlay.json` exists, STOP.** B161-1: PRE-1 lets through 16 forms that 12f8e566 refuses at boot. A present overlay could pass PRE-1 and then have the app refuse to start.
4. **Overlay copy:** record its path, size, sha256 and modes; never open, move or delete it. Kam's retention ruling (b) is MPSCALC-203's job.
5. **No local-build fallback.** Kam's option says "from the CI package", and a local build would need a heavy slot that B165 holds. `fetch` fails → STOP.
6. **The leak check will meet 2 new real customer rates** at `infoHintWords.ts:61,67` (list W 41-42, approved by Kam). The seat adjudicates them by line and never prints the figures.
7. **Rollback precondition covers snapshots too** (the Disallow reader at `0f8ad97`).
8. **The B156 tool set lives at `.tools/qa-B156/tools/`.** Copy it from there, not from qa-B92.

## Things Tuesday should know (none blocks the launch)
- **"Deals closed" is still on screen** at `QuoteList.tsx:148` @12f8e566 (a quote-list title for a won-period filter). List W item 31 says Deals won/lost "replace 'Deals closed'"; that is true on Home only. Kam approved list W as written, so this is a words/records note, not a STOP. The brief expects a count of 1 (control 3).
- **Hint words 41-42 carry the review quote's real customer rates in code.** Kam's yes on list W covers them, and the card text said so.
- **Option b's sha `798fe98`** was not ruled. The brief deploys `12f8e566` only.

## Launch command (checked: no `Datasec/MPS-K2` pane exists; the name form is accepted)
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-K2 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B166_SEAT-K2_mps-hosted-deploy-12f8e56.md'"
```
Before launch, re-run `git --no-optional-locks -C '<project>/2_Project_Files' ls-remote origin refs/heads/main`. The brief handles a moved main (deploy 12f8e566 only, or STOP), but Tuesday may want to know first.
