## You are Seat D 24th (lane Secuura/Blockchain-D): two small items Kam ruled this morning. Post ONE line to Stuart on KS-695, and measure, read-only, when demo's "provisioning smoke (demo)" API key was last used. Then report and wrap

**Why you exist:** Kam tapped two cards on the live board at 08:20 AEDT 2026-10-20, both the recommended option. Read FIRST, whole: `5_Project_History/2026-10-20_seatD-23rd/HANDOVER.md` (your predecessor: demo's state, the KS-1032 vouch secret it armed, the KS-695 part ii precondition it found, and the KS-1584 census that found this key). Model: the routing row for a small census + ticket comment is Sonnet; your launcher pins Opus 5; Wednesday may switch your pane at a ZOOMED idle and tells you by mail if so.

---
## BLUF
1. **KS-695: post exactly ONE comment, addressed to Stuart, carrying this question and nothing else of substance:** *"Stuart, has uat-ps reached build aeae5ca (or later)? Per your 2026-10-13 rule on this ticket, demo-pk takes KS-695 part ii only after uat-ps does; the demo deploy is waiting on this."* You may add one line saying who asks (the Platform K team) and nothing else. Read it back by id. **No other message to Stuart or Peter, on any channel.** (Kam ruled card `secuura-demo-deploy-ks695-uatps-precondition-1020` = a, verbatim *"Ask Stuart on the ticket"*.)
2. **Demo key `key_66e82ef0-a96f-4d4d-9e0f-b6fb6d0b08c0` ("provisioning smoke (demo)", created 2026-07-30, no organisation, no connector): measure its LAST USE, read-only.** Whatever the key store and the request/audit logs record (a `last_used_at` column if one exists; audit or access log rows naming the key id or its `sk_9321ba561` prefix), each source named with its query and a positive control (a key known to be used recently must show a recent use, e.g. the Platform S instance key `key_61774985…`). **Revoke NOTHING; change nothing on the box.** (Kam ruled card `secuura-demo-smoke-provisioning-key-unbounded-1020` = a, verbatim *"Measure its last use first, then come back"*.)
3. **Report in ONE mail:** the KS-695 comment id and its read-back; the key's last-use date per source, or "no record in <source>" with the control that proves the source records uses; anything that suggests a script still uses it. Then wrap (handover + history entry at the top).

## PARTITION
**Yours:** the KS-695 comment; read-only reads on the DEMO box via the project's own deploy tooling and identity. **Nothing else:** no deploy, no rsync, no build, no container recreate, no `.env` edit, no `az`, no key change.
**NOT yours (live):** Seat R 57th (Secuura/Blockchain-R), KS-1677 round 2 in m365; Seat C 30th (Secuura/Blockchain-C), KS-1116 follow-ups in vc-issuer. You share one inbox: a mail naming another seat is not yours. Establish your seat from your pane and process (`@cockpit_name`).

## HOLDS
- Client-facing communication is ticket comments only; the extranet is not a channel. The ONE KS-695 comment is the only client-facing word this round.
- Secrets: never print a key's secret or hash value; key id, name, prefix and dates only.
- Never delete; quarantine. Rotate inside your 80-90 band at a clean boundary.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- `secuura-demo-deploy-ks695-uatps-precondition-1020` = a (2026-10-20 08:20 AEDT): this brief's item 1 puts it in its artefact (the KS-695 comment).
- `secuura-demo-smoke-provisioning-key-unbounded-1020` = a (2026-10-20 08:20 AEDT): this brief's item 2; Wednesday re-raises the revoke question with Kam on your measurement.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The demo deploy of a4187f0f6622 stays NOT GO until Stuart notes uat-ps on KS-695 (ruled to D 23rd 2026-10-20 ~06:3x AEDT).

PROVENANCE:
- KS-695 In Progress, High (scope: S<->K K-side erasure by external_ref, documents.title coverage, connector-scoped org erasure), 29 comments, newest 2026-10-19T14:17Z by Stuart | Linear issue read with the project key by Wednesday | read 2026-10-20
- key_66e82ef0 'provisioning smoke (demo)' ACTIVE, created 2026-07-30, no connector; key_61774985 'Platform S provisioning - uat-ps' ACTIVE | D 23rd's census in its QUESTION 19:35Z and its handover (not re-run by Wednesday) | read 2026-10-20
- both cards ruled a | Kam live board 08:20, kam_rulings_today.sh read by Wednesday, ruled in the store | read 2026-10-20

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-20 08:22
