# DeepSeek V4 Flash on the ZGX Spark — Agent Handoff

**Status:** Deployed and verified working, 2026-09-22.
**Purpose:** Everything needed to use this model for coding tests.
**Scope:** Isolated single-device deployment. No Ornith, no Mac Studio, no pooled/sharded tier.

Every number in this document was **measured on this box**. Where a measurement
contradicts the original deployment brief, the measurement wins and the conflict
is called out explicitly in §9.

---

## 1. Connect

The server is bound to **loopback only** (`127.0.0.1:8888`). There is **no auth**
in front of it, so do not widen the bind without putting something in front.

```bash
# from the MacBook (or any machine with the ZGX-Nano-G1n ssh alias)
# keepalive flags matter — a plain `ssh -f -N -L` tunnel WILL drop silently
ssh -f -N -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
        -o ExitOnForwardFailure=yes -L 8888:127.0.0.1:8888 ZGX-Nano-G1n

curl -sf http://127.0.0.1:8888/health && echo OK
```

**A dropped tunnel looks exactly like a dead server.** This was observed in
practice: `ConnectionResetError: [Errno 54] Connection reset by peer` while the
server was perfectly healthy. Before debugging the model, check the tunnel:

```bash
pgrep -fl 'L 8888:127.0.0.1:8888' || echo "TUNNEL GONE — re-establish it"
ssh ZGX-Nano-G1n 'curl -sf -m 5 http://127.0.0.1:8888/health && echo "server is fine"'
```

**For a long coding-test run, prefer running the harness ON the Spark** — no
tunnel, no drop:

```bash
scp harness.py ZGX-Nano-G1n:~/spark-eval/
ssh ZGX-Nano-G1n 'python3 ~/spark-eval/harness.py'
```

Then point any OpenAI-compatible client at:

| | |
|---|---|
| Base URL | `http://127.0.0.1:8888/v1` |
| Model name | `deepseek-v4-flash-0731` |
| API key | not required (send anything if your client insists) |

**Verified:** `/health` and a full chat completion both succeed from the MacBook
through this tunnel.

### Host facts

| | |
|---|---|
| SSH alias | `ZGX-Nano-G1n` (defined by NVIDIA Sync, key-based, no password) |
| Hostname | `zgx-15d5` / `zgx-15d5.local` |
| User | `datasec-rd` |
| IP | `192.168.4.33` — **DHCP, it moves.** Prefer the mDNS name `zgx-15d5.local` |
| GPU | NVIDIA GB10, 121 GB unified, driver 580.178.04, CUDA 13.0 |
| `sudo` | **requires a password** — not available to automated agents |

---

## 2. ⚠️ The one thing that will waste your time

**Thinking mode is ON by default at `effort=max`.** With a normal token budget the
model spends the entire budget reasoning and returns an **empty `content` field**.
This looks identical to the model failing. It is not.

Measured, same prompt, same server:

| | Thinking ON (default) | Thinking OFF |
|---|---|---|
| `finish_reason` | `length` (truncated) | `stop` |
| Completion tokens | 1000 (whole budget) | **94** |
| `content` length | **0 — EMPTY** | 331 |
| `reasoning` length | 3970 | 0 |
| Wall time | 53.7 s | **2.3 s** |
| Answer correct | never emitted one | **yes, all cases** |

### For coding tests, disable thinking

```json
{
  "model": "deepseek-v4-flash-0731",
  "messages": [{"role": "user", "content": "..."}],
  "max_tokens": 1024,
  "temperature": 0,
  "chat_template_kwargs": {"thinking": false}
}
```

If you *want* reasoning, keep it on but budget **several thousand** `max_tokens`,
and read `reasoning_content` (non-streaming) or `reasoning` (streaming) in
addition to `content`. Always check `finish_reason`: `length` means truncated.

### Field placement (measured)

- **Non-streaming, thinking off** → answer in `content`, `reasoning` empty.
- **Non-streaming, thinking on, budget too small** → `content` EMPTY, all output in `reasoning_content`.
- **Streaming** → emits both `reasoning` and `content` deltas. A client reading only
  `content` gets the answer but loses the reasoning trace.

Defensive accessor:

```python
msg = resp["choices"][0]["message"]
text = msg.get("content") or msg.get("reasoning_content") or msg.get("reasoning") or ""
truncated = resp["choices"][0]["finish_reason"] == "length"
```

---

