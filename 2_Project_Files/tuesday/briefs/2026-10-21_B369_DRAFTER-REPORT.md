# B369 drafter report (HPSM-POC PR #166 builder fix round, SEAT-D10), 2026-10-21 05:16-05:30 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B369_SEAT-D10_hpsmpoc-pr166-fix-round2.md` (123 lines, 2 unfilled stamp slots: `@MAIN_SHA@`, `@STAMP_TIME@`, B364's format). **No `.pre-stamp` copy exists for B369**: I wrote the brief once, at its final name, with the slots in it. Tuesday saves the `.pre-stamp` copy before stamping (the seat's REFUSE slot-count control reads it).

## What I read (whole)
B367 STATUS (289 lines; findings `:212-240`), B364 brief (105 lines), B364 STATUS (125 lines); the raw text of `Hpsmpoc290Tests.cs` (319 lines) and `PkcsInPackageTests.cs` (386 lines) at the PR head and `FeedbackAttachmentTests.cs` (`Form`, `Upload`, `Part`) at the PR head, by `gh api` raw GET; the B364 `.pre-stamp` Stamp paragraph (for the slot format).

## Facts (MEASURED 05:16-05:25 unless marked)
- `ls-remote`: branch `b364/feedback-pkcs-test-gaps-294-295` and `refs/pull/166/head` both `4794bde3ac1fc7e0025146e37c11dfa6bd63db90`; `main` `6818896b68090777c8edbf0e694741928c96ca3f`; `refs/heads/b369*` none (control: `b364*` returns the PR branch). `date` 05:16:30 AEDT, load1 3.77.
- `.tools/b369` and `.tools/wt-b369-*` absent; `.tools/b364`, `.tools/b366`, `.tools/b367` exist. Listeners in 7360-7389: 0 (control: unfiltered `lsof` = 12 lines). B366's block 7360-7369 is quiet at this instant (so B366 may not be binding yet); the brief still forbids it.
- Line numbers at the head, `Hpsmpoc290Tests.cs`: `Unreadable` `:29`; `Rows` `:48-67`; `HelperRows` `:82`; `HelperRowData` `:85-94`; old guard comment `:158`; `FaultingHost` `:170`; `SignedIn` `:173`; `PostWithFailingBody` `:183-190` (carrier `"x"` `:186`); control row `:196-208` (`seen` `:202`, assert `:207`); 500 test `:213-224` (`seen` `:217`); IO twin `:227-238`; helper theory `:241-242`; `FailingBody` `:260`; `FailingBodyFilter` `:299`. `PkcsInPackageTests.cs`: `PackageVersionOf` `:139-141`; pin theory `:326-330`; build-0 fact `:334-338`.
- **Hazard I found that the gate did not state (by reading, not by running):** `Form` builds `new MultipartFormDataContent()` with a random boundary (`FeedbackAttachmentTests.cs:36`), while `FailingBody`'s head bytes use the constant boundary `b284fault` (`Hpsmpoc290Tests.cs:257-258`) and the reader takes the boundary from the request's Content-Type. So "use the control's `Form(Item, a.png)` as the carrier" (R2) cannot be done literally: either the header keeps `b284fault` over a body with another boundary (the unplanted case then is not a clean 201), or the header keeps the form's own boundary (the planted head bytes then carry the wrong one). The brief names the two ways out (i) `FailingBody`/filter take the boundary from the request's Content-Type, (ii) a local `MultipartFormDataContent(Boundary)` helper, and makes the seat record which and why.
- Test-method renames count as lost names: the helper theory is called `The_four_rows_...` and will run six rows; the pin theory is called `..._not_against_10_0`. The brief forbids renames and requires the comments to be made true.
- The 500 test also reads `seen` before its host starts (`:217`) but asserts the specific planted text, so it is not weak the way the control is; the brief says leave it.
- Gate figure I could not reproduce from the text: its fix-shape says "mG in 7" for route (a); consistent with 5 + 2 name rows (my arithmetic, not a gate measurement).

