---
date: 2026-09-25
type: reference
source: Kam, live board (Friday tab) 2026-09-25 09:29, verbatim — "Please create the handout document for the studio on how to use the Spark, how to connect, and all the other information that it will need."
written_by: Friday (laptop seat), from HANDOFF.md (measured 2026-09-22), the spark-kit (2026-09-23) and Friday's own smoke test and harness (2026-09-23)
audience: the Studio seat (Wednesday, Mac Studio) and any agent it briefs to use the Spark
status: live
---

# The Spark: a handout for the Studio

## BLUF

The **Spark** is an HP ZGX Nano (NVIDIA GB10, 121 GB unified memory) on the office LAN. It serves **DeepSeek V4 Flash** through an OpenAI-compatible API at `127.0.0.1:8888` **on the box itself**. You reach it with an **ssh tunnel**, and there's **no auth**, so never widen the bind.

- **It's fast and good at algorithmic code.** Measured: 37 tok/s decode, 1,030 tok/s prefill. First-round coding tests pass about 84–90%, and about 98% after one repair round. **It's weak on distributed or concurrent semantics.**
- **The run costs nothing. The brief is the whole cost.** Use the kit's method (§6).

**Before the Studio sends it anything, three things must be true:**

1. **Kam has ruled on client use (§0).** Today it is Datasec-only.
2. **The Studio has an ssh key on the box (§2).** This needs Kam's hands.
3. **The container is running.** Kam stopped it on 2026-09-24 at 13:58, and at 09:25 today `zgx-15d5.local` did not resolve from the laptop.

---

## §0 Whose box is it: read this first

- **The box's login is `datasec-rd`.** Wednesday's kit says it was commissioned "so that Datasec work can continue while travelling".
- **Kam ruled on 2026-09-23 that the Spark and the kit are Friday's.** Friday serves both clients, so Friday's standing default until Kam rules is: **the Spark takes Datasec work only.**
- **The Studio's work is Secuura plus general work.** Sending Secuura code to hardware provisioned for Datasec is exactly the cross-client leak hard rule 2 exists to prevent.
- **So the Studio sends it no Secuura code until Kam rules.** Friday has put this question to Kam as a card on the Friday tab (`spark-studio-client-scope`). **If he doesn't answer, the default is Datasec only.**
- **Client-neutral work is fine now:** benchmarks, harness smoke tests and synthetic tasks carry no client content.
- **Ornith is still the Studio's local model.** The Spark is a different box running a different model. The Spark also has an Ornith recipe on disk, but it uses **port 8888 too, so only one of the two can run on the Spark at a time.**

## §1 What it is (measured 2026-09-22 unless stated)

| | |
|---|---|
| Hardware | HP ZGX Nano G1n: NVIDIA GB10, 121 GB unified memory, driver 580.178.04, CUDA 13.0, 3.2 TB free |
| Hostname | `zgx-15d5` / **`zgx-15d5.local`** (mDNS). The IP `192.168.4.33` is DHCP and moves, so use the name |
| Network | LAN only, on Wi-Fi (the wired NIC is up but has no IP). **Not reachable from outside the office network** |
| User | `datasec-rd`, key-based. **`sudo` needs a password**, so no agent can do anything that needs root (including power-off) |
| Model | `deepseek-v4-flash-0731`: EXL3 3.0 bpw, REAP-pruned to 216/256 experts. Not the vision variant, not uncensored |
| Endpoint | `http://127.0.0.1:8888/v1` on the box. Model id `deepseek-v4-flash-0731`. No API key (send anything if a client insists) |
| Context | `max_model_len` **384,000** tokens (KV pool 449,519). A ~74K-token whole-file prompt fits; size costs time (about 70 s of prefill), not failure |
| Concurrency | **`MAX_NUM_SEQS=1`**: one request at a time, and others queue. Never fan out against it |
| Prefix caching | On. Salt your prompts when benchmarking |
| Recipe | `~/DeepSeek-v4-Flash-One-DGX-Spark` on the box. Image pinned by digest; weights on disk (~103 GB + ~99 GB checkpoint) |

## §2 Connecting from the Studio

**Step 1 — Kam's hands, once: give the Studio an ssh identity on the box.**

The laptop reaches the box through the alias `ZGX-Nano-G1n`. **NVIDIA Sync** writes it as an `Include` in `~/.ssh/config`. The Studio has no such alias. Friday has not checked the Studio's `~/.ssh`; this seat cannot read that machine. Two ways to fix it, and Kam chooses:

a. **Install NVIDIA Sync on the Studio and sign in** (the same way the laptop got the alias). *Recommended: it is how the working setup was made.*

b. Append the Studio's public key to `/home/datasec-rd/.ssh/authorized_keys` on the box. Then add to the Studio's `~/.ssh/config`:

```
Host ZGX-Nano-G1n
  HostName zgx-15d5.local
  User datasec-rd
  IdentityFile ~/.ssh/<the key you authorised>
```

**Step 2 — check you can reach it:**

```bash
ssh ZGX-Nano-G1n 'hostname; free -g | head -2'
```