## 3. ⚠️ Concurrency: this is a ONE-REQUEST-AT-A-TIME server

`MAX_NUM_SEQS=1`. Concurrent requests **queue**; they do not run in parallel.

Do **not** design an orchestrator fan-out against this deployment as configured.
Run coding tests sequentially, or reconfigure and re-measure (see §7).

From the server's own metrics: `kv_cache_max_concurrency = 1.17`.

---

## 4. Measured performance

| Metric | Measured | Brief claimed |
|---|---|---|
| Decode, code gen | **37.13 tok/s** median of 3 (36.92 / 37.13 / 41.58) | 38.12 |
| Prefill | **1,032 tok/s** on a 47,096-token prompt | 1,055 @ 252K |
| Agentic turn, 23.6K in / 1K out | **53.7 s** | ~54 s |
| Short answer, thinking off | 94 tok in **2.3 s** | — |

Performance matches the brief closely. Treat ~37 tok/s decode and ~1,030 tok/s
prefill as the planning numbers.

**Budgeting a coding test:** a turn with ~30K of context and a short answer costs
roughly **50–55 s** with thinking on, or a few seconds with it off and a small
answer. Prefill dominates at large context; decode dominates at long outputs.

---

## 5. Capability verification (7/7 passed)

Run `2026-09-22T04:37Z` against the live server:

| Test | Result |
|---|---|
| Served model id | `deepseek-v4-flash-0731` |
| Reasoning field placement | `content` populated (with adequate budget) |
| KV pool / cache metrics | captured, see §6 |
| Decode tok/s | 37.13 median |
| Prefill tok/s | 1,032 |
| **Generated code executes correctly** | `solve([2,7,11,15],9) → [0,1]` ✓ |
| **Structured `tool_calls`** | `get_weather({"city":"Sydney"})` ✓ |

Plus a realistic bug-fix task (`parse_duration` with h/m/s suffixes): with thinking
off the model produced a correct function passing **all four** test cases
(`1h30m→5400`, `45s→45`, `2h→7200`, `10m→600`).

Tool calls arrive as a **proper `tool_calls` field**, not raw text — no parser
workaround needed for this model.

Re-run the suite any time:

```bash
ssh ZGX-Nano-G1n 'python3 ~/spark-eval/probe.py'
# raw JSON -> ~/spark-eval/results.json
```

---

## 5b. Coding capability profile (11 complex tasks, measured)

Eleven non-trivial tasks were generated, executed and scored against hidden test
suites. Pipeline per task: generate (thinking off) → execute → score → feed back
the exact failures → regenerate → re-score.

### Headline

| | Round 1 | After one repair round |
|---|---|---|
| All 10 suite tasks (159 tests) | 84.3% | 98.1% |
| **Excluding the delegated regex task** | **95.7%** | **97.9%** |
| Tasks perfect on first attempt | **6 / 10** | — |

Ten tasks cost **168 s of total generation time**. This model is fast enough to
run a real coding-test loop against.

### Per-task

| Task | Round 1 | Round 2 | Tests |
|---|---|---|---|
| topo-scheduler | 12 | — | 12 ✅ first try |
| interval-set | 18 | — | 18 ✅ first try |
| ttl-lru-cache | 13 | — | 13 ✅ first try |
| jsonpath | 14 | — | 14 ✅ first try |
| fuzzy-trie | 15 | — | 15 ✅ first try |
| state-machine | 17 | — | 17 ✅ first try |
| semver-resolver | 14 | **16** | 16 — repaired |
| regex-engine | 0 | **19** | 19 — see caveat |
| expr-evaluator | 20 | 21 | 22 — one stuck |
| line-diff | 11 | 11 | 13 — **repair failed** |
| spreadsheet engine (separate) | 16 | 24 | 26 — **repair failed** |

### What it is good at

Standard algorithms and data structures, first time: graph toposort with cycle
detection, merged interval sets with splitting removal, LRU+TTL eviction with an
injected clock, JSONPath traversal, Levenshtein trie search, finite state
machines with atomic replay. Also recursive-descent parsing, operator
precedence, and dependency-cycle detection.

### What it is bad at — and this is the useful part

**Mechanical bugs repair reliably. Subtle semantic bugs do not.**

Fixed on one repair round: a missing `import`, a tuple-unpacking error, a
case-insensitivity miss. All mechanical.

