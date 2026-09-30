# ANSWER (Seat B 49th): plan CONFIRMED; the six advisories go FIRST as ITEM A, an in-range lock refresh measured then raised as ONE PR, Refs KS-1378; no acceptance. ctx:30% at 2026-09-30 13:45

## BLUF
**Your ctx: ctx:30%** (Wednesday's read of pane %81, 2026-09-30 13:45 AEST). **Continue.**
**Plan CONFIRMED** as you wrote it, with one addition that **SUPERSEDES the queue order of your brief and of ADDENDUM 1: A → 1a → 1c → 2 → 3 → (4, 5).** Q1 (rebase `-b47-1`, existing name), Q2, Q3 (`Refs KS-729` for ITEM 2), Q4, Q5: all adopted as you stated them.
**ITEM A (Wednesday's route for §1: your (a) then (b); NOT (c), NOT (d)):**
1. **MEASURE** in scratch worktrees at `3e3a68260d0e`: an in-range lock refresh (`npm update <pkg> --package-lock-only --ignore-scripts`, per lock, B 48th finding 2) that moves `brace-expansion` and `fast-uri` to patched versions (and `ip-address` 10.7.0 → a patched 10.x in `services/mcp-server`, if an in-range one exists), in every lock legs 6/7 read, with the PRISTINE CONTROL beside every root-lock regen (B 48th finding 3). Compare bytes, never the `up to date` banner (finding 1).
2. **If ALL SIX clear by in-range refreshes and legs 6 + 7 + contract read 0/0/0 with NO baseline row:** raise ONE PR, `Refs KS-1378` (In Progress; "Five new advisories block EVERY push" is exactly this class; KS 729 de-hyphenated in the body for the ip-address pair), locks only (no manifest change unless a range forces it: then say which and why). **Before the READY, measure** the images whose locks move (root, `services/mcp-server`, `services/nft-certificate` at least: `docker compose -p b49probe build <svc>`, build only, the served tree's resolved versions read, never `up`/`prune`), and those services' suites before/after. **T1** (production entries in shipped images). Push under lock-45; legs 6/7 run in the hook; quote them.
3. **STOP and mail Wednesday instead of raising if:** any of the six clears only by a MAJOR, only by touching `mobile/secuura-app` (KS 769's scope, not yours), only by a baseline row, or the refresh moves anything in a shipped tree beyond the named packages and the 12-entry drift the control attributes. **An acceptance of a production-reaching advisory is Kam's** (the 09-09 grant's exception fires on production entries), so that would become a card, not your call and not mine.
**Authority:** an ordinary gated change under v1.3 (the same footing gate48a's N-1354-8 gave the js-yaml bump), in the direction Kam ruled on 09-29's advisory card (a, bump) and on 09-30 ("And fix now"). **The 09-09 baseline grant is NOT used.**
**Parallel local work is allowed:** while ITEM A's builds or suites run in the background, you may do ITEM 1a's LOCAL proof (rebase, `cmp`, exec bit, red-first on both runners, commit) in `s-b49-ks1054`, because its files are disjoint from every lock. **Push nothing but ITEM A until ITEM A has merged** (every other push would be refused by the hook anyway).
**gate49:** ITEM A's READY goes to its own quick gate FIRST (it unblocks the fleet), the rest batch after. Wednesday names the GO strings.

## ON YOUR FINDINGS
- **Leg 7's empty CLEANUP by construction** (`audit-locks.mjs:298`, 0 of 26 rows carry `scope`): accepted. The rule in the brief was unsatisfiable as written; your probe copy (its reported map, deleted after, 0 files left) is the right instrument. `{mwp4}` confirmed. **ITEM 2 stays blocked behind ITEM A, as you said.**
- **The re-key with no bare "44" and no seat-token rule, plus the three default-seat literals made REQUIRED:** KEEP all of it. The unproven `B49_WRAP` guard is honest as stated; prove it at the first real GO.
- **ADDENDUM 1 reached you only by counting the inbox:** correct, and that is Wednesday's gap. The ADDENDUM went mail-only without a pointer tap because you were booting. From now on every mail to you gets a verified pointer tap unless your pane shows you mid-turn at the moment of sending.
- **The F-02 preflight line:** the same standing as B 48th, whose pushes worked through the repo-local `core.sshCommand`. Prove the push with `ls-remote` after it, as the brief says.
- **The KS-1387 comment count moved:** noted. It is not yours; say nothing about it on the ticket.
- **ctx:10% read off your own pane:** disclosed and harmless; Wednesday's reading governs.

PROVENANCE:
- your ctx | `tmux capture-pane -p -t %81` statusline ctx:30% | read 2026-09-30 13:45
- the six advisories, legs 6/7 rc 1 at develop 3e3a68260d0e, contract rc 0, the prod census, the in-range patched versions already present in services/originate and services/anchoring | your plan-confirmation mail (03:45:00Z), read in full; not re-derived by Wednesday | read 2026-09-30 13:45
- Kam's direction: bump | card secuura-five-new-advisories-block-every-push-0929 ruled a (bump), 09-29; card secuura-undici-ghsa-r53p-exception-1354 note "And fix now", 09-30 11:03:17 | the 09-29 and 09-30 notes of this seat's brain | read 2026-09-30 13:45
- the 09-09 grant's exception on production entries | learnings/2026-09-09_advisory-baseline-standing-authority.md, as quoted in gate48a's NO GO | read 2026-09-30 13:45
