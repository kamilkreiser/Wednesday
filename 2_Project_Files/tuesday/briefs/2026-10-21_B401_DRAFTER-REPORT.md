# B401 drafter report (2026-10-21, 11:07-11:13 AEDT, clock from `date`)

Brief: `2026-10-21_B401_SEAT-G24_hpsmpoc-pr170-gate-round2.md` (42 long lines). Slots: exactly 3, one each: `@STAMP_TIME@`, `@STAMP_HEADS@`, `@LAUNCH_AUTH@` (`/usr/bin/grep -o -E '@[A-Z_]+@' | sort | uniq -c` = 1/1/1; the brief's REFUSE line expects the `.pre-stamp` copy = 3, so Tuesday must make that copy before filling). Last line `READ-WHOLE-BY-TUESDAY: PENDING`.

## What I read (whole)
B399 brief (shape), B391 brief (its -232 parts: lines 6, 36, 44-59, 60-75, 76-97), B391 STATUS (315 lines), B397 STATUS (114 lines), B397 brief name/ports, B399 drafter report (shape), B400 brief (ports lines only), `model-routing.md:104-112` (G1 at :108, cap at :111).

## What I measured (instrument: `gh api` GETs under HPSM-POC's `GH_CONFIG_DIR`; `git --no-optional-locks ls-remote`; `/usr/sbin/lsof`; `ls`; clock = `date`)
- 11:08:02 `pulls/170`: head `c0ee7ce6…`, ref `b380/hosted-first-impression-235-234-232`, open, not draft, mergeable true, state blocked, commits 5, files 6, +720/-10, base `f06d2a69`. Title as given.
- 11:08 `compare main...c0ee7ce`: ahead 5, behind 0; commits d14089a7 (54fbceac), 383fa090, b5ea627e, b1ae0544, c0ee7ce6 (b1ae0544, f06d2a69); 6 files with stats as in the brief. Main = `f06d2a69` by API and `ls-remote` (11:08:31 and 11:12:05).
- 11:09:04 `compare b5ea627e...c0ee7ce`: 13 files; neither `FirstVisitWarmup.cs` nor `Caller.cs` is among them (so both are unchanged since `b5ea627e`: MEASURED by the compare listing, to be proved by `git diff --quiet` in the gate). `compare b5ea627e...b1ae0544`: 1 commit, 4 test files (2 modified, 2 added), none in `api/src`. `compare 54fbceac...b5ea627e` product-file stats = +35/-5 and +46/-0, equal to `main...c0ee7ce`'s.
- Required contexts (GET protection): the five expected, verbatim.
- **CI at c0ee7ce (11:08:02, 11:09:04, 11:12:05): NOT FINISHED, and the decisive shard is pending.** 11:09:04, 18 check-runs: success = dependency review, secrets (gitleaks), infra (Bicep validate), **web build (audit, lint, typecheck, build, deploy package)** (was red at b5ea627e; green now), Analyze actions / javascript-typescript / python; neutral = CodeQL. in_progress = `api (ASP.NET Core)`, `api on SQL Server (api-assessment)`, **`api on SQL Server (api-other-and-feedback)`**, `web unit tests (vitest)`, `web e2e` x5, `Analyze (csharp)`. At 11:12:05 the non-green set is: web e2e x4 (journey-and-prototype, playbook-desktop-2, playbook-mobile-1, playbook-mobile-2), both SQL Server shards, `api (ASP.NET Core)`; web unit tests, playbook-desktop-1 and the C# analysis were no longer in the non-success list at 11:12 (success, or I did not read their conclusion: I filtered on `!= success`, so they are success). Aggregates `web (Next.js)` and `api on SQL Server` not yet created at 11:09.
- Code scanning `ref=refs/pull/170/head`, commit c0ee7ce: 3 analyses (javascript-typescript, python, actions), results 0 each at 11:08; open alerts at the ref = 0. (The 4th, C#, was in progress at 11:08/11:09.)
- Open PRs 11:08: #173 (549e6b95), #171 (cc3eae47), #170. #175 is absent from the open list; its branch `b380/hosted-first-impression-235-234` = `89bdb18e` (merged or closed: the gate GETs `pulls/175`).
- `ls-remote` branch heads: no `refs/heads/b401*`, `b400*` (control: `b380*` prints 2 lines). `.tools/` has no `b400*`, `b401*`, `wt-b40*` (11:09; control `b399` exists). Listeners on 7580-7619: none (lsof rc 1, 11:08:31 and 11:09). Whole 7550-7799 range: none.
- Load at 11:07:52 = 3.85/6.25/6.69; 11:09 = 2.33/5.26/6.28 (so the box is lighter than during B391).
- B400 file exists as of 11:09 (it appeared during my work): ports `7590-7599` (a `7590-7609` string in it is only its own `lsof` probe). B366 `7360-7369`; B397 `7550-7559`; B398 `7560-7569`; B399 `7570-7579`; B396 `7540-7549`. Composer briefs of earlier days hold 7580-7589.

## PORT BLOCK: `7600-7609` (no 2026-10-2x brief names it; disjoint from B399, B400, B366, B397, B398, B396, B391).
Note for the gate: it needs essentially no ports (no web, no servers); the block is held for form and for any scratch rig.

## Slot list
`@STAMP_TIME@` (stamp time), `@STAMP_HEADS@` (suggest: `c0ee7ce6` and main `f06d2a69`, re-measured at stamp), `@LAUNCH_AUTH@` (suggest, as drafted by you: Kam's 2026-10-16 grant (merge-once-tested on every Datasec project; HPSM-POC unfrozen) + Kam's terminal words 2026-10-21 ~07:2x about providing the site to HP for review Thursday or Friday + the 2026-09-05 tiered gate and its two-NO-GO cap (round 2 of 2)).

## Design decisions in the brief (so you can overrule)
- Scope: -232 only. B391-3..-6 (and -235/-234 notes B391-7, -10, -11) declared OUT OF SCOPE (shipped in #175); B391-8 stays a FOR TUESDAY note.
- Product proof is by `git diff --quiet b5ea627e c0ee7ce6 -- <2 files>` plus `54fbceac f06d2a69` (main did not touch them), with controls.
- Mutants N1-N12 + P1/P2 rebuilt from B397's text; N6 (the survivor) gets N6b/N6c/N6d plus an exhaustive truth-table over command shapes, to test "equivalent by assertion redundancy" rather than accept it.
- Fixture honesty: B397's SQL Server texts vs the failing job's log (job 118918697027), including that the SELECT shape was built from a log preview, not a verbatim line.
- SQL Server shard (TRX + log) is the decisive evidence: the plant must have fired on SQL Server (`failed (DbUpdateException)`), three tracked reds allowed only if the only reds.
- The gate adds a Jira GET (as B391 allowed) for B391-2.
- Local suites: `HpsmPoc.Api.Tests` only; web not touched (CI cited).

## Open questions (max 5), each with my recommended answer
1. **The decisive shard is pending now (11:12) and the brief makes a pending shard "STOPPED: NEEDS TUESDAY", not a conditional verdict.** Launch now? Recommend: yes. Local work (mutants, truth table, suites) takes the gate well beyond the shard's finish (B391's shard finished within minutes of start); the 45-minute poll covers the tail.
2. **B391-2 (Jira comment 39865 overclaims) cannot be closed by a test, and B397 only drafted the correction (not posted).** Brief default: the gate reports `open` and it is a Note, never a NO GO cause by itself (B391 had it Major). Recommend: post the corrected comment (your records seat) before the verdict if you want `closed`; otherwise keep the default. Alternatively say "Major open", which would hold a GO at GWF.
3. **Mutants N1-N12 are many for one gate.** Each is a filtered single-class run (40 rows, light, a few seconds after one build), so I kept them all; N6's truth-table is the longest. Recommend keep; if you want it shorter, cut N8-N11 (split-regex and bare-SET variants).
4. **Expected `HpsmPoc.Api.Tests` delta = +33 over main (6 rollback rows from b5ea627e + 27 new), assuming main's own count equals B397's 1,524 base.** I did not run it (no dotnet allowed). The gate runs main itself and says what moved if not. Recommend: leave as written.
5. **The gate may read job logs and the TRX artifact zip (8 MB-class), saved under `.tools/b401/ci-art/`, summaries only in evidence (as B391 did).** Recommend: allow.

## Anything that makes the gate unsafe to launch
Nothing blocking. Watch: (a) CI at c0ee7ce not finished (above, handled by the poll/STOPPED rule); (b) `.pre-stamp` copy must exist (count 3) or the gate's REFUSE control fails; (c) if the branch moves before launch (the push of a fix to a red CI leg), the stamp slot for heads must be re-measured: the brief refuses a non-pure-addition move.
