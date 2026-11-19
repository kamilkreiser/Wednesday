# SWEEP-1630 — Tuesday's answers (s293, 2026-11-19). Decisions are Tuesday's under the 11-06 backlog grant; none is Kam's.

Read by Tuesday: the sweep's REPLY (saved below, condensed) and, at source, MPS CLARIFICATIONS.md C-108 (heading line 2707:
the product owner's 2026-11-11 acceptance of four wording calls; MPSCALC-195 and 316 "not moved (LATER)"). The sweep
DOCUMENT itself was NOT read whole by Tuesday yet. HPSM-POC was excluded from the sweep by commission (Kam's hold to
2026-12-10).

## The sweep's result (its own figures, not re-measured by Tuesday)
10 buildable keys (7 NexusAI, 2 MPS, 1 Composer conditional), 10 candidate decisions.
Lanes: N-K (RD-1011 + RD-1013 + RD-1012; server.js, capabilities.js, role inventory, accessAudit.js, entraProvisioning.js;
G1), N-L (RD-349 + RD-175; two CSS files; G2), N-M (RD-1008; server.js + static/js/index.js; after N-F; G2 + CodeQL),
N-O spare (RD-759; cspReport.js; G2), M-G (MPSCALC-195 + 316; accepted wording; G2). Composer: 0 firm (PCOMP-44 conditional).
To be ticketed: AUDIT_ACTIONS.SETTINGS_CHANGE used at server.js 17353 and 17600, defined nowhere.
Blocking classes: MPS 162 open = buildable 2, landed 46, words 35, unread or seed 23, umbrella or answered 21, deploy 11,
ruling 11, planned build 8, outside data 4, client 1. Composer 78 = hold 24, behind an unbuilt predecessor 17, umbrella
or superseded 9, ruling 7, deploy 6, words 5, landed 4, client 3, other 2, conditional 1. NexusAI top 60 = ruling 23,
design or measurement first 9, buildable 5, words 5, landed 4, in flight 3, hold 3, deploy 3, outside 2, other 2, stale 1
(819 further open NexusAI tickets unclassified).
Candidate decisions (ranked by tickets freed): MPS words pack for the v13.4.1 lanes (35); MPS hosted deploy + the seed
identity's expired secret (11); Composer reviewer-round hold (13, with 17 behind); Composer Guided hold (10); MPS question
sheet (11); NexusAI CodeQL baseline disposition (5); NexusAI roles-UI word pack B and C; and smaller ones in the document.
Built on main while the ticket reads open: RD-532, RD-577, PCOMP-52. Answered but open: MPSCALC-120, 78, 85, 188, RD-810.

## Answers
1. QuoteEndpoints.cs error string: text a user can see. In lane M-G ONLY if the accepted C-64 sentence fits byte for byte
   (C-108: "in the remaining places"); any other wording = not edited, listed, a words question. (In commission B1741.)
2. Order: N-K BEFORE RD-929. N-K is a spelled-out administrator check on four routes a viewer can reach today (Medium,
   security); RD-929 is design-sized and is drafted against the main N-K lands on. NexusAI serial queue now:
   N-F (building) -> N-J (B1739, drafted) -> N-K -> N-M -> N-L -> N-O; RD-929 drafting after N-K.
3. PCOMP-44: NOT started. Tuesday has not read it; the Composer sits under two holds with no end named. Read it at the
   next checkpoint; until then the default is no lane.
4. "Needs a ruling" rows: any whose ticket says the ruling is Tuesday's (RD-633 "until Tuesday rules") are Tuesday's to
   rule under the grant after reading the ticket; OWED: go through the 23 NexusAI rows and rule or card each.
5. RD-1011: refuse all four routes (the ticket's proposal) as Tuesday's default, said as a default in the kit, the PR
   text and the ticket; the ticket's own question to the product owner (must the two reads stay open to a viewer?)
   stays visible on the ticket and the change is one line per route to reverse.
6. Records pass for the tickets built on main but still open (MPS 46, Composer 4, NexusAI 4 by the sweep's reading):
   YES, one records seat per project, each ticket verified at source before any comment or move, a ticket a client human
   opened left for them to close. MPS first, AFTER lane M-G is drafted (same board). Not HPSM.
7. RD-300 and RD-564 (Declined, counted open): left as they are; a note for the next NexusAI records pass.

## Cards for Kam (NOT yet posted)
Each candidate decision becomes a card only after Tuesday reads its section of the sweep document and runs
`decision_queue.sh prior` on its subject (he may have ruled it; a hold he set is his to lift). One card per decision,
a default on each. Order: the MPS words pack, the MPS hosted deploy and seed secret, the two Composer holds, the MPS
question sheet.
