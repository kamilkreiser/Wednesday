From Friday (laptop seat), 2026-10-10. Replies to friday-laptop-agent@agentmail.to (or your STATUS).

# BRIEF B22 · SEAT-A — Datasec / MPS Commercial Calculator: make the catalogue overlay persist on the hosted showcase (DRAFT for Friday)
**Report:** `1_Project_Definition/Briefs/2026-10-10_B22_STATUS.md`. Its last line is exactly **`READY FOR GATE`** or **`STOPPED: NEEDS FRIDAY`** + the one blocking question.
**Branch:** `b22/overlay-persistence` from `origin/main` = `ef694d4`. **Worktree:** `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B22'` (single-quoted because of the `!`; `chmod 700`). Drafter measured: no `wt-B22*` exists and no `refs/heads/b22*` on origin (2026-10-10 ~19:40 AEDT).
**Pane:** `*MPS*-A`. Your commission is the newest file in `Briefs/` containing `_SEAT-A_`. **Tier 1** (a write path for prices; confidential data on a shared disk). **Ports:** API `5580` only.

## AUTHORITY
- **Kam, mail 2026-10-10 03:28Z, verbatim as relayed** (`Briefs/2026-10-10_B16_SEAT-C_proposal-document.md:12`): *"…the quote tool should have inventory section and an ability to add and modify prices as well as margins … Please work on all of these today and tomorrow."*
- **Kam, mail 2026-10-10 05:23Z, verbatim** (`Briefs/2026-10-10_B21_SEAT-C_hosted-redeploy.md:21`; recorded as C-13 on `records/b21`, `CLARIFICATIONS.md:187-212`): *"This is perfect. Please put it into action"*.
- **Friday's reading (not Kam's words):** an inventory whose price, markup and manual-item edits disappear at every restart does not meet "add and modify prices". C-13 itself lists the in-memory overlay as **not settled** (`records/b21:1_Project_Definition/CLARIFICATIONS.md:212`), and B21 handed it to Seat A as code work, not a setting (`Briefs/2026-10-10_B21_STATUS.md:85`; BACKLOG **B21-1**, `records/b21:BACKLOG.md:183-192`).

## THE PROBLEM (premises @ `ef694d4`; re-measure what you build on)
- **The refusal.** `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs:63-66`: when `hosted` is true and a path is configured, the store throws *"Start refused: MpsCalc:CatalogueOverlay:Path must be empty when hosted (Entra mode)…"* (`:65`). An empty path gives the in-memory store (`:59-62`).
  - The caller is `src/MpsCalc.Api/Program.cs:56`, which passes `hosted = authMode == AuthMode.Entra`. Comment `:54-55`: "Entra: in memory only this round". The class doc says the same (`CatalogueOverlayStore.cs:32-33`).
  - A test pins the refusal: `tests/MpsCalc.Api.Tests/InventoryApiTests.cs:398-402` (`Hosted_mode_keeps_the_overlay_in_memory_and_refuses_a_configured_path`). The gate also measured it live on the package (`Briefs/2026-10-10_B19_STATUS.md:157`, item 12).
- **What is lost live.** On a restart the site loses catalogue sell prices, default markups, manual catalogue rows and the `/inventory/audit` log. A draft that used a lost `man_…` row then recalculates as Blocking, and the version counter restarts at v0 (B21-1; `B21_STATUS.md:79-85`). After B21 the live state was `overlayVersion` 0 with 0 manual rows (`B21_STATUS.md:38`).
- **How the quote store was made persistent (B12; the pattern to mirror).**
  - Entra branch: `Program.cs:50-52` → `QuotePersistence.OpenHosted` (`src/MpsCalc.Api/Quotes/QuoteFileStore.cs:30-31`) → `QuoteFileStore.OpenHosted` (`:144-191`).
  - `ResolveHosted` (`:214-251`) refuses a path that is not absolute (`:216-219`), a root that is not absolute (`:220-223`), a path not strictly inside `HostedRoot` (`:226-229`), a symbolic link or a file at or below the root (`:230-245`), and a path inside `wwwroot` (`:246-249`).
  - Modes: directories are set to 0700 and a probe file to 0600, then read back (`CheckMode` `:193-209`). A mismatch is refused (`:181-185`) unless `PlatformModes = Accept`, in which case `PlatformModesWarning` is set (`:186-190`) and logged at every start (`Program.cs:64-67`).
  - Options: `HostedStoreOptions.From` (`:63-76`). Keys `MpsCalc:QuoteStore:HostedRoot` (default `/home/data/`) and `MpsCalc:QuoteStore:PlatformModes` (`:18-20`); only empty or `Accept` is allowed (`:70-73`).
  - Atomic write: temp file + `Flush(flushToDisk: true)` + rename (`:273-299`, the flush is at `:287`).
  - Gate B15 then measured a restart in Entra on the real package: 10/10 quotes identical (`B15_STATUS.md:206`).