**Never fixed, even with the exact failing input, actual vs expected output, and
in one case the root cause plus the fix written out:**

1. `line-diff` — emits `insert` before `delete`; spec explicitly requires the
   reverse. Unchanged after repair.
2. `expr-evaluator` — `-2^2` returns `4`, should be `-4` (unary minus must bind
   looser than `^`). Unchanged after repair.
3. `spreadsheet` cache invalidation — declared `dependencies` / `dependents` maps
   and wrote correct-looking recursive invalidation, but **never populated either
   map**, so it was dead code. Survived **three** repair rounds including one
   that supplied the root cause and the exact fix. Verified zero write-sites.

The pattern: where correct behaviour contradicts the model's prior (conventional
diff ordering, conventional unary-minus binding), it reverts to the prior and
restates the same wrong code confidently. Telling it the symptom does not help.
Telling it the root cause does not help either.

### Implications for a coding-test harness

1. **Always execute the output.** All three stuck bugs produce plausible,
   well-structured, confidently-commented code that is simply wrong.
2. **Budget one repair round; it is worth it.** It converts most mechanical
   failures into passes for ~50% extra time.
3. **Do not budget more than two.** Round 3 on the spreadsheet task gained
   nothing, and round 3 with the root cause supplied gained nothing either.
4. **Watch for shortcut solutions.** Asked to implement a regex matcher "in pure
   Python (stdlib only)", it imported `re` and delegated to `re.fullmatch`. Not a
   rule violation as written — a test-design gap. State forbidden modules
   explicitly.
5. **Grade on semantics, not shape.** Dead-but-plausible code is this model's
   characteristic failure.

---

## 5c. Four-model comparison (identical tasks, identical pipeline)

Same 10 tasks, same hidden suites, same two-round repair loop, same scorer.
Task prompts byte-identical across all four models.

| Task | DeepSeek V4 Flash | Ornith 1.5 35B | Opus 4.8 | Opus 5 |
|---|---|---|---|---|
| regex-engine | 0/19 | 19/19 | 19/19 | 19/19 |
| topo-scheduler | 12/12 | 12/12 | 12/12 | 12/12 |
| interval-set | 18/18 | 15/18 | 18/18 | 18/18 |
| ttl-lru-cache | 13/13 | 13/13 | 13/13 | 13/13 |
| jsonpath | 14/14 | 14/14 | 14/14 | 14/14 |
| expr-evaluator | 20/22 | **3/22** | 22/22 | 22/22 |
| fuzzy-trie | 15/15 | **8/15** | 15/15 | 15/15 |
| semver-resolver | 14/16 | 16/16 | 16/16 | 16/16 |
| line-diff | 11/13 | 13/13 | 13/13 | 13/13 |
| state-machine | 17/17 | 17/17 | 17/17 | 17/17 |
| **Round 1** | 134/159 (84.3%) | 130/159 (81.8%) | **159/159 (100%)** | **159/159 (100%)** |
| **After repair** | **156/159 (98.1%)** | 130/159 (81.8%) | 159/159 (100%) | 159/159 (100%) |
| Perfect first try | 6/10 | 7/10 | 10/10 | 10/10 |
| Wall-clock | 168 s | **132 s** | 231 s | 116 s |

### Findings

**Both Opus versions scored 100%.** This benchmark cannot distinguish Opus 4.8
from Opus 5 — it is saturated at the top. The only measurable difference is
speed: Opus 5 finished in 116 s vs 231 s, roughly 2x faster for identical output.
Any claim about relative Opus quality needs a harder suite.

**The two local models are close in aggregate but fail differently.**
84.3% vs 81.8% on first attempt looks like a tie. The per-task view is not:

- Ornith beat DeepSeek on `line-diff` (13/13 vs 11/13) — a task DeepSeek could
  never fix across two repair rounds — and on `semver-resolver`.
- DeepSeek beat Ornith decisively on `expr-evaluator` (20/22 vs **3/22**) and
  `fuzzy-trie` (15/15 vs 8/15).

**The decisive difference is response to feedback.**

| | Round 1 → Round 2 |
|---|---|
| DeepSeek | +22 tests (84.3% → 98.1%) |
| Ornith | **net 0** (+1 on one task, **-1** on another) |

DeepSeek uses failure feedback productively. Ornith does not — its repair round
gained one test and lost another, and on `expr-evaluator` it reproduced 3/22
twice. For an agentic loop that iterates on test failures, that difference
matters more than the 2.5-point gap in raw first-attempt score.

