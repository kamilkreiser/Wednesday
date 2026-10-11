From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to friday-laptop-agent@agentmail.to. This project has no mail key, so your STATUS file is your wrap.
# BRIEF B42 · SEAT-B: FIX ROUND for gate B41 (M-1 Blocker, M-2 Major, plus the cheap Minors and Notes) on `b40/source-lifecycle-admin-api`
**Written:** @NOW@ AEDT 2026-10-12. This is a draft. Friday sets the time when he fires it. **Pane:** `Datasec/MPS-B`. Your commission is the newest file in `Briefs/` whose name contains `_SEAT-B_`.
(The draft writer checked the launcher. `Launch_Claude.command:107` takes the seat letter from a pane name that matches `*MPS*-?`. Line `:111` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". At drafting (08:05 AEDT), `ls -t Briefs | grep _SEAT-B_` printed `2026-10-11_B37_SEAT-B_gate-b36-fix-round.md` first. This file replaces it.)
**Seat:** Seat B, a Claude build seat. One branch, red-first. **QA tier 1** throughout: this lane changes which prices every new calculation uses, and M-1 is a tier-1 class (a value in an error page and a log line).
**Round:** FIX ROUND. This is **round 2 of 2** under the two-NO-GO cap (lane A2: B41 was round 1, `B41_STATUS.md:1`). The next gate is a **deltas gate**. **If it says NO GO, Friday ships what is closed and tickets the rest; there is no round 3.** So close each row completely, or list it as NOT DONE. Never leave a row half-done.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B42_STATUS.md`. Its **last line** is exactly one of these:
- `READY FOR GATE: b42/gate-b41-fix-round <sha>`, where `<sha>` is the full 40-hex SHA read back by `git ls-remote origin refs/heads/b42/gate-b41-fix-round` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.

## FIRST STEP (before anything else, Friday's order)
**Re-read B41's STATUS at start and take every finding in its FINAL form. If B41's last line is not yet its final READY FOR REVIEW with a complete findings list, STOP: NEEDS FRIDAY.**
- Friday says gate B41 was still being filled in at drafting. Its mutant suite, probe runs and Playwright legs were still running.
- **Note:** at 08:04 AEDT the file's last line already read `READY FOR REVIEW` (`:306`), but placeholders were still unfilled (listed in AUTHORITY). So `READY FOR REVIEW` alone does not prove the file is final.
- **"Final" means all of these:**
  - the last line is `READY FOR REVIEW`;
  - `grep -nE 'RE-PIN-2-|E2E-TABLE|MUT-B40-TABLE|MUT-OWN-TABLE|NEWWORDS-TABLE|PROCS-SECTION|SELFSCAN|MERGE-LINE'` gives **0** hits;
  - `## Findings` and `## Notes` are complete, and every item named in `## Verdict lines` is defined.
- If any of these fails: **STOP: NEEDS FRIDAY**.
- **M-1 and M-2 stay the core of this round.** Where the final text changes a quote below, the final text wins. Record each difference in PRIOR-WORK CHECK.

## AUTHORITY
- **Gate B41** (`Briefs/2026-10-12_B41_STATUS.md`, Seat E, round 1) gave `B40 70c8172: NO GO` (`:295`), `overall: NO GO` (`:304`): **M-1 Blocker, M-2 Major; M-3, M-4 Minor** (`:295`), and Notes N-1…N-20 (`:214-241`).
- **The draft writer read 306 lines** (`wc -l` at 08:04 AEDT). At that moment the file still held unfilled placeholders: `RE-PIN-2-T` / `RE-PIN-2-M` (`:30`), `E2E-TABLE` (`:99`), `MUT-B40-TABLE` (`:133`), `MUT-OWN-TABLE` (`:136`), `NEWWORDS-TABLE` (`:212`), `PROCS-SECTION` (`:278`), `SELFSCAN` (`:292`) and `MERGE-LINE` (`:303`). Its last line was `READY FOR REVIEW` (`:306`). **The gate seat may still have been writing.**
  - **First read at firing:** `wc -l` the B41 STATUS and diff it against the lines quoted here. If the verdict, the findings list, or any line quoted below changed, record each change in PRIOR-WORK CHECK. **If a new Blocker or Major appears, STOP: NEEDS FRIDAY.** New Minors or Notes: add them to the TAKEN/LEFT table under the rule below.
- **Friday reopens M-1 and M-2 in full.** He also reopens **every gate Minor and Note that is cheap and inside B40's files**. The draft writer's take/leave call for each one is in the table under ROWS. Each row quotes B41 by line. A row marked LEFT goes to RECORDS. You may move a row from TAKEN to LEFT only by giving the measured reason in STATUS. Moving a row from LEFT to TAKEN is **STOP: NEEDS FRIDAY**.
- B40 is **not merged**. Main is still `4437460` (see Base). This round builds on B40's head, not on main.
- These stand unchanged: C-07, C-12, the I-2 matrix (C-13), **Q-16 (MPSCALC-82, retention: build nothing that deletes)**, **Q-09 (never activate a real price book; synthetic sets only)**, Q-10 (no expiry policy), the SITE HOLD and the P-1 HOLD (HOLDS).
- **The fix shapes below are the gate's, not Friday's.** Every row marks them *"the gate proposes; verify before building"*. If you build something else, say why in STATUS.

## READ WHOLE FIRST
- The project `CLAUDE.md`; `1_Project_Definition/CLARIFICATIONS.md` on records `main` (`564f86d`); `Questions_and_Answers/00_QUESTIONS_FOR_KAM.md` (Q-09, Q-10, Q-16).
- **`Briefs/2026-10-12_B41_STATUS.md` in full**, in particular `## Findings` M-1…M-4 (`:138-187`), `## Notes` (`:214-241`), the per-claim table (`:101-109`) and NOT TESTED (`:261-268`). Also its evidence in `Briefs/2026-10-12_B41_evidence/` (`out_e6-echo.json`, `out_restart3.json`, `logs_restart3b.txt`, as named at `:105`, `:108`).
- `Briefs/2026-10-12_B40_SEAT-A_source-lifecycle-admin-api.md` (215 lines) and `2026-10-12_B40_STATUS.md` (679 lines), to see what was built and why.
- The gate's instruments, **read-only. Copy them; never run them in place:** `.tools/qa-B41/tools/echo41.py`, `planted41.py`, `restart3.py`, `restart3b.py`, `start41.py`, `arms3.py`, `apictl41.sh`, `words41.py`, `checkwords41.py`, `leak41.py`, `mut41.py`. The planted documents are in `.tools/qa-B41/syn/planted/`: **24 variants** `p01…p24` plus `markers.json` (25 files, `ls | wc -l`). That includes `p06-bad-currency.json` and `p07-bad-price-kind.json` (M-1's two) and `p14-bom.json` (M-3).