- **What `/home` is.** Seat C measured `/home` as **777 `nobody:nogroup`**: chmod 700/600 read back 777 (`Briefs/2026-10-10_B14_STATUS.md:44,135-137,495`).
  - Friday ruled **Accept** (gate B15 N-1, `B15_STATUS.md:291-295`; `B12_STATUS.md:305`). The ruling is live as `MpsCalc__QuoteStore__PlatformModes: 'Accept'` (`infra/modules/showcase.bicep:83-86`), and B21 read it back unchanged (`B21_STATUS.md:33`).
  - **Records note:** the commission says "per C-12", but C-12 (`records/b12`/`records/b21` `CLARIFICATIONS.md:168-186`) rules F-12/F-13 only. The Accept ruling sits in the gate and STATUS files cited above, not in a C-entry. Build on those files.
- **How the overlay writes today.**
  - `Mutate` (`CatalogueOverlayStore.cs:122-142`) holds an **in-process** `Lock` (`:41`). It enforces append-only (`:130-133`) and writes through `ReferenceStore.WritePrivate` (`:136`).
  - `ReferenceStore.WritePrivate` is in `src/MpsCalc.Import/Store/ReferenceStore.cs:36-71`, which is **FROZEN**. It does temp + rename but **no flush to disk**, unlike the quote store's `:287`.
  - At load, a file that does not parse, has the wrong format, or has an audit out of sequence refuses the start and is left as it is (`:74-86`, `InSequence` `:90-92`).
- **Configuration.**
  - `appsettings.json:10`: `CatalogueOverlay.Path = ""`.
  - `appsettings.Development.json:6`: `../../.local/catalogue-overlay/`.
  - `appsettings.Production.json:1-8` has no overlay key.
  - Hosted app settings: `infra/modules/showcase.bicep:60-87`. That resource **replaces the whole set on every Bicep deploy** (comment `:57-58`). It has no overlay key (B21 read it back: `MpsCalc__CatalogueOverlay__Path` absent, `B21_STATUS.md:33`).
- **Docs.**
  - `docs/API.md:235-239` says writes go under `.local/catalogue-overlay/`.
  - "Hosted configuration" `:317-335` has no overlay row.
  - "Quote store rule per mode" is at `:337-344`.
- **Tests at base:** **UNMEASURED by the drafter** at `ef694d4`. The nearest measurements are .NET 784/784 at T3′ and at `22351cf` (`B19_STATUS.md:30`, `B20_STATUS.md:48`), and web 225/225 at r3 (`B20_STATUS.md:43`). `ef694d4` is the r4 tree `29acdb7e…` (measured `git rev-parse ef694d4^{tree}`). **Measure both suites at `ef694d4` first** and record the counts.

## DESIGN (Friday's; build it this way, or write a disagreement in STATUS before you build)
1. **Same directory family, same guards.** In Entra mode a configured `MpsCalc:CatalogueOverlay:Path` opens under the **hosted rule**:
   - reuse `QuoteFileStore.ResolveHosted` and `HostedStoreOptions.From` unchanged, with the same `HostedRoot` and the **same `PlatformModes` key**. Add no new modes key;
   - the hosted value is `/home/data/catalogue-overlay/`;
   - the mode probe and `Accept` behave as `OpenHosted` (`:149-190`). Factor the probe into one helper used by both stores; quote behaviour stays byte-for-byte;
   - when `Accept` lets the overlay open without the modes, log a **Warning at every start**, worded like the quote store's warning and naming the overlay directory (`Program.cs:64-67` pattern).

   DevStub keeps the git rule (`ResolvePrivate`, `QuoteFileStore.cs:417-481`) unchanged. An empty path stays in memory in both modes.
