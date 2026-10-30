import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spec_mcp import S as S0
S = dict(S0)
S['dir'] = 'ks_1410_p5_mcp_http_500_no_echo_rebrief'
S['title'] = S0['title'] + ' [REBRIEF 1 of 1]'
S['intro'] = S0['intro'] + " THIS IS THE ONE REBRIEF after round 1 FAILED at A2 (see below): same task, same golden, one added paragraph under `## The exact change`."
S['loose'] = S0['loose'] + ("**REBRIEF (round 1 failed A2):** your first diff wrote each hunk's new `res.status(500)...` line as an UNCHANGED context line (leading space) and never emitted the `-` line, so the old side of every hunk did not match the file. "
 "EVERY one of the nine hunks has exactly ONE `-` line (the old `res.status(500).json(...)` line, quoted under 'old lines you REMOVE') and exactly TWO `+` lines (the `console.error(...)` line, then the new `res.status(500).json(...)` line). A hunk with no `-` line is wrong. "
 "In the last hunk (POST /generate-package) the `console.error` `+` line goes directly after the `const message` line and BEFORE the unchanged `if (!res.headersSent) {` line; its `-`/`+` pair is the old and new `res.status(500)` line inside the `if`.\n\n")