**Step 3 — open the tunnel. Keep the keepalive flags; a plain `-f -N -L` drops silently:**

```bash
ssh -f -N -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
    -o ExitOnForwardFailure=yes -L 8888:127.0.0.1:8888 ZGX-Nano-G1n
curl -sf http://127.0.0.1:8888/health && echo OK
```

⚠ **On the Studio, check local port 8888 is free first** (`lsof -nP -iTCP:8888 -sTCP:LISTEN`). If Ornith or anything else holds it, forward to another local port (`-L 18888:127.0.0.1:8888`) and use that port in the base URL. **The Studio's port block is in `2_Project_Files/PORTS.md`**; pick from it and record your choice there.

**A dropped tunnel looks exactly like a dead server** (`ConnectionResetError`, connection refused). Before debugging the model:

```bash
pgrep -fl 'L 8888:127.0.0.1:8888' || echo "TUNNEL GONE — re-open it"
ssh ZGX-Nano-G1n 'curl -sf -m 5 http://127.0.0.1:8888/health && echo "server is fine"'
```

**For long runs, run the harness ON the box instead:** no tunnel, so nothing to drop.

```bash
scp harness.py ZGX-Nano-G1n:~/spark-eval/
ssh ZGX-Nano-G1n 'python3 ~/spark-eval/harness.py'
```

The tunnel does not survive a reboot of either machine. Put it on the Studio's own `PORTABILITY.md` / `doctor.sh` list if it becomes routine; the laptop's is PORTABILITY item 22.

## §3 Turning it on and off

The container is often **stopped to free the box's RAM**, as it has been since 2026-09-24 13:58. **Start it before you call the endpoint "broken".**

```bash
ssh ZGX-Nano-G1n
cd ~/DeepSeek-v4-Flash-One-DGX-Spark
./start.sh ps         # status
./run-a2.sh           # the relaunch wrapper used for this deployment (SERVING_HOST=127.0.0.1, STARTUP_WAIT=21600)
./start.sh stop       # stop; keeps weights and caches
./start.sh restart
```

- **Boot from disk takes about 5 minutes** to `/health`. The first-ever boot took 5 h 40 m because it downloaded the weights; that doesn't recur.
- **`docker logs` is nearly empty by design** (stdout is buffered). Don't read that as a hang. The real signals are:
  - `curl -sf http://127.0.0.1:8888/health` (authoritative)
  - `free -g` (about 118 GB used = loaded)
  - `nvidia-smi` (about 96% under load)
- **`(unhealthy)` during boot is cosmetic:** the healthcheck's start period expires while the model loads.
- **Only one of DeepSeek or the Spark's Ornith recipe can run at a time** (both use port 8888).
- **Power-off needs `sudo`, which no agent has.** Kam runs `ssh -t ZGX-Nano-G1n sudo shutdown -h now` himself.

## §4 Calling it: the one setting that wastes an afternoon

**Thinking is ON by default at `effort=max`.** With a normal budget the model spends it all reasoning and returns **empty `content`**, which looks exactly like failure.

Measured on one prompt:

| | Thinking on | Thinking off |
|---|---|---|
| Result | `finish_reason=length`, content empty, 53.7 s | 94 tokens, correct answer, 2.3 s |

**For coding, always send `"chat_template_kwargs": {"thinking": false}`, and always check `finish_reason`: `length` means truncated.**

```python
import json, urllib.request
BASE = "http://127.0.0.1:8888/v1"          # or your forwarded port
def ask(prompt, max_tokens=2048):
    body = {"model": "deepseek-v4-flash-0731", "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens, "temperature": 0, "chat_template_kwargs": {"thinking": False}}
    req = urllib.request.Request(BASE + "/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=1800).read())
    c = r["choices"][0]; m = c["message"]
    return {"text": m.get("content") or m.get("reasoning_content") or m.get("reasoning") or "",
            "truncated": c["finish_reason"] == "length", "usage": r["usage"]}
```

- **Tool calls arrive as a proper `tool_calls` field.** No parser workaround is needed.
- **Friday's smoke test (2026-09-23 12:52, thinking off): 3/3 passed.**
  - Code generated and executed: 5/5 cases.
  - A multi-turn revision: 3/3.
  - A tool call.
  - Script: `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/friday_smoke_test.py`.

## §5 What it is good and bad at (measured, 2026-09-22)

| Work | Use the Spark? |
|---|---|
| Data structures, parsers, algorithms, complexity-bound code | **Yes.** 14/14 first try on a persistent balanced BST and on a lazy segment tree |
| Exact numeric semantics | **Yes, with one repair round** (18/19 → 19/19) |
| Distributed or concurrent correctness, convergence, inheritance protocols | **No.** A CRDT stayed 7/12 and transitive priority inheritance stayed 10/12 through repair |