2. **No overlap.** In Entra mode the overlay directory may not equal, contain, or sit inside the quote store path, or the directory that holds `MpsCalc:ReferenceStorePath`. A path that does is **refused**, with its own reason.
3. **Atomic, durable writes.** The overlay writes with the quote store's write (temp, `Flush(flushToDisk: true)`, rename; make `QuoteFileStore.Write` `:273-299` internal and call it), **not** the frozen importer's `WritePrivate`.
   - The document is written before it becomes current, as `Mutate` already does (`:134-138`).
   - The audit stays append-only (`:130-133`).
4. **Two writers.** The in-process lock does not cover a second process on the same share, for example an old and a new instance overlapping across a deploy restart.
   - Under an exclusive lock file in the overlay directory (`overlay.lock`, created once and **never deleted**; held only for read → compare → write), `Mutate` re-reads `overlay.json` and, if its `Version` differs from the in-memory one, reloads it (with the same load checks) **before** applying the change. A client's stale `overlayVersion` then still gets 409, as today.
   - If the lock cannot be taken within a short bound, answer **503** with a new problem code. Never write without the lock. A new code means a `contract:` commit of its own, pushed first, with its sha in STATUS.
   - Whether the lock excludes across processes on App Service `/home` (an SMB-backed share) is **UNMEASURED**. Say so; the gate or the post-deploy check measures it live.
5. **A restart mid-write.** The rename means the reader sees the old or the new document, never a mix.
   - A stray `.overlay.json.<guid>.tmp` from a killed process is **never loaded and never deleted**. It is logged once at start, with its name only.
   - A corrupt `overlay.json` keeps today's rule (refuse the start, file untouched). Write in STATUS what that means hosted: the site stays down until a human moves the file. That is a Friday/Kam decision, not yours to relax.
6. **Version continuity.** After a restart, the next edit is v(n+1), not v1. This closes B21-1's "a later `catalogue-overlay-v1` can name different content".
7. **Snapshots never change.** An approved snapshot and its proposal bytes stay identical across an overlay edit, a restart, and an edit after the restart.

## THE PROPOSAL WORDING NIT (yours this round; the only `web/` change)
- **Where:** `web/src/proposal/template/sections.ts:103-107`, `pricingCallout`. At `:105` it appends `package`/`packages` after joining the labels with `' and the '`. It is rendered at `web/src/proposal/ProposalDocument.tsx:260`.
- **Why it reads "…package and the … package packages":** the section labels already end in "package" (`tools/demo/scenarios/S4.json:27,33`; `web/src/proposal/fixtures/s4Proposal.ts:38,54`). The existing coverage call `web/src/proposal/template/template.test.ts:17` passes `'first label'`/`'second label'`, so it never sees this.
- **Fix:** no doubled noun for labels that already end in "package" (any case), and correct grammar for 1, 2 and 3 labels.
  - Red first: add a unit test in `web/src/proposal/template/` with labels ending in "package" and labels that do not, red at `ef694d4`.
  - Keep the `template.test.ts` scan covering the function.
  - List the new sentence under NEW WORDS.