## Base and branch
- **Base: B40 head = `70c8172fe0c3eec8aa7025dd5e2b2b2ec7d3cc37`** (tree `6797e11a10a44580ea5d585a4c396ed24714be90`, parent `790951c`, subject "contract: sync web/src/api/generated to the B40 contract (790951c)"). This is `git log -1 --format='%H %T %P %s' 70c8172`, read by the draft writer.
  - `git ls-remote origin 'refs/heads/*'` at 08:05 AEDT printed `70c8172fe0c3eec8aa7025dd5e2b2b2ec7d3cc37 refs/heads/b40/source-lifecycle-admin-api` and `44374606f49bc5c5498ad7fbd19230de487d85c2 refs/heads/main`. It listed **no `b41`, `b42` or later branch**.
  - `rev-list --left-right --count 4437460...70c8172` = `0 6`: B40 is a fast-forward of main (also B41 `:33`). So every `file:line` in B41 holds at your base.
- **Branch choice: a new branch `b42/gate-b41-fix-round` cut from `70c8172`. Do not add commits to `b40/…`.**
  - This follows the B37 precedent: a new `bNN/gate-…-fix-round` branch with its own worktree (`B37…md:35`, last line of `B37_STATUS.md`: `READY FOR GATE: b37/gate-b36-fix-round f48edf0…`). It also leaves the ref that gate B41 pinned untouched.
  - The deltas gate diffs `70c8172...<your head>`. Friday's PR from `b42/…` carries B40's six commits plus yours.
- **First action:** `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/b40/source-lifecycle-admin-api refs/heads/main`.
  - If they print `70c8172…` and `4437460…`, proceed.
  - If `b40/…` moved, or main moved and `git diff --name-only 4437460 <main>` touches your write set: **STOP: NEEDS FRIDAY**. Never rebase on your own.
- Worktree: `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B42'` (`chmod 700`), created with `worktree add -b b42/gate-b41-fix-round … 70c8172`. Take base measures in `.tools/wt-B42-base`, detached at `70c8172`.
- The draft writer read every `file:line` below at `70c8172` with `git show 70c8172:<path>`. Re-check each one at your base before you edit, and list any that moved.
- **Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.** The Datasec org requires CodeQL.

## Ports
**6640–6649** (API 6640, web 6643 by default). This is B40's range (`B40…md:43`).
- B40's seat is closed: its STATUS last line is `READY FOR GATE: b40/source-lifecycle-admin-api 70c8172…`. **Friday reassigns 6640–6649 to B42.** This overrides the standing line "never use any port named in an earlier brief" for this range only.
- `lsof -nP -iTCP:6640-6649 -sTCP:LISTEN` at 08:07 AEDT printed nothing (rc 1): **0 listeners**.
- **Gate B41 used 6650–6659** (`B41_STATUS.md:277`, Entra stub 6659 `:114`). Never touch that range. Every other port named in an earlier brief or STATUS stays off limits, for example 6620–6629 and 6750–6909. Check your ports again before you bind. Never edit a shared config default.

