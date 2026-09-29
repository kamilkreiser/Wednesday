# gate48a — the NEW baseline row's `reason`, VERBATIM, split into sentences for REASON-TEXT-TRUE

Read 2026-09-29T22:34:28Z by baseline_gate48a.py: `git show 4370be410bbf37b839b1030f3e28f95d11c454fe:Blockchain/Dev/scripts/audit/audit-baseline.json`, row `GHSA-r53p-7pc4-xj5r`. reason sha256 e75b662a69b9b686eccdbf17ff9cecc73f9decdf4b24d19ff3beda8f8aeee58b, 1631 chars, 10 sentence(s). The split is at `. ` / `; ` before a letter; the gate checks EVERY sentence as a row (claim · instrument + tree/image · TRUE / FALSE / UNMEASURED / TRUE-BUT-CONDITIONAL). The drafter checked NONE of them. It is a PUBLISHED record: it lands in develop and every later reader of the baseline reads it.

1. Same closed build-tree-only path as GHSA-2mjp-6q6p-2qxm, re-measured 2026-09-30 for this advisory (published 2026-09-29, first patched 6.28.1).
2. The pin is undici 5.29.0, reached only via frontend/issuer -> @meshsdk/core -> @meshsdk/provider -> @utxorpc/sdk -> @connectrpc/connect-node (which declares undici ^5.28.3).
3. Measured FROM THE ARTEFACT, not the manifest: the issuer image built from this tree serves 58 files from nginx with ZERO node_modules directories anywhere in the image, and undici, connectrpc and connect-node each occur 0 times in the served tree, with positive controls react=27 and secuura=8 firing in the same grep.
4. undici is pinned in 0 of the 27 service standalone locks (all 45 tracked locks parsed, 14924 package entries).
5. No Dockerfile copies the workspace-root lock: every image copies a per-directory manifest, so the root lock's own undici entry reaches no image either.
6. No patched version exists inside ^5.28.3 - the newest 5.x on the registry is 5.29.0 itself - so this cannot be closed by a lock bump;
7. an unscoped overrides entry would close it and all 12 sibling rows, sized 2026-09-30 in a scratch regen at 723->721 entries, with its build and suites UNMEASURED.
8. TEMPORARY, expires 2026-10-09: it joins the single shared re-triage date this file already carries (four rows on that date) rather than taking a fresh one.
9. This is a NEW acceptance on that shared date, not a re-date of any row Kam dated - those four carry his signed instruction in their own reason and are untouched here.
10. The real fix is the unscoped overrides bump, which also closes the 12 sibling rows, and it is due by that date.
