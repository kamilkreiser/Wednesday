/**
 * =============================================================================
 * KS-952 — THE RATE-LIMIT BUCKET NAMESPACE
 * =============================================================================
 * `POST /api/rate-limit/check` took its bucket `key` from the request body with
 * no binding to the authenticated principal, and `windowMs` per request. So any
 * authenticated caller, in any tenant, could name ANOTHER tenant's bucket and
 * set its window: a 1s window turns the owner's 100/minute into 100/second
 * (60x), and a 24h window turns an intended 60s lockout into 1440x. Both were
 * driven at the wire by the #882 tier-1 gate at two SHAs.
 *
 * THE TWO ROUTES DO NOT GET THE SAME RULE, and that is the whole point of this
 * module existing rather than one shared helper being applied blindly:
 *
 *   /check  — no role gate at all; ANY authenticated principal reaches it. The
 *             bucket is DERIVED from the principal and the body can no longer
 *             choose it. There is no platform exception: naming someone else's
 *             bucket on a *check* is the attack, not a capability.
 *
 *   /reset  — already platform-gated (`requirePlatformOperatorForRateLimit`).
 *             Clearing another tenant's bucket is plausibly the INTENDED
 *             function of a platform-operator reset, so strict binding there
 *             would break a real capability. A platform role may therefore name
 *             any scope explicitly; omitting it targets the caller's own.
 *
 * A blanket "bind the key to the principal" across both would close /check
 * correctly and break /reset. That trap was identified by the QA agent on the
 * KS-698 gate before anyone built the fix — it is its find, and it is the
 * reason KS-645 and KS-952 were merged into one ticket rather than fixed twice.
 *
 * Exported as a test seam: this service has no supertest dependency, so the
 * cells call these functions directly. Exporting changes no behaviour.
 * =============================================================================
 */

/**
 * F10: `key: z.string().min(1)` had no maximum and a 100,000-character key was
 * accepted and stored. A cap bounds one ENTRY.
 *
 * KS-952 round 2, F4 — correcting this comment's own claim rather than the
 * sweep: `sweepExpired` does NOT bound the map. It removes only entries that
 * are expired or unusable, so a caller naming many distinct keys whose windows
 * are all still open grows it past the soft max unchecked. The soft max is the
 * point at which sweeping STARTS, not a ceiling. Bounding live entries is a
 * separate decision (it means evicting a live bucket, which is itself a
 * rate-limit bypass) and is deliberately not made here.
 */
export const RATE_LIMIT_KEY_MAX = 256;

/** Above this many entries a write sweeps expired ones first. */
export const RATE_LIMIT_STORE_SOFT_MAX = 10_000;

import { isRepresentableInstant } from './rateLimitBounds';

export interface RateLimitPrincipal {
  tenantId?: unknown;
  userId?: unknown;
  sub?: unknown;
}

/**
 * KS-970 item 2. A claim is one of three things, and collapsing the last two
 * into `null` is the defect this replaces.
 *
 *   a usable string  - scope by it
 *   ABSENT           - the token simply does not carry it; fall through
 *   MALFORMED        - it IS there and cannot be used (not a string, or blank)
 *
 * The old version returned `null` for both ABSENT and MALFORMED, so a token
 * whose `userId` claim was a NUMBER was treated as if it had no user at all and
 * silently scoped to the TENANT-WIDE bucket. That contradicts this module's own
 * rule three paragraphs up - tenant alone "leaves every user inside a tenant
 * sharing one bucket ... so one tenant member could still throttle another" -
 * and it was asymmetric: the same shape on `tenantId` ended in a 403 only
 * because nothing else was left to scope by, not because it was refused.
 *
 * MALFORMED is now a REFUSAL. Absent is not: falling through from `userId` to
 * `sub` is a deliberate feature, and a token that carries neither is already
 * handled by the null at the end of `principalScope`.
 */
const ABSENT = Symbol('claim-absent');
const MALFORMED = Symbol('claim-malformed');
type Claim = string | typeof ABSENT | typeof MALFORMED;

function claim(value: unknown): Claim {
  if (value === undefined || value === null) return ABSENT;
  if (typeof value !== 'string') return MALFORMED;
  const trimmed = value.trim();
  return trimmed === '' ? MALFORMED : trimmed;
}

