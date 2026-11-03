"use strict";
/**
 * KS-698 — the rate-limit window bounds, and the two decisions that rest on them.
 *
 * Extracted from `index.ts` so the PUBLISHED contract (`security.openapi.ts`) can
 * import the same constant the runtime enforces. The #882 tier-1 gate found that
 * the runtime gained a `.max()` while the published schema kept only a `.min()`,
 * so a client following the contract could send a legal-per-spec value the
 * runtime refused — and the tool that FOUND KS-698 is spec-driven, so it would
 * have generated exactly that value. Importing `index.ts` into the spec module
 * would execute the whole service; a shared module is the smaller change.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.MAX_RATE_LIMIT_WINDOW_MS = void 0;
exports.isRepresentableInstant = isRepresentableInstant;
exports.usableRateLimitEntry = usableRateLimitEntry;
exports.persistableResetAt = persistableResetAt;
/** ECMAScript time-value range. Beyond this, `new Date(ms).toISOString()` throws. */
const MAX_EPOCH_MS = 8_640_000_000_000_000;
/** True when `ms` can be handed to `new Date()` and survive `toISOString()`. */
function isRepresentableInstant(ms) {
    return Number.isFinite(ms) && Math.abs(ms) <= MAX_EPOCH_MS;
}
/**
 * 24h. A rate-limit window longer than a day is a configuration error, not a use
 * case.
 *
 * The literal matters and is pinned by a cell: expressed as `24 * 60 * 60 * 1000`
 * the value is only ever compared against itself, so re-defining it to any number
 * at all left the boundary cells green. It is a security-relevant number — it is
 * the ceiling on how long one request can hold a key — and a security-relevant
 * constant that nothing holds is a constant that drifts.
 */
exports.MAX_RATE_LIMIT_WINDOW_MS = 24 * 60 * 60 * 1000;
/**
 * KS-698 fix 3, as a FUNCTION rather than an inline ternary — so a test can call
 * the decision the handler actually makes instead of restating it. A cell that
 * re-implements the rule passes whether or not the handler still applies it.
 *
 * Returns the entry only when it is usable. An entry whose `resetAt` cannot be
 * rendered is a key poisoned before this fix; treating it as absent routes the
 * request down the create branch, so the key heals on its next request.
 */
function usableRateLimitEntry(stored) {
    return stored && isRepresentableInstant(stored.resetAt) ? stored : undefined;
}
/**
 * KS-698 fix 2, extracted for the same reason fix 3 was — and the gate was right
 * that it needed to be.
 *
 * The reason originally given for leaving fix 2 uncovered was false in BOTH
 * halves, and the false reason is what made the gap look unclosable:
 *
 *   - "there is no way to reach it without an HTTP-level test" — an HTTP test
 *     does not reach it either. With fix 1 in place the schema refuses the input
 *     first, so the branch is unreachable over the wire as well. HTTP was never
 *     the missing ingredient; fix 1's ABSENCE is what reaches it.
 *   - "this service has no supertest dependency" — true and irrelevant. The
 *     `__tests__` directory already holds a supertest-free HTTP harness that
 *     drives this very route family.
 *
 * Which means fix 2 is NOT dead code: it is the live second line of defence under
 * exactly the drift it was kept for, and that can now be said on evidence rather
 * than asserted.
 *
 * Returns the resetAt to persist, or null when it must not be written.
 */
function persistableResetAt(now, windowMs) {
    const resetAt = now + windowMs;
    return isRepresentableInstant(resetAt) ? resetAt : null;
}
