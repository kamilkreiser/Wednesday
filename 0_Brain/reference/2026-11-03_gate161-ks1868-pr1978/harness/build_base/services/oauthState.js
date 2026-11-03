"use strict";
/**
 * =============================================================================
 * SOCIAL OAUTH `state` STORE — KS-722 Shape 1 (KS-781's remaining door)
 * =============================================================================
 * The social sign-in initiate handler minted a `state`, put it in the provider
 * URL, returned it to the caller — and never stored it. The callback contained
 * ZERO references to it. Measured at `6dc083ba3`: `state` appeared exactly three
 * times in the whole of `routes/auth.ts`, all three inside the initiate handler,
 * and `query.state|oauthState|verifyState|stateStore|consumeState` across all of
 * `services/auth/src` returned 0 — against a non-zero control (`query.code`,
 * 1 hit) proving the probe could match.
 *
 * A `state` that is never read back is not a CSRF defence. It is the shape of
 * one. Anyone who can get a victim's browser to hit
 * `/api/auth/social/<provider>/callback?code=<attacker's code>` completes a
 * sign-in the victim never initiated — the login-CSRF the parameter exists to
 * stop (RFC 6749 §10.12).
 *
 * There was nothing to reuse. `routes/oauth.ts` (the separate `/api/oauth`
 * implementation) mentions `state` nine times and every one is PASS-THROUGH: it
 * echoes the client's value back and stores none of it. So this is a store, not
 * an adapter over an existing one.
 *
 * DESIGN NOTES, each because the alternative is wrong rather than merely worse:
 *
 *  · SINGLE USE. Consuming deletes. A `state` that verifies twice is a replay
 *    token: capture one callback URL and it works again. The read and the
 *    delete are ONE atomic step (`GETDEL`, or a MULTI where the server runs
 *    both as a unit) so two concurrent callbacks cannot both see the value.
 *
 *  · BOUND TO ITS PROVIDER. The stored value is the provider name, and consume
 *    requires it to match. Without that, a `state` minted for `google` is a
 *    valid `state` on the `github` callback — one flow's token laundered into
 *    another's.
 *
 *  · FAIL CLOSED. No Redis means no verification, and an unverifiable callback
 *    is refused. Same posture as `refreshDenylist.ts`: a Redis outage is
 *    recoverable, letting an unverified sign-in through is not.
 *
 *  · SHORT TTL. An authorization round-trip is seconds to a couple of minutes.
 *    Ten minutes is generous and bounds how long a leaked `state` is worth
 *    anything.
 * =============================================================================
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.OAUTH_STATE_TTL_SECONDS = void 0;
exports.storeOAuthState = storeOAuthState;
exports.consumeOAuthState = consumeOAuthState;
const session_1 = require("./session");
const logger_1 = require("../utils/logger");
/** Ten minutes — generous for an authorization round-trip, short for a leak. */
exports.OAUTH_STATE_TTL_SECONDS = 600;
/**
 * KS-819 F-2 — THE PROVIDER IS IN THE KEY, not only in the value.
 *
 * The original shape was one shared key per `state` with the provider name as
 * the VALUE, compared after the read. Because the read is destructive, that
 * comparison could only ever run on a value already deleted: presenting a
 * google `state` on the github callback refused correctly and destroyed the
 * user's real google flow on the way out. Binding by KEY moves the decision
 * ahead of the delete — a lookup on the wrong provider misses its own key and
 * touches nothing.
 *
 * Deploy cost, stated rather than discovered: keys written in the old shape are
 * unreadable in the new one, so sign-ins already in flight at the moment of a
 * deploy refuse once and the user starts again. Bounded by the 10-minute TTL.
 */
const stateKey = (state, provider) => `oauth_state:${provider}:${state}`;
/**
 * Record a freshly minted `state` against the provider it was minted for.
 * Throws if Redis is unavailable — the caller must not hand out a `state` it
 * cannot later verify, because that is exactly today's defect.
 */
async function storeOAuthState(state, provider) {
    const redis = (0, session_1.getRedisClient)();
    if (!redis) {
        logger_1.logger.error('[OAuthState] Redis unavailable — cannot store OAuth state', { provider });
        throw new Error('OAuth state storage requires Redis');
    }
    await redis.setex(stateKey(state, provider), exports.OAUTH_STATE_TTL_SECONDS, provider);
}
/**
 * Verify and BURN a `state`. Returns true only when the value existed and was
 * minted for this same provider.
 *
 * Returns false — never throws — for every rejection, so the caller answers one
 * refusal for "absent", "expired", "already used" and "wrong provider" alike.
 * Distinguishing them would tell a prober which of those it hit.
 *
 * KS-819 F-3 — THAT SENTENCE WAS UNTRUE, and this is what makes it true.
 * A Redis that is ABSENT returned false; a Redis that was CONNECTED BUT BROKEN
 * (loading, read-only replica, command timeout) threw, and the route answered
 * 500 where it authors 403. Fail-closed held in both cases — nothing was ever
 * signed in — but the contract did not, and a 500 on a refusal path is an
 * availability signal a prober can read.
 *
 * The catch below is deliberate and narrow: it converts a storage fault into
 * the SAME refusal every other rejection produces, and logs at error level so
 * the fault is not hidden from operations. It is not a swallowed exception —
 * the alternative, letting it propagate, is what produced the wrong status.
 *
 * `storeOAuthState` deliberately still THROWS on the same fault: handing out a
 * `state` that can never be verified is the KS-722 defect itself, so the two
 * halves are asymmetric on purpose.
 */
async function consumeOAuthState(state, provider) {
    const redis = (0, session_1.getRedisClient)();
    if (!redis) {
        // Fail closed: unverifiable is refused.
        logger_1.logger.error('[OAuthState] Redis unavailable — refusing social callback', { provider });
        return false;
    }
    if (!state)
        return false;
    // Provider-scoped: a `state` minted for another provider is a MISS here, not
    // a hit that gets compared after being deleted. See `stateKey`.
    const key = stateKey(state, provider);
    let stored;
    try {
        // GETDEL (Redis >= 6.2) is one server-side step. Where it is unavailable, a
        // MULTI still executes both commands as a unit, so a second concurrent
        // consumer's GET runs after this DEL and sees nothing.
        const client = redis;
        if (typeof client.getdel === 'function') {
            stored = await client.getdel(key);
        }
        else {
            const results = await redis.multi().get(key).del(key).exec();
            const first = results?.[0];
            stored = (first && first[1]) ?? null;
        }
    }
    catch (err) {
        logger_1.logger.error('[OAuthState] Redis command failed — refusing social callback', {
            provider,
            error: err instanceof Error ? err.message : String(err),
        });
        return false;
    }
    if (stored === null)
        return false;
    // An integrity assert, and honestly labelled as one: with the provider in the
    // key this CANNOT fail today, because key and value derive from the same
    // argument. It is here so that a later change to one half without the other
    // fails CLOSED instead of silently accepting a foreign provider's state.
    return stored === provider;
}
