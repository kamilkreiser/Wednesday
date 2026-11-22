Adds the local registration material of the Universal Print connector (WP4.1, in part): one new folder
`Registration/` in `src/Datasec.Suite.UniversalPrint` (beside the untouched `Ipp/` encoder) and one in its test
project. Two commits on main `185b9eef`: the change itself (`f4cee23b`) and ONE fix commit (`94fe6067`, below).
**Nothing here calls Universal Print, Microsoft's registration or device-token service, or any other endpoint, and
nothing is built on any app registration: no client id, tenant, endpoint or scope appears in the code.**

## What it adds

- **`RegistrationKeys`** (behind `IRegistrationKeys`): per registration an RSA-2048 key pair made in process and a
  PKCS#10 signing request (SHA-256 with PKCS#1 v1.5, no extension, over the fixed subject the Workpath client sends).
  The private key is kept only as ONE record of the secret store it is given (`ISecretStore` on main), named
  `uprint/` plus a random 32-hex id; the record is the library's own JSON, read back strictly. `CreateRegistration`
  hands out the id, the request and the public key. No public or protected member returns private-key bytes, an
  `RSA` object or a certificate holding a private key.
- **`AttachCertificate`** keeps an issued certificate in the same record only when, in this order: the id parses;
  the bytes are not empty and at most 65536 (before any parse); the record exists and reads; it holds no certificate
  yet (attach once); the bytes are exactly one DER certificate (the loader's output equals the input byte for byte,
  and the bytes outside the issuer's signature have their one DER shape); it carries the stored public key; the wall
  clock lies inside its window; it chains to a configured issuer (`X509Chain`, custom root of exactly the configured
  issuers, no revocation check, no download, every status flag clear, at least two elements). **With no issuer
  configured every certificate is refused.** Attaches of one instance run one at a time.
- **`DeleteRegistration`** is the store's delete of the record.
- **`CloudDeviceTokenHolder`**: one device token per registration, in memory only, handed out as copies; renewed only
  through `ICloudDeviceTokenIssuer` (the real issuer is later work; the tests use a fake) at 90% of its stated
  lifetime on the MONOTONIC clock, or after `Invalidate(id, refused)` with a copy of the token still held; one issuer
  call per registration at a time, bounded by 30 seconds; an answer held only when it is valid. The type names carry
  the prefix `Cloud` so they do not collide with the OXPd adapter's `DeviceTokenHolder`.
- Every failure is a `RegistrationException` with one of thirteen reasons and a fixed message (no inner exception,
  never a key, certificate, token, id or store name).

## The fix commit

The first head read red on the hosted Linux leg only, in ONE test (C01, every byte of a good certificate changed in
turn): OpenSSL loaded a certificate with a changed validity date and threw only when the date was read, so a
platform exception left `AttachCertificate`. `94fe6067` reads the public key and both dates inside the parse rule
(such bytes are now refused as malformed) and treats any failure of the chain build as not trusted. No test changed;
the second head is green on all four jobs. Nothing that was refused before is accepted now.

## What does not change

No package, no solution line, no workflow, no build script. The library gains one project reference, to the secret
store; the restore rewrote four lock files (this library's, its tests', and the two of the Jobs projects, which
reference this library) by project entries only, every package row unchanged. The server references none of this, so
the published output is unchanged.

## Limits, stated plainly

- The private key is in clear in the server's memory during `CreateRegistration` and the calls that read the record
  (in buffers cleared after use and in the platform's key object until disposed). No non-exportable key provider
  (Key Vault, HSM or TPM) yet.
- Which certificate signs the real device certificates is UNMEASURED: until a later step configures it, every real
  certificate is refused. Whether the service accepts this signing request from a server is UNMEASURED.
- The certificate's window is read on the wall clock (a clock set back can pass an expired certificate). A leaf that
  marks itself a certificate authority, or names any extended key usage, is not refused by any rule here (the real
  certificate's extensions are UNMEASURED).
- One process per store partition, and attaches are serialised within one instance only. A removal is not
  serialised with an attach of the same instance: a removal that lands while an attach is writing leaves the record
  written again (recorded for the work that adds the removal flow).
- An issuer whose call blocks before it returns its task is not bounded by the 30 seconds (the bound starts on the
  returned task). The device token is lost at a restart.
- The host does not use this library yet.

## Who decides

Every choice inside this change (the record, the certificate rules and their order, the issuer rule, the token's
renewal point and bounds, the names) is the coordinator's, made as coordinator, never the product owner's. The open
questions the design leaves (whose app registration is used; the real issuer; where the token lives across a
restart; the store partition the host gives) stay open.

54 new tests (1524 -> 1578 locally and on both hosted legs; skipped 4 on linux and 19 on windows, as before; RULES 500
files). Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
