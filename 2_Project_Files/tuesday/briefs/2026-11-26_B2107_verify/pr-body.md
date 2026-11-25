Three backlog items of the quotes API and its docs, in two commits on `main` `56f508a7` (behind 0, ahead 2): the
contract commit `f8644cce`, then `b740f548`, which holds only the three regenerated files of `web/src/api/generated/`
(the project's own `contract.sync.test.ts` reads the contract from a committed ref, so the sync takes two commits).
Eight files: `src/MpsCalc.Api/Quotes/QuoteStore.cs`, `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`,
`tests/MpsCalc.Api.Tests/QuoteApiTests.V0Duplicate.cs`, `docs/api/openapi.json`, `docs/API.md` and the three generated
files. No package, no lock file, no project file, no workflow, no setting, no new member of the contract.

## Why

- **MPSCALC-233.** The product owner's 2026-11-11 ruling on a cloned quote's reference: a reference someone types that
  already exists is refused ("Two quotes with one reference break the audit trail."). Before this change the clone
  accepted any typed reference, including the source's own, and the docs said `quoteRef` is not unique.
- **MPSCALC-316.** The agreed sentence for the reference's length unit, "at most 100 UTF-16 code units (an emoji counts
  as two)", stood in the refusal text but not beside `maxLength` 100 in the two schema places.
- **MPSCALC-120.** The contract version practice (a minor bump plus the brief's suffix at a feature's contract change)
  is the written rule by the product owner's 2026-11-11 acceptance, and gets its own section that later work can cite.

## What changed

- **The clone (`POST /api/v1/quotes/{quoteId}/duplicate`).** A `quoteRef` the caller types (not blank) that the current
  version of any stored quote already holds, compared as the same UTF-16 code units (no trimming, no case folding), is
  refused with the existing `400 BAD_REQUEST` and its existing headline `The draft is not valid.`, with no `errors`
  entry, and nothing is stored: no quote, no event on the source. A new store method, `QuoteStore.AddIfRefFree`, makes
  the look and the add one step under one new store lock, taken before any quote's own lock and by no other path, so
  two clones typed with one reference cannot both be stored. The refusal is the last one: a missing source (404), the
  role (403), the value checks (400 with entries) and the pricing-rights 403 come first. A derived reference (no body,
  `{}` or a blank `quoteRef`: the source's with `-COPY` added) is not refused, as before, so a source copied twice
  still gives two copies that share its `-COPY` reference.
- **The answer's words.** No new sentence reaches a caller: the refusal reuses an existing headline, and the sentence
  that names the cause is left for the product owner's words. The web Clone button never types a reference, so today
  only a direct API caller can meet the refusal.
- **Docs and contract.** `docs/API.md` and the operation's description in `docs/api/openapi.json` say the refusal in
  place of the sentence that said `quoteRef` is not unique; `QuoteDraft.quoteRef` gains the unit sentence as its
  description and `DuplicateRequest.quoteRef`'s description starts with it and names the refusal; `maxLength` keeps its
  value 100 in every place. `docs/API.md` gains `## Contract version`, the rule and the nine version values the
  contract has carried (`0.1.0-lane2b` to `0.9.0-b103`). `info.version` is unchanged at `0.9.0-b103`.
- **Generated copies.** `web/src/api/generated/SOURCE.txt`, `openapi.snapshot.json` and `schema.ts` are the output of
  `web/scripts/sync-contract.mjs` run on the contract commit, byte for byte (no hand edit).

## Choices (the coordinator's, as coordinator; none is the product owner's beyond the rulings quoted above)

- Only a typed reference is refused; the derived `-COPY` reference is not.
- The match is exact and is made against each stored quote's current version only.
- The refusal carries the existing headline and no entry until the product owner gives its sentence.
- The unit sentence goes beside `maxLength` in the two schema places as the coordinator's reading of the 2026-11-11
  acceptance; whether that acceptance reaches those two places stays open for the product owner on MPSCALC-316.
- `info.version` is not bumped; the dev stub's clone (`web/src/api/stub/`) is not changed.
- **MPSCALC-195 is not in this change:** the accepted engine-target sentence it asks for is on no record available to
  this work, so it stays open until its words are supplied.

## What proves it

- The new cells failed first on the unchanged code: with the cells alone, the filtered run `V0_` read
  `Failed: 10, Passed: 136, Total: 146` (the four refusal cells and the eight-at-once cell, once per host); the blank,
  exact-match and order cells pass there on purpose, pinning what must not change.
- At the head: `V0_` `Passed: 146`; the whole Api test project `Passed: 3681, Failed: 0` (base 3663 plus 18 new);
  the Release build 0 warnings; Engine 743 and Import 198 passed; the whole `vitest` run 149 files and 1742 tests;
  `eslint`, `tsc -b`, `npm audit` and the production build with `check-bundle.mjs` rc 0.
- Two planted mutants of the store method each turn exactly one cell red on both hosts: the look and the add without
  the lock (the eight-at-once cell) and a match that ignores case (the exact-match cell).
- The independent review re-ran the red table, the green run, the whole Api project and both mutants in its own
  clones with the same totals, replayed the frozen edit list on `main` with the same five file blobs, regenerated the
  three generated files from the contract commit with the same three blobs, and probed the lock for a lock-order cycle
  (none: the new lock is taken only by the clone, which holds no quote lock when it calls it) and with 192 mixed
  requests per host at once (all finished; one holder per typed reference).
- Secret scan (gitleaks, planted control first): no leaks in the eight files or the commit messages.

## Still open (records, not this change)

- A derived reference can still equal a reference another quote holds, and a quote can still get a held reference by
  create or by an edit of its draft; the ruling is about the clone's typed reference, and whether create or an edit
  must refuse too is the product owner's to say.
- A derived copy of a source whose reference is 96 to 100 code units long, when that source is itself a derived copy
  (or its reference is 100 units ending `-COPY`), gets exactly its source's reference (the `-COPY` cut is unchanged by
  this change); MPSCALC-233's first clause is not met for that shape.
- The dev stub's clone does not refuse a repeated typed reference; two sibling length sentences still say
  "characters"; `SOURCE.txt` names the contract commit of the branch, which a squash does not keep on `main`.
- MPSCALC-195 (the engine-target sentence) and MPSCALC-316's reading of the 2026-11-11 acceptance stay open.

Who decides: the coordinator lands this change; nothing is deployed and no hosted site changes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
