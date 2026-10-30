TASK: test_only_typefix

The INPUT is a JSON object with `brief` (the full written brief: read it first and execute it exactly) and `files` (the FULL current content of every file you may change, keyed by repo-relative path).
Produce the change the brief specifies as ONE unified diff against those files, and nothing else. The `+` lines are given byte-exact in the brief; copy them. Context lines are copied from `files`. Touch only the edits the brief names.
