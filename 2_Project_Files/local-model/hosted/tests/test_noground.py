"""tests for hosted/noground.py (2026-11-11). Fast by default; the checker controls (two --shared clones + the
api-gateway suite, ~6-10 min) run unless NOGROUND_SKIP_CHECKER=1.

Run: python3 -m unittest discover -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/tests -p 'test_noground.py' -v
"""
import json
import os
import shutil
import socket
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
HOSTED = os.path.dirname(HERE)
sys.path.insert(0, HOSTED)
import noground as ng  # noqa: E402
import replay as R  # noqa: E402

TIP = "fcd178ff34fa3b289baeb1c1fb6783161bec3e0d"
SPARK_2011 = os.path.join(R.LM, "runs", "spark_secuura_2026-11-11_ks_2011_o143_p1_api_gateway_redis_fallback_notification_settings_expire_after_the_redis_ttl")
FAKE_ISSUE = {"identifier": "KS-2011", "title": "api-gateway redis fallback: notification-settings Maps never pruned (fixture)",
              "priority": 4, "state": {"name": "Backlog"}, "assignee": {"name": "someone"},
              "description": "The two notification-settings Maps in the in-memory fallback are never pruned (fixture text).",
              "comments": {"nodes": [{"body": "second comment", "createdAt": "2026-11-02T00:00"}, {"body": "first comment", "createdAt": "2026-11-01T00:00"}]}}
TASK_2011 = {"id": "KS-2011", "tier": "rung", "rung": 5, "products": ["services/api-gateway/src/services/redis.ts"]}


def fake_response(content, provider="DeepInfra", reasoning="", cost=0.001):
    return json.dumps({"id": "gen-1", "provider": provider, "choices": [{"finish_reason": "stop", "message": {"content": content, "reasoning": reasoning}}],
                       "usage": {"prompt_tokens": 1000, "completion_tokens": 500, "cost": cost}}).encode()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ngtest_")
        self.patches = [mock.patch.object(ng, "NG_STATE", os.path.join(self.tmp, "state")),
                        mock.patch.object(ng, "NG_RUNS", os.path.join(self.tmp, "runs")),
                        mock.patch.object(ng, "NG_DONE", os.path.join(self.tmp, "done_noground.md")),
                        mock.patch.object(ng, "TASKS", os.path.join(self.tmp, "tasks.json")),
                        mock.patch.object(R, "WORK", os.path.join(self.tmp, "work"))]
        for p in self.patches:
            p.start()
        os.makedirs(os.path.join(self.tmp, "state", "inputs"))

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)   # the test's own temp dir only

    def write_task(self, d, task=TASK_2011):
        with open(ng.TASKS, "w") as f:
            json.dump({"tip": TIP, "tasks": [task]}, f)
        with open(os.path.join(ng.NG_STATE, "inputs", task["id"] + ".json"), "w") as f:
            json.dump(d, f, ensure_ascii=False)


class TestBuild(Base):
    def test_input_is_golden_free_and_byte_true(self):
        d = ng.build_one(TASK_2011, TIP, FAKE_ISSUE)
        ng.no_golden_proof(d)  # does not raise
        self.assertEqual(d["defect_line"], {"line": 0, "text": "", "sites": [], "expected_plus": [], "red_cells": []})
        self.assertTrue(d["ticket"]["description"].startswith(FAKE_ISSUE["description"]))
        self.assertLess(d["ticket"]["description"].index("first comment"), d["ticket"]["description"].index("second comment"))
        p = "Blockchain/Dev/services/api-gateway/src/services/redis.ts"
        self.assertEqual(d["files"][p], ng.show(TIP, p))  # byte-equal to the tip
        self.assertEqual(d["product_files"], [p])
        self.assertEqual(d["test_files"][0]["status"], "new")
        self.assertTrue(d["reference_test_file"].startswith("Blockchain/Dev/services/api-gateway/src/__tests__/"))
        self.assertEqual(d["files"][d["reference_test_file"]], ng.show(TIP, d["reference_test_file"]))
        self.assertNotIn("golden", json.dumps(d["files"]).lower()[:0])  # files are tip content only

    def test_golden_shaped_input_is_refused(self):
        d = ng.build_one(TASK_2011, TIP, FAKE_ISSUE)
        d["defect_line"]["expected_plus"] = ["x"]
        with self.assertRaises(R.Refused):
            ng.no_golden_proof(d)
        d = ng.build_one(TASK_2011, TIP, dict(FAKE_ISSUE, description="## The exact change\n```diff\n+x\n```"))
        with self.assertRaises(R.Refused):
            ng.no_golden_proof(d)

    def test_products_across_services_refused(self):
        with self.assertRaises(R.Refused):
            ng.build_one({"id": "KS-1", "tier": "rung", "products": ["services/api-gateway/src/services/redis.ts", "services/billing/src/index.ts"]}, TIP, FAKE_ISSUE)

    def test_excerpt_for_big_file_carries_cited_lines(self):
        body = "\n".join(f"line {i}" for i in range(1, 5001))
        e = ng.excerpt(body, "see big.ts:3000 and `line 4500 marker`", "x/big.ts")
        firsts = [(r["first_line"], r["last_line"]) for r in e["regions"]]
        self.assertEqual(firsts[0][0], 1)
        self.assertTrue(any(a <= 3000 <= b for a, b in firsts))
        for r in e["regions"]:
            self.assertEqual(r["text"].split("\n")[0], f"line {r['first_line']}")


