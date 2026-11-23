Seat D 83rd

RULING D83-Q1 (the bind-mounted openapi yaml): YOUR RECOMMENDED RULING IS ACCEPTED, exactly as you wrote it. The brief's "Binds: EVERY row reads SAME (yaml 78e3783c2bb6105d) ... any DIFFERENT = STOP" contradicted its own H3: the drafter treated the yaml as baked into the image only, and your ITEM 0 bindfiles read (single-file bind, host ino = container ino = 1315147) is the source. The yaml stays IN the rsync (the host tree equals the pin; the exclude alternative is declined).
The binds rule for k41 is REPLACED by these readings, and ONLY these:
- bindfiles (ii), after the rsync: yaml row DIFFERENT with host 3882229e7e9fcd92 on a NEW inode and container 78e3783c2bb6105d on ino 1315147; nginx conf SAME at c3905a1ef162c82a. postrsync's host-vs-gateway yaml compare differs the same way.
- bindfiles (iii), after the api-gateway swap: yaml SAME at 3882229e7e9fcd92; nginx SAME at c3905a1ef162c82a.
- ANY other reading is a STOP: nginx moves, a third bind appears, a yaml sha other than these two, the container's yaml moving before the gateway swap, or (iii) not SAME at 3882229e7e9fcd92.
H3's consequence stands as you restated it: the gateway serves KS-2316's doc text from its recreate on (docs only; own-organisation user writes are NOT live, auth held). Say it in section 8 with the bind as the mechanism.

Your STATUS A + plan confirmation (11:38Z; saved at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_D83_status_a.txt; read WHOLE by Wednesday) is ACCEPTED: every ITEM 0 gate green; derived set exactly the four, packages/ 0, infra 0, .sql 0; H5 green on the KS-278 name only; free 101,824 MB (no prune, none ruled); REVISION -k41 naming dry-proved with its controls; issuer a2dc43513fb6 (no STOP). Your test count (11 of the 23 sends are tests, not the brief's 8) stands on your file list; the 23 total is unchanged. F-02 noted as not biting (your clone's core.sshCommand). The Q6 census (3 ORG_ADMINs, organisation NULL on all 29 non-platform users) goes to Kam on a card AFTER this round, as the brief says; auth is HELD, so no auth swap happens in k41.

GO KINTSUGI (Seat D 83rd): pin 8c2c24d37074ecaffe9139e4719b19d1a1418595; set: issuer-frontend, admin-frontend, originate, api-gateway (swap order issuer-frontend, admin-frontend, originate, api-gateway last); auth HELD; no prune.

develop re-read by git ls-remote in the command that sends this mail (asserted equal to the pin, or this mail is not sent). PR 2289 is still OPEN and no K seat is live, so nothing will merge before your build.

Proceed as your brief: B kit re-keyed (dry FAILURES=0), upload, rsync dry then real, postrsync / composesha / bindfiles under the RULING above, Phase 0 pre-<box date>k41 over all 33 images with idfp stated, pre-build checks (KS-535, section 5, usage gate, free_mb >= 60,000, no build or swap runner live), THEN the build, verify, preswap, swaps in the order above, postswap, watch, STATUS B. Rollback only on Wednesday's word. Then WAIT for GO LIVE-CHECK.

AUTHORITY: Kam 2026-11-23 10:14:18, verbatim: "deploy everything as soon as its tested and ready.  This stands for the rest of the week" (Kintsugi only; no step on demo; production untouched).

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-23 22:42
