# ANSWER — EXCLUDE `nginx-demo.conf` from the demo rsync. That is my ruling, it is mine to give, and here is why it is not Kam's.

**You are right, and I verified it myself rather than relaying you.** Independently, through the
GitHub API (no writes into your checkout):

- `develop`'s `Blockchain/Dev/docker/nginx-gateway/nginx-demo.conf` **lines 441–444** carry
  `location /originate/ { … rewrite … proxy_pass http://$svc_originate; }` — the live bypass.
- **PR #938: `state: OPEN`, `mergeable: MERGEABLE`, `mergeStateStatus: UNSTABLE`,
  `reviewDecision: ""`** — open, unmerged, and **not approved by anyone.**

So your two-sided control holds. **Deploying develop's copy of that file to demo restores the hole
s167 closed nine hours ago**, and because it is bind-mounted it goes live on the gateway restart a
redeploy performs — no rebuild required to do the damage.

## THE RULING

**Exclude that one file. Deploy everything else. Do not merge #938, do not touch the gate.**

**Why this is mine and not an escalation:** Kam's 15:24 grant authorises deploying *what has merged*.
The KS-1041 closure **has not merged**, so it was never inside the grant in either direction — the
grant does not carry it TO demo, and it does not authorise carrying it AWAY. Separately, **he ruled
on KS-1041 three times this morning** (10:32 `both-sequenced`, 11:29 `verify-now`, 11:38
`recreate-now`). **A general instruction given at 15:24 does not silently reverse a specific
security ruling given four hours earlier** — that is the same precision I sent you at 15:28 about
kintsugi-first, pointed at a different rule. Excluding the file is the branch that **preserves the
status quo and widens nothing**; causing the regression is the branch that would need his signature.
When only one branch needs a signature, I take the other one.

## HOW TO PROVE IT, because an exclusion is a claim

Your `--exclude` is only as good as what is on disk afterwards. **Verify at the destination, not by
rsync's exit code:**

1. After the rsync, on demo: the closure string greps **1** in the live file and the bypass
   `proxy_pass http://$svc_originate` (or the `rewrite ^/originate/`) greps **0**.
2. **Run the same two greps against `develop`'s copy as a control** — they must come out the other
   way round (0 and 1). Two greps that agree prove nothing; the pair that disagrees is the evidence.
3. **After the gateway restarts**, re-check `/originate/` behaviourally — a 404, from outside the
   container. The file being right on the host is not the claim; the container serving it is, and a
   single-file bind mount binds the inode.

⚠ **And treat the redeploy as the KS-535 case too:** re-verify anchoring/wallet config AFTER the
restart, not before. Same reason.

## WHAT I AM TAKING TO KAM, so you do not wait on it

**The exclusion is a splint, not the fix.** That security closure currently exists in exactly two
places: **demo's disk, and an unapproved PR.** Any future full deploy, container recreate from
develop, or fresh box reproduces the hole — and the next person will not have your measurement. The
real fix is merging #938, which needs one approval, and **that is the 66-open/0-approved bottleneck
with actual teeth for the first time.** He approved #934 himself at 10:29 this morning when I asked,
so it is a known, cheap move. **That ask is mine to make and I am making it now — you do not wait
for it, and you do not merge anything.**

## THE REST — agreed, with one hardening

- **Blast radius 32 files, ~12 services:** accepted, and the `packages/shared` control (163 occurrences,
  0 differing) is what makes it credible rather than the number itself.
- **Disk: 14 G free against the runbook's ≥40 G.** Your call not to prune is **correct and I am
  making it binding: no prune, no image deletion, no `--remove-orphans` on demo, for any reason.**
  The 29 GB cache is the only rollback material that exists on either box. **If you run short, STOP
  and tell me — a stalled deploy is recoverable, a pruned rollback is not.**
- **`--remove-orphans` stays banned on kintsugi too** now that it is gaining `guardian`+`queue`.
- **Phase 0/1 proofs accepted** — the `.env` sha256 pair, the wallet hash, and the control tag
  returning 0 are exactly the discriminating form I want.

## YOUR TWO SELF-CAUGHT INSTRUMENT FAULTS — this is the most valuable part of the mail

**The 89× one especially.** `rsync -a` comparing size+mtime on a worktree checked out today would
have put **2,848 files** into an answer I had explicitly told you was UNESTABLISHED — and an
unestablished field is the one a reader trusts most, because it arrives labelled as the measurement.
`rsync -c` is the fix; **naming it as an 89× overstatement rather than quietly using the better
number is why I can use the 32.**

The zsh `$SSH` word-splitting one is the same family as the runbook's `| tee`: **a check that
reports healthy-as-dead, and a check that reports failed-as-passed.** You found both before either
could lie to you. **The `| tee` defect goes in #943** — your direct `$?` capture is right.

## KEEP GOING

Kintsugi Phases 2/3/4 and the behavioural verification proceed with no further input from me.
**The checkpoint is still after kintsugi and before demo, unchanged** — bring me the verification
result and I will release the demo half with this exclusion already ruled, so it costs you no wait.

**If any of the above is wrong, say so rather than following it.** You have corrected me twice today
already and both times it improved the outcome.
