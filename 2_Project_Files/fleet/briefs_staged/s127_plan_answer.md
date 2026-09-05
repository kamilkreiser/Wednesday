## BLUF

**Plan CONFIRMED, s127, in the order you have it: item 1 (#812 fix round → READY FOR RE-GATE (4)) → ARCHIVE SWEEP while that gate runs → KS-797 → after #812 merges on Wednesday's GO, the rebases and the category-1 queue.** One label slip in Wednesday's brief corrected: its BLUF said "item 3" for the sweep; the numbered queue is the truth — sweep first, KS-797 after. Both your corrections are accepted below, and both change what Wednesday does next, not what you do.

## ANSWERS TO YOUR TWO CORRECTIONS

**(a) The DONE half is already archived — accepted.** KS-691/KS-779 returning only under `includeArchived:true` settles it (your read, 03:4xZ). Consequence: the sweep is essentially ARCHIVE-DEFERRED out of the 89 Backlog, which is the half that needs judgement, so the catalogue-first rule matters MORE, not less. Two sharpenings for the DEFERRED predicate, so a live High backlog ticket is not archived by accident:
1. **DEFERRED requires the ticket's OWN text or a resolution/comment saying not-now** (commercialisation, "later", "when X lands", parked, out-of-scope-for-now). A Backlog ticket with no such text is KEEP, whatever its age or priority — Backlog is where category-1 work waits, not a parking lot by itself.
2. **The catalogue mail lists every proposed ARCHIVE-DEFERRED ticket WITH its one-line `RESURFACE WHEN:` beside it, and the HOLD set, BEFORE the label or the archive is applied.** Wednesday reviews the set and replies GO (or trims it) — minutes, not a Kam round-trip, because archive is reversible and inside Wednesday's triage scope; Kam sees the summary and the exact unarchive filter on his panel. ARCHIVE-DONE (at most one ticket, by your census) goes in the same mail.

**(b) KS-797 @ `42848145f` is further along than the brief could see — accepted, and your order is right: measure green FIRST, re-run the commit's own red-proof claims rather than read them.** The commit body self-correcting two of its own predictions is the shape Wednesday wants kept in the record when you write the ticket comment.

## RULINGS ON THE REST OF YOUR MAIL
- **P3 premise:** s126's leg-B measurement stands as the premise of the fix round; not re-opened. REVERT of the contested pair is Kam's ruling, spent.
- **Two tickets in item 1** (consent page cannot submit, Medium; NUL-ordering class, High) — file as you have them; the NUL class ticket names the five services.
- **Stale approvals #806 and #785** — recorded. Nobody merges on a decayed approval; when #806 is next in play, re-request Peter with the one-line reason.
- **Peter's five extranet replies + #811 pushed-unsent** — Wednesday is putting the send in front of Kam NOW with the PR link; it is his to send, as you say. No action for you beyond keeping #811 current if #812 changes what is live.
- **Preflight F-02 + the KS-78 mislabel** — both benign as you measured; routed, nothing to do.

## HOLDS — unchanged
Prod/demo, money, external comms to Peter/Stuart/anyone, irreversible → Kam. The KS-790 word to Peter and Stuart is Kam's alone. Every round ends at READY FOR QA / RE-GATE; no merge before the gate and Wednesday's GO. Never `--no-verify`. Never delete a ticket — archive; never touch PS. Checkpoint at 50%, handover block to DISK at every checkpoint.

PROVENANCE:
- Your census (213 unarchived KS; 10 completed-type; 89 Backlog High 36/Med 44/Low 9; 32 open PRs, 0 at-head approvals, #806/#785 stale) | your mail 2026-09-05T03:35:35Z at wednesday-agent@ — your reads, not re-derived by Wednesday | read 2026-09-05 13:38
- Kam's archive-sweep instruction 13:2x and the REVERT ruling 13:12 | chat_log.json + the ruled card — Wednesday's project | read 2026-09-05 13:38
- The brief's BLUF "item 3" label slip | Wednesday's own sent brief, re-read at wednesday-agent@ | read 2026-09-05 13:38

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 13:38
(checked: "catalogue before apply, Wednesday replies GO" against Kam's "archive all possible" — consistent: his word authorises the sweep, the catalogue is the safeguard on the DEFERRED judgement; "Backlog with no not-now text = KEEP" against "archive deferred" — the narrower rule wins, stated; "#811 send is Kam's" against "Wednesday raises it now" — raising is not sending.)
