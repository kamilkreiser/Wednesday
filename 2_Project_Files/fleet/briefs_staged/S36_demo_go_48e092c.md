## BLUF
**DEMO DEPLOY GO — Kam's word (panel 21:00, verbatim: "Deploy to both"). Deploy `48e092c` — the same image digest `sha256:5d6187df…` now serving the dev app as `0000097` — to the DEMO app, BY DIGEST/SHA, now, before your checkpoint. Same recipe, same rule: rollback digest read live from the demo's serving revision first; `az containerapp update` with `--container-name`; verify ONLY after the OLD demo revision has terminated (RD-302), then two identical rounds; `:latest` unmoved (verify by digest after); the env-name set difference between the old and new demo revisions EMPTY and every secretRef intact; the boot log filtered on the NEW demo revision for the persistence sentinel and the seed line; nothing else on the demo.**

## Receipt (STATUS by mail, then your checkpoint)
The demo's old and new revision names, the digest, the rollback digest, the old revision's terminal state and time, the two rounds, `:latest` unchanged by digest, the boot-log sentinel line, the SSO boundary stated — the same shape as the dev receipt. Then RD-308's comment gains the demo revision; RD-318's evidence comment likewise. If anything in the demo's config differs from dev in a way the recipe does not cover (a different mount, a different env set), STOP before the update and mail a QUESTION — a demo that differs by design is not a dev deploy with a different name.

## Holds
Kam's word covers ONE deploy of `48e092c` to the demo — nothing else moves on the demo; `:latest` unmoved; nothing deleted; no template re-run.

PROVENANCE:
- Kam's word "Deploy to both" (panel 21:00, verbatim) on Wednesday's question "demo tonight too? default dev only" (panel 20:47 + 20:59) | `tools/kam_rulings_today.sh` | read 2026-09-05 21:00
- The dev deploy's facts (`0000097`, digest `5d6187df…`, rollback `9be3d389…`, `:latest` `09b397e7…`, the 108 s window) | your DEPLOY DONE mail 2026-09-05T10:56:33Z, read whole — YOUR reads, not re-derived by Wednesday | read 2026-09-05 20:5x
- The demo app served `--0000092` (`ca98a55`) on 2026-09-02 | Wednesday's INDEX/daily record — NOT re-read on the platform; you read the demo's live revision before you move | read 2026-09-05 21:00

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 21:00
(checked: "before your checkpoint" against the ACK's "three comments then checkpoint" — Kam's word arrived after; the deploy pre-empts and the comments follow it; stated. "one deploy" against "Deploy to both" — dev is done; this is the second half; consistent.)
