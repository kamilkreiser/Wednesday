# B256 DRAFTER REPORT (HPSM-POC hosted deploy 787d159)

**Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B256_SEAT-F_hpsmpoc-hosted-deploy-787d159.md`, 90 lines. sha256 `912da8ad9d222349f48ad38a356c11ff35dcfef761526e14203ae71e44640342` at 04:09Z (before this report was written).
**Template:** B253 brief (read whole) + `B253_STATUS.md` (read whole, 256 lines) + `B255_STATUS.md` (verdict block `:1-12`, merge/post-merge `:216-224`, `:273-287`, NEW WORDS `:227-231`, verdict `:327`).

## Measured (drafter's own reads, UTC 2026-10-17)
- `ls-remote origin refs/heads/main` = `787d159089d8a774801b03e959f269c8a12e4ce1` (04:04:43Z).
- GitHub API (project `GH_CONFIG_DIR`, `kamilDatasec`):
  - PR #157 merged 04:03:43Z, head `7a2c7ae5b9af…`, `merge_commit_sha` `787d159…`.
  - Commit `787d159`: tree `a5ac7f54761e28564b4c6c6cdb9399f84de74013` (= B255 `:217`), one parent `72073da`, 3 files +103/−4 (2 `.csproj`, 1 test).
  - Compare `72073da...787d159`: ahead 1, behind 0, 1 commit.
- CI on `787d159`: `ci` **39001143811 in_progress** (04:09:03Z); CodeQL "Push on main" **39001143695 completed success** (04:09:03Z; it was in_progress at 04:06:52Z). PR runs: ci 39000249834 success, CodeQL 39000248415 success. Open alerts 0 (control: 1 in any state). Open PRs 0.
- Way back: run 38974522883 (`72073da`) `deploy-web-72073da…` 15,358,881 B expires **2026-10-23T22:21:13Z**; `deploy-api-72073da…` 49,387,048 B expires **2026-10-23T22:27:53Z**; `expired=false` (04:05:02Z). Fetched copies in `.tools/wt-B253/out/deploy-packages/72073da…/` (web.zip `b7a534f8…`, api.zip `c9f02f92…`, from `SHA256SUMS`). Second fallback run 38470487072 (`d916baf`): web expires 2026-10-20T21:33:27Z, api 21:39:15Z, `expired=false`.
- `787d159` absent from the local object store (`2_Project_Files`, `.tools/b255/repo`, `wt-B253`, `wt-B249`). `wt-B253` HEAD `72073da`, 0 tracked changes; `wt-B249` HEAD `d916baf`, 0. `.tools/b256`, `.tools/wt-B256` absent; `.tools/.git-lock` absent.
- Ports: `lsof` 04:06:11Z, 6900–7099: only 7000 (`ControlCe`). Brief assigns **6990–6999**.
- Pane: `cockpit.sh status` 04:06Z lists no HPSM-POC pane: `Datasec/HPSM-POC-F4` free.
- `brief_seat.sh`: item 1 at line 12, exports at 25-26 (confirmed); `PLAYWRIGHT` 0 hits (B253 Open 4 still open; the brief tells the seat to set it).

## Traps written into the brief
1. CI not yet green at drafting: the seat waits for `ci` 39001143811 success before step 5; a red is a STOP, never a re-run.
2. The risky-path query now FIRES on 2 `.csproj` files (unlike B253). Expected; the seat reads both diffs whole and stops on anything beyond the Pkcs pin + the rank target.
3. B255 post-merge check on the real `deploy-api-787d159…` api.zip: 2/2/2/121, `grep -c … || true`, never under bare `set -e`; 2/0/2 = DLL shipped unlisted = FAIL. Control: the `72073da` zip gives 0/0/0/119.
4. Web package: the range has no `web/` path, but CI rebuilt it. Zip `entry_time` (MANIFEST) and probably the Next build id differ; byte-equality beyond that is UNMEASURED. The seat lists the differing paths; anything other than build-id files → STOP.
5. Rollback with `--clean` must remove the 2 Pkcs paths (api 119, site-only 0). Rolling back to `d916baf` also undoes #156.
6. Runtime stays 10.0.12; which Pkcs loads on hosted is NOT measurable without a hosted probe (forbidden). Evidence = package on site + B255 container proof (`:165-166`). HPSMPOC-254 stays OPEN.
7. Playwright browsers path (B253 Open 4); feedback count mid-render (B253 Open 5).

## Not done / UNMEASURED
- No `az`, no HTTP to any hosted site, no write under `!CODING/`. The `787d159` deploy packages (not created yet), hosted today, records `origin/main` today, Tuesday's completion-check record.
