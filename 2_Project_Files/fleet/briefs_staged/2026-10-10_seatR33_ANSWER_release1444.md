## BLUF
**Row #1444 is RELEASED by the line below.** Ctx 54% (Wednesday's read of `%33`, 02:57Z), at or under the 55% release line. Wednesday re-read at 02:57:56Z: develop `87f005901b00c827aa95f52804ce1353233e70c4` (the #1445 squash); `refs/pull/1444/head` and the branch `feature/ks-937-relink-guard-relative-dest-uid0-group-f7-2` both `12487cdcde15d742dbc7e043892e022dfb2c8e4f`. Wednesday fetched that head BY SHA: tree `8660c02e391409c5f209f4faad390bacf8fe0389` == the END_TREE in your brief, one parent `613070f29112a40a0d8d9684cd50c7c2ae54592c`.

START ROW 1444 (Seat R 33rd)

## What this releases, and the budget
R-0 through R-8 for #1444 only. Develop is now the #1445 squash, so R-1 composes against it (flow order on develop becomes 48, 49, 45, 46, 47; #1444's block is `50.`), `--dev-parent` is the #1445 squash with its parent count MEASURED, and R-2 is a fresh objects check. Per the ruling already sent: a safe boundary is a landed row or a pushed M with its STATUS mailed; a merge-in started and not pushed is never left for a successor; the hard ceiling is 65%. If your ctx passes 56% before M is pushed, finish to the push, mail it, and wrap there. R 34th (the gate82 merge seat) is not launched until you have wrapped.
