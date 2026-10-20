From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-1 to B386 (SEAT-D17). It answers your FOR TUESDAY items 1 and 2. Everything else in your brief stands (HOLD, partition, load rule, no PR, no merge, no deploy, never delete).

## RULED BY TUESDAY (2026-10-21, s133)
1. **ONE PR, at a new tip.** Your FOR TUESDAY 2 option (b), done by you now: B377-3's expectation changes in `web/e2e/hosted-entra.spec.ts` are added to YOUR branch as ONE new commit on top of `687246aa`. Lane 5 (B384) was never launched, so nobody else owns that file today; this addendum grants you that ONE file for those changes only. Why: one tier-1 gate for all six items instead of two gates on a loaded machine; the gate keeps the cut (`e5a5c21` stands alone if B377-3 fails).
2. **B377-6 is DEFERRED past the HP review.** The two `hosted.test.tsx` rows assert a banner-per-page rule; changing them needs a ruling on that rule against C-27 b, which is not tonight's work. Leave the quarantined change where it is. Do NOT commit it.

## Your steps
1. Re-read pins: `ls-remote` main still `54fbceac…`; your branch still `687246aa…`. If either moved, STOP with what you read.
2. In your worktree on the branch: edit ONLY `web/e2e/hosted-entra.spec.ts`, ONLY the 5 places you listed (`:22-23`, `:85-86`, `:92-93`, `:118-119` -> the new `/?next=%2Fworkspace` URL; `:33-35` -> the `/workspace` landing). The new expectations must assert the NEW behaviour exactly (match the URL including `next`), not loosen it (no `.*`, no dropped assertion). Say in STATUS, line by line, old -> new.
3. Run that spec locally if Playwright and its stand-in run here at load1 < 8 (the project's own e2e command for that shard; read how CI runs it in `.github/workflows/ci.yml`); if it cannot run here, say NOT RUN plainly and why: CI's `web e2e` shard on the PR is then the evidence.
4. Whole web suite, typecheck and lint once more at the new tip (counts unchanged from your 1898, names lost 0).
5. ONE commit (message `B377-3: e2e expectations follow the deep-link return (hosted-entra.spec.ts)`), plain push, read the head back by `ls-remote`.
6. Last line, exactly: `READY FOR QA: B386 b386/reviewer-path-fixes-b377 @ <sha40> · tier 1 · commits 1,2,3,4,7,6 + e2e (B377-6 deferred) · e2e spec <run locally: n/n | NOT RUN: reason> · web <n>/<n> · 0 tickets, 0 comments`.

## Do NOT
Open a PR (Tuesday opens it), touch `hosted.test.tsx`, commit B377-6, edit any other e2e spec, post Jira, or merge. The Jira drafts in `.tools/b386/texts/` stay drafts (Tuesday's records seat posts them).
