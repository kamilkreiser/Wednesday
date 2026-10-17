# B254 DRAFTER REPORT · HPSM-POC · HPSMPOC-254 Pkcs 10.0.13 in the API package
Drafter, 2026-10-17 10:0x-10:2x AEDT. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B254_SEAT-H2_hpsmpoc-pkcs-10013-in-package.md`. Nothing written under `!CODING/`; git read verbs only (`--no-optional-locks`); `gh api` GETs under HPSM-POC's own `GH_CONFIG_DIR` (login `kamilDatasec`); one Jira GET (creds read in-process, never printed); no az, no hosted HTTP.

## Measured (instrument)
- Main `72073dace1635899e1262548e561781073b4c7b4` (`ls-remote`); in `2_Project_Files`' object store (`cat-file -t` → commit). Check runs 18 success / 1 skipped; open PRs 0; open alerts 0. Only Pkcs branch on origin: `b248/pkcs-9-0-21` @ `73909e9`; no `b254*`.
- Pin: `HpsmPoc.Modules.Assessment.csproj:28` Pkcs **9.0.21** (comment `:25-27`). No other Cryptography reference in any csproj/props/targets/global.json. `HpsmPoc.Api.csproj` (Web SDK) has none; gets it via `ProjectReference` `:5`. `Directory.Build.props:6` TreatWarningsAsErrors. No csproj/props/global.json change `d916baf..72073da`.
- **Xml: referenced nowhere.** All 10 projects' `project.assets.json` (`.tools/wt-b252-sep`, HEAD d916baf) list 0 Xml libraries; crypto = Pkcs/9.0.21, ProtectedData, Microsoft.Bcl.Cryptography. Pkcs enters via SqlClient 6.1.6 → Pkcs 9.0.11.
- global.json `10.0.401` + `latestFeature`. CI main run 38974522883, api job 117220629571: runtime **10.0.13**, SDK **10.0.402**; 0 warnings; tests 289/270/809/164/**1445**, 0 failed; `OK api package … 119 files`. Local `.tools/dotnet`: SDK 10.0.401, runtimes 10.0.12 only.
- **Main's real CI api.zip** (artifact 12078234485, expires 2026-10-23T22:27:53Z; sha256 `c9f02f92…85c5e`, = B253 STATUS:116): **119 files**, 85 under `runtimes/`; Pkcs DLL **0**, deps Pkcs keys **0**, Xml **0**; control ProtectedData DLL 1, deps lines 3. runtimeconfig frameworks `10.0.0`.
- Deploy checker: `deploy-package.py` has no fixed API count (only `API_REQUIRED` `:64`, MANIFEST self-check `:345-347`, `:367-368`); grep `\b119\b|Pkcs|Cryptography` over infra/ scripts/ .github/: 0 (control `API_REQUIRED` hit). `deploy-from-ci.sh` 109 lines, no count. → no checker change expected.
- Ticket HPSMPOC-254: Backlog, label `b248-found`, 1 comment (39430). **"Done when" is runtime-based** (every runtime that runs the API read as ≥10.0.13).
- Hosted runtime `DOTNETCORE-10.0.12` from `B253_STATUS.md:74` (not measured by me).
- Ports: `lsof 6900-7299` LISTEN = only `ControlCe *:7000` (10:15); 71xx unclaimed in briefs → **7120-7129**. Load 2.11. Cockpit: only `Datasec/HPSM-POC-G2` alive → **`HPSM-POC-H2` free**. lock.sh b250 = b198 (sha256 d9df031b…). Docker has `aspnet:10.0.12` and `:10.0.13`.

## UNMEASURED
- Tip package count (expect 119 → 121, +root and `runtimes/win/lib/net10.0/` Pkcs) and whether the Assessment pin to 10.0.13 raises NU1510/any NU warning.
- Whether the HPSM API loads Pkcs or Xml on any path.
- The SDK tie rule / host rule: taken from the sibling project's STATUS (its source citations), not re-read from dotnet/sdk or dotnet/runtime by me. The brief makes the seat re-read them.
- Whether `gh api /advisories?affects=…` returns the Xml advisories as phrased.

## Traps (in the brief)
1. **False green on the laptop SDK:** 10.0.401 has the 10.0.12 targeting pack, so a 10.0.13 pin wins on file version with no rank target. CI uses 10.0.402 (tie) → the rank target is what matters. The seat must install 10.0.402 in `.tools/b254/`.
2. The rank target must sit in the **publishing** project (Api), while the pin sits in Assessment.
3. Ticket "Done when" will not be met literally (hosted stays 10.0.12); amending it is Tuesday's.
4. Root checkout is at `8869b1a` with an untracked `2_Project_Files/HP Docs/` folder: added to the hold.
5. Branch CI does not keep the package (`ci.yml:136-137`): proof is the CI log line + local CI-shaped package; Tuesday checks main's package after merge (FOR TUESDAY).
6. Next hosted-deploy brief must expect the +Pkcs paths outside wwwroot in the API file list.
7. Future SDK with framework > 10.0.13 drops the DLL again → guard red; Xml stays the host's.
8. Seats here do not write Jira (B251/B253 rule) → comment line goes in STATUS.
9. zsh: use `${S}` (zsh `:` modifiers ate `$S:global.json` in my first read); wrap loops in `bash -c`.

## Launch
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-H2 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B254_SEAT-H2_hpsmpoc-pkcs-10013-in-package.md'"
```
Scratch (my downloads, not in any project): `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2392c438-09c4-4ba2-9b32-b68afb3a6e21/scratchpad/b254/`.
