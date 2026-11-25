#!/usr/bin/env python3
"""QA-MEASURE-2 own per-run counter (independent of check_run.py). Prints counts only, never a command line or path.
usage: python3 -I -B qm2_counter.py <model-id> <log>...
Model: every token shaped like a Claude model id (claude-<family>-...) on ANY line, by line shape:
  dispatch (`dispatching to … model=`), other shapes listed by their fixed words; count of the read id vs any other id.
Hooks, own pattern: a command-hook execution line names its command in [..] or (..) next to an event name:
  "Hooks: <Ev>:<m> [cmd] …", "Hook <Ev> (cmd) …", "<Ev>:<m> [cmd] completed|finished|failed|timed out".
Hooks, catch-all: ANY line holding "hook" (any case) and any of status|returned|completed|finished|failed|timed out|
  spawn|exec|running|command, except the builtin module lines ("hooks module cc-plugin-…@builtin", "hooks modules not
  loaded", "hooks native host"), counted as foreign unless it names hook_stub.py or answer.py. Lines that carry no
  command at all ("Hook approved tool use…", "Hook result has…", "Successfully parsed…", "Hooks: Checking/Parsed/Initial…",
  quoted "Hook <Ev>:<tool> (<Ev>) success", "executePermissionRequestHooks called") are counted separately as NO-CMD."""
import re, sys, collections
sys.dont_write_bytecode = True
model = sys.argv[1]
MID = re.compile(r"\bclaude-[a-z]+-\d[-0-9a-z.]*")
OURS = ("hook_stub.py", "answer.py")
OWN = [re.compile(r"Hooks: (\w+):?\S* \[(.+?)\]"), re.compile(r"\bHook (\w+) \((.+?)\) (?:returned|failed|error|success|timed)"),
       re.compile(r"\] (\w+):\S* \[(.+?)\] (?:completed|finished|failed|timed out)")]
CATCH = re.compile(r"(?i)hook")
CATCHW = re.compile(r"(?i)status|returned|completed|finished|failed|timed out|spawn|exec|running|command")
BUILTIN = re.compile(r"hooks module cc-plugin-\S+@builtin|hooks modules not loaded|hooks native host|executePermissionRequestHooks called")
NOCMD = re.compile(r"Hook approved tool use|Hook result has|Successfully parsed and validated hook|Hooks: (?:Checking first line|Parsed initial|Initial response|checkForNewResponses)|\"Hook \w+:\S+ \(\w+\) success|Registered \d+ hooks|Loading hooks from plugin|Read hooks\.json|hook_registered|unhooked|edit_hook|ConfigChange hook blocked|resolved by hook|Hook PreToolUse:\S+ requires")
for log in sys.argv[2:]:
    shapes = collections.Counter(); same = other = 0; others = collections.Counter()
    own_ours = own_foreign = 0; c_lines = c_foreign = 0; nocmd = 0; unknown = collections.Counter()
    for line in open(log, encoding="utf-8", errors="replace"):
        ids = MID.findall(line)
        if ids:
            body = re.sub(r"^\S+ \[\w+\] ", "", line)
            shape = re.sub(r"\bclaude-[-0-9a-z.]+", "<MODEL>", re.sub(r"\d+", "N", body)).strip()[:70]
            shapes[shape] += 1
            for i in ids:
                if i == model: same += 1
                else: other += 1; others[i] += 1
        hit = False
        for rx in OWN:
            m = rx.search(line)
            if m:
                hit = True
                if any(o in m.group(2) for o in OURS): own_ours += 1
                else: own_foreign += 1
                break
        if re.search(r"\] \w+:\S* \[.+?\] (?:completed|finished|failed|timed out)", line) and not CATCH.search(line):
            c_lines += 1
            if not any(o in line for o in OURS): c_foreign += 1; unknown["(bracket shape) " + re.sub(r"\d+", "N", line.split("] ", 1)[-1])[:45]] += 1
        if CATCH.search(line) and not BUILTIN.search(line):
            if NOCMD.search(line): nocmd += 1
            elif CATCHW.search(line):
                c_lines += 1
                if not any(o in line for o in OURS): c_foreign += 1; unknown[re.sub(r"\d+", "N", line.split("] ", 1)[-1])[:60]] += 1
    print("== %s" % log.split("/m2-")[-1].split("/raw/")[-1])
    print("  model-id tokens: %s %d ; any other id %d %s" % (model, same, other, dict(others)))
    for s, n in shapes.most_common(): print("    shape x%d: %s" % (n, s))
    print("  hooks own pattern: ours %d foreign %d ; catch-all lines %d of which naming none of our stubs %d ; no-command hook lines %d" % (own_ours, own_foreign, c_lines, c_foreign, nocmd))
    for u, n in unknown.items(): print("    catch-all foreign shape x%d: %s" % (n, u))