## Write set (B40's files only)
- `src/MpsCalc.Api/Sources/**` (B40's `SourceLifecycle.cs`, `SourceAdminEndpoints.cs`, `SourceDocumentChecks.cs`, `SourceGovernance.cs`, `ActiveSources.cs`);
- `tests/MpsCalc.Api.Tests/**`, new and existing files. List every modified pre-existing test in STATUS, before → after, with the reason;
- `docs/API.md` and `docs/api/openapi.json`, only where a row changes documented behaviour or words;
- `web/src/api/generated/**`, regenerated **only** by `web/scripts/sync-contract.mjs`, as its own `contract:` commit, never by hand.

**Frozen** (for each one, a need is **STOP: NEEDS FRIDAY**):
- `src/MpsCalc.Import/**` and `src/MpsCalc.Engine/**`. M-1 is fixed at the API's catch sites, never in the importer's converters;
- `src/MpsCalc.Api/Contracts/Dtos.cs`. Every existing record stays byte-equal, and this round adds none. This is why N-11's field is LEFT (below);
- `src/MpsCalc.Api/Program.cs`;
- `src/MpsCalc.Api/Quotes/**` (all of it, including `QuoteEndpoints.cs` and `ExportFieldRegistry.cs`);
- `src/MpsCalc.Api/Inventory/**`, `web/src/**` except `generated/**`, `infra/**`, `scripts/**`, `.github/**`, the root build files, and `docs/{DEMO,ENGINE,IMPORTER}.md`.

If origin carries another seat's branch, newer than your base, that touches your write set: **STOP: NEEDS FRIDAY**.

## Tier 1 (all rows)
- **No value leaves an admin route, in any answer or any log line you can provoke.** Prove it with planted-marker controls, in both the response bodies (plain text and `Accept: text/html`) and `ApiHost.Logged` (`tests/MpsCalc.Api.Tests/Infrastructure/ApiHost.cs:99`).
- **Store off = base, byte for byte** (B41 item (a), 163/163 × 4 arms).
- **Approved history never moves** (B41: 38/38 files, 14/14 reads, 4/4 proposals).
- **The I-2 matrix is byte-for-byte unchanged:** `git diff 70c8172 -- web/src/auth/pricePolicy.ts src/MpsCalc.Api/Quotes/PricingPolicy.cs` is empty, and `RoleMatrixTests` and `PricingPolicyTests` are green.
- Administrator only, in both modes. The store stays off in Entra mode.
- No price, total or applied percent moves on any fixture. A refusal changes nothing: registry, events, `Current`, `versions/` and temp files all stay as they were.

## PRIOR-WORK CHECK (record before you change anything)
- **Suites at `70c8172`, as measured by B41** (`:86-89`): .NET **990/990** (Engine 235, Import 72, Api 683), Release with 0 warnings, 7/7 projects with no vulnerable packages; web **325/325** (50 files). Re-measure both at your base. Do not trust these numbers.
- **Stage's catch list** (`src/MpsCalc.Api/Sources/SourceLifecycle.cs:235-250`): `ReferenceStore.Load(temp)` at `:237` catches `JsonException` (`:239`), `InvalidDataException` (`:243`) and `NotSupportedException` (`:247`). Nothing else.
- **`Answer`** (`SourceAdminEndpoints.cs:158-179`) catches only `IOException` / `UnauthorizedAccessException` (`:165`), and answers 500 `SOURCE_STORE_WRITE_FAILED` (`:167-168`).
- **Other places a stored document is parsed again** (each one is a catch site M-1 must cover):
  - `LoadDocument`, `:417-439`: `JsonSerializer.Deserialize(bytes, …)` at `:432` catches `JsonException` only (`:435`). Validate uses it (`:290`), and so do activate and rollback (`:346`).
  - Activate and rollback catch `InvalidDataException or ArgumentException` (`:348`).
  - `LoadVerified`, `:475-487`: `ActiveSourceSet.From(ReferenceStore.Load(path))` at `:486`, with no catch. The start uses it (`:199`).
  - The start's reference registration, `:171`, with no catch.
  - `SourceDocumentChecks.cs:91-98`: `ActiveSourceSet.From(doc)` catches `ArgumentException` (`:95`).
- **Throw sites the draft writer found by reading** (`git grep -n -E 'throw |ThrowIf'` over `src/MpsCalc.Import` and `src/MpsCalc.Engine` gives 53 lines; the ones a document can reach):
  - `CurrencyCode.cs:12`: `ArgumentException`, with the value in its message.
  - `ReferenceStore.cs:124`: `Enum.Parse<SourcePriceKind>(reader.GetString()!)`. This gives `ArgumentException` with the value, and `ArgumentNullException` for a null `kind`.
  - `ReferenceStore.cs:77`, `:80`: `InvalidDataException`. The `:80` message carries `doc.Format`, a document value. It is caught at `:243` today with fixed words; keep it that way.
  - `ReferenceStore.cs:112`, `:133`, `:141`: `JsonException`. The `:133` message carries the document's field name.
  - `ReferenceData.cs:62`, `:75`: `ArgumentException`. The `:75` message is "Duplicate {what}: {key(row)}", which carries a key from the document. It is reached through `ActiveSourceSet.From`.
  - `PurchaseCatalogue.cs:162`: `ArgumentException`, which carries the SKU.
  - `CurrencyCode.cs:23`: `InvalidOperationException`.
  - **UNMEASURED:** which reader-level exceptions System.Text.Json passes through unwrapped from a custom converter (`InvalidOperationException` from `GetString()` on a non-string token, `FormatException` / `OverflowException` from `GetDecimal()`). B41's p04, p11 and p12 variants did not echo (`:151`). This does not prove those types are wrapped. Your enumeration closes it.
- **Start with no registry** (`SourceLifecycle.cs:151-156`): `CreatePrivateDirectory` for the store and for `versions/` (`:153-154`), then `File.Exists(registryPath) ? ReadRegistry(…) : SourceRegistryDocument.Empty` (`:156`). `ReadRegistry` (`:495-511`) refuses an unreadable registry, with *"It is never repaired."* (`:508`).

## ROWS (one commit per row, red test first; any contract sync is its own commit)

### Row M-1 · Blocker · a staged document can raise an exception that escapes as a raw 500, with the value in the response and in the log
- **Finding, verbatim (B41 `:139`, `:141-152`):** *"M-1 · Blocker · `src/MpsCalc.Api/Sources/SourceLifecycle.cs:239-250` (Stage's catch list) with `SourceAdminEndpoints.cs:165` (`Answer` catches only `IOException` / `UnauthorizedAccessException`)"*. FOUND: *"Its converters throw `ArgumentException`, which carries the offending text"*, and *"System.Text.Json does not wrap those exceptions into `JsonException`, and nothing up the stack catches them."*
- **Oracle (B41 `:146`):** *"any marker outside the stored document; any 500 other than `SOURCE_STORE_WRITE_FAILED`; any exception text."* Measured: p06 and p07 gave a 500 holding the marker, `System.ArgumentException`, a stack trace and absolute build paths, and the server log held the marker (`:148-150`). That is 2/24 variants.
- **Fix shape. The gate proposes; verify before building** (`:154-156`): *"treat any exception from `ReferenceStore.Load` other than an I/O failure as "not a document" … answered with `SafePath`-style words that print no value. Make `Answer` (or a route-level filter) turn every other exception into a fixed-text 500 that names no value."*
- **Friday's scope (wider than the gate's list):** cover **every** exception type a staged document can provoke, not only `ArgumentException`:
  1. **Enumerate first.** List every throw site reachable from a document body: the importer, the engine record constructors, the STJ reader inside the custom converters, `ActiveSourceSet.From` / `ReferenceData` / `PurchaseCatalogue`, and `SourceDocumentChecks`. Give each one as `file:line`, its exception type, whether its message carries a document value, and which API catch site meets it. Do this at every catch site listed in PRIOR-WORK CHECK (Stage, LoadDocument, activate/rollback, LoadVerified at start, the start registration at `:171`, the checks at `:95`). The table goes in STATUS.
  2. **Stage:** every document-provoked exception answers a **coded 4xx** (`SOURCE_DOCUMENT_INVALID`, 400) in fixed words with at most a `SafePath` location. It never carries `ex.Message`, a field value, a field name taken from the document, a type name or a path. Nothing is stored, and 0 temp files remain.
  3. **Validate / activate / rollback:** a stored document that fails to parse never yields a raw 500. Choose its code and say which (M-3 below names the validate case).
  4. **Start:** a document-provoked exception refuses the start in fixed words that carry no value. The log line is value-free.
  5. **Backstop:** `Answer`, or a route-level filter inside `Sources/**`, turns any other exception into a fixed-text 500 with a code. It logs **value-free**: a fixed event text and the exception **type name** only, never `ex.Message` or `ex.ToString()`. **No planted variant may reach the backstop:** count = 0. The backstop is for bugs, not documents.
  - Do not catch an I/O failure as "not a document". The `SOURCE_STORE_WRITE_FAILED` path stays as it is.
