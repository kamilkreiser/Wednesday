---
date: 2026-08-05
type: principle
source: "Kam, 2026-08-05 (responding to my gh-identity 'cleanup queue' flag): 'i will switch between accounts and jobs. this will happen. tell me if you need me to auth but 1)critical not to get the job / client wrong 2)to make things as portable as possible'"
status: live
supersedes: ""
---

# Identities float by design — verify at point of use, never propose "cleanup"

**The lesson:** Kam deliberately switches accounts and jobs on every machine —
global identity state (gh CLI, az CLI, browser Google/Microsoft/GitHub
sessions, u/N account slots) is a FLOATING POINTER, not a fixed configuration.
Today's proof: the Studio's global gh was kksecura while the laptop's is
kamilDatasec — neither is "wrong"; both are snapshots of whatever Kam did
last. Framing this as a "cleanup queue" was the wrong model.

**The two hard requirements he set:**
1. **CRITICAL: never get the job/client wrong.** The burden of identity
   correctness is on the AGENT at the moment of action, never on the
   machine's state or on Kam keeping things tidy.
2. **Maximum portability.** Nothing may depend on a machine being in a
   particular identity state; everything that can live on-drive does.

**How to apply:**
1. **Verify identity at point of use, EVERY time** — `gh auth status`,
   `az account show`, the account avatar/email on any web page — before any
   client-scoped action, even seconds after a previous check, even when
   memory says what it should be. Never infer from machine, history, or
   what was true this morning.
2. **Wrong identity present → ABORT + ask.** Never borrow an adjacent
   identity because it's logged in ("kamilDatasec can probably read this
   Secuura repo" = severity-max thinking). Tell Kam exactly WHAT to auth
   and WHERE: "I need the kksecura identity in Chrome for the Secuura org
   packages page" — he switches, I proceed.
3. **Prefer structurally-isolated state over global state:** per-project
   AZURE_CONFIG_DIR / GH_CONFIG_DIR (the launcher pattern), on-drive
   credentials in 4_Credentials/, secret files with 0600. Global state is
   for Kam's hands, not agents'.
4. **Portability bias in every build:** tools compiled on-drive, tokens
   on-drive, machine-local grants (TCC etc.) minimized, and whatever is
   unavoidably machine-local goes on PORTABILITY.md + doctor.sh the same
   session it appears.
5. In briefs to other agents: carry this rule — their wrap culture already
   refuses wrong identities (VSP agent precedent, 08-04); keep rewarding
   refusal over convenience.

**Related:** [[2026-08-03_mental-model-not-source-of-truth]] (identity is
the sharpest case of model-vs-reality), [[2026-07-31_fully-portable-drive]],
[[../people/kam.md]]
