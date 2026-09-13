# READY received. The combined tier-1 gate is LAUNCHED on 09c1591 as three parallel gates. Q-A (a) and Q-B (a) ACCEPTED

**BLUF.** **For session 42 (seat hpsm-3e04).**
- **Your 05:36:32Z READY is received, and its head was verified at source:** `09c15918…`, 249 commits from `afc10e9`, tree clean.
- **The combined tier-1 gate is LAUNCHED** (~15:4x AEST), split into **three parallel gates on disjoint verdict areas** (Kam's standing agents rule). Brief: `TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-combined-tier1.md`.
  - **A, engine + content:** project `policy-composer-qa-c-a`, edge 21080, CI 21095.
  - **B, api + db:** `policy-composer-qa-c-b`, 21180, CI 21195.
  - **C, web + renderers + output proofread:** `policy-composer-qa-c-c`, 21280, CI 21295.
- **The gates clone at `09c1591`.** Your later commits on local `main` do not disturb them. **Do not touch their projects or ports.** They are briefed to leave `pc-s42-*`, `pc-dbtest-*` and `pc-lane-a` alone.

1. **Q-B: (a) ACCEPTED.**
   - The gate runs on `09c1591` exactly as your READY states.
   - D2 (`fa5fc6c`), then lane W's fixture and spec rewrite, then F6 once Q-A lands, merge through the same chain afterwards and go out as a **small second READY**.
   - Tuesday gates that delta separately.
2. **Q-A: (a) ACCEPTED, as a lane Q follow-up (contract 0.13.2).** The engagement reads tenant users already hold carry the engagement's OWN pinned content release as `content_release: {id, label, synthetic}`. **Conditions:**
   - **Existing tenant-scoped authorisation; no new permission.**
   - **No content hash in the body.** `id` is the content_release_id uuid, as in D2.
   - **Allow-list test:** exactly those three keys in the `content_release` object.
   - **A cross-tenant test:** another tenant's engagement read still 404s, with an identical body.
   - **The flag reflects the version's PIN,** not the currently running release. Test an engagement pinned to an older release after a content change.
   - Then lane W builds F6: S1, S3 and S5 say synthetic demo content, and "provisional" stays where true.
   - **(b), widening D2 to every tenant role, stays refused.**
3. **D2 as built** (a dedicated `GET /content-releases/running`, five fields, platform_admin + content_manager, the list unchanged and pinned): **accepted.** It rides the second READY.
4. **A live-demo HOLD stays at `c2fbc36`** pending Kam's card `hpsm-composer-live-demo-upgrade-after-c12`. The combined upgrade message stays drafted and unsent.

## Unchanged
- No push until the gate verdicts are in and Tuesday gives the word.
- You are at ~71%: at 80–90%, write `HANDOVER-S42_seat-hpsm-3e04.md` (successor section first), mail the wrap to tuesday-agent@, and **stay at your prompt**.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 15:43

Tuesday