- **Your `web/` rows this round:** `web/src/proposal/template/sections.ts` and test files under `web/src/proposal/**` only. Nothing else in `web/`: no `package*.json`, no `sync-contract.mjs`, no generated types.
  - If `openapi.json` changes (item 4's code), Friday commissions the web re-sync separately. Say so in STATUS.
  - Run `npm run lint`, `typecheck` and `test` in `web/` as the house does, and record the counts beside base.

## INFRA (one setting, said out loud)
- If the hosted path must be configured, and it must (an empty path stays in memory by design), you may change **exactly one line** of `infra/modules/showcase.bicep` this round: add `MpsCalc__CatalogueOverlay__Path: '/home/data/catalogue-overlay/'` beside `:81-82`, with a comment naming B22 and the Accept ruling.
  - Nothing else in `infra/`, `scripts/`, `.github/`.
  - Write in STATUS: "Seat A changed infra: one app setting".
- **STOP: NEEDS FRIDAY** if the design needs any new Azure resource: a storage account, file share mount, database, Key Vault, slot or anything else. `/home/data` is already the persistent share (`showcase.bicep:68-69`).
- **Deploy order, for Friday (you run none of it):** the code must be live **before** the setting. `ef694d4`'s code refuses to start with a configured path (`CatalogueOverlayStore.cs:65`), so applying the setting first would take the site down. Write the order in STATUS.

## ITEMS AND ACCEPTANCE (red first for every new guard; one arm per conjunct)
| # | Test | Pass condition |
|---|---|---|
| A0 | Base | `git fetch origin`; assert `git rev-parse origin/main` = `ef694d47176922f01fb877597344d6bd00c02d26` (else **STOP: NEEDS FRIDAY**); record `^{tree}` (drafter: `29acdb7edbb851b0630f05ad551a80bf9b6c276f`); .NET and web counts at base |
| A1 | **Restart, Entra** | `EntraApiHost` with `HostedRoot` = a temp root and the overlay path under it: create a manual row, PATCH a sell price and a default markup (each with a reason), then dispose the host. A **new** host on the same root has the rows, overrides, `overlayVersion` n and the audit (n entries, in sequence, byte-equal). The next edit is v(n+1). RED at `ef694d4` (the host refuses to start) |
| A2 | **Hosted path accepted only inside the root** | Entra: a path inside `HostedRoot` opens. Refused, one arm each: relative; outside the root; the root itself; a symbolic link at the root; a symbolic link below the root; a file in place of the directory; inside `wwwroot`; equal to, inside, or containing the quote store path; containing the reference store's directory. DevStub: a `/home/data`-style path is still refused by the git rule. The existing `InventoryApiTests.cs:398-402` is **replaced**, not deleted: declare it under modified tests, with before and after |
| A3 | Modes | Injected `IUnixModes` (the `HostedStoreTests` `FakeModes` pattern, `tests/MpsCalc.Api.Tests/HostedStoreTests.cs:34`): a throw or a read-back of 0777 → the start is refused naming `PlatformModes = Accept`; with `Accept` → it opens and the overlay warning names the measured modes. Real modes on the Mac → 0700/0600, no warning |
| A4 | Atomic + durable | A write fails after the temp file is written (injected) → `overlay.json` unchanged, in-memory document unchanged, the API answers an error, and nothing is half-applied. The write path flushes (red-prove by a tamper that drops the flush, if a test can observe it; otherwise say UNVERIFIED) |
| A5 | **Two writers** | Two `CatalogueOverlayStore` instances on one directory, interleaved: both edits present, the audit 1..n in sequence with no gap or duplicate, and no lost update. A stale `overlayVersion` from instance 2 after instance 1's write → 409. One red arm per term: remove the reload → lost update; remove the lock → red under a forced interleave |
| A6 | Restart mid-write | A planted `.overlay.json.<guid>.tmp` (garbage) beside a valid `overlay.json` → opens with `overlay.json`, and the tmp file is still there (byte-equal). A corrupt `overlay.json` → start refused, file untouched (existing rule, now also in Entra) |
| A7 | **Approved snapshot never changes** | Entra, on the hosted temp root: approve a synthetic purchase quote that uses a catalogue override and a manual row; edit both in the overlay; restart; edit again. `GET /snapshots/{id}` and its proposal are **byte-identical** at all four points. The calculation's `sourceVersions` names `catalogue-overlay-v<n>` as at approval |
| A8 | Roles unchanged | The I-2 inventory matrix (`InventoryApiTests` and its Entra twin) is green unmodified, and so is `EntraAuthTests.ApiOperations` |
| A9 | Wording nit | The new unit test is red at `ef694d4` and green at head; the full web suite is green; NEW WORDS lists the sentence |
| A10 | Quality | `dotnet build MpsCalc.slnx -c Release --no-incremental` 0 warnings; `dotnet test MpsCalc.slnx` passed/total beside base; `dotnet list … package --vulnerable --include-transitive` 0 high/critical; web lint, typecheck and test beside base; leak and secret scans (B17 recipe, `B17_SEAT-A_purchase-bom-api.md:104-105`) with the denominator and a control that fires |
| A11 | Docs | `docs/API.md`: the overlay paragraph `:235-239` per mode; a "Hosted configuration" row for `MpsCalc__CatalogueOverlay__Path`; the overlay under "store rule per mode"; the deploy-order note |

**Synthetic data only:** manual rows `SYN-…`, invented prices, `@example.test` users. No price-book value, no real SKU tied to a price, and nothing from the example client folder.

## PARTITION (this round)
| Path | B22 · SEAT-A |
|---|---|
| `src/MpsCalc.Api/**`, `tests/MpsCalc.Api.Tests/**`, `docs/API.md` | write |
| `docs/api/openapi.json` | write **only** in a `contract:` commit of its own, pushed first (expected: none, unless A5's 503 code is added) |
| `web/src/proposal/template/sections.ts` + test files under `web/src/proposal/**` | write (the nit only) |
| `infra/modules/showcase.bicep` | **one added line** (above) |
| Everything else: `src/MpsCalc.Engine/**` (frozen again), `src/MpsCalc.Import/**` (FROZEN, `ReferenceStore.cs` included), the rest of `web/**`, `tools/**`, `scripts/**`, `.github/**`, root files, `MpsCalc.slnx` | read-only. **No new .NET project and no NuGet or npm package**, otherwise STOP: NEEDS FRIDAY |
| `.local/pricebooks/**` | read-only, by absolute path; never copied or hash-printed |

## HOLDS (absolute)
- **No deploy, no `az`, no Kudu, no app-setting change, no pricebook upload, no `scripts/**` run.** Friday deploys after a gate.
- **No mail and no message to any human.** The STATUS is the wrap if `4_Credentials/.env` has no `AGENTMAIL_API_KEY`; the drafter counted 0 such lines today.
- **Never delete: quarantine** to `.tools/_quarantine/2026-10-10_B22_<what>/` (0700) and say so. The overlay's lock and tmp files are never removed by code.
- **Synthetic data only** (B17 synthetic-only rule, `B17_SEAT-A_purchase-bom-api.md:104`).
- **Datasec GitHub rule (C-08, C-11).** Push **your branch only** and read it back with `git ls-remote` in the same action as writing the head line. **Friday opens the PR** and merges only when CodeQL C#, Python and JavaScript/TypeScript and every check are green. Never push to `main`, never force-push, never use `--no-verify`/`--admin`, and never dismiss a CodeQL alert: fix it in code.
- **Git:** in `2_Project_Files` use only `fetch`, `worktree add` and `ls-remote`; commits and pushes happen on your branch only. Never `checkout`/`switch` there, and never `gc`/`prune`/`worktree remove`/`branch -D`/`reset` on a shared ref.
- **Processes: kill by port + cwd, never by name.** Use `lsof -nP -iTCP:5580 -sTCP:LISTEN` → PID → `lsof -a -p <PID> -d cwd`, which must be inside `wt-B22`. Never use `pkill`/`killall`. Stop what you started before READY. `caffeinate` is Friday's.
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. In zsh use `$pipestatus[1]`. macOS has no `timeout`. Verdicts are ratios with denominators. Scripted tampers use a unique anchor, and each restore is checked by sha256.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`, and build with `-nodeReuse:false -p:UseSharedCompilation=false`. Fix warnings; never suppress them.
- **F-1, F-12 and F-13 are not changed.** Rental behaviour and every existing test stay green; each modified test is declared with before and after (B19 G-5/G-6, B20 G-2).

## STATUS
Write `1_Project_Definition/Briefs/2026-10-10_B22_STATUS.md` with these sections:
- BLUF;
- branch + head (read back with `ls-remote`);
- `## Test Evidence`: each command verbatim, its real rc, passed/total, and the base count beside it;
- the acceptance table A0–A11 (PASS/FAIL + evidence);
- red proofs (term → test → RED n/m → restore);
- leak and secret counts (denominator + control);
- `## PRIOR WORK` (B12's hosted store, B17's overlay);
- modified pre-existing tests (each, before → after);
- NEW WORDS (every new problem text, refusal, warning and the proposal sentence, verbatim);
- the infra line ("Seat A changed infra: one app setting", or "none");
- the deploy order for Friday;
- UNMEASURED;
- `## NOT DONE / NOT COVERED`;
- needs-Friday;
- processes started and stopped.

One entry at the top of `5_Project_History/history.md` (re-read it immediately before writing). Do not commit the records repo.

## UNMEASURED (drafter)
- Test counts at `ef694d4` (.NET and web).
- Whether an exclusive lock file excludes across processes on App Service `/home`.
- Whether `Flush(flushToDisk)` is honoured end to end by the share.
- How often App Service recycles this B1 site (`B21_STATUS.md:126`).
- Whether the app container sees the same 777 modes as the Kudu container (`B14_STATUS.md:545`).
- The live behaviour of any of this. Unit- and host-proven only; the gate and Friday's post-deploy check measure it live.

READY FOR GATE: A0–A11 PASS with ratios; the restart, hosted-root and snapshot-immutability tests red at `ef694d4` and green at head; infra = at most the one line; branch `b22/overlay-persistence` pushed and read back.
