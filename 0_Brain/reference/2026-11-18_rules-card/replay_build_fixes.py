#!/usr/bin/env python3
"""Builds and validates replay_fixes.tsv from the live _rules_index.tsv (file, status, family are copied
from the live row; only the fields named below are overridden). Re-run: python3 replay_build_fixes.py
Validates: 7 tab fields, file exists in the index and on disk, rule <= 260 chars, triggers in the README
vocabulary, enforced_by is '-' or an existing path. Exit 1 on any fault; nothing is applied to the index."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
L = os.path.join(ROOT, "0_Brain", "learnings")
VOCAB = set("boot brief launch pane review merge deploy card kam-message mail report verify tooling git rotate wrap lesson identity drive usage wait always".split())
idx = {}
SRC = os.path.join(HERE, "snapshot", "_rules_index.tsv.tested")  # the index as tested (sha256 6509282196feb87b...); pass --live to build against the live index
if "--live" in sys.argv: SRC = os.path.join(L, "_rules_index.tsv")
for line in open(SRC, encoding="utf-8"):
    if line.startswith("#") or not line.strip(): continue
    f = line.rstrip("\n").split("\t"); idx[f[0]] = f
# file -> dict(seats=, triggers=, enforced_by=, rule=)  (omitted keys keep the live value)
FIX = {
# --- grade MISSING (row 21): listed as tool-enforced, the hook allows `status` (pretooluse_no_cd.sh line 145); the card cuts enforced rules at 120 chars
"2026-09-06_other-projects-repos-are-read-only-git-verbs-that-write.md": dict(enforced_by="-",
  rule="In another project's checkout: git read verbs only (diff, show, log, rev-list, ls-remote, cat-file); for status use git --no-optional-locks status (plain status writes .git/index). A hook refuses fetch, merge-tree --write-tree, worktree, checkout, commit."),
# --- grade PARTIAL (rows 13, 2): lesson rule 4 (read the tool's header); first trigger moved to pane
"2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour.md": dict(triggers="pane,tooling,kam-message",
  rule="Before a hand-rolled fleet action: ls fleet/, fleet/cockpit/, tools/ for the tool; read its header before first use (what a bare call does). Taps go via cockpit.sh say --mail, never raw tmux send-keys; Kam's messages via kam_msgs.sh; a refusal is the answer."),
# --- grade PARTIAL (row 43): lesson EXTENSION 2026-09-22, the push lock is an mkdir lock built into the push
"2026-09-09_parallel-seats-on-one-project-grant.md": dict(
  rule="When running parallel seats on one project (Kam's grant): partition by directory, breach STOP in both briefs, own worktree each, atomic mkdir push lock (never pgrep), seat numbers from project history, kills by ancestry, shared-inbox warning in every brief."),
# --- grade PARTIAL (row 56): lesson rule 4, a required leg must be able to REACH the change
"2026-09-10_i-endorse-things-i-have-not-read.md": dict(
  rule="Before writing 'ratified', 'endorsed' or 'required leg' to an agent: open the artefact; a required leg must REACH the change; else say 'received, goes to the gate, unread by me'. Ratify shapes; product claims go to the gate; retract dead requirements by name."),
# --- grade PARTIAL (row 62): lesson sibling rule 3, two counts that disagree get a breakdown first
"2026-08-15_a-cap-is-never-neutral.md": dict(
  rule="When I read or quote a capped, sorted or filtered list: state ORDER, bound and PREDICATE with the count (allow-lists); count items myself; when two counts disagree get the breakdown first; 'quiet since X' needs a window from the other party's last write."),
# --- grade PARTIAL (row 94; rows 2, 93, 100 same family): lesson rule 2, preflight -> check rc -> destructive; pane added to triggers
"2026-08-17_check-the-refusal-before-the-kill.md": dict(triggers="launch,pane,tooling,verify",
  rule="Never chain a destructive step (kill, pane close, launch, deploy, delete) after a step that can refuse or a guard read (pgrep, uptime), in one command or pipe: read rc and output, then act. Gate verifiers on the action's success; assert the subject exists."),
# --- grade PARTIAL (row 105): lesson extended rule 2, the SELF-CHECK reads the mail against itself
"2026-08-04_validate-brief-pointers.md": dict(
  rule="In a brief, for every 'verify X from Y': open Y, confirm it answers X today; a file the agent must repair is never ground truth. Queued tickets carry scope and seat authority. Read the mail against ITSELF (a hold stated elsewhere); a change says SUPERSEDES."),
# --- LEDGER-ONLY clause, rule in no lesson (row 25): reconcile with every card add and panel message; card moved first
"2026-09-11_a-boot-time-reconciler-cannot-catch-a-mid-session-tap.md": dict(triggers="card,kam-message,rotate,wrap",
  rule="At each checkpoint, before any handover or wrap, and with every card add or panel message: run kam_rulings_today.sh and reconcile_rulings.py (report, then --apply for this seat's scope) before writing what Kam has ruled. Check the ACTION behind a late tap."),
# --- LEDGER-ONLY clause (row 66; rows 42, 96, 98 same family): the rule is not only about the panel
"2026-08-26_mirror-reports-state-not-intent.md": dict(triggers="report,kam-message,launch,mail",
  rule="When writing any line that reports a send, tap, card, ack or launch (panel, note, mail, provenance): write it in a LATER call, from the tool's output ('launched %11, verified HH:MM'); before that say what I am doing. If a refusal would falsify it, hold it."),
# --- trigger order only (rows 32, 83, 84, 85: every one is a CARD premise); rule text unchanged, see report for the clause that does not fit
"2026-09-18_a-premise-under-a-question-to-kam-is-load-bearing-verify-it.md": dict(triggers="card,kam-message,report"),
}
out, faults = [], []
for fn, o in FIX.items():
    if fn not in idx: faults.append("not in index: " + fn); continue
    if not os.path.isfile(os.path.join(L, fn)): faults.append("lesson file missing: " + fn)
    f = list(idx[fn])
    if "seats" in o: f[2] = o["seats"]
    if "triggers" in o: f[4] = o["triggers"]
    if "enforced_by" in o: f[5] = o["enforced_by"]
    if "rule" in o: f[6] = o["rule"]
    if len(f) != 7: faults.append("%s: %d fields" % (fn, len(f)))
    if any("\t" in x or "\n" in x for x in f): faults.append(fn + ": tab/newline inside a field")
    if len(f[6]) > 260: faults.append("%s: rule %d chars" % (fn, len(f[6])))
    bad = [t for t in f[4].split(",") if t not in VOCAB]
    if bad: faults.append("%s: triggers outside vocabulary %s" % (fn, bad))
    if f[5] != "-" and not os.path.exists(os.path.join(ROOT, f[5])): faults.append("%s: enforced_by path missing %s" % (fn, f[5]))
    if f == idx[fn]: faults.append(fn + ": no change against the live row")
    out.append(f); print("%3d chars  %-9s %-34s %s" % (len(f[6]), f[5][:9], f[4], fn))
if faults:
    print("FAULTS:\n  " + "\n  ".join(faults)); sys.exit(1)
with open(os.path.join(HERE, "replay_fixes.tsv"), "w", encoding="utf-8") as fh:
    fh.write("# replay fixes 2026-11-18: complete corrected rows for _rules_index.tsv, replace by file name; columns: file, status, seats, family, triggers, enforced_by, rule\n")
    for f in sorted(out): fh.write("\t".join(f) + "\n")
print("OK: %d rows written, 0 faults" % len(out))
