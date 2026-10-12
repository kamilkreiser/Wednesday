BRIEF to S96O (Datasec/NexusAI-O): build RD-840 + RD-841 (the two Sustainability feedback tweaks you filed). PLAN CONFIRMATION FIRST; no code before Tuesday answers. Your item-11 merge turn (RD-828+833) comes first whenever its TURN mail arrives: pause this build for it.

KAM RULED (live board, 2026-10-13 09:46:43 AEDT, view=tuesday, verbatim): "Decision nexusai-sustainability-feedback-rd840-rd841-1013: a — Do both". Option a's text: "Build RD-840 and RD-841; screenshots in both themes to you before any demo deploy." Comment the ruling on both tickets in your first turn and mail Tuesday the comment ids. These change a design Kam ratified on 2026-09-03 (RD-262, RD-281); his ruling today is the authority for exactly these two changes and nothing wider.

SCOPE (the tickets' own text, as you filed them):
- RD-840: right-align the metric numbers with the unit before them; Improvements tiles lighter and full column width.
- RD-841: replace the per-figure eye with the circled "i" the other tabs use.

THE PLAN CONFIRMATION MUST CARRY
- PRIOR WORK: what RD-262/RD-264/RD-267/RD-281 built and why (the mock, the ratified layout), and where the circled "i" lives on the other tabs (reuse it, do not invent a new glyph).
- STYLE: colours and weights ONLY from NexusAI's own style guide / brand tokens (name the file you read). "Lighter" means a lighter token from that guide, never an invented colour; any colour that does not resolve to the guide is a Major.
- PARTITION, both sides: your expected files (sustainability-ui.js/.css and their tests), checked against every open head not yet merged (git diff --name-only main...<head>), including your own rd-828/833, rd-801/822, rd-802, and N's rd-839 and the coming rd-838. Name any overlap.
- TESTS: red-first cells for the alignment, tile width and icon; the existing Sustainability dark-mode and colour-corpus tests in the C-68 set.
- SCREENSHOTS: before and after, both themes, every Sustainability state the change touches, saved under session-tools/s96o/. They go to Kam through Tuesday BEFORE any demo deploy; a merge to main does not deploy demo by itself, and you check deploy-demo.yml says so.
- TIER: 2 with a browser leg at the gate (a rendered surface).

HOLDS: no merge outside the turn order; no deploy; nothing to any human; never delete; one branch per ticket or one combined branch named from both tickets, your choice, say which.
-- Tuesday
