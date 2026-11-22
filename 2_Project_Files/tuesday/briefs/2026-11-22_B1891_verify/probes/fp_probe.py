import sys
sys.path.insert(0, sys.argv[1] + "/build/tests")
import test_pipeline_controls as t
w = open(t.WORKFLOW, encoding="utf-8", newline="").read()
for label, x in {"FLOOR=084": w.replace("FLOOR=108", "FLOOR=084"), "FLOOR=0": w.replace("FLOOR=108", "FLOOR=0"),
                 "BOM added": "﻿" + w, "final newline dropped": w[:-1], "NBSP for a space": w.replace("name: ci", "name: ci", 1)}.items():
    print("%-22s whole-file moved %-5s floors %s" % (label, t.workflow_sha256(x) != t.REVIEWED_WORKFLOW, t.floors(x)))
