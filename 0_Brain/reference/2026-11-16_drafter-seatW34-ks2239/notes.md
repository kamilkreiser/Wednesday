# Drafter notes: Seat W 34th, KS-2239 (2026-11-16 16:44 to 16:55 AEDT, Opus)
- Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatW34_ks2239.md (about 39.7 KB; STAMP blank; SELF-CHECK 16:54 after the re-read).
- W-1 (the lead): issuer.did is NOT the chain's actorDid/orgDid. Its source is certification_metadata.issuerDid, written from cert.issuer.did, which is getUserFromRequest(req).did, which is req.user.did. No mint carries a did claim (auth jwt.ts: 0 did keys; control userId 4; did-key census 0 in auth, gateway and middleware, controls 110/36/5/5). The legacy fallback, documents.metadata.issuerDid, is caller-typed document data. actorDid/orgDid come from S's body.identity via anchorIdentityFields and are anchored by anchoring. Nothing links the two. What IS anchored from this route's write side is issuer.id, as issuerOrgId (certifications.ts 667 → anchorSchema.ts 359). Recommendation A (withhold from non-parties); Wednesday can rule it at the stamp.
- W-2: "owner" = callerMayReadCertification (platform admin, issuer, holder = owner_user_id, issuing connector). It is the rule GET /:id uses to return the full issuer, so no new disclosure. W-3 default: ORG_ADMIN not a party.
- Develop moved during the draft: e5a6eb82c607 (16:45) → eb27110fc6e4 (PR 2124, 2 script files, 0 originate). Read at 16:49.
- Overlap: certifications.ts = PR 2160 only (hunk @@ -932, issue catch); merge-tree NOT run by me. PR 2162 (B 195th) 0 originate.
- Forced cell: ks1699v V-C7 (its VERIFIER is a non-party). V1 in ks1699-share-and-recertify asserts no issuer and stays green.
- Billing: the charge line is untouched; X-C5 and m-X6 pin it.
- Ordinal W 34th 0 (controls W 33rd 1, W 32nd 1). Branch ks-2239 free (0 of 1,540; control 1). Push queue empty.
- Corrections to the board: gate 375's Q1 table gives issuer.did's MEANING, not a measured VALUE. Candidate for Kam: the user id is anchored on chain as issuerOrgId.
- Not done: no suite, merge-tree or cockpit run (forbidden or out of scope); no DB read.
Scratch: _work/ (source copies at e5a6eb82/eb27110, pr_files.tsv, branches.txt, tree.txt, grep outputs, lin_read.py + lin_ks2239.json; no secret in any file).
