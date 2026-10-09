#!/usr/bin/env python3
"""Tests for hosted/replay.py — run: python3 -m unittest discover -s <hosted>/tests -v

Every test writes only into a temp dir (HOSTED_TEST_TMP, else the system temp dir). No test reaches OpenRouter:
the network function is replaced by a fake, and the dry-run test blocks the socket layer outright.
The checker positive control (CheckerControl) clones the Spark cache at a recorded tip and runs the real checker;
skip it with HOSTED_SKIP_CHECKER=1.
"""
import email.message
import io
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from contextlib import redirect_stdout

HOSTED = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HOSTED)
import replay  # noqa: E402

RUNS = os.path.join(replay.LM, "runs")
# three real Spark inputs, one per prompt path: code_patch (tasks/code_patch/task.md), bash_patch, code_patch2 (run-dir task.md)
REAL = {
    "code_patch": os.path.join(RUNS, "spark_secuura_2026-10-05_KS-723-anchors-tx"),
    "bash_patch": os.path.join(RUNS, "spark_secuura_2026-10-09_KS-998-format-gate-npm-stdin"),
    "code_patch2": os.path.join(RUNS, "spark_secuura_2026-10-07_KS-1410-apigw-batch-audit-export-500"),
}
FAKE_KEY = "sk-or-TEST-not-a-real-key-0000"


def tmpdir():
    return tempfile.mkdtemp(prefix="hosted_t_", dir=os.environ.get("HOSTED_TEST_TMP") or None)


def rbytes(path):
    with open(path, "rb") as f:
        return f.read()


def fake_response(cost=None, pt=20000, ct=1000, provider="DeepInfra", content="```diff\n--- a/x\n+++ b/x\n```"):
    usage = {"prompt_tokens": pt, "completion_tokens": ct, "total_tokens": pt + ct}
    if cost is not None:
        usage["cost"] = cost
    return json.dumps({"id": "gen-fake", "provider": provider, "model": "m",
                       "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": content}}],
                       "usage": usage}).encode()


class FakePost:
    def __init__(self, responses):
        self.responses, self.calls = list(responses), []

    def __call__(self, url, data, headers, timeout):
        self.calls.append((url, json.loads(data)))
        return self.responses.pop(0)


class Isolated(unittest.TestCase):
    """Points replay's state/runs/work/done/env at a temp dir."""

    def setUp(self):
        self.t = tmpdir()
        self.saved = {k: getattr(replay, k) for k in ("STATE", "RUNS", "WORK", "DONE_DIR", "ENV_FILE")}
        replay.STATE, replay.RUNS, replay.WORK, replay.DONE_DIR = (os.path.join(self.t, x) for x in ("state", "runs", "work", "done"))
        os.makedirs(replay.DONE_DIR)
        replay.ENV_FILE = os.path.join(self.t, "absent.env")
        self.saved_cap = os.environ.pop("HOSTED_BUDGET_USD", None)

    def tearDown(self):
        for k, v in self.saved.items():
            setattr(replay, k, v)
        if self.saved_cap is not None:
            os.environ["HOSTED_BUDGET_USD"] = self.saved_cap
        else:
            os.environ.pop("HOSTED_BUDGET_USD", None)
        shutil.rmtree(self.t, ignore_errors=True)

    def with_key(self):
        replay.ENV_FILE = os.path.join(self.t, "test.env")
        replay._wtext(replay.ENV_FILE, f"# test\nOTHER=1\nexport {replay.KEY_NAME}=\"{FAKE_KEY}\"\n")


# ------------------------------------------------------------------------------------------------ 1. routing
class Routing(Isolated):
    def body(self, mk="deepseek"):
        msgs, _ = replay.build_messages(REAL["code_patch"])
        return replay.build_body(mk, msgs)

    def test_green_every_model_carries_all_four_fields(self):
        for mk in replay.MODELS:
            b = self.body(mk)
            replay.assert_routing(b, mk)  # no raise
            p = b["provider"]
            self.assertEqual(p["only"], [replay.MODELS[mk]["provider"]])
            self.assertIs(p["allow_fallbacks"], False)
            self.assertIs(p["zdr"], True)
            self.assertEqual(p["data_collection"], "deny")

    def test_red_body_without_zdr_is_refused_before_any_send(self):
        self.with_key()
        b = self.body()
        del b["provider"]["zdr"]
        fp = FakePost([fake_response(cost=0.001)])
        bud = replay.Budget(os.path.join(self.t, "b.json"), 5.0)
        with self.assertRaises(replay.Refused) as cm:
            replay.send(b, "deepseek", FAKE_KEY, bud, "t", 0.001, post=fp)
        self.assertIn("zdr", str(cm.exception))
        self.assertEqual(fp.calls, [], "a request without zdr reached the network function")
        self.assertEqual(bud.total(), 0.0, "a refused request was charged")

    def test_red_each_field_missing_or_wrong_is_refused(self):
        for field in replay.REQUIRED_ROUTING:
            b = self.body()
            del b["provider"][field]
            with self.assertRaises(replay.Refused, msg=f"missing {field}"):
                replay.assert_routing(b, "deepseek")
        for field, bad in (("only", ["deepinfra", "streamlake"]), ("only", ["xiaomi"]), ("allow_fallbacks", True),
                           ("zdr", False), ("data_collection", "allow")):
            b = self.body()
            b["provider"][field] = bad
            with self.assertRaises(replay.Refused, msg=f"{field}={bad}"):
                replay.assert_routing(b, "deepseek")
        b = self.body()
        del b["provider"]
        with self.assertRaises(replay.Refused):
            replay.assert_routing(b, "deepseek")


