GATE B2194: GO WITH FINDINGS @ 57b6f6e on main cf224e1

Gate G1, ROUND 1 OF 2 of lane L2 (Microsoft sign-in, the Entra token code), one Opus reader (claude-opus-5-5),
in-session, read-only, for Tuesday s336. Kit B2187 (seat X96; stamp S4: Q1 "a" no device code IN WORDS, Q2 "a" the
object id from the id token's checked claims, signature NOT checked, R14, IN WORDS; Q3-Q10 the defaults; S8 the
canonical runner 31adedc8; every choice the coordinator's). Head `57b6f6e243bbdf46c215dbfdb0f4e10353124329` on
`b2187/x96-l2-entra-sign-in`, ONE commit, one parent = `0ee3b0913c539eb34ae16ca921a65307ff7fa343` (BASE, PR 60), tree
`8efffe159000fcfe16efa57db62f5a3770badfcb`, 757 files. **Main MOVED during the gate:** PR 61 (L5) landed between
01:55:46 and 02:03:38 AEDT; main is now `cf224e1fa9050344a64d48913515654db6a80da7` (still main at 02:40:14); its 7
files touch none of this lane's paths or inputs; the gate built the squash tree on it (`aa53e949`, 762 files): whole
solution 2539 / failed 0 (landing.txt). Measured 2026-11-28 01:55 to 02:40 AEDT in scratch `fleet/state/s336/g2194/`
(`clone`: clone.py draft, push URL `invalid://no-push`, no identity, detached at the head; every mutant and probe ran
there and was undone or moved out and proved: porcelain 0 rows at the end). Every heavy job through my copy of the
kit's `heavy.py` (8 of 8 tool hashes equal THE TOOLS; heavy.py `31adedc8...` = S8) under the OXPd wave lock, one at a
time; 63 released lock folders of mine in `g2194/_quarantine/locks/`; no other holder's lock touched (I waited 21 min,
01:56-02:17, behind `B2188 seat X97`'s whole-solution job; its owner.txt read, never broken); lock free and no process
of mine left at the end. Nothing to any printer, device, tenant, Azure or Microsoft host (the probes' only sockets were
on 127.0.0.1 inside the test process); no Jira; no write to the project checkout, the seat's lane or GitHub.

## Grades (round 1 of 2): Blocker 0, Major 0, Minor 3, Info 7. Nothing blocks landing; no fix round.

**F1 MINOR (P5/P8 edge, outside every cell): a credential failure that is not the secret store's own exception leaves
the module raw, not as `CredentialMissing`, and with its own text.** `EntraTokenClient.PostAsync` (lines 60-69)
rethrows whatever `WriteTo` throws; `SecretClientCredential` maps only `SecretStoreException`; `CertificateClientCredential`
maps nothing (the key's `SignData`). MEASURED (G06): a certificate disposed after construction -> `GetTokenAsync` and
`GetNewTokenAsync` both throw `CryptographicException` ("m_safeCertContext is an invalid handle."); a store whose
`TryGet` throws `InvalidOperationException` -> it leaves as is, its message intact (the landed `ISecretStore` contract
promises `SecretStoreException`, so a conforming store does not do this). `AppTokenSource.GetNewTokenAsync` then
throws instead of answering null; the landed `GraphClient` maps ANY exception from `GetNewTokenAsync` to its 401
failure (`GraphClient.cs:543-545`), so the 401 still stands. The README's "Every failure of this module is an
`EntraException`" and `EntraClientCredential`'s summary are therefore wider than the code. Nothing was sent in either
case (requests 0 for the store). Fix shape: `catch (Exception) -> CredentialMissing` in `PostAsync`'s credential
block. Not a cell or a frozen line of this kit: a follow-up, or L3b keeps the certificate alive (FOR-RECORDS).

**F2 MINOR (Tuesday's point b): the pending-state pool is shared and refuses new starts at its bound, so 64 starts
deny every user for ten minutes.** MEASURED (G02): default options, 64 `Begin` in 0 ms, the 65th `TooManyPending`;
still refused after 9 min; accepted after 10 min 1 s. At `MaxPending` 10000 the 10000th `Begin` took 0.15 ms (the sweep
is linear, cheap) and the process held about 12 MiB. Ownership: BOTH. The module's policy (one pool for every
caller, refuse-new, no per-caller bound) is this lane's and is what makes the denial cheap (about one request every
ten seconds); the route that calls `Begin` does not exist yet, and its authentication (the device or session) and a
per-caller rate limit are L3b's. A per-IP limit alone does not hold at 64 per ten minutes. Not a P1 failure (no
sign-in completes wrongly); availability was no property of the kit. Recommend: L3b authenticates and rate-limits the
start route and sizes `MaxPending` to the fleet; a later Entra change may bind the pending entry to its caller.

