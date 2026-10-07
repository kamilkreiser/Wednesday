# DRAFTER REPORT — Seat R 7th (#1398 merge + PRs 3-5 raise), 2026-10-07 ~00:1xZ UTC

Nothing was sent, launched, merged, pushed or commented. The drafter wrote exactly four files:
- the brief: `fleet/briefs_staged/2026-10-07_seatR7_merge1398_raise3to5.md` (sha256/16 `dbeb9d416f88a697`);
- the DRAFT GO: `fleet/briefs_staged/2026-10-07_seatR7_GO_1398_DRAFT.md` (49 lines, `0e929476618bd9bf`);
- the squash body: `fleet/qa-agent/gatesets/2026-10-06_gate71/recomposed_2026-10-07/1398_squash_body.txt` (7,647 B, sha256 `1a0da3578a906e84d4ea50c8f26799ff17e987e4556f66a9508e61e451132148`). It is the ONE kit write; the file did not exist before;
- this report.

Everything else went to the session scratchpad `…/0e6aaa67-…/scratchpad/r7/`. `!CODING` was read with read verbs only. The shared store's `rev-parse --all` (1,610 lines, `63d58abcdcc5a0b6`) and `.git/config` (`4f624a213933d54b`) were identical before and after. The kit holds 0 `__pycache__` at the end, and the only kit path newer than the drafter's start is the body file.

## R 6th's handover
It did NOT exist at the drafter's start (the 23:57:26Z listing showed R1-R5 only). It appeared at 23:59:31Z: `HANDOVER-seatR6-2026-10-06.md`, 209 lines, 16,907 B, sha256/16 `7bc86aab5da1773a`. It was read whole. The R 6th WRAP mail (`…_seatR6_WRAP.txt`) was also read.

## What I measured, and how
1. **develop and the heads.**
   - Instrument: `ls-remote` with the checkout's own sshCommand and `GIT_SSH_COMMAND` unset, at 23:58:07Z and again at 00:08:37Z.
   - Readings: develop `69f2045af2a4f5f0b83b2f76c62514512abdc7b5` both times; pull/1398 `9414aa54…`; pull/1383 `32e8459bc0f5` (open).
   - In a by-SHA-fetched `--shared` scratch clone: 69f2045's tree is `a4a219b87271`, ONE parent `fa24bddedf3b`, subject 66, 0 trailers, exactly #1404's 4 paths. This agrees with Wednesday's 23:56:29Z verification.
2. **T'' for #1398, from the gate71 kit.**
   - `python3 -I -B c4_docs_gate71.py predict --pr 1398 --head 9414aa54… --develop-after 69f2045a… --num-map 23:28` gives rc 0 and `PASS M1 PREDICTED squash tree of #1398 on 69f2045af2a4: ce7f6c7bbda2b45491dbd3b184df7a49d4d52528` (CHECKED 1, 0 FAIL).
   - Flow tail `[23, 24, 27, 28]`; cheat tail `…KS-1305, KS-1436, KS-1136`.
   - Kit default num-map: same tree, rc 0. Arm `--num-map 23:23`: rc 1, `REFUSED: develop ALREADY carries 23`.
3. **Guard.** `c4 guard --tree ce7f6c7b…`, run from `/private/tmp` (F-3), gives rc 0, `12 passed, 0 failed` = **(12, 0)**.
4. **Hand build cross-check** (`r7/handbuild.py`).
   - Recipe: temp index, read-tree D, the head's 2 code blobs and modes, and the kit's `1398_{flow,cheat}_block.html` inserted verbatim before D's single `</body>`.
   - Result: `ce7f6c7bbda2…`, doc blobs `df566caf8916…` / `b938c3291299…` (== the kit MANIFEST).
   - Positive control: the same recipe for #1404 on fa24bdd gives `a4a219b87271` (== R 6th's T').
   - Negative control: `23.` kept gives `6db4e4c89353` (differs).
5. **Cross-checks.**
   - `mergetree`: rc 1, both docs DIVERGENCE (1 marker each), 0 paths outside.
   - `targets --develop-after 69f2045`: REFUSES at T1, because #1404's code is already on develop. This is expected, so `targets` is the wrong instrument after #1404 and `predict` is the right one.
   - Merge-in counts: 9414..T'' 197 paths (195 non-doc, 2 deletions); D..T'' 4; merge-base `d75bfe2deb80`.
