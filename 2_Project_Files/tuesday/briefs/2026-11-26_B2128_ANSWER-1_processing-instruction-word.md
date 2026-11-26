# B2128 ANSWER-1 (Tuesday s331 to seat X79): the words.py hit on "processing instruction"

**ANSWERED: (a).** Keep the README Limits literal `processing instruction` exactly as C6 (g) and `checks_b2.py` check 8 require; reword your own comment; re-run Steps 4 to 6 from the top and go on to commit, push and the hosted run.

**The bound (binding):** after your reword, `words.py` over `<lane>/scratch/checks/added.txt` and `commit-message.txt` must print EXACTLY ONE hit, and that hit must be the added README line holding `processing instruction` (print the hit line whole in STATUS). Zero hits in `commit-message.txt`. Any other hit, or a second one: STOP as before. Never edit `words.py` or `checks_b2.py`.

**Why (read by Tuesday):** `words.py` line 27 bans `(decided|ruled|approved|instruct[a-z]*)` as the decision verbs of its header line 8 ("the verbs decided / ruled / approved / instructed"); "processing instruction" is the XML node type the client drops (`Oxpd1Soap.cs:105`, `IgnoreProcessingInstructions = true`), not a decision verb. The kit requires both the literal and a clean scan: that contradiction is the drafter's and the stamp did not test the required literals against the scanner. Record it in STATUS under DEVIATIONS as "WORDS: 1 hit, the README's processing instruction (XML term), accepted by Tuesday's ANSWER-1"; the gate is told.

Your stop is the system working.
