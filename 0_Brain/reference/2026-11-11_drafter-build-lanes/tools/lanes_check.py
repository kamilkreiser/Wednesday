import json, re, sys, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import excl
D = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_drafter-build-lanes/"
B = "Blockchain/Dev/"
A = [B+"scripts/typecheck-tests/baseline-originate.txt", B+"services/originate/tsconfig.test.json", B+"scripts/preflight/test-types-ratchet.sh",
     B+"scripts/__tests__/preflight_test_types_ratchet_leg.test.sh", B+"scripts/typecheck-tests/check.cjs",
     B+"scripts/prisma-generate.cjs", B+"scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh",
     B+"scripts/__tests__/ks1728_batch3_test_files_grade_without_a_closing_pipe.test.sh"]
A += [B+"scripts/__tests__/%s.test.sh" % n for n in ["check_no_latest_tags","docs_fragments","ks1347_proxy_out_dir_spaced_checkout","pre_push_hook_current_develop","preflight_deps","check_shared_relink_case","check_shared_relink_tooling_tokens","ks812_whatsapp_bot_default_api_target","pre_push_hook_base_fixture_guard","preflight_gateway_slot"]]
split = open(D+"evidence/deadhost_split.txt").read().split("\nFREE\n")[1].splitlines()
free = [l.split("\t")[0] for l in split]
keep = lambda p: not (p.endswith(".pyc") or "/USER_TESTING/" in p or p.startswith("USER_TESTING/") or "/tests/" in p or p.startswith("Blockchain/Testing") or p.startswith("Projects Documents") or "systemTest" in p or p.endswith("/scripts/generate-openapi.ts") or p.endswith("insurance-test-runner.js") or p.endswith("auth-matrix-smoke.sh") or p.endswith("ks812_whatsapp_bot_default_api_target.test.sh") or "TEST-REPORT" in p or p.endswith("monitor-log.md") or p.startswith("5_Project_History"))
# note: Group C's USER_TESTING/gmail-addon-code.js is re-added by name below
Bl = list(free)  # free paths are already repo-root relative as git printed them (some are at the repo root, e.g. .cursor/, USER_TESTING/)
Bl = [p for p in Bl if keep(p)]
Bl.append("USER_TESTING/gmail-addon-code.js")
Bl = [p for p in Bl if "Credentials" not in p and "CREDENTIALS" not in p and not p.endswith("CLI-AGENT-INSTRUCTIONS.md") and not p.endswith("docs/E2E-TESTING-PLAN.md")]
Bl = sorted(set(Bl)); Bl.append(B+"packages/shared/src/__tests__/ks1490-shipped-files-name-no-dead-container-apps-host.test.ts")
for sv in ["billing","kyc","referral","wallet-connector","guardian","queue"]:
    A += [B+"services/%s/tsconfig.test.json" % sv, B+"scripts/typecheck-tests/baseline-%s.txt" % sv]
json.dump({"A": A, "B": Bl}, open(D+"evidence/lane_files.json", "w"), indent=1)
print("A", len(A), "B", len(Bl))
for lane, fs in (("A", A), ("B", Bl)):
    for p in fs:
        r = excl.check(p)
        if r: print("EXCLUDED-HIT", lane, p, r)
print("A∩B:", sorted(set(A) & set(Bl)))
# path tokens from live seats' briefs
S = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/"
rx = re.compile(r'(?:Blockchain/Dev|systemTest|observability|Start_Up|\.githooks)/[A-Za-z0-9_./@{}-]+\.[A-Za-z0-9]+')
for name in ["2026-11-11_seatR95_raise.md","2026-11-11_R95_addendum_o135.md","2026-11-11_R95_addendum_o136.md","2026-11-11_R95_addendum_o137.md","2026-11-11_seatB133_merge.md","2026-11-11_seatS55_board.md","2026-11-11_seatU23_fix.md","2026-11-11_B133_answer_plan.md","2026-11-11_S55_answer_plan.md"]:
    toks = set(rx.findall(open(S+name, encoding="utf-8", errors="replace").read()))
    hit = sorted(t for t in toks if t in set(A) | set(Bl))
    print(name, "path tokens", len(toks), "lane-file hits", hit)
