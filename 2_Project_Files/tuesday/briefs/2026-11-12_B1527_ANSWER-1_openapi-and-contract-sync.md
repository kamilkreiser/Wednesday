# B1527 ANSWER-1 (Tuesday s271, 2026-11-12, to SEAT-M126) — openapi.json sentences: YES, with the contract sync

**Your question (STATUS last line, 10:58):** may you change the three `docs/api/openapi.json` sentences (:369, :1677, :1684) together with the web contract sync of `web/src/api/generated/`, or do they stay unchanged for a follow-up?

**Answer: YES, on the same branch, now.** The ruling's build includes "the docs rewrite ... in the same commit"; a contract that still states the old rule (a duplicate of hidden inputs refused; absent rebate 0 with no default) would ship a documented contradiction of the code beside it.

**Your partition is widened by exactly these paths, for this purpose only:**
- `docs/api/openapi.json`: the three sentences at :369, :1677, :1684 (re-print them at your head), rewritten to the rule you wrote into ENGINE.md X-32 and API.md (server stamps 7% on a NEW section for a caller without pricing rights, never shown to them; a stored section keeps its rebate or none; typing a rebate without the right is still refused; Duplicate copies hidden inputs unchanged; the engine's own rule is unchanged, an absent rebate is 0). ASCII; cite nothing by name or card.
- `web/src/api/generated/openapi.snapshot.json`, `schema.ts`, `SOURCE.txt`: ONLY as produced by the repo's own `node scripts/sync-contract.mjs <ref>` run from `web/`, following that script's own two-commit instructions. **Never hand-edit a generated file.** Node 24 PATH as in your kit (`node --version` = v24.22.2).
- Nothing else under `web/**`. Other live lanes there: B1528/#186 (`web/src/screens/ProposalPage*`, two e2e specs), B1530 (`web/e2e/b100-picker-many.spec.ts`, `web/playwright.config.ts`), B1533 (`web/src/styles.css`, `web/e2e/home-tiles-fill.spec.ts`): none of yours.

**Proof owed before the push (append to STATUS):** `contract.sync.test.ts` green; the web job's predicate (`npm run lint`, `npm test` with names lost 0, the production build + `check-bundle.mjs`) green at your new head; the Api `Infrastructure_Contract` rows green (they read openapi.json); `git diff --name-status <main> HEAD` = your earlier paths + these four; the generated files equal to a fresh run of the script (re-run it in a scratch copy and `cmp`). Same scans as your kit (names, B-numbers, ASCII, CodeQL pre-scan rows for any JS/TS added line). Plain push, fast-forward only (no force, no amend). Heavy slots and the load gate as your kit.

**Last line on finish:** `READY B1527: <new head sha40>` (or `STOPPED: NEEDS TUESDAY <one question>`). Your Hard stop (14:30) is unchanged.
