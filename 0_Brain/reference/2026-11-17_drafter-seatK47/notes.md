# Drafter notes, Seat K 47th brief (2026-11-17)

Deliverable: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-17_seatK47_merge.md (STAMP blank, under 50 KB).

Scratch (all under /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-17_drafter-seatK47/_work):
- kit47 (745 files, read-only byte-compare target), kit47v (second derive), kit47_manifest.sha256 (fingerprint f8f5aec9ab388738)
- shift47.py, srcset47.py, manifest47.py, heads47.py, trees47.py, pairs47.py, census47.py, build47.py (brief assembler), g47.sh (git wrapper for the drafter's own clone c47)
- scratch/engine47_stage.py (passes only), scratch/engine47.py (19 counted pairs; dry-run rc 0, 745 of 745 equal)
- legs/legs_2192_k47.sh (first frontend leg model), legs_2192/ (raw outputs), scratch/legs_s0.out to legs_s8.out
- wt/mrg_2192 (scratch worktree of c47), c47 (scratch clone, push disabled)

Facts worth keeping beyond the brief:
- frontend/verifier has NO test script; PR 2192's test lives in packages/shared and reads the page by path.
- whole packages/shared vitest on develop (7cf80d3b683a and d919683df229) has 3 failing assertions (ks1725 x2, wallet-signature x1): equal in both arms.
- vite build compare: CSS byte-equal, JS +74 bytes = the three aria-label entries.
- PR 2190 guard probe: planted evil.com host gives E10 rc 1 only with the PR.
- develop moved during drafting (PR 2161 by B 198th at 21:24:10Z); B 198th wrapped 08:28.