**Ornith is not disadvantaged by quantisation here.** It ran Q4_K_M (~4.5 bpw)
against DeepSeek's 3.0 bpw, on the same GB10 — the more generous quant — and
still lost on aggregate and on repair.

### Caveats, stated plainly

1. **Opus ran through the `claude` CLI**, not the raw API, so it carries a
   coding-oriented system prompt the local models did not get, and that path
   exposes no temperature control. Task prompts were identical; the wrapper was
   not. This likely flatters Opus somewhat.
2. **Thinking parity had to be forced.** Ornith's first run truncated on 5 of 10
   tasks because its default thinking block consumed the token budget — the same
   failure mode as DeepSeek. Re-run with `reasoning_effort: "none"` to match
   DeepSeek's `thinking: false`. The default-config run (unusable for comparison)
   is preserved in `results_ollama_defaultcfg.json`.
3. **Two harness bugs were found and fixed mid-study**, both mine:
   - Model-generated code hung the harness in an infinite loop (20 min at 96%
     CPU). Now guarded by 20 s / 60 s watchdogs.
   - Errored tasks dropped out of the denominator, producing incomparable totals
     like "73/91". Failed tasks now score 0 out of their full count.
   Any earlier number computed over a denominator below 159 is void.
4. **The regex task is weak evidence.** DeepSeek reached 19/19 by importing `re`
   and calling `re.fullmatch`. Opus 5 wrote a genuine 94-line matcher with zero
   `re` references. Same score, different thing measured — my spec permitted the
   shortcut. DeepSeek's round-1 `0/19` was merely a missing `import`.

---

## 5d. HARD suite — property-based, oracle-checked (DeepSeek vs Opus 5)

The §5c suite saturated: Opus 4.8 and Opus 5 both scored 100%, leaving no
resolution. This suite replaces example-based assertions with **property-based
testing against brute-force oracles**, randomised operation sequences,
convergence invariants and measured asymptotic complexity.

