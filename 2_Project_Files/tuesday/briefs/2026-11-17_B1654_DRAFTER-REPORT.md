STARTABLE: YES, QUEUED - the kit is complete and its sidecar passes, but it launches only after seat N141 (B1652, live, holding the jest lock since 06:09) has ended and its landing is on main; its REFUSE 4 enforces that and re-reads main and the counts pair at launch.

# B1654 drafter report (lane NX-T2, SEAT-N142, Sonnet, row L6, gate G2)
Written Tue 17 Nov 2026 06:18 AEDT (clocks from `date`). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-17_B1654_SEAT-N142_nexusai-lane-nx-t2-test-pins.md` (279 lines) and its sidecar `.measured` (122 claim lines plus 24 extra source lines X01 to X25). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s285/b1654/`.

## BLUF
- One lane, four existing test files and the counts file, no product file: RD-998 (rd452: the tamper stamped with the file's counter, the check ordered by it, cells W1 to W4), RD-985 residual (rd969: cell H8, POST with no content type and no body, plus the reworded comment above H6), RD-996 (rd770 cell calls the helper on every row; rd772 title). Three commits A, B, C plus K. Predicted +5 cells, +0 suites.
- **Two findings the lane needed and the sweep did not have.** (1) The rd770 cell as the ticket proposes it (call the helper per row, compare, `toEqual`) would NOT have gone red when the helper's answer for the `undefined` table row is flipped: jest's `toEqual` ignores `undefined` array items. Measured: 13 of 14 rows red under `toEqual`, 14 of 14 under `toStrictEqual`; the kit freezes `toStrictEqual`. (2) The rd772 title the ticket suggests ("a keyword ending in a non-word character matches nothing") is false for `(x`; the measured truth is: `a.b` and the backslash keyword match one query each, `(x`, `x*` and `[ab]` match none, their own text included. The kit's title claims only that.
- Slot 5 (band 23200-23839), trees `b1654-nodot/{old4,new14,mut8,v7,chk1,chk35}`, no port block. Disjoint from OWNS-B1652 and OWNS-B1648 except the counts file (printed below).
- H8's HTTP answer is NOT measured (no server was run); its proof is plant P7 in the seat's chain, and the kit STOPs if H8 is not red under it.

## Facts re-measured (instrument, control)
- Main `ed3b1aed592b0a249c32537c49f390efde9b59d5` (tree `5145e124...`), open PRs 0, counts 5828/374: `gh api -X GET branches/main` at 05:56 and again at 06:17 (unchanged). Closed PRs #210, #209, #208 (control for the pulls call).
- Four file blobs (`git hash-object` over the raw files; control: GitHub's contents-API sha for rd772 equals mine): rd452 `6147c06c9314`, rd969 `8f343d059a16`, rd770 `e5ee8a34607e`, rd772 `be001e14f1d0`. Last commits `bbb87bac`, `cc855fe9`, `8aae34b3`, `12fca8f3`.
- Jira (GET only, `jwhole1654.py`, all comments whole): RD-998, RD-985 (one comment), RD-996, all To Do; text in `jira_lane.txt`. No HELD or DROPPED line for any of the three keys in the pickup or the last two daily notes (control: RD-987 returns hits in the same files).
- Cells: the four W cells run in a scratch jest 29.7.0 (the project's binary read-only, scratch rootDir, no server): BASE check W1 RED and W2 to W4 green; head check all green; plants P1 clock-back -> W1 only; P2 clock `<=` -> W2 only; P3 order reversed -> W1 W2 W3; P4 missing stamp accepted -> W4 only (`jx_matrix.txt`). rd770 cell with a per-row flip wrapper: 14 of 14 rows red under `toStrictEqual`, the `undefined` row green under `toEqual` (`jx2_matrix.txt`, `jx4_matrix.txt`).
- Body check, real text in a vm (`sim1654.js`): as written `undefined`, `{}` and `[]` each return the five required names; forced true, `undefined` THROWS (the handler's catch answers 500) and `{}`, `[]` return the same five. So H6 and H7 cannot tell the check apart and a request whose body stays undefined can. Express 5.2.1, body-parser 2.4.0 per the lockfile; the only body-parser source on this machine is the stale local checkout at 2.3.0 (`json.js:78`, `:80`, `read.js:46-48`), so those lines are RELAYED and the seat re-reads at its clone.
- Patches apply to the four base files (`patch --dry-run -p1`, A, B, C); `node --check` passes on all four patched files; added lines hold 0 non-ASCII characters and 0 banned tokens (25, 14, 3, 1 added lines); jest runs no hook of a describe whose cells are all filtered out (scratch jest, control run boots the hook), which is why the W plants run in seconds.
- Deploy demo `paths-ignore` is `**.md`, `docs/**`, `tests/**`: `__tests__/**` is not ignored, so a landing starts a run whose jobs must read `skipped` (the #208 merge's did, RELAYED).
- Code scanning on main: 0 open alerts in the four files (paginated; control: `tests/uat-run.js` 1 row; `state=fixed` 218 rows so pagination fires).
- Locks and panes at 06:10 to 06:17: `nexusai-jest.lock/owner` tag `b1652-chain`, `queue-jest/` 0; B1652 STATUS last line `WORKING: B1652 chain, FIFO 1 of 1 (holding the jest lock), step p-plain started 06:10:59`; B1648 STATUS absent; `heads/b1654`, `heads/b1652`, `heads/b1648` 0 (control `heads/b1618` 1).
- Ports: `lsof -nP -iTCP:23200-23839 -sTCP:LISTEN` 0 rows (control: machine-wide listeners 13 at 06:03, 28 at 06:10 when N141's chain was running); a scan of the other SEAT-N kits of 16 and 17 Nov finds `slot 5` 0 times (control `slot 15` 13 times); slot program controls `b1648-nodot/old8` 16, `b1633-nodot/old22` 17, `b1603-nodot/old13` 12 equal those kits' stated slots; all six tree names print slot 5; none of the paths exists.

## Disjointness (printed by `partition1654.py`, `partition.txt`)
OWNS-B1652 (6): `__tests__/rd771-static-page-production-host.test.js`, `__tests__/rd805-entra-test-route-guid-path-parts.test.js`, `backend/routes/entraProvisioning.js`, `scripts/verify-expected-counts.json`, `static/js/index.js`, `static/js/settings.js`. OWNS-B1648 (3): `__tests__/session-cookie-inherited-name-refused.test.js`, `backend/jsonStorage.js`, `scripts/verify-expected-counts.json`. OWNS-B1654 (5): the four test files and the counts file. **B1654 intersect B1652 = the counts file only; B1654 intersect B1648 = the counts file only** (control: B1652 intersect B1648 = the counts file). Census of 46 `heads/b1*` refs by `compare main...<ref>`: two are ahead (the stale b1480 pair), neither touches a test path of this lane (control: compare `0c1dcd30...dcac002d` lists rd452 and rd969). No test, helper, script or workflow names any of the four files (control: `rd395-server-harness` lists 62 files).

## Chain inputs (rule 4: each input is produced by an earlier step or exists at BASE)
| step | inputs | produced by |
|---|---|---|
| 0 browser | tree `new14` at C | commits A, B, C and `worktree add` in Step 1 |
| 1 base-counts | tree `old4` at BASE, the four base files | BASE exists |
| 2 new-cells | `new14`, step 1's per-file counts | steps 1 and the commits |
| 3 scanners | `new14`, the list of Step 1b(ii) | Step 1b |
| 4 mut | `mut8` at C, plant specs and `plant.py` | the seat's tools (Step 1) |
| 5 mainmove | clone, origin | none needed |
| 6 p-plain | `chk1` at C, committed counts at C | commits |
| 7 u-update | `v7` at C | commits |
| 8 kstep | counts file regenerated in `v7` | step 7 |
| 9 p-plain-K | `chk35` at K (or M) | step 8 |

## D-decisions (drafter's, Tuesday may overrule)
- D-1 Three commits (A RD-998, B RD-985, C RD-996) then K, each standing alone green.
- D-2 rd770: call the helper on every row against the table's THIRD column and end in `toStrictEqual`; removal of the cell rejected (it would drop the count by 1 and lose the documented seven rows).
- D-3 H8 sends no content type AND no body; its own header set is built by a one-line helper that strips `content-type`; the cell still sends the CSRF header and cookie (CSRF runs at `server.js:1615`, before the route).
- D-4 W cells named W1 to W4 (the sister's T1 to T4 are taken in the same file).
- D-5 Template parity for the verify flow: plain at head (predicted to refuse on counts only), then update, K, plain at K; costs one verify more than skipping the first (Q3).
- D-6 No local CodeQL step: no product, `static/` or `backend/` path is touched, and 0 alerts sit in the four files; the hosted CodeQL on the merge commit is Tuesday's.
- D-7 The rd969 header index (lists M1 to H5, H3b, E1; says "seven cells") is stale since #208; reported, not edited.
- D-8 The three rd452 server cells that call the check are exercised end to end only by plants P5 and P6 (PREDICTED, not run by the drafter); the tamper stamp point is after the file write, like `at`, so the only possible error is a spurious refusal, never a spurious pass.

## Questions for Tuesday (each with a default)
- Q-1 Launch gate: the kit refuses while N141's STATUS has no final last line or its branch is pushed but not on main. Default: launch only after N141 ends and Tuesday has landed its branch; if Tuesday wants N141's branch merely pushed, an ANSWER file waives 4(b) and the seat regenerates the counts file after main moves (HOLD 20).
- Q-2 rd770: call the helper (kept) rather than remove the cell. Default: kept.
- Q-3 Skip the plain verify at the head (save about 24 minutes of lock hold)? Default: no, template parity (D-5).
- Q-4 If H8 stays green under P7 after two runs the seat STOPs (the ticket's premise changed). Default: STOP.
- Q-5 Row L6's own first choice is the night runner's test-only tier and its Sonnet entry is the fallback; the commission says a Sonnet seat. Default: launch as commissioned (Sonnet, pane `Datasec/NexusAI-N142`); the kit's launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Q-6 The rd969 header index stays stale. Default: report only.

## Before stamping (Tuesday's)
Fill HEADS AT LAUNCH (main, counts pair, N141 ended and landed, B1648 status), LAUNCH WINDOW and the HARD STOP clock (kit predicts about 1 hour setup plus about 2.5 hours of lock hold); re-run `stamp_check.py` and spot-measure at least five sidecar lines; re-check the lock owner file and `lsof` on band 23200-23839 at launch; note body-parser lines are from a stale local checkout (2.3.0 against the lockfile's 2.4.0). Launch uses the newest form (`launch_when_cool.sh`) copied from the B1652 kit with `BRIEF_SEAT_LEVEL=sonnet`.

## UNMEASURED
H8's HTTP answer (RELAYED from the ticket's review probe: 400 at head, 500 under a forced check, no content type and no body); plants P5 and P6; the cell counts per file (a seat's jest JSON); per-run durations; the wider census of non-`b1` heads touching these files (B1618 found seventeen stale session-era heads); the reason three keywords match nothing in rd772 (the kit's title makes no causal claim); the body-parser 2.4.0 source lines.

## Outside-the-fences disclosure
Read-only reads outside the briefs folder: the NexusAI Jira `.env` by name through an in-process reader (no token printed, no write); `gh api -X GET` only; a tarball of main extracted into scratch; `.tools/b1618` and `.tools/b1633` file lists and `lib.sh`/`s6_verify.sh` heads, the two clones' `git config --local --get` (lengths only), the B1618 STATUS, N141's STATUS last line and the lock `owner` file, `lsof`, `tmux list-panes`. I ran the project's jest 29.7.0 binary from `2_Project_Files/node_modules` (read-only) against scratch files with a scratch rootDir and cache: no server, no port, no write inside `!CODING`, so I took no jest lock; scratch only. A hook refused one command (an unquoted separator, nothing ran). Never read: the ledger, `fleet/briefs_staged`, other projects' trees, N141's working trees. No decision-queue call, no Jira write, no push, no mail.

DRAFTED B1654: kit 279 lines, sidecar rc 0, questions 6