/**
 * KS-975 item 2 — the BODY side of the same tri-state. It exists because a body field and a
 * token claim are asked DIFFERENT questions, and `claim` can only answer one of them.
 *
 *   a TOKEN claim that is `null`  — the token does not carry it. ABSENT, and falling through
 *                                   to the next part is correct: that is what a token with no
 *                                   `userId` looks like, and `principalScope` already handles
 *                                   "carries nothing" with the null at its end.
 *   a BODY field that is `null`   — the caller SENT the field and sent something unusable.
 *                                   Treating it as absent silently retargets the CALLER's own
 *                                   bucket, which is item 1's exact shape one field over, and
 *                                   `null` is precisely what a client library serialising an
 *                                   unset field sends.
 *
 * So `undefined` (the key was not sent) stays ABSENT and still falls back to the caller's own
 * scope — that fallback is the documented `/reset` capability, not a defect — while an
 * explicit `null` is MALFORMED and refuses.
 *
 * `principalScope` is deliberately left on `claim`. Changing `claim` itself would have moved
 * the token side too, which the KS-975 fix-shape rules out in as many words: "`explicitScope`
 * should treat `null` in a body as MALFORMED while `principalScope` keeps treating a `null`
 * claim as ABSENT — different questions about different inputs."
 *
 * Reachability, stated honestly and unchanged by this fix: `scopeField()` is a non-nullable
 * `z.string()`, so the schema refuses `null` first and this arm is NOT reachable at the wire
 * today (the KS-949 gate drove it: `{"key":"login","tenantId":null}` -> 400 invalid_type).
 * This is the second line, for a caller that bypasses the schema — which is the only reason
 * the second line exists at all.
 */
function bodyClaim(value: unknown): Claim {
  if (value === undefined) return ABSENT;
  if (value === null) return MALFORMED;
  return claim(value);
}

/** The usable string, or `null` for a part that is absent. */
function usable(c: Claim): string | null {
  return typeof c === 'string' ? c : null;
}

/**
 * The namespace a principal's buckets live under, or `null` when the token
 * carries nothing to scope by.
 *
 * `null` is a REFUSAL, not a wildcard — the same rule `GET /api/audit/logs`
 * adopted in KS-743, where a caller with no tenant claim used to fall through
 * to every tenant's rows. A rate-limit bucket that defaults to a shared
 * namespace when the claim is missing is that same fail-open: it would put two
 * unrelated callers in one bucket, which is both a cross-principal throttle and
 * a way back to the behaviour this change removes.
 *
 * Both parts are included rather than tenant alone. Tenant alone closes the
 * cross-TENANT finding but leaves every user inside a tenant sharing one bucket
 * under a caller-chosen name, so one tenant member could still throttle another.
 */
export function principalScope(user: RateLimitPrincipal | undefined | null): string | null {
  const tenant = claim(user?.tenantId);
  // `sub` substitutes for an ABSENT `userId` only. A MALFORMED one is not a
  // gap to route around - falling through would hide exactly the case KS-970
  // item 2 is about.
  const rawUser = claim(user?.userId);
  const user_ = rawUser === ABSENT ? claim(user?.sub) : rawUser;

  // KS-970 item 2: present-but-unusable is a REFUSAL, not a silent downgrade.
  if (tenant === MALFORMED || user_ === MALFORMED) return null;

  const tenantId = usable(tenant);
  const userId = usable(user_);
  if (tenantId === null && userId === null) return null;
  return buildScope(tenantId, userId);
}

/**
 * KS-952 round 2, F2. A lone surrogate is not representable in UTF-8: every one
 * of them encodes to the SAME replacement bytes, so `Buffer.from(…, 'utf8')`
 * maps '\ud800', '\ud801' and '\ufffd' onto one string. Making the encoder
 * total without refusing these first would trade an uncaught 500 for a fresh
 * collision class in the exact property this module exists to establish.
 *
 * So the malformed input is refused at the boundary (`resetRateLimitSchema`)
 * and the encoder below stays total anyway.
 *
 * KS-970 item 3 — CORRECTING THIS COMMENT'S OWN EARLIER CLAIM. It used to say
 * the encoder stayed total "because the /check path builds its scope from JWT
 * CLAIMS, which no request schema stands in front of", which implies /check is
 * the ONLY unrefined path. That is FALSE, and the round-2 gate caught it:
 * `explicitScope` falls back to `principalScope(caller)` whenever the body
 * names no scope, so `/reset` reaches the encoder through raw claims TOO.
 * `resetRateLimitSchema` guards the BODY fields; it never sees a claim.
 *
 * The residual is real and is stated rather than implied away: two principals
 * whose tenant claims are DIFFERENT unpaired surrogates share one namespace,
 * because every unpaired surrogate encodes to the same UTF-8 replacement bytes.
 * Measured: `explicitScope({}, {tenantId:'\ud800'})` and the same with
 * '\ud801' both yield `t:77-9|u:…`, against a control where two ordinary
 * tenants do not collide. It is close to unreachable — claims are minted from
 * Postgres, which cannot store an unpaired surrogate — but "close to
 * unreachable" is not "refused", and the difference belongs in the comment
 * rather than in a reader's assumption. Pinned by a cell so this paragraph
 * cannot drift again.
 */
export function hasLoneSurrogate(value: string): boolean {
  for (let i = 0; i < value.length; i++) {
    const code = value.charCodeAt(i);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = value.charCodeAt(i + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) return true;
      i++; // a well-formed pair — skip its low half
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      return true; // a low surrogate with no high half before it
    }
  }
  return false;
}

