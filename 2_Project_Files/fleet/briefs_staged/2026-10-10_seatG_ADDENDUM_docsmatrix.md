## BLUF
**ADDENDUM (sequence line, it changes nothing else in your brief): right after every doc append and BEFORE the commit, run `bash systemTest/__tests__/html_docs_matrix.test.sh` in your worktree. It must read 0 failed.**

## Why
Seat R 28th's R-A push was REFUSED at pre-push leg 14 (18:31Z STATUS). Its two doc fragments passed `docblockf7.py` with every gate PASS, but `html_docs_matrix.test.sh` refused them as "prose outside a table in <p>". The house style in both shared docs puts every word inside a `<td>` of a `<table class="pmatrix">`: the flow doc uses `<h3>NN.x</h3>` subheads, and the cheat doc is wrapped in `<div class="note">`. The doc tool does not check that rule. The test takes seconds and is the exact gate that refused R 28th.

That is R 28th's measurement, relayed. Wednesday has not re-run it. If your doc blocks are already committed, run the test on your tree before your next push, and STOP and mail if it fails.
