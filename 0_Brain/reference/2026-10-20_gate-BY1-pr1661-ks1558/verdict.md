VERDICT: GO WITH NOTE at head 7ecb3257ec69... (tier 2, round 1 of 2; landing tree a3a5463b68cb0d4fe30c6a2fb2e76869cf4d961d on develop 3cc46ae41fed0ba8f9b3423f7737344a4916c948; 0 blockers, 3 notes)

## BLUF
The ticket check does what it says. A reason citing KS-nnn/PS-nnn passes; a reason citing none (or `KS-`, or lowercase `ks-1`) fails; a ticket in the PATH half does not excuse it. The two Akto exceptions pass. The suite is 23/23 at the PR head and on the landing tree; develop alone is 14/14. Nothing to block on. Three notes, none touching the claim.

Heads: ls-remote at start and end both read #1661 = 7ecb3257ec69221057b98c4df20d33133451c229 (identical, as Wednesday read it). Develop MOVED during the gate: 108091b2... at start, 3cc46ae4... at end (one commit, "Refs KS-1659", touching 0 of the two files). Landing derived on both; the one above is the live one.

## Findings (notes)
N1 No word boundary. `*KS-[0-9]*` is a substring glob, so `NOTKS-666: Akto...` (arm B3) PASSES (rc 0, "106 invariants hold"). Likewise `KS-1abc` (digit first, junk after). Lowercase, `KS-`, `KS-abc`, `KS 687`, `ps-9` all correctly fail. Cosmetic: nobody writes NOTKS-666 by accident, but "a ticket-shaped token" is looser than the comment says.
N2 No-pipe entry. `${_e#*|}` on an entry with no `|` returns the WHOLE entry, so a bare path containing a ticket token (arm B7, `...assert-compose-project.sh KS-9`) satisfies the ticket check. It is not an escape today: the existing "carry no reason" check (inside the census branch) still reds it (rc 1, seen). It matters only if that sibling check is ever removed or the census returns empty. Same family as the author's M1, one step over.
N3 bash 3.2 + `set -u` + EMPTY `LAUNCHER_EXCEPTIONS=()` dies "LAUNCHER_EXCEPTIONS[@]: unbound variable" (rc 1, arm B8). NOT a regression: the PRE-PR file (pr1661~2) dies identically at the older `_declared` loop (seen), and CI is ubuntu-latest (bash 5, empty-array expansion is fine there). The new loop shares the exposure; nobody is going to empty a 5-entry list, but the primitive is confirmed (`a=(); for e in "${a[@]}"` unbound on 3.2, `${a[@]+"${a[@]}"}` reaches).

Confirmed, author-disclosed, not findings: R1 pins file content only; both cited tickets are Done so the guard proves attribution not need.

## Q1 - refuses a ticketless reason, passes a ticketed one, path half excluded
Positive control: unmodified gate rc 0, "OK - 106 shared-stack safety invariants hold (KS-666)" (develop alone says 105).
Author's arms (bash 3.2, in-tree variants, each parse-checked with bash -n):
- A1 both Akto tickets stripped: rc 1, `cite no ticket (KS-1558): systemTest/akto/scripts/start.sh systemTest/akto/scripts/assert-compose-project.sh`.
- A3 `KS-666:` -> `KS-:`: rc 1, names start.sh only (assert-compose keeps KS-687).
- A4 path renamed `KS-666-start.sh`, reason ticketless: rc 1, `cite no ticket` names `.../KS-666-start.sh` (other reds also fire because the rename orphans the real start.sh).
- Author's M1 (predicate widened to `"$_e"`) reproduced in my clone: suite 22 passed / 1 failed, exactly `FAIL RED KS-1558 R4`. Restored by `git checkout --`, sha256 prefix 96bf0dec551c8b97 before = after, `git status --short` empty, suite back to 23/23.
My own arms: B1 lowercase `ks-666` / `ks-1` (rc 1, both named); B2 `KS-` and `KS- ` no number (rc 1, both named); B4 `KS-abc` (rc 1); B5 `KS 687` (rc 1); B6 `ps-9` (rc 1); B3 and B7 are N1 and N2. Each arm had a fixture-took check (identical-file detector; B7's first attempt did not take, was said so, and was redone).

## Q2 - Akto exceptions; ticketless fails OUTSIDE the census branch
Real tree: the two Akto entries cite KS-666 / KS-687 and the gate is rc 0. Outside-census proof: a copy of the gate in a NON-git directory (so `git ls-files` finds nothing and the census matches ZERO) with Akto's tickets stripped prints BOTH `cite no ticket (KS-1558): ...start.sh ...assert-compose-project.sh` and `census matched ZERO scripts`. Control: the same non-git copy with tickets intact prints only the ZERO-scripts line and NOT the ticket line. So the ticket error fires independent of the census.

## Q3 - portability
macOS /bin/bash 3.2.57: gate rc 0 at PR head; suite 23/23; every arm above ran on 3.2. Paths with spaces: an entry `systemTest/akto/my scripts/sta rt.sh` ticketless is reported intact in the message (it is space-joined, so two names run together visually, cosmetic) and a ticketed spaced entry raises no ticket error. `set -u` + empty list: N3. CI bash: workflow runs `bash scripts/check-stack-safety.sh` on ubuntu-latest (working-directory Blockchain/Dev); no bash 5 binary exists on this machine, so CI's bash was NOT run (see NOT RUN).

## Q4 - landing, runner before and after
`merge-tree --write-tree` develop 3cc46ae4... + PR head: rc 0, tree a3a5463b68cb. Also rc 0 against the earlier develop 108091b2 (tree dc1561a7b191). develop moved 108091b -> 3cc46ae touching 0 of the two files, so the gate/suite content on the landing is identical either way.
Runner (bash 3.2) by cell: develop 108091b = 14 passed / 0 failed, gate 105 invariants. Landing commit of 108091b + PR (synthetic, in my clone) = 23 passed / 0 failed, gate 106 invariants. The 9 added cells, all `ok`: CONTROL array read (5 entries) · RED R1 · CONTROL pristine says nothing · RED R2 · CONTROL PS-nnn counts · RED R3 bare KS- · CONTROL still names only stripped entries · CONTROL path-token fixture took · RED R4.

## FOUND / TESTED / HOW
FOUND: 3 notes, 0 blockers; the PR's claims (23/23, 106, R4 kills M1) all reproduce.
TESTED: Q1-Q4 above; 9 own/author arms + M1 mutant, 2 landings.
HOW: scratch clone under the scratchpad (`git clone --shared` of the cache, fetch of refs/pull/1661/head and develop with the project's deploy key as a fetch only), gate variants as untracked files beside the real one and made with `sed`, moved out (no rm) afterwards; the M1 edit restored by content and asserted. Nothing under !CODING, no push, no GitHub/Linear write, no Docker, no box.

## NOT RUN
CI's bash 5 (none installed locally; no Docker allowed). The full run-shell-suites.sh and the other CI jobs. The suite on the FINAL develop 3cc46ae (not run; the 1 new commit touches neither file, merge-tree clean). The "carry no reason" sibling check was exercised only through B7. No launcher against any stack.

## Wall-clock
About 4 minutes of commands (203 s at the first checkpoint, 01:17 to 01:21 UTC), plus the landing re-derivation.
sha256 of `sed '1d;$d' verdict.md | shasum -a 256`: ef573419df74a30459202cdb83f18d6faebd502319502ddd9332df50a50cc353
