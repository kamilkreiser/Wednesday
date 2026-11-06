From Tuesday, Datasec / NexusAI, to seat N104 (B1340). ADDENDUM-4. This adds one step to your kit and SUPERSEDES its "push the NEW branch once" for this one case.

What changed: PR #178 (the route-capability inventory) landed on main ahead of you: main is 993be21a4448b8cda473c991f7763ba5e119fa31. It moved scripts/verify-expected-counts.json. Tuesday chose this order because your branch has no gate yet, so a re-merge costs you one verify and no repeat gate. Read your kit's counts lines against that blob yourself.

Finish your current ticket and your three commits exactly as your kit says, then, before READY:
1. Fetch origin main. ONE merge of origin/main into your branch, as a merge commit. If the counts file is the only conflict, resolve it through one --update-counts run and assert the arithmetic: main's pair plus exactly what your new test files add. Any conflict in any other file: STOPPED: NEEDS TUESDAY, with the file names.
2. One plain verify at the new head, through the jest lock. No tag of yours may contain the word merge: the lock tool places such a tag ahead of waiting builders, and you wait in the FIFO.
3. One forward push of the same branch, no force. If you have already pushed your three commits, this is your second and last push. No PR.
4. Your READY line names the new head and the pair, and STATUS says both the pair before the merge and after it.

A gate is queued behind you on the jest lock (tags b1358-gate-*); that is not a finding. Your hard stop stays 02:30:00; if this step would miss it, say so in your last line by 02:15 and Tuesday moves it. No other change to scope.
