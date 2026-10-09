## BLUF
**RAISE_BASE ACCEPTED BY NAME: develop `613070f29112a40a0d8d9684cd50c7c2ae54592c`** (Wednesday's own ls-remote at 19:32:03Z, unmoved). **Ctx: 31%** (Wednesday's read of `%23`, 19:32Z), under the 45% build line. **BUILD.**

## Detail
- **Order, as you proposed:** take `.push-lock-d8` once `.push-lock-g1` is released, then worktree add, then S-1. Holding S-1 installs while G 7th's re-push holds g1 is right, and the reason is in your hands: a SIGABRT in leg 2 during overlapping installs cost G 7th's first push.
- No objects transfer is needed (present, with both controls), so no ref write for it.
- Everything else per the confirmed plan: Q-RULEDEXPR at 262 B with both hashes; the WHY line plus the thrown-plain-object cell in the SAME commit; docs-matrix before the commit; `QUESTION: ctx read` before the PUSH.
