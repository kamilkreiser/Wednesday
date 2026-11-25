import os,sys,time,subprocess,json
b,d=sys.argv[1],sys.argv[2]
env={"PATH":"/usr/bin:/bin","HOME":d+"/h","TMPDIR":d+"/t"}; os.makedirs(env["HOME"]); os.makedirs(env["TMPDIR"])
p=subprocess.Popen([b+"/coagentd","--data-dir",d+"/k","--coagent",b+"/coagent","--keep-relay-identity","--idle-exit-secs","60"],env=env,stdout=subprocess.DEVNULL,stderr=open(d+"/err","wb"))
def ctl(c):
    r=subprocess.run([b+"/coagentd","ctl","--data-dir",d+"/k",json.dumps({"v":1,"id":1,"cmd":c})],env=env,capture_output=True)
    return r.stdout
for _ in range(100):
    if ctl("status"): break
    time.sleep(0.1)
print(ctl("invite")[:80]); time.sleep(1)
print(os.listdir(d+"/k"))
p.terminate(); print("exit",p.wait(20))
