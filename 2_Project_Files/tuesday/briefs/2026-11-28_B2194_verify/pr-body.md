## Why

The server needs its own Microsoft sign-in token code: the user sign-in shown on the printer panel, the refresh behind
the session broker, the card store's app-only Graph token, and a user session's Graph token. This is plan lane L2
("Entra sign-in"), written by hand over the host's `HttpClient` with no identity package. Every choice in it (no device
code, where the user's object id comes from, both credentials, the bounds) is the coordinator's.

## What changed

21 files, all under `src/Datasec.Suite.Identity.Entra/` and `tests/Datasec.Suite.Identity.Entra.Tests/` (18 added,
3 changed: the source project file gains three project references, and NuGet rewrote the two lock files; no package
is added).

- `EntraSignIn`: `Begin` returns the sign-in page address (state and nonce of 16 random bytes, a PKCE verifier of 64,
  SHA-256 challenge, `prompt=login`) and keeps the started sign-in in memory (10 minutes, at most 64).
  `CompleteAsync` removes it before anything else (a state completes at most once), redeems the code with its
  verifier, requires both tokens, and requires an id token whose `aud`, `tid`, `iss`, `nonce` and `oid` pass.
- `EntraTokenRefresher` (the broker's `ITokenRefresher`), `AppTokenSource` (app-only Graph token, kept to 5 minutes
  before expiry), `SessionGraphTokens` (a session's Graph token from the broker; after a 401, the broker's refreshed
  one or null).
- `SecretClientCredential` (the secret read from the secret store at every request) and
  `CertificateClientCredential` (an RS256 assertion signed by a certificate the host hands in).
- `EntraTokenClient`: one form POST per token request, no `Authorization` header, a 3xx refused, the answer read
  under a bound; fixed messages and masks for every text.

## What proves it

- Cells E01 to E19 (51 cases) against a fake handler; the Entra test executable `Total: 52, Failed: 0`; whole
  solution 2496 / failed 0 locally and on both hosted legs of the branch push.
- Eleven mutants of the change each turn their intended cell red (re-run independently: 11 of 11 MATCH), plus nine
  more independent mutants (issuer, object id, assertion life and audience, text masks, sweep, margin, renewal,
  time-out) that each turn a cell red.
- Secret scan and word scan clean over the added lines and the message.

## Named limits (from the module README and the independent read)

1. The id token's signature is NOT checked: the token arrives directly from the token address over the host's TLS
   connection, and that connection is the trust. Anyone who can answer the token request (a TLS-intercepting proxy
   the host trusts, a misconfigured authority host) already receives the client credential, the code and the
   verifier, and can name any user of the tenant; a signature check against keys fetched from the same authority
   would not stop that. The host must keep the authority fixed and the TLS check intact.
2. The host's `HttpClient` must carry no default `Authorization` header and must NOT follow redirects: measured on
   .NET 10, a client that follows them resends the form (client secret, code, verifier) to the target of a 307 or
   308 and the module then accepts that target's answer.
3. Started sign-ins live in memory, at most `MaxPending` (64) for ten minutes, shared by every caller: 64 unanswered
   starts refuse every further start for ten minutes, so the start route needs the caller's authentication and a
   per-caller rate limit, and `MaxPending` sized to the fleet.
4. An id token at a refresh naming another user is refused; the broker counts that as a failed refresh and keeps the
   session on the token it holds (it does not end it).
5. A credential failure other than the secret store's own (for example a certificate whose key cannot be used)
   leaves as the platform's exception, not as `CredentialMissing`.
6. No device code; how Microsoft Entra really answers each call (the issuer form, the assertion header and life, an
   id token on refresh, `expires_in`, the error words) is not measured: every fake answer is an assumption.
7. A session's Graph token becomes a string nobody can clear (the broker's own named limit).

## Who decides

The coordinator lands this pull request (squash, pinned to the reviewed head). Nothing ran against a tenant, a
printer or a device. Nothing is deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
