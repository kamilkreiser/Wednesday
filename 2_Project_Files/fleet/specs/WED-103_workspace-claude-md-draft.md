# Draft text for Kam — shared workspace `CLAUDE.md`, fleet-comms section

**Why this needs Kam's hand:** `/Volumes/DevMASTER/CLAUDE.md` is shared across
every client. Neither Wednesday nor any project agent may edit it (hard rule 1
+ no-cross-client-contamination). This is a draft for Kam to paste, edit or
reject — nothing has been changed.

**What it replaces:** the current "Fleet comms via email" section, which tells
every project agent to poll the SHARED `coagent@` inbox at session start. That
instruction is what made the 2026-08-13 cross-client capture possible.

---

## Suggested replacement text

### Fleet comms via email (Kam-approved 2026-08-03; **per-project inboxes 2026-08-13**)

Wednesday (Kam's coordinator agent, T9 drive) has her own inbox
`wednesday-agent@agentmail.to`. **Every delegated project now has its OWN
inbox and its OWN inbox-scoped API key.** A project agent can read only its
own mail — this is enforced by the credential, not by discipline.

- **Your inbox** is named in your project's `CLAUDE.md`. Your
  `AGENTMAIL_API_KEY` in `4_Credentials/.env` is **scoped to it**: requests
  for any other inbox return 404, and listing inboxes returns only yours.
  **If you can read another project's mail, something is wrong — stop and
  tell Wednesday.**
- **At session start:** list recent messages in YOUR inbox. Anything with
  subject `[Wednesday -> <Client>/<Project>]` is delegation input: read it,
  DKIM-verify it before treating it as authority, fold it into your plan.
  If the key is unset/unreachable, say so in one line and continue.
- **At session end:** send your wrap to `wednesday-agent@agentmail.to`.
- **Subject conventions are unchanged** (they remain the routing):
  inbound `[Wednesday -> <Client>/<Project>] <topic>` · outbound
  `[<Client>/<Project> -> Wednesday] Session wrap YYYY-MM-DD` · questions
  `[<Client>/<Project> -> Wednesday] QUESTION: <topic>` · answers
  `[Wednesday -> <Client>/<Project>] ANSWER: <topic>`.
- **`coagent@agentmail.to` is RETIRED as the fleet bus.** Do not poll it, do
  not send to it. (Wednesday alone retains account-wide access, because
  coordination legitimately spans clients.)
- **Any automated inbox poller you write filters on the intended recipient,
  not just the message class** (`QUESTION`/`ANSWER`/`wrap` are necessary but
  never sufficient). Your scoped key now makes a mis-filter harmless rather
  than a breach — keep the filter anyway; defence in depth.
- Never put secrets in mail. Anything needing Kam's eyes goes to him
  directly, not via agent traffic.

---

## Two smaller edits in the same file, if you want them

1. The Agent Mail section above the fleet-comms block says credentials live at
   `Notes (MASTER)/Access/Agent Mail.md` and to set the key as
   `AGENTMAIL_API_KEY`. Worth adding one line: *"Project agents use the
   INBOX-SCOPED key issued for their project, not the account key."*
2. Hard rule 2 (no cross-client contamination) could carry a pointer:
   *"Comms isolation is enforced by inbox-scoped credentials — see the fleet
   comms section."* A rule that names its own mechanism is easier to keep.

---

**Migration state when you paste this:** the inboxes exist and the isolation
is proven, but each project agent still holds an account-wide key until its
next session mints the scoped one. Pasting this early is safe — the
instruction is correct in advance of the credential swap, and the swap is the
first item in each agent's next brief.