class TestRun(Base):
    def setUp(self):
        super().setUp()
        self.d = ng.build_one(TASK_2011, TIP, FAKE_ISSUE)
        self.write_task(self.d)

    def test_routing_is_zdr_pinned_for_every_model(self):
        for mk in ("mimo", "glm", "v41"):
            body = R.build_body(mk, [{"role": "user", "content": "x"}])
            R.assert_routing(body, mk)
            self.assertEqual(body["provider"]["zdr"], True)
            self.assertEqual(body["provider"]["allow_fallbacks"], False)
            bad = json.loads(json.dumps(body)); del bad["provider"]["zdr"]
            calls = []
            with self.assertRaises(R.Refused):
                R.send(bad, mk, "k", R.Budget(os.path.join(self.tmp, "b.json"), 5), "t", 0.01, post=lambda *a: calls.append(a))
            self.assertEqual(calls, [])

    def test_dry_run_makes_no_network_call(self):
        def boom(*a, **k):
            raise AssertionError("network touched")
        with mock.patch.object(socket.socket, "connect", boom), mock.patch.object(R, "_http_post", boom):
            self.assertEqual(ng.main(["run", "--model", "mimo", "--dry-run"]), 0)

    def test_no_key_is_rc2_and_nothing_sent(self):
        calls = []
        with mock.patch.object(R, "read_key", return_value=None):
            self.assertEqual(ng.main(["run", "--model", "mimo"], post=lambda *a: calls.append(a)), 2)
        self.assertEqual(calls, [])

    def test_budget_cap_refuses_before_sending(self):
        calls = []
        with mock.patch.object(R, "read_key", return_value="k"), mock.patch.dict(os.environ, {"NOGROUND_BUDGET_USD": "0.0001"}):
            self.assertEqual(ng.main(["run", "--model", "glm", "--no-check"], post=lambda *a: calls.append(a)), 2)
        self.assertEqual(calls, [])

    def test_wrong_provider_served_is_harness_and_key_never_stored(self):
        with mock.patch.object(R, "read_key", return_value="sk-SECRET-test"):
            rc = ng.main(["run", "--model", "mimo", "--no-check"], post=lambda *a: fake_response("```diff\n```", provider="SomeoneElse"))
        self.assertEqual(rc, 5)
        done = open(ng.NG_DONE).read()
        self.assertIn("HARNESS", done)
        for root, _, files in os.walk(self.tmp):
            for f in files:
                self.assertNotIn("sk-SECRET-test", open(os.path.join(root, f), errors="replace").read())

    def test_missing_provider_is_harness(self):
        with mock.patch.object(R, "read_key", return_value="k"):
            rc = ng.main(["run", "--model", "v41", "--no-check"], post=lambda *a: fake_response("```diff\n```", provider=None))
        self.assertEqual(rc, 5)

    def test_resume_skips_a_real_verdict(self):
        ng.append_done(["2026-11-11 22:00:00", "mimo", "KS-2011", "rung", 5, 1, "FAIL", "x", 1, "1+1", 0, "0.001", "DeepInfra", "/r"])
        calls = []
        with mock.patch.object(R, "read_key", return_value="k"):
            ng.main(["run", "--model", "mimo", "--no-check"], post=lambda *a: calls.append(a) or fake_response("x"))
        self.assertEqual(calls, [])


@unittest.skipIf(os.environ.get("NOGROUND_SKIP_CHECKER") == "1", "checker controls skipped (NOGROUND_SKIP_CHECKER=1)")
class TestCheckerControls(Base):
    """The golden-free checker leg on a REAL fix: the Spark's own KS-2011 PASS (o143), judged with NO golden, no red
    cells, no '+' lines. Positive: its red cells relabelled with the red circle (the harness shape we tell the model)
    -> PASS 7/7. Negatives: product section dropped -> FAIL at A3; original titles (no red circle) -> FAIL at A4."""

    def setUp(self):
        super().setUp()
        self.out = open(os.path.join(SPARK_2011, "out.md"), encoding="utf-8").read()
        spark_in = json.load(open(os.path.join(SPARK_2011, "input.json"), encoding="utf-8"))
        d = ng.build_one(TASK_2011, TIP, FAKE_ISSUE)
        t = spark_in["test_files"][0]["path"]          # the test path the Spark's diff writes
        d["test_files"] = [{"path": t, "status": "new"}]; d["suggested_test_file"] = t
        self.d = d
        self.write_task(d)

    def _run(self, content):
        with mock.patch.object(R, "read_key", return_value="k"):
            rc = ng.main(["run", "--model", "mimo"], post=lambda *a: fake_response(content))
        row = [l for l in open(ng.NG_DONE).read().split("\n") if l.startswith("| 20")][-1]
        return rc, row

    def test_positive_real_fix_passes_with_no_golden(self):
        rc, row = self._run(self.out.replace("it('RED ks2011", "it('🔴 RED ks2011"))
        self.assertEqual(rc, 0, row)
        self.assertIn("| PASS |", row)

    def test_negative_product_dropped_fails_at_a3(self):
        body = self.out.replace("it('RED ks2011", "it('🔴 RED ks2011")
        start = body.index("diff --git a/Blockchain/Dev/services/api-gateway/src/services/redis.ts")
        end = body.index("diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/")
        rc, row = self._run(body[:start] + body[end:])
        run = row.strip().strip("|").split("|")[-1].strip()
        fails = [l for l in open(os.path.join(run, "checker.out"), errors="replace").read().split("\n") if l.startswith("FAIL")]
        self.assertEqual(rc, 1, row)
        self.assertIn("stopped at A3", row, fails)
        self.assertTrue(any("declared but UNTOUCHED" in l for l in fails), fails)
        print("NEGATIVE product-dropped checker FAIL lines:", fails[:3])

    def test_negative_red_cells_without_marker_fail_at_a4(self):
        rc, row = self._run(self.out)
        self.assertEqual(rc, 1, row)
        self.assertIn("A4", row)


if __name__ == "__main__":
    unittest.main()
