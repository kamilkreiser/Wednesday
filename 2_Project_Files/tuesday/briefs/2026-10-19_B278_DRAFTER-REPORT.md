# B278 drafter report (2026-10-19, read-only)

**Wrote:** `2026-10-19_B278_SEAT-W2_composer-records-fold-minio-options.md` and this file. Nothing else; no tool beyond Read, Write and read-only Bash.

## Read
- B277 brief and B277 STATUS, whole (structure, REFUSE checks, standing lines, HOLDS, slot and last-line conventions copied).

## Measured (read-only, in the Composer project root and stale `2_Project_Files`)
- Root `main` 06124b9e, `records/b155` 3266142b, `records/b277` a61a5dd4; `git remote` count 0; mail key count 0.
- `main` ends at `### C-74`; `records/b155` adds `### C-75` (so next is C-76, if no other branch also adds one: not scanned beyond b155/b277).
- `main...records/b155` touches 28 paths (CLARIFICATIONS +36, history +17); `main...records/b277` touches BACKLOG.md (58 rows), history.md, STATUS, evidence. So the only predicted conflict is `history.md` (both add at the top). Not run.
- **Collision hazard found:** the root working tree holds UNTRACKED copies of B155's and B277's brief, STATUS and evidence folder (git status). A plain merge would refuse over them; the brief has the seat quarantine (move, not delete) after `cmp`, and copy B277's root STATUS (which has extra sections) back over the committed one. Also the tracked `B26_STATUS.md` is modified in the root; the brief asserts its diff hash is unchanged.
- B138 `:49` (C5) and `:52` (C9) text; B152 STATUS `:7` (card ids, lines 35934 and 36010, ruled a at 06:58:19 and 06:58:17). Line 7 gives the ruling ids but not the card text, hence Tuesday's two slots.
- C-65 at `CLARIFICATIONS.md:1034`, AMENDMENT lines at `:1079` and `:1123`.
- Stale checkout: `compose.yaml:117` has the pinned digest; MinIO is referenced in `object-store.ts`, `services.ts`, `server.ts`, `startup.test.ts`, `edge.nginx.conf`, `health-check.sh`, `edge-upstream-recreate-test.sh`; a `memory-object-store.ts` test double exists. No `DEPLOY.md` read (it lives in worktrees, not the stale checkout).
- `uptime` load 10.24 at drafting.

## Slots left (11)
B_NUMBER_CONFIRM, ROOT_MAIN_SHA, B155_SHA, B277_SHA, COMPOSER_MAIN_SHA, MODEL, STAMP_TIME, PANE, PANE_SUFFIX, CARD_TEXT_WORDS, CARD_TEXT_LOOK. Slot-token grep prints a count >= 1 on the draft (control state); the stamp section names slots without tokens so it does not self-match. Brief is about 110 long lines.

## Doubts
1. Collision handling (quarantine the untracked copies, copy B277's root STATUS back over the committed one) is my addition, not in the commission: R-W2-2, veto if you prefer another route.
2. Candidate MinIO alternatives (SeaweedFS, Garage, RustFS, forks) are from memory, marked UNMEASURED in the brief; licences are not asserted.
3. #297's "true wording" is not in what I read; the brief makes the seat quote only the gate's/row's words or STOP.
4. Whether the 9 "B278" substring hits in Composer Briefs are all hash fragments: I read one only.
5. Three C-entries (C-76/77/78) is my split; fold them if you want fewer. The last-line range follows.
6. Part B's "mirror" route may be dead if no machine holds the bytes: the brief tells the seat to say so.
