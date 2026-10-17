# B255 DRAFTER REPORT · HPSM-POC · QA gate (tier 1, round 1 of 2) on b254/pkcs-in-package @ 7a2c7ae
Drafter, 2026-10-17 12:53-12:59 AEDT. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B255_SEAT-G3_hpsmpoc-gate-b254-pkcs.md` (106 lines; B252 134). Nothing written under `!CODING/`; git read verbs only (`--no-optional-locks`), against `2_Project_Files` and B254's clone `.tools/b254/repo` (the branch object is only there); `gh api` GETs under HPSM-POC's `GH_CONFIG_DIR`; no Jira GET, no az, no hosted HTTP. My downloads (main's artifact, job logs) are in the scratchpad, not in any project: `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2392c438-09c4-4ba2-9b32-b68afb3a6e21/scratchpad/art-main/` and `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2392c438-09c4-4ba2-9b32-b68afb3a6e21/scratchpad/job-*.log`.

## Measured
- `ls-remote` 12:53:12: main `72073dace1635899e1262548e561781073b4c7b4`, `b254/pkcs-in-package` `7a2c7ae5b9afee35fa5fe5fd6e976a83721e5589` (both = the commission). `7a2c7ae` NOT in `2_Project_Files`' store; in `.tools/b254/repo` it is.
- `72073da..7a2c7ae`: 1 commit (parent 72073da), 3 paths, +103 −4; numstat Api.csproj 12/0, Assessment.csproj 6/4, PkcsInPackageTests.cs 85/0; head tree `a5ac7f54761e`. Target at `HpsmPoc.Api.csproj:25-29`; guard's SDK choice at `PkcsInPackageTests.cs:60`.
- Check runs on 7a2c7ae: 15 (14 success, 1 skipped). Open PRs 0, open alerts 0.
- Run 38991454533: `workflow_dispatch`, head 7a2c7ae, success, attempt 1. Job logs (with `--allow-escape-sequences`): api job 117274538073 `:140` runtime 10.0.13, `:151` SDK 10.0.402, tests 289/270/809/164/1446, `:405` 121 files sha256 `496a6d42…`; shard other-and-feedback 560 + 270. Main run 38974522883: api 1445, `:405` 119 files `c9f02f92…`; shard 559 + 270.
- CI installs the SDK with `install-dotnet.sh --channel 10.0` (setup-dotnet + `global-json-file`, global.json 10.0.401 `latestFeature`), i.e. the newest 10.0 SDK on the day.
- CI durations (job timestamps): shard other-and-feedback main 12:39 vs branch 11:55 (timeout 20); api main 13:39 vs branch 12:25 (timeout 25).
- Trx artifacts available: main api 12078274374, shards 12079330870 / 12079171095; branch api 12085866135, shards 12085304170 / 12085667455. Main deploy-api 12078234485 expires 2026-10-23T22:27:53Z.
- **Post-merge commands on main's real api.zip** (sha256 `c9f02f92…85c5e` verified): 0 / 0 / 0; controls ProtectedData DLL 1, `ProtectedData/9\.0\.11` deps lines 2; 119 files; `grep -c` on 0 → rc 1.
- Local `.tools/dotnet`: SDK 10.0.401 only, AspNetCore 10.0.12 only; `PlatformManifest.txt:42` Pkcs file version 10.0.1226.42308; `PackageOverrides.txt:38` only Xml; `FrameworkList.xml` 0 Pkcs / 1 Cryptography.Xml.
- Docker: aarch64, 8.3 GB; images aspnet:10.0.12 `222759b391a1`, :10.0.13 `d5633778c754`, mssql `2b5b58162112`; no sdk:10.0.402. `b254-mssql*` Exited 137.
- Ports: `lsof 6900-7399 LISTEN` = only `ControlCe *:7000`; 713x named in 0 briefs dated 10-16/17 (Tuesday's tree + HPSM-POC Briefs) → **7130-7139**. Load 6.87 (12:53), 9.65 (12:56). `.tools/.git-lock` absent. Lineage sha256: b250/lock.sh `d9df031b…`, b248/lostnames.py `3eaa9842…`, b244/addedscan.py `e9591087…`.
- Cockpit: `Datasec/HPSM-POC-H2` alive (finished builder), no `HPSM-POC-G*` → **`HPSM-POC-G3` free**. `.env`: 28 names, 0 `AGENTMAIL_API_KEY`, the 3 `JIRA_*` present.
- STANDING HOLD: copied verbatim from B253's brief `:83`, plus B252's `HP Docs/` sentence.

## UNMEASURED
- HPSMPOC-254 "Done when" (quoted from B254 `:35`; no Jira GET by me). Hosted runtime 10.0.12 (via B254 from B253).
- Whether `publish --no-build` sees the prepended list (T-d); whether the append mutant (m3) is red; whether the guard's publish uses 402 or falls to 401 under brief_seat's PATH (T-c).
- Whether an honest "newer framework" simulation exists for m-sdk.
- Vision gate 22's port block (its brief not located); MPS B167 uses 6820-6829.

## Traps (in the brief)
1. **T-a, the SDK floats:** `--channel 10.0` means the next .NET servicing SDK turns the guard red on main and every branch with no code change. That is a designed tripwire, but it also reddens main for everyone. The gate grades it and it is a ticket candidate.
2. **T-b, the 401 false green:** every rank-target result counts on 402 only.
3. **T-c:** `brief_seat.sh:27-28` puts the 401 SDK first on PATH, and the guard falls back to `dotnet` from PATH, so a 402 run can still publish with 401 and give a false green. The gate must prove which SDK ran each guard publish.
4. **T-f:** `grep -c` exits rc 1 when it finds 0, which aborts Tuesday's post-merge check under `set -e`.
5. **T-g:** `gh api …/logs` without `--allow-escape-sequences` writes 0 lines, which reads as a false zero (it hit me once).
6. **T-h:** never `docker pull --platform linux/amd64` by the shared tags, because that re-points the tag on a shared machine. linux-x64 stays NOT TESTED by default. If you want an amd64 leg, rule how to get it (for example by digest into a `b255-` tag).
7. The ticket is expected OPEN (hosted 10.0.12 and Xml). The verdict is on the change, the ticket grade is separate.
8. Never reuse B254's SDK, hook or kits. The gate installs its own 402 into `.tools/b255/dotnet-402` (about 240 MB download).

## Launch
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-G3 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B255_SEAT-G3_hpsmpoc-gate-b254-pkcs.md'"
```
Before launch, Tuesday reads the brief WHOLE, re-stamps the SELF-CHECK line and re-reads `ls-remote` and cockpit `status`.
