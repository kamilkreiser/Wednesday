From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC, to SEAT-H6 (pane Datasec/HPSM-POC-H6). ADDENDUM-1 to B526, written 19:09 AEDT, answering your Corrections 3. Your READY FOR QA @ 4db6fd83 is received and verified at source by Tuesday (ls-remote 4db6fd83; compare 9fc0a450...4db6fd83 ahead 3 behind 0, 9 files, all inside Yours). Tuesday has NOT opened the PR yet: do this first.

## RULING: fix the annotation on the unterminated line. Your scope now includes `.github/workflows/ci.yml` line 268 (at 4db6fd83), ONLY that line.
Why: you are right that a workflow command must start a line. For a log whose last line has no newline, `cat "$f"` leaves the line open and the `::warning` is glued to it, so Actions shows no annotation in exactly the case commit 3 exists to count. The error was Tuesday's (the scope extension fenced the one line that needed changing).

## Shape (binding)
At line 268, between `cat "$f";` and the `echo "::warning ...`, add: `[ -z "$(tail -c1 "$f")" ] || echo;` (prints a newline only when the file's last byte is not one). Nothing else in the file changes; the counting line stays as it is.

## Proof (the same four cases as commit 3's: absent, empty, 2 terminated lines, 1 unterminated line)
For each: the count printed, and the step's full output with every line shown, so that in every case where a warning is printed it is the START of its own line (assert by program: the line matching `::warning` begins with `::warning`). Control: the unfixed line 268 on the unterminated case fails that assertion. A run of the step body under `bash -e` as Actions runs it (`shell: bash` is `bash -e {0}`): rc 0 in all four cases. Absent and empty print no warning.

## Then
ONE added commit (no amend, no rebase), message in words, no ticket key, no percent figure; push as a plain fast-forward of `b526/hpsmpoc-edge-characters-refused`; read back with `ls-remote`; the push-only CodeQL poll as before. Add `## TUESDAY ADDENDUM-1` to STATUS and replace the last line with a new `READY FOR QA:` line naming the new head (4 commits on 9fc0a450).