6. **Squash body.**
   - `GET /pulls/1398` (GH_TOKEN by name, never printed): body 7,430 B, sha256/16 `aba1d9423478a0b6`, which equals the gate's reading.
   - `r7/build_body.py` applies 3 exact-once edits and asserts, and an independent shell re-check agrees:
     - 0 trailers (`interpret-trailers --parse` 0 B vs a 23 B control);
     - `Refs KS-1136` is the only Refs line, and the only hyphenated key is KS-1136;
     - KS 878, KS 1305 and KS 1436 are de-hyphenated;
     - 0 `(#`, 0 `merged by` (case-insensitive, control 1), 0 co-authored-by;
     - ASCII, LF.
   - `#1051` (cited by the body) was GET-verified as merged 2026-09-18.
7. **Composed docs.** The kit has none for 1398. I extracted them from the blobs the kit's own `predict` wrote: `r7/composed_1398/1398_composed_{flow,cheat}_doc.html`. Flow is 223,118 B, sha256 `c2ec5de7…`; cheat is 238,104 B, sha256 `673baaee…`. Each one's hash-object equals its blob. They need to be placed in the kit (see Q1).
8. **Other readings.**
   - PR/Linear (00:00:16Z): #1404 merged 23:54:09Z; KS-1313 still UNASSIGNED; KS-1136 In Progress.
   - The three PR 3-5 payloads strict-apply at 69f2045 (check 0 / apply 0); the tamper control refuses at `:177`.
   - vitest 5.0.3.
   - `69f2045` is ABSENT from the shared store.
   - `s-ra3-ks1136` is ATTACHED to the ks-1136 branch at 9414aa54, porcelain 0.
   - R 3rd's handover re-hashed: 235 L, 18,818 B, `35ad164280e587d5`, unchanged.
   - R 6th's tool copies hashed (they differ from R 5th's where R 6th re-keyed them).

## Contradictions / things that differ from the commission
- **C1 — the kit tooling pin `06-tenant-isolation.sh` moved.** Row 1398 in kit.json pins it as unchanged; #1404 changed it (4d077ab30259 -> 6bd87f1308d4). Under R 6th's Q-COVER condition (2) that needs acceptance BY NAME. It is the gate's own ruled merge condition, so acceptance looks right, but it is Wednesday's ruling (placeholder in the GO).
- **C2 — the field label.** The commission calls the target T'', but R 6th's builder parses `- Target tree T\x27?:`, so a `T''` line would fail its regex. The GO writes `T'` on the field line and says so.
- **C3 — `targets` cannot run post-#1404** (see 5). The commission said "predict/targets"; predict is the valid one.
- **C4 — the composed docs** must live in the kit for the GO's "kit's composed doc files" field, and the drafter may not write there.
- **C5 — Actions.** The R 6th builder requires the Actions clauses from a Wednesday ADDENDUM file, not from the GO. The GO therefore releases M-0..M-3 only, and an ADDENDUM releases M-4: the shape R 6th's round actually ran. The zero-new-failures wording is kept OUT of the GO entirely.
- **C6 — length.** The brief is ~291 lines after the house formatter split its long bullets (the commission asked for under ~200). Content was not padded; trimming would mean dropping carried rules.
- **C7 — body edits beyond Q4's letter** (see Q2).

## Open questions for Wednesday (one per line; each also marked in the GO)
- **Q1.** Copy `r7/composed_1398/1398_composed_{flow,cheat}_doc.html` into `gate71/recomposed_2026-10-07/` (hash-object `df566caf…` / `b938c329…`) before sending the GO? Or strike the field and let R 7th extract them?
- **Q2.** Keep body edits E2/E3 (landing text says flow `28.` after `27.`/KS 1436 instead of the authored `23.` after `22.`/KS 1305)? Or narrow the body to Q4's single edit E1? The sha256 changes if reverted. The body keeps the PR's markdown `##` headings: harmless through the GitHub API, but they would be stripped by any `git commit` cleanup path.
- **Q3.** Q-COVER7 (2): accept the 06 pin by name, or re-gate?
- **Q4.** `--dev-paths` for `mergeinra7_1398.sh`: the drafter infers the 7 non-doc paths of b3905..D. R 7th should re-derive it from the tool's own meaning; confirm or leave it to the tool.
- **Q5.** Budget: R 6th reached 52% after one merge. Should track A be pre-assigned to R 8th unless B finishes under ~45%?

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-07 11:1x AEDT