# ------------------------------------------------------------------------------------------------ 2. budget
class BudgetGuard(Isolated):
    def test_red_refuses_at_the_cap_with_a_fake_usage_feed(self):
        bud = replay.Budget(os.path.join(self.t, "b.json"), 0.012)
        fp = FakePost([fake_response(cost=0.005) for _ in range(5)])
        b = replay.build_body("deepseek", replay.build_messages(REAL["code_patch"])[0])
        replay.send(b, "deepseek", FAKE_KEY, bud, "a", 0.003, post=fp)   # 0 + .003 <= .012 -> sent, settles .005
        replay.send(b, "deepseek", FAKE_KEY, bud, "b", 0.003, post=fp)   # .005 + .003 <= .012 -> sent, total .010
        with self.assertRaises(replay.Refused) as cm:
            replay.send(b, "deepseek", FAKE_KEY, bud, "c", 0.003, post=fp)  # .010 + .003 > .012 -> REFUSED
        self.assertIn("BUDGET", str(cm.exception))
        self.assertEqual(len(fp.calls), 2, "the guard let a third request through")
        self.assertAlmostEqual(bud.total(), 0.010, places=9)
        d = replay._rjson(os.path.join(self.t, "b.json"))
        self.assertEqual([e["state"] for e in d["entries"]], ["settled", "settled"])
        self.assertEqual({e["source"] for e in d["entries"]}, {"usage.cost"})

    def test_cost_absent_is_computed_from_tokens_and_prices(self):
        bud = replay.Budget(os.path.join(self.t, "b.json"), 5.0)
        fp = FakePost([fake_response(cost=None, pt=10000, ct=2000, provider="Z.AI")])
        b = replay.build_body("glm", replay.build_messages(REAL["code_patch"])[0])
        _, usd, source, _ = replay.send(b, "glm", FAKE_KEY, bud, "g", 0.02, post=fp)
        self.assertAlmostEqual(usd, 10000 * 0.15e-6 + 2000 * 0.50e-6, places=12)
        self.assertTrue(source.startswith("computed"))

    def test_budget_is_shared_across_models(self):
        bud = replay.Budget(os.path.join(self.t, "b.json"), 0.010)
        fp = FakePost([fake_response(cost=0.006), fake_response(cost=0.006, provider="Z.AI")])
        msgs = replay.build_messages(REAL["code_patch"])[0]
        replay.send(replay.build_body("deepseek", msgs), "deepseek", FAKE_KEY, bud, "a", 0.003, post=fp)
        with self.assertRaises(replay.Refused):
            replay.send(replay.build_body("glm", msgs), "glm", FAKE_KEY, bud, "b", 0.005, post=fp)
        self.assertEqual(len(fp.calls), 1)

    def test_main_stops_the_drain_at_the_cap_and_never_prints_the_key(self):
        self.with_key()
        os.environ["HOSTED_BUDGET_USD"] = "0.012"
        fp = FakePost([fake_response(cost=0.004) for _ in range(10)])
        out = io.StringIO()
        with redirect_stdout(out):
            rc = replay.main(["--model", "deepseek", "--no-check", "--limit", "10"], post=fp)
        self.assertEqual(rc, 2)
        # deepseek worst case per task ~ $0.0045-0.0060: spent .004k + worst must stay <= .012
        self.assertLess(len(fp.calls), 10)
        self.assertLessEqual(replay.Budget(os.path.join(replay.STATE, "budget.json"), 0.012).total(), 0.012)
        self.assertIn("BUDGET", out.getvalue())
        self.assertNotIn(FAKE_KEY, out.getvalue())
        for url, body in fp.calls:
            self.assertNotIn(FAKE_KEY, json.dumps(body))
        rows = [l for l in replay._rtext(os.path.join(replay.DONE_DIR, "done_deepseek.md")).splitlines() if l.startswith("| 20")]
        self.assertEqual(len(rows), len(fp.calls))


