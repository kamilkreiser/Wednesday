## What this changes (RD-445, item 2 only)

The Marketplace SaaS webhook (`/api/marketplace/webhooks/...`) checks two things: an HMAC signature of the body, then a Microsoft-signed bearer token. `backend/marketplaceJwt.js` had an escape flag, `MARKETPLACE_SKIP_JWT=true`, meant for local runs and the hand-run smoke script.

**Before:** if that flag was set on a production instance, the bearer token was not checked at all. Any caller who got past the HMAC check could send any bearer value (a made-up or self-signed token, or plain text) and the request went through as `{ iss: 'skipped', sub: 'skipped' }`. The only trace was one warning line per request.

**Now:** when the server runs with `NODE_ENV=production` (compared trimmed and case-insensitively, so `Production` or a padded value counts), the flag is ignored. The bearer is checked by the same function, with the same options and the same 401 answers as when the flag is unset. The server logs one error line when the router is built and one for each webhook request that meets the flag. The log lines are fixed text; they hold no token, header or caller value.

**Kept:** the flag is not removed. Outside production it works as before, and it now also logs one warning line when the router is built, so a run with the flag on is visible before any request comes in.

## What it does not cover

- **An instance whose `NODE_ENV` is unset or is not `production` still skips the check when the flag is on.** That includes `prod`, `staging`, `development`, `test` and an empty value. The server fills an unset `NODE_ENV` with `development`. Every shipped run path sets `production` (the Dockerfile, both compose files, the Marketplace template, the systemd unit, `.env.example` and `npm start`); only `npm run dev` or a bare run with no environment leaves it out. Whether any running instance has the flag set cannot be read from the repository.
- **The new cells mock the token library (`jose`) and the logger.** They prove which path the check takes and what it does with the answer. They do not prove a signature check. The review also loaded the real library outside the test runner, with a throwaway key served on a local port and no outside network. It found that a token signed by the served key was accepted. Tokens were refused when signed by another key, when using `alg: none`, when changed after signing, when carrying the wrong audience, a non-Microsoft issuer or an expired time, when built with the HS256 key confusion, or when not a JWT. Answers were the same in production with the flag on as with the flag unset. Microsoft's real keys and endpoints were not contacted.
- RD-445 stays open for items 1, 3 and 4 (other files).
- Not deployed.

## Files

- `backend/marketplaceJwt.js`: two helpers, the production refusal and the log lines (+30 -4).
- `__tests__/rd445-marketplace-jwt-skip-flag.test.js`: new, 20 cells.
- `scripts/verify-expected-counts.json`: 6128/386 to 6148/387.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
