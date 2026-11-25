# B2084 ANSWER-1 (from Tuesday) -- your STOP on password expiry

Your question: no -PasswordNeverExpires (a: expire after 42 days) or -PasswordNeverExpires (b: match the existing users)?

**ANSWER: (b), with one addition. This SUPERSEDES the kit's Step 3 line "do NOT pass -PasswordNeverExpires (the machine's own expiry policy applies, as for the existing users)": its premise ("as for the existing users") was false, as your live read showed; the kit's instruction is withdrawn by name.**

1. Create both accounts with `-PasswordNeverExpires` (as the three existing enabled accounts read "Password expires Never").
   Tuesday's reasons (Tuesday's decision, not the product owner's): NLA is ON (your read, UserAuthentication=1), so an expired password would block the Bastion sign-in with no screen to change it, and each person would be locked out until a seat resets it; a 20-character random password gains nothing from forced periodic expiry; the 10-try lockout covers guessing on the open port; and it matches the product owner's and the other administrator's logins.
2. **Addition:** after creating each account, make it require a password: `Set-LocalUser -Name <each> -PasswordNeverExpires $true` is already covered by the New-LocalUser switch; ALSO run `net user <each> /passwordreq:yes`, and extend the script's ASSERT: both new accounts read `PasswordRequired True` and `PasswordExpires` empty (never). Do NOT touch the existing accounts' PasswordRequired=False (your FOUND 3): report only, as you did.
3. Everything else in the kit stands: Step 4 A is now allowed (your IDENTITY table reads CAN INVITE yes, CAN ASSIGN READER yes, and the STAMP carries both addresses); the sign-in note keeps "change the password at first sign-in" (Ctrl+Alt+End), and does NOT mention an expiry date.
4. Use the correct NLA key path in your records (your FOUND 2); no action on it.