# ------------------------------------------------------------------------------------------------ 3. dry-run
class DryRun(Isolated):
    def test_dry_run_makes_zero_network_calls(self):
        attempts = []

        def blocked(*a, **k):
            attempts.append(a[:2])
            raise OSError("network blocked by test")

        saved = (socket.socket.connect, socket.socket.connect_ex, socket.create_connection, socket.getaddrinfo, replay._http_post)
        socket.socket.connect = lambda self, *a: blocked(*a)
        socket.socket.connect_ex = lambda self, *a: blocked(*a)
        socket.create_connection = blocked
        socket.getaddrinfo = blocked
        replay._http_post = blocked
        try:
            # control: the block is live (an attempted fetch IS caught and counted)
            with self.assertRaises(Exception):
                urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=5)
            self.assertEqual(len(attempts), 1, "the socket block did not catch a real attempt — the test would be blind")
            attempts.clear()
            for mk in replay.MODELS:
                out = io.StringIO()
                with redirect_stdout(out):
                    rc = replay.main(["--model", mk, "--dry-run"])
                self.assertEqual(rc, 0, out.getvalue()[-600:])
                n = sum(1 for l in out.getvalue().splitlines() if l.startswith("DRY "))
                self.assertEqual(n, len(replay.spark_rows()))
                self.assertIn('"zdr": true', out.getvalue())
                self.assertIn("key ABSENT", out.getvalue())
        finally:
            socket.socket.connect, socket.socket.connect_ex, socket.create_connection, socket.getaddrinfo, replay._http_post = saved
        self.assertEqual(attempts, [], f"dry-run attempted the network: {attempts}")

    def test_missing_key_is_rc2_one_line(self):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = replay.main(["--model", "mimo"])
        self.assertEqual(rc, 2)
        self.assertEqual(len(out.getvalue().strip().splitlines()), 1)
        self.assertIn(replay.KEY_NAME, out.getvalue())


# ------------------------------------------------------------------------------------------------ 4. byte identity
class ByteIdentity(Isolated):
    def test_three_real_spark_inputs_rebuild_byte_identically(self):
        for tier, run in REAL.items():
            msgs, info = replay.build_messages(run)  # raises Refused on any mismatch
            meta = replay._rjson(os.path.join(run, "out.md.meta.json"))
            self.assertEqual(info["tier"], tier)
            got = sum(len(m["content"].encode("utf-8")) for m in msgs)
            self.assertEqual(got, meta["prompt_bytes"], run)
            raw_input = rbytes(os.path.join(run, "input.json"))
            self.assertIn(raw_input.decode("utf-8").strip(), msgs[1]["content"])
            body = replay.build_body("mimo", msgs)
            self.assertIs(body["messages"], msgs)
        # the QWEN122_AB like-for-like reference: the Spark recorded 70,129 B for KS-1410 batch
        self.assertEqual(replay.build_messages(REAL["code_patch2"])[1]["prompt_bytes"], 70129)

    def test_red_a_one_byte_change_to_the_input_is_refused(self):
        src = REAL["bash_patch"]
        dst = os.path.join(self.t, "run")
        os.makedirs(dst)
        for f in ("round.json", "out.md.meta.json", "input.json"):
            shutil.copyfile(os.path.join(src, f), os.path.join(dst, f))
        b = rbytes(os.path.join(dst, "input.json"))
        replay._wtext(os.path.join(dst, "input.json"), b.replace(b"{", b"{ ", 1), "wb")
        with self.assertRaises(replay.Refused) as cm:
            replay.build_messages(dst)
        self.assertIn("byte-identity", str(cm.exception))


# ------------------------------------------------------------------------------------------------ 5. rate limit + resume
def http_error(code, retry_after=None):
    hdrs = email.message.Message()
    if retry_after is not None:
        hdrs["Retry-After"] = str(retry_after)
    body = json.dumps({"error": {"code": code, "message": "temporarily rate-limited upstream. Please retry shortly"}}).encode()
    return urllib.error.HTTPError(replay.API_URL, code, "rate limited", hdrs, io.BytesIO(body))


class ScriptedPost(FakePost):
    """Each scripted entry is bytes (returned) or a zero-arg callable that builds an exception (raised)."""

    def __call__(self, url, data, headers, timeout):
        self.calls.append((url, json.loads(data)))
        r = self.responses.pop(0)
        if callable(r):
            raise r()
        return r