- **Red-first cell (the gate's planted-marker variants):**
  - **Test:** copy all **24** B41 variants as synthetic test inputs (`.tools/qa-B41/syn/planted/p01…p24`, with their markers; never print a marker from a price book). Turn them into planted-marker tests. For each variant assert: no 500; a 4xx with a code (or 201 for a valid one); **0 markers** in the response, in plain text and HTML; **0 markers** in `ApiHost.Logged`; and nothing stored when refused. Add one variant per enumerated exception type that the 24 do not already hit, and name each one.
  - **RED at base:** p06 and p07 at least (500 with the marker). Give `RED n/m`.
  - **GREEN at head.**
  - **Tampered back RED:** (a) remove the new Stage catch; (b) put `ex.Message` back into the answer; (c) log `ex.Message` in the backstop. Each one goes RED on its own.
  - **Probe:** run a copy of `echo41.py` against your head on your ports, store on, DevStub. Expect **0/24** echo, with its controls fired (11/11 markers found in the stored documents, as `:151`).

### Row M-2 · Major · a missing `registry.json` with `versions/` present re-initialises the store silently
- **Finding, verbatim (B41 `:163-164`):** *"M-2 · Major · `src/MpsCalc.Api/Sources/SourceLifecycle.cs:156` (`File.Exists(registryPath) ? ReadRegistry(…) : SourceRegistryDocument.Empty`)"*. FOUND: *"a store directory with no `registry.json` is treated as a new store, even when `versions/` holds staged documents."*
- **Oracle (`:165-171`):** *"a restart that disagrees with what the API last answered 2xx, or a restart refusal that writes a file."* Measured: the start succeeded, wrote a new registry and calculated on the reference set. It listed 1 version and 2 events. Truncated, half, not-JSON, wrong-format and null-versions registries are refused (5/5), as are a missing or edited Active document (2/2).
- **Fix shape. The gate proposes; verify before building** (`:172`): *"refuse (*"never repaired"*, as the other registry refusals) when `registry.json` is absent but the directory (or `versions/`) is not empty. Initialise only an empty directory."*
  - **Order matters.** `:153-154` create the directories before `:156`. The refusal must create nothing and move nothing. Decide what "empty" means, and say so in STATUS: stray `.tmp` files (N-2) and a `versions/` that holds only temp files are cases to decide.
- **Red-first cell:**
  - **Test:** a store with one staged Active version and its `registry.json` removed. The start is refused with words that carry no value. No file is created, and `versions/` is byte-identical (list and sha256 before and after). Add one arm with the reference version Active (B41 arm F, `:170`), and one arm with an empty directory, which still initialises.
  - **RED at base** (the start succeeds and writes the registry).
  - **GREEN at head.**
  - **Tampered back RED:** restore `:156`'s behaviour.
  - **Probe:** copies of `restart3.py` and `restart3b.py`. Every refused arm leaves nothing changed.

### Gate Minors and Notes: TAKEN / LEFT (draft writer's call; each quoted from B41 by line)
"Cheap and inside B40's files" means: the fix fits in `Sources/**`, tests, `docs/API.md` or `openapi.json`, with no frozen file and no ruling. **TAKEN rows each get their own commit, red first.**

| Item (B41 line) | Gate's words (verbatim, shortened with …) | Call | Reason / shape (the gate proposes; verify) |
|---|---|---|---|
| **M-3** Minor (`:176-181`) | *"a document with a UTF-8 BOM stages … Every validate then answers **409 `SOURCE_DOCUMENT_CHANGED`** … That is false"* | **TAKEN** | Same file as M-1 (`:432` vs `:237`). The gate's HOW (`:181`): *"read the bytes with the same reader in both places (skip a UTF-8 BOM, or refuse it at stage with 400). Answer a parse failure at validate with a parse code, not `SOURCE_DOCUMENT_CHANGED`."* Test with p14: it either validates or is refused at stage, never stuck. Already-stuck Drafts are N-12a (LEFT). |
| **M-4** Minor (`:183-187`) | *"a well-formed registry whose `activeVersionId` names no version **starts** … Every calculation answers **503 `SOURCES_UNAVAILABLE`**"* | **TAKEN** | Same start path as M-2. The gate's HOW (`:187`): *"refuse unless the pointer names exactly the one version whose state is `Active` (or both are absent). Test with the C6 tamper."* No repair, nothing written. |
| **N-1** (`:215`) | *"an in-process throw from `AfterRegistryWrite` … answers **500 *"Nothing changed"*** while the disk already holds the new registry … Reachable only through the test seam"* | LEFT | No production path reaches it (the gate's words). A real fix (reload from disk after a failed swap) is not cheap. Goes to RECORDS. |
| **N-2** (`:216`) | *"a kill -9 inside the `BeforeRegistryRename` window leaves **1 stray `.tmp`** … never cleaned or reported at start"* | **TAKEN (report only)** | At start, report the count of stray temp files in the store root and in `versions/`: counts only, no names, value-free. **Never delete them (Q-16).** If reporting needs a logger that only `Program.cs` can supply, move the row to LEFT with that reason (UNMEASURED: whether `SourceLifecycle.Open` can log without a `Program.cs` change). |
| **N-3** (`:217-221`) | *"both starting at once on an empty store each register the reference file under a **different** Active id … **v2 and 4 events vanished**"* | LEFT | Declared `[B40-R8]`. A cross-process lock is not cheap, and it is a prerequisite for any hosted switch-on (`:221`). Add a dated line to `[B40-R8]` in RECORDS. |
| **N-4** (`:222`) | *"a **dangling** reference-file link with the store on crashes the start with an unworded `FileNotFoundException` (`SourceLifecycle.cs:160-162` …), after creating `versions/`"* | **TAKEN** | `Sources/**` only. Give a worded refusal before any directory is created, and covered by the M-1 start rule (the log stays value-free). Test with a dangling link: refused, 0 directories created. |
| **N-5** (`:223`) | *"the overlap compare ignores case (declared in `API.md`) … Safe direction."* | LEFT | Declared, and the safe direction. No change. |
| **N-6** (`:224`) | *"a store path that is a link *outside* `.local` resolving into `.local` is accepted … same rule as the quote store."* | LEFT | Parity with `QuoteFileStore.ResolvePrivate` (frozen `Quotes/**`). |
| **N-7** (`:225`) | *"a hard link of the reference file inside the store directory: the start is accepted (the code cannot see hard links). No write goes through it"* | LEFT | Cannot be seen portably; no write goes through it. RECORDS only. |
| **N-8** (`:226`) | *"the refusals "contains the quote store / overlay" leave the quote store and overlay directories created by their own openers, which run before the version-store check (base code order)."* | LEFT | The opener order is in `Program.cs` (frozen). |
| **N-9** (`:227`) | *"store off, the list with a query string: base ignores it; T filters or answers 400 … Declared"* | LEFT | Declared (B40 STATUS `:214`). Ignoring filters while off would trade a working filter for byte parity. That is a choice for Friday, not a cheap fix. |
| **N-10** (`:228`) | *"a draft calculated on v1 and submitted + approved after v2 is Active … B40's brief does not settle"* | LEFT | Marked by the gate as *"needs Friday against FR-ADM-009"*. A ruling, not a deferred problem: list it in needs-Friday, not in RECORDS. |
| **N-11** (`:229`) | *"the quote DTO's `lineMarkups` are a dry run on the *current* set, while `sourceVersions` show the stored calculation's set. No field names the set the markups came from"* | **TAKEN (words) / LEFT (field)** | See Row N-11 below. |
| **N-12** (`:230`, first half) | *"duplicate JSON keys are accepted (the last wins; both kept in the stored bytes)."* | LEFT | Detection needs a raw-token pre-scan of a 16 MiB body, with a rule choice (refuse, or keep last wins). Not cheap. |
| **N-12a** (`:230`) | *"a never-validated Draft counts in the duplicate-id rule (`SourceDocumentChecks.cs:68-71`) … an abandoned Draft … blocks that document for good."* | LEFT | Changing which states count in DATA-IMP-001 (`SourceDocumentChecks.cs:66-70`) is a rule change. With no delete (Q-16), the remedy needs a ruling. M-3's fix stops new stuck BOM Drafts. RECORDS. |
| **N-13** (`:231`) | *"validation passes documents with a null currency in one slot, a null supply SKU, or an option whose device is absent … the declared `[B40-R7]`"* | LEFT | Declared `[B40-R7]`. But each of these must stay value-free under the M-1 enumeration: include p16, p17 and p23 in the M-1 tests. |
| **N-14** (`:232-235`) | *"pre-existing, base parity … Not a B40 finding."* | LEFT | Not B40's (`CallerResolver.cs`, outside the write set). |
| **N-15** (`:236`) | *"`SOURCES_UNAVAILABLE` (`QuoteEndpoints.cs:218`, `:693`) still says *"…(mpscalc-import) and restart."* … Note for the wording round."* | LEFT | `Quotes/**` is frozen this round. The two sites are identical strings, and `:693` was never in B40's carve-out (`B40…md:50` named only the base `:219`). The gate itself routes this to the wording round. RECORDS. |
| **N-16** (`:237`) | *"stage returns `Draft`, not the spec row's `state=Validating` … the reasoning holds"* | LEFT | The gate accepts it. No change. |
| **N-17** (`:238`) | *"`docs/IMPORTER.md:89` still lists the lifecycle under "Not in this lane" (declared `[B40-R5]`, lane D)."* | LEFT | `IMPORTER.md` is frozen (lane D). |
| **N-18** (`:239`) | *"bodies at the 16 MiB limit are accepted and kept for the life of the store (Q-16 default; no cap)."* | LEFT | Q-16 is Kam's. |
| **N-19** (`:240`, also `:46`) | *"the test project now compiles two importer-test sources; their future edits reach the API suite."* | LEFT | Informational; the gate judged it acceptable (`:46`). |
| **N-20** (`:241`) | *"no suite test runs with the key **absent** (`ApiHost.cs:106` always sets it)."* | **TAKEN** | Tests only. Add a host variant with `MpsCalc:SourceVersions:Path` absent, asserting the list body equals the off body and 0 files are created. It is a guard, so it is green at base and at head. Kill it with a tamper (the absent key treated as on): RED. |

### Row N-11 · Note · name the source set the `lineMarkups` came from (minimum: words)
- **Finding, verbatim (B41 `:229`):** see the table. The gate adds: *"By design (B30), and not a mix inside one computation."* NOT TESTED `:268`: *"The `lineMarkups` race window (N-11): not widened by a mutant"*.
- **What is cheap and in B40's files:** the words. Today `docs/api/openapi.json:762` says lineMarkups are *"Recomputed on every quote response from the saved draft and the current catalogue overlay"*, and `docs/API.md:175-186` describes them. Neither says the dry run uses the **currently Active source set**, which can differ from `sourceVersions` once the lifecycle store is on.
  - **TAKEN:** add that sentence in `API.md` (near `:175-186`) and in the `lineMarkups` description at `openapi.json:762`. Follow with a `contract:` sync commit. Every changed line goes in NEW WORDS.
  - **LEFT, with the reason:** a field naming the set (like `lineMarkupsOverlayVersion`, `Dtos.cs:147-149`) needs an existing-DTO change (`Dtos.cs` frozen: existing records byte-equal) and a change in `QuoteEndpoints.cs:756-779` (frozen `Quotes/**`). Record it for Friday as a candidate for the next API lane.
- **Mechanical cell:** `contract.test.ts` is green. The `generated/**` diff is exactly the changed description plus the SOURCE header. NEW WORDS count = count.

## NEW WORDS (verbatim; Friday shows Kam before any deploy)
- Every user-visible or API-visible string this round adds or changes goes in STATUS under `## NEW WORDS`, old → new, with `file:line` (or JSON path) at your head. That covers M-1's refusal and backstop words and codes, M-2 / M-4 / N-4 start refusals, M-3's validate code, the N-2 log text, the N-11 sentences, and every added or removed line of `docs/API.md`. **No generic row** (B36 K-7).
- Run copies of `words41.py` and `checkwords41.py` over `70c8172...<head>`. Every extracted string appears in your table (count = count), and a planted undeclared string must be flagged.
- Scan the new words against the example-document lists with a copy of `leak41.py`, counts only: **0 hits**, with controls that fired.

## Test Evidence (run each command as `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head (`wt-B42-base` at `70c8172`, `wt-B42`):**
  - .NET: the full suite, a Release build `--no-incremental` with **0 warnings**, and `dotnet list package --vulnerable --include-transitive` with 0 vulnerable packages;
  - web: `npm ci`, `lint`, `typecheck`, the full `test` suite and `build`.
  - Reconcile every count change by test name (`--list-tests`, `comm`).
- **Red-proof table, one line per conjunct:** the term, the tamper, `RED n/m` on the full suite, and the sha256 restore. It covers every TAKEN row. Also re-apply B41's sampled B40 tampers from a copy of `mut41.py` (`:287`: 6 sampled). Each must still be RED, with the count reconciled.
- **Probes** (copies; synthetic stores only; your ports; DevStub, plus Entra-fake to prove the store stays off there):
  - `echo41.py`: 0/24 echo;
  - `restart3.py` and `restart3b.py`: M-2 and M-4 refused, nothing changed;
  - `start41.py` / `arms3.py`: N-4 refused before any directory exists;
  - a stage → validate → activate → calculate → rollback → calculate chain, with the reference file's sha256 and every approved proposal body read before and after.
- **Store off = base:** a copy of `off41.py` / `cmp41.py`, 4 arms, base vs head.
- **I-2:** `RoleMatrixTests` and `PricingPolicyTests` green; the policy files sha-identical to base.
- **Playwright** (stub and live, synthetic data only; mask money cells): no screen changes, so run the full suites. The `smoke.spec.ts:36` timeout is pre-existing (B36 N-7). Report it; it is not yours.
- **Leak + secret scan** over `git diff 70c8172...HEAD` and `git log --format=%B 70c8172..HEAD`, using copies of `leak41.py` and its list builders. Counts only, every class with a planted control that fired. Never print the avoid list.
- **No frozen change:** `git diff --numstat 70c8172 -- infra scripts .github src/MpsCalc.Engine src/MpsCalc.Import src/MpsCalc.Api/Inventory src/MpsCalc.Api/Quotes src/MpsCalc.Api/Program.cs src/MpsCalc.Api/Contracts/Dtos.cs web/src/auth docs/DEMO.md docs/ENGINE.md docs/IMPORTER.md` is empty.
- Evidence goes in `Briefs/2026-10-12_B42_evidence/` (folder 0700, files 0600). Tools and logs go in `.tools/qa-B42/` (0700).

## RECORDS (route: a LOCAL `records/b42` branch, commit only)
- **The draft writer measured the records repo (the project root), read-only:**
  - `git remote -v` printed **0 lines**: no remote.
  - Records `main` = `564f86d624e0a04bf74fd326f5cf516d73d02134`.
  - `records/b40` = `80a5abb95b657ec8f79e9a0e54930f19bd563bd8` ("Records: lane A2 remainders (B40): name [B40-R8] …"). `rev-list --left-right --count main...records/b40` = `0 3`: **not folded into main**.
- **Steps:**
  - `git -C '<project root>' worktree add .tools/wt-B42-records -b records/b42 records/b40` (base it on `records/b40` so the `[B40-R*]` rows exist), then `chmod 700`. Commit there only.
  - Never `checkout`, `switch`, `stash`, `merge` or `reset` in the root worktree. Never fold into `main`. That is Friday's.
- **Add rows to `BACKLOG.md` under `## Deferred problems`**, in the existing row shape (Where / Symptom in the gate's words, quoted / Fix shape / Why deferred / Discovered), each with source and date. Use one commit, message `Records: gate B41 rows not fixed in B42 (B42)`. The rows:
  - one row each for the LEFT items N-1, N-7, N-12, N-12a, N-15, and the N-11 field;
  - dated lines appended (never removed) to `[B40-R8]` (N-3), `[B40-R5]` (N-17) and `[B40-R7]` (N-13);
  - one row per TAKEN or M-row you leave NOT DONE.
  - **Do not** record N-10. It is a ruling for Friday.
- `CLAUDE.md`, `JIRA.md`, `history.md` and Jira are Friday's. Write none of them.

## FOUND / TESTED / HOW / NOT TESTED
For each row (M-1, M-2 and every TAKEN item), write a four-line block in STATUS:
- **FOUND:** what you found at base, citing `file:line`;
- **TESTED:** the tests that pin the fix (file and name), with red-first counts;
- **HOW:** the instrument (suite, tamper, probe or read-back), with ratios;
- **NOT TESTED:** what is left, and why.

## STATUS sections
- BLUF, with a one-line verdict per row;
- PRIOR-WORK CHECK (every cite above re-read at base, which moved, and the B41 line-count diff);
- Commits;
- Test Evidence;
- the M-1 throw-site enumeration table;
- Red-proof table;
- Tier-1 conditions;
- FOUND / TESTED / HOW / NOT TESTED, per row;
- Fix shape chosen per row: the gate's or another, and why;
- The TAKEN / LEFT table as built (any move to LEFT, with its measured reason);
- Modified pre-existing tests (before → after, and why);
- NEW WORDS (verbatim);
- UNMEASURED;
- `## NOT DONE / NOT COVERED`, as prominent as the evidence;
- RECORDS: the `records/b42` SHA, its rows, and `git log -1`;
- needs-Friday: N-10, and one draft Jira line per ticket (MPSCALC-50, -53, -55), "advances, not Done";
- Leak + secret scan;
- processes started and stopped;
- worktrees and files left.

## Time-box
**About 2 h.** If you run short, finish in this order: **M-1** (the Blocker, enumeration first), **M-2**, M-4, M-3, N-4, N-20, N-11 words, N-2. NEW WORDS go alongside each row. List what is left as **NOT DONE**, never half-built. Remember there is no round 3.

## UNMEASURED (by the draft writer, each with its closing instrument)
- **Whether STJ wraps reader-level exceptions thrown inside the custom converters** (`InvalidOperationException`, `FormatException`, `OverflowException`): UNKNOWN. It closes with your M-1 enumeration and one planted test per type.
- **Whether `ReferenceData` / `PurchaseCatalogue` duplicate messages (`ReferenceData.cs:75`, `PurchaseCatalogue.cs:162`) can reach a log through the start path (`:199` → `:486`, no catch):** read by eye only. It closes with an M-1 start test (a duplicate-key Active document, so start refuses and the log is value-free).
- **Whether `SourceLifecycle.Open` can log N-2's count without a `Program.cs` change:** UNKNOWN. It closes with your read of how the lifecycle is constructed (`Program.cs:64-66`).
- **The final B41 text:** 306 lines read, with placeholders unfilled (AUTHORITY). It closes with your line-count diff at firing.
- **CodeQL and CI for `70c8172`:** B41 could not see them (`:256`). Friday reads them on the PR.
- **Ports 6640–6649 at firing:** free at 08:07 AEDT. Re-check with `lsof` before you bind.

## HOLDS
- Datasec only. No other client's names, tickets or paths.
- **CodeQL policy:**
  - push your branch only;
  - never push to main;
  - never dismiss an alert;
  - never ask for a bypass.
  Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.
- **No deploy.** No Azure write, no setting change, nothing sent to any human.
  - **P-1 HOLD (records BACKLOG `## Holds on the hosted site`, B39):** before any hosted deploy of main ≥ `4437460`, the hosted quotes with a repeated fleet `lineNumber` must be counted (B41 `:275`). This round deploys nothing and does not run P-1.
  - A hosted MPS deploy needs Kam's card.
- **Q-09 hold (carried from B41 `:264`):** synthetic price sets only. **Never stage, validate or activate a real price book.** Every process sets `MpsCalc__ReferenceStorePath` to a synthetic copy under `.tools/qa-B42/`, never `.local/pricebooks/`. The leak scan's list loaders may read the books by path for counts only.
- **SITE HOLD:** none of the four store path settings changes; `ReferenceStorePath` stays a regular file, never a link; activation never repoints it.
- No pricing rule change. No price, total or applied percent moves on any fixture.
- **No real client data anywhere.** The price books and the example quote are CONFIDENTIAL: report counts only, in code, tests, fixtures, commit messages and STATUS.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-12_B42_<what>/` (0700), and say so. That includes N-2's stray temp files: count them, never remove them. **Never edit a running script.** Write a new file instead.
- **Own worktree and own ports.**
  - Allowed: `fetch`, `worktree add`, and commits and pushes on `b42/gate-b41-fix-round`. On records, commits on `records/b42` only (no remote).
  - Never `checkout` or `switch` in `2_Project_Files` or the project root. **Never `gc`, `prune`, `reset`, `worktree remove`, `branch -D` or force-push.**
  - Never push to `b40/…`. Never touch another seat's worktree: `wt-B40*` and `wt-B41*`, `qa-B40/` and `qa-B41/` are read-only. Copy from them.
  - No merge, no Jira write.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate`, the shared `VBCSCompiler` and any listener outside 6640–6649 are not yours.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`. Build with `UseSharedCompilation=false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero needs a positive control that fired.
- **Records:** write only your STATUS, your evidence folder, `.tools/qa-B42/`, your worktrees, and `records/b42`.

## End
The last line of `Briefs/2026-10-12_B42_STATUS.md` is exactly one of these:
- `READY FOR GATE: b42/gate-b41-fix-round <sha>`, where `<sha>` is the full SHA read back by `git ls-remote origin refs/heads/b42/gate-b41-fix-round` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.
