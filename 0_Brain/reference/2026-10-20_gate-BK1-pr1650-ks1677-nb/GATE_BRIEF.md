# Gate brief: GATE BK1 = PR #1650 (KS-1677 gate BI1's NB1 + NB2 + NB4: PKCE verifier secrecy/randomness cells, the bicep redirect-URI ternary polarity check, one stale comment), Sonnet 5.5, tier 2 (test-only follow-up), round 1 of 2

Commissioned by Wednesday after Seat R 58th's READY FOR GATE (22:52Z). The author's CLAIM is beside this brief: `R58_READY_2252Z.txt` (read it WHOLE). Source of the residue: gate BI1's `0_Brain/reference/2026-10-20_gate-BI1-pr1647-r2-delta/verdict.md` (NB1, NB2, NB4) and KS-1677 comment 81993547.

**Why tier 2, and when to escalate:** the PR claims it is test-only plus one comment line (`packages/shared/src/crypto/encryptedField.ts:61`). If ANY non-test, non-comment byte changes, or a test helper is imported by product code, escalate: say TIER 1 in the verdict and stop at the finding.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE your own scratch folder `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bk1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`, then fetch the PR branch `feature/ks-1677-bi1-verifier-secrecy-and-bicep-polarity-cells` and develop there. Run npm ONLY with an explicit cwd inside that clone, never with the WEDNESDAY tree as cwd.

**Heads (Wednesday's ls-remote, ~09:5x AEDT 2026-10-20):** #1650 head `902b1ee093f921bc4395b40dedb45a9ab6667eb4`; develop `89956fe92956a810f6821fdee09915f087feea7b`. Re-read both at start and at the end; if either moved, say so first.

## Questions (instrument for each; name what you did NOT run)
1. **Test-only, measured:** the three-dot diff file set and a byte-level check that the only non-test change is the one comment line (its text before/after; `tokenCrypto.ts:28` really declares `tokenAad` at develop, with a control).
2. **NB1 cells bite:** re-apply BI-M1 (`codeVerifier = state`) and BI-M5 (`sha256Hex(connectionId)`) yourself on a snapshot, each `tsc` rc 0 first, and show the new cells red on each by ASSERTION (not load failure), restore asserted. Do the cells read the verifier through the service's own decrypt path, and could they pass vacuously (e.g. zero rows read)? Add one mutant of your own that the author did not run.
3. **NB2 polarity:** BI-M4 (`!empty(apiPublicUrl)`) reds H3 by assertion; BI-M6 still reds H1 (control); H1/H2 byte-identical to develop as claimed. Does H3's parser handle the real line shape at `deployment/azure/services.bicep` (read the line), and would it fail closed (red) if the line were reformatted, rather than silently match nothing?
4. **No weakening:** the m365-integration suite by cell NAME at develop vs the head (author: 20 files/201 -> 21/206, 0 vanished).
5. **Landing:** merge-tree of the head on live develop; give the landing tree sha; m365 `tsc --noEmit` rc 0 at the landing, and the new test file type-checked in its own program.
6. **The author's two residue points:** confirm or refute by measurement (a) m365-integration is absent from preflight leg 16's corpus (read the leg's script, cite the line); (b) packages/shared suite green at develop (run it). Findings only.

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 902b1ee093f9... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. Last line: the sha256 of `sed '1d;$d' verdict.md` (the file without its first and last line), labelled with that method.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; **no Docker** (another seat is using it on this machine); every zero with a positive control. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.