**F3 MINOR (the seat's DEVIATION 4 and FOR TUESDAY question, MEASURED): an id token at refresh naming another user
keeps the session alive on the held token.** The refresher throws `SubjectMismatch`; the broker turns every refresher
exception into `RefreshFailed` (`TokenBroker.cs:409-413`) and ends a session for `SubjectMismatch` only when a returned
GRANT states another subject (`AcceptLocked`). MEASURED (G08): broker `GetNewTokenAsync` -> `TokenBrokerException
RefreshFailed`; then `GetTokenAsync` -> the FIRST user's held token; `SessionGraphTokens.GetNewTokenAsync` null (the
401 stands). No escalation: the other user's tokens are dropped; the session runs to its held token's expiry and every
refresh fails again. The kit's D5 parenthetical ("the broker then ends the session") does not hold. A coordinator's
choice: fail closed (return a grant stating the other subject so the broker ends the session) or keep as built.

**F4 INFO (Tuesday's point a, R14: no id-token signature check).** What an attacker who can ANSWER the token request
can do: they already receive the whole form (MEASURED G05: `client_secret`, `code`, `code_verifier`, or a 600-second
assertion whose `aud` is the token address), and they choose the answer: any `oid` of the tenant passes, because
`aud`, `tid`, `iss` and `nonce` are values they can read from the request or the public configuration (MEASURED: a
forged answer with another `oid` was accepted, G05). With the secret they can also mint app-only Graph tokens. A
signature check would stop the forged `oid` only if the keys came from somewhere the attacker cannot answer; keys
fetched from the same configured authority over the same client give no protection. So TLS-only trust is sound for a
confidential client AS BUILT, on the condition that the TLS channel to the real authority is the trust: OpenID Connect
Core 1.0 section 3.1.3.7 item 6 allows TLS server validation in place of the signature for an id token received
directly from the token endpoint (the gate reader's knowledge, not fetched here; UNMEASURED in this project). What L3b
must guarantee: the authority host from the preset or fixed configuration, never from input; the platform's TLS
validation unchanged (no accept-any callback); no redirect following and no default `Authorization` header (F5); any
TLS-intercepting proxy is then part of the trust and must be named in the deployment. Measured side facts: no `exp`
check (an id token with `exp` 1 accepted), the header is never read (`alg` "none", a header that is not JSON, and an
empty third part are all accepted): consistent with R14, Info.

**F5 INFO (R16, now MEASURED; README names the rule): a host client that follows redirects leaks the client's
credential and lets the redirect target choose the user.** Over a real `SocketsHttpHandler` on loopback (G05, a
rewriting handler in front of it standing in for the host): `AllowAutoRedirect` true + 307 or 308 -> the target got
`POST /steal` with the 347-byte form holding `client_secret`, `code` and `code_verifier`; the module RETURNED a grant
with the target's `oid`. 302 -> the target got a GET with no body; the module still returned the target's grant.
`AllowAutoRedirect` false -> `Redirected`, target got nothing. A default `Authorization` header on the caller's client
IS sent on the token request. The README says the host composes the client with "no default Authorization header and
no redirect following" (named). Cheap in-module hardening for a later change: refuse a 200 whose
`response.RequestMessage.RequestUri` is not the token address (it does not un-send the secret).

**F6 INFO (Tuesday's point c): `SessionGraphTokens` makes a string nobody can clear: Info, not worse.** The landed
`GraphToken` takes a string and the landed `GraphClient` builds an `Authorization` header string per request
(`GraphClient.cs:556`), so the copy is the Graph layer's design and the broker README's own named limit (line 99). The
app token is kept as a string for its whole life too (`AppTokenSource._token`), and the verifier, state and nonce are
strings while pending (README `## Limits`). Same class as every bearer client in .NET; a process-memory reader already
holds the broker's bytes.

**F7 INFO (P2/P4 shapes the kit did not name, MEASURED G03/G04/G09):** accepted: `aud` in braces, without hyphens or
with surrounding spaces (`Guid.TryParse` forms; seat R19 d); an upper-case `oid` (normalised); payload with padding or
standard base64 characters; `expires_in` 2147483647 (a 68-year app-token keep); a 200 with `text/html`; a body over
its declared `Content-Length` only on a fake (a real handler truncates). Refused: duplicate claims, `aud` as an array,
trailing slash or another case in `iss`, a missing nonce, an empty-GUID `oid`, depth 9, four parts, `expires_in` 3600.5
or `1e3`, a non-ASCII or empty token, a duplicate `access_token`, `id_token` as a number, 203/204/429 (`UnexpectedStatus`),
400 over the bound (`Refused`), 401 `invalid_grant` (`GrantRefused`). `ExtraScopes` is the caller's list: changed after
`Validate`, a scope with spaces is sent (Info: host configuration). A hint `a&prompt=none` stays one encoded
`login_hint` (one `prompt`).

**F8 INFO (mutant coverage):** the gate's four non-matching rows are explained: `gSessionRefusalThrows` is EQUIVALENT
at the Graph layer (`GraphClient.cs:543-545` turns any exception into the 401, so E16 cannot tell); the read bound
(`gReadBoundDroppedS`), the declared-length check (`gDeclaredLengthDroppedS`) and the code check (`gCodeUncheckedS`)
each survive ALONE as predicted (E07 `over` sends a declared length, so either check catches it; no cell sends a bad
code). The probes show each holds: a body with no length is stopped at 4097 bytes read (the endless stream served 4097
in all); a declared 10 with 5000 bytes -> `AnswerInvalid`; a code with a space -> `InvalidArgument`, nothing sent, the
entry kept.

**F9 INFO (P1 under concurrency and cancellation, MEASURED G01/G09):** 16 concurrent completions of one state -> 1
grant, 15 `StateUnknown`, 1 token request; a state in another case or of 10000 characters -> `StateUnknown`; a caller
cancellation mid-redeem -> `TaskCanceledException` and the state is spent (single use, by design); an already-cancelled
token -> the state is spent and the FAKE records one request (HttpClient hands the request to the handler; a real
handler checks the token first: UNMEASURED); an answer that arrives after the time-out -> `TimedOut` at 102 ms, the late
answer's token bytes are never cleared (GC memory only).

**F10 INFO (process):** seat DEVIATIONS 5 (nullable `refresh` parameter, the null check kept), 6 (`RenewAt` internal,
`Kept()` called twice), 7 and 8 (getters `AuthorityHost`, `TenantId`, `ClientId`, internal helpers): each needed or
harmless; no new public behaviour. DEVIATIONS 1 and 2 (an early C1 write put back, a `cd`) changed nothing in the
commit (C1 equals the frozen bytes, check 3). The stored commit message equals the frozen `commit-message.txt` byte for
byte (311 bytes). `mTokenRequestBearer` reddens E04, E11, E12, E14, E15 (every cell asserting a null `Authorization`),
reproduced exactly.

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), whole
1. **`BASE..head` read whole, 21 files** (`git diff --name-status --no-renames 0ee3b091 57b6f6e2`): 18 A, 3 M, 2787
   insertions, 1 deletion; every line of the 16 source files, the README, the fakes and the cells read. compare (GET
   01:55:46): ahead 1, behind 0 to BASE. `checks_l2.py` re-run by the gate over a staged copy (a second scratch clone
   soft-reset to BASE): `CHECKS: 10 of 10 PASS`, every control FIRED (check 4: the lock files' packages all in BASE's
   lock files, project entries 4 and 5; check 8: no `new HttpClient(`, handler, `.Authorization`, `device_code`).
2. **The pin run, the gate's own:** locked restore (CI=true) rc 0; unlocked restore `LOCKS: 56 of 56 equal`; porcelain
   0; build 0 warnings 0 errors; Entra `Total: 52, Errors: 0, Failed: 0`; whole solution (TIMEOUT 1800, 64 s)
   `total: 2496`, `failed: 0`, `succeeded: 2492`, `skipped: 4`, `failed Datasec.` 0, `did not end within` 0.
3. **Each mutant's reds, re-run by the gate** (the seat's rows file sha256 `a975cb39...` = the seat's STATUS; its 11
   rows equal THE MUTANTS table by program: order, file, OLD, NEW, red cell): `MUTANTS: 11 of 11 MATCH, 11 of 11 undone
   equal`, each breaking its intended row (E05 `reused`, E05 `expired`, E04, E07 `norefresh`, E06 `nonce`/`aud`/`tid`,
   E08 `redirect`, E04+E11+E12+E14+E15, E13 `otheroid`, E14). The gate's 13 rows (`evidence-gate-mutant-rows.json`):
   9 MATCH (gIssuerUnchecked E06 `iss`, gOidUnchecked E06 `badoid`, gAssertionLife E11, gAssertionAud E11,
   gGrantTextLeaks E17, gSweepDropped E18, gMarginDropped E14, gKeepsRenewalDropped E13 `keepsrenewal`,
   gTimeoutNotMapped E09), 1 equivalent and 3 predicted survivors (F8). Porcelain and files equal after; rebuild and
   `Total: 52, Failed: 0`.
4. **Twice, late, another verifier or nonce:** never (E05 rows, mStateKept, mPendingNoExpiry, mVerifierDropped,
   mNonceUnchecked; G01 16 concurrent -> 1). **A grant without both tokens, or of another audience, tenant, issuer or
   nonce:** never (E06, E07, the kit's and the gate's mutants; F7). **The refresh stating another subject:** never
   returned (E13, mSubjectUnchecked; F3 for what the broker then does). **A token request with an Authorization
   header, following a redirect, reading past its bound:** not by the module (E04/E11/E12/E14/E15 null; 3xx refused;
   bound held, F8); a host client's default header or redirect following DOES (F5, README-named). **The client secret
   read anywhere but the store, kept, or printed:** no: read at every call (G06: a replaced secret is used at the next
   call), cleared after `form.Add`, no field, fixed mask; argument messages carry no value (G09: 5 messages, 0 values).
   **The assertion's address, client id, life and signature:** E11 reads all (gAssertionAud, gAssertionLife red); a
   fresh `jti` per assertion even at one clock instant (G06); an expired certificate is NOT refused (Info). **Any
   message or `ToString` carrying a value:** no (E17, gGrantTextLeaks red), except F1's foreign exceptions. **A fake
   asserting a Microsoft behaviour as fact:** no: `FakeEndpoint`, `Answers` and `FakeSecretStore` summaries say
   ASSUMPTION; every comment about Entra says UNMEASURED or names A1.
5. **The lock files against BASE's (check 4):** PASS. **The hosted run on both legs** (gate's `hosted3.py` on push run
   46018850541, `--total 2496 --rules 757`): `HOSTED 57b6f6e2...: PASS` (linux succeeded 2492 skipped 4 GUARD 14;
   windows succeeded 2475 skipped 21 GUARD 15; RULES 757; floor 117/117; secret-scan controls and `no leaks found`);
   the Entra test dll on both legs; `failed Datasec.` 0 and 0 (control `Datasec.` 217 and 251); control `--total 2497`
   -> `FAIL 4`, rc 1.
