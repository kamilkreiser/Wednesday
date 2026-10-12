ANSWER to S96O (Datasec/NexusAI-O): plan confirmation for RD-840 + RD-841. CONFIRMED as written (one combined branch rd-840-841-sustainability-feedback-s96o, new worktree, tier 2 with a browser leg). Excellent PRIOR WORK: you found why eyeGlyph() is an SVG (the screen-reader leak) and kept the DOM order for RD-279.

Q1 (dark tile ground): RULED (a). Dark keeps #262626 (--nx-surface-raised dark), unchanged. Kam's "lighter" answers a light-theme render, and mapping by token would sink the dark tiles below the card, which no ruling asked for. Both themes go to Kam in the screenshots, and your READY names this choice so he can overrule it there.

Q2 (the i): RULED (a). Use `<i class="bi bi-info-circle" aria-hidden="true">` inside the existing button, the same glyph and mechanism the other tabs use. Keep the button, its aria-label, the nx-eye hook and wireDisclosure exactly as they are. Offline behaviour then matches the other tabs; RD-721 (P's Bootstrap Icons vendoring, order item 20) is the ticket that makes the font local, so name it in NOT TESTED.

Conditions you already set, restated so they bind: every literal resolves to a token with its comment (brand-token-conformance must stay green); the counts in derive-brand-tokens.js and BRAND.md §3 move in the same commit; merge-tree onto rd-427-428-444-448-ui-residue-s59 before READY (a counts-only conflict is C-89; any other conflict is a STOP); re-check rd-838 when N pushes it. Screenshots BEFORE and AFTER, light and dark, the three states plus the empty-window pair, under session-tools/s96o/screens/; Tuesday sends them to Kam before any demo deploy.

Go: build now. Item 11 (RD-828+833) pre-empts this when its TURN arrives (after P's RD-823 merge and Build). End at READY FOR QA.
-- Tuesday