/**
 * The scope parts are ENCODED, and a null part encodes to the EMPTY string
 * rather than a `-` placeholder. Both halves are load-bearing rather than
 * tidiness.
 *
 * WHY ENCODED AT ALL. The first version of this joined the raw claims with `|`
 * and `:`, and it was not injective: a victim whose userId contained `|k:`
 * shared a stored key with an attacker in a different scope who chose the
 * matching remainder as their `key` —
 *
 *   victim   t:1  u:'2|k:evil'  key 'foo'      -> t:1|u:2|k:evil|k:foo
 *   attacker t:1  u:'2'         key 'evil|k:foo' -> t:1|u:2|k:evil|k:foo
 *
 * — which is the very cross-principal collision this module exists to prevent,
 * reintroduced by the separator. Encoding removes `|` and `:` from both parts,
 * so the two delimiters are unambiguous and the map from (tenant, user, key) to
 * stored key is injective. The raw key stays unencoded: it is LAST, so nothing
 * it contains can be read as part of a scope.
 *
 * WHY NOT `encodeURIComponent` (F2). It is PARTIAL — it throws
 * `URIError: URI malformed` on a lone surrogate. Both scope builders reach it
 * with caller-influenced text, so `{"key":"k","tenantId":"\ud800"}` on /reset
 * became an uncaught 500. That path did not exist before this module, so it is
 * a regression of this change and is closed by it rather than ticketed.
 * base64url is TOTAL over every JS string and its alphabet [A-Za-z0-9-_] cannot
 * contain either delimiter, so the injectivity argument above still holds.
 *
 * WHY NO `-` SENTINEL (F3). `-` is itself a legal claim value, so
 * `buildScope(null, 'x')` and `buildScope('-', 'x')` both produced `t:-|u:x` —
 * the cross-principal collision this module exists to prevent, reintroduced by
 * the placeholder. ENCODING THE SENTINEL DOES NOT FIX THIS: base64url('-') is
 * the constant 'LQ', so the two still collide, measured. The sentinel has to
 * GO. `claim()` never returns an empty string and base64url of a non-empty
 * input is never empty, so '' is unreachable for a present value and "absent"
 * is distinguishable from every one of them.
 */
function encodeScopePart(value: string | null): string {
  return value === null ? '' : Buffer.from(value, 'utf8').toString('base64url');
}

function buildScope(tenantId: string | null, userId: string | null): string {
  return `t:${encodeScopePart(tenantId)}|u:${encodeScopePart(userId)}`;
}

/**
 * Build the scope for an EXPLICITLY named target. Only a platform role may
 * reach this — see the module header. A field left undefined falls back to the
 * caller's own claim, so naming a tenant without a user targets that tenant's
 * unnamed-user bucket rather than silently widening to the caller's.
 */
export function explicitScope(
  target: { tenantId?: unknown; userId?: unknown },
  caller: RateLimitPrincipal | undefined | null,
): string | null {
  const tenant = bodyClaim(target.tenantId);
  const targetUser = bodyClaim(target.userId);
  // A body field that is present but unusable is refused rather than treated as
  // absent - otherwise naming a blank scope silently retargets the CALLER's own
  // bucket and the route answers 200 (KS-970 item 1). The schema refuses these
  // first; this is the second line, for any caller that bypasses it.
  //
  // KS-975 item 2: `bodyClaim`, not `claim` - an explicit `null` is a field the
  // caller SENT and is refused here, while a `null` token claim stays ABSENT in
  // `principalScope`. An omitted field (`undefined`) still falls back below.
  if (tenant === MALFORMED || targetUser === MALFORMED) return null;
  const named = usable(tenant) !== null || usable(targetUser) !== null;
  if (!named) return principalScope(caller);
  return buildScope(usable(tenant), usable(targetUser));
}

/**
 * The stored map key: an encoded scope, then `|k:`, then the caller's raw key.
 * Injectivity rests on `buildScope` encoding the scope parts — see the note
 * there for the collision the unencoded version allowed.
 */
export function scopedRateLimitKey(scope: string, rawKey: string): string {
  return `${scope}|k:${rawKey}`;
}

/**
 * F10: the map was never swept, so a caller naming unlimited distinct keys grew
 * it without bound. Sweeping only ABOVE a threshold keeps the common path O(1);
 * only expired entries go, so no live bucket is ever cleared by the sweep — a
 * sweep that dropped a live entry would be a rate-limit bypass, which is the
 * thing this file exists to prevent.
 *
 * Returns the number removed, so a cell can assert the sweep rather than infer it.
 */
export function sweepExpired(
  store: Map<string, { resetAt: number }>,
  now: number,
  softMax: number = RATE_LIMIT_STORE_SOFT_MAX,
): number {
  if (store.size <= softMax) return 0;
  let removed = 0;
  for (const [key, entry] of store) {
    // `isRepresentableInstant` is KS-698's own decision, called rather than
    // restated. A poisoned entry holds a resetAt beyond the time-value range —
    // finite, and FAR in the future — so a naive `resetAt <= now` keeps it for
    // ever. Reusing the real predicate means the sweep and the read path agree
    // on what "unusable" means, which is the whole point of that extraction.
    const unusable = typeof entry?.resetAt !== 'number' || !isRepresentableInstant(entry.resetAt);
    if (unusable || entry.resetAt <= now) {
      store.delete(key);
      removed++;
    }
  }
  return removed;
}
