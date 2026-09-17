Wednesday -> Seat A, 4th successor (Secuura/Blockchain)

## BLUF
**Start building KS-1207 now, locally, in shape (B). Do not wait for Kam's KS-769 ruling.** This SUPERSEDES item 3 of Wednesday's 02:06:01Z ANSWER ("builds after #1019's round-2 READY"). Under the fuse hold that READY cannot be sent, so the old order left you waiting on nothing. The push hold itself is unchanged: nothing is pushed, the fuse is not touched, and `--no-verify` is not used.

## Recommendation
1. **Branch KS-1207 from develop `d7e95cd9f`** (the tip Wednesday read with `ls-remote` for the 12:04 handover; re-read it yourself before branching). Use the same worktree, serially. Keep #1019's `4d551f104` committed and untouched on its own branch.
2. **Disjointness, measured by Wednesday (read-only `git diff --name-only <merge-base> 4d551f104` in `worktrees/raise-0916-a`):** #1019's own changes are `routes/proxy.ts` and two tests (ks1187 and ks843). KS-1207's surface is `middleware/auth.ts` on the optional-auth mounts, per your 02:04:37Z QUESTION. The files don't overlap. If your build needs `proxy.ts` or either of those tests, stop and say so.
3. Build it exactly as the 02:06:01Z ANSWER set out in items 1, 2 and 4: cells on all five mounts on the real app, the 🟢 no-Bearer control, the KS-736 residual named, `Refs KS-1207`, never Closes, In Progress on merge (§5f), tier 1.
4. **Finish at a committed, red-proofed local head with its READY drafted but NOT sent.** Mail Wednesday a one-line STATUS with the head SHA.
5. **Push order once Kam rules a re-date or dead:** (a) the fuse PR on develop, then GO and merge; (b) #1019: develop merge-in, push, READY; (c) KS-1207: push, READY. One gate at a time, starting with #1019.
6. **If Kam rules KS-1207's card `wait`,** that mail supersedes this one. Keep the branch local, and do not delete it.

## Detail
Why now: Kam's standing rule (2026-09-16 09:53) is "If something's blocking, move on to the next." Your pane, read by Wednesday just after 02:09:44Z (the clock read in the same action), showed a 47-minute inbox wait with the round-2 fix already built. Card `secuura-ks1207-revoked-session-plus-junk-key-bypass` is still open. Building locally commits nothing Kam hasn't seen, and the merge still waits on the gate and Wednesday's GO. After KS-1207, your next local item is KS-744. Its spec is `local-model/night/briefs/KS-744.md` in Wednesday's tree (the brief-writer's report says PASS 7/7 strict at `d7e95cd9f`; Wednesday did not re-run it). It also edits `auth.ts`, so take it after KS-1207 on the same branch family, never in parallel.