class RateLimitAndResume(Isolated):
    T1 = os.path.basename(REAL["bash_patch"])
    T2 = os.path.basename(REAL["code_patch"])

    def setUp(self):
        super().setUp()
        self.with_key()
        self.waits = []
        self.saved_sleep = replay._sleep
        replay._sleep = self.waits.append

    def tearDown(self):
        replay._sleep = self.saved_sleep
        super().tearDown()

    def rows(self):
        p = os.path.join(replay.DONE_DIR, "done_deepseek.md")
        return [l for l in replay._rtext(p).splitlines() if l.startswith("| 20")] if os.path.exists(p) else []

    def run_main(self, fp, only):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = replay.main(["--model", "deepseek", "--no-check", "--only", ",".join(only)], post=fp)
        return rc, out.getvalue()

    def test_red_429_twice_then_200_completes_the_same_request(self):
        fp = ScriptedPost([lambda: http_error(429, retry_after=7), lambda: http_error(429), fake_response(cost=0.001)])
        rc, out = self.run_main(fp, [self.T1])
        self.assertEqual(rc, 0, out[-800:])
        self.assertEqual(len(fp.calls), 3)
        self.assertTrue(all(c[1] == fp.calls[0][1] for c in fp.calls), "a retry changed the request")
        for _, b in fp.calls:
            replay.assert_routing(b, "deepseek")
            self.assertEqual(b["provider"]["only"], ["deepinfra"])
        self.assertEqual(self.waits[0], 7, "Retry-After not honoured")
        self.assertTrue(40 * 0.85 <= self.waits[1] <= 40 * 1.15, self.waits)  # after attempt 2: backoff step 2 = 40s x jitter
        rows = self.rows()
        self.assertEqual(len(rows), 1)
        self.assertIn("UNCHECKED", rows[0])
        self.assertNotIn("SKIPPED", rows[0])
        # budget: the two 429s (no usage) were released; only the 200's usage.cost is counted
        self.assertAlmostEqual(replay.Budget(os.path.join(replay.STATE, "budget.json"), 5).total(), 0.001, places=9)

    def test_red_429_forever_is_skipped_and_the_run_continues(self):
        fp = ScriptedPost([lambda: http_error(429)] * replay.RETRY_ATTEMPTS + [fake_response(cost=0.001)])
        rc, out = self.run_main(fp, [self.T1, self.T2])
        self.assertEqual(rc, 4, out[-800:])
        self.assertEqual(len(fp.calls), replay.RETRY_ATTEMPTS + 1, "the drain did not continue to the next task")
        self.assertEqual(len(self.waits), replay.RETRY_ATTEMPTS - 1)
        self.assertTrue(all(1 <= w <= replay.RETRY_CAP for w in self.waits), self.waits)
        self.assertGreater(self.waits[-1], self.waits[0])
        rows = self.rows()
        self.assertEqual(len(rows), 2)
        skipped = [r for r in rows if "SKIPPED-RATE-LIMIT" in r]
        self.assertEqual(len(skipped), 1)
        self.assertEqual(skipped[0].split("|")[2].strip(), [t for t in (self.T1, self.T2) if t in skipped[0]][0])
        self.assertIn("UNCHECKED", [r for r in rows if r not in skipped][0])
        self.assertIn("SKIPPED-RATE-LIMIT", out)

    def test_non_retryable_http_error_still_stops_at_once(self):
        fp = ScriptedPost([lambda: http_error(404), fake_response(cost=0.001)])
        rc, out = self.run_main(fp, [self.T1])
        self.assertEqual(rc, 4)
        self.assertEqual(len(fp.calls), 1)
        self.assertEqual(self.waits, [])

    def test_resume_a_done_row_is_not_resent_and_skipped_rows_are(self):
        a = [r for r in replay.spark_rows() if os.path.basename(r["run"]) == self.T1][0]
        b = [r for r in replay.spark_rows() if os.path.basename(r["run"]) == self.T2][0]
        replay.append_done("deepseek", ["2026-10-09 18:00:00", self.T1, "FAIL (x)", 1, "1+1", 0, "0.001", "FAIL", "-", "/r", a["run"]])
        replay.append_done("deepseek", ["2026-10-09 18:00:01", self.T2, "SKIPPED-RATE-LIMIT (HTTP 429 x6)", "-", "-", "-",
                                        "0.00000", "PASS", "-", "/r2", b["run"]])
        fp = ScriptedPost([fake_response(cost=0.001)])
        rc, out = self.run_main(fp, [self.T1, self.T2])
        self.assertEqual(rc, 0, out[-800:])
        self.assertEqual(len(fp.calls), 1, "a task with a PASS/FAIL row was resent")
        sent_user = fp.calls[0][1]["messages"][1]["content"]
        self.assertIn(replay._rtext(os.path.join(b["run"], "input.json")).strip(), sent_user)
        self.assertIn("RESUME — 1 task(s)", out)


