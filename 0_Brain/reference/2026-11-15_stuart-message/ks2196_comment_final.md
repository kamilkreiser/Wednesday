**BLUF:** Stuart, the FAILED sign anchor on demo-pk was our bug: the transaction did not pay the Conway reference-script fee for one wallet output it spent. Nothing reached the chain and no fee was paid. The fix is merged to develop (918f5e6d312a); it is not yet deployed: Kam will confirm timing. Below: your four questions, the fix, and how we are working now, which we would like your view on.

**Short version.** The Cardano node refused the transaction because its fee was too small, and it was our bug. But not
for the reason either of us first assumed. The fee was correct for the transaction's *bytes*; what it did not include
is a **reference-script charge** that the Conway era adds when a transaction spends a wallet output that carries a
script. Our platform wallet holds a few such outputs, and this particular anchor happened to spend one.

**Your four questions.**

1. **Why it failed.** The node asked for 244,248 lovelace of fee and our transaction offered 178,393. That is not a
   near miss, and it is not random: the arithmetic reconciles exactly. The node charges 15 lovelace per byte of any
   reference script carried by an input, the output we spent carries a 4,405-byte script, and 15 x 4,405 is the
   missing amount almost to the lovelace. Our code never saw that charge, because the library we build with does not
   include it and the wallet data we fetch gives the script's identity but not its size. Three attempts, all refused
   the same way within eighteen seconds — which is why it already read FAILED when you polled at 94 seconds.

2. **The one-second pair.** Not a shared output, so your guess was wrong in mechanism — but you were right that the
   pair is involved, and it is the reason this surfaced now. The wallet had exactly one output with no script
   attached. Your declare took it and confirmed. One second later the sign could not have it, so our coin selection
   fell to the next largest output, which carries the script. Had the two been minutes apart, the sign would have
   taken the change from the declare and nothing would have gone wrong. For completeness: a genuine clash over the
   same output gives a different error, "All inputs are spent", which is what nine older failures of ours say.

3. **Will our retry pick it up.** Our own reconciler will not: once a row is `failed` it leaves it alone. But your
   polling does more than read — each poll re-submits the anchor, and we can see it in our logs running three fresh
   attempts at 06:42 and again at 06:54 on 13 November, all refused for the same reason. So it was never silently
   final; it was retrying and failing. There is no harm in it, for the reason in (4).

4. **Final, or re-submittable.** Nothing from it ever reached the chain and **no fee was ever paid** — we checked both
   submitted transaction hashes on a public preview explorer and neither exists, while the declare has thousands of
   confirmations. So re-submitting is safe and cannot double-charge. Once our fix is deployed, the next re-send from
   your side should confirm, and you will not need to create a new anchor. If you would rather send a fresh anchor for
   the signed copy, that works too.

**The fix**, in one line: an anchor now refuses to spend any wallet output carrying a script or a datum — it never
needs one — and it checks, before submitting, that the fee covers what it is about to send. There was a second reason
to do it that way: spending one of those outputs would have *consumed* it, destroying a deployed script.

**One thing worth flagging for your side.** The document's earlier anchors all confirmed, so the document's own
history is intact. It is only the signed copy's anchor, and the events recorded against it, that are affected.

**Status of the fix.** Merged to develop tonight as 918f5e6d312a after a tier-1 QA gate (the anchoring suite 842 passing at the merge, the one pre-existing unrelated failure named). It is not deployed to demo yet; Kam will come back to you on timing. Once deployed, your next re-send should confirm without a new anchor.

**Kintsugi (dev) this evening.** develop 4e4347818772 now runs in eight services on Kintsugi (originate, kyc, tokenisation, vc-issuer, governance, mcp-server, auth, api-gateway). Client-visible: kyc's four routes answer 403 to a non-subject (KS-2166); a typed document create answers 503 while Redis is unavailable (KS-1952); a Pwned Passwords padding row no longer counts a password as breached (KS-2021); originate's 409 mapping follows an unreadable node's other children (KS-2163). None was exercised live. Demo was not touched.

**How we are working now, and a question for you.** The rules Kam has set for Platform K:
1. We approve and merge our own work once it is TESTED: a QA gate verdict at the PR's exact head plus the author's test evidence (Kam, 2026-09-11, "For the time being, I / you will approve our own elements"; widened the same day to "anything that has been finished and tested").
2. The recent merge rules override older holds: a PR that is ready merges unless a current, specific reason holds it (Kam, today).
3. We now run your test suites ourselves before merging (Schemathesis pre-merge, Akto, Playwright, k6 and the full preflight on a local stack slot), so that nothing your process would catch reaches you first. Until that slot is live, every merge says which suites were NOT run.
4. Demo stays behind your nod; merges go to develop and Kintsugi.
**Do you disagree with any of these?** If so, say which, and Kam will discuss it with you.
