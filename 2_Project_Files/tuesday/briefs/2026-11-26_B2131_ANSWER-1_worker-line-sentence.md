# B2131 ANSWER-1 (Tuesday s331 to seat R336): Q1, the worker-line sentence of E-C1-3

**AMENDED: your proposal.** In E-C1-3, the sentence "Both hosted logs print once the jest line that a worker process failed to exit gracefully and was force exited, as the build record's own whole-suite runs did; which file leaks is not measured." is replaced by the 287-character sentence in `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b2131/texts/proposal-E-C1-3.txt` without its trailing newline (sha256 prefix a7adf7b48c14 over those 287 characters, read by Tuesday). Nothing else of E-C1-3 or of any other text changes. Run your entry scan, doubled-group and repeated-run checks on the filled line again, then Step 6 and Step 7 as the kit says.

Tuesday's check, read in this answer's action: the two job logs fetched by `gh api -X GET --allow-escape-sequences`: merge commit job 139899767138 (2093718 bytes) holds 'failed to exit gracefully' on 0 lines; head job 139880765953 (2100886 bytes) on 1 line; control 'VERDICT: PASS' on 1 line of each.

Your stop is the system working: the drafter read the head log only, while the merge run was still in progress.