# ------------------------------------------------------------------------------------------------ 6. checker positive control
@unittest.skipIf(os.environ.get("HOSTED_SKIP_CHECKER") == "1", "HOSTED_SKIP_CHECKER=1")
class CheckerControl(unittest.TestCase):
    """check.sh on a REAL Spark output (copied out.md + input.json) must reproduce the verdict the Spark round recorded."""

    def control(self, spark_run):
        t = tmpdir()
        try:
            run = os.path.join(t, "run")
            os.makedirs(run)
            for f in ("input.json", "out.md", "out.md.meta.json"):
                shutil.copyfile(os.path.join(spark_run, f), os.path.join(run, f))
            rj = replay._rjson(os.path.join(spark_run, "round.json"))
            gold = os.path.join(rj["brief_dir"], "golden.diff")
            p = subprocess.run(["bash", os.path.join(HOSTED, "check.sh"), run, rj["tier"], rj["tip"], os.path.join(t, "work"),
                                gold if os.path.isfile(gold) else ""], capture_output=True, text=True, timeout=1800)
            last = p.stdout.strip().splitlines()[-1]
            want_v = "PASS" if rj["verdict"] == "PASS" else "FAIL"
            self.assertTrue(last.startswith(f"CHECK {want_v} "), f"{last}\n{p.stderr[-800:]}")
            self.assertIn(f"result={rj['spark_result']}", last)
            self.assertIn(f"checker={rj['checker_result']}", last)
            self.assertIn(f"golden={rj['golden']}", last)
            rec = replay._rtext(os.path.join(spark_run, "checker.out"))
            new = replay._rtext(os.path.join(run, "checker.out"))
            for prefix in ("RESULT:", "SPARK RESULT:"):
                self.assertEqual([l for l in rec.splitlines() if l.startswith(prefix)],
                                 [l for l in new.splitlines() if l.startswith(prefix)], prefix)
            return p.returncode
        finally:
            shutil.rmtree(t, ignore_errors=True)

    def test_end_to_end_main_with_a_fake_post_reaches_the_checker(self):
        """main() -> send (fake) -> write_outputs -> check.sh -> round.json + done row, fed the Spark's own KS-998 answer."""
        iso = Isolated("setUp")
        iso.setUp()
        try:
            iso.with_key()
            ans = replay._rtext(os.path.join(REAL["bash_patch"], "out.md"))
            fp = FakePost([fake_response(cost=0.0012, content=ans)])
            out = io.StringIO()
            with redirect_stdout(out):
                rc = replay.main(["--model", "deepseek", "--only", os.path.basename(REAL["bash_patch"])], post=fp)
            self.assertEqual(rc, 0, out.getvalue()[-800:])
            self.assertEqual(len(fp.calls), 1)
            self.assertIn("HOSTED deepseek spark_secuura_2026-10-09_KS-998-format-gate-npm-stdin: PASS", out.getvalue())
            rows = [l for l in replay._rtext(os.path.join(replay.DONE_DIR, "done_deepseek.md")).splitlines() if l.startswith("| 20")]
            self.assertEqual(len(rows), 1)
            self.assertIn("TREE-IDENTICAL", rows[0])
            run = rows[0].split("|")[10].strip()
            self.assertFalse(os.path.exists(os.path.join(replay.WORK, os.listdir(replay.WORK)[0], "clone")), "clone not removed")
            self.assertEqual(rbytes(os.path.join(run, "input.json")), rbytes(os.path.join(REAL["bash_patch"], "input.json")))
            self.assertNotIn(FAKE_KEY, replay._rtext(os.path.join(run, "request.json")))
        finally:
            iso.tearDown()

    def test_pass_verdict_reproduces(self):
        self.assertEqual(self.control(REAL["bash_patch"]), 0)  # KS-998 npm-stdin: PASS (7/7), TREE-IDENTICAL

    def test_code_patch_pass_reproduces(self):  # the prepare_clone + spark_checker.sh path (jest)
        self.assertEqual(self.control(REAL["code_patch"]), 0)  # KS-723 anchors-tx: PASS (7/7), DIFFERS

    def test_fail_verdict_reproduces(self):
        self.assertEqual(self.control(os.path.join(RUNS, "spark_secuura_2026-10-09_KS-1438-html-docs-check-resolved-paths-r2")), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
