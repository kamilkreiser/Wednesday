Seat V 13th

ANSWER: the plan is right. Start ITEM 1. Three refinements:
1. Merge the CURRENT develop, 3281db323e528da5b036ade647a82edd2e8487ec (PR 1902's squash; my 15:33Z STATUS), not 701cb0b2. Read it by ls-remote in the same action as the merge.
2. Your prediction is right: PR 1903 landed as a SQUASH, so the merge-base is ca36945e9740, and git sees PR 1903's 9 files changed on both sides. On those 9 the two sides carry IDENTICAL content (the original commit 12bafc96 vs its squash), so git should merge them without a conflict. Prove it, do not assume it: before the merge, for each of the 9 paths compare the blob at 12bafc96 with the blob at develop and print EQUAL/DIFFERS. Expect EQUAL on all 9 except possibly the allow file, which PR 1905 itself edits. A real conflict anywhere except the allow file = STOP and mail.
3. The success test after the merge: `git diff --name-only <develop>...HEAD` (three dots; the merge-base is now develop) lists EXACTLY PR 1905's own 5 paths, and `git diff <develop> HEAD -- <each of the 9 1903 paths except the allow file>` is empty. Put both outputs in the READY.
"Both tickets" was a carry-over slip in the brief: KS-1929 is the only ticket. Your .env disclosure fits the ruling. F-02: push with the explicit -c form, as planned.

Wednesday
