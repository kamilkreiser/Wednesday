# B163 drafter report · 2026-10-17 ~06:1x AEDT · for Tuesday
Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B163_SEAT-V_mps-gate-lane-d-r2.md` (259 lines). It is NOT launched.

## Launch command (form: `brief_seat.sh:4`)
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-V "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B163_SEAT-V_mps-gate-lane-d-r2.md'"
```

## Instruments (read verbs only on the project checkout; write verbs only in my throwaway clone)
- `git --no-optional-locks -C <repo> ls-remote origin` at 06:04:24 AEDT, re-read at 06:12:53: 150-r2 `847dc32b1d9f3a1a1c7eb3635cd27046480f6088`, 158-r2 `259cbc27f862e5ea48751634509f14cbd7b038be` (= the READY line, `B103_STATUS.md:343`), main `ec29d51a35873e7082e8e56c94cf6c44a4f710bc`. Same at both reads.
- Throwaway `git clone --shared --no-checkout` at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/4fc01a1b-80dc-4d56-906d-73b9eb0776ff/scratchpad/b163-clone`, push URL `DISABLED` (`remote -v` read back). `merge-tree --write-tree` and one `commit-tree` scratch commit (`345ffbd`, never pushed) there only.
- Slots, load and ports at 06:06: slots 1-3 free, load 2.35, `lsof -iTCP:6800-6809 -sTCP:LISTEN` rc 1. B161 is running (`Briefs/2026-10-17_B161_evidence/` exists, no STATUS yet; `.tools/qa-B161/` exists). No B162 brief exists yet in either Briefs folder.
- No `gh`, no HTTP, no Jira, no az, no build or test run.

## Merge predictions vs main `ec29d51` (a READING; the gate re-measures)
- main + 150-r2: clean, tree `b56f8776`. main + 158-r2 (the stack): clean, tree `04d77b92`.
- Onto main + stack, each clean: `b102/mpscalc-105-negative-bounds` `161def0` (`a84e5a05`), `b160/pkcs-in-package` `0d525ad` (`f51a3953`), `b107/mpscalc-183-pre1-in-deploy` `41af1e3` (`66d26491`), `b104/mpscalc-147-customisation-r2` `56a4e3b` (`12227983`).
- #68 (`ec29d51`, the only main commit after the builder's base `a6813d7`) shares 0 files with the stack's 21 (`comm` empty).

## Traps found (each written into the brief)
1. **Main moved after the builder's CI line.** The builder ran CI on `a6813d7` and says it did not re-run on `ec29d51` (`B103:338-339`). #68 is web-only, so the web baseline (builder 665) is stale. The gate measures its own `base-main` baseline (Check 8).
2. **The generated files' `SOURCE.txt` name `53b2d38` / `7389b64` ("at HEAD"), not the heads.** I checked the contract blobs: `71ac82ea` is the same at `53b2d38` and at `847dc32`, and `3c1cd61c` is the same at `7389b64` and at `259cbc2`. Each head's snapshot equals its `openapi.json`. A plain fresh `sync-contract.mjs <head>` run will therefore differ on header line 2. The brief says what to expect, gives a two-way reproduction, and grades a header-only difference as a Note.
3. **The stored-quote byte-equal check needs exactly one exemption.** B158-1's fix changes the `ZERO YIELD` / `INVALID CONSUMABLE` message for non-internal readers, and on recalculation for internal readers too. A naive byte-compare would go RED. A broad mask would hide a real leak. The brief allows only that `message` path and asks for every differing path to be listed.
4. **"Snapshots stored before the fix" has two sources.** Section supplies come from main (main's text still names the part). Deal supplies come only from `7270732`, because deal usage never reached main or hosted. `INVALID CONSUMABLE` is Blocking, so it can never reach an approved snapshot. Its old text lives only in a stored latest calculation, and the brief tests that path separately.
5. **`RestrictIssue` matches on the issue CODE only** (`Mapping.cs:240-246`). Any other issue that carries consumable text would get past it. The gate lists every supplies-targeted issue.
6. **B158-3's fix adds a new marker surface.** The price audit now stores `usage.supplies` as JSON (`PriceAudit.cs:79`), part numbers and costs included, and it is frozen into snapshots (`QuoteEndpoints.cs:312`). Only internal callers are served it (`:856`, `:598`). By that reading it is safe, but the gate measures it.
7. **Target clicks live in `usage.supplies`,** so on 158-r2 every what-if target change needs a reason and is audited (`B103:327-328`). Left as OPEN (a), a REPORT for you or Kam, not a grade.
8. **The builder's red-first base was hand-edited** (`RestrictIssue` replaced by identity). The gate uses real history instead: `7270732` and `6f2b719`. One unit test calls `Mapping.RestrictIssue`, which is a compile red at `7270732`, so the brief has the gate drop that one method from its scratch copy and say so.
9. **The 158-r2 head is a merge commit** (`259cbc2`, parents `03b7c47` + `847dc32`). The brief says to use `diff <merge-base> <head>`, never `show`.
10. **zsh:** my own `"$r:web/…"` was read as a zsh `:w` modifier and broke a `git show`. The brief says to use `${r}` and bash. It carries today's B161 lessons: no `rm` at all, bash not zsh, a 0-test run is never a pass, names only from `ls-remote`.
11. Smaller items in the brief: the `ENGINE.md` "Deal usage" paragraph still says parity at 1e-18 (`:151` @ `259cbc2`; B158 measured 1e-28). The builder noted it but did not fix it, and the gate notes it. `PriceAudit.cs` is +6 −0, exactly the grant. `Proposal.cs` is +20 −0, all rows, `typeof` or comments. Main's X-29 row (`ec29d51:docs/ENGINE.md:141`) is byte-equal to the head's `:145`. `--diff-filter=MDR` over tests `a6813d7..259cbc2` is empty.

## Choices I made that you may want to overrule
- **Reusing B158's instruments:** the gate may COPY B158's QA instruments from its evidence folder after re-anchoring them, and must never run anything inside `.tools/qa-B158/`. This is faster, and they are QA-made, not builder claims.
- **A false ask on an unchanged re-save is graded Major.** It would block ordinary saves without a reason.
- **A round-1 store-compat probe** (`31cd9ea`) is a REPORT only, because round 1 was never on main or hosted.
- **No `gh` grant** (none needed). Network is Jira GET plus npm/NuGet only.

## What I could not verify
- Jira acceptance for MPSCALC-150 and -158 today (no Jira call). The brief diffs them against B158's quotes.
- Any build, test, API or `sync-contract.mjs` run. Every behaviour in the brief is a reading of the source.
- The web test count on `ec29d51`, and whether B162's slot and port use will clash (B162 is not drafted yet). Ports 6800-6809 were free at 06:06.
- The export surfaces Check 2 lists come from `QuoteApiTests.ExportRegistry.cs`, which I did not open. The gate reads it.
