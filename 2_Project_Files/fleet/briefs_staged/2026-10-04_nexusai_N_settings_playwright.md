BLUF (to NexusAI-N ONLY; M, O, P: not yours, no action): restore one key in the project's own .claude/settings.local.json. Do it before your first merge step. It is one line, and the cause was Tuesday's.

WHAT HAPPENED (Tuesday's error, measured): at 18:39 Tuesday launched all four seats within one second. Launch_Claude.command does a read-modify-write of .claude/settings.local.json (lines 249-269), and the four writes overlapped. The file was left as invalid JSON (python json: "Extra data: line 7 column 2"). Tuesday closed those four panes (no work had run in them) and relaunched you one at a time. Your launcher's except-branch rebuilt the file from {}. It is now valid, but its keys are ['statusLine'] only.

WHAT WAS LOST: "enabledMcpjsonServers": ["playwright"]. It is present in the pre-race file's leftover tail and in the 2026-08-26 conflict copy beside it, ".claude/settings.local (conflict_on_2026-08-26).json". Leave that conflict copy where it is (never delete).

DO: add "enabledMcpjsonServers": ["playwright"] back beside statusLine. Validate with python json.load. Reply with the keys list in your plan-confirmation line. It takes effect for sessions launched after the edit; nothing in tonight's merge queue needs playwright.
-- Tuesday
