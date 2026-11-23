## What this changes

`__tests__/helpers/rd615-slow-audit-flush-preload.js` writes its signal file with `fs.writeFileSync` (a create, then a
write). `rd711-audit-flush-serialised.test.js` and `rd615-audit-flush-cannot-resurrect-erased-entries.test.js` read it as
soon as `existsSync` was true, so a read between the create and the write saw an empty file and `JSON.parse` threw
`Unexpected end of JSON input`. One hosted build failed four rd711 cells from that one throw (1 red in 20 builds that
carried rd711).

Each reader now treats the signal as given only once its text parses. A read that throws is polled again inside the
bound the test already had (`waitMs` in rd711, 15 s in rd615). Two files, +16 -4 lines, one hunk each, one commit.
The preload, every cell and `scripts/verify-expected-counts.json` are unchanged.

## Who decided

The test-side fix (the preload left as it is) is the coordinator's default. The atomic write in the preload (tmp, then
rename) was not taken.

## Independent check

- With a writer that creates the file empty and holds 700 ms before writing: the two files at the old readers read
  8 of 8 red (`Unexpected end of JSON input`); with the new readers 8 of 8 green; with the real preload 8 of 8 green.
- A file created empty and never written still fails the cells by value (6 of 8 red, no throw) and the wait ends at its
  bound (138 s for both files, no hang).
- No other file reads the signal file (3 files name it: the preload and the two readers).
- Local CodeQL comparison at this head: no new and no kept high-severity result (29 results at head, 29 at base).

## Not tested

- The hosted Build and CodeQL on the merge commit; Linux; the real race on a loaded hosted runner (the planted writer
  makes the gap certain, not likely); a full verify by the gate (the author's verify read 6235 / 394 PASS).
- The Deploy demo run a merge starts, which must read skipped.

Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
