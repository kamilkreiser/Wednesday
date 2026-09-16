#!/usr/bin/env python3
"""Render .claude/settings.template.json into .claude/settings.local.json.

WHY (2026-09-16): settings.local.json is gitignored, so the hooks and permission guards
never travelled between seats. Measured that morning: Wednesday's file was 1775 bytes with
six hooks and six permission rules; Tuesday's was 169 bytes — a statusline and nothing else.
She had been running with no PreCompact block and no PreToolUse guards, and nothing in
PORTABILITY.md or doctor.sh said so. The fix is not "copy the file" (it is per-machine and
carries each seat's own statusline); it is a TRACKED template plus this renderer, run by the
launcher at every boot.

WHAT IT PRESERVES: everything in the local file that the template does not name — `theme`,
`statusLine`, and any key a seat adds later. It replaces exactly `hooks` and `permissions`.

WHAT IT REFUSES: to write a file it cannot first parse, and to write when the result would be
identical (so a boot is quiet unless something actually changed).

Usage:
  render_claude_settings.py [--check] [--project-dir DIR]
    --check   report only; exit 1 if the rendered result would differ from what is on disk
Exit: 0 ok/unchanged · 1 would change (--check) · 2 error
"""
import json, os, sys, shutil, datetime

def die(msg, code=2):
    sys.stderr.write(f"render_claude_settings: {msg}\n")
    sys.exit(code)

args = sys.argv[1:]
check = "--check" in args
project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if "--project-dir" in args:
    project_dir = args[args.index("--project-dir") + 1]

tpl_path = os.path.join(project_dir, ".claude", "settings.template.json")
loc_path = os.path.join(project_dir, ".claude", "settings.local.json")

if not os.path.isfile(tpl_path):
    die(f"no template at {tpl_path} — nothing to render (is this a seat tree?)")

try:
    tpl = json.load(open(tpl_path, encoding="utf-8"))
except Exception as e:
    die(f"template is not valid JSON ({e}) — refusing to render from it")

# The workspace root is the VOLUME the seat's tree sits on: /Volumes/DevMASTER/WEDNESDAY ->
# /Volumes/DevMASTER. Derived, never hardcoded — Tuesday's tree is on another volume entirely,
# and a hardcoded path is the travel-pointer defect (2026-08-25).
parts = project_dir.rstrip("/").split("/")
workspace = "/".join(parts[:3]) if len(parts) > 3 and parts[1] == "Volumes" else os.path.dirname(project_dir)

def subst(x):
    if isinstance(x, str):
        return x.replace("@WORKSPACE@", workspace)
    if isinstance(x, list):
        return [subst(i) for i in x]
    if isinstance(x, dict):
        return {k: subst(v) for k, v in x.items()}
    return x

local = {}
if os.path.isfile(loc_path):
    try:
        local = json.load(open(loc_path, encoding="utf-8"))
    except Exception as e:
        # Never silently overwrite something we could not read — that would destroy a seat's
        # statusline on a stray comma (2026-08-26: never delete; a clobber is a delete).
        die(f"{loc_path} exists but is not valid JSON ({e}) — refusing to overwrite it. "
            f"Fix or move it aside, then re-run.")

merged = dict(local)
for key in ("hooks", "permissions"):
    if key in tpl:
        merged[key] = subst(tpl[key])

before = json.dumps(local, indent=2, sort_keys=True)
after = json.dumps(merged, indent=2, sort_keys=True)

def hookcount(d):
    n = 0
    for blocks in (d.get("hooks") or {}).values():
        for b in blocks:
            n += len(b.get("hooks", []))
    return n

if before == after:
    print(f"settings: already current ({hookcount(merged)} hooks, "
          f"{len((merged.get('permissions') or {}).get('ask') or [])} ask rules)")
    sys.exit(0)

if check:
    print(f"settings: WOULD CHANGE — on disk {hookcount(local)} hooks, "
          f"template gives {hookcount(merged)}")
    sys.exit(1)

if os.path.isfile(loc_path):
    shutil.copy2(loc_path, loc_path + ".pre-render-" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
os.makedirs(os.path.dirname(loc_path), exist_ok=True)
with open(loc_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2)
    f.write("\n")
print(f"settings: rendered — {hookcount(local)} hooks -> {hookcount(merged)}, "
      f"{len((merged.get('permissions') or {}).get('ask') or [])} ask rules, workspace {workspace}")
