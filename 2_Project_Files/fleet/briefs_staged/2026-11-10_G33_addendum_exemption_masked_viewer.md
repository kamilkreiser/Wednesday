Seat G 33rd

ADDENDUM: the exemption form is RULED: option a, masked viewer, no raw reads (Seat G 33rd). This is the exemption ADDENDUM that item 2 of my 08:0x ADDENDUM ('push the always-blocked half now') told you to hold for. It does not change round 1.

KAM'S RULING, verbatim from his live board (09:03:23 AEDT, view=wednesday; recorded on card secuura-ks1785-exemption-premise-moved-1110 as choice 'a', ruled_ts 2026-11-10T09:03:58+11:00):
"Decision secuura-ks1785-exemption-premise-moved-1110: a — Match platform-s: masked viewer, no raw reads"
What option a means, per its detail line (read by Wednesday with decision_queue.sh show at 09:04): the localhost-only systemTest env files become readable only through a masked viewer, every password, key and secret is masked in tool output, and raw reads are refused; the same rule as platform-s and Stuart's 28 Oct ruling.

WHAT ROUND 2 IS:
1. The guard refuses RAW reads of the localhost-only systemTest env files (no raw-localhost exemption: option b was not chosen).
2. Those files are readable only through a masked viewer that masks every password, key and secret in tool output. Platform-s calls its viewer show_env_masked.py; build yours from the specs, as my platform-s route ANSWER said (copy CLASSES and NAMES; no platform-s code was read, and your PR body says so).
3. The three systemTest .env.example comments you held back from round 1 now get their wording for this form.
4. Red-first and your own mutants, as for round 1: a raw read of a localhost-only file refused; the viewer's output carries no secret value (fake fixtures only); a mutant that lets one raw read through, and one that unmasks one value class, each reddens a named cell.

METHOD: round 2 is a NEW commit on the same branch (never a force push, never a rebase). Census before the push, then an exact-name QUESTION if anything overlaps, then the push, then READY FOR GATE, TIER 1, round 2, naming this ADDENDUM. A tier-1 Opus compare gate follows. If round 1 is still in your push queue or at its gate, finish that first; round 2 starts after the round-1 READY is sent.

If this form needs a design choice the card does not make, STOP and QUESTION it. Do not choose.

Wednesday
