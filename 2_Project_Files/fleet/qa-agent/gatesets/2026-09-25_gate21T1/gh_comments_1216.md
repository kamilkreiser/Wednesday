--- comment 5826043933 by linear[bot] at 2026-09-25T03:11:01Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-975/ratelimitscope-tri-state-a-malformed-sub-silently-became-a-403-on-the">KS-975 rateLimitScope tri-state: a MALFORMED `sub` silently became a 403 on the ungated /check, and `null` still slips through explicitScope's second line</a></summary>
<p>

## BLUF

**Two arms of the ABSENT-vs-MALFORMED tri-state in** `rateLimitScope.ts` **that nothing pins.** Item 1 is a **behaviour change that already shipped on a live, ungated route** and is currently reversible without a single test going red. Item 2 is a hole in a backstop, not reachable at the wire today.

**Correcting the framing I was handed:** the grouping described both as *"unpinned arms rather than live defects"*. That is right for item 2 and **understates item 1** — item 1 changed a live response from **200 to 403** on `/api/rate-limit/check`, which has **no role gate**. Unpinned, yes; but not merely theoretical.

## ITEM 1 (MINOR by severity, but a live behaviour change — gate F-2) — a MALFORMED `sub` became a refusal, undisclosed and unpinned

**Location:** `rateLimitScope.ts:118` — `const user_ = rawUser === ABSENT ? claim(user?.sub) : rawUser;`

Gate measurement, same input at both SHAs:

| claims | #893 `ab1053141` | #894 `e02d0fecc` |
| -- | -- | -- |
| `{tenantId:'…a', sub:123}` | `t:…\|u:` (tenant bucket, **200**) | `null` **-> 403** |
| `{tenantId:'…a', sub:'  '}` | `t:…\|u:` (**200**) | `null` **-> 403** |

`sub` inherits the refusal because `claim(user?.sub)` can itself return `MALFORMED`, and `:121` refuses on `MALFORMED`.

**Verified in code at** `0281b0faa`**:** the comment at `:114-116` does address `sub` — but only to say a MALFORMED `userId` must not route around via `sub`. It never states that a MALFORMED `sub` is itself a refusal. So the gate's reading is right: the documented tri-state covers `userId`, and the new cells cover `sub` only as a good string.

**It is unpinned, proved by the gate:** restoring #893's behaviour (map a MALFORMED `sub` back to `ABSENT`) leaves **all 179 cells green**. A future change can silently revert it. **A check that cannot fail wearing a feature's clothes.**

**Fix-shape:** decide it deliberately, say so in the comment, and pin it — one cell each way (`sub: 123` refuses; `sub: 'u1'` scopes), so the arm has a failure mode.

## ITEM 2 (MINOR, gate F-4) — `explicitScope`'s second line still has item 1's exact hole for `null`

**Location:** `rateLimitScope.ts:86` — `if (value === undefined || value === null) return ABSENT;`

The design is stated at `:228-231`: *"The schema refuses these first; this is the second line, for any caller that bypasses it."* Across 14 shapes the second line refuses 12 (`'   '`, `'\t\n'`, `''`, NBSP, BOM, U+3000, `123`, `{}`, `[]`, `false`, `NaN`, `0`) and **treats JSON** `null` **as ABSENT**, which falls through to `principalScope(caller)` — reproducing item 1's exact shape: a **present** field silently retargeting the caller's own bucket.

**Honestly bounded, and this is the half not to lose: NOT reachable at the wire today.** `z.string()....optional()` rejects `null` — the gate drove it: `{"key":"login","tenantId":null}` -> `400 invalid_type, expected string, received null`, caller's bucket untouched. Independently confirmed here before filing: `scopeField()` is a non-nullable `z.string()`, and the only product caller of `explicitScope` (`index.ts:1373`) passes already-validated `parsedBody.data`.

So this is **a hole in the backstop, not a live defect**. It matters only because the backstop exists precisely for the case where the schema is bypassed — and `null` is exactly what a client library serialising an unset field would send.

**Fix-shape:** `explicitScope` should treat `null` in a **body** as MALFORMED while `principalScope` keeps treating a `null` **claim** as ABSENT — different questions about different inputs. **Regression test:** extend the second-line cell with `explicitScope({tenantId: null}, caller)` -> `null`, plus a CONTROL that `explicitScope({}, caller)` still returns the caller's own scope.

## SEARCHED BEFORE FILING

SYMBOL `rateLimitScope`, `explicitScope`, `principalScope`, `claim(`, `MALFORMED`, `ABSENT`, `scopeField` · PATH `services/security/src/rateLimitScope.ts`. Only **KS-970** (this work's parent) returns an open hit; `scopeField` returns 0. Control: a `KS-970` search is non-zero, so the search discriminates.

## PROVENANCE

QA tier-1 gate on **#894 over #893**, verdict 2026-09-07T09:45:45Z, quoted verbatim by the coordinator. **Every code claim re-verified against** `0281b0faa` **before filing.**
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-975-scopenull-explicitscope-treats-an-explicit-null-body-field-as-260e5bd82e3b">Review in Linear</a></p>

