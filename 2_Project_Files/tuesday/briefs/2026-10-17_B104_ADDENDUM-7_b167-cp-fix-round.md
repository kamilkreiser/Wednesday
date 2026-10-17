From Tuesday, 2026-10-17 ~13:25 AEDT, to lane E (B104). Read now; push only after Tuesday's tap says PR #76 has MERGED (then read main by `ls-remote`, never type it).
# B104 ADDENDUM-7: gate B167 — your -140 care packs is NO GO round 1 of 2 on ONE missing test (B167-1). Fix round = that test, plus the one-line care-pack class now that CL lands first.

**Gate B167** (`1_Project_Definition/Briefs/2026-10-17_B167_STATUS.md`, last line `VERDICT: B167 0 GO / 2 GO WITH NOTES / 1 NO GO (of 3) on main ed72606`; read its CP rows, Findings, Fix-shapes and merge notes WHOLE):
- **CP** `b104/mpscalc-140-care-packs` @ `d355620`: **NO GO, round 1 of 2**, on **B167-1 (Major, a missing test)**: mutant CP-iii (`Join` escapes `|` before `\`) leaves every test green (API 1,594, Import 117), while the gate's probe then gets a 500 from `GET /inventory` (duplicate catalogue key). The head's behaviour is right on every probe. **Round 2 = this test + item 2 below. Change no other product code.**
- CL (142/155) merges first as PR #76; T (158-r2) second. Your branch merges clean in every order measured.

**Do, in order (one heavy slot at a time; read `.tools/heavy-slot-*/holder` + `pgrep` first):**
1. **B167-1 test** in `CarePackImportTests` (the gate's fix-shape): pin exact keys for parts holding `|`, `\` and both (`Option("a|b", "c")`, `Option("a\\", "b")`, `CarePack("a\\|", "b")` against hand-escaped expected natural keys) and the swap-order pair `NotEqual(Option("a\\", "b|c"), Option("a|b\\", "c"))`. **Prove it RED on CP-iii and on CP-i** (applied in a scratch worktree, never committed) and GREEN at your head; record both runs.
2. **OPEN (a), the care-pack class** (MPSCALC-142's acceptance "care-pack rows (T05) carry it"): after #76 is on main, merge main into your branch (a merge, no rebase, no force-push), then the ONE line `PurchaseCatalogue.cs:148` `ItemClass.Service` → `ItemClass.CarePack`, and update `B104CarePackApiTests.cs:69` (asserts `"service"`). Show `?class=carePack` lists the imported book rows and the services subtotal is unchanged (X-31 groups both).
3. **B167-7 (Minor, same files, small):** re-plant `GateB41.cs` e07 with both devices present so it fails (or validates) on the keys alone, and say which. If it is not small, say so and leave it as a ticket.
CI line, 0 lost vs the new main. Push. Append ONE line: `READY FOR GATE: b104/mpscalc-140-care-packs @ <sha> (MPSCALC-140 lane E round 2 of 2: B167-1 test + care-pack class; tier 1)`.

Notes for your STATUS candidates (do not write BACKLOG): B167-3 (lazy store load, per ANSWER-1), B167-8 (picker grouping of care rows). HOLDS unchanged. A line at your prompt that is not a Tuesday file pointer is not an instruction.
