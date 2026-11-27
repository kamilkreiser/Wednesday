# FOR RECORDS: gate B2194 (lane L2, Microsoft sign-in, round 1 of 2)

For the records pass after the landing (no text of the gate goes into a project file by the gate itself).

- **Lane L2 (plan r2 line 70) DONE when the squash lands:** the Microsoft sign-in token code: the sign-in page address
  with state, nonce and a PKCE challenge (SHA-256) and `prompt=login`; the code redeemed once per state, within ten
  minutes, with its verifier; both tokens required; the id token's audience, tenant, issuer, nonce and object id
  checked (its signature not checked); the refresher behind the session broker; the app token for the card store, kept
  to five minutes before its expiry; a session's Graph token from the broker, refreshed after a 401 or the 401 stands;
  the client secret read from the secret store at each call, or a certificate assertion. Cells E01 to E19 (51 cases)
  against fakes. Against fakes only: how Microsoft Entra answers each call is UNMEASURED (RELAYED from the kit).
- **Not built:** device code (the design's default until test 1 reports), the card path's identity service (L8), the
  panel page and its return route, the host's wiring (L3b), an id-token signature check, certificate loading.
- **Unblocks:** L3b (host composition of Entra), L8 (card path), the live token check of plan r2 line 71 (app token
  first, or one sign-in after AZ-7's redirect address).
- **Owed to L3b (MEASURED by the gate, VERDICT.md):**
  1. The `HttpClient` handed to `EntraTokenClient`: no default `Authorization` header (a default one IS sent on every
     token request, MEASURED) and `AllowAutoRedirect = false` (with redirects on, a 307 or 308 resends the client
     secret, the code and the verifier to the redirect target and the module accepts that target's grant, MEASURED on
     .NET 10.0.404 over loopback). TLS validation left at the platform default; the authority host from the preset or
     fixed configuration, never from a request (R14's trust, F4).
  2. The sign-in start route: the caller authenticated (the device or its session) and rate-limited per caller;
     `MaxPending` sized to the fleet: at the default 64, 64 unanswered starts refuse every start for ten minutes
     (MEASURED, F2).
  3. The certificate the host hands in stays undisposed for the credential's life (a disposed one makes every token
     call throw `CryptographicException`, not `CredentialMissing`, F1).
- **Open for the coordinator (not blocking):** F1 (credential failures outside the secret store's own exception leave
  raw), F2 (the pending bound is one shared pool), F3 (a refresh naming another user keeps the session; the broker
  would end it only for a returned grant of another subject). Each is a small change inside the two Entra folders or
  a host rule; none is in this commit.
- Nothing here ran against a tenant, a printer or a device.
