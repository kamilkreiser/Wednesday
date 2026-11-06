From Tuesday, Datasec / NexusAI, to seat N108 (B1354). ADDENDUM-1. This adds one step after your READY and supersedes your kit's "no merge" and "one push" lines for this one case. Your READY at 25f493ec stands as your record.

What changed: main is 993be21a4448b8cda473c991f7763ba5e119fa31; PR #178 moved scripts/verify-expected-counts.json to 5338/321, so your counts file conflicts. Your D6 said this was coming.

Do this, then a new READY line:
1. Fetch origin main. ONE merge of origin/main into b1354/nexusai-l2-tokens, as a merge commit. If the counts file is the only conflict, resolve it through one --update-counts run and assert the arithmetic: main's pair plus exactly what your branch adds. Any conflict in any other file: STOPPED: NEEDS TUESDAY, with the file names.
2. One plain verify at the new head, through the jest lock. No tag of yours may contain the word merge: the lock tool places such a tag ahead of waiting builders.
3. One forward push of the same branch, no force. No PR.
4. Regenerate the render set ONLY if tokens.css changed; if its sha256 is the one in INDEX.md, say so and leave the set alone.
5. The new READY line names the new head and the pair, and STATUS says both pairs. Hard stop: 06:30 AEDT on 7 Nov 2026.

If rd913-archiver-sqlite3-characterisation reads red once in your verify: it is a known race outside your files, on main too. Do not re-run into green and do not chase it: file a new ticket, run it alone once, name both results in STATUS, and last line STOPPED: NEEDS TUESDAY. PR #179 (tests/e2e only) may land meanwhile; it does not touch the counts file, and that move is not a finding. Nothing else changes.
