# B271 DRAFTER REPORT · HPSM-POC · QA gate (tier 1 overall, item 0 = B266, one verdict per ticket, round 1 of 2 each) on b267/round3-bff-counter-locks-pkcs @ e8f5208
Drafter, 2026-10-18 19:27-19:40 AEDT. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B271_SEAT-G6_hpsmpoc-gate-b267.md` (189 lines) with its unstamped copy `…md.pre-stamp` beside it (`cmp` equal, sha256 `9c297700dffcdecf…` both, 19:40:04; `grep -c -i "RULED: _""___"` on the copy = 9, one per slot). Template: B263's kit, its drafter report and B263 STATUS.
**B271 was free:** `ls <tuesday/briefs> | grep -c B271` = 0 and the same in HPSM-POC `1_Project_Definition/Briefs/` = 0 (19:28).
**Nothing was written under `!CODING/`.** Git: read verbs only (`--no-optional-locks`), against `2_Project_Files` (`ls-remote`, `cat-file`) and B267's clone `.tools/b267/repo` (the only local store holding `e8f5208`: `log`, `show`, `diff`, `diff-tree`, `rev-parse`, `rev-list`, `merge-base`, `grep`). `gh api` GETs only, under HPSM-POC's `GH_CONFIG_DIR` (`kamilDatasec`). No docker, dotnet, npm, az, Jira, or HTTP to any app host. One scratch download: records CLARIFICATIONS at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/9fb21003-2535-4473-bb01-07a9389ebc79/scratchpad/clar.md`.

## Read whole
- B263 kit (188 lines), its drafter report (62), B263 STATUS (356).
- B267 stamped brief (136), B267 STATUS (299), its `00_FAIL-first.md` (39); the evidence directory listing (raw 72 entries, probes 19, mutants 58 files incl. 8 `mk*.py`).
- B266 stamped brief (123), B266 STATUS (203); its evidence and `.tools/b266/logs` listings.
- At `e8f5208`: `web/src/server/formGate.ts` whole (373 lines); `SqliteNonTransactionalMigrationsTests.cs` whole (57); the full diffs of `ApiFactory.cs`, `PkcsInPackageTests.cs`, `HostedDemoRobustnessTests.cs`; the new rows of `formMeter.test.ts` (`:170-216`, `:315-395`) and `bff.formstream.test.ts` (`:96-170` by grep + `:156-164`); `FeedbackFiles.cs:290-360`; `FeedbackModule.cs:150-155`; `HostedDemoRobustnessTests.cs:96-125`; `ci.yml` shard / image / gitleaks lines.
- B269's brief (86 lines) skimmed for scope only (it is live).

