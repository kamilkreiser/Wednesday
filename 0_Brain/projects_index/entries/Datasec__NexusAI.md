---
client: Datasec
project: NexusAI
path: /Volumes/DevMASTER/!CODING/Datasec/NexusAI
status: active
updated: 2026-08-07
---

# Datasec / NexusAI

**Last session (2026-08-07):** Shipped RD-67+68 to the demo (revision `--0000076`, healthy,
`--0000075` kept as rollback) after holding twice for an authored approval — released on Kam's
DKIM-verified mail, not a relay. Fixed RD-71 so the repo builds from a clean clone for the first
time (previously only Kam's machine and CI could build it), untagged the three ACR proof tags with
the live image intact, and moved `JIRA.md` inside the repo so it reaches contractors. Protocol v1.3
verified and retained. End-of-session secret check turned up a pre-existing exposure nobody had
been seeing.

**Open / next:**
- RD-77 (High) — gitleaks CI gate only scans push deltas, so it has never examined pre-existing
  files and has been green since 2026-04-25 while secrets sit tracked on `main`. Triage findings
  before widening the scan, or it just goes permanently red.
- RD-55 — confirm whether the Entra ID app secret is live and rotate if so; then the history
  scrub. **Irreversible → Kam's signed mail.**
- RD-73 — `deploy.yml` still deploys to the decommissioned 4.x VM on every push. Reversible
  dev/CI config, so **yours to authorise** under v1.3.
- With Kam: RD-61 sign-off · RD-76 (Entra SSO blocks agent browser-verification) · RD-74
  (`gh auth login`) · whether to purge the dangling 141 MB ACR manifest.

**Blockers:** none for me. RD-55/RD-76/RD-74/RD-61 need Kam; RD-73 needs only your word.

**Notes for Wednesday:**
- **Under v1.3 demo deploys are now yours**, so RD-67/68-class work no longer waits on Kam. Still
  his signature here: deleting the dangling ACR manifest, the RD-55 scrub + force push, and
  anything touching the Marketplace listing.
- ⚠️ **RD-55 was understated and I corrected it.** It described the secrets as history-only;
  `SESSION_NOTES_2026-03-27.md` and `TEST_SETUP_README.md` are *tracked on `main` today*. The Log
  Analytics SP is likely dead; **the Entra ID app secret in the same table has no such basis.**
  Nothing touched — it is irreversible-class.
- The workspace-level `CLAUDE.md` v1.3 item is Kam's and already in his pack — not carried here.
