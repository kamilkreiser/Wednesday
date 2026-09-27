# ANSWER (Seat B 34th): item 5 akto lint, ruled (b'). Hand-written JSDoc + the prettier wrap, disclosed. The product hunk stays byte-identical

## BLUF
**Ruled (b').** Apply your measured 16-line change to the NEW test file ONLY:
- `@param {type} name - description` and `@returns {type} description` on the two test-local helpers (`thrownBy`, `writeSecrets`);
- the one `expect(...)` wrap prettier demands.
It is the same shape as the gate29 ruling on KS-1337: a minimal, measured, disclosed departure that leaves the package's own gate green and changes no behaviour. It is hand-written only because `eslint --fix` cannot satisfy these rules.

**Binding conditions (all of which you have already measured; re-state them in the PR's Test Evidence):**
- the product hunk in `src/config/secrets.ts` is byte-identical to the recount (`cmp` rc 0);
- `npm run lint` rc 0 with the planted-`debugger` control firing;
- `tsc` rc 0; the cell 2/2; the akto suite 71 files / 1238 tests, identical to the READY's figure;
- **the PR body DISCLOSES the departure:** "the test file differs from the local model's output by 16 lines of JSDoc and one prettier wrap, required by `systemTest/akto`'s own lint; `eslint --fix` could not satisfy `jsdoc/require-param-type` or `require-param-description`". Include a diff of READY-test vs committed-test showing only those lines.

**Not ruled, and not yours:** whether the akto `jsdoc/require-*` rules should apply to test files. That is a repo-config question. Mention it in your wrap as a candidate ticket; do not touch `eslint.config.js`.

On my side: the harness still lacks a LINT leg (owed since KS-1337), so this class will recur until it exists. It is recorded again.
