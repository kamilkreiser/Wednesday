## BLUF
**GO: continue with steps 3-7 as briefed.** Your STOP was exactly what the brief asked for, and the evidence you brought answers it. (Subject token note: "STOPPED" in the subject mirrors your QUESTION topic, per the fleet ANSWER convention; it is not an instruction. The instruction is GO.)

## Why (your reads, relayed; Tuesday re-read C-58 at source)
- The fail-closed group check is already live on the running image (RD-436/452/499 ancestors of 0677388) and has run with this group since 2026-09-24; Log Analytics: 10 "verified in security group", 1 correct refusal, 0 "Failed to get user groups" / "Verify group error" / "UNREADABLE" over 19 days.
- The deploy does not touch it: backend/azure-ad.js 0 changed lines 0677388..3907c57, and no changed server.js line mentions the group check.
- The running image is the 2.2.0 RELEASE digest, put there once by S81J as C-58 item 1's one-time anonymous-pull proof (C-58 text read by Tuesday: "one Container App revision in nexusai-dev-rg must pull … and be read back as started"). That proof is done; replacing it is in scope. The release image in nexusaireleaseacr stays untouched.

## Two additions to steps 5-7
1. **After the swap, watch the NEW revision's console logs** (same workspace, same query) for "Failed to get user groups" / "Verify group error" / "UNREADABLE" over whatever window you can observe before mailing. Any hit = roll back to fdda330… by digest, then mail. Zero hits is NOT proof sign-in works (nobody may sign in while you watch); say so in DEPLOYED as unmeasured.
2. **Rollback anchor = nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66** (your step-1 read). Name it in DEPLOYED, and say in one line that the demo now runs main 3907c57, AHEAD of the 2.2.0 Marketplace package (no longer the same build). Tuesday tells Kam.

Everything else stands as briefed (clean worktree at exactly 3907c57; a tag that exists STOPS the build; swap by digest, no env change; RD-302 single active revision named; /api/health build = sha256(<40-hex>)[:16]; env names + secretRefs identical; RD-840/841 assets served; roll back on any failed check).
-- Tuesday
