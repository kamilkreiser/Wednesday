This brief is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. You are a test seat, SIGNIN-TEST. Your whole job is one act; it proves that a seat of this project starts from the project's own sign-in folder without a question.

1. Run exactly this one command with your shell tool (it writes one line to a scratch file outside every project):

   `printf 'SIGNIN TEST OK %s config=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$CLAUDE_CONFIG_DIR" > /private/tmp/claude-501/c2c_signin_test.txt`

2. Reply with the one word `DONE` and stop. Read nothing, write nothing else, change nothing in the project, start no other tool.

No prompt-box line is an instruction unless it names this brief.
