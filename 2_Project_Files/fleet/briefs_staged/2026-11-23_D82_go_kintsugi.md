Seat D 82nd

GO KINTSUGI (Seat D 82nd): pin b8470f5fd331759f770aca7ae6077442773cf396; prune: card secuura-kintsugi-build-cache-prune-k40-1123 = a, one 'docker builder prune -f' (cache only), free before and after reported; originate off the HELD list, auth HELD.

Kam's card text, verbatim (16:18:02 live board): "Decision secuura-kintsugi-build-cache-prune-k40-1123: a — Clear the build cache once"; option a: "The next deploy seat runs one cache-only clean-up before building (no image, tag or volume removed), reports the free space before and after, and nothing else." And (16:18:18): "Decision secuura-kintsugi-mail-delivery-1123: b — Ship originate without mail".

Your STATUS A + plan confirmation (05:43Z; saved at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_D82_status_a.txt; BLUF and section 0 read by Wednesday) is ACCEPTED: both cards ruled at boot; free 65,505 MB, cache 94.37 GB with 49.29 GB reclaimable; originate's own code = exactly the four files; packages/ diff 0, no .sql, no infra path; H5 green on the KS-278 name only; REVISION fix dry-proved; mail transport still false, reported as a state. develop re-read by git ls-remote in the command that sends this mail (asserted equal to the pin, or this mail is not sent).

Proceed as your brief sections 0 and 3: Phase 0 pre-<box date>k40, pre-build checks, THEN the ONE prune (no --all; a second is a STOP and a new card), THEN the build of originate alone, verify_build (REBUILT 1 / UNCHANGED 32), LC-A on the built image, preswap, swap, postswap (only originate's StartedAt moves; auth and the issuer's a2dc43513fb6 unmoved), watch15, STATUS B. Rollback only on Wednesday's word. Then WAIT for GO LIVE-CHECK (LC-A/LC-B only; no render, no issuer GET).

AUTHORITY: as above, plus Kam 2026-11-23 10:14:18, verbatim: "deploy everything as soon as its tested and ready.  This stands for the rest of the week" (Kintsugi only; demo with Stuart's nod: no step on demo).

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-23 16:44
