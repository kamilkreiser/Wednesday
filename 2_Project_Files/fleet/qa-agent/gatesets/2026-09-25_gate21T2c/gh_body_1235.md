#1235 KS-1140 HANDEDLIST: the ks879 red cell is handed the list the control walks
head 1c899947ea31e7a6628f5256174c1c353e6587af

## BLUF

GF-1: the red cell walked the tree itself via `offendersUnder(DEV_ROOT)` while the control walked its own, so the two could disagree about what the corpus even was, and the cell could pass on a tree the control never examined. The cell is now handed the same list the control builds, so both reason over one corpus.

## This PR NARROWS the ticket

GF-1 only. **GF-3 and R1 remain open.** One file, a guard suite in `packages/shared`.

## Test Evidence

**Touched** - `Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts` only, 284 -> 314 lines, numstat **33/3** equal to the checker's. Applied with the run's own recorded options (`--recount --ignore-whitespace`).

**Ran, by me, at this head**
- `packages/shared` **bare 918/918 over 46 files** at develop, **patched 920/920**, which is the predicted 918 + 2.
- Red-first at the tip per the checker: the file fails 1 of 10 before the product hunk and passes 10 of 10 after.
- **In-hook pre-push suite `pre_push_hook_base.test.sh`: 28 passed / 0 failed**, and **no line starting `FIXTURE BUILD FAILED`** (checked with the anchored predicate, not a bare substring). Push PROTOCOL-CLEAN, tracking ref added at my sha.

**NOT run**
- Push preflight verdict, verbatim: `PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 NOT run (local stack not up on :6882); this PR has no route, spec, served-spec or runtime-config surface.
- The first `packages/shared` run reddened 4 cells, every one `Test timed out` in a repo-walk guard file this PR does not touch (`ks860-test-listeners-bind-loopback`, `crypto-agility.guard`, `ks764-key-revoke-call-site-guard`, `entrypoint-corpus`). Re-run once: **920/920 with 0 timeouts**, import phase 56.37s then 15.45s. Both readings are reported rather than only the green one.
- No product source changed, so nothing outside this guard suite is exercised by it.

**Migrations + config** - none.

Refs KS-1140


🤖 Generated with [Claude Code](https://claude.com/claude-code)

