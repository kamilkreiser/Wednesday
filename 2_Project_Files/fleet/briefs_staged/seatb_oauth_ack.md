# ACK — seat B (s142): KS-798+KS-841 READY received. KS-799 → GO on Option 2 (the safe path).

## BLUF
**KS-798 + KS-841 READY received on PR #881 (`24f1c00ce`)** — queued behind the batched QA gate;
nothing merges without the gate and Kam's GO. **KS-799: GO on Option 2** — make the consent form
satisfy CSRF via a small JS submit (the XSRF cookie is httpOnly:false, so no exemption is needed and
the double-submit choke point stays intact). **Option 1 is correctly REJECTED** — exempting the path
re-opens the cross-origin, preflight-free surface to a password-verifying endpoint that caused the
KS-781 revert; that would be a security-posture change and Kam's, not ours. Build KS-799 to READY and
join it to the cluster.

## RATIFIED (shape/reasoning) — correctness goes to the gate
Your KS-841 cause-2 analysis (already-closed by KS-804/822's shared resolver; regression test with a
load-bearing control), the red-proofs, and removing ks781-n1's now-redundant overrides while flipping
its precondition to a positive assertion — all sound reasoning. The measurements go to the QA gate,
not my ratification.

## GUARD
If building Option 2 reveals it needs ANY CSRF exemption after all, STOP and bounce it — that flips it
to a security-posture decision (Kam's). READY FOR QA only, gates are Wednesday's, demo frozen,
client-comms = ticket comments only (your KS-798/841 comments are the sanctioned channel). Rotate at
your 80–85% band with a handover.

— Wednesday
