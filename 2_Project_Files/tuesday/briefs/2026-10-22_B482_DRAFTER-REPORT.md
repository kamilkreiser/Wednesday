# B482 drafter report (Sonnet, read-only), 2026-10-22 about 22:10-22:35 AEDT

Brief: `2026-10-22_B482_SEAT-A2_hpsmpoc-b466-heldname-fixround1.md` (115 lines) plus `.pre-stamp` (cmp equal). Fix round 1 of 2 on `b466/hpsmpoc-177-178-hidden-chars` @ `3eded1128663b53251e3f263f8d0e6985dcdbce7`; pane `Datasec/HPSM-POC-A2` (live panes at 22:2x: G45, H5, R2, W2, fleet-monitor, tuesday; no A1, no A2); Sonnet C2; delta gate tier 1 after. Shape cloned from B481.

## Read
B478 STATUS (163 lines, whole), B481 `.pre-stamp` + drafter report, B466 brief (whole), ADDENDUM-2 (whole), B466 STATUS lines 1-20 and 75-95 (ADDENDUM-1 not opened: its lock rules are in B481's standing line 9, reused). `git show 3eded112:` of `Requests.cs` :122-165 and :208-222, `CustomerEndpoints.cs` :186-215, `customer-detail.ts` :1-130, `Hpsmpoc177InvisibleCommentTests.cs` :1-40 and :155-215, `Hpsmpoc178CustomerNameTests.cs` :1-75, `InvisibleCharacterTests.cs` :67-92, `ApiSteps.tsx` :70-78.

## Item -> file:line map (head 3eded112)
| Finding | Item | Source | Test home |
|---|---|---|---|
| B478-1 MAJOR | 1 | `Requests.cs:134-135` signature, :141 the rule, :147 the `heldIndustry` use; `CustomerEndpoints.cs:194` update (passes `heldIndustry`), :73 create (no held arg); mock `customer-detail.ts:55` `nameRefusal`, :83 its PUT call, :85 `readIndustry(b, c.industry)`; `api.ts:193` create call | `Hpsmpoc178CustomerNameTests.cs` (plant via `factory.Database()` :75); `customer-name.test.ts` |
| B478-3 MINOR | 2 | note guard `Requests.cs:213-221` (`HasControl(notes)` :216); weak row `Hpsmpoc177InvisibleCommentTests.cs:183` | new row in `Hpsmpoc178CustomerNameTests.cs` (Api project; `Journey` helpers, pattern at `InvisibleCharacterTests.cs:70-85`) |

How `heldIndustry` works: `Shape.Customer(..., string? heldIndustry = null)` (:134-135, doc :132); the industry rule is refused unless `CustomerIndustries.IsListed(chosen)` OR `string.Equals(chosen, heldIndustry, Ordinal)` (:147); only the update passes it (`CustomerEndpoints.cs:194`, `heldIndustry: customer.Industry`); the mock twin is `readIndustry(b, held)` (`customer-detail.ts:45`, called :85 with `c.industry`). The brief mirrors it: `heldName` last optional parameter, `HasControl(name) && !string.Equals(name, heldName, Ordinal)`, update passes `heldName: customer.Name`, create unchanged, mock `nameRefusal(b, held = null)` with `putCustomerRoute` passing `c.name`.

## Partition intersection (`git diff --name-only 48521806...<tip>` vs Yours = b466's 10 paths + `CustomerEndpoints.cs` = 11)
```
b465 c65a5ab667e7 n=19 shared=0
b467 d6eba5f68137 n=9  shared=0
b461 53052201a968 n=14 shared=0
b429 4c02e8b94f19 n=43 shared=0
b462 e8ecb8ae5fca n=6  shared=0
b472 e353322e7094 n=1  shared=0
b460 b9fd28edff53 n=1  shared=0
planted control (Requests.cs appended to the b465 list): 1
self control: 11
main-only paths (8) vs Yours: 0
```
Empty. B481 (R2, live) will add `ShowcaseSeedTests.cs` and Reporting test paths to b467 later: none are in Yours (b467's own list has 0 ShowcaseSeedTests today; the scratch lists were not retained beyond the scratchpad).

## Main vs branch
`merge-base 3eded112 48521806` = `4695d7f2`. `rev-list --left-right --count 48521806...3eded112` = `3 2` (main-only `d70f9dc` #182, `1d1fa46` #183, `4852180` #185). Legacy 3-arg `merge-tree 4695d7f2 48521806 3eded112`: 0 `+<<<<<<<` (no marker control built here). Main-only paths vs Yours: 0. Default in the brief: no main merge. The gate did not run `4852180`; the PR merge ref covers it.

## Ports and locks
Block **8330-8339**: `grep -w '833[0-9]'` over `tuesday/briefs/*.md` no hit (control: `832[0-9]` hits B481 files; 8300-8329 are named in B478/B480/B481 and neighbours); `lsof -nP -iTCP:8330-8339 -sTCP:LISTEN` empty, rc 1, 14 listeners overall (positive bind control left to the builder). `.tools/b482` absent (`ls -d` error), no `wt-b482-*` (`find` empty); `.tools/b198/lock.sh` and `.tools/b267/waitload.sh` exist; no `refs/heads/b482*` on origin (control: the same `ls-remote` listed b46*, b47* lines). Stamp slots `grep -c -E '_''_''_''_'` = 8; person-name grep = 0 (control: `Kam x` = 1). Non-ASCII in the brief: only U+00B7 (as in B481); the file tool turned my U+202E escape into a raw char once, caught and re-escaped by program.

## Assumptions (marked)
- The note-surface row lives in `Hpsmpoc178CustomerNameTests.cs` (Api project, ApiFactory, Journey helpers) because the Feedback test project cannot reach the Journey helpers (not checked beyond its csproj referencing `HpsmPoc.Api`, not `Api.Tests`). The row is a 177 counterpart sitting in a 178 file: a no-new-file choice. Your call.
- Item 2 is green at base and head by design (the route already refuses); its proof is mutant M482-N1 (`Requests.cs:216`), not red-at-base.
- Held comparison is ordinal against the stored (already trimmed) name with no trim, as `heldIndustry` is; not measured against a name stored with an edge character.
- Optional one-clause README edit allowed only if the B92-R1 row would read false (not checked line by line; the row at README :86 says names are refused "on create and rename").
- `CustomerEndpoints.cs` is the one product file b466 did not touch; the brief adds it to Yours explicitly (the gate's protected list named it).
- Whole-Api expected figure left for the builder to print (the gate's 1887 was on the merged tree at `1d1fa46`, not the head).
- Mock state's ability to hold a hidden stored name unmeasured; unit rows cover `nameRefusal` either way.
- B478-2, -4, -5, -6, -7 are named as not in scope; hard stop / target READY left to you at stamp.
