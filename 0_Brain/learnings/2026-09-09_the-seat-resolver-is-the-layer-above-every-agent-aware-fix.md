---
name: the-seat-resolver-is-the-layer-above-every-agent-aware-fix
date: 2026-09-09
type: correction
source: Tuesday s2 — booted with the wrong seat identity by the launcher's own hostname default, one day after the same class was fixed one layer down
status: live
tier: W
---

# Parameterising the JOBS does not help if the thing that decides WHICH SEAT is still guessing — fix the resolver, then sweep every sibling that hardcodes the answer

**The operative case, so the headline matches it:** a mechanism has just been made
agent-aware — an installer, a plist, a digest, a ledger line. **Before calling the class
closed, ask what decides `WED_AGENT` in the first place, and then grep every sibling file
for the literal `wednesday`.** A parameterised job that receives the wrong seat name is
exactly as wrong as a hardcoded one, and it is harder to see, because the file you fixed
looks correct when you read it.

## The case, measured

On 2026-09-08 Tuesday s1 found `install_scheduler.command` arming three `com.wednesday.*`
jobs on any machine, quarantined them, and carded it. Kam ruled **`parameterise`** at
08:21. s1 built it: all four jobs agent-aware, the plists carrying `WED_AGENT` because
launchd does not inherit the environment, and two extensions beyond the ruling stated as
extensions. Good work, and the class read as closed.

**The next boot of that seat came up as WEDNESDAY, in Tuesday's tree, on Tuesday's
machine.** `Launch_Wednesday.command` was started directly rather than through
`Launch_Tuesday.command`, and its fallback resolved the seat **from the hostname**:

    Kamils-MBP*) AGENT="tuesday" ;;
    *)           AGENT="wednesday" ;;

Tuesday had moved from the laptop to `Kamils-Mac-mini` **that same morning**, so the map
was wrong in **both** directions at once: the mini fell through to `wednesday`, and the MBP
still claimed `tuesday`. The seat was handed Wednesday's identity, Wednesday's Secuura
scope, an instruction to read Wednesday's 548 KB `_ledger.md`, Wednesday's AgentMail inbox,
and a statusline reading `[Wednesday]` — while Wednesday was genuinely live on the Studio,
against Kam's own "one Wednesday at a time" practice.

**Three surfaces carried the wrong seat and none of them disagreed with each other**, which
is why nothing in the boot could have caught it by internal consistency. What caught it was
the tree: `Launch_Tuesday.command`, `NEXT-PICKUP-TUESDAY.md`, the history entry and Kam's
verbatim scope ruling all say Tuesday, and the launcher said Wednesday.

**And the class was NOT confined to the launcher.** Sweeping the siblings the same session:
`inbox_digest.sh` keys correctly on `WED_AGENT`; **`wake_watch.sh` hardcodes
`wednesday-agent@agentmail.to` on line 54 and the pane name `wednesday` on line 46.** So on
a correctly-booted Tuesday the mail tripwire polls **Wednesday's** inbox, fires wakes at
Tuesday about another client's mail, and — because it filters out `wednesday-agent@` as
"own outbound" — **suppresses exactly the cross-seat mail from Wednesday that Tuesday most
needs.** One instance fired live during this session before it was measured.

## Why the 09-08 fix did not prevent this (the diagnosis w=2 owes)

**The ruling was applied to the things the card NAMED, and the card named jobs.** `parameterise`
was read as "make the installer and doctor agent-aware", which is precisely what it said. Nobody
asked the next question up: *and where does `WED_AGENT` come from?* The launcher's own comment
even records the answer honestly — *"the hostname map below is only the DEFAULT... deliberately
not the authority"* — and a default that is documented as untrustworthy is still the value that
gets used.

**The general shape: a resolver is invisible because every consumer of it looks correct.** Each
parameterised file reads as fixed. The defect lives one layer up, in the single place that
answers the question all of them ask.

## How to apply

1. **When a mechanism is made agent-, tenant-, client- or environment-aware, fix the RESOLVER in
   the same action** — the code that decides which value the parameter takes. A parameter with a
   guessed argument is not parameterised, it is indirected.
2. **Then grep the siblings for the literal you just replaced.** `grep -rn 'wednesday' 2_Project_Files/`
   is one command and it is what surfaced `wake_watch.sh`. A class is closed when the sweep is
   empty, not when the reported instance is fixed.
3. **Prefer a discriminator that is LOCAL to the thing being identified.** The two trees are clones
   of one repo, so every tracked file is identical in both and cannot discriminate; the checkout
   path is the only thing that differs, which is why the folder name is the right key and the
   hostname is not. Ask: *what property is true of this seat and could not be true of the other?*
4. **A guess-by-default must become a REFUSAL.** Kam's own words in `Launch_Tuesday.command`:
   *"a seat that guesses its own client is precisely the failure the two-agent split exists to
   prevent."* The fixed resolver reads the tree, falls back to the hostname, and then **exits 2 with
   the two one-line fixes named** rather than picking a seat.
5. **A machine move invalidates every hostname map on the drive, silently and on the same day.**
   When a seat changes machines, that is the trigger to sweep for hostname keys — they are the
   travel-pointer defect pointed at identity instead of at paths.

**Family:** [[2026-09-08_a-ruling-can-be-voided-by-removing-its-precondition]] (the machine move
removed the map's precondition) · [[2026-09-07_a-census-complete-over-a-frame-that-is-not]] (the
09-08 sweep was complete over JOBS and silent about the RESOLVER) ·
[[2026-08-25_travel-drive-stale-pointers]] (a stored absolute wakes up on the wrong volume; a
stored hostname wakes up as the wrong agent) · [[2026-08-13_shared-bus-tag-filter-or-leak]] (the
`wake_watch` half is R0 at the comms layer) · [[2026-08-05_identities-float-verify-always]] ·
[[2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit]] (the ruling was read for what it
scoped, correctly — and the layer above it was nobody's).
