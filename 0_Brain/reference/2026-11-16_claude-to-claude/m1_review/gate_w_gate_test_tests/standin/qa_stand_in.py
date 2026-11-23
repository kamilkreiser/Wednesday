# QA-W-GATE-TEST copy of mac/stand_in_claude.py (head 3838bd5) with fault switches added (QA_FAULT, comma-separated):
#   madefile  : make CANARY.txt even when a hook blocked (a host that blocks in words but writes)
#   noerr     : report blocked tool results with is_error false
#   wrongmode : report permissionMode bypassPermissions always
#   nohook    : run no hook at all (same as W1_STANDIN_IGNORE_HOOKS)
#   bashlist  : add Bash to the tool list after --tools is applied
#   chsettings: change $HOME/.claude/settings.json during the run (the owner's settings changed)
#   monitorlist: add Monitor to the tool list
#   bashlater : add Bash from the SECOND run on (marker file $QA_MARK)
#!/usr/bin/env python3
"""A STAND-IN FOR CLAUDE CODE, for the Mac only. It is NOT Claude Code and calls NO model.

It exists so that `w1.py run-set` (process start and kill, the mid-call kill, the hook timeout, the raw files, the judge)
can run end to end on this Mac against the REAL `coagent-hook` and the REAL `w1-stub`, with zero model runs. It proves
only the runner's plumbing. Everything W1 is about (how Claude Code on Windows runs an exec-form hook, honours exit 2 and a
deny, applies `onFailure`, kills a timed-out hook) is exactly what this file does NOT show: it behaves as G1 and G2
observed Claude Code 2.1.325 behave on macOS, and its error texts are copied from those spikes' raw streams
(`spikes/G1-deny-blocks-write/raw/*-deny.stream.jsonl`, `spikes/G2-dead-daemon-blocks/raw/*-onfailure-block.stream.jsonl`).

Accepts the argument shape `w1.py run-set` passes: -p <prompt> --model M --output-format stream-json --verbose
--strict-mcp-config --permission-mode manual|bypassPermissions [--allowedTools T] [--settings F]. Writes stream-json to
stdout. The tool list of its first event is $W1_STANDIN_TOOLS (comma-separated; default Bash,PowerShell,Read,Write),
or exactly the --tools list when one is given.
RED CONTROL: W1_STANDIN_IGNORE_HOOKS=1 makes it run no hook at all (a host that lets every call through).
"""
import json, os, subprocess, sys
QF=set((os.environ.get("QA_FAULT") or "").split(","))


def arg(name):
    a = sys.argv[1:]
    return a[a.index(name) + 1] if name in a else None


def emit(o):
    sys.stdout.write(json.dumps(o) + "\n")
    sys.stdout.flush()


prompt, mode_flag = arg("-p") or "", arg("--permission-mode") or "manual"
mode = "default" if mode_flag == "manual" else mode_flag
if "wrongmode" in QF: mode = "bypassPermissions"
if "chsettings" in QF:
    _p=os.path.join(os.environ["HOME"],".claude","settings.json"); open(_p,"a").write(" ")
tools = (os.environ.get("W1_STANDIN_TOOLS") or "Bash,PowerShell,Read,Write").split(",")
if arg("--tools") is not None and os.environ.get("W1_STANDIN_IGNORE_TOOLS") != "1":   # RED CONTROL switch; as Claude Code's --tools: the session lists only these built-in tools
    tools = [t for t in arg("--tools").split(",") if t]
if "bashlist" in QF: tools = ["Bash"] + tools
if "monitorlist" in QF: tools = tools + ["Monitor"]
if "bashlater" in QF:
    _m = os.environ["QA_MARK"]
    if os.path.exists(_m): tools = ["Bash"] + tools
    else: open(_m, "w").write("1")
tool = "PowerShell" if "PowerShell tool" in prompt else "Write"
cwd = os.getcwd()
tin = {"command": "Set-Content -Path CANARY.txt -Value canary"} if tool == "PowerShell" else \
      {"file_path": os.path.join(cwd, "CANARY.txt"), "content": "canary"}
emit({"type": "system", "subtype": "init", "cwd": cwd, "tools": tools, "model": arg("--model"),
      "permissionMode": mode, "claude_code_version": "stand-in (NOT Claude Code)"})
once = os.environ.get("W1_STANDIN_VOID_ONCE")   # TEST ONLY: the first run issues no tool call (a void case)
if once and not os.path.exists(once):
    open(once, "w").write("1")
    emit({"type": "result", "subtype": "success", "is_error": False, "num_turns": 1, "result": "no tool used"})
    sys.exit(0)
emit({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "toolu_standin", "name": tool, "input": tin}]}})

event = {"session_id": "stand-in", "cwd": cwd, "permission_mode": mode, "hook_event_name": "PreToolUse",
         "tool_name": tool, "tool_input": tin, "tool_use_id": "toolu_standin"}
blocked, allowed_by_hook = None, False
settings = json.load(open(arg("--settings"))) if arg("--settings") else {}
if os.environ.get("W1_STANDIN_IGNORE_HOOKS") == "1" or "nohook" in QF:   # RED CONTROL ONLY: a host that fails open on every hook
    settings = {}
for entry in settings.get("hooks", {}).get("PreToolUse", []):
    if entry.get("matcher") not in ("*", tool):
        continue
    for h in entry.get("hooks", []):
        argv = [h["command"]] + list(h.get("args", []))
        label = "PreToolUse:%s hook error: [%s]" % (tool, " ".join(argv))
        failure = None
        try:
            p = subprocess.run(argv, input=json.dumps(event).encode(), capture_output=True, timeout=h.get("timeout", 600))
        except subprocess.TimeoutExpired:
            failure = "timed out"
        except OSError:
            failure = "failed"
        else:
            out = p.stdout.decode("utf-8", "replace").strip()
            if p.returncode == 0 and out:
                hso = json.loads(out).get("hookSpecificOutput", {})
                if hso.get("permissionDecision") == "deny":
                    blocked = "PreToolUse:%s hook error: %s" % (tool, hso.get("permissionDecisionReason", ""))
                elif hso.get("permissionDecision") == "allow":
                    allowed_by_hook = True
            elif p.returncode == 2:
                blocked = "%s: %s" % (label, p.stderr.decode("utf-8", "replace").strip())
            elif p.returncode != 0:
                failure = "failed"
        if failure and h.get("onFailure") == "block":
            blocked = '%s: %s; blocking because onFailure is "block"' % (label, failure)
        if blocked:
            break
    if blocked:
        break

if blocked:
    result, err = blocked, ("noerr" not in QF)
    if "madefile" in QF: open(os.path.join(cwd, "CANARY.txt"), "w").write("canary\n")
elif mode == "bypassPermissions" or allowed_by_hook or tool in (arg("--allowedTools") or "").split():
    open(os.path.join(cwd, "CANARY.txt"), "w").write("canary\n")
    result, err = "File created successfully (stand-in)", False
else:
    result, err = "This command requires approval (stand-in)", True
emit({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "toolu_standin", "is_error": err,
                                               "content": result}]}})
emit({"type": "result", "subtype": "success", "is_error": False, "num_turns": 2, "result": "REFUSED" if err else "done"})
