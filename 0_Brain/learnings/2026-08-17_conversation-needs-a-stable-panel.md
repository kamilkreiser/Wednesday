---
date: 2026-08-17
type: preference
source: "Kam, 2026-08-17 ~12:2x (verbatim in prompt-log): back-and-forth format is perfect, but longer discussions get buried under agent prompts/actions/updates — 'difficult for me to keep track when I'm reading a component and then it disappears down the page. Is there another way for us to keep the conversation in a different panel, and for all this to either happen in the background or on a separate panel?'"
status: live
supersedes: ""
tier: W
---

# The conversation deserves a stable panel — fleet mechanics must not scroll Kam's reading away

**The lesson:** the terminal transcript interleaves two different things: our CONVERSATION
(what Kam reads and thinks against) and my FLEET MECHANICS (mail checks, gate runs, taps,
verification output). When both share one scrolling pane, every agent event pushes the thing
he was reading off screen. The burden of a stable reading surface is mine.

**The operating pattern (adopted 2026-08-17):**
1. **The dashboard chat tile is the stable conversation surface.** Every substantive
   conversational reply to Kam is MIRRORED to `0_Brain/dashboard/data/chat_log.json` (via
   `2_Project_Files/tools/chat_reply.sh`) — short form, no fleet mechanics, links/pointers to
   documents for anything long. His messages there already reach me (watcher chat leg).
2. **Anything long becomes a document with a stable home** — the 2026-08-17 HPSM sitting-pack
   PDF is the template: BLUF-structured, delivered as a file, referenced from chat. A
   walkthrough that lives only in scrollback is not delivered.
3. **Fleet mechanics stay in the terminal** (the engine room) and in the daily note. They
   never go into the chat mirror.
4. The full fix is a built one: a two-panel dashboard view (conversation + live fleet
   activity feed) — WED ticket, delegated per the threshold rule.

## Extension, same day — CORRECTED BY KAM within minutes, and the correction is the lesson

My first remedy was to give conversation "right of way" — defer wrap-processing to lulls.
**Kam stopped it mid-edit: "I dont want to stop the backround work with other agents. I just
want to keep a stream that is easier to follow."** Then: **"what if we build a chat window?"**

**The rule as he actually set it: separate the SURFACES, never throttle the WORK.**
1. Fleet processing continues at full speed, full verbosity, in the terminal — wakes handled
   the moment they land, exactly as before. No deferral, no queuing of fleet work behind
   conversation.
2. The conversation gets its own WINDOW — a dedicated chat surface (v1: standalone page over
   `chat_log.json` on the dashboard server; the full two-panel version is WED-113, after the
   2026-08-18 meeting). Kam follows the stream there; the terminal remains the engine room
   he can glance at.
3. My mis-read worth remembering: when Kam says the stream is hard to follow, the fix he
   wants is a better SURFACE, not less THROUGHPUT. Slowing the machine to make it readable
   trades the thing he values most (everything moving) for the thing he asked me to fix
   (where he reads).

**Why this is a principle, not a convenience:** Kam's priority #2 is seamless integration —
"one great way to interact with me, and me managing things downstream." Additive, never
substitutive (Life-OS rule 1): the terminal keeps working; the chat mirror adds the stable
surface on the same underlying truth. Same family as BLUF and the ask-format: the reader's
attention is the scarce resource, and the reader must never have to reconstruct or re-find.

**Related:** [[2026-08-06_bluf-write-for-the-reader]],
[[2026-08-05_life-os-commission-principles]],
[[2026-08-03_role-beyond-code-three-priorities]], [[../people/kam]]
