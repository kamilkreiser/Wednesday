# B447 DRAFTER REPORT (round 3 of 3, tier 1 gate, HPSM-POC telemetry 224)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B447_SEAT-G35_hpsmpoc-telemetry-gate-round3-tier1.md` (47 lines, 46.6 KB). Read-only drafter: nothing built, tested, fetched, mailed or posted. Cloned from the B436 kit (and B431 through it); read whole: B436 kit, B431 kit, B436 STATUS, B440 brief, ADDENDUM-1, ADDENDUM-2, B440 STATUS.

## Measured by me (11:24 AEDT, git read verbs, `lsof`, `ls`, `uptime`)
- `ls-remote`: `b429/telemetry-224` = `473bfaca6c7eb8dddef0636326fb0468233b035f`; main = `a93b926ac8534bd0c9ae67fe63229ede46c39fd4` (B438 #180); control `b386*` printed; no `b447*` ref.
- Ports 8130-8139: `lsof` rc 1. `.tools/b447` and `wt-b447-*` absent. Load `3.92 5.45 6.14`.
- merge-base `01dd9e4b`; `rev-list --left-right --count main...head` = 1 24 (the branch has not merged `a93b926`). Three-dot name-status = 40 paths (A 29, M 11) = the 35 + 5 new test files (all inside the owned globs). Two-dot = 42. B440's own delta vs `39d4d1a2` = 19 paths (22 minus 3 merge-brought main files).
- gitleaks.ignore: +3 lines vs `39d4d1a2` (comment + the two ADDENDUM-2 fingerprints, text matches the addendum); +13 vs main.
- Legacy 3-arg `merge-tree` vs `a93b926`: 0 conflict-marker lines, but with no positive control, so the brief calls it weak and has the gate re-run it with one.
- Code anchors (TelemetryScrub.cs, TelemetrySetup.cs, scrub.ts, setup.ts) re-read by `git grep` at the head and written into the brief as anchors, not as proof.

## What changed vs the round-2 kit
1. Slots are `____` (B440 style); REFUSE count uses the split pattern `'_''_''_''_'`; 16 slot hits in the unstamped file (Stamp paragraph, Stamp section, last line `READ-WHOLE-BY-TUESDAY: ____`).
2. New centre of check 2: (b) the full round-2 canary set (41 / 31 / 52) PLUS B436-1/-2/-7 shapes and round-3-specific attacks; (c) a closed-grammar assertion by the gate on the WHOLE field, pattern written before looking, extra-key check, dead-run rule; (d) type token by provenance with built look-alike names (emitted `System.InvalidOperationException`, byte-loaded assembly named `System.Private.CoreLib`, `LoadFrom` from a temp folder and a sub-folder, prefix-folder attack); (e) log records: message equals the constant, MIXED/CONCAT 0, plus new shapes (escapes, `LogError(ex)` exception text on a log record, category from a runtime string).
3. Check 4 is now start-up: gate's own >= 200 corpus with a recorded seed (not 440), API in-process AND as a real process, web unit, web real server (>= 20 members, B440 ran 5), an `EventListener` on all event sources (B440 greps log lines only), own doubles for throw at start/export/build/stop.
4. Check 5 = the 11 retired rows by name, replacement strictly stronger, each red at base; check 6 = gitleaks ADDENDUM-2 (JSON without ignore file: exactly 2 on `b50f5bc`, 11 findings in all); check 7 = B431 + B436 regression table (closed/open/regressed counts); check 8 = class hunt by program (frame/type shapes 0 at head, shape rules left in exception paths 0, dead helpers proved dead); check 9 = suites, explicit `-warnaserror`, `npm --prefix`, infra read by OUTPUT, 9 of B440's 14 mutants + 3 own (`ShippedFolders` prefix compare, narrow catch in the guard, generic type arguments leak), CodeQL expectation, merge-tree.
5. Cap wording: NO GO ends the work (product owner's card), no round 4 suggested.

## Things you should know before stamping
1. **Builder census gap.** B440 ran only 13 canaries on the real Program (round 2: 52) and 1 on the real server (round 2: 31), and says so. The kit makes the full 124 the gate's job and adds a stock-exporter control on the real server (round 2 had none).
2. **Provenance joint.** The API type token trusts "not dynamic, file folder exactly one of three". The kit attacks it (built names, sub-folder, prefix sibling, empty `Location`) and has own-mutant 1 (`StartsWith`). A file dropped into a shipped folder is a deployment act; the kit says judge it, Note unless a caller can cause it.
3. **B440's dead helpers** (`FramesOnly`/`StrictFrame`, `framesOnly`, `IsStructuredTemplate`) still hold shape rules with 0 product callers. Kit: prove dead by program; reachable = Blocker, dead = Note. Your call whether you want that stricter (it could matter to "shape rules left in exception paths 0").
4. **Code-only shapes B440 left** (web `scrub.ts:145`, `setup.ts:144,146`): the kit has the gate probe what Next puts in `routePath` on a dynamic route. B440 did not.
5. **Harness defect** B440 reported: `test_security_baseline.py` exits 0 on `FAILED (errors=4)`. The kit reads infra OUTPUT, not rc, and puts it in FOR TUESDAY. Not routed by me.
6. **Main moved** to `a93b926` after the builder's last merge; overlap with the 40 is 0, the PR will show main one commit ahead. The kit asks for the merge-tree with a control.
7. B440 read the vault Access file for the mail key and used mail for two QUESTION mails (agentmail inbox only); not a gate matter.
8. Round-2 STOP-and-card wording is preserved but flipped to "ends the work": no round 4.

## Fill before launch (Tuesday)
Stamp paragraph in the middle (stamp time, seat, heads at stamp, launch authority, hard stop, load/MPS note, rulings), the `## Stamp` section, and the last line. Keep an unstamped copy (`.pre-stamp`) so the REFUSE control reads >= 1. Hard stop 15:30 / target 14:30 AEDT are my proposal as asked; the MPS seat shares the machine (load rule load1 < 7 stated as binding).

## Not done / judgment calls
- Did not open any `.tools/b4*` tree, `Notes (MASTER)`, decision queue, Jira, fleet-wide stores, or any hosted site; did not use Artifact/Docs/mail/chat.
- Mutant floor: >= 9 of B440's 14 + round-2 extras + 3 own = verdict line "n of 12+".
- Did not verify B440's RELAYED numbers (suite counts, mutants, bytes); they are labelled RELAYED in the kit.

Paths:
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B447_SEAT-G35_hpsmpoc-telemetry-gate-round3-tier1.md
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B447_DRAFTER-REPORT.md
