Seat C 44th

ANSWER: chain-first issuerName from legacy anchors (Seat C 44th). RULED: (b). On the three chain-first answers (v1 verify-file, v1 by hash, v2 chainOnlyMatch): issuer null, certifiedBy null, and onChainMetadata.issuerName null, ALWAYS. This SUPERSEDES the chain-first half of the stamp's C44-R1 ("@"-free chain issuerName shown); Rule R for row-backed answers is unchanged.

WHY: Kam's 11:12 ruling opens names and keeps personal data out. On a chain-first path there is no row, so nothing can tell a company string from an email local part, and by your reading every chain issuerName that exists predates KS-240 (2026-07-30) and was written by the certify route from the email local part. Where the two cannot be told apart, the answer withholds. Since KS-240 the name is not anchored at all, so (b) withholds almost nothing a company would have shown.

READY MUST SHOW: the 3 to 6 cells you named (a legacy-shape anchor carrying a local part answers null on all three paths and in onChainMetadata; a row-backed answer still shows the company name by Rule R), each red on a mutant that restores the "@"-filter; and one sentence in the PR body: "chain-first answers no longer show an issuer name: an anchor cannot tell a company name from an email-derived one (pre-KS-240 anchors carry the certifier's local part)". UNMEASURED stays UNMEASURED: whether any such anchor exists on preview; say so.

Wednesday will put this in the post-merge receipt to Kam as a client-visible change (chain-only verify answers carry no issuer name).

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-16 11:12:46 (live board, verbatim): "Decision secuura-verify-names-personal-data-1116: a — Open the names, but not personal data".
- Kam 2026-11-16 07:03 (live board, verbatim): "new rule for all related tasks and tickets. Audit records and verification can be read by anyone in the world. writing can only be done by the creator and other uses expressly allowed in the smart contract".