## Measured (each with its command and time)
- **Pins, 19:28:53** (`ls-remote origin refs/heads/main 'refs/heads/b267*' 'refs/heads/b26*'`): branch `e8f5208c97c8a1aae6e23938ed2622dc638466f5`, main `dff401929dc3408de03e631cdf1255eb1d629975` = the commission. `e8f5208` not in `2_Project_Files`' store; `dff4019` is.
- **GitHub 19:32:45:** compare ahead 7 / behind 0 / 7 files / merge-base `dff4019`; 0 check runs on `e8f5208`; 0 open PRs; 0 open code-scanning alerts; records main `d479cb67…` (CLARIFICATIONS 1,512 lines, 115 C-headings, C-113 `:1424`, C-114 `:1442`, C-115 `:1469`, 19:32:56). The four superseded SHAs of B267 F-9 → "No commit found" (19:34:31; control `e8f5208` found).
- **Range (19:29:05):** 7 commits in queue order, +526 −53, 7 paths, 0 under `api/src`; head tree `bff186533c34…`; `dff4019`'s tree `5180070b0f31…` (= gated `094602f`'s). Per-commit numstat in PINS. `.github`, `global.json`, `infra`, `scripts`, `guard.ts`, `web/package*.json`, `api/src`: `diff --quiet` rc 0 (19:35:01).
- **Machine 19:31:28:** load `3.70 4.98 6.20`; 8 cores; panes `tuesday`, `QA/NexusAI-gate25`, `Datasec/HPSM-POC-R6` (B269, live), `Datasec/MPS-K3`, `Datasec/NexusAI-O`, `fleet-monitor`; `.tools/.git-lock` absent; `lsof 6900-7399` = only `ControlCe *:7000`.
- **Ports:** 7170-7179 `lsof` rc 1 (19:32:05); `\b717[0-9]\b` in 0 brief/STATUS/evidence files of 15-18 Oct (control `\b716[0-9]\b` → 6: B264 was assigned 7160-7169 and used none, so I did not reuse it).
- **Toolchain (listing only, 19:32:39):** `.tools/dotnet/sdk` 10.0.401, 10.0.402; `shared/Microsoft.{AspNetCore,NETCore}.App` 10.0.12, 10.0.13; backup `.tools/b266/quarantine/dotnet-before-b266` present.
- **Kit sha256 (19:32:34-39):** listed in the brief's "Gate lineage". B267's `lock.sh` = B263's (`d9df031b…`). B266's `sdk.tar.gz` `ef081ec3…` (= B266 brief's figure), `releases.json` `8ba714cf…`, `manifest-backup.txt` `4bf159f0…` (= B266 STATUS's prefix), `mutate.py` `95da4670…`.
- **Decision queue 19:33:03:** `list open` has 0 HPSM-POC lines; `hosted-runtime-10013-1017` ruled **a** (18:59, B269's); `require-sqlserver-ci-check-1006` b; `steve-dbs-pdfs` a.
- **Mail key:** `grep -c '^AGENTMAIL_API_KEY='` on the project `.env` = 0; control `^JIRA_BASE_URL=` = 1 (names only, 19:33:03).
- **Prior work (19:34:31, B267's clone):** `HPSMPOC-(281…287|269)([^0-9]|$)` → 0 each on `dff4019`; control `HPSMPOC-260` → 2. `-S MAX_PART_HEADERS` / `indexOfBytes` → `a6576ce`; `-S PackageVersionOf` / `MigrationsLockWaits` → `dff4019`. All equal B267's PRIOR WORK section.
- **Every `file:line` in the brief** was re-read at `e8f5208` in the action that wrote it (`git show … | nl`), and three were corrected before saving (`BothAtFeedbackLock` ends `:240`, the new -282 test starts `:246`, B267's brief is 136 lines).

## UNMEASURED (and why)
- **Jira:** no GET (my rules allow `gh api` only). The Done-when quotes in the brief are the builders' verbatim quotes, with their STATUS line numbers. The gate re-GETs them.
- **Docker:** I ran no docker, so whether images `2b5b58162112` and `830430c1da1a` are still local, and the state of `b267-mssql`, are unmeasured. B267 ran the mssql image at 18:47.
- **Every adversarial row in the brief:** I ran no .NET, node or vitest.
  - The prime candidate (header name `Content-Dıſposıtıon`, T-b) is a hypothesis from reading. JS `/i` without `u` never folds a non-ASCII letter to ASCII; whether .NET's header lookup folds `ı`/`ſ` is unknown to me.
  - So are the `copyWithin` cost (T-d), the 10.0.12-vs-10.0.13 reading (T-a) and the bare-CR/LF limit shapes (T-e).
- **`ShapeAnchorTests`, `quad2f.mjs`, B267's probe sources and `raw/` data:** not read. The traps rest on the product file and on B267's stated numbers.

## Slots (recommendation · default if unanswered)
1. **R-1, item 0's mutants at `e8f5208`** (plus a 10.0.401 discrimination control through a scratch `global.json`, not the backup root).
   - Why: the merge candidate is what CI will run, and the `.csproj` is byte-equal to `dff4019`'s.
   - The tie and m4b message templates are unchanged by -283 (`RaiseThePin` touches only the above-pin branches, `:63`, `:116`).
   - Default (a).
2. **R-2, SQL Server shard 1 AND shard 2 at tip mandatory, base conditional, Azurite on.**
   - Shard 1 holds items 6 and 7 (both in namespace `…Tests.Assessment`).
   - Shard 2 holds `PkcsInPackageTests` (items 0 and 5), and B267 did not run it.
   - Default (a).
3. **R-3, read .NET on both 10.0.12 and 10.0.13.**
   - Hosted runs 10.0.12 until B269 says otherwise. B267 measured only 10.0.13.
   - The cost is a second run of the same probe.
   - Default (a).
4. **R-4, F-2 on the local API.** Measure it.
   - A 500 is pre-existing API behaviour, not -281's failure, because the BFF counts that part.
   - My lean is Note (crafted only).
   - Default (a).
5. **R-5, one simulated crash between the two transactions** on a scratch SQLite file.
   - It is seconds of work and turns F-7's "reading of the measured order" into a measurement.
   - It is findings only and never re-litigates Tuesday's keep ruling.
   - Default (a).
6. **R-6, the wire leg conditional, not required for a GO** (B263 R-1 precedent). Default (a).
7. **R-7, how to grade a residual bypass.**
   - A bypass inside the class a ticket claims to handle is graded against that ticket on B257's bar.
   - A new class, such as header-name folding, is a new candidate on the same bar.
   - This stops a T-b hit from failing -281 for a class it never claimed.
   - Default (a).
8. **R-8, launch while B269 is live.**
   - B269 is hosted-only and writes nothing under `.tools/` or the code repo.
   - The brief fences B269's read paths and accepts its load.
   - Default (a).
9. **R-9, the last-line shape** (B263's contract, adapted: `VERDICT: B271 b267 on main <sha7>: HPSMPOC-269 … · HPSMPOC-287 …`). Default stands.

## Claims in B267's STATUS the gate should try to break
1. **"0 bypass lines … 248 at dff4019" (`:66`).** It is measured on B263's own corpus, through B263's own dnprobe, with B263's generator. That is the gate's lineage, which the builder tuned to. The brief therefore makes the gate's own encoded-word, header-shape and value-less families mandatory (2b, 2c, 2e).
2. **"decodes exactly the measured forms … in each charset's width and order" (F-1, `:203`).** This was measured on 10.0.13 only. Watch:
   - `:179` strips only `[ \t\r\n]`. What .NET does with FF and VT inside the data is unmeasured.
   - `atob` decoding versus `Convert.FromBase64String`.
   - The `false` branch (`:183-186`) is the only way a bypass can arise in the decoder.
3. **"Its header limit is now the API's, in every chunking" (`:23`, `:92`).** It was swept on clean lines only. Untested:
   - bare CR, bare LF, LF-only line ends, and a trailing lone CR (`:272`);
   - the API's `HeadersCountLimit = 16` (`FeedbackFiles.cs:300`);
   - obs-fold at the limit.
4. **"linear time (~2 bytes searched per header byte)" (`:25`, `:107`).** The spy sees only `Uint8Array.prototype.indexOf`. It misses:
   - `copyWithin(0, 0, len)` on every chunk while a header block waits (`:285` with `i = 0`);
   - `set`;
   - `indexOfBytes`' inner compare loop.
   B267's own wall-clock ratio of 2.11 is close to its 2.2 bar. This is the strongest technical trap in the kit (T-d).
5. **Item 6 "red at base".** It is shown by a retargeted B263 listener and a tip mutant, not by the test (F-8). Two further points:
   - B267 says host **A** failed where B263 saw host **B**.
   - The new rendezvous falls through after 5 s, so under load the test may pass without both hosts reaching the Feedback lock.
6. **Item 7's test is not a host start** (T-i). The gate compares its list with a real SQLite host start, and re-derives the transaction order behind F-7 with its own log (T-j).
7. **"0 lost test names" and the suites.** Azurite was OFF (22 + 2 skipped) and shard 2 was never run. The gate runs both.
8. **-284 at `bd42324` alone is slower than base** (F-11). Check 14 must say -284 is not separable from -285.

## Expected wall-clock and load
- **Wall-clock:** about **2.5-3.5 hours**. B263 took 14:04 → 15:44 for ten tickets. This gate adds:
  - item 0's batch of 6 publishes (B266's took about 1 min each);
  - two runtimes for every .NET probe;
  - new corpora of about 4-6 k lines × 3 readers × 5 chunkings;
  - two SQL Server shards with Azurite (shard 1 alone took 4 m 28 s for B267);
  - the -282 forced-hold runs (about 40 s each, several of them);
  - the SQLite suite with Azurite.
- **Load:** the 1-minute load was 3.70 at 19:31. The SQL Server shards and the .NET suite will lift it to roughly 8-9 (B263 about 9, B266 7.85), which is why the brief allows one heavy job at a time below 6. The waits behind `QA/NexusAI-gate25` and B269's browser visit may add 20-40 minutes.

## Launch
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-G6 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B271_SEAT-G6_hpsmpoc-gate-b267.md'"
```
Before launch, Tuesday:
1. Reads the brief WHOLE.
2. Fills the nine `RULED:` slots and the SELF-CHECK line.
3. Re-reads `ls-remote`, cockpit `status` (B269 still live?), `lsof 7170-7179`, `.tools/.git-lock` and the load (below 6).
