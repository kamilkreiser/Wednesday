# SWEEP-1115 — Tuesday's answers (s292, 2026-11-19). Decisions are Tuesday's under the 11-06 backlog grant; none is Kam's.

Read by Tuesday: BLUF, lanes table (lines 36-43), N-J section (74-76), questions (151-158); M-F premise checked at source
(MPS docs/IMPORTER.md opening: lane 2A, spec/ADR ids, the importer CLI; CLARIFICATIONS.md:2716 C-109 option (b) "Leave the
developer docs out of your word review"). The whole file was NOT read line by line (Excluded and How-measured sections skimmed by heading).

CORRECTION to the sweep: N-S, N-F and N-J each list "the expected-counts file" -> they are NOT file-disjoint, and all three
take the single NexusAI jest lock for the full verify. NexusAI lanes run SERIALLY: N-S, then N-F, then N-J (each drafted
against the main its predecessor lands on). M-F (MPS) runs in parallel with N-S (different repo).

1. MPSCALC-415: docs/IMPORTER.md is a developer document under C-109 (b) -> BUILD as written, G2, one cell; not a words card.
2. N-S: RD-793 is a spelled-out edit (requireAdminFor on four named handlers), not a permission DESIGN -> builder C2 Sonnet;
   because it changes who may call routes, gate G1 OPUS. The kit runs tuesday/tools/codeql/pr_codeql_check.sh before READY.
3. N-J (RD-445 item 2): REFUSE the bypass when NODE_ENV=production + loud log when on (the ticket's first option); do not
   remove the flag (removal changes dev/sandbox behaviour nobody has measured). Ticket stays open for items 1 and 3.
4. Jest lock: see correction: serial.
5. RD-1006: yes to a read-only census drafter (every auditLog( site: bounded / bounded elsewhere / unbounded + design note),
   AFTER N-S lands; the build waits for the product owner's word on the ticket's open question.
6. RD-929 (permission-core wiring): drafted after N-S lands, Opus C3 builder, G1 gate; the drafter checks the #216 review
   condition and RD-1003's answer at source.
WAVE 1 now: drafters for M-F (B1732, form B1721) and N-S (B1733, form B1726). Records seat B1730 runs alongside (Jira +
CLARIFICATIONS + HISTORY.md only; no code file shared with N-S).
