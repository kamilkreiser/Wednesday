## BLUF
Kam ruled KS-1695 gap 2 (documents with no recorded owner) as **option b**. Merge #1667 first (separate GO mail, same minute). Gap 2 is a NEW tier-1 build and is sequenced behind #1654; do not start it before you have read this whole mail.

## Kam's ruling, verbatim (live board, 14:00 AEDT 2026-10-20, card `secuura-ks1695-ownerless-records-who-reads-1020`, recorded on the card by Wednesday at 15:02 with `reconcile_rulings.py --apply`)
> Decision secuura-ks1695-ownerless-records-who-reads-1020: b - Platform S's connectors and platform administrators only

The card's own text for (b): only the connector that created a record, plus platform administrators, can open owner-less records; no person in the tenant can, administrators included, unless they are platform administrators. Records with no creation record (older bare ones, and S records created with no person attached) become unreadable to S too. The card states S's new versions need PR 1654 first.

## What Wednesday reads that to mean (Wednesday's reading; correct it if the code says otherwise)
1. Gap 2 is built as option (b), AFTER #1654 (seat E's migration 055 round 3, at the gate now or next) is merged to develop. Before it, take the counts the card said were not yet taken: how many owner-less records sit on demo and kintsugi, and how many have no creation record. Report them in your PLAN; they decide whether (b) strands anything.
2. Tier 1 (security read path). One build, one Opus gate at most before merge; the two-round cap applies to the class.
3. Nothing in this mail changes #1667; gap 1 ships as gated.

## Provenance
- The card text above: `decision_queue.sh show secuura-ks1695-ownerless-records-who-reads-1020`, read at 15:02 in the same action as the ruling; status ruled, choice b.
- Kam's tap line: `kam_rulings_today.sh` row at 14:00.
- "#1654 first": the card's own sentence, not re-derived by Wednesday from the code.

## Ask back
Your PLAN for gap 2 (files, the counts, how the creating-connector check reads the creation record) before you build. Send it as a QUESTION; Wednesday answers within the usual window.
