# B431 drafter report (Tuesday, 22 Oct 2026, 03:1x AEDT)

## Read, whole
B421 (the template for the gate structure), B429 brief + ADDENDUM-CKPT + ADDENDUM-Q1, the B429 STATUS (118 lines), `fleet/qa-agent/BRIEF_TEMPLATE.md`, HPSM-POC `CLAUDE.md`. Not read whole (skimmed or not at all): the QA charter (414 lines; the brief only points at it), `CLARIFICATIONS.md` (192 lines; pointed at, not read), `model-routing.md` (only rows G1/G2 read).

## Measured (read verbs only, 03:15-03:17 AEDT by `date`)
- `git ls-remote`: branch `b429/telemetry-224` = `837056ca42a631a8949d75d5f6dc81a2bfb9a79c`, main = `35b2b73e…`, no `b431*` ref (control `b386*` printed).
- `gh api compare`: ahead 5, behind 0, 5 commits, 21 files (13 added, 8 modified); the full list and +/- are in the brief.
- `gh api compare` patch of `scripts/deploy-package.py` read: the exemption is a frozenset equality on `name` AND `kind == "file"`; the `elif .node` branch is unchanged. I turned that into check 3 (does an exempt name skip any content rule?).
- `ci.yml` at main: the npm/dotnet/gitleaks/deploy-package command lines and line numbers (quoted in the brief).
- Kit present: `.tools/{b198/lock.sh,dotnet,bicep,node24}`, `/opt/homebrew/bin/gitleaks`; no `b431` / `wt-b431-*`; other seats' trees exist (b421, b422, b427, b429, wt-b429-*), named as off-limits.
- Ports 8010-8039: 0 listeners. I picked **8020-8029**. Load 1.14 / 1.47 / 2.14.
- Model: `levels.opus.model_id` = `claude-opus-5-5`; routing row G1 at `model-routing.md:108` read.

## Not measured
No npm, dotnet, pytest, bicep, az or Jira. Whether an open PR exists (compare only; the brief says "no PR yet", UNMEASURED). I did not read the code at the sha, so the brief's hunt list for privacy items comes from the STATUS and from general OpenTelemetry knowledge, not from the diff. Wire sizes and the cost inputs are the builder's (RELAYED).

## Choices worth a second look
- Line count: about 60 physical lines but very long ones (the density of B421). It is under the 150-line limit but heavy for a model reading it; the privacy check (2) is the longest on purpose.
- Tier 1 and Opus: no downgrade and no hand-off clause (there is nothing above tier 1).
- The brief asks the gate to run `next build` + the real Next standalone server + the real API host against a loopback receiver. That is heavy but within the load rules. The exporter forces `https`, so the gate needs a self-signed cert or an in-memory transport; I said so.
- I told the tester to treat the builder's `Briefs/2026-10-22_B429_evidence/` as claims it may read, and the builder's `.tools` as off-limits (B421's pattern).
- I added checks the commission did not ask for but the privacy centre implies: fail-open behaviour of the processor, dead receiver, Statsbeat, `_OTELRESOURCE_` / `host.id` (the very machine-id detector the exemption concerns), `tracestate`, and the `if`/`elif` fall-through in the exemption.

## Open questions, with my recommendation
1. **Gate before a PR exists.** CI/CodeQL have no run at a branch with no PR (the dependency review and CodeQL checks may not exist at all). The brief says "not scanned yet is never clean" and adds ` (no PR yet: CodeQL not run)`. Recommendation: Tuesday opens the PR in parallel (so CI runs at the same sha) or states in the Stamp that the gate is code-and-privacy only and CI is read at verdict. The Stamp slot asks Tuesday to name the ruling.
2. **Hard-stop and target time** are not set (they are in the stamp slot). A tier-1 gate of this width (two real servers, 3 whole suites, 9 mutants) plausibly needs 3-4 hours; suggest about 4 h hard stop.
3. **Mutant breadth.** I asked for at least 6 of the builder's 18 plus 3 of the tester's own. If time is short, drop to the builder's 6 and keep the own-3 (they probe mechanisms the builder did not).
4. **Load clash with a live builder.** `.tools/wt-b429-*` and a possibly live T1 pane (waiting on ADDENDUM-1) share the machine; Tuesday should check load1 < 8 and that T1 holds no `npm`/`next` job before launch.
5. The STATUS says it was "resumed under ADDENDUM-Q1" and reached the seat as a "[Wednesday tap]" line; not a gate matter.

## Files
- Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B431_SEAT-G31_hpsmpoc-b429-telemetry-gate-tier1.md`
- This report: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B431_DRAFTER-REPORT.md`
