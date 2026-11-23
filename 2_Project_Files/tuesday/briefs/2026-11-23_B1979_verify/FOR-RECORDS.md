# FOR RECORDS: OXPd 2 device token client (lane TA, kit B1973, seat X47), gate G1 round 1 of 2 of lane TA, reader B1979

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: this lane's cut and every choice inside it (kit B1973 D1 to
D7; Q1 = a in words at its stamp S4, Q2 to Q7 the defaults), and the landing order (TA may land first). Nothing here
says the product owner decided, ruled or approved anything about this lane (kit B1973's CLARIFICATIONS counts for the
subject words were 0, RELAYED).

## What the client does (at head 4d4e933c)

- `DeviceAuth/DeviceTokenClient`: one form-encoded POST per call to the device root plus `TokenPath` (default
  `/cdm/oauth2/v1/token`), over its own `SocketsHttpHandler` (no proxy, no redirect followed, no cookie, revocation
  check off). TLS trust is the SHA-256 of the presented leaf certificate compared in fixed time with the pin, and
  nothing else (no chain, name or expiry check; MEASURED by the gate: a pinned certificate that is expired and for
  another name is accepted; the issuer of the pinned leaf is refused, DA05).
- Three grants: administrator password (`DeviceAdminAccess`, memory only, zeroed by `Dispose`); install-code exchange
  (refused with nothing sent past the window, 5 minutes default, on the client's `TimeProvider`); refresh.
- `DeviceSolutionTokenEndpoint`: the holder's `ISolutionTokenEndpoint`; a refusal (400, 401) is null, so the holder
  marks `NeedsRepair`; every other failure throws, so the holder reports `RefreshFailed`. Reads the refresh bytes
  before returning its task (BACKLOG item 65's open part closed for this binding, if it lands).
- `IDeviceSecretVault.TryGet` doc comment: the fresh-copy sentence (BACKLOG item 45's last open line, if it lands).

## Q2 to Q5 as decided (the coordinator's), each with its UNMEASURED part

- Q2: the form and answer field names are RFC 6749's (DERIVED from the standard). UNMEASURED: every name an HP device
  sends or reads. A device that differs fails closed (`AnswerInvalid` or `Refused`).
- Q3: 400 and 401 refuse; every other non-200 is `UnexpectedStatus`; a 3xx is `Redirected` (MEASURED by the gate
  against the code: 201, 204, 402, 404, 407, 429, 502 `UnexpectedStatus`; 300, 303, 304 `Redirected`). UNMEASURED:
  which status a device gives for a wrong password, a used or late code, or a dead refresh value.
- Q4: `client_id` is sent on the refresh. UNMEASURED: whether a device needs or refuses it.
- Q5: the pin is private to `DeviceTokenClient`; L1 and IP keep their own; one shared helper is a later round.
  UNMEASURED: nothing (a structure choice).
- What a device answers to any grant, which of the two paths (`/cdm/oauth2/v1/token`, `/oauth2/v1/token`) it serves,
  and how it behaves over HTTP/2: UNMEASURED until a FutureSmart 6 device or HP's simulator is reached. The product
  owner's M577 is OXPd 1.x (B1968, RELAYED) and will never answer this client.

## From this gate (for the backlog)

1. **Owed, Minor (VERDICT FOUND 1):** a device root with a path is accepted and its path dropped (MEASURED:
   `https://127.0.0.1:<port>/base/` sends to `/cdm/oauth2/v1/token`). README Part 3 says "the device root plus
   `TokenPath`". Refuse such a root (`InvalidArgument`) or state the rule; one line plus a DA14 row in a later round.
2. **Info: AIA fetch during chain building is not switched off.** The client sets `CertificateRevocationCheckMode =
   NoCheck` but not `CertificateChainPolicy.DisableCertificateDownloads = true`. MEASURED on macOS arm64: a presented
   leaf with an unsent issuer and AIA caIssuers and OCSP URLs on 127.0.0.1 drew 0 connections to either, pinned or
   not. Linux and Windows UNMEASURED; .NET documents certificate downloads as on by default (DERIVED). The kit's D2
   wording "so the handshake fetches nothing" is not proven off macOS; the README says only "no revocation fetch",
   which is true.
3. **Info: the path checks have a near-equivalent of `//host`.** `TokenPath = "/\host/x"` passes the constructor and
   the request line carries `//host/x` to the pinned device (MEASURED: the connection stays on the device; no other
   host reached). Harmless under the pin; a stricter path rule (no `\`) is a later choice.
4. **Info: an install code is not consumed and carries no client.** MEASURED: one code exchanged twice is sent twice
   (the device decides); a code made by one client is judged by another client's clock (with two test clocks a
   20-minute-old code was sent). With `TimeProvider.System` everywhere the clocks share a base (DERIVED), so the
   window holds in the product.
5. **Info: caller cancellation** leaves as `TaskCanceledException` mid-call and before the call (0 connections when
   cancelled before), no hang; no cell covers it.
6. **Info: a UTF-8 BOM before the JSON answer is `AnswerInvalid`** (MEASURED), fail closed; whether a device sends one
   is UNMEASURED.
7. **Info: Windows hosted timing.** The adapter test assembly passed on Windows in 33.9 s at the head and 31.1 s at
   main (Linux 7.8 s and 8.0 s); the 28 new cases add about 3 s, far from the cells' 10 s guard. Per-cell times are not
   in the log.

## Carried, not in this lane (RELAYED from kit B1973)

- The host's registration of `DeviceSolutionTokenEndpoint` and of each device's root and pin (lane H or later); the S1
  install sequencer (lane L3, wave 2); OQ-2 (a stored OXPd 2 admin password) stays open.
- The pin coded three times in the wave (L1, IP, TA); folding is a later round (Q5).
- Named limits (README): leaf-hash pin only; HTTP/2 and renegotiation UNMEASURED (the client sends HTTP/1.1 requests
  by .NET's default request version, so it offers no HTTP/2: DERIVED); the window counts from receipt; `token_type`
  and `scope` not read; values pass through .NET strings; a form zeroed at a time-out may send zeros; the
  declared-length check held by the bounded read too.
- The volume event of 11:38:32 during the seat (RELAYED from its STATUS): its own results were not affected.

## UNMEASURED

Every cell and probe shape on Linux and Windows locally (only the hosted legs ran the cells, green); the AIA behaviour
off macOS; the merge with any main but da8d64a8 (IP first is landing.txt MAIN MOVES (B)); CodeQL on the pull request.
