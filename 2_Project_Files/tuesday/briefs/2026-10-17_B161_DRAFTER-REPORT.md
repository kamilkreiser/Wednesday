# B161 drafter report · 2026-10-17 ~05:5x AEDT · for Tuesday
Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B161_SEAT-T_mps-gate-b160-183-105.md` (346 lines). It is NOT launched.

## Launch command (form: `brief_seat.sh:4`)
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-T "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B161_SEAT-T_mps-gate-b160-183-105.md'"
```

## Instruments (all read verbs on the project checkout; write verbs only in my throwaway clone)
- `git --no-optional-locks -C <repo> ls-remote origin` at 2026-10-17 05:43:59 AEDT (165 refs, saved to this session's scratchpad `lsremote-b161.txt`). All three heads = READY lines; main = `a6813d70407ebfbfbe2b0e9b130c0a787508d986`.
- Throwaway `git clone --shared --no-checkout` at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/4fc01a1b-80dc-4d56-906d-73b9eb0776ff/scratchpad/b161-clone`, push URL `DISABLED` (`remote -v` read back). `merge-tree --write-tree` and `commit-tree` scratch commits there only, never pushed.
- Slots, load and ports at 05:46: slot 1 = B103 lane D (05:44:45), slot 2 = B104 lane E 147r2 (05:45:30), slot 3 free; load 5.85; `lsof -iTCP:6780-6789 -sTCP:LISTEN` rc 1.
- No `gh`, no HTTP, no Jira, no az.

## Merge predictions vs current main `a6813d7` (a READING; the gate re-measures)
- 160 alone: clean, tree `53aa5a8d`. 183 alone: clean, tree `d9641fa6`. 105 alone: clean, tree `d12c37cd`.
- Sequence 160 → 105 → 183: clean (`53aa5a8d` → `a54cd0f5` → `323983fc`).
- 105 after lane D's in-progress `b103/mpscalc-158-target-click-r2` @ `acd44c9…`: clean (`1f58dbd5`). Lane D's ADDENDUM-3 work may still touch `QuoteEndpoints.cs`.
- No textual conflict. But see trap 1: 183 merges clean and is semantically stale against main.

## Traps found (each written into the brief)
1. **183's PRE-1 is out of date against main #59 (`169e5a8`) in a way its drift test cannot see.** Main now refuses at start a row with no `itemClass`, an integer `itemClass`, and a repeated property name (`CatalogueOverlayStore.cs:435-447`, `:463-486` @ `a6813d7`). PRE-1 @ `41af1e3` counts an absent `itemClass` as INFO (not a stop), with the comment "opens as device" (`deploy-package.py:431`, `:458`). It accepts integers (`:461`) and cannot see repeated names (`json.load`, `:471`). The drift test only compares `ShowsNothingRanges` and the `ItemClassDto` names (`test_deploy_pre1.py:125-134`), and both are unchanged, so CI stays green. This is my reading, not a run: Check 6 measures it. It is `[B107-2]` widened. Today it does not bite: hosted had no `overlay.json` at B156 (`B156_STATUS.md:186`).
2. **The "overlay changed" stop in your task list does not exist in the code.** `deploy-from-ci.sh` @ `41af1e3` reads the overlay once, before `az webapp deploy` (`:121-128`), and never re-reads or compares it. The brief makes the gate measure the race (Check 5e) and REPORT it, not grade a missing feature, unless MPSCALC-183's acceptance names one.
3. **The saved copy's directory is not protected by the umask.** `mkdir -p "$DIR.live"` (`:111`) runs outside the `( umask 077; … )` subshell (`:113`). The file should be 0600, but the folder takes the operator's default umask. Check 5 measures both modes, whether a copy stays on the STOP and 404 paths, and same-second overwrite. The default place is `<repo>/.local/deploy-packages/<sha>.live/`, which is git-ignored by `.gitignore:16-17` @ `41af1e3`.
4. **"48 → 50" is stale.** B160 measured 48 → 50 on main `621e330`'s package. Main has moved 23 commits since then. The brief expects (main `a6813d7`'s CI package count) + 2, measured by a `gh run download` of main's own artifact, and gives a fallback if it has expired.
5. **160's red only shows on SDK 10.0.402.** On 10.0.401 (`.tools/dotnet`) the base already keeps the DLL (`B160_STATUS.md:56`). The gate installs its own 10.0.402 into `.tools/qa-B161/`. B160's install in `.tools/b160/` is another seat's tree, so the gate must not use it.
6. **183 needs a curl route without a fake curl.** The script forces `--proto =https`, and the host regex forbids a port (`deploy-from-ci.sh:92`). The brief routes the REAL curl through a scratch `CURL_HOME/.curlrc` (`connect-to`, `cacert`) to the gate's own HTTPS fake on 6780-6789, with `.invalid` host names. A no-`.curlrc` control proves nothing reaches a real host. If routing fails, the fallback is a shim, and the gate must say so.
7. **105's duplicate route also calls `InRange`** (`:495` on the merged tree). Duplicating a stored quote that holds a negative is therefore refused, while `new-version` and `calculate` do not call it. Check 7c tabulates this.
8. **105 at `QuoteApiTests.InputRange.cs` is +49 −0, and 160's `PublishOutputTests.cs` is +32 −2** (numstat). The gate names those 2 removed lines.
9. Last session's gates had hold slips: zsh word-split worktrees, `rm -f` by B158 and B159, and a green with 0 tests run by B157. The brief bans `rm` outright, requires bash, and requires a count of tests run on every result line.

## Choices I made that you may want to overrule
- **Network for the gate:** `gh` read-only (advisories, check-runs, run logs, and a download of main `a6813d7`'s package only), the official `dotnet-install.sh` into the gate's own tree, NuGet/npm, and optional Docker pulls for a Linux leg. Yesterday's gates had no `gh` grant. The task's "advisories re-read from the advisory API" and "package job log" need it.
- Merge order in the MERGE line: 160, 105, 183. They are independent, so any order works.
- `baseChargeOverride` and `[B107-2]`'s scope stay REPORTS, not grades, because both are open questions for you.

## What I could not verify
- Jira acceptance for MPSCALC-183 and -105, and whether any MPSCALC ticket covers B156 F-1 (no Jira call). The gate reads them.
- CI check-runs on the three heads and on `a6813d7`; whether main's `a6813d7` package artifact exists; the SDK/runtime CI installs today (no `gh` call).
- Any run: no build, test or script was executed. Trap 1 and trap 3 are readings of the source.
- Whether `curl` honours `.curlrc` alongside `--config -` on this machine's curl (the gate's control decides).
- The 183 copy's real directory mode (it depends on the operator's umask).