## Predictions written into the brief (all UNMEASURED; the seat measures)
Class `Hpsmpoc290Tests` 28 -> 32 (the gate measured 32 with two scratch rows, `B367_STATUS.md:110`); Feedback project 298 -> 302; `PkcsInPackageTests` 23 -> 25; Api 1514 -> 1516; mN 5, mG 7, mG-name-only 5, mG-file-only 2, mF 2, mF2 2, mMajor 2 (the two new rows: the 11.0.x row goes null, the 10.0.500.0 row goes "10.0.5"), a-pin 4 (B364 measured 2).

## UNMEASURED, with the instrument that would measure it
- Exact header values of the gate's two extra rows and their answers at the head: a scratch test through the shared host (the seat does it, quarantined).
- Whether the control's request logs anything in the capture after the `seen` move (R4): a scratch test; brief says STOP that row if red, not weaken it.
- Whether the two new rows were a 500 at `befd45e` (so the comments must not claim it): run at the pre-fix commit; the brief tells the seat not to claim it.
- Pane `Datasec/HPSM-POC-D10` free, B366 live/idle: the cockpit pane list (I may not read tmux).
- Whether the weekly gauge allows a Sonnet launch (P2/P3): Tuesday's launch check.
- Whether the 20/20 CI result holds on the next push: CI after the seat's push.

## Decisions I made that Tuesday may reverse
- One commit (not per finding) as the recommended shape; per-finding is allowed in the text.
- The seat may `cp`+`cmp` the previous builder's kit from `.tools/b364/` (and re-aim it); it may not read `.tools/b366/`, `.tools/b367/`, `.tools/wt-b367-*`.
- The seat builds its own worktree on a LOCAL branch `b369/local-fix-round2` because `.tools/wt-b364-fix` has the PR branch checked out; it pushes with `HEAD:refs/heads/b364/...`. (Reason from git's rule that one branch has one worktree; the worktree list was not read.)
- "No `dotnet build-server shutdown`" also overrides B364's release line.
- No Jira comment on HPSMPOC-295 even though R3 adds a row (your ruling: nothing else to Jira).
- The brief avoids the client's name and every person's name (the restricted-docs path is referenced by B364's line instead of retyped; the gh account is referenced by B364/B367 STATUS lines instead of retyped).

## Questions for Tuesday (recommended answers)
1. **R2 boundary: do you want to pick (i) or (ii) now?** Recommend leave it to the seat with the constraint written (smallest sound way, recorded); I lean (i) because the carrier is then exactly `Form(Item, a.png)` and no form builder is invented.
2. **Is a second `Form`-like helper (option ii) a breach of B364's "do not invent a form builder"?** Recommend no; that line was about the first round and about not duplicating the head bytes. The brief keeps it inside `Hpsmpoc290Tests.cs`.
3. **Copy from `.tools/b364/` allowed?** Recommend yes (previous seat done, kit is read-only copies). If you say no, the seat rewrites its runner and mutator, which costs time and load.
4. **Round 2 of 2 cap: should the seat be told what happens on a second NO GO?** The brief says "goes to the product owner"; recommend keep, per your message.
5. **Stamp:** save `.pre-stamp` first, fill the two slots, re-run `ls-remote` for main, the PR branch head and `refs/pull/166/head` just before launch (a push by anyone changes the REFUSE).
6. **Dependabot alert and the stray upstream line in the shared `.git/config`** are left to you (named in HOLDS as not the seat's). Recommend route them to the records seat, not this seat.

Process note (own error, in the open): I first wrote the file with a `.pre-stamp` suffix by mistake and then `mv`'d it to the final name (a rename of my own file; nothing deleted; no stray file left). Everything else was read-only: `ls-remote`, `gh api` GET, `lsof`, `ls`, `uptime`. Scratch copies of the three raw files are in the session scratchpad only.
