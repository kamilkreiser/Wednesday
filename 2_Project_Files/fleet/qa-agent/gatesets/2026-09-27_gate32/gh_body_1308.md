#1308 KS-1108: name the file and position when akto's secrets.yml will not parse
head f9348a9d10b7512d22a33a0a471f9042ad622831

Refs KS-1108

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run.

## What changes

`systemTest/akto`'s `loadSecretsYml` parsed `config/secrets.yml` with **no catch**. A malformed file therefore threw js-yaml's own `YAMLException`, which carries **the whole file in `mark.buffer`** and, for a bare tag or anchor value, **the value itself in `reason`**. Any uncaught print showed every credential in the file.

The parse is now wrapped. On failure it throws an `Error` naming **only the file and the position** — never the reason, the message, the mark, or a cause. Plus a new akto unit cell that plants a secret-shaped sentinel in a malformed file and asserts the thrown error does not carry it, with a control that a valid file still parses.

**Not covered, stated rather than implied.** The cells pin the *thrown* error. They do **not** capture stdout, so a future logger that prints the raw exception elsewhere would not be caught here. Key-suffix matching has limits: the redaction names a position, not a taxonomy of what could leak. `Refs`, not a close.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**The READY's hunk headers are miscounted**, so the brief's recounted copy was used. **Proven equivalent, not assumed:** stripping the `@@` lines from the READY block and from the recount leaves them **identical, 81 lines each**; the two header changes are `-36,7 -> -36,5` and `+1,82 -> +1,58`; a control fires on a one-token mutation. The READY's `-36,7` is **arithmetically wrong** — the hunk body has 4 context + 1 removed = **5** old-side lines. Under GNU `patch -F0` the READY block gives rc 2 (`malformed patch at line 24`) and the recount rc 0; under `git apply --check` the READY-headed section is refused outright.

**Apply.** Strict `git apply`, no `--recount`, no fuzz: **both sections rc 0**. Each with a control that must fail:
- section 1 is an **existing** file, so a **path tamper** is valid: rc 1, `No such file or directory`.
- section 2 is a **new** file, so the **hunk count** is corrupted instead: rc 128.
- **And the reason the path arm would not do for a new file is measured, not quoted: a wrong-path new file still applies, rc 0.** That control would have proven nothing.

**RED — the product hunk WITHHELD** (this item changes product, so no tamper is needed):
- **1 failed / 1 passed of 2**, and the failure is the declared cell **on its assertion**: `AssertionError: expected 'YAMLException: unknown scalar tag !<!…' not to contain 'ks1108-tag-Pw-4c2e91'`. That sentinel is the secret-shaped token the test plants in the file, and at the base the raw exception carries it. **That assertion is the ticket.**
- Restored and verified byte-identical to my head.

**GREEN at my head.** The cell: **2 of 2 passed**.

**Suite, bare vs patched** (`vitest run -c vitest.unit.config.ts`):

| | files | tests |
|---|---|---|
| bare (product reverted, test moved aside) | 70 | **1236** |
| patched (my head) | 71 | **1238** |

**0 new reds.**

**`tsc`.** Unlike the api-gateway packages, **akto's own tsconfig does not exclude its tests** — measured with `--listFilesOnly`: the program is **563 files and this new test is present exactly once**. So no widened program was needed. `tsc --noEmit -p tsconfig.json`: **rc 0, 0 errors**.

**Lint, and a control that actually fires.** `npm run lint` is **rc 0**. ⚠ The planted-`debugger` control used for the api-gateway packages **does not fire here** — `no-debugger` appears **0 times** in akto's `eslint.config.js`, so that plant is the wrong instrument for this package and its silence proved nothing. Replaced with a plant this package demonstrably enforces: **removing one `@param` line gives rc 1, `jsdoc/require-param`**, and restoring it returns rc 0. The zero is proven.

**Gate lines: `fleet STOP: NOT APPLICABLE (format gate only)`.** This push touches **no `Blockchain/Dev/` path**, so the pre-push hook's path filter means the platform preflight **never ran**, and none of the fleet STOP counts apply here. Measured with a control: the tokens `pre_push_hook_base`, `PREFLIGHT INCOMPLETE` and `code guards passed` appear **0, 0 and 0** times in this push's log and **4, 1 and 1** times in a `Blockchain/Dev` push of mine. What did run:

```
[format-gate] systemTest/akto — format:check OK
[format-gate] 1 package(s) checked, 0 skipped, 0 failed
```

Push rc 0; `ls-remote` after the push confirms the branch at this head.

## DISCLOSED DEPARTURE FROM THE LOCAL MODEL'S OUTPUT

**The new test file differs from the model's output by 16 lines: 12 of JSDoc and 4 of one wrapped call.** It is required by `systemTest/akto`'s **own** lint, which the model's output failed with **5 errors** (`jsdoc/require-param` ×2, `jsdoc/require-returns` ×2, `prettier/prettier` ×1) while `tsc` was green — `tsc` green is not lint green.

**`eslint --fix` could not fix it, and made it worse: 5 errors became 6.** It scaffolds a bare `@param fn` line, which then trips `jsdoc/require-param-type` and `jsdoc/require-param-description`, rules it cannot invent values for. So the JSDoc was hand-written with types and descriptions on the two **test-local** helpers (`thrownBy`, `writeSecrets`).

Classified line by line, the 16 changes are **12 JSDoc, 4 prettier-wrap, 0 other** — documentation and formatting only. The whole akto suite reads **71 files / 1238 tests** both with the model's bytes and with the committed version, so no behaviour changed. **The product hunk in `src/config/secrets.ts` is byte-identical to the recount** (its `+`/`-` line sequence compared directly: 15 lines, identical).

A candidate follow-up, not taken here and not mine to decide: whether akto's `jsdoc/require-*` rules should apply to test files at all. Nothing in `eslint.config.js` was touched.

## Wednesday's figures, as hers
Re-checked today at this tip in her scratch clone: the test file alone **1 failed / 1 passed**, with the product hunk **2 passed**, and the whole akto unit suite **71 files / 1238 tests**. Not my proof; mine is above.

