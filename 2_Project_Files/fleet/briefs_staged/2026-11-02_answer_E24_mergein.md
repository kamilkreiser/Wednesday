Seat E 24th

ANSWER: do NOT merge develop in. Push the delta on your built base, as you planned. This SUPERSEDES the forward-move rule's "merge the new develop in" step for PR 1897 only. The reasons:
- develop moved by two squashes (8126b22bd5aa, ad78fa106785) that share 0 paths with your 9 (your measurement), and your base is their ancestor;
- the merge seat proves merge-tree on the live pin in the same action as the merge, and squash merging lands it as one commit either way;
- a merge-in commit would put 12 unrelated paths into the delta range and blur the delta gate's blob table.
If develop moves again with a SHARED path before the merge, that is a stop-and-mail, as the rule says.

Filing accepted as you did it: F2 on KS-1214 (comment cb994edc), F3 as KS-1928, F4 held by KS-1868 with the cross-reference. The READY-mail correction (22 checks, not 24) is noted.

Next as you wrote: VERIFIED push -> PATCH notes -> READY FOR GATE: PR 1897 delta (G82-F1) with the blob table and the product diff.

Wednesday
