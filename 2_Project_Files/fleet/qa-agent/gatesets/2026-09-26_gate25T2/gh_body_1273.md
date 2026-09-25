#1273 KS-1321: match the description verb on a word boundary, not a bare includes
head b800791a3295f048b40f920435b080a270c65106

## What

`DESCRIPTIONPOINTSATSOURCE` (landed by #1252) forbade a dedicated-route verb appearing in the published `LifecycleEventRequest.action` description by **substring** match: `dedicatedVerbs.filter((verb) => description.includes(verb))`. Several of those verbs are ordinary English words — `anchor`, `revoke`, `share`, `verify`, `version` — so the check could refuse innocent prose while proving nothing about a real relabel.

**Measured on the three descriptions the ticket names**, and this is in the GREEN cell as its own conjunct: `"a new version of this list"`, a back-quoted `` `version` ``, and a slash-delimited `/version` all return `["version"]` from the bare `includes()`. **All three, identically** — so the old check could not discriminate them at all. It reds today on nothing, because the live description happens to contain no verb substring; the widening was latent.

## The rule, and why each branch is the width it is

- a **hyphenated** verb (`sig-json`, `sign-cert`, `sign-wallet`, `transfer-custody`) cannot occur as ordinary English, so a word-boundary match is enough and nothing is given up;
- a **single-word** verb counts only in **route-token** form: back-quoted, or slash-delimited on either side.

**The `verb/` form is in that rule because of a measurement, not by symmetry.** With only `/verb`, the historical inline list `share/transfer-custody/revoke` returned `['revoke','transfer-custody']` and **missed `share`** — the one term with no slash in front of it. The list still reddened the cell, so the guard was working; but a rule that can only see the tail of a list is not describing the shape it refuses. An arm of mine whose *expected value* was wrong is what surfaced it, and the expectation was the wrong thing to correct.

**What the rule still does NOT catch is stated in the code, not left implied:** a single-word verb written as bare prose with no delimiter (`"share must use its own route"`). That is inherent to the fix the ticket asks for — `version` in "a new version" is the same string as the verb, and only the delimiter tells them apart. The hyphenated verbs have no such ambiguity, which is why their branch exists.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts` (test-only).

**Ran** — `worktrees/s-b29-ks1321` at develop `4db87c3e4b98`, `packages/shared` BUILT (88 dist files):

| arm | result |
|---|---|
| originate BARE, `npx jest --runInBand` in `services/originate` | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED, same command | **880 passed / 880, 74 suites**, rc 0 (+2 cells) |
| `ks978` file alone, BARE | 13 passed / 13 |
| `ks978` file alone, PATCHED | 15 passed / 15 |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

`packages/shared` is run because its guard suites read originate sources by TEXT. Both restores between arms were asserted by sha256.

**Red-proved one conjunct per arm, six arms, each reddening EXACTLY the named cell (14 passed / 1 failed each):**

| arm | conjunct falsified | cell that reds |
|---|---|---|
| C1 | the helper reverts to the bare `includes` | ORDINARYWORDSTAYSGREEN |
| C2 | the `verb/` alternative dropped (the list's FIRST term) | ROUTETOKENSTILLREDS |
| C3 | the back-quoted alternative dropped | ROUTETOKENSTILLREDS |
| C4 | the `/verb` alternative dropped | ROUTETOKENSTILLREDS |
| C5 | the hyphenated branch removed | ROUTETOKENSTILLREDS |
| C6 | the non-vacuity conjunct: the registry read yields NO verbs | ORDINARYWORDSTAYSGREEN |

Three instrument rules in the runner, each from a recorded failure: every tamper asserts its anchor is **unique** and stops the run otherwise; every arm names the cell it expects and FAILS if a different cell reds **or none does**; verdicts are read from `--json` `fullName`, never the console line.

**Two defects in my own runner, found by running it:**
1. **`C5` applied and was INERT.** Removing the hyphenated branch changed nothing, because every fixture's hyphenated verb was *also* slash-delimited and the single-word rule already caught it. A tamper that finds nothing is a statement about the fixtures, not the product — so a discriminating fixture was added (`"A transfer-custody must use its own route."`, hyphenated in **bare prose**), which is the only case that branch is needed for. C5 is now a real arm and the branch is proven load-bearing.
2. **`C6` returned 0 passed / 0 failed** — the suite never compiled (an unused parameter), which reds nothing and is indistinguishable from an inert tamper if only the failed set is read. The runner now treats `0 passed and 0 failed` as its own `LOADFAIL` verdict rather than a silent miss.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `11/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves in this PR, so there is no LEG-8-PORT reading.
- The ticket's title says `ks1293/ks978`; the `ks1293` file is #1261's and is not on develop, so **only `ks978` is touched** here.
- The rule's uncaught case (a bare, undelimited single-word verb) is **not** covered by a cell, because no fixture can distinguish it from prose. It is recorded in the code instead.

Refs KS-1321

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Base attribution for the counts above (per the 19:30Z fleet correction)

**This worktree does NOT contain develop `d7cdecf1d2ee`**, and the object is not even present in the checkout — no fetch was taken. Measured: `git cat-file -t d7cdecf1d2ee` fails here, against a positive control where `git cat-file -t 4db87c3e4b98` returns `commit`. The worktree base is `4db87c3e4b98` (`HEAD~1`).

So every count in this PR measures **`4db87c3e4b98` + this change**, not the combined tree with `d7cdecf1d2ee`. The push gate read `pre_push_hook_base` **28/0**, `fixture_guard` **6/0**, `run_shell_suites` **49/0**, shell suites **60 passed / 0 failed of 60**, and `^FIXTURE BUILD FAILED` **0 times** — the same quadruple the fleet declaration names for `d7cdecf1`, but **this is not a confirmation of it**: a pre-merge worktree reading the old quadruple is the old tree agreeing with itself. Stated as attribution, not as evidence about develop.