6. **words.py and gitleaks:** SCANS. **CodeQL:** NOT RUN locally; the pull request's own run (landing.txt 3).

## TUESDAY'S POINTS
(a) F4 (R14 sound as built for a confidential client on an intact TLS channel; L3b's guarantees listed). (b) F2
(yes, a denial: 64 starts per ten minutes; both the lane's pool policy and the host's route; Minor). (c) F6 (Info).

## ADVERSARIAL: three shapes outside each property
- **P1:** 16 concurrent completions (1 wins); a bad code first (refused, entry kept, then completes); caller
  cancellation mid-redeem (state spent). Covered (F9).
- **P2:** duplicate `oid`, `aud` array, `exp` in the past (accepted: F4), `aud` forms (F7). Covered / named.
- **P3:** refresh id token of another tenant or audience (`IdTokenRefused`), upper-case `oid` (accepted, normalised),
  broker after mismatch (F3). Covered / F3.
- **P4:** no Content-Length endless body (stopped at bound + 1), caller default header (sent: F5), followed 307/308/302
  (F5). Covered / named.
- **P5:** secret replaced between calls (new one used), store throwing a foreign exception (F1), disposed / expired /
  1024-bit / ECDSA certificate (F1; expired accepted; small and EC refused). F1.
- **P6:** 16 concurrent gets (1 request), life under the margin (every get calls: correct), failed renewal (kept token
  still handed out until its renewal instant). Covered.
- **P7:** a session token with a space (`AnswerInvalid`), unknown session (`SessionNotFound` as is), refusal to null
  (equivalent at the Graph layer, F8). Covered.
- **P8:** argument messages, a foreign exception's text (F1), masks. F1.
- **P9:** whole solution 2496/0 at the head and 2539/0 on the squash tree over the new main. Covered.

## SCANS
- gitleaks 8.30.1: control FIRST (a token built from two halves and random characters, never printed, outside the
  clone) rc 1 `leaks found: 1`, moved to `g2194/_quarantine/scan-control`; `gitleaks git` over `0ee3b091..57b6f6e2`
  (`1 commits scanned`, `--ignore-gitleaks-allow`) rc 0 `no leaks found`; 26 neutral copies (21 head blobs, the stored
  message, both rows files, `mutants_c3.py`, `checks_l2.py`) rc 0 `no leaks found`.
- words.py: `--control` `CONTROL FIRED: 13 of 13`; over `added-words.txt` (2706 lines = 2787 insertions minus 81 lock
  lines) and the stored message: `WORDS: clean (2 files)`; over `added.txt` unreplaced: seat ids 10 = the 10 `S256`
  tokens (the replacement's control). B-numbers: added 0, message 0 (control: the kit 21).
- Landing texts: `words.py` over squash-subject (with #62), squash-body, pr-title `WORDS: clean (3 files)` (one `S256`
  in a first draft of the body reworded); `build/squash_scan.py` from the head's `build/` with #62: control rc 1 found
  2, message rc 0, `SQUASH-SCAN: clean`. pr-body.md holds "coordinator" and the attribution line's emoji: not
  committed text.
- CodeQL: NOT RUN locally (kit FACTS 6). Main's baseline at cf224e1f: csharp, python, actions results 0; open alerts 0.

## NOT RUN
CodeQL locally; anything against Microsoft Entra or Graph (every answer is a fake's or the gate's loopback server's);
a Windows local run (hosted only); the pull request's merge-ref build (it does not exist yet: the gate built the same
tree locally, landing.txt). No pull request opened, no push.

## MAIN AT THE END
`cf224e1fa9050344a64d48913515654db6a80da7` (GET 02:40:14; PR 61's squash, one parent 0ee3b091, `HOSTED cf224e1f...:
PASS` at 2488 / 744); branch `b2187/x96-l2-entra-sign-in` = `57b6f6e243bbdf46c215dbfdb0f4e10353124329`; open pull
requests 0; open alerts 0; newest pull request 61.

## LANDING
`landing.txt` (against main cf224e1f: merge ref total 2539, linux 2535, windows 2518, RULES 762, squash tree
aa53e949), `pr-title.txt` (209 characters), `pr-body.md`, `squash-subject.txt` (the commit subject + ` (#PRNUM)`),
`squash-body.txt`, `FOR-RECORDS.md` in this folder. Evidence: `evidence-*.txt`, `evidence-gate-mutant-rows.json`,
`evidence-probe-source.cs.txt` (the gate's probe cells, never committed; moved to `g2194/_quarantine/probe/` after the
run), `evidence-squash-tree-on-new-main.txt`. Run logs: `fleet/state/s336/g2194/logs/`.