- **Repair fixes mechanics, not misconceptions.** A missing import, a tuple-unpacking error or a case miss gets fixed in one round. A behaviour that contradicts the model's prior (diff ordering, `-2^2`, a dependency map it declared and never populated) survives every round, even when the root cause is written out for it.
- **So spend one repair round and never a third.** Kam's counter for this box (2026-09-23): **the original brief plus ONE rebrief, then the ticket goes to Opus 5.5 in the cloud.** It's a counter, not a judgement; don't reason past it.
- **It takes shortcuts the spec allows.** Asked for a regex engine "in pure Python", it imported `re`. Name forbidden modules explicitly.
- **Against Ornith 1.5 35B on the same 10 tasks:** similar first-round scores (84% vs 82%), but DeepSeek gains +22 tests from feedback while Ornith gains none. For a loop that iterates on test failures, that difference matters most.

## §6 How to run work through it: the method (the kit, adopted)

**The kit is at `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/spark-kit_2026-09-23/`.** Read `02_FOR_THE_COORDINATOR.md` before the first task of a session. Where the kit says "Tuesday", read "whoever runs the box". The rules that decide outcomes:

1. **Never queue a task built from a bare ticket description.** Write a brief with `03_BRIEF_TEMPLATE.md`, with every heading filled. A runner that falls back to the ticket text has refused, not succeeded.
2. **Selection predicate, checked at source:**
   - one product file
   - the ticket spells out the fix shape ("decide whether…" is a card for a human, not a task)
   - a runnable in-process test nearby to copy
   - not an auth, token, credential or security surface
   - a test runner the checker can actually run

   Expect most of a backlog to fail this; a thin pool is normal.
3. **Brief shape:**
   - Exact edits: line number, the line's CURRENT text at the tip, and the new text.
   - At most 3 edit points; otherwise split the task.
   - What must NOT change, named.
   - Every premise with the line it was read at.
   - An UNMEASURED section.
4. **The checker's six clauses; a PASS means nothing unless all six held:**
   1. Applies at a known commit, with the apply MODE recorded (strict or recount), **plus an anchor check** (see failure mode 9 below).
   2. Added lines byte-identical to the brief.
   3. The touched-file set is exactly what the brief named.
   4. The new test goes RED on a deliberate break and GREEN when restored.
   5. The rest of the suite is no worse, with before-and-after counts.
   6. Every assertion's output is kept.
5. **Smoke-test the harness first.** Run a trivial known change, then two deliberate breaks: a wrong expected line must fail clause 2, and a non-existent line number must fail clause 1. A harness that can't fail has told you nothing.
6. **Reading the diff against the brief can't be delegated. A PASS is a candidate, never a merge.** The model holds no identity and raises nothing; merges go through the normal QA gate and a signed GO.
7. **Every FAIL is classified (model, harness or brief) and fixed where it lives.** Every prompt rule gets a checker twin that can refuse.

**Friday's working harness (Python stdlib only; in this repo, so the Studio has it after a pull), at `2_Project_Files/friday/spark/`:**

- `spark_run.py --brief <brief.md> --repo <checkout> --out <run dir>` sends ONE brief with thinking OFF.
  - It **refuses** a brief with no `Tip:`, a repo not at the tip, a missing `File:`, or an input over 300K tokens.
  - Exit codes: 0 = one diff extracted (a candidate), 2 = refused, 3 = not exactly one diff, 4 = truncated or empty, 5 = transport error.
- `spark_check.py --brief-json <expect.json> --diff <file.diff> --repo <checkout> --out <evidence dir>` asserts the six clauses in a fresh clone. It never modifies the source.
  - Verdicts: PASS / FAIL / INCOMPLETE.
- `tests/selftest.py` and `tests/unfenced_arms.py` are the harness's own arms.
- `briefs/SMOKE-arms-path.*` is the smoke brief.
- The runs are in `runs/2026-09-23_smoke/`.

**Two failure modes found on THIS model, beyond the kit's list (kit file 04, §8–9):**

- **8.** It sometimes omits the code fences around a correct diff. The runner accepts an unfenced answer only if it is pure unified-diff grammar.
- **9.** `git apply` relocates a hunk by context, so a wrong line number still "applied strict". The checker now asserts every hunk's old side sits at exactly its header's start line.

## §7 Known issues on the box (from HANDOFF.md §10; not re-measured today)

- About 11 GB of orphaned `.incomplete` download files, owned by root. Harmless at 3.2 TB free; removing them needs `sudo`, which is Kam's.
- **The container env once held a write-scoped Hugging Face token.** A read-only token is in `~/.cache/huggingface/token` and is picked up on restart. Whether the write token was revoked is **unmeasured** by Friday.
- No remote access (LAN or ssh only, by design). DHCP IP. Wi-Fi rather than the wired NIC.

## §8 Owner and contacts

- **The loop's owner is Friday** (Kam, 2026-09-23). The claim is in `wed_claim.sh`: "Spark … local-model loop".
- **If the Studio starts using the box, claim it too,** so two seats never queue at a one-request server without knowing. Mail Friday (`friday-laptop-agent@agentmail.to`) before a long run; Friday does the same.
- **Anything needing the box's power, `sudo`, or a client-scope ruling is Kam's.**
