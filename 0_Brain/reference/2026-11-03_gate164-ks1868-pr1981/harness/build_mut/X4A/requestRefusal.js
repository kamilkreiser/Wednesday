"use strict";
/**
 * =============================================================================
 * KS-976 item 1 — a 400 must name the field that actually failed
 * =============================================================================
 * `POST /api/rate-limit/reset` answered every schema refusal with the constant
 * top-level message `'Key required'` (index.ts, the `resetRateLimitSchema`
 * arm). The QA tier-1 gate on #894 measured three refusals where the key was
 * supplied and perfectly fine:
 *
 *   {"key":"login","tenantId":"   "}      -> 400 "Key required"
 *                                            details [{path:["tenantId"], message:"must not be blank"}]
 *   {"key":"login","tenantId":"\ud800"}   -> 400 "Key required"
 *                                            details [{path:["tenantId"], message:"must not contain an unpaired surrogate"}]
 *   {"key":"login","tenantId":257 c.p.}   -> 400 "Key required"
 *                                            details [{path:["tenantId"], message:"must not exceed 256 characters"}]
 *
 * Charter §4d: a 4xx must not be scored as a healthy rejection without knowing
 * WHY it was returned — and a message that names the wrong field actively
 * misleads about the why. KS-970 item 6 had just published "Refused with 400 if
 * present but blank" for `tenantId`, so the contract promised a refusal whose
 * top-level message named a different field.
 *
 * This is recoverable rather than silent — `details` always carried the truth —
 * which is why the fix derives the message FROM `details` rather than inventing
 * a second source of truth. `details` is unchanged and still authoritative; the
 * top-level message is now a readable summary of its first entry.
 *
 * Kept in its own module, like `requestSchemas.ts`, because `index.ts` calls
 * `app.listen()` at module load — so this is unit-testable without a boot.
 * =============================================================================
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.GENERIC_BODY_REFUSAL = void 0;
exports.bodyRefusalMessage = bodyRefusalMessage;
// KS-1725: zod 4 issues rendered in zod 3.25.76's shape for every response (the client contract unchanged).
const zod3_compat_1 = require("@secuura/shared/zod3-compat");
/** The generic fallback, for an error that names no field at all. */
exports.GENERIC_BODY_REFUSAL = 'Invalid request body';
/**
 * A top-level 400 message derived from the FIRST failing path in a Zod error.
 *
 * The first issue is used rather than all of them: the top-level message is a
 * summary for a human reading a log line, and `details` — untouched — is what a
 * client parses. Joining every issue would produce an unbounded message whose
 * length a caller controls, which is a different defect.
 *
 * A path-less issue (the body itself is the wrong type, so `path` is `[]`)
 * falls back to the generic form rather than emitting a stray separator.
 */
function bodyRefusalMessage(error) {
    const first = (0, zod3_compat_1.zod3Issues)(error.issues)[0];
    if (!first)
        return exports.GENERIC_BODY_REFUSAL;
    const path = first.path.map((segment) => String(segment)).join('.');
    if (path === '')
        return exports.GENERIC_BODY_REFUSAL;
    return `${exports.GENERIC_BODY_REFUSAL}: ${path} ${first.message}`;
}
