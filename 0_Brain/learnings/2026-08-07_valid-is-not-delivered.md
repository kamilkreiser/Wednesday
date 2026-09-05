---
date: 2026-08-07
type: correction
source: "Self-caught: the 23:00 close bell reported 'fleet inboxes unreachable' two nights running with HTTP 403. I diagnosed it on 08-07 morning as rate limiting, on the reasoning that the key was valid and worked minutes later. It was not rate limiting. The key never reached the code — close_wednesday.sh sourced a bare-assignment .env WITHOUT `set -a`, so the bash guard passed while python's os.environ.get() returned '', and an empty Bearer token is answered with 403."
status: live
supersedes: ""
tier: M
---

# "The credential is valid" and "the credential reached the code" are different claims

**The failure.** Two nights of `fleet inboxes: unreachable`. On the morning of
08-07 I established, correctly, that the key was valid (a live call returned
200), that it was byte-identical to the one my session uses, and that the
launchd-env theory was wrong. From those true facts I inferred a cause —
*"a 403 with a valid key that works minutes later points at rate limiting"* —
and reported it to Kam as the likely answer. I then built exponential backoff
for it.

**The actual cause, found by reproducing the failure at 13:00 rather than
waiting for 23:00.** `4_Credentials/.env` uses **bare assignments**, no
`export`. The close script ran `source "$ENV_FILE"` with no `set -a`, which
makes the key a **shell** variable and not an **environment** variable. So:

- the bash guard `[ -n "${AGENTMAIL_API_KEY:-}" ]` **passed** — bash could see it;
- the python heredoc's `os.environ.get("AGENTMAIL_API_KEY", "")` returned `""`;
- an empty Bearer token is answered with **403**, every attempt, every night.

Deterministic, not transient. One `set -a` fixes it. Both paths then verified in
the real script: the fire path returned live inbox counts, the quiet path still
skipped outside the window.

**Why my diagnosis felt rigorous and wasn't.** Every check I ran was on the key
**at rest** — its value, its length, its equality with the working one. Not one
check asked the only question that mattered: *does the process that makes the
call actually have it?* This is [[2026-08-05_verify-the-chain-not-the-legs]]
applied to a credential rather than a file sync — I verified the source, never
the destination — and it is the same shape as
[[2026-08-06_artifact-presence-is-not-execution]]: the key's presence in `.env`
is evidence that something wrote it there, not that anything read it.

**The tell I walked past:** the script's own message. It printed
`unreachable` rather than `key unset`, because the guard that distinguishes
those two cases was checking the wrong scope. A message that cannot be wrong in
the way you assume is worth more than a message that sounds right.

**How to apply:**
1. **Verify a credential at the point of use, not at rest.** The question is
   never "is the key good?" but "does the code that fails have it?" One print of
   `len(key)` inside the failing process beats an hour of comparing values.
2. **The precise class rule** (checked across the drive, and it is narrower than
   it first looks): sourcing a bare-assignment `.env` **without `set -a`** is
   perfectly fine for same-shell expansion — `curl -H "... $KEY"` works, which is
   why `shift_change.sh` was never broken — and **breaks any child process that
   reads `os.environ` / `getenv`**. Python heredocs are the common case here.
   `doctor.sh` only greps the file and is also fine. **Not everything matching
   the pattern is broken; check how the value is consumed.**
3. **A plausible cause is not a diagnosis.** "403 with a valid key" genuinely
   does suggest rate limiting. It was still wrong, and I built a mechanism for
   it. Before shipping a fix, reproduce the failure — I could have reproduced
   this at any hour of any day and did not try for two days because the symptom
   had a time attached to it.
4. **Reproduce off-schedule.** A bug that appears at 23:00 is rarely *about*
   23:00. `WEDNESDAY_TEST_HOUR` now exists on the close ritual for exactly this,
   matching the shift-change pattern.

**Kept anyway:** the backoff was built for the wrong cause but is correct
hygiene for a network call, and it now reports 403 honestly — a deliberately
invalid key returns 403 too, so the script no longer claims to know which it is.

**Related:** [[2026-08-05_verify-the-chain-not-the-legs]],
[[2026-08-06_artifact-presence-is-not-execution]],
[[2026-08-06_never-discard-stderr]] (the stderr fix from 08-06 is what made this
findable at all — without it there was no 403 to chase), [[_ledger]]
