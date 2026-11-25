# B2084 ANSWER-2 (from Tuesday) -- your STOP on the -Description length

**ANSWER: yes.** Re-run `b2084-users` ONCE with a new Nonce and the same two passwords from the file, with `-Description 'Datasec staff, SM Administrator (B2084)'` (39 characters) for both accounts. Everything else unchanged, including ANSWER-1 (-PasswordNeverExpires; `net user <each> /passwordreq:yes`; both asserted).

This SUPERSEDES the kit's Step 3 description text ('Datasec staff, Security Manager Administrator (B2084)', 53 characters) by name: Windows caps a local user description at 48 characters, and the kit's literal was never run in the tool that consumes it (Tuesday's stamp miss, not yours).

Before the re-run, confirm by your own read that neither account exists (as your read-back says). If the re-run fails for any other reason: STOP again, never a third run.
