---
client: Datasec
project: CypherKey
path: /Volumes/DevMASTER/!CODING/Datasec/CypherKey
status: active
updated: 2026-08-02
---

# Datasec / CypherKey (OneTimePad)

**Last session (2026-08-02):** Four tickets closed. Shipped ADR-0013 HSM-keyed
expected-response digests (CPKEY-155 — closes the DB-breach enumeration finding F1,
deployment-gated, SoftHSM live-verified, 711/711 tests) and digest-pinned ACA deploys
with a single-app roll mode (CPKEY-160, live-verified). Closed CPKEY-95 (compose
staleness — cannot reproduce, canary documented) and CPKEY-101 (legacy native-app gap
pass finally ran with the backups mounted → four follow-up tickets filed).

**Open / next:**
- Kam decisions: enable keyed digests on the demo (`OTP_ERD_ROOT_KEY`, permanent once
  set) · Android app-lock fail-open posture (CPKEY-163) · Twilio token rotation ·
  `gh auth login` · start CPKEY-93 (store publishing)?
- Build queue: CPKEY-161 (iOS activation countdown + expiry messaging), CPKEY-162
  (top-up ceremony — the low-watermark warning is currently a dead end), CPKEY-163/164
  (platform parity passes), then CPKEY-157/156 (attestation, PQC).

**Blockers:** none hard; several items wait on Kam's decisions above.

**Notes for Wednesday:** jira-cli write ops (create/comment) hang on this machine —
REST recipe in the project's JIRA.md. Demo env runs unkeyed digests until Kam opts in.
