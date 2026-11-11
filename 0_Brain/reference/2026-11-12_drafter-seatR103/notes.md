# Drafter notes, Seat R 103rd brief (2026-11-12 ~07:0x AEDT)

Develop at start and end: c78c80bd537015674fa5e22701d745946f94d4fb (ls-remote, same both reads).
Method: fences extracted from the READY files (first ```diff block) with the R102 drafter's ext.py; own blobless clone at develop in the session scratchpad; `git apply --cached --check` (GIT_DIR form, since a `-C` write verb outside WEDNESDAY is refused by the hook); census = R102 drafter's census.py (GraphQL, 94 open PRs, 408 file rows, no truncation); (ii) = GraphQL search by key (all states) plus ls-remote branch globs. Gate 319 verdict.md: ABSENT at read.

## Per-row (i)-(iv)
| row | key | (i) READY exists | (ii) no PR raised it | (iii) strict apply at c78c80bd | (iv) open-PR census | result |
|---|---|---|---|---|---|---|
| 39 | KS-1868 o143 P1 | yes | OK (no PR on issuerCerts.ts; umbrella has other PRs) | rc 0 | zero hits | OK |
| 30+33 | KS-1868 o138 P2 + o139 P1 | yes (both) | OK | rc 0 each, sequence rc 0 | zero hits (issuerCert.ts) | OK |
| 32+34 | KS-1868 o138 P4 + o139 P2 | yes (both) | OK | rc 0 each, sequence rc 0 | zero hits (tokenisation index.ts) | OK |
| 16 | KS-2021 | yes | OK (0 branches; 4 unrelated merged) | rc 0 | zero hits | OK |
| 19 | KS-1931 | yes | OK (merged 1900 is the KS-1868 kyc PR) | rc 0 | zero hits | OK |
| 12 | KS-1923 | yes | OK (merged 1888 audit KS-1868) | rc 0 | zero hits | OK |
| 46 | KS-1053 | n/a (seat builds it) | no PR raises it (PR 2075 other ticket) | n/a | ks949 test file hit PR 2052 only (expected) | OK, merge-tree gate is the seat's |
| KS-2005 | KS-2005 O103 P3 | yes | OK (PR 2184 is KS-1959) | rc 0 | zero hits (ks1990 test path) | OK, tier 2, LAST |
| KS-2110 | O108 P1 | yes | MERGED copy: G5b cell is on develop line 176, PR 2109 merged | rc 1 (ks1536 test, patch failed at line 82) | PR 2139 (open) edits the same file | DROPPED (stale, already merged) |

Controls: PR 2125 (api-gateway src/index.ts) fired; planted absent path hit nothing; ks949 file hit PR 2052. Planted apply-failure control: KS-2110 itself failed rc 1 (a natural negative); the R102 drafter's planted-context control (ctl_planted.patch) was not re-run.

## Not measured
- Gate 319 verdict (absent) and which gate covers PR 2194.
- Linear state of any ticket; whole suites, red-first/green of any row (the seat measures).
- Fence vs READY canonical patch (fence only).
- KS-2110: whether PR 2109's merged content equals the held patch byte for byte (judged by G5b present on develop plus rc 1).
- KS-2005 red-first and its per-cell durations.
