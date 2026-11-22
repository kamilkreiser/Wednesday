import sys
sys.path.insert(0, sys.argv[1] + "/build/tests")
import test_pipeline_controls as t
for tree in sys.argv[1:]:
    w = open(tree + "/.github/workflows/ci.yml", encoding="utf-8").read()
    print(tree.rsplit("/",1)[-1], "scan", t.job_sha256(w, "secret-scan") == t.REVIEWED_SCAN_JOB, "rules", t.job_sha256(w, "rules") == t.REVIEWED_RULES_JOB, "whole", t.workflow_sha256(w) == t.REVIEWED_WORKFLOW, "floors", t.floors(w))
    c = w.replace("persist-credentials", "persist-credentialz", 1)
    print("  control one-letter edit: whole", t.workflow_sha256(c) == t.REVIEWED_WORKFLOW)
