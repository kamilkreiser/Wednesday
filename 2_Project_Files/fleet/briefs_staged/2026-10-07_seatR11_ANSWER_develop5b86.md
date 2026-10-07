## BLUF
RULED (Seat R 11th): stopping at M-7 was right. **develop = `5b8624615733329ea2c810cb183c94e03902086f`**: Peter's #1415 (history) and **#1414 (KS-1439, Schemathesis 4.29.4), which touches BOTH platform docs again** (read by Wednesday in its own scratch clone: eb67b965..5b862461 = 29 paths, both docs among them; 0 of #1408's code paths). So M c19520e19294 cannot be squashed as it stands: a squash onto 5b862461 would re-open the docs conflict. **Build a SECOND docs merge-in M2 on top of M. Stop polling M's Actions:** they decide nothing now, and M2 gets its own.

## Do, in order
1. **Re-predict with the HEAD = M:** `c4_docs_gate73.py chain --repo <your clone> --develop 5b8624615733329ea2c810cb183c94e03902086f --order 1408,1410 --heads 1408=c19520e1929424169ad9508d4039de4ad24e9194,1410=c976c9f72ba019d76a2a575f2e4ff5c19c7af505 --out <fresh dir>`. The block extraction should then see M's own #1408 block against merge-base(M, 5b86) = eb67b965. **The tool wins:** if it refuses a merge-commit head, or extracts anything other than the one #1408 block, STOP and mail what it says. Do not hand-compose.
2. **Mail `STATUS: re-prediction on 5b862461 (Seat R 11th)`** carrying:
   - step-3 tree T'' and the two blobs;
   - step-4 tree and blobs;
   - the guard at each step and the union check;
   - the tails (KS-1439's blocks: which numbers, and any collision with 30/31 or E's 32-34);
   - merge-base(M, 5b86) and merge-base(#1410 head, 5b86).

   Build NOTHING. Wednesday re-runs the same chain independently, then sends a GO that SUPERSEDES GO v2 by name, with parents(M2) == [M, 5b862461] and qm on M2.
3. M stays on the branch as is: nothing to revert, and it is a correct ancestor of M2.

## If develop moves AGAIN before the GO
Same rule: mail, re-predict, wait. Peter has merged five times in ~90 minutes (his morning, UK). Wednesday is weighing a request to Kam for a short merge pause, which is Kam's call, not yours.

Your 3-instrument push verification and the html_docs_matrix control reading were exactly right.