71 assertions across 5 tasks. Oracles were validated before use (the banker's
rounding oracle was checked against Python's `decimal` on 4,000 random cases).

| Task | DeepSeek R1 | DeepSeek R2 | Opus 5 |
|---|---|---|---|
| persistent-bst (immutable, balanced, structural sharing) | **14/14** | — | 14/14 |
| lazy-segment-tree (interacting add/assign tags, O(log n)) | **14/14** | — | 14/14 |
| crdt-sequence (convergence under shuffled delivery) | 7/12 | **7/12** | 12/12 |
| exact-decimal (banker's rounding, 900 property checks) | 18/19 | **19/19** | 19/19 |
| priority-scheduler (transitive priority inheritance) | 10/12 | **10/12** | 12/12 |
| **TOTAL** | 63/71 (88.7%) | **64/71 (90.1%)** | **71/71 (100%)** |
| Wall-clock | 276 s | | **148 s** |

### What this establishes

**DeepSeek is genuinely strong on hard algorithmic work.** It scored 14/14 first
try on BOTH the persistent balanced BST (structural sharing verified by node
identity, balance verified against 3*log2(n)+3 on 2000 ascending inserts, 120
historical versions checked for corruption) and the lazy segment tree (600
randomised mixed ops vs brute force, plus a 20,000-operation complexity budget
that an O(n) implementation cannot meet). These are not easy problems.

**The gap is concentrated in distributed-systems reasoning.** `crdt-sequence`
is where it collapsed: 5 of 12 failed, all convergence properties. Local edits
were correct; replicas diverged the moment ops arrived in different orders. The
minimal case is diagnostic — two replicas insert at index 0 concurrently and end
with `A='ba-'` vs `B='b-a'`: the tie-break is not deterministic across replicas,
which is the entire point of a CRDT.

**Transitive priority inheritance also failed** and stayed failed.

**The repair pattern is identical to §5b/§5c.** One mechanical bug (a division
rounding edge case) was fixed on feedback, +1. Both conceptual failures —
convergence and transitive inheritance — survived the repair round unchanged,
with the same wrong output. Feedback fixes mechanics, not misconceptions.

### The ceiling is still not found

Opus 5 scored 100% on this suite too, first attempt, no repair. So this
benchmark bounds DeepSeek (~90%) but still does not discriminate among frontier
models. Separating Opus 4.8 from Opus 5 needs something harder again.

### Practical reading for routing

| Work type | Local model viable? |
|---|---|
| Data structures, parsers, algorithms, complexity-bound code | **Yes** — 14/14 twice on genuinely hard instances |
| Exact numeric semantics | **Yes, with a repair round** — 18/19 → 19/19 |
| Distributed/concurrent correctness, convergence, inheritance protocols | **No** — send to cloud |

---

## 6. Serving configuration (from the running server)

| | |
|---|---|
| `max_model_len` | **384,000** tokens |
| KV pool | **449,519 tokens** |
| `kv_cache_max_concurrency` | 1.17 |
| `num_gpu_blocks` | 9,811 (block size 4) |
| KV cache dtype | `nvfp4_ds_mla` |
| Prefix caching | **enabled** (sha256) |
| GPU memory utilisation | 0.94 |
| `MAX_NUM_BATCHED_TOKENS` | 8,224 |
| Speculative decoding | `MODE=dspark`, K5 draft |
| Host memory while serving | ~118 GB of 121 GB |

Prefix caching is on — repeated identical prefixes across test cases will be
cheaper than cold numbers suggest. Randomise or salt prompts when benchmarking.

---

## 7. Operating it

```bash
cd ~/DeepSeek-v4-Flash-One-DGX-Spark

./start.sh ps        # container status
./start.sh logs      # tail logs (see caveat below)
./start.sh stop      # stop, preserves ./data and caches
./start.sh restart
./start.sh down      # remove container, preserves weights
```

Relaunch wrapper used for this deployment (`run-a2.sh`) sets:
`SERVING_HOST=127.0.0.1`, `STARTUP_WAIT=21600`, `HF_TOKEN` from
`~/.cache/huggingface/token`.

**A restart is cheap now** — weights are on disk. Expect ~5 minutes from container
start to `/health`, not the original 5h40m.

### To enable concurrency (requires re-measuring)

Edit `MAX_NUM_SEQS` in `start.sh` and restart. Note from the recipe's own comments:
the KV pool **shrinks as sequences are added** — 2 sequences were observed at
~337K total (~169K each), not 2×449K. Lower `MAX_MODEL_LEN` accordingly or boot
will fail its KV check.

### Log caveat

`docker logs` is **nearly empty** — the container's Python buffers stdout when not
attached to a TTY. This is not a hang. Use these as real signals instead:

```bash
free -g                                              # ~118G = loaded and serving
nvidia-smi --query-gpu=utilization.gpu --format=csv  # ~96% under load
curl -sf http://127.0.0.1:8888/health                # authoritative
```

Also: the container reports `(unhealthy)` during boot. That is Docker's healthcheck
`start_period` expiring while the model loads. Plain Docker does not restart on
healthcheck failure — it is cosmetic.

---

## 8. What is installed

| | |
|---|---|
| Recipe | `~/DeepSeek-v4-Flash-One-DGX-Spark` (MiaAI-Lab, `--depth 1`) |
| Image | `ghcr.io/0xsero/deepseek-v4-flash-0731-spark-sparkinfer@sha256:2e077489a83a…` (pinned by digest) |
| Weights | `0xSero/deepseek-v4-flash-0731-spark` rev `22f28d32b9b29b4352eaa380ff8c2c170b2847ab` |
| Weight cache | `~/DeepSeek-v4-Flash-One-DGX-Spark/hf-hub` (~103 GB real) |
| TP1 checkpoint | `~/DeepSeek-v4-Flash-One-DGX-Spark/data` (~99 GB) |
| Container | `deepseek-v4-flash-spark-deepseek-v4-flash-1` |
| Probe suite | `~/spark-eval/probe.py`, results `~/spark-eval/results.json` |
| `hf` CLI | `~/.venvs/hf/bin/hf` v1.32.0 with `hf_xet` |
| Disk free | 3.2 TB |

Model: **mainline DeepSeek V4 Flash 0731**, EXL3 3.0 bpw, REAP-pruned to 216 of
256 experts (15.6%). **Not** the vision variant, **not** uncensored. Safe for
customer-facing work.

---

## 9. Corrections to the original deployment brief

The brief at `~/Downloads/spark-studio-deployment-brief.md` is wrong on several
points. Verified corrections:

1. **HF token is NOT required.** All repos on both A1 and A2 paths are
   `gated=false`. A1's README states it outright. No access request needed.
2. **The "30 minutes for /health" rule is wrong and dangerous.** `start.sh`'s own
   default is `STARTUP_WAIT=7200` (2 h), and the ~106 GB download happens *inside*
   that window. Actual first boot took **5h40m**. Following the brief would have
   killed a healthy build.
3. **KV pool is 449,519 tokens** — not the 439,622, 986,275, or 264,867 quoted in
   different parts of the brief.
4. **`max_model_len` is 384,000**, not 262,144.
5. **The concurrency table is wrong.** `MAX_NUM_SEQS=1`; "~13 concurrent tasks at
   32K" is not a configuration that exists by default.
6. **Disk requirement is ~130 GiB**, not ≥250 GB.
7. **A2 does have a published quality number** — 60.8% MMLU-Pro, cited in A1's
   README. The brief claims A1 is the only build with one.
8. **The pruning rationale is inverted.** The brief says code generation is the
   most pruning-sensitive category. The recipe author's direct measurement of a
   REAP-216 build (same 15.6% rate) shows code retained at **94%** while **prose
   collapsed to 57%**. Code is the *least* sensitive axis. Good news for coding
   work; bad news if this model is ever pointed at prose.
9. **A1 has moved on.** `./start.sh` in the GaelicThunder repo now deploys a newer
   "Kalibrated" pack (100.08 GiB, 37.6 tok/s, 90% token-prob retention), not the
   MixedK pack the brief's A1 column describes. Use `PACK=mixedk ./start.sh` for
   the brief's exact A1.
10. **Tool calls work correctly** — the parser fix the brief describes applies to
    Ornith, not to this model.

---

## 10. Known issues / open items

| Item | Detail |
|---|---|
| ~11.2 GB stranded | Orphaned `.incomplete` files in `hf-hub/.../.cache/huggingface/download/`, owned by `root`, from a mid-download container restart. Needs `sudo find … -name '*.incomplete' -delete`. Harmless at 3.2 TB free. |
| HF write token live | The **running container** holds a `scope=write` token in its env. A read-only token is at `~/.cache/huggingface/token` and will be picked up on next restart. Revoke the write token — serving does not touch HF. |
| Port 8888 | Collides with the Ornith recipe. Only one can run on the Spark at a time. |
| IP is DHCP | `192.168.4.33` today. Use `zgx-15d5.local`. |
| SSH tunnel drops silently | Observed in practice. Presents as `ConnectionResetError` / connection refused and mimics a dead server. Use the keepalive flags in §1, or run the harness on the Spark. |
| No remote access | LAN/SSH only by design. Unreachable from outside the office network. |
| Wired NIC unused | `enP7s7` up at 1000 Mb/s, no IP. Spark currently on Wi-Fi. |
| `sudo` needs password | Blocks any automated task requiring root. |

---

## 11. Copy-paste starting point

```python
import json, urllib.request

BASE = "http://127.0.0.1:8888/v1"   # after: ssh -f -N -L 8888:127.0.0.1:8888 ZGX-Nano-G1n
MODEL = "deepseek-v4-flash-0731"

def ask(prompt, max_tokens=2048, thinking=False, temperature=0.0):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "chat_template_kwargs": {"thinking": thinking},
    }
    req = urllib.request.Request(
        BASE + "/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    body = json.loads(urllib.request.urlopen(req, timeout=1800).read().decode())
    choice = body["choices"][0]
    msg = choice["message"]
    return {
        "text": msg.get("content") or msg.get("reasoning_content") or msg.get("reasoning") or "",
        "truncated": choice["finish_reason"] == "length",   # ALWAYS check this
        "usage": body["usage"],
    }

r = ask("Write a Python function that reverses a linked list. Code only.")
assert not r["truncated"], "raise max_tokens or disable thinking"
print(r["text"])
```

**Rules for a coding-test harness against this server:**

1. `thinking: false` unless you specifically want reasoning traces.
2. Assert on `finish_reason` — silent truncation is the main failure mode.
3. Run sequentially. `MAX_NUM_SEQS=1`.
4. Budget ~50–55 s per 30K-context turn; a few seconds for short ones.
5. Salt prompts when benchmarking — prefix caching is on.
6. Execute generated code rather than eyeballing it. It passes when you do.

---

*Deployed and verified 2026-09-22. Build: 22:57Z → 04:37Z (5h40m), download-bound
at ~8 MB/s. Reload from disk is ~5 minutes.*
