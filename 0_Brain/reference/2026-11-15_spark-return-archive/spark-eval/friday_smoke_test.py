import json, urllib.request, time, random
BASE="http://127.0.0.1:8888/v1"; M="deepseek-v4-flash-0731"
def call(payload):
    t=time.time(); req=urllib.request.Request(BASE+"/chat/completions",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    b=json.loads(urllib.request.urlopen(req,timeout=600).read()); return b, time.time()-t
def code_of(txt): return txt.split("```python")[1].split("```")[0] if "```python" in txt else txt
salt=random.randint(1,10**9)
p={"model":M,"max_tokens":1024,"temperature":0,"chat_template_kwargs":{"thinking":False},
   "messages":[{"role":"user","content":f"(run {salt}) Write a Python function parse_duration(s) that converts strings like '1h30m', '45s', '2h', '10m' to total seconds. Reply with ONLY the code in one ```python block, no tests."}]}
b,dt=call(p); c=b["choices"][0]; txt=c["message"].get("content") or ""
print(f"T1 finish={c['finish_reason']} tokens={b['usage']['completion_tokens']} {dt:.1f}s")
ns={}; exec(code_of(txt),ns); f=ns["parse_duration"]
cases={"1h30m":5400,"45s":45,"2h":7200,"10m":600,"1h1m1s":3661}
res={k:f(k)==v for k,v in cases.items()}; print("T1 exec:",res,"PASS" if all(res.values()) else "FAIL")
p["messages"]+=[{"role":"assistant","content":txt},{"role":"user","content":"Now make it raise ValueError on an empty string or an unknown unit like '5x'. Reply with ONLY the full code block."}]
b,dt=call(p); c=b["choices"][0]; txt2=c["message"].get("content") or ""
ns={}; exec(code_of(txt2),ns); f=ns["parse_duration"]
def raises(x):
    try: f(x); return False
    except ValueError: return True
r2={"1h30m still 5400":f("1h30m")==5400,"empty raises":raises(""),"5x raises":raises("5x")}
print(f"T2 finish={c['finish_reason']} {dt:.1f}s exec:",r2,"PASS" if all(r2.values()) else "FAIL")
p3={"model":M,"max_tokens":512,"temperature":0,"chat_template_kwargs":{"thinking":False},
 "messages":[{"role":"user","content":"What's the weather in Sydney? Use the tool."}],
 "tools":[{"type":"function","function":{"name":"get_weather","description":"Get weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}
b,dt=call(p3); c=b["choices"][0]; tc=c["message"].get("tool_calls") or []
calls=[(t['function']['name'],t['function']['arguments']) for t in tc]
print(f"T3 finish={c['finish_reason']} {dt:.1f}s tool_calls={calls}","PASS" if calls and calls[0][0]=="get_weather" else "FAIL")
