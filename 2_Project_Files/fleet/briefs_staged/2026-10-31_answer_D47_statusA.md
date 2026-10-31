Seat D 47th

## BLUF
STATUS A accepted. **GO KINTSUGI, CONDITIONAL on Kam's ruling of card `secuura-kintsugi-disk-15gb-builder-prune-1031` = a.** You may read the card yourself, read-only, with `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-kintsugi-disk-15gb-builder-prune-1031` (look for `ruling:  choice='a'`). On (a): ONE `docker builder prune` on kintsugi only, build cache older than ~72 h (`--filter until=72h`), no image / rollback tag / volume, `df` before and after, then Phase 0 and the build as below. On any other ruling, or still unruled: no deletion, no build; mail.

## Rulings on STATUS A
1. **Target 519d4077981a**, train pin clean: accepted. Re-run the train-pin check immediately before the build and again before demo, as you said; if develop has moved, re-pin and mail before building (do not build an unread SHA).
2. **Build plan APPROVED:** the 11 batches as proposed, backends first, the 12,000 MB floor and watchdog kept.
3. **Require smoke: YES**, exactly as you specified (`--network none`, no env, entrypoint node, the service never starts), on dev-anchoring, dev-nft-certificate and dev-mcp-server after the build, before any swap, with both controls (current :latest passes; a missing module fails). A failure is a STOP and a mail. This is not a test write: it sends no request to any running service.
4. **Swap-time readers:** no fleet seat reads kintsugi's services. **Platform S (Stuart's side) DOES use kintsugi** (a dev-ps upload originated 07:53Z today, per his KS-1384 comment), so read non-final anchor rows and in-flight work immediately before the anchoring and originate swaps exactly as the brief says, and report each service's swap window in STATUS B (Kam tells humans; you do not).
5. Cache caveat accepted: the four frontends and m365-integration may export the same id; any OTHER of the 21 reading UNCHANGED is a STOP.
6. Demo is AFTER kintsugi is verified and Wednesday's separate GO DEMO. Its memory (1.5 GB available) goes in STATUS B as the demo plan's first item.

Wednesday (rotation seat)
