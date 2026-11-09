From Tuesday (Datasec coordinator seat), Datasec / NexusAI. ADDENDUM-1 to EVERY NexusAI lane kit of 10 Nov (B1430 N114, B1431 N115, B1432 N116, B1433 N117). It sits beside any lane-specific addendum you already have; both bind you.

## F-1, found by lane F (N116) and adopted for all lanes
`npm run verify` run from a path that contains a dot-directory (your kits' `.tools/<bNNNN>/...`) fails `__tests__/rd438-dot-segment-gate.test.js` (CTRL-EXACT, login 404) **even at origin main**. The cause is `backend/server.js:2859`: `res.sendFile(path.join(__dirname, '../static/login.html'))` with no `root` or `dotfiles` option, and Express refuses an absolute path that crosses a dot-directory. The same suite at the same commit passes from a non-dot path (N116 measured 5/5). Root cause and measurement: `<project>/1_Project_Definition/Briefs/2026-11-10_B1432_STATUS.md:50,87`.

## Ruling
1. **Your full-suite verify (the one a push needs) runs from a NON-DOT path:** a worktree or clone at `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/<bNNNN>-nodot/<name>`, i.e. your own B-number, inside the project folder and outside `.tools`. The tree must be identical to the head you will push: prove it with `git rev-parse HEAD^{tree}` equal in both.
2. **It still goes through the shared jest-lock FIFO.** Keep your place; do not bypass it.
3. **A verify run from `.tools/` that fails ONLY `rd438-dot-segment-gate` is not counted** as a red against your branch. Write `F-1 (path)` beside it in STATUS. Any other red counts as usual.
4. **Push rule unchanged:** no push before a green full-suite run of the exact head tree, from the non-dot path.
5. **The product question** (whether `/login` should be served independent of the checkout path) is NOT fixed in this sweep. `backend/server.js` is lane S's file; lane S does not change it for this. It becomes a ticket by the records pass.
6. Clean up nothing. The `<bNNNN>-nodot/` folders stay; never delete.

Lane-specific rulings already sent (B1430 and B1433: jest-lock ADDENDUM-1) still stand.
